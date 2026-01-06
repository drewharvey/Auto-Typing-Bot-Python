#!/usr/bin/env python3
"""
Demo script to show the help button functionality
This demonstrates what the popup looks like without requiring a full GUI
"""

import platform

def show_help_text_for_platform(system):
    """Display help text based on platform."""
    print("=" * 70)
    print(f"Demo: Help Button Popup for {system}")
    print("=" * 70)
    print()
    
    if system == "Darwin":  # macOS
        print("TITLE: Setup Information")
        print()
        print("MESSAGE:")
        print("-" * 70)
        print("""macOS Accessibility Setup Required

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

Alternative path:
System Settings → Privacy & Security → Accessibility → Add Python/Auto-Typing-Tool

For more help, check your macOS version's documentation on accessibility permissions.""")
    else:
        print("TITLE: Setup Information")
        print()
        print("MESSAGE:")
        print("-" * 70)
        print("""Auto Typing Tool - Setup Information

This tool uses keyboard automation to simulate typing.

macOS Users:
• You need to enable accessibility permissions
• Go to: System Settings → Privacy & Security → Accessibility
• Add Python or Auto-Typing-Tool to the allowed applications

Linux Users:
• The tool should work without special permissions
• If you have issues, ensure pynput is properly installed

Windows Users:
• The tool should work without special permissions
• Some antivirus software may require approval

If you encounter any issues, please check that:
• pynput library is installed (pip install pynput)
• You have proper permissions to control the keyboard
• No other application is blocking keyboard input""")
    
    print("-" * 70)
    print()

def main():
    """Main demo function."""
    print()
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║          Auto Typing Tool - Help Button Demo                     ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print()
    
    # Show current system
    current_system = platform.system()
    print(f"Current System: {current_system}")
    print()
    
    # Show help for current system
    show_help_text_for_platform(current_system)
    
    # If not on macOS, also show macOS version for demonstration
    if current_system != "Darwin":
        print()
        print("─" * 70)
        print("For demonstration, here's what macOS users would see:")
        print("─" * 70)
        print()
        show_help_text_for_platform("Darwin")
    
    print()
    print("✅ Demo complete!")
    print()
    print("In the actual GUI application:")
    print("  • The 'ℹ️ Help' button appears in the top-right of the window")
    print("  • Clicking it opens a popup with the appropriate message")
    print("  • The message is platform-specific based on the OS")
    print()

if __name__ == "__main__":
    main()
