#!/usr/bin/env python3
"""
Integration tests for the Pause Directive feature.

These tests verify that pause directives work correctly within the context
of the full auto-typing system, including:
- Pause directives are not typed (skipped in output)
- Pause timing is approximately correct
- Interaction with pattern matching
- Interaction with whitespace handling
- Multiple pauses in sequence
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, call
import time

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pause_directive import PauseDirectiveParser, PauseDirective


class MockKeyboardController:
    """Mock keyboard controller that records typed characters."""
    
    def __init__(self):
        self.typed_chars = []
    
    def type(self, char):
        """Record a typed character."""
        self.typed_chars.append(char)
    
    def get_typed_text(self):
        """Return all typed characters as a string."""
        return ''.join(self.typed_chars)
    
    def reset(self):
        """Clear recorded characters."""
        self.typed_chars = []


class MockTextWidget:
    """Mock tkinter text widget for testing."""
    
    def __init__(self, text):
        self.text = text
    
    def get(self, start, end):
        """Return the text content."""
        return self.text + '\n'  # Mimics tk.END behavior


class TestPauseDirectiveNotTyped(unittest.TestCase):
    """Tests verifying that pause directives are not typed."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_single_pause_removed_from_output(self):
        """Verify single pause directive is not in typed output."""
        text = "Hello {{PAUSE:1}} World"
        expected_output = "Hello  World"
        
        # Simulate what auto_type does: skip pause directives
        output_chars = []
        position = 0
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output_chars.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output_chars), expected_output)
    
    def test_multiple_pauses_removed_from_output(self):
        """Verify multiple pause directives are not in typed output."""
        text = "A{{PAUSE:1}}B{{PAUSE:2}}C{{PAUSE:0.5}}D"
        expected_output = "ABCD"
        
        output_chars = []
        position = 0
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output_chars.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output_chars), expected_output)
    
    def test_pause_at_start_removed(self):
        """Verify pause directive at start is not typed."""
        text = "{{PAUSE:1}}Hello"
        expected_output = "Hello"
        
        output_chars = []
        position = 0
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output_chars.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output_chars), expected_output)
    
    def test_pause_at_end_removed(self):
        """Verify pause directive at end is not typed."""
        text = "Hello{{PAUSE:1}}"
        expected_output = "Hello"
        
        output_chars = []
        position = 0
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output_chars.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output_chars), expected_output)
    
    def test_adjacent_pauses_removed(self):
        """Verify adjacent pause directives are not typed."""
        text = "X{{PAUSE:1}}{{PAUSE:2}}Y"
        expected_output = "XY"
        
        output_chars = []
        position = 0
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output_chars.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output_chars), expected_output)


