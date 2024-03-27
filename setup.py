from setuptools import setup, find_packages

long_description = "graficador-newave"

requirements = []
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()


setup(
    name="graficador-newave",
    version="0.0.0",
    author="David Alexander",
    author_email="david.tbsilva@gmail.com",
    description="graficador-newave",
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
        graficador-newave=main:main
    """,
)
