import argparse
import json
import os
from time import sleep

from pynput import keyboard

import pyautogui as pag

sticker_dir = 'stickers'
sticker_bkp_dir = '__' + sticker_dir + '__bkp__'
file_list = os.listdir(sticker_dir)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action='store_true', help="Saved pos file")
    parser.add_argument("-r", action='store_true', help="Load pos file")
    parser.add_argument("-t", action='store_true', help="Test")
    return parser.parse_args()


def on_press(key):
    pass


def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        print('Stop listener')
        return False

    if (key == keyboard.Key.space):
        pos = pag.position()
        record_positions(pos)


pos = dict()
args = get_args()


def record_positions(p):
    if not 'select_file' in pos:
        pos['select_file'] = p
        print('select_file pos =', str(pos['select_file']))
        print('Move cursor to emoji_file and press space')
    elif not 'emoji_file' in pos:
        pos['emoji_file'] = p
        print('emoji_file pos =', str(pos['emoji_file']))
        print('Move cursor to sent emoji and press space')
    elif not 'sent_emoji' in pos:
        pos['sent_emoji'] = p
        print('sent_emoji pos =', str(pos['sent_emoji']))
        print('Move cursor to "Add sticker" and press space')
    elif not 'add_sticker' in pos:
        pos['add_sticker'] = p
        print('add_sticker pos =', str(pos['add_sticker']))
    elif not 'delete_message' in pos:
        pos['delete_message'] = p
        print('delete_message pos =', str(pos['add_sticker']))
    elif not 'delete_message_confirm' in pos:
        pos['delete_message_confirm'] = p
        print('delete_message_confirm pos =', str(pos['add_sticker']))

        print('All positions are recorded! ')
        print(pos)
        if args.s: save()
        print('Press space again to start processing')
    else:
        run()


def save():
    with open('pos.json', 'w') as f:
        json.dump(pos, f, indent=4)


def action():
    # Select file icon
    pag.click(pos['select_file'])
    sleep(0.5)

    # Select emoji and double click
    pag.click(pos['emoji_file'], clicks=2)
    sleep(0.5)

    # Press enter to send
    pag.press('enter')
    sleep(1.5)

    # Right click
    pag.click(pos['sent_emoji'], button='right')
    pag.moveTo(pos['add_sticker'])
    pag.click()

    sleep(0.1)
    # delete_message
    pag.click(pos['sent_emoji'], button='right')
    pag.moveTo(pos['delete_message'])
    pag.click()
    sleep(0.2)
    pag.click(pos['delete_message_confirm'])

    move_next_file()
    sleep(0.5)


def move_next_file():
    if file_list:
        os.rename(os.path.join(sticker_dir, file_list[0]),
                  os.path.join(sticker_bkp_dir, file_list[0]))
        file_list.pop(0)


def ensure_dir(f):
    d = f
    if not os.path.exists(d):
        os.makedirs(d)

    return os.path.exists(f)


def run():
    ensure_dir(sticker_bkp_dir)

    while file_list:
        action()

    os.rmdir(sticker_dir)
    os.rename(sticker_bkp_dir, sticker_dir)


if __name__ == '__main__':

    if args.r:
        print('Use pos.json')
        with open('pos.json', 'r') as f:
            pos = json.load(f)
            run()
    if args.t:
        ensure_dir(sticker_bkp_dir)
        move_next_file()

    else:

        with keyboard.Listener(on_press=on_press,
                               on_release=on_release) as listener:

            print('Move cursor to selecting file icon and press space')
            listener.join()
