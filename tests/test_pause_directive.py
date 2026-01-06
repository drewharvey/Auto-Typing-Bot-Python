#!/usr/bin/env python3
"""
Unit tests for the Pause Directive Parser module.

Tests cover:
- Finding single and multiple pause directives
- Decimal duration parsing
- Duration validation and clamping
- Handling of invalid/malformed directives
- No conflicts with Java code syntax
- Directive removal and utility functions
"""

import sys
import os
import unittest

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pause_directive import (
    PauseDirective,
    PauseDirectiveParser,
    has_pause_directives,
    PAUSE_DIRECTIVE_PATTERN,
    MIN_PAUSE_DURATION,
    MAX_PAUSE_DURATION,
)


class TestPauseDirective(unittest.TestCase):
    """Tests for the PauseDirective dataclass."""
    
    def test_directive_creation(self):
        """Test creating a PauseDirective instance."""
        directive = PauseDirective(
            start_position=0,
            end_position=11,
            duration=2.0,
            raw_text="{{PAUSE:2}}"
        )
        self.assertEqual(directive.start_position, 0)
        self.assertEqual(directive.end_position, 11)
        self.assertEqual(directive.duration, 2.0)
        self.assertEqual(directive.raw_text, "{{PAUSE:2}}")
    
    def test_directive_length_property(self):
        """Test the length property calculation."""
        directive = PauseDirective(
            start_position=5,
            end_position=16,
            duration=2.0,
            raw_text="{{PAUSE:2}}"
        )
        self.assertEqual(directive.length, 11)
    
    def test_directive_length_with_decimal(self):
        """Test length property with decimal duration directive."""
        directive = PauseDirective(
            start_position=0,
            end_position=14,
            duration=2.5,
            raw_text="{{PAUSE:2.5}}"
        )
        self.assertEqual(directive.length, 14)


class TestPauseDirectiveParserFindAll(unittest.TestCase):
    """Tests for PauseDirectiveParser.find_all_directives()."""
    
    def setUp(self):
        """Set up parser instance for tests."""
        self.parser = PauseDirectiveParser()
    
    def test_find_single_directive(self):
        """Test finding a single pause directive."""
        text = "Hello {{PAUSE:2}} World"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 2.0)
        self.assertEqual(directives[0].start_position, 6)
        self.assertEqual(directives[0].end_position, 17)
        self.assertEqual(directives[0].raw_text, "{{PAUSE:2}}")
    
    def test_find_multiple_directives(self):
        """Test finding multiple pause directives."""
        text = "First {{PAUSE:1}} Second {{PAUSE:3.5}} Third"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 2)
        self.assertEqual(directives[0].duration, 1.0)
        self.assertEqual(directives[1].duration, 3.5)
    
    def test_find_adjacent_directives(self):
        """Test finding adjacent pause directives."""
        text = "{{PAUSE:1}}{{PAUSE:2}}{{PAUSE:3}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 3)
        self.assertEqual(directives[0].duration, 1.0)
        self.assertEqual(directives[1].duration, 2.0)
        self.assertEqual(directives[2].duration, 3.0)
    
    def test_find_no_directives(self):
        """Test text with no directives."""
        text = "Hello World, no pauses here!"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 0)
    
    def test_find_directive_at_start(self):
        """Test directive at the beginning of text."""
        text = "{{PAUSE:5}}Starting with pause"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].start_position, 0)
    
    def test_find_directive_at_end(self):
        """Test directive at the end of text."""
        text = "Ending with pause{{PAUSE:5}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].end_position, len(text))
    
    def test_empty_text(self):
        """Test with empty text."""
        directives = self.parser.find_all_directives("")
        self.assertEqual(len(directives), 0)


class TestPauseDirectiveParserDecimalDurations(unittest.TestCase):
    """Tests for decimal duration parsing."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_decimal_duration_single_digit(self):
        """Test parsing single decimal digit."""
        text = "{{PAUSE:0.5}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 0.5)
    
    def test_decimal_duration_multiple_digits(self):
        """Test parsing multiple decimal digits."""
        text = "{{PAUSE:2.75}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 2.75)
    
    def test_decimal_duration_zero_point(self):
        """Test parsing 0.X durations."""
        text = "{{PAUSE:0.1}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 0.1)
    
    def test_integer_duration(self):
        """Test that integer durations work."""
        text = "{{PAUSE:10}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 10.0)
    
    def test_zero_duration(self):
        """Test zero duration."""
        text = "{{PAUSE:0}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 0.0)


class TestPauseDirectiveParserValidation(unittest.TestCase):
    """Tests for duration validation and clamping."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_duration_below_minimum_clamped(self):
        """Test that durations below minimum are clamped."""
        # Note: regex only matches positive numbers, so we test validate_duration directly
        result = self.parser.validate_duration(-5.0)
        self.assertEqual(result, MIN_PAUSE_DURATION)
    
    def test_duration_above_maximum_clamped(self):
        """Test that durations above maximum are clamped."""
        text = "{{PAUSE:999}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, MAX_PAUSE_DURATION)
    
    def test_duration_at_maximum_boundary(self):
        """Test duration at exactly maximum."""
        text = "{{PAUSE:60}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 60.0)
    
    def test_duration_just_below_maximum(self):
        """Test duration just below maximum."""
        text = "{{PAUSE:59.99}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 59.99)
    
    def test_custom_min_max_duration(self):
        """Test parser with custom min/max duration."""
        custom_parser = PauseDirectiveParser(min_duration=1.0, max_duration=10.0)
        
        # Test clamping to custom max
        text = "{{PAUSE:20}}"
        directives = custom_parser.find_all_directives(text)
        self.assertEqual(directives[0].duration, 10.0)
        
        # Test value within range
        text2 = "{{PAUSE:5}}"
        directives2 = custom_parser.find_all_directives(text2)
        self.assertEqual(directives2[0].duration, 5.0)


