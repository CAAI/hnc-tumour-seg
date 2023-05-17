'''
Purpose
Calculate biomarkers based on PET-CT and MTV delineation inputs. 
'''

from MEDIcaTe.utilities import get_nii_image_to_numpy
from MEDIcaTe.nii_resampling import find_pix_dim, resample_nii_to_voxel_size
import torchio as tio
import raster_geometry as rg
import numpy as np
from scipy.ndimage import label, generate_binary_structure
import collections
from MEDIcaTe.file_folder_ops import basename


def region_mean(pet, lab):
    region_mean = pet[lab == 1].mean()
    return region_mean


def region_max(pet, lab):
    region_max = pet[lab == 1].max()
    return region_max


def sphere(shape, radius, position):
    """Generate an n-dimensional spherical mask."""
    # assume shape and position have the same length and contain ints
    # the units are pixels / voxels (px for short)
    # radius is a int or float in px
    assert len(position) == len(shape)
    #n = len(shape)
    semisizes = (radius,) * len(shape)

    # genereate the grid for the support points
    # centered at the position indicated by position
    grid = [slice(-x0, dim - x0) for x0, dim in zip(position, shape)]
    position = np.ogrid[grid]
    # calculate the distance of all points from `position` center
    # scaled by the radius
    arr = np.zeros(shape, dtype=float)
    for x_i, semisize in zip(position, semisizes):
        # this can be generalized for exponent != 2
        # in which case `(x_i / semisize)`
        # would become `np.abs(x_i / semisize)`
        arr += (x_i / semisize) ** 2

    # the inner part of the sphere will have distance below or equal to 1
    return arr <= 1.0

def region_peak(image_nii, label_nii):
    # resample to 1x1x1
    transform = tio.Resample(1)
    lab = tio.LabelMap(label_nii)
    image = tio.ScalarImage(image_nii)
    label_transformed = transform(lab)
    image_transformed = transform(image)
    image_t_np = np.squeeze(image_transformed.numpy())
    label_t_np = np.squeeze(label_transformed.numpy())
    lt_size = label_t_np.shape
    if lt_size != image_t_np.shape:
        print("WARNING: Sizes do not match. Check what is up")
        print(f'Case: {basename(label_nii)}')
        print(f'image_nii = {image_nii}')
        print(f'label_nii = {label_nii}')
        print(f'label_t_np.shape = {label_t_np.shape}')
        print(f'image_t_np.shape = {image_t_np.shape}')

    image_masked = image_t_np*label_t_np
    location_max = np.where(image_masked == np.amax(image_masked))
    location_max_idx = (location_max[0][0], location_max[1][0], location_max[2][0])
    sphere_label = sphere(lt_size, 6.2, location_max_idx)

    region_peak = image_t_np[sphere_label].mean()

    return region_peak

def n_objects_in_label(lab):
    s = generate_binary_structure(3,3)
    labeled_array, num_features = label(lab, s)
    return num_features


def region_volume(lab, label_nii):
    pix_dim = find_pix_dim(label_nii)
    n_voxels = len(lab[lab == 1])
    volume = n_voxels * (pix_dim[0] * pix_dim[1] * pix_dim[2]) / 1000
    return volume


def get_all_biomarkers(label_nii, pet_nii):
    pet = get_nii_image_to_numpy(pet_nii)
    lab = get_nii_image_to_numpy(label_nii)

    has_ones = np.any(lab) # only run this part if something was detected

    if has_ones:
        n_objects = n_objects_in_label(lab)
        mtv = region_volume(lab, label_nii)
        suv_peak = 'debug later' #region_peak(pet_nii, label_nii)
        suv_mean = region_mean(pet, lab)
        suv_max = region_max(pet,lab)
        tlg = mtv*suv_mean
    else:
        n_objects = 'no label detected on this case'
        mtv = 'no label detected on this case'
        suv_peak = 'no label detected on this case'
        suv_mean = 'no label detected on this case'
        suv_max = 'no label detected on this case'
        tlg = 'no label detected on this case'

    biomarkers = collections.namedtuple("biomarkers", ["n_objects", "mtv", "suv_peak", "suv_mean", "suv_max", "tlg"])

    return biomarkers(n_objects=n_objects, mtv=mtv, suv_peak=suv_peak, suv_mean=suv_mean, suv_max=suv_max, tlg=tlg)

if __name__ == '__main__':
    pet_nii = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/images/HNC03_002_0001.nii.gz'
    label_nii = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_doctor_study/md_renamed/HNC03_002.nii.gz'

    pet = get_nii_image_to_numpy(pet_nii)
    lab = get_nii_image_to_numpy(label_nii)

    n_objects = n_objects_in_label(lab)
    suv_peak = region_peak(pet_nii, label_nii)
    mtv = region_volume(lab, label_nii)
    suv_mean = region_mean(pet, lab)
    suv_max = region_max(pet,lab)
    tlg = mtv*suv_mean

    print(f'n_objects = {n_objects}')
    print(f'mtv = {mtv} cm^3')
    print(f'suv_peak = {suv_peak}')
    print(f'suv_mean = {suv_mean}')
    print(f'suv_max = {suv_max}')
    print(f'tlg = {tlg}')
