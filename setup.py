import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='MEDIcaTe',
    version='0.0.8',
    author='David Gergely Kovacs Petersen',
    author_email='dkov0001@regionh.dk',
    description='Image processing utilities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/CAAI/hnc-tumour-seg/MEDIcaTe',
    project_urls={
        "Bug Tracker": "https://github.com/CAAI/hnc-tumour-seg/MEDIcaTe/issues"
    },
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        "nibabel",
        "matplotlib",
        "numpy",
        "pillow",
        "pandas",
        "mycolorpy",
        "argparse",
        "SimpleITK",
        "scipy",
        "torchio"
    ],
    entry_points={
        'console_scripts': [
            'hello=MEDIcaTe.extrafunctions:hello',
            'my_cli=MEDIcaTe.extrafunctions:main',
            'add=MEDIcaTe.extrafunctions:addparser',
            'dice_haus=MEDIcaTe.calculate_dice_haus:main',
            'visualization=MEDIcaTe.visualization:Entry_Point',
            'test=test:Entry_Point'
        ],
    },
)
