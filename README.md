<p align="center">
  <img src="src/assets/ROT.png" alt="ROT Logo" />
</p>

# ROT - Game Input Emulation Script

ROT is a Python script that demonstrates how to use the vgamepad library to emulate an Xbox 360 game controller for educational purposes. It reads configurations for key bindings and rotation sequences from separate files, allowing for customization and exploration of game mechanics. This project is intended to help users learn programming concepts, input emulation, and understand in-game mechanics.

## Disclaimer

This script is for educational purposes only and is not intended for use in violation of any terms of service or end-user license agreement (EULA) associated with any specific game. The author does not encourage or condone the use of this script to cheat, exploit, or gain an unfair advantage in any game. Please use this script responsibly and in compliance with the rules and policies of the game you are playing.

## Educational Value

The primary goal of this project is to provide a learning resource for users interested in understanding:

1. How to interact with the vgamepad library to create virtual gamepad inputs.
2. The use of the configparser library to read configuration files for key bindings and rotation sequences.
3. The implementation of multi-threading to run separate processes concurrently.
4. The use of the keyboard library to create hotkeys for script control.

Please utilize this script in a manner that promotes learning and understanding of the underlying concepts without violating any terms of service, EULA, or other legal and ethical guidelines.

## Contributing

Contributions to this project should focus on improving its educational value or expanding its capabilities for learning and experimentation, without promoting or enabling cheating or exploitation in any game.

## Installation and Setup

Follow these steps to install the required libraries and set up the necessary tools to use this script.

### Prerequisites

1. Install Python (3.6 or higher) from [python.org](https://www.python.org/downloads/).

2. Install the following Python libraries using pip:

`pip install vgamepad keyboard configparser`
or
`pip install -r requirements.txt`

### Setting Up Your Game

For games such as World of Warcraft, you will need to install an addon that allows you to use a physical game controller to control character movement and abilities. This script will emulate a second virtual Xbox 360 controller, allowing you to use the physical controller for movement and the virtual controller for abilities.

Download and install the ConsolePort addon for World of Warcraft from [CurseForge](https://www.curseforge.com/wow/addons/console-port) or your preferred addon manager.

This application is not specifically designed for any game but can be used with any game that supports the use of a physical game controller. If you are using a game other than World of Warcraft, you may need to install an additional addon or other software to enable controller support. World of Warcraft is just one example of a game that the script can be used with.

### Setting Up Controllers

To use your own controller for character movement while also using this script, follow these steps:

1. Ensure your physical game controller (e.g., Xbox, PlayStation, or another compatible controller) is connected to your computer before running the script.

2. Start your game with any addons needed to enable controller support.

3. After connecting your physical controller and enabling the addon, run the script. The script will emulate a second virtual Xbox 360 controller, allowing the script to control character abilities.

By connecting your physical controller before running the script, you ensure that your game detects it as the first controller, allowing you to retain full control over character movement. Otherwise, your game may disable controller movement while the script is running as it has taken 1st position and a MNK must be used to move the character while the script is running.

## Usage

Before using this script, please ensure you have the vgamepad library installed, a 'YOURGAME.ini' file set up with key bindings in a seperate folder called 'bindings', and a separate folder called 'rotations' containing rotation configuration files for different game classes or builds.

When running the script, it will prompt you to press a specific hotkey combination to toggle the combat rotation on and off. Note that this functionality is provided for educational purposes and should not be used to gain an unfair advantage or violate the terms of service of any game.

1. Ensure you have completed the installation process and properly set up the controller as described in the [Installation and Setup](#installation-and-setup) section.

2. Create a folder called `bindings` in the script's directory and add game configuration files for different games and their key bindings. An example can be found in the repository.

3. Create a folder called `rotations` in the script's directory and add rotation configuration files for different game classes or builds. An example can be found in the repository.

4. Run the script using the following command:

`python ROT.py`

5. The script will prompt you to press a specific hotkey combination (e.g., 'DEL') to toggle the combat rotation on and off. Press the hotkey to start or stop the script's ability control. I chose 'DEL' because it is easy for me. You can choose any key you want by changing the value of the `TOGGLE_ROTATION` constant in the script's application variables.

6. To exit the script, press the specified hotkey combination for exit (e.g., 'Shift+X'). You can change this by changing the value of the `EXIT_PROGRAM` constant in the script.

Please note that the usage of this script for automating gameplay, especially in a manner that violates a game's terms of service or EULA, is not recommended. Use this script responsibly, and focus on the educational value and understanding of the underlying concepts.

## Support and Community

If you need help or have questions about this application, the best way to get support is by joining the Discord.

To join the Discord, click on this invite link: [Discord](https://discord.com/invite/aP9CjWE)

## Support and Donations

If you enjoy using this project and find it helpful, please consider supporting its development. Your support helps to ensure the project's continued development, bug fixes, and improvements.

### Other Ways to Support

- Share this project.
- Report any issues you encounter or suggest new features and improvements by creating a new issue on the GitHub repository.
- Contribute to the project by submitting pull requests with bug fixes, new features, or improvements to the code or documentation.
- Star the repository on GitHub to show your appreciation for the project.
- Show your support on social media. [Linktree](https://linktr.ee/3v1lxd)

### Donations

If you would like to make a financial contribution to support development, you can donate using the following method:

- [PayPal](https://paypal.me/ScottDIT)

Your donation, no matter the size, is greatly appreciated and will help to support future development and maintenance. Thank you for your generosity!
