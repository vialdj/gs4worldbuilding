from setuptools import setup, find_packages

setup(
    name='gs4worldbuilding',
    version='0.0.0',
    packages=find_packages(include=['gs4worldbuilding', 'gs4worldbuilding.*']),
    install_requires=[
        'numpy>=1.20.2',
        'scipy>=1.6.2',
        'ordered_enum>=0.0.6',
        'astropy>=4.3.1'
    ]
)