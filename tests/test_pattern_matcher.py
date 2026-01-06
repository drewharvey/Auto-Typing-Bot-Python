#!/usr/bin/env python3
"""
Unit tests for PatternMatcher class.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pattern_matcher import PatternMatcher


class TestPatternDetection(unittest.TestCase):
    """Tests for pattern detection in code."""
    
    def setUp(self):
        self.matcher = PatternMatcher('java')
    
    def test_detects_public_keyword(self):
        """Test detection of 'public' keyword."""
        result = self.matcher.find_pattern_at_position("public class Test", 0)
        self.assertIsNotNone(result)
        self.assertEqual(result['matched_text'], 'public')
    
    def test_detects_static_keyword(self):
        """Test detection of 'static' keyword."""
        text = "public static void main"
        pos = text.index('static')
        result = self.matcher.find_pattern_at_position(text, pos)
        self.assertIsNotNone(result)
        self.assertEqual(result['matched_text'], 'static')
    
    def test_detects_boilerplate_pattern(self):
        """Test detection of boilerplate like System.out.println."""
        result = self.matcher.find_pattern_at_position("System.out.println(\"test\");", 0)
        self.assertIsNotNone(result)
        self.assertEqual(result['matched_text'], 'System.out.println')
    
    def test_detects_annotation(self):
        """Test detection of @Override annotation."""
        result = self.matcher.find_pattern_at_position("@Override", 0)
        self.assertIsNotNone(result)
        self.assertEqual(result['matched_text'], '@Override')
    
    def test_no_pattern_for_variable_name(self):
        """Test that custom variable names don't match patterns."""
        result = self.matcher.find_pattern_at_position("myCustomVariable = 5", 0)
        self.assertIsNone(result)
    
    def test_pattern_has_speed_multiplier(self):
        """Test that detected patterns have speed multiplier."""
        result = self.matcher.find_pattern_at_position("public", 0)
        self.assertIsNotNone(result)
        self.assertIn('speed_multiplier', result)
        self.assertGreater(result['speed_multiplier'], 1.0)


class TestLanguageSwitching(unittest.TestCase):
    """Tests for switching between languages."""
    
    def setUp(self):
        self.matcher = PatternMatcher('java')
    
    def test_switch_to_javascript(self):
        """Test switching to JavaScript mode."""
        self.matcher.set_language('javascript')
        self.assertEqual(self.matcher.language, 'javascript')
        
        result = self.matcher.find_pattern_at_position("const x = 5", 0)
        self.assertIsNotNone(result)
        self.assertEqual(result['matched_text'], 'const')
    
    def test_switch_back_to_java(self):
        """Test switching back to Java mode."""
        self.matcher.set_language('javascript')
        self.matcher.set_language('java')
        
        result = self.matcher.find_pattern_at_position("public class", 0)
        self.assertIsNotNone(result)
        self.assertEqual(result['matched_text'], 'public')
    
    def test_java_specific_pattern(self):
        """Test Java-specific pattern detection."""
        result = self.matcher.find_pattern_at_position("public static void main", 0)
        self.assertIsNotNone(result)


class TestSpeedMultipliers(unittest.TestCase):
    """Tests for speed multiplier values."""
    
    def setUp(self):
        self.matcher = PatternMatcher('java')
    
    def test_keyword_speed_multiplier(self):
        """Test that keywords have appropriate speed multiplier."""
        result = self.matcher.find_pattern_at_position("public", 0)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result['speed_multiplier'], 1.5)
    
    def test_boilerplate_faster_than_keyword(self):
        """Test that boilerplate is typed faster than keywords."""
        keyword = self.matcher.find_pattern_at_position("public", 0)
        boilerplate = self.matcher.find_pattern_at_position("System.out.println", 0)
        
        self.assertIsNotNone(keyword)
        self.assertIsNotNone(boilerplate)
        self.assertGreaterEqual(boilerplate['speed_multiplier'], keyword['speed_multiplier'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