class TestPauseDirectiveParserInvalidFormats(unittest.TestCase):
    """Tests for handling invalid/malformed directives."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_invalid_non_numeric_duration(self):
        """Test that non-numeric durations are not matched."""
        text = "{{PAUSE:abc}}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_invalid_empty_duration(self):
        """Test that empty duration is not matched."""
        text = "{{PAUSE:}}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_invalid_missing_duration(self):
        """Test that missing duration is not matched."""
        text = "{{PAUSE}}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_invalid_single_braces(self):
        """Test that single braces are not matched."""
        text = "{PAUSE:2}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_invalid_wrong_keyword(self):
        """Test that wrong keyword is not matched."""
        text = "{{WAIT:2}}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_invalid_lowercase(self):
        """Test that lowercase PAUSE is not matched."""
        text = "{{pause:2}}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_invalid_extra_spaces(self):
        """Test that extra spaces break the match."""
        text = "{{ PAUSE:2 }}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_invalid_negative_number_format(self):
        """Test that negative numbers are not matched (regex doesn't allow -)."""
        text = "{{PAUSE:-5}}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_invalid_multiple_decimals(self):
        """Test that multiple decimal points are not matched."""
        text = "{{PAUSE:1.2.3}}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)


class TestPauseDirectiveParserJavaCodeCompatibility(unittest.TestCase):
    """Tests to ensure no conflicts with Java code syntax."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_no_match_java_generics(self):
        """Test that Java generics are not matched."""
        text = "Map<String, List<Integer>> map = new HashMap<>();"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_no_match_java_array_init(self):
        """Test that Java array initialization is not matched."""
        text = "int[] arr = {1, 2, 3};"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_no_match_java_annotations(self):
        """Test that Java annotations are not matched."""
        text = "@Override\npublic void method() {}"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_no_match_java_lambda(self):
        """Test that Java lambda expressions are not matched."""
        text = "list.forEach(item -> { System.out.println(item); });"
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_no_match_java_string_template(self):
        """Test that string templates are not matched."""
        text = 'String template = "{name}";'
        directives = self.parser.find_all_directives(text)
        self.assertEqual(len(directives), 0)
    
    def test_no_match_java_class_body(self):
        """Test that a full Java class is not matched."""
        java_code = """
public class HelloWorld {
    private Map<String, Integer> counts = new HashMap<>();
    
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5};
        for (int num : numbers) {
            System.out.println(num);
        }
    }
    
    @Override
    public String toString() {
        return "HelloWorld{}";
    }
}
"""
        directives = self.parser.find_all_directives(java_code)
        self.assertEqual(len(directives), 0)
    
    def test_directive_embedded_in_java_code(self):
        """Test pause directive can be embedded in Java code."""
        java_code = """
public static void main(String[] args) {
    {{PAUSE:2}}
    System.out.println("Hello");
    {{PAUSE:1.5}}
    System.out.println("World");
}
"""
        directives = self.parser.find_all_directives(java_code)
        self.assertEqual(len(directives), 2)
        self.assertEqual(directives[0].duration, 2.0)
        self.assertEqual(directives[1].duration, 1.5)


class TestPauseDirectiveParserFindAtPosition(unittest.TestCase):
    """Tests for PauseDirectiveParser.find_directive_at_position()."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_find_at_exact_position(self):
        """Test finding directive at exact start position."""
        text = "Hi {{PAUSE:1}} there"
        directive = self.parser.find_directive_at_position(text, 3)
        
        self.assertIsNotNone(directive)
        self.assertEqual(directive.duration, 1.0)
        self.assertEqual(directive.start_position, 3)
    
    def test_no_directive_at_position(self):
        """Test returning None when no directive at position."""
        text = "Hi {{PAUSE:1}} there"
        directive = self.parser.find_directive_at_position(text, 0)
        
        self.assertIsNone(directive)
    
    def test_no_directive_inside_directive(self):
        """Test that position inside directive doesn't match."""
        text = "{{PAUSE:1}}"
        # Position 2 is inside the directive (at 'P')
        directive = self.parser.find_directive_at_position(text, 2)
        
        self.assertIsNone(directive)
    
    def test_find_at_position_zero(self):
        """Test finding directive at position 0."""
        text = "{{PAUSE:5}}Hello"
        directive = self.parser.find_directive_at_position(text, 0)
        
        self.assertIsNotNone(directive)
        self.assertEqual(directive.duration, 5.0)
    
    def test_find_second_directive(self):
        """Test finding second directive by position."""
        text = "{{PAUSE:1}} middle {{PAUSE:2}}"
        directive = self.parser.find_directive_at_position(text, 19)
        
        self.assertIsNotNone(directive)
        self.assertEqual(directive.duration, 2.0)


