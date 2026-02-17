"""
AutoUIMini — Simple UI automation helper using pyautogui
Methods:
- `sleep(t)`: Sleep for a specified time adjusted by the speed rate.
- `wait_imgdiff(x, y, width, height, timeout)`: Wait for a change in a specified screen region.
- `log(msg, key)`: Log messages with timestamps.
- `presskey(key1, key2, key3)`: Press one or more keys.
- `repeatkey(key, n)`: Press a key multiple times.
- `typewrite(text)`: Type text with a delay between keystrokes.
- `runapp(appname, wait, width, height)`: Launch an application and optionally resize its window.
- `move_cursor(x, y, isswing)`: Move the mouse cursor to specified coordinates with optional swinging.
- `swing(swing_width)`: Swing the mouse cursor left and right.
- `click(x, y, isswing)`: Click at specified coordinates with optional swinging.
- `leftclick(x, y, isswing)`: Left click at specified coordinates with optional swinging.
- Properties:
- `t_rate`: Speed rate for adjusting timings.
- `t_key`: Delay after key presses.
- `t_short`: Short wait time.
- `t_move`: Mouse move delay.
- `app_timeout`: Timeout for launching applications.
- `scale`: Coordinate scaling factor for converting logical coordinates to physical pixels.
"""

import numpy as np  
import time
import sys
import subprocess
import ctypes

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
        self.scale = 1.0 # DPI scaling factor

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

    def runapp(self, appname: str, wait: float = 2.0, width: int = None, height: int = None) -> str:
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
                # move window to (0,0)
                win.moveTo(0, 0)
                # If width/height provided, resize; otherwise maximize
                try:
                    if width and height:
                        win.resizeTo(int(width), int(height))
                    else:
                        win.maximize()
                except Exception:
                    # Some window types may not support resizeTo; fall back to maximize
                    try:
                        win.maximize()
                    except Exception:
                        pass
                self.sleep(self.t_short)
                break
        if not added:
            return ""
        return added[0]

    def move_cursor(self, x: int, y: int, isswing: bool = False) -> None:
        # Use self.scale to convert logical coordinates -> physical pixels
        phys_x = int(round(x * self.scale))
        phys_y = int(round(y * self.scale))
        pyautogui.moveTo(phys_x, phys_y, duration=self.t_move)
        self.sleep(self.t_move)
        if isswing:
            self.swing()

    def swing(self, swing_width: int = 30) -> None:
        # Swing the mouse cursor left and right from its current position.
        x, y = pyautogui.position()
        for dx in [-swing_width, swing_width, -swing_width, swing_width, 0]:
            pyautogui.moveTo(x + dx, y, duration= 0.2)
    
    def click(self, x: int, y: int, isswing: bool = False) -> None:
        # Click at logical coordinates (x,y) after applying self.scale.
        phys_x = int(round(x * self.scale))
        phys_y = int(round(y * self.scale))
        if isswing:
            self.swing()
        pyautogui.click(phys_x, phys_y)
        self.sleep(self.t_key)
    
    def leftclick(self, x: int, y: int, isswing: bool = False) -> None:
        # Left click at logical coordinates after applying self.scale.
        phys_x = int(round(x * self.scale))
        phys_y = int(round(y * self.scale))
        if isswing:
            self.swing()
        pyautogui.click(phys_x, phys_y, button='left')
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
    ui.move_cursor(490,990, isswing=True)

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