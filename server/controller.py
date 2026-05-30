import time

import nxbt
import atexit
import random

nx = None


def init():
    global nx
    nx = nxbt.Nxbt()
    print("Initializing nx...")

    saved_addresses = nx.get_switch_addresses()
    print(f"Found saved Switch addresses: {saved_addresses}")

    controller_index = nx.create_controller(
        nxbt.PRO_CONTROLLER,
        reconnect_address=saved_addresses
    )
    print(f"Waiting for Nintendo Switch to connect... (Index: {controller_index})")

    nx.wait_for_connection(controller_index)
    print(f"Nintendo Switch connected! (Index: {controller_index})")

    atexit.register(shutdown, controller_index)
    return controller_index


def play(controller_index, states):
    if 'team_selection' in states:
        select_team(controller_index)
    if 'mega_evolve' in states:
        mega_evolve(controller_index)
    if 'combat_attack' in states:
        combat_attack(controller_index)
    if 'combat_switch' in states:
        combat_switch(controller_index)
    if 'continue' in states:
        continue_battling(controller_index)


def shutdown(controller_index):
    # This frees up the adapter that was in use by this controller
    nx.remove_controller(controller_index)


def t():
    return random.uniform(1.1, 1.3)


def select_team(controller_index):
    time.sleep(10)
    for i in range(0, 3):
        nx.press_buttons(controller_index, [nxbt.Buttons.A], t())
        time.sleep(t())
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN], t())
        time.sleep(t())

    for i in range(0, 3):
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN], t())
        time.sleep(t())

    for i in range(0, 2):
        nx.press_buttons(controller_index, [nxbt.Buttons.A], t())
        time.sleep(t())


def combat_attack(controller_index):
    for i in range(0, 2):
        nx.press_buttons(controller_index, [nxbt.Buttons.A], t())
        time.sleep(t())


def mega_evolve(controller_index):
    nx.press_buttons(controller_index, [nxbt.Buttons.R], t())
    time.sleep(t())


def combat_switch(controller_index):
    nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN], t())
    time.sleep(t())

    for i in range(0, 2):
        nx.press_buttons(controller_index, [nxbt.Buttons.A], t())
        time.sleep(t())


def continue_battling(controller_index):
    for i in range(0, 2):
        nx.press_buttons(controller_index, [nxbt.Buttons.A], t())
        time.sleep(t())


if __name__ == "__main__":
    print("Let's go!")
    init()
