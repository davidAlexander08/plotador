from setuptools import setup, find_packages

long_description = "cpamp"

requirements = []
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()


setup(
    name="cpamp",
    version="1.0.0",
    author="Rogerio Alves",
    author_email="rogerioalves.ee@gmail.com",
    description="cpamp",
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
        cpamp=main:main
    """,
)