class TestPauseDirectiveWithJavaCode(unittest.TestCase):
    """Tests for pause directives embedded in Java code."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_pause_in_java_method(self):
        """Test pause directive in Java method body."""
        java_code = """public static void main(String[] args) {
    {{PAUSE:2}}
    System.out.println("Hello");
}"""
        expected_output = """public static void main(String[] args) {
    
    System.out.println("Hello");
}"""
        
        output_chars = []
        position = 0
        while position < len(java_code):
            directive = self.parser.find_directive_at_position(java_code, position)
            if directive:
                position = directive.end_position
                continue
            output_chars.append(java_code[position])
            position += 1
        
        self.assertEqual(''.join(output_chars), expected_output)
    
    def test_multiple_pauses_in_java_code(self):
        """Test multiple pause directives in Java code."""
        java_code = """{{PAUSE:1}}public class Test {
    {{PAUSE:0.5}}
    private int value;
    {{PAUSE:2}}
}"""
        
        # Count directives
        directives = self.parser.find_all_directives(java_code)
        self.assertEqual(len(directives), 3)
        
        # Verify cleaned output
        cleaned = self.parser.remove_all_directives(java_code)
        self.assertNotIn("{{PAUSE", cleaned)
        self.assertIn("public class Test", cleaned)
        self.assertIn("private int value", cleaned)
    
    def test_java_code_without_pauses_unchanged(self):
        """Test that Java code without pauses is unchanged."""
        java_code = """public class Test {
    Map<String, List<Integer>> map = new HashMap<>();
    int[] arr = {1, 2, 3};
}"""
        
        output_chars = []
        position = 0
        while position < len(java_code):
            directive = self.parser.find_directive_at_position(java_code, position)
            if directive:
                position = directive.end_position
                continue
            output_chars.append(java_code[position])
            position += 1
        
        self.assertEqual(''.join(output_chars), java_code)


class TestPauseDirectiveTiming(unittest.TestCase):
    """Tests for pause directive timing behavior."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_pause_duration_extracted_correctly(self):
        """Test that pause durations are extracted correctly."""
        test_cases = [
            ("{{PAUSE:1}}", 1.0),
            ("{{PAUSE:0.5}}", 0.5),
            ("{{PAUSE:2.5}}", 2.5),
            ("{{PAUSE:10}}", 10.0),
            ("{{PAUSE:0}}", 0.0),
        ]
        
        for text, expected_duration in test_cases:
            with self.subTest(text=text):
                directive = self.parser.find_directive_at_position(text, 0)
                self.assertIsNotNone(directive)
                self.assertEqual(directive.duration, expected_duration)
    
    def test_total_pause_time_calculation(self):
        """Test calculation of total pause time."""
        text = "A{{PAUSE:1}}B{{PAUSE:2}}C{{PAUSE:0.5}}D"
        total = self.parser.get_total_pause_time(text)
        self.assertEqual(total, 3.5)
    
    def test_pause_timing_with_mock_sleep(self):
        """Test that pause triggers sleep with correct duration."""
        text = "Hello{{PAUSE:2}}World"
        
        sleep_calls = []
        
        def mock_sleep(duration):
            sleep_calls.append(duration)
        
        # Simulate auto_type behavior
        position = 0
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                mock_sleep(directive.duration)
                position = directive.end_position
                continue
            position += 1
        
        self.assertEqual(len(sleep_calls), 1)
        self.assertEqual(sleep_calls[0], 2.0)
    
    def test_multiple_pauses_timing(self):
        """Test timing with multiple pauses."""
        text = "{{PAUSE:1}}A{{PAUSE:0.5}}B{{PAUSE:2}}"
        
        sleep_calls = []
        
        def mock_sleep(duration):
            sleep_calls.append(duration)
        
        position = 0
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                mock_sleep(directive.duration)
                position = directive.end_position
                continue
            position += 1
        
        self.assertEqual(len(sleep_calls), 3)
        self.assertEqual(sleep_calls, [1.0, 0.5, 2.0])


