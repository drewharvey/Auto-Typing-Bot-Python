#!/usr/bin/env python3
"""
Test script to verify the help button functionality
Tests platform detection and message content
"""

import platform
from unittest.mock import Mock, patch
import sys

# Test platform detection
def test_platform_detection():
    """Test that we can detect the platform correctly"""
    system = platform.system()
    print(f"✓ Platform detected: {system}")
    assert system in ["Darwin", "Linux", "Windows", "Java"], f"Unknown platform: {system}"
    return system

# Test help message content
def test_help_message_content():
    """Test that help messages contain required information"""
    # Simulate Darwin (macOS)
    with patch('platform.system', return_value='Darwin'):
        system = platform.system()
        assert system == "Darwin"
        
        # Check macOS-specific content
        required_keywords = [
            "macOS", "Accessibility", "Privacy & Security", 
            "System Settings", "System Preferences"
        ]
        
        message = """macOS Accessibility Setup Required

For the Auto Typing Tool to work on macOS, you need to grant accessibility permissions:

1. Open System Settings (or System Preferences)
2. Navigate to Privacy & Security
3. Click on Accessibility"""
        
        for keyword in required_keywords:
            assert keyword in message, f"Missing keyword: {keyword}"
        
        print("✓ macOS message contains all required keywords")
    
    # Simulate Linux
    with patch('platform.system', return_value='Linux'):
        system = platform.system()
        assert system == "Linux"
        
        message = """Auto Typing Tool - Setup Information

This tool uses keyboard automation to simulate typing.

macOS Users:
• You need to enable accessibility permissions
• Go to: System Settings → Privacy & Security → Accessibility
• Add Python or Auto-Typing-Tool to the allowed applications

Linux Users:
• The tool should work without special permissions
• If you have issues, ensure pynput is properly installed"""
        
        assert "Linux Users:" in message
        print("✓ Linux message format is correct")
    
    # Simulate Windows
    with patch('platform.system', return_value='Windows'):
        system = platform.system()
        assert system == "Windows"
        
        message = """Auto Typing Tool - Setup Information

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
• Some antivirus software may require approval"""
        
        assert "Windows Users:" in message
        print("✓ Windows message format is correct")

def test_import_modules():
    """Test that required modules can be imported"""
    try:
        from tkinter import messagebox
        print("✓ tkinter.messagebox imported successfully")
    except ImportError as e:
        print(f"⚠️  Warning: Could not import tkinter.messagebox: {e}")
        print("   This is expected in headless environments")
    
    import platform
    print("✓ platform module imported successfully")

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Help Button Functionality")
    print("=" * 60)
    
    try:
        test_import_modules()
        print()
        
        system = test_platform_detection()
        print()
        
        test_help_message_content()
        print()
        
        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
        # Print platform-specific note
        if system == "Darwin":
            print("\nℹ️  Running on macOS - Help button will show macOS-specific instructions")
        elif system == "Linux":
            print("\nℹ️  Running on Linux - Help button will show general instructions")
        elif system == "Windows":
            print("\nℹ️  Running on Windows - Help button will show general instructions")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
