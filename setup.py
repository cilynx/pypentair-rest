from setuptools import find_packages, setup

setup(
    name='pypentair-rest',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask-restful',
        'pypentair'
    ],
)
