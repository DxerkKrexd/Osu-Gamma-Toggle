import ctypes
import keyboard
import os
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image
from colorama import Fore, Style, init

init(autoreset=True)

# ---------------- STATE ---------------- #

console_visible = True
tray_icon = None

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
hdc = user32.GetDC(0)

NORMAL_GAMMA = 1.0
OSU_GAMMA = 2.5

STEP = 0.1
MIN_GAMMA = 0.5
MAX_GAMMA = 4.0

TOGGLE_KEY = "F8"
gamma_enabled = False


# ---------------- TRAY ICON ---------------- #

def create_icon():
    try:
        img = Image.open("C:/Users/B1rd/Downloads/Gamma Toggle/reze.jpg").convert("RGBA")
        return img.resize((64, 64), Image.LANCZOS)
    except:
        return Image.new("RGBA", (64, 64), (80, 80, 80, 255))


def show_console(icon=None, item=None):
    global console_visible
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 5)
    console_visible = True


def hide_console(icon=None, item=None):
    global console_visible
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 0)
    console_visible = False


def toggle_console(icon=None, item=None):
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if ctypes.windll.user32.IsWindowVisible(hwnd):
        hide_console()
    else:
        show_console()


def exit_app(icon=None, item=None):
    global tray_icon

    if tray_icon:
        tray_icon.stop()

    os._exit(0)


# ---------------- GAMMA ---------------- #

def set_gamma(gamma):
    ramp = ((ctypes.c_ushort * 256) * 3)()

    for i in range(256):
        value = int(((i / 255.0) ** (1.0 / gamma)) * 65535)
        value = max(0, min(65535, value))

        ramp[0][i] = value
        ramp[1][i] = value
        ramp[2][i] = value

    gdi32.SetDeviceGammaRamp(hdc, ramp)


# ---------------- UI ---------------- #

def draw_ui():
    os.system("cls")

    art = f"""
{Fore.CYAN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡴⣆⠀⠀⠀⠀⠀⣠⡀ ᶻ 𝗓 𐰁 .ᐟ ⣼⣿⡗⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠀⠘⠷⠶⠶⠶⠾⠉⢳⡄⠀⠀⠀⠀⠀⣧⣿⠀⠀⠀⠀⠀
⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⣤⣤⣤⣤⣿⢿⣄⠀⠀⠀⠀
⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠙⣷⡴⠶⣦
⠀⠀⢱⡀⠀⠉⠉⠀⠀⠀⠀⠛⠃⠀⢠⡟⠀⠀⠀⢀⣀⣠⣤⠿⠞⠛⠋
⣠⠾⠋⠙⣶⣤⣤⣤⣤⣤⣀⣠⣤⣾⣿⠴⠶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀
⠛⠒⠛⠉⠉⠀⠀⠀⣴⠟⢃⡴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠁ {Fore.MAGENTA}Made By Nacht/Dxerk{Fore.CYAN}
{Style.RESET_ALL}
"""

    print(art)
    print("osu! Gamma Toggle\n")

    print(f"{Fore.WHITE}Toggle Key : {TOGGLE_KEY}")
    print(f"OSU Gamma  : {OSU_GAMMA:.2f}")
    print(f"Normal     : {NORMAL_GAMMA}\n")

    print(f"Adjust     : [+] increase | [-] decrease")
    print(f"Current    : {OSU_GAMMA:.2f}")

    if gamma_enabled:
        print(Fore.GREEN + "STATUS: [ON] High Gamma Enabled")
    else:
        print(Fore.RED + "STATUS: [OFF] Normal Gamma")


# ---------------- CONTROLS ---------------- #

def toggle_gamma():
    global gamma_enabled

    gamma_enabled = not gamma_enabled
    set_gamma(OSU_GAMMA if gamma_enabled else NORMAL_GAMMA)
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


# ---------------- KEYBOARD ---------------- #

def keyboard_loop():
    keyboard.add_hotkey(TOGGLE_KEY, toggle_gamma)
    keyboard.add_hotkey("+", increase_gamma)
    keyboard.add_hotkey("-", decrease_gamma)
    keyboard.wait()


# ---------------- TRAY ---------------- #

def setup_tray():
    global tray_icon

    tray_icon = Icon(
        "GammaToggle",
        create_icon(),
        "Gamma Toggle",
        menu=Menu(
            MenuItem("Show / Hide", toggle_console),
            MenuItem("Exit", exit_app)
        )
    )

    tray_icon.run()


# ---------------- START ---------------- #

if __name__ == "__main__":
    try:
        draw_ui()

        threading.Thread(target=keyboard_loop, daemon=True).start()

        setup_tray()

    except Exception as e:
        print("Crash:", e)
        input("Press Enter to exit...")
