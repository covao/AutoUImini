        # AutoUImini
"""
AutoUI — Simple UI automation helper using pyautogui

Class: autouimini
Methods:
- sleep(t): Sleep for t seconds (adjusted by speed rate).
- wait_imgdiff(x, y, width=40, height=40, timeout=5.0): Wait for image change in the specified region.
- log(msg, key="Info"): Log a message with timestamp.
- presskey(key1, key2="", key3=""): Press a key or combination of keys.
- repeatkey(key, n): Press a key n times.
- typewrite(text): Type text with delay.
- runapp(appname): Launch an application by name and focus its window.
- move_cursor(x, y): Move mouse cursor to (x, y).
- swing(): Swing the mouse cursor left and right.
- click(x, y): Move to (x, y) and click.
- leftclick(x, y): Move to (x, y) and left-click.
- set_clipboard(text): Set the system clipboard to the specified text.

"""

import numpy as np  
import time
import sys
import subprocess

import pyautogui
import pygetwindow as gw
from PIL import ImageChops
class autouimini:
    def __init__(self) -> None:
        self.t_rate = 1.0 # speed rate
        self.t_key = 0.2 # key press delay
        self.t_short = 0.3 # short wait
        self.t_move = 0.5 # mouse move delay
        self.app_timeout = 10.0 # app launch timeout

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

    def sleep(self, t: float) -> None:
        try:
            time.sleep(t / self.t_rate)
        except KeyboardInterrupt:
            self.log("Interrupted by Ctrl+C. Exiting...", "Info")
            sys.exit(1)

    def wait_imgdiff(self, x, y, width=40, height=40, timeout=5.0):
        region = (int(x), int(y), int(width), int(height))
        start = time.monotonic()
        prev = pyautogui.screenshot(region=region)

        while time.monotonic() - start < timeout:
            self.sleep(self.t_short)
            cur = pyautogui.screenshot(region=region)
            if ImageChops.difference(prev, cur).getbbox() is not None:
                self.log("Image change detected.")
                return True
            prev = cur      
        return False

    def log(self, msg: str, key: str = "Info") -> None:
        t=time.time()
        timestamp = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))}.{int((t - int(t)) * 1000):03d}"
        msg = f"{timestamp} {msg}"    
        print(msg)
        sys.stdout.flush()

    def presskey(self, key1: str, key2: str = "", key3: str = "") -> None:
        if key2 and key3:
            pyautogui.hotkey(key1, key2, key3)
        elif key2:
            pyautogui.hotkey(key1, key2)
        else:
            pyautogui.press(key1)
        self.sleep(self.t_key)

    def repeatkey(self, key: str, n: int) -> None:
        for _ in range(n):
            self.presskey(key)
            self.sleep(self.t_key)

    def typewrite(self, text: str) -> None:
        pyautogui.typewrite(text, interval=self.t_key)
        self.sleep(self.t_short)

    def runapp(self, appname: str, wait: float = 2.0) -> str:
        old_windows = gw.getAllWindows()

        self.log(f"Opening {appname}...")
        self.presskey("win","r")
        self.sleep(self.t_short)
        self.typewrite(appname)
        self.presskey("enter")
        self.sleep(wait) # Wait launching new app window

        # Wait for new window to appear
        start_time = time.time()
        while True:
            new_windows = gw.getAllWindows() # Get current window titles after launching the app
            added = [w for w in new_windows if w not in old_windows]
            # timeout after app_timeout seconds
            if time.time() - start_time > self.app_timeout:
                self.log(f"Failed to launch {appname}")
                break
            if added:
                self.log(f"Launced {appname} successfully")
                self.sleep(self.t_short)
                # focus the new window
                win = added[0]
                win.activate()
                #move window to (0,0)
                win.moveTo(0, 0)
                # Set fullscreen
                win.maximize()
                self.sleep(self.t_short)
                break
        if not added:
            return ""
        return added[0]

    def move_cursor(self, x: int, y: int) -> None:
        pyautogui.moveTo(x, y, duration=self.t_move)
        self.sleep(self.t_move)

    def swing(self, swing_width: int = 30) -> None:
        # Swing the mouse cursor left and right from its current position.
        x, y = pyautogui.position()
        for dx in [-swing_width, swing_width, -swing_width, swing_width, 0]:
            pyautogui.moveTo(x + dx, y, duration= 0.2)
    
    def click(self, x: int, y: int) -> None:
        pyautogui.moveTo(x, y, duration=self.t_move)
        pyautogui.click(x, y)
        self.sleep(self.t_key)
    
    def leftclick(self, x: int, y: int) -> None:
        self.sleep(self.t_move)
        pyautogui.click(x, y, button='left')
        self.sleep(self.t_key)

    def set_clipboard(self, text: str) -> None:
        subprocess.run("clip", text=True, input=text)


def main() -> None:
    # Demo: Open MS Paint, paste screenshot, resize it.
    ui = autouimini()

    # Capture the current screen to clipboard first
    ui.log("Capturing full screen to clipboard")
    # Press PrintScreen key
    ui.presskey("alt", "printscreen")
    # Then open MS Paint and paste
    ui.runapp("mspaint")

    # Resize image to 10x10 before pasting
    ui.log("Resize to 10x10")
    ui.presskey("ctrl", "e")
    ui.typewrite("10")
    ui.presskey("tab")
    ui.typewrite("10")
    ui.presskey("enter")

    ui.log("Pasting image from clipboard")
    ui.presskey("ctrl", "v")
    ui.presskey("ctrl", "a")
    ui.presskey("escape") 
    
    ui.log("Resize to 50%")
    ui.presskey("ctrl", "w")
    ui.typewrite("50")
    ui.presskey("enter")

    ui.log("Copying final image to clipboard")
    ui.presskey("ctrl", "a")
    ui.presskey("ctrl", "c")

    ui.log("Demo completed.")

if __name__ == "__main__":
    main()