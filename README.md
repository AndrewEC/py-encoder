# py-encoder
A POC python package for creating a customizable Base64 encoder and decoder.

## Playground
First run the powershell script `CreateVenv.ps1` from the root of this project then run the run.py script:
`python run.py --help`.

## Encoding Dictionary
The available dictionaries for encoding and decoding are available in the `dictionaries` directory. You can add more
custom or generated dictionaries by creating a new yaml file and adding it to the `dictionaries` folder. Once added
you can run a command like `python run.py encode string --help` and get a list of available dictionaries that can
be supplied with the `--dictionary` argument.

## Test Scripts
To execute the unit test suite change to the `package` directory and run the command:
`python -m unittest encoder.tests._run_all`