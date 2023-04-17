import vgamepad as vg
import configparser
import threading
import keyboard
import time
import sys

#############################################
# Application Variables

# Read Application Variables from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

BINDINGS_FILE = config.get('Application', 'bindings_file')
ROTATION_FILE = config.get('Application', 'rotation_file')
ABILITY_DELAY = config.getfloat('Application', 'ability_delay')
KEEP_RUNNING_DELAY = config.getfloat('Application', 'keep_running_delay')
RUN_LOOP_DELAY = config.getfloat('Application', 'run_loop_delay')
BUTTON_DELAY = config.getfloat('Application', 'button_delay')
TOGGLE_ROTATION = config.get('Application', 'toggle_rotation')
EXIT_PROGRAM = config.get('Application', 'exit_program')

#############################################


#############################################
# Gamepad Controls

gamepad = vg.VX360Gamepad()

# Gamepad button constants
# Constants for each button on the gamepad, used for easier identification and use in the code.
DU = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
DD = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
DL = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
DR = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
START = vg.XUSB_BUTTON.XUSB_GAMEPAD_START
BACK = vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
LTHUMB = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
RTHUMB = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
LB = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
RB = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
GUIDE = vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
A = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
B = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
X = vg.XUSB_BUTTON.XUSB_GAMEPAD_X
Y = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y

# Dictionary mapping button names to their corresponding constants
gpad = {
    'DU': DU,
    'DD': DD,
    'DL': DL,
    'DR': DR,
    'START': START,
    'BACK': BACK,
    'LTHUMB': LTHUMB,
    'RTHUMB': RTHUMB,
    'LB': LB,
    'RB': RB,
    'GUIDE': GUIDE,
    'A': A,
    'B': B,
    'X': X,
    'Y': Y
}


def left_trigger():
    """
    Fully press the left trigger on the gamepad.
    """
    gamepad.left_trigger(value=255)
    update()


def right_trigger():
    """
    Fully press the right trigger on the gamepad.
    """
    gamepad.right_trigger(value=255)
    update()


def lr_trigger():
    """
    Fully press both triggers on the gamepad.
    """
    gamepad.left_trigger(value=255)
    gamepad.right_trigger(value=255)
    update()


def lt_release():
    """
    Release the left trigger on the gamepad.
    """
    gamepad.left_trigger(value=0)
    update()


def rt_release():
    """
    Release the right trigger on the gamepad.
    """
    gamepad.right_trigger(value=0)
    update()


def lrt_release():
    """
    Release both triggers on the gamepad.
    """
    gamepad.left_trigger(value=0)
    gamepad.right_trigger(value=0)
    update()


def press(button):
    """
    Press a button on the gamepad.
    :param button: The button to press.
    """
    gamepad.press_button(button=button)
    update()


def update():
    """
    Update the gamepad state.
    """
    gamepad.update()
    time.sleep(BUTTON_DELAY)


def reset():
    """
    Reset the gamepad state by releasing all buttons and triggers.
    """
    gamepad.reset()
    gamepad.update()
#############################################


config = configparser.ConfigParser()
config.read('bindings/' + BINDINGS_FILE)

buttons = {}
for button, ability in config['Bindings'].items():
    if ability != 'None':
        buttons[ability] = button.upper()

keep_running = False
thread_running = True


def trigger_action(trigger_type):
    """
    Perform the specified trigger action and update the gamepad state.

    :param trigger_type: The trigger action to be performed (e.g., 'LT', 'LTRT', or 'RT')
    """
    trigger_func = {
        "LT": left_trigger,
        "LTRT": lr_trigger,
        "RT": right_trigger,
    }

    if trigger_type in trigger_func:
        trigger_func[trigger_type]()


def press_button(button):
    """
    Press the specified button and print the bound ability being activated.

    :param button: The button to be pressed
    :param bound_ability: The ability associated with the button
    """
    press(gpad[button])


def activate_ability(ability):
    """
    Activate an ability by performing the associated trigger action, pressing the button,
    and updating the gamepad state.

    :param ability: The ability to be activated
    """
    if ',' in ability:
        ability_delay = int(ability.split(',')[1]) / 1000
        ability = ability.split(',')[0]
    else:
        ability_delay = ABILITY_DELAY

    for bound_ability, button in buttons.items():
        if bound_ability in ability:
            print(f'Activating {bound_ability} with {button}')
            trigger_type = button.split('_')[0]
            if trigger_type in ['LT', 'LTRT', 'RT']:
                trigger_action(trigger_type)
                button = button.replace(trigger_type + '_', '')
            else:
                trigger_type = None

            press_button(button)
            reset()
            time.sleep(ability_delay)


def run_loop():
    """
    Function that runs the main loop for executing the rotation.
    The loop runs indefinitely as long as thread_running is True, but the rotation execution is controlled by the keep_running flag.
    """
    global keep_running, thread_running
    while thread_running:
        if keep_running:
            print(F"Running rotation... [{ROTATION_FILE}]")
            config.read('rotations/' + ROTATION_FILE)
            rotation = config['ROT']['Rotation'].replace('[', "")
            rotation = rotation.replace(']', "")
            rotation = rotation.split("','")
            rotation = [x.replace("'", "") for x in rotation]

            for ability in rotation:
                if keep_running:
                    reset()
                    activate_ability(ability)

            time.sleep(KEEP_RUNNING_DELAY)
        else:
            time.sleep(RUN_LOOP_DELAY)


def toggle_loop():
    """
    Function that toggles the main loop's keep_running flag when the hotkey is pressed.
    """
    global keep_running
    keep_running = not keep_running

    if not keep_running:
        reset()
        print("Stopped.")


def exit_program():
    """
    Function to stop the background thread and exit the script.
    """
    global thread_running
    thread_running = False
    print("Exiting...")
    sys.exit()


def main():
    """
    Main function that initializes and starts the loop_thread and sets up the hotkeys for toggling the loop and exiting the program.
    """
    loop_thread = threading.Thread(target=run_loop)
    loop_thread.start()

    keyboard.add_hotkey(TOGGLE_ROTATION, toggle_loop)
    keyboard.add_hotkey(EXIT_PROGRAM, exit_program)

    print(
        f"Press '{TOGGLE_ROTATION}' to toggle the rotation. Press '{EXIT_PROGRAM}' to exit.")

    loop_thread.join()


if __name__ == "__main__":
    main()
