from setuptools import setup, find_packages

setup(
    name='camera_service',
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'numpy',
        'opencv-python-headless',
        'requests',        
    ],
)


