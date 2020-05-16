import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reptile",
    version="1.0.2",
    author="Alessandro",
    url="https://github.com/alessandrosp/reptile",
    description=(
        "Reptile is a command-line interface for Python. Specifically, "
        "Reptile helps with producing interactive REPL-like software."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=(
        "prompt-toolkit, cli, command-line, commandline, "
        "command-line-interface, python-inquiry, inquirer, "
        "reptile, REPL, prompt"
    ),
    install_requires=["prompt-toolkit>=3.0.5", "pygments>=2.6.1"],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
)
