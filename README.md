# AutoUImini - Simple UI Automation Helper

## Features
- Simple UI automation using Python and pyautogui
- Supports keyboard and mouse actions
- Application launching by Win+R and typing the app name
- Waiting commands by screen change detection
- Logging of actions for debugging and tracking
- Swing-like cursor movement for pointting and clicking
- Simple API for easy integration into Python projects

## Installation
Download the source code autouimini.py and import it in your Python project.

## Example Usage
```python
from autouimini import autouimini
ui = autouimini.autouimini()
ui.runapp("notepad")
ui.log("launched Notepad")
ui.typewrite("Hello, this is AutoUI Mini!")
ui.log("Typed text in Notepad")
ui.move_cursor(50,200, isswing=True)
```


