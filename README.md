# py-encoder
A POC python package for creating a customizable Base64 encoder and decoder.

## Cloning
To clone the project and the required submodules run:
> git clone --recurse-submodules https://github.com/AndrewEC/py-encoder.git

## Playground
First run the powershell script `RunScript.ps1 All` from the root of this project then run the run.py script:
`python run.py --help`.

## Encoding Dictionary
The available dictionaries for encoding and decoding are available in the `dictionaries` directory. You can add more
custom or generated dictionaries by creating a new yaml file and adding it to the `dictionaries` folder. Once added
you can run a command like `python run.py encode string --help` and get a list of available dictionaries that can
be supplied with the `--dictionary` argument.

## Quality Metrics
To run the unit and integration tests simply run the `RunScript.ps1 All` script the run the build script via:
`python build.py`

This build script, in addition to the running the unit and mutation tests, will also generate coverage reports,
install required dependencies, ensure a proper virtual environment is active, generate Sphinx docs, and run Flake8.

Separate mutation and unit test coverage reports will be generated at the following locations:
* Unit Tests - `html/index.html`
* Mutation Tests - `html/index.html`