class TestPauseDirectivePositionTracking(unittest.TestCase):
    """Tests for correct position tracking after pause directives."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_position_after_single_pause(self):
        """Test position is correct after single pause."""
        text = "AB{{PAUSE:1}}CD"
        
        position = 0
        chars_typed = []
        
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            chars_typed.append((position, text[position]))
            position += 1
        
        # Should have typed A at 0, B at 1, C at 13, D at 14
        self.assertEqual(chars_typed[0], (0, 'A'))
        self.assertEqual(chars_typed[1], (1, 'B'))
        self.assertEqual(chars_typed[2], (13, 'C'))
        self.assertEqual(chars_typed[3], (14, 'D'))
    
    def test_position_with_newlines_and_pause(self):
        """Test position tracking with newlines around pause."""
        text = "line1\n{{PAUSE:1}}\nline2"
        
        position = 0
        output = []
        
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output), "line1\n\nline2")


class TestPauseDirectiveWithPatternMatcher(unittest.TestCase):
    """Tests for pause directive interaction with pattern matching."""
    
    def setUp(self):
        self.pause_parser = PauseDirectiveParser()
    
    def test_pause_before_keyword(self):
        """Test pause directive before a Java keyword."""
        text = "{{PAUSE:1}}public class Test"
        
        output = []
        position = 0
        pause_executed = False
        
        while position < len(text):
            directive = self.pause_parser.find_directive_at_position(text, position)
            if directive:
                pause_executed = True
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        self.assertTrue(pause_executed)
        self.assertEqual(''.join(output), "public class Test")
    
    def test_pause_after_keyword(self):
        """Test pause directive after a Java keyword."""
        text = "public{{PAUSE:1}} class Test"
        
        output = []
        position = 0
        
        while position < len(text):
            directive = self.pause_parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output), "public class Test")
    
    def test_pause_between_keywords(self):
        """Test pause directive between Java keywords."""
        text = "public static{{PAUSE:2}} void main"
        
        output = []
        position = 0
        
        while position < len(text):
            directive = self.pause_parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output), "public static void main")


class TestPauseDirectiveResumeScenarios(unittest.TestCase):
    """Tests for pause/resume scenarios with pause directives."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_resume_at_pause_directive(self):
        """Test resuming when position is at a pause directive."""
        text = "Hello{{PAUSE:1}}World"
        
        # Simulate typing stopped at position 5 (just before pause)
        start_position = 5
        
        output = []
        position = start_position
        
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output), "World")
    
    def test_resume_after_pause_directive(self):
        """Test resuming when position is right after a pause directive."""
        text = "Hello{{PAUSE:1}}World"
        
        # Position 16 is right after the pause directive (at 'W')
        start_position = 16
        
        output = []
        position = start_position
        
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output), "World")


class TestPauseDirectiveLineStartTracking(unittest.TestCase):
    """Tests for line-start tracking with pause directives."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_pause_directive_at_line_start(self):
        """Test pause directive at the start of a line."""
        text = "line1\n{{PAUSE:1}}line2"
        
        output = []
        position = 0
        at_line_start = True
        
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                # After pause, check if at line start
                if position > 0 and position < len(text):
                    at_line_start = (text[position - 1] == '\n')
                continue
            
            char = text[position]
            output.append(char)
            
            if char == '\n':
                at_line_start = True
            elif char not in ' \t':
                at_line_start = False
            
            position += 1
        
        self.assertEqual(''.join(output), "line1\nline2")
    
    def test_pause_between_newlines(self):
        """Test pause directive between newlines."""
        text = "line1\n{{PAUSE:1}}\nline2"
        
        # The pause is on its own line
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 1)
        
        cleaned = self.parser.remove_all_directives(text)
        self.assertEqual(cleaned, "line1\n\nline2")


class TestPauseDirectiveEdgeCasesIntegration(unittest.TestCase):
    """Integration tests for edge cases."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_only_pause_directive(self):
        """Test text that is only a pause directive."""
        text = "{{PAUSE:1}}"
        
        output = []
        position = 0
        
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output), "")
    
    def test_empty_text(self):
        """Test empty text."""
        text = ""
        
        output = []
        position = 0
        
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        self.assertEqual(''.join(output), "")
    
    def test_malformed_directive_typed_literally(self):
        """Test that malformed directives are typed literally."""
        text = "Hello {{PAUSE:abc}} World"
        
        output = []
        position = 0
        
        while position < len(text):
            directive = self.parser.find_directive_at_position(text, position)
            if directive:
                position = directive.end_position
                continue
            output.append(text[position])
            position += 1
        
        # Malformed directive should be typed as-is
        self.assertEqual(''.join(output), "Hello {{PAUSE:abc}} World")
    
    def test_very_long_pause_clamped(self):
        """Test that very long pause is clamped to maximum."""
        text = "{{PAUSE:9999}}"
        
        directive = self.parser.find_directive_at_position(text, 0)
        self.assertIsNotNone(directive)
        self.assertEqual(directive.duration, 60.0)  # Clamped to max


if __name__ == '__main__':
    unittest.main(verbosity=2)
