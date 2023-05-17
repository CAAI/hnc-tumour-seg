class hnc_tumor_model(SegmentationModelBase):
    def __init__(self) -> None:
        super().__init__(
            azure_dataset_id=None,
            # Adjust this to where your dataset_folder is on your local box
            local_dataset="/homes/kovacs/project_data/hnc-auto-contouring/inner-eye",
            image_channels=["ct","pet"],
            ground_truth_ids=["heart", "lung"],
            # Segmentation architecture
            architecture="UNet3D",
            feature_channels=[32],
            # Size of patches that are used for training, as (z, y, x) tuple
            crop_size=(64, 224, 224),
            # Reduce this if you see GPU out of memory errors
            train_batch_size=8,
            # Size of patches that are used when evaluating the model
            test_crop_size=(128, 512, 512),
            inference_stride_size=(64, 256, 256),
            # Use CT Window and Level as image pre-processing
            norm_method=PhotometricNormalizationMethod.CtWindow,
            level=40,
            window=400,
            # Learning rate settings
            l_rate=1e-3,
            min_l_rate=1e-5,
            l_rate_polynomial_gamma=0.9,
            num_epochs=120,
            )