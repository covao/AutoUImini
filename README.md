# AutoUImini - Simple UI Automation Helper

## Features
- Simple UI automation using Python and pyautogui
- Supports keyboard and mouse actions
- Image-based screen change detection
- Application launching and window management

## Installation
Download the source code pyauto_mini.py and import it in your Python project.

## Example Usage
```python
from pyauto_mini import autouimini
ui = autouimini.autouimini()
ui.runapp("notepad")
ui.log("launched Notepad")
ui.typewrite("Hello, this is AutoUI Mini!")
ui.log("Typed text in Notepad")
ui.move_cursor(50,200, isswing=True)
```


