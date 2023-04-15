import vgamepad as vg
import configparser
import threading
import keyboard
import time

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
DPAD_UP = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
DPAD_DOWN = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
DPAD_LEFT = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
DPAD_RIGHT = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
START = vg.XUSB_BUTTON.XUSB_GAMEPAD_START
BACK = vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
LEFT_THUMB = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
RIGHT_THUMB = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
LEFT_SHOULDER = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
RIGHT_SHOULDER = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
GUIDE = vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
A = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
B = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
X = vg.XUSB_BUTTON.XUSB_GAMEPAD_X
Y = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y

# Dictionary mapping button names to their corresponding constants
gpad = {
    'DPAD_UP': DPAD_UP,
    'DPAD_DOWN': DPAD_DOWN,
    'DPAD_LEFT': DPAD_LEFT,
    'DPAD_RIGHT': DPAD_RIGHT,
    'START': START,
    'BACK': BACK,
    'LEFT_THUMB': LEFT_THUMB,
    'RIGHT_THUMB': RIGHT_THUMB,
    'LEFT_SHOULDER': LEFT_SHOULDER,
    'RIGHT_SHOULDER': RIGHT_SHOULDER,
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


def lt_release():
    """
    Release the left trigger on the gamepad.
    """
    gamepad.left_trigger(value=0)


def right_trigger():
    """
    Fully press the right trigger on the gamepad.
    """
    gamepad.right_trigger(value=255)


def rt_release():
    """
    Release the right trigger on the gamepad.
    """
    gamepad.right_trigger(value=0)


def lr_trigger():
    """
    Fully press both triggers on the gamepad.
    """
    gamepad.left_trigger(value=255)
    gamepad.right_trigger(value=255)


def lrt_release():
    """
    Release both triggers on the gamepad.
    """
    gamepad.left_trigger(value=0)
    gamepad.right_trigger(value=0)


def press(button):
    """
    Press a button on the gamepad.
    :param button: The button to press.
    """
    gamepad.press_button(button=button)


def update():
    """
    Update the gamepad state.
    """
    gamepad.update()


def reset():
    """
    Reset the gamepad state by releasing all buttons and triggers.
    """
    gamepad.reset()
#############################################


# Get bindings from bindings file
config = configparser.ConfigParser()
config.read('bindings/' + BINDINGS_FILE)

buttons = {}
for button, ability in config['Bindings'].items():
    # check if ability is bound to a button
    if ability != 'None':
        buttons[ability] = button.upper()

# Flags to control the while loop and background thread
keep_running = False
thread_running = True


def trigger_action(trigger_type):
    """
    Perform the specified trigger action and update the gamepad state.

    :param trigger_type: The trigger action to be performed (e.g., 'LT_', 'LTRT_', or 'RT_')
    """
    trigger_func = {
        "LT_": left_trigger,
        "LTRT_": lambda: [left_trigger(), right_trigger()],
        "RT_": right_trigger,
    }

    if trigger_type in trigger_func:
        trigger_func[trigger_type]()
        update()
    else:
        lt_release()
        update()
        rt_release()
        update()


def press_button(button, bound_ability):
    """
    Press the specified button and print the bound ability being activated.

    :param button: The button to be pressed
    :param bound_ability: The ability associated with the button
    """
    trigger_prefixes = ['LT_', 'LTRT_', 'RT_']
    for prefix in trigger_prefixes:
        if prefix in button:
            button = button.replace(prefix, '')

    press(gpad[button])
    print(f'Activating {bound_ability} with {button}')
    update()


def activate_ability(ability):
    """
    Activate an ability by performing the associated trigger action, pressing the button,
    and updating the gamepad state.

    :param ability: The ability to be activated
    """
    if ', ' in ability:
        ability_delay = int(ability.split(', ')[1]) / 1000
        ability = ability.split(', ')[0]
    else:
        ability_delay = ABILITY_DELAY

    for bound_ability, button in buttons.items():
        if bound_ability in ability:
            trigger_type = button.split('_')[0] + '_'
            trigger_action(trigger_type)
            time.sleep(BUTTON_DELAY)
            press_button(button, bound_ability)
            time.sleep(BUTTON_DELAY)
            reset()
            update()
            time.sleep(ability_delay)


def run_loop():
    """
    Function that runs the main loop for executing the rotation.
    The loop runs indefinitely as long as thread_running is True, but the rotation execution is controlled by the keep_running flag.
    """
    global keep_running, thread_running

    while thread_running:
        if keep_running:
            print("Running rotation...")
            config.read('rotations/' + ROTATION_FILE)
            rotation = config['ROT']['Rotation'].split('\n')

            for ability in rotation:
                if keep_running:
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
    print("Starting rotation" if keep_running else "Stopping rotation")
    if not keep_running:
        # reset controller on stop
        lrt_release()
        update()
        reset()
        update()


def exit_program():
    """
    Function to stop the background thread and exit the script.
    """
    global thread_running
    thread_running = False
    print("Exiting...")


def main():
    """
    Main function that initializes and starts the loop_thread and sets up the hotkeys for toggling the loop and exiting the program.
    """
    loop_thread = threading.Thread(target=run_loop)
    loop_thread.start()

    # Set up the hotkey to toggle the loop (for example, 'DEL')
    keyboard.add_hotkey(TOGGLE_ROTATION, toggle_loop)
    # Set up the hotkey to exit the program (for example, 'shift+x')
    keyboard.add_hotkey(EXIT_PROGRAM, exit_program)

    print(
        f"Press '{TOGGLE_ROTATION}' to toggle the rotation. Press '{EXIT_PROGRAM}' to exit.")

    # Keep the main thread running so the hotkeys can be detected
    loop_thread.join()


if __name__ == "__main__":
    main()
