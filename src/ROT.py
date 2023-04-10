import vgamepad as vg
import configparser
import threading
import keyboard
import time

#############################################
# Application Variables

# Game bindings to load, change and reload app to switch bindings
BINDINGS_FILE = 'bindings/WOW.ini'
# Rotation file to load, change and reload app to switch rotations
ROTATION_FILE = 'rotations/WOW_warrior_arms.ini'
# Delay between each ability in the rotation
ABILITY_DELAY = 0.1
# Delay between each rotation loop
KEEP_RUNNING_DELAY = 1
# Delay between each run loop to detect hotkeys and reduce CPU usage.
RUN_LOOP_DELAY = 1
# Delay to wait for button presses to be registered
BUTTON_DELAY = 0.1

# Hotkeys
# Refer to the keyboard docs for information on hotkeys and their syntax.
# https://github.com/boppreh/keyboard#keyboard.add_hotkey
# Toggle the rotation
TOGGLE_ROTATION = 'DEL'
# Exit the application
EXIT_PROGRAM = 'shift+x'

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
config.read(BINDINGS_FILE)

buttons = {}
for button, ability in config['bindings'].items():
    # check if ability is bound to a button
    if ability != 'None':
        buttons[ability] = button.upper()

# Flags to control the while loop and background thread
keep_running = False
thread_running = True


def run_loop():
    """
    Function that runs the main loop for executing the rotation.
    The loop runs indefinitely as long as thread_running is True, but the rotation execution is controlled by the keep_running flag.
    """
    global keep_running, thread_running
    while thread_running:
        if keep_running:
            print("Running rotation...")
            # load new config file from rotations folder
            config.read(ROTATION_FILE)
            rotation = config['ROT']['Rotation'].split('\n')
            # spam rotation
            for ability in rotation:
                if keep_running:
                    if ', ' in ability:
                        ability_delay = int(ability.split(', ')[1]) / 1000
                        ability = ability.split(', ')[0]
                    else:
                        ability_delay = ABILITY_DELAY

                    for bound_ability, button in buttons.items():
                        if bound_ability in ability:
                            # check if button includes a trigger pull
                            if 'LT_' in button:
                                left_trigger()
                            elif 'LTRT_' in button:
                                lr_trigger()
                            elif 'RT_' in button:
                                right_trigger()
                            else:
                                lrt_release()

                            # wait for trigger to be pulled or released
                            # vgamepad doesn't seem to support multiple presses/releases in a single update
                            # so we need to wait for the trigger before pressing another button
                            update()
                            time.sleep(BUTTON_DELAY)

                            if button != 'RIGHT_SHOULDER' and button != 'LEFT_SHOULDER' and button != 'RIGHT_THUMB' and button != 'LEFT_THUMB' and button != 'START' and button != 'BACK' and button != 'GUIDE' and button != 'DPAD_UP' and button != 'DPAD_DOWN' and button != 'DPAD_LEFT' and button != 'DPAD_RIGHT':
                                if '_' in button:
                                    button = '_'.join(button.split('_')[1:])

                            press(gpad[button])
                            print('Activating ' + bound_ability +
                                  ' with ' + button)

                            # wait for ability delay
                            update()
                            time.sleep(ability_delay)

                            # wait for button to be released
                            reset()
                            update()
                            time.sleep(BUTTON_DELAY)

            # Adjust this delay as needed to reduce CPU usage when the loop is running
            time.sleep(KEEP_RUNNING_DELAY)
        else:
            # Adjust this delay as needed to reduce CPU usage when the loop is not running
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
