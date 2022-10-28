import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bunker",
    version="0.1.0",
    author="nexryai",
    author_email="gnomer@tuta.io",
    description="Backup server data to S3 object storage safety.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.sda1.net/nexryai/bunker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache2.0 License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['bunker = bunker.bunker:main']
    },
    python_requires='>=3.7',
)
