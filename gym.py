import sys
import keyboard
from datetime import datetime
from time import sleep

import vgamepad as vg

global KEY_DELAY
KEY_DELAY = 0.1
global SPECIAL_ACTION
SPECIAL_ACTION = ""

gamepad = vg.VDS4Gamepad()

direction = ""


def push_button(button):
    gamepad.press_button(button=button)
    gamepad.update()
    sleep(KEY_DELAY)
    gamepad.release_button(button=button)
    gamepad.update()


def push_trigger(button, hold_at_half=False):
    if button == "L2":
        vgbutton=vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_LEFT
    elif button == "R2":
        vgbutton=vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_RIGHT
    gamepad.press_button(button=vgbutton)
    for i in range(30, 256, 25):
        x=i/255
        if button == "L2":
            gamepad.left_trigger_float(value_float=x)
        elif button == "R2":
            gamepad.right_trigger_float(value_float=x)
        gamepad.update()
        if hold_at_half == True and i == 105:
            print("hold at half")
            global move_delay
            sleep(move_delay * 1.5)
    sleep(KEY_DELAY)
    for i in range(255, -1, -25):
        if i < 25:
            i = 0
        x=i/255
        if button == "L2":
            gamepad.left_trigger_float(value_float=x)
        elif button == "R2":
            gamepad.right_trigger_float(value_float=x)
        gamepad.update()
    gamepad.release_button(button=vgbutton)
    gamepad.update()


def rapid_trigger(button, count=7):
    for i in range(count):
        if i > 0:
            sleep(KEY_DELAY)
        push_trigger(button)


def delay(val):
    sleeptime = val - KEY_DELAY - 0.001
    if sleeptime <= 0:
        return
    sleep(sleeptime)


def play_gym(direction):
    if direction.upper() == "L":
        move_data = ["L1","R1","L2","R2"]
    elif direction.upper() == "R":
        move_data = ["R1","L1","R2","L2"]
    else:
        print(f"Exiting due to missing direction (L or R)")
        exit(1)

    # Start
    global SPECIAL_ACTION
    move_count = 0
    global move_delay
    move_delay = 0.8
    points_count = 0
    start_time = datetime.now()

    # Loop
    while True:
        if move_delay > 0.5:
            move_delay = round(move_delay - 0.05, 3)
        elif move_delay > 0.25:
            move_delay = round(move_delay - 0.01, 3)
        # Play the move data
        for i, line in enumerate(move_data):
            timestamp = (datetime.now() - start_time).total_seconds()
            print(f"Playing loop [{line}] [{points_count}][{move_delay}][{timestamp}] special = {SPECIAL_ACTION}")
            if line == "S":
                delay(move_delay)
            elif line == "L1":
                push_button(vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)
                delay(move_delay)
            elif line == "L2":
                if direction.upper() == "L" and SPECIAL_ACTION == "o":
                    push_trigger("L2", hold_at_half=True)
                    SPECIAL_ACTION = ""
                elif direction.upper() == "L" and SPECIAL_ACTION == "p":
                    rapid_trigger("L2")
                    SPECIAL_ACTION = ""
                else:
                    push_trigger("L2")
                delay(move_delay)
            elif line == "R1":
                push_button(vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)
                delay(move_delay)
            elif line == "R2":
                if direction.upper() == "R" and SPECIAL_ACTION == "o":
                    push_trigger("R2", hold_at_half=True)
                    SPECIAL_ACTION = ""
                elif direction.upper() == "R" and SPECIAL_ACTION == "p":
                    rapid_trigger("R2")
                    SPECIAL_ACTION = ""
                else:
                    push_trigger("R2")
                delay(move_delay)
            move_count += 1
        points_count += 1


def assign_special(action):
    global SPECIAL_ACTION
    SPECIAL_ACTION = action

def setup_listener():
    keyboard.on_press_key("o", lambda _: assign_special("o"))
    keyboard.on_press_key("g", lambda _: assign_special("o"))
    keyboard.on_press_key("p", lambda _: assign_special("p"))
    keyboard.on_press_key("y", lambda _: assign_special("p"))
    print("Starting...")
    play_gym(direction)


def get_dir_from_user():
    global direction
    direction = input("Which direction would you like to play (L or R)? ")

if __name__ == "__main__":
    try:
        print("Gym Crunch Off vs. Jules")
        print()
        print("Special action keys available during play.\nPress corresponding key when colour/action appears on screen.")
        print("[G]reen - Hold at half - alternate key - [O]")
        print("[Y]ellow - Rapid press - alternate key - [P]")
        print()
        get_dir_from_user()
        setup_listener()
    except KeyboardInterrupt:
        print("User requested to stop the script. Exiting gracefully.")
        sys.exit(0)
