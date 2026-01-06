# Auto Typing Tool

Simulates typing for code demonstrations and tutorials.

![Auto Typing GUI Screenshot](auto-typer-screen.png)

## Features

- Adjustable WPM with pattern-based speed variation
- Language support: Java, JavaScript, TypeScript, React, CSS, Python, C++, C#
- Pause directives: `{{PAUSE:X}}` pauses for X seconds (max 60)
- Skip leading whitespace option for IDEs with auto-indent

## Installation

### Running the App (macOS)

1. Download the latest release from the github release page
1. Run the app
1. Grant accessibility permissions: **System Settings → Privacy & Security → Accessibility → Add the app**

> **Note**: After each new build, remove the old app from Accessibility permissions and re-add the new one.

### Development Setup

1. Clone/download the repo
1. Install pynput: `pipx install pynput`
1. Run main.py: `python3 src/main.py`

> **Note**: Running via `python3`, or `python`, requires granting accessibility permissions to your terminal app (e.g., Terminal, iTerm2) or Python executable. Do this at your own risk. If permissions don't work, build the app with `python build.py` and run the `.app` to test keyboard simulation.

## Usage

1. Set WPM range and language
2. Paste text
3. Click **Start** (3-second delay to switch windows)

### Pause Directive

```java
System.out.println("Hello");
{{PAUSE:2}}
System.out.println("World");  // Typed after 2s pause
```

## License

MIT
