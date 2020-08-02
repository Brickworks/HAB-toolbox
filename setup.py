import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="HAB-Toolbox",  # Replace with your own username
    version="0.0.1",
    author="Brickworks",
    description="Software to assist in mechanics calculations, and simulations"
    " of high altitude balloon payloads",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Brickworks/HAB-toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'ambiance',
        'Click',
        'matplotlib',
    ],
    extras_require={
        'test': [
            'pytest',
        ]
    },
)
