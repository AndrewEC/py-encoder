from typing import Dict, Tuple
from pathlib import Path
import os
import re

import click
import yaml

from encoder.encode import encode_string, encode_bytes
from encoder.decode import decode_to_string, decode_to_bytes
from encoder.generator import generate_dictionary


_DICTIONARY_FOLDER = Path(__file__).parent.joinpath('dictionaries').absolute()


def _file_name_to_option(file_name: str) -> str:
    index = file_name.rfind('.')
    file_name = file_name[:index]
    components = re.findall('[A-Z][^A-Z]*', file_name)
    return '-'.join([component.lower() for component in components])


def _build_dictionary_list() -> Dict[str, str]:
    return {_file_name_to_option(file_name): file_name for file_name in os.listdir(_DICTIONARY_FOLDER)}


def _read_dictionary_from_file(dictionary: str) -> Tuple[str, Dict[str, str]]:
    dictionary_file_name = _AVAILABLE_DICTIONARIES[dictionary]
    dictionary_file = _DICTIONARY_FOLDER.joinpath(dictionary_file_name).absolute()
    with open(dictionary_file, 'r') as file:
        contents = yaml.safe_load(file)
        return contents['padding'], contents['mappings']


_AVAILABLE_DICTIONARIES = _build_dictionary_list()


@click.group('encode')
def encode_group():
    pass


@click.command('string')
@click.argument('value')
@click.option('--dictionary', '-d', type=click.Choice(list(_AVAILABLE_DICTIONARIES.keys())), default='default')
def encode_string_command(value: str, dictionary: str):
    padding, mappings = _read_dictionary_from_file(dictionary)
    print(encode_string(value, mappings, padding))


@click.command('file')
@click.argument('file')
@click.option('--dictionary', '-d', type=click.Choice(list(_AVAILABLE_DICTIONARIES.keys())), default='default')
def encode_file_command(file: str, dictionary: str):
    file_path = Path(file)
    if not file_path.is_file():
        raise Exception('The provided path does not exist or does not point to a file.')
    with open(file_path, 'rb') as file:
        padding, mappings = _read_dictionary_from_file(dictionary)
        encoded_value = encode_bytes(file.read(), mappings, padding)
        print(encoded_value)


encode_group.add_command(encode_string_command)
encode_group.add_command(encode_file_command)


@click.group('decode')
def decode_group():
    pass


@click.command('string')
@click.argument('value')
@click.option('--dictionary', '-d', type=click.Choice(list(_AVAILABLE_DICTIONARIES.keys())), default='default')
def decode_string_command(value: str, dictionary: str):
    padding, mappings = _read_dictionary_from_file(dictionary)
    print(decode_to_string(value, mappings, padding))


@click.command('file')
@click.argument('value')
@click.argument('output')
@click.option('--dictionary', '-d', type=click.Choice(list(_AVAILABLE_DICTIONARIES.keys())), default='default')
def decode_file_command(value: str, output: str, dictionary: str):
    padding, mappings = _read_dictionary_from_file(dictionary)
    decoded = decode_to_bytes(value, mappings, padding)
    with open(output, 'wb') as file:
        file.write(decoded)


decode_group.add_command(decode_file_command)
decode_group.add_command(decode_string_command)


@click.command('generate')
@click.argument('binary_key_length', type=int)
@click.argument('encoded_character_length', type=int)
@click.option('--padding-character', '-p', default='=')
@click.option('--outfile', '-o')
def generate_command(binary_key_length: int, encoded_character_length: int, padding_character: str, outfile: str):
    generated = generate_dictionary(binary_key_length, encoded_character_length, padding_character)
    dictionary = {'padding': padding_character, 'mappings': generated}
    if outfile is None:
        return print(yaml.safe_dump(dictionary))
    with open(outfile, 'w') as file:
        yaml.safe_dump(dictionary, file)


@click.group()
def main():
    pass


main.add_command(encode_group)
main.add_command(decode_group)
main.add_command(generate_command)


if __name__ == '__main__':
    main()
