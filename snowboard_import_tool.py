#!/usr/bin/env python3
import curses
import json
import re
from curses import panel, wrapper
from pathlib import Path
from typing import Callable, Dict, List, Optional

import requests

DATA_FILE = '_data/snowboards.json'


def read_data_file() -> Dict:
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def write_data_file(data) -> None:
    with open(DATA_FILE, 'w') as f:
        json.dump(f, data, indent=4, sort_keys=True)


def check_url_is_valid(url: str) -> Optional[str]:
    request = requests.get(url)
    if request.status_code != 200:
        return f'URL is not valid (status code {request.status_code}'
    else:
        return None




def download_picture(url: str, destination: Path) -> None:
    picture_request = requests.get(url)
    if picture_request.status_code != 200:
        raise Exception(f'Failed to download picture: {picture_request.text}')
    with destination.open('wb') as f:
        f.write(picture_request.content)


def menu(items: List[str], stdscreen) -> int:
    # Adapted from https://stackoverflow.com/a/14205494
    window = stdscreen.subwin(0, 0)
    window.keypad(1)
    menu_panel = panel.new_panel(window)
    menu_panel.hide()
    panel.update_panels()

    position = 0

    menu_panel.top()
    menu_panel.show()
    window.clear()

    while True:
        window.refresh()
        curses.doupdate()
        for index, item in enumerate(items):
            if index == position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            msg = "%d. %s" % (index, item)
            window.addstr(1 + index, 1, msg, mode)

        key = window.getch()

        if key in [curses.KEY_ENTER, ord("\n")]:
            if position == len(items) - 1:
                break
            else:
                return position

        elif key == curses.KEY_UP:
            position -= 1
            if position < 0:
                position = 0

        elif key == curses.KEY_DOWN:
            position += 1
            if position >= len(items):
                position = len(items) - 1

    window.clear()
    menu_panel.hide()
    panel.update_panels()
    curses.doupdate()


def printline(screen, prompt: str, y=None):
    if y is None:
        screen.addstr(screen.getyx()[0], 0, prompt)
    else:
        screen.addstr(y, 0, prompt)
    screen.move(screen.getyx()[0] + 1, 0)  # Move to next line down
    screen.refresh()


def get_input(screen, prompt: str, check_function: Callable[[str], Optional[str]] = None) -> str:
    screen.addstr(screen.getyx()[0], 0, prompt)
    screen.refresh()

    result = ''
    while True:
        key = screen.getch()
        if key in [curses.KEY_ENTER, ord('\n')]:
            screen.move(screen.getyx()[0] + 1, 0)  # Move to next line down
            result_str = str(result)
            if check_function is None:
                return result_str
            check_result = check_function(result_str)
            if check_result is None:
                return result_str
            else:
                printline(screen, check_result)
                result = ''
                screen.addstr(screen.getyx()[0], 0, prompt)
                screen.refresh()
        else:
            result += chr(key)
            screen.addch(key)
            screen.refresh()


def check_short_name(short_name: str) -> Optional[str]:
    if not re.match('[a-z]+', short_name):
        return 'Must be a lowercase name'
    else:
        try:  # TODO: convert to is_exists
            image_dir = Path(f'assets/img/vendors/2021/{short_name}')
            image_dir.mkdir()  # This will fail if it already exists
            return None
        except Exception:
            return 'Short name already exists'


def add_brand(screen):
    screen.clear()
    printline(screen, 'Adding new brand.', y=0)
    short_name = get_input(screen, 'Short Name: ', check_short_name)
    image_dir = Path(f'assets/img/vendors/2021/{short_name}')

    human_name = get_input(screen, 'Human Name: ')
    # TODO: figure out where to insert the brand in the brand list

    url = get_input(screen, 'URL: ', check_url_is_valid)
    logo_url = get_input(screen, 'Logo URL: ', check_url_is_valid)

    extension_tuple = logo_url.rsplit('.', 1)
    if len(extension_tuple) != 2:
        raise Exception('ERROR: logo URL does not have an extension')

    image_name = f'logo.{extension_tuple[1]}'
    download_picture(logo_url, image_dir / image_name)

    data = read_data_file()
    data['brands'].append({
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

    printline(screen, f'You put in {short_name}')
    screen.getkey()


def add_snowboard():
    pass


def main(screen):
    screen.clear()

    screen.addstr(0, 0, 'Welcome to the snowboard import program')
    screen.addstr(1, 0, 'Please select an option:')

    menu_items = ['Add Brand', 'Add Snowboard']

    selected = menu(menu_items, screen)

    if selected == 0:
        add_brand(screen)
    elif selected == 1:
        add_snowboard(screen)

    # screen.refresh()
    # screen.getkey()


if __name__ == '__main__':
    wrapper(main)
