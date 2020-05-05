import setuptools

setuptools.setup(
    name="reptile",
    version="1.0",
    author="Alessandro",
    url="https://github.com/alessandrosp/reptile",
    description=(
        "Reptile is a command-line interface for Python. Specifically, "
        "Reptile helps with producing interactive REPL-like software."
    ),
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
)
