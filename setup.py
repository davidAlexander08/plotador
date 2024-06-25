from setuptools import setup, find_packages

long_description = "plotador"

requirements = []
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()


setup(
    name="plotador",
    version="0.0.0",
    author="David Alexander",
    author_email="david.tbsilva@gmail.com",
    description="plotador",
    long_description=long_description,
    install_requires=requirements,
    packages=find_packages(),
    py_modules=["main", "apps"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        plotador=main:main
    """,
)
