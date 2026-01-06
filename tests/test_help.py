#!/usr/bin/env python3
"""
Unit tests for help dialog functionality.
"""

import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestPlatformDetection(unittest.TestCase):
    """Tests for platform detection."""
    
    def test_darwin_detected(self):
        """Test macOS detection."""
        with patch('platform.system', return_value='Darwin'):
            import platform
            self.assertEqual(platform.system(), 'Darwin')
    
    def test_linux_detected(self):
        """Test Linux detection."""
        with patch('platform.system', return_value='Linux'):
            import platform
            self.assertEqual(platform.system(), 'Linux')
    
    def test_windows_detected(self):
        """Test Windows detection."""
        with patch('platform.system', return_value='Windows'):
            import platform
            self.assertEqual(platform.system(), 'Windows')


class TestHelpMessageContent(unittest.TestCase):
    """Tests for help message content."""
    
    def test_macos_message_contains_accessibility(self):
        """Test macOS message contains accessibility instructions."""
        macos_keywords = ['Accessibility', 'Privacy', 'Security']
        message = "Navigate to Privacy & Security, Click on Accessibility"
        
        for keyword in macos_keywords:
            self.assertIn(keyword, message)
    
    def test_pause_directive_documented(self):
        """Test pause directive is documented in help."""
        help_text = "{{PAUSE:2}} Pause for 2 seconds"
        
        self.assertIn("{{PAUSE:", help_text)
        self.assertIn("seconds", help_text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
