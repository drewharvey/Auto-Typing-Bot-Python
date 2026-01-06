#!/usr/bin/env python3
"""
Unit tests for whitespace skipping functionality.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def simulate_whitespace_skip(text, ignore_leading_whitespace):
    """Simulate the auto-type whitespace skipping logic.
    
    Args:
        text: Text to process
        ignore_leading_whitespace: Whether to skip leading whitespace
        
    Returns:
        String that would actually be typed
    """
    result = []
    at_line_start = True
    
    for char in text:
        if ignore_leading_whitespace and at_line_start and char in ' \t':
            continue
        
        if char not in ' \t':
            at_line_start = False
        
        result.append(char)
        
        if char == '\n':
            at_line_start = True
    
    return ''.join(result)


class TestWhitespaceSkipping(unittest.TestCase):
    """Tests for whitespace skipping logic."""
    
    def test_skips_leading_spaces(self):
        """Test that leading spaces are skipped."""
        text = "line1\n    indented"
        result = simulate_whitespace_skip(text, True)
        
        self.assertNotIn("    indented", result)
        self.assertIn("indented", result)
    
    def test_skips_leading_tabs(self):
        """Test that leading tabs are skipped."""
        text = "line1\n\t\tindented"
        result = simulate_whitespace_skip(text, True)
        
        self.assertNotIn("\t\tindented", result)
        self.assertIn("indented", result)
    
    def test_skips_mixed_whitespace(self):
        """Test that mixed spaces and tabs are skipped."""
        text = "line1\n \t  indented"
        result = simulate_whitespace_skip(text, True)
        
        self.assertIn("indented", result)
        self.assertFalse(result.startswith(" ") or result.split('\n')[1].startswith(" "))
    
    def test_preserves_inline_whitespace(self):
        """Test that whitespace within lines is preserved."""
        text = "int x = 5"
        result = simulate_whitespace_skip(text, True)
        
        self.assertEqual(result, text)
        self.assertIn(" = ", result)
    
    def test_preserves_empty_lines(self):
        """Test that empty lines are preserved."""
        text = "line1\n\nline2"
        result = simulate_whitespace_skip(text, True)
        
        self.assertIn("\n\n", result)
    
    def test_disabled_preserves_all(self):
        """Test that when disabled, all whitespace is preserved."""
        text = "line1\n    indented"
        result = simulate_whitespace_skip(text, False)
        
        self.assertEqual(result, text)
    
    def test_java_code_indentation(self):
        """Test with typical Java code indentation."""
        text = """public class Test {
    void method() {
        int x = 5;
    }
}"""
        result = simulate_whitespace_skip(text, True)
        
        self.assertIn("void method()", result)
        self.assertIn("int x = 5;", result)
        self.assertNotIn("    void", result)
        self.assertNotIn("        int", result)


class TestWhitespaceResume(unittest.TestCase):
    """Tests for whitespace handling when resuming."""
    
    def simulate_resume(self, text, ignore_whitespace, pause_pos):
        """Simulate resume from a position."""
        result = []
        
        # First pass up to pause
        at_line_start = True
        for i in range(pause_pos):
            char = text[i]
            if ignore_whitespace and at_line_start and char in ' \t':
                continue
            if char not in ' \t':
                at_line_start = False
            result.append(char)
            if char == '\n':
                at_line_start = True
        
        # Resume: recalculate line start
        if pause_pos > 0:
            at_line_start = (text[pause_pos - 1] == '\n')
        else:
            at_line_start = True
        
        # Second pass from pause
        for i in range(pause_pos, len(text)):
            char = text[i]
            if ignore_whitespace and at_line_start and char in ' \t':
                continue
            if char not in ' \t':
                at_line_start = False
            result.append(char)
            if char == '\n':
                at_line_start = True
        
        return ''.join(result)
    
    def test_resume_mid_line(self):
        """Test resuming in middle of a line."""
        text = "public class Test {\n    void method()\n}"
        pause_pos = 10  # Middle of first line
        
        result = self.simulate_resume(text, True, pause_pos)
        
        self.assertIn("void method()", result)
        self.assertNotIn("    void", result)
    
    def test_resume_after_newline(self):
        """Test resuming right after a newline."""
        text = "line1\n    line2"
        pause_pos = 6  # Right after newline
        
        result = self.simulate_resume(text, True, pause_pos)
        
        self.assertIn("line2", result)
        self.assertNotIn("    line2", result)
    
    def test_resume_from_start(self):
        """Test resuming from position 0."""
        text = "    indented"
        
        result = self.simulate_resume(text, True, 0)
        
        self.assertEqual(result, "indented")


if __name__ == '__main__':
    unittest.main(verbosity=2)
