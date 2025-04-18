from typing import List, Tuple, Dict
from pathlib import Path
import os
from getpass import getpass

import click
import yaml

from encoder import encode_string, encode_bytes, decode_to_bytes, decode_to_string, generate_encoding_dictionary


_DICTIONARY_FOLDER = Path(__file__).parent.joinpath('dictionaries').absolute()
_DICTIONARY_NAME_TEMPLATE = '{}.yml'


def _remove_extension(file_name: str) -> str:
    return Path(file_name).stem


def _build_dictionary_list() -> List[str]:
    return list(map(_remove_extension, os.listdir(_DICTIONARY_FOLDER)))


def _read_dictionary_from_file(dictionary: str) -> Tuple[str, Dict[str, str]]:
    dictionary_file_name = _DICTIONARY_NAME_TEMPLATE.format(dictionary)
    dictionary_file = _DICTIONARY_FOLDER.joinpath(dictionary_file_name).absolute()
    with open(dictionary_file, 'r') as file:
        contents = yaml.safe_load(file)
        return contents['padding'], contents['mappings']


_AVAILABLE_DICTIONARIES = _build_dictionary_list()


@click.group('encode')
def encode_group():
    pass


def _get_value_to_encode(value: str) -> str:
    return getpass('Enter string to encode: ') if value == '?' else value


@click.command('string')
@click.argument('value')
@click.option('--dictionary', '-d', type=click.Choice(list(_AVAILABLE_DICTIONARIES)), default='default')
def encode_string_command(value: str, dictionary: str):
    padding, mappings = _read_dictionary_from_file(dictionary)
    print(encode_string(_get_value_to_encode(value), mappings, padding))


@click.command('file')
@click.argument('file')
@click.option('--dictionary', '-d', type=click.Choice(list(_AVAILABLE_DICTIONARIES)), default='default')
def encode_file_command(file: str, dictionary: str):
    file_path = Path(file)
    if not file_path.is_file():
        raise Exception('The provided path does not exist or does not point to a file.')
    with open(file_path, 'rb') as file:
        padding, mappings = _read_dictionary_from_file(dictionary)
        encoded_value = encode_bytes(file.read(), mappings, padding)
        print(encoded_value)


@click.group('decode')
def decode_group():
    pass


@click.command('string')
@click.argument('value')
@click.option('--dictionary', '-d', type=click.Choice(list(_AVAILABLE_DICTIONARIES)), default='default')
def decode_string_command(value: str, dictionary: str):
    padding, mappings = _read_dictionary_from_file(dictionary)
    print(decode_to_string(value, mappings, padding))


@click.command('file')
@click.argument('file_path')
@click.argument('output')
@click.option('--dictionary', '-d', type=click.Choice(list(_AVAILABLE_DICTIONARIES)), default='default')
def decode_file_command(file_path: str, output: str, dictionary: str):
    padding, mappings = _read_dictionary_from_file(dictionary)
    with open(file_path, 'r') as file:
        file_content = ''.join([line.strip() for line in file.readlines()])
    decoded = decode_to_bytes(file_content, mappings, padding)
    with open(output, 'wb') as file:
        file.write(decoded)


@click.command('generate')
@click.argument('binary_key_length', type=int)
@click.argument('encoded_character_length', type=int)
@click.option('--padding-character', '-p', default='=')
@click.option('--outfile', '-o')
def generate_command(binary_key_length: int, encoded_character_length: int, padding_character: str, outfile: str):
    generated = generate_encoding_dictionary(binary_key_length, encoded_character_length, padding_character)
    generated_dict = dict(generated)
    if outfile is None:
        return print(yaml.safe_dump(generated_dict))
    with open(outfile, 'w') as file:
        yaml.safe_dump(generated_dict, file)


@click.group()
def main():
    pass


encode_group.add_command(encode_string_command)
encode_group.add_command(encode_file_command)

decode_group.add_command(decode_file_command)
decode_group.add_command(decode_string_command)

main.add_command(encode_group)
main.add_command(decode_group)
main.add_command(generate_command)


if __name__ == '__main__':
    main()
