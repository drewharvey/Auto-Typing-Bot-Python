"""
Help window for Auto Typing Tool.

Provides platform-specific help and setup instructions.
"""

import platform
from tkinter import messagebox


# Help text sections
_PAUSE_FEATURE_INFO = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAUSE DIRECTIVE FEATURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add pauses during typing using the {{PAUSE:X}} syntax:

  {{PAUSE:2}}       Pause for 2 seconds
  {{PAUSE:0.5}}     Pause for 0.5 seconds
  {{PAUSE:10}}      Pause for 10 seconds

• The pause directive is executed but NOT typed
• Maximum pause duration: 60 seconds
• Syntax uses double curly braces (won't conflict with Java)

Example in code:
  public static void main(String[] args) {
      {{PAUSE:2}}
      System.out.println("After 2 second pause");
  }
"""

_MACOS_HELP = """AUTO TYPING TOOL - HELP

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
macOS ACCESSIBILITY SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For the Auto Typing Tool to work on macOS, you need to grant accessibility permissions:

1. Open System Settings (or System Preferences)
2. Navigate to Privacy & Security
3. Click on Accessibility
4. Click the lock icon (🔒) to make changes
5. Enter your password if prompted
6. Find "Python" or "Auto-Typing-Tool" in the list
7. Enable the checkbox next to it
8. If not in the list, click the '+' button and add it

Note: You may need to restart the application after granting permissions.
""" + _PAUSE_FEATURE_INFO

_OTHER_PLATFORM_HELP = """AUTO TYPING TOOL - HELP

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SETUP INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This tool uses keyboard automation to simulate typing.

macOS Users:
• Enable accessibility permissions
• Go to: System Settings → Privacy & Security → Accessibility
• Add Python or Auto-Typing-Tool to allowed applications

Linux Users:
• Should work without special permissions
• Ensure pynput is installed (pip install pynput)

Windows Users:
• Should work without special permissions
• Some antivirus software may require approval
""" + _PAUSE_FEATURE_INFO + """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you encounter issues, check that:
• pynput library is installed
• You have proper keyboard control permissions
• No other application is blocking keyboard input"""


class HelpWindow:
    """Help window displaying setup instructions and feature documentation."""
    
    TITLE = "Auto Typing Tool - Help"
    
    @staticmethod
    def _get_help_text() -> str:
        """Get platform-appropriate help text."""
        if platform.system() == "Darwin":
            return _MACOS_HELP
        return _OTHER_PLATFORM_HELP
    
    @classmethod
    def open(cls) -> None:
        """Open the help dialog."""
        messagebox.showinfo(cls.TITLE, cls._get_help_text())