class TestPauseDirectiveParserRemove(unittest.TestCase):
    """Tests for PauseDirectiveParser.remove_all_directives()."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_remove_single_directive(self):
        """Test removing a single directive."""
        text = "Hello {{PAUSE:2}} World"
        result = self.parser.remove_all_directives(text)
        self.assertEqual(result, "Hello  World")
    
    def test_remove_multiple_directives(self):
        """Test removing multiple directives."""
        text = "A{{PAUSE:1}}B{{PAUSE:2}}C"
        result = self.parser.remove_all_directives(text)
        self.assertEqual(result, "ABC")
    
    def test_remove_from_text_without_directives(self):
        """Test removing from text with no directives."""
        text = "No directives here"
        result = self.parser.remove_all_directives(text)
        self.assertEqual(result, text)
    
    def test_remove_only_directive(self):
        """Test removing when text is only a directive."""
        text = "{{PAUSE:5}}"
        result = self.parser.remove_all_directives(text)
        self.assertEqual(result, "")
    
    def test_remove_preserves_java_code(self):
        """Test that removal preserves Java code."""
        text = "int[] arr = {1, 2}; {{PAUSE:1}} Map<K,V> m;"
        result = self.parser.remove_all_directives(text)
        self.assertEqual(result, "int[] arr = {1, 2};  Map<K,V> m;")


class TestPauseDirectiveParserUtilities(unittest.TestCase):
    """Tests for utility methods."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_get_total_pause_time(self):
        """Test calculating total pause time."""
        text = "{{PAUSE:1}}{{PAUSE:2}}{{PAUSE:0.5}}"
        total = self.parser.get_total_pause_time(text)
        self.assertEqual(total, 3.5)
    
    def test_get_total_pause_time_no_directives(self):
        """Test total pause time with no directives."""
        text = "No pauses"
        total = self.parser.get_total_pause_time(text)
        self.assertEqual(total, 0.0)
    
    def test_get_directive_count(self):
        """Test counting directives."""
        text = "{{PAUSE:1}} text {{PAUSE:2}} more {{PAUSE:3}}"
        count = self.parser.get_directive_count(text)
        self.assertEqual(count, 3)
    
    def test_get_directive_count_zero(self):
        """Test counting when no directives."""
        text = "No directives"
        count = self.parser.get_directive_count(text)
        self.assertEqual(count, 0)


class TestHasPauseDirectivesFunction(unittest.TestCase):
    """Tests for the has_pause_directives convenience function."""
    
    def test_has_directives_true(self):
        """Test returns True when directives present."""
        self.assertTrue(has_pause_directives("{{PAUSE:1}}"))
        self.assertTrue(has_pause_directives("Hello {{PAUSE:2}} World"))
    
    def test_has_directives_false(self):
        """Test returns False when no directives."""
        self.assertFalse(has_pause_directives("No pauses here"))
        self.assertFalse(has_pause_directives(""))
        self.assertFalse(has_pause_directives("{PAUSE:1}"))  # Single braces


class TestPauseDirectiveEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def setUp(self):
        self.parser = PauseDirectiveParser()
    
    def test_very_long_duration_number(self):
        """Test very long duration number."""
        text = "{{PAUSE:99999999}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, MAX_PAUSE_DURATION)
    
    def test_many_decimal_places(self):
        """Test duration with many decimal places."""
        text = "{{PAUSE:1.123456789}}"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertAlmostEqual(directives[0].duration, 1.123456789)
    
    def test_directive_on_newline(self):
        """Test directive on its own line."""
        text = "line1\n{{PAUSE:1}}\nline2"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
    
    def test_unicode_around_directive(self):
        """Test directive with unicode characters around it."""
        text = "Hello 你好 {{PAUSE:1}} World 世界"
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].duration, 1.0)
    
    def test_directive_in_multiline_string(self):
        """Test directive in multiline text."""
        text = """First line
{{PAUSE:2}}
Second line
{{PAUSE:3}}
Third line"""
        directives = self.parser.find_all_directives(text)
        
        self.assertEqual(len(directives), 2)


if __name__ == '__main__':
    # Run with verbosity
    unittest.main(verbosity=2)
