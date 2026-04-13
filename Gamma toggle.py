import ctypes
import keyboard
import os
from colorama import Fore, Style, init

init(autoreset=True)

# Windows stuff idk
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
hdc = user32.GetDC(0)

# Adjustment and toggle settings
NORMAL_GAMMA = 1.0
OSU_GAMMA = 2.5

STEP = 0.1
MIN_GAMMA = 0.5
MAX_GAMMA = 4.0

TOGGLE_KEY = "F8"
# change "F8" to change the gamma toggle key.

gamma_enabled = False


# How da shi works
def set_gamma(gamma):
    ramp = ((ctypes.c_ushort * 256) * 3)()

    for i in range(256):
        value = int(((i / 255.0) ** (1.0 / gamma)) * 65535)
        value = max(0, min(value, 65535))

        ramp[0][i] = value
        ramp[1][i] = value
        ramp[2][i] = value

    gdi32.SetDeviceGammaRamp(hdc, ramp)


# ascii
def clear():
    os.system("cls")


def draw_ui():
    clear()

    art = f"""
{Fore.CYAN}{Style.DIM}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡴⣆⠀⠀⠀⠀⠀⣠⡀ ᶻ 𝗓 𐰁 .ᐟ ⣼⣿⡗⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠀⠘⠷⠶⠶⠶⠾⠉⢳⡄⠀⠀⠀⠀⠀⣧⣿⠀⠀⠀⠀⠀
⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⣤⣤⣤⣤⣿⢿⣄⠀⠀⠀⠀
⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠙⣷⡴⠶⣦
⠀⠀⢱⡀⠀⠉⠉⠀⠀⠀⠀⠛⠃⠀⢠⡟⠀⠀⠀⢀⣀⣠⣤⠿⠞⠛⠋
⣠⠾⠋⠙⣶⣤⣤⣤⣤⣤⣀⣠⣤⣾⣿⠴⠶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀
⠛⠒⠛⠉⠉⠀⠀⠀⣴⠟⢃⡴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠁ Made By Nacht/Dxerk
{Style.RESET_ALL}
"""

    print(art)
    print("osu! Gamma Toggle\n")

    print(f"Toggle Key : {TOGGLE_KEY}")
    print(f"OSU Gamma  : {OSU_GAMMA:.2f}")
    print(f"Normal     : {NORMAL_GAMMA}\n")

    print(f"Adjust     : [+] increase | [-] decrease")
    print(f"Current    : {OSU_GAMMA:.2f}")

    if gamma_enabled:
        print(Fore.CYAN + "STATUS: [ON]  High Gamma Enabled")
    else:
        print(Fore.CYAN + "STATUS: [OFF] Normal Gamma")


# Keybinds
def toggle_gamma():
    global gamma_enabled

    gamma_enabled = not gamma_enabled

    if gamma_enabled:
        set_gamma(OSU_GAMMA)
    else:
        set_gamma(NORMAL_GAMMA)

    draw_ui()


def increase_gamma():
    global OSU_GAMMA

    OSU_GAMMA = min(MAX_GAMMA, OSU_GAMMA + STEP)

    if gamma_enabled:
        set_gamma(OSU_GAMMA)

    draw_ui()


def decrease_gamma():
    global OSU_GAMMA

    OSU_GAMMA = max(MIN_GAMMA, OSU_GAMMA - STEP)

    if gamma_enabled:
        set_gamma(OSU_GAMMA)

    draw_ui()


# ACHANGE these to change the and adjustment binds. NOT the toggle bind, TOGGLE is Line 21
keyboard.add_hotkey(TOGGLE_KEY, toggle_gamma)
keyboard.add_hotkey("+", increase_gamma)
keyboard.add_hotkey("-", decrease_gamma)

draw_ui()
print("\nPress F8 to toggle gamma.")
keyboard.wait()
