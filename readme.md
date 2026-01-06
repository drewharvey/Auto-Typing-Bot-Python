# Auto Typing Tool

Welcome to the **Auto Typing Tool**, an advanced, fast, and optimized solution for automated typing tasks, built with Python! This tool is designed to save time and effort, offering unmatched speed and precision. Whether you need a bot for text simulation or just an auto typer to handle repetitive tasks, this is the fastest and best choice.

![Auto Typing GUI Screenshot](auto-typer-screen.png)

## Features

### 🚀 Speed and Performance
- **Human-like typing speed variation**: Typing speed dynamically adjusts based on code patterns for more realistic simulation
  - Keywords (public, static, void, etc.) are typed ~1.8x faster
  - Common boilerplate (System.out.println, etc.) typed ~2.0x faster  
  - Bracket pairs (<>, [], (), {}) typed ~3.0x faster
  - Natural pauses after punctuation (semicolons, braces)
- Adjustable typing speed with **Min WPM** and **Max WPM**.
- Smooth, natural typing simulation using the `pynput` library.
- **Optimized typing delays** for realistic performance.
- Speed adjustment: Increase typing speed dynamically by **1.5x**.
- **Pattern recognition** for Java, JavaScript, TypeScript, React, CSS, Python, C++, and C# code

### 💻 User-Friendly Interface
- Built with **Tkinter**, providing a clean and interactive GUI.
- Editable input fields for custom text and speed control.
- Real-time status updates for better usability.
- Language selection dropdown to optimize typing for specific programming languages
- **Help button** with setup instructions for accessibility permissions (especially for macOS users)

### 🔄 Typing Controls
- **Start**: Begin typing with your configured speed.
- **Pause**: Temporarily halt the typing process.
- **Continue**: Resume typing seamlessly.
- **Stop**: Stop and reset the progress at any time.
- **Ignore leading whitespace**: Toggle to skip leading spaces/tabs at the beginning of lines (useful for IDEs with auto-indent)

### 🧠 Intelligent Design
- Handles large text inputs effortlessly.
- Dynamically calculates delay per character for optimized performance.
- Safe and robust threading to ensure smooth operation.

## Getting Started

Follow these steps to set up and run the Auto Typing Tool on your system.

### Prerequisites
Make sure you have the following installed:
- **Python 3.6+**
- Required libraries:
  - `tkinter`
  - `pynput`

You can install the `pynput` library using pip:
```bash
pip install pynput
```

#### macOS Users - Important Setup Step
On macOS, you need to grant accessibility permissions for the app to simulate keyboard input:

1. Open **System Settings** (or **System Preferences** on older versions)
2. Navigate to **Privacy & Security**
3. Click on **Accessibility**
4. Click the lock icon (🔒) to make changes
5. Enter your password when prompted
6. Find **Python** or **Auto-Typing-Tool** in the list and enable it
7. If not listed, click the **+** button and add the application

You can also click the **ℹ️ Help** button in the application for detailed setup instructions.

**Note:** You may need to restart the application after granting permissions.

### Installation
1. Clone the repository or download the script.
2. Save the file as `auto_typing_tool.py`.
3. Open a terminal and navigate to the script’s directory.

### Running the Application
To start the Auto Typing Tool:
```bash
python auto_typing_tool.py
```
This will launch the graphical interface where you can configure typing parameters and start auto typing.

## How to Use

1. **Get Help (if needed)**:
   - Click the **ℹ️ Help** button to view setup instructions, especially for macOS accessibility permissions.
2. **Set Typing Speed**:
   - Enter desired values for **Min WPM** and **Max WPM** in the input fields.
3. **Select Language**:
   - Choose your programming language from the dropdown (Java, JavaScript, TypeScript, React, CSS, Python, C++, C#).
   - The tool will automatically apply human-like speed variations based on language-specific patterns.
4. **Configure Whitespace Handling** (optional):
   - Check **"Ignore leading whitespace"** if typing into an IDE that automatically adds indentation.
   - This prevents duplicate indentation by skipping spaces/tabs at the beginning of lines.
   - Useful for IntelliJ IDEA, VS Code, PyCharm, and other IDEs with auto-indent features.
5. **Input Text**:
   - Paste or type your target text (e.g., Java code) in the **Main Text** field.
6. **Start Typing**:
   - Click the **Start** button to begin the auto typing process.
   - The tool will vary typing speed based on detected code patterns for a more realistic experience.
7. **Control Typing**:
   - Use the **Pause**, **Continue**, and **Stop** buttons to control the operation.
8. **Boost Speed**:
   - Click the **Increase Speed** button to raise the typing speed by 1.5x instantly.

## System Functionalities

| Functionality         | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| **Help Button**       | Displays setup instructions, including macOS accessibility permissions.    |
| **Start Typing**      | Begins typing the text at the configured speed with human-like variations. |
| **Pause Typing**      | Pauses the typing process temporarily.                                     |
| **Continue Typing**   | Resumes typing from where it was paused.                                   |
| **Stop Typing**       | Stops the typing process and resets progress.                              |
| **Increase Speed**    | Dynamically increases typing speed by 1.5x, updating WPM values.           |
| **Language Selection**| Choose programming language for optimized pattern-based typing.            |
| **Pattern Recognition**| Automatically detects code patterns and adjusts typing speed accordingly.  |
| **Ignore Leading Whitespace**| Skips leading spaces/tabs at line starts to prevent duplicate indentation in IDEs. |
| **GUI Interaction**   | Intuitive interface for configuring and controlling the auto typing bot.   |

## Technical Details

- **Language**: Python
- **Frameworks**: Tkinter for GUI, Pynput for keyboard simulation.
- **Pattern Recognition**: Custom pattern matcher for language-specific code patterns.
- **Threading**: Ensures seamless typing without freezing the interface.
- **Intelligent Speed Variation**: Applies different typing speeds based on:
  - Keywords (e.g., `public`, `class`, `int`) - 1.8x faster
  - Boilerplate code (e.g., `System.out.println`, `public static void main`) - 2.0x faster
  - Bracket pairs (e.g., `{}`, `[]`, `()`, `<>`) - 3.0x faster
  - Operators and punctuation - Variable speeds with natural pauses
  - Custom identifiers - Base typing speed
- **Logging**: Debug logs saved to `auto_typing_debug.log` in your system's temp directory for troubleshooting.

## Why Choose This Auto Typing Tool?

- **Fastest Auto Typer**: Configurable speeds ensure you’re always ahead.
- **Best Python Typing Bot**: Built with clean, modular code.
- **SEO-Optimized**: Perfect for text simulation, writing bots, and automation tasks.
- **Lightweight and Efficient**: Requires minimal resources to operate.

## Contribution

We welcome contributions to improve this Auto Typing Tool! Feel free to fork the repository, create new features, or optimize the existing ones.

## License
This project is licensed under the MIT License. You’re free to use, modify, and distribute this tool as long as proper credit is given.

---

Download, run, and experience the fastest and best **Auto Typing Bot** built with Python today!


## Testing the Features

You can test the features without running the GUI:

```bash
# Run the pattern detection test
python3 test_pattern_typing.py

# Run the typing speed demonstration
python3 demo_typing_speed.py

# Test the whitespace ignore feature
python3 test_whitespace_ignore.py

# Demonstrate the whitespace ignore feature
python3 demo_whitespace_feature.py

# Test resume functionality with whitespace handling
python3 test_resume_whitespace.py
```

These scripts will show you how the tool detects code patterns and applies speed variations.
