from setuptools import find_packages, setup

setup(
    name="datajob",
    version="0.0.2",
    plat_name="",
    packages=[".", *find_packages(
        exclude=[
            "tests"
        ]
    )],
    package_data={".":["*.py"]},
)