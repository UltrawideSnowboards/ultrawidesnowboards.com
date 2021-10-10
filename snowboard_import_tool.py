#!/usr/bin/env python3

import json
import re
from pathlib import Path
from typing import Callable, Dict, List, Optional

import requests

DATA_FILE = '_data/snowboards.json'


def read_data_file() -> Dict:
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def write_data_file(data) -> None:
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def check_url_is_valid(url: Optional[str]) -> Optional[str]:
    if url is None:  # Allow bypassing
        return None

    request = requests.get(url)
    if request.status_code != 200:
        return f'URL is not valid (status code {request.status_code})'
    else:
        return None


def download_picture(url: str, destination: Path) -> None:
    picture_request = requests.get(url)
    if picture_request.status_code != 200:
        raise Exception(f'Failed to download picture: {picture_request.text}')
    with destination.open('wb') as f:
        f.write(picture_request.content)


def menu(items: List[str], prompt: str = 'Please select one of the following:') -> int:
    print(prompt)
    for i, item in enumerate(items):
        print(f'    {i}) {item}')
    while True:
        try:
            result = int(input('-> '))
        except ValueError:
            print('Must input an int')
            continue

        if result >= 0 and result < len(items):
            return result
        else:
            print(f'Must chose from 0 to {len(items) - 1}')


def get_input(prompt: str, check_function: Callable[[Optional[str]], Optional[str]] = None) -> Optional[str]:
    result_str: Optional[str] = input(prompt)
    if result_str == '':
        result_str = None
    if check_function is None:
        return result_str
    check_result = check_function(result_str)
    if check_result is None:
        return result_str
    else:
        print(check_result)
        return(get_input(prompt, check_function))


def get_input_float(prompt: str) -> Optional[float]:
    result = get_input(prompt, check_float)
    try:
        return float(result)
    except ValueError:
        return None


def check_short_name(short_name: Optional[str]) -> Optional[str]:
    if short_name is None:
        return 'Can not be an empty string'
    if not re.match('[a-z]+', short_name):
        return 'Must be a lowercase name'
    elif Path(f'assets/img/vendors/2021/{short_name}').exists():
        return 'Short name already exists'
    else:
        return None


def check_float(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    try:
        float(value)
        return None
    except ValueError:
        return 'Must be a float'


def add_brand():
    print('Adding new brand.')
    short_name = get_input('Short Name: ', check_short_name)
    image_dir = Path(f'assets/img/vendors/2021/{short_name}')
    image_dir.mkdir()

    human_name = get_input('Human Name: ')
    # TODO: figure out where to insert the brand in the brand list

    url = get_input('URL: ', check_url_is_valid)
    logo_url = get_input('Logo URL: ', check_url_is_valid)

    if logo_url is not None:
        extension_tuple = logo_url.rsplit('.', 1)
        if len(extension_tuple) != 2:
            raise Exception('ERROR: logo URL does not have an extension')

        image_name = f'logo.{extension_tuple[1]}'
        download_picture(logo_url, image_dir / image_name)
    else:
        image_name = 'logo.FAKE'

    data = read_data_file()
    data['brands'].append({
        'short_name': short_name,
        'name': human_name,
        'url': url,
        'logo': f'2021/{short_name}/{image_name}',
        'solid': {
            'notes': None,
            'maxmimum': None,
            'boards': []
        },
        'splitboards': {
            'notes': None,
            'maxmimum': None,
            'boards': []
        }
    })

    write_data_file(data)
    print(f'You have added {short_name}')


def add_snowboard():
    data = read_data_file()
    brand_names = [i['name'] for i in data['brands']]

    brand_index = menu(brand_names, 'Select brand name:')
    brand_short_name = data['brands'][brand_index]['short_name']
    short_name = get_input('Board short name: ', check_short_name)

    image_url = get_input('Image URL: ', check_url_is_valid)
    if image_url is not None:
        extension_tuple = image_url.rsplit('.', 1)
        if len(extension_tuple) != 2:
            raise Exception('ERROR: logo URL does not have an extension')

        image_name = f'{short_name}.{extension_tuple[1]}'
        image_dir = Path(f'assets/img/vendors/2021/{brand_short_name}')
        download_picture(image_url, image_dir / image_name)
    else:
        image_name = f'{short_name}.FAKE'

    url = get_input('URL: ', check_url_is_valid)

    snowboard_types = ['solid', 'splitboards']
    board_type = snowboard_types[menu(snowboard_types, 'Select the type of snowboard')]

    human_name = get_input('Model Human Name: ')
    length = get_input_float('Length (cm): ')
    waist_width = get_input_float('Waist width (cm): ')

    side_cut = get_input('Side cut (m): ')
    try:
        side_cut = float(side_cut)
    except ValueError:
        pass

    stance = get_input('Stance: ')
    setback = get_input('Setback: ')
    price = get_input('Price: ')
    profile = get_input('Profile: ')
    category = get_input('Category: ')
    shape = get_input('Shape: ')

    data['brands'][brand_index][board_type]['boards'].append({
        'image': f'2021/{brand_short_name}/{image_name}',
        'short_name': short_name,
        'name': human_name,
        'length': length,
        'waist_width': waist_width,
        'side_cut': side_cut,
        'stance': stance,
        'setback': setback,
        'price': price,
        'url': url,
        'profile': profile,
        'category': category,
        'shape': shape
    })

    write_data_file(data)
    print(f'You have added {short_name}')


def main():
    print('Welcome to the snowboard import program')
    print('Please select an option:')

    menu_items = ['Add Brand', 'Add Snowboard']

    selected = menu(menu_items)

    if selected == 0:
        add_brand()
    elif selected == 1:
        add_snowboard()


if __name__ == '__main__':
    main()
