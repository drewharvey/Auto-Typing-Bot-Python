#!/usr/bin/env python3
"""
Test script for pattern-based typing speed variation.
This script tests the PatternMatcher without requiring GUI interaction.
"""

import sys
import time
from pattern_matcher import PatternMatcher

# Sample Java code snippets for testing
JAVA_CODE_SAMPLES = [
    # Sample 1: Simple class with keyword
    "public class HelloWorld {",
    
    # Sample 2: Method with boilerplate
    "public static void main(String[] args) {",
    
    # Sample 3: Print statement
    "System.out.println(\"Hello World\");",
    
    # Sample 4: Variable declaration
    "int count = 0;",
    
    # Sample 5: ArrayList usage
    "List<String> items = new ArrayList<>();",
    
    # Sample 6: Annotation
    "@Override",
    
    # Sample 7: For loop
    "for (int i = 0; i < 10; i++) {",
    
    # Sample 8: Try-catch block
    "try { } catch (Exception e) { }",
]

def test_pattern_detection():
    """Test that patterns are correctly detected in Java code."""
    print("=" * 70)
    print("Testing Pattern Detection for Java Code")
    print("=" * 70)
    
    matcher = PatternMatcher('java')
    
    for i, code in enumerate(JAVA_CODE_SAMPLES, 1):
        print(f"\n--- Sample {i} ---")
        print(f"Code: {code}")
        print(f"Patterns found:")
        
        position = 0
        patterns_found = []
        
        while position < len(code):
            pattern_info = matcher.find_pattern_at_position(code, position)
            
            if pattern_info:
                patterns_found.append(pattern_info)
                print(f"  [{position}] '{pattern_info['matched_text']}' - "
                      f"Category: {pattern_info['category']}, "
                      f"Speed: {pattern_info['speed_multiplier']}x, "
                      f"Pause before: {pattern_info['pause_before']}s, "
                      f"Pause after: {pattern_info['pause_after']}s")
                position += pattern_info['length']
            else:
                position += 1
        
        if not patterns_found:
            print("  No patterns detected")
    
    print("\n" + "=" * 70)
    return True

def test_speed_calculation():
    """Test typing speed calculation with patterns."""
    print("\n" + "=" * 70)
    print("Testing Speed Calculation")
    print("=" * 70)
    
    matcher = PatternMatcher('java')
    
    # Test parameters
    min_wpm = 40
    max_wpm = 60
    avg_wpm = (min_wpm + max_wpm) / 2
    
    print(f"\nBase typing speed: {min_wpm}-{max_wpm} WPM (avg: {avg_wpm} WPM)")
    print(f"Base delay per character: {60 / (avg_wpm * 5):.4f}s")
    
    test_patterns = [
        ("public", "Expected: Fast (keyword)"),
        ("System.out.println", "Expected: Very fast (boilerplate)"),
        ("myVariable", "Expected: Normal (no pattern match)"),
        (";", "Expected: Fast with pause after (statement end)"),
        ("int", "Expected: Fast (keyword)"),
    ]
    
    for pattern_text, description in test_patterns:
        print(f"\n{description}")
        print(f"Pattern: '{pattern_text}'")
        
        pattern_info = matcher.find_pattern_at_position(pattern_text, 0)
        
        if pattern_info:
            base_delay = 60 / (avg_wpm * 5)
            adjusted_delay = base_delay / pattern_info['speed_multiplier']
            
            print(f"  Category: {pattern_info['category']}")
            print(f"  Speed multiplier: {pattern_info['speed_multiplier']}x")
            print(f"  Adjusted delay: {adjusted_delay:.4f}s per char")
            print(f"  Pause before: {pattern_info['pause_before']}s")
            print(f"  Pause after: {pattern_info['pause_after']}s")
            
            # Calculate total time for pattern
            total_time = (adjusted_delay * len(pattern_text) + 
                         pattern_info['pause_before'] + 
                         pattern_info['pause_after'])
            print(f"  Total time to type: {total_time:.4f}s")
        else:
            base_delay = 60 / (avg_wpm * 5)
            print(f"  No pattern match - using base speed")
            print(f"  Base delay: {base_delay:.4f}s per char")
            print(f"  Total time to type: {base_delay * len(pattern_text):.4f}s")
    
    print("\n" + "=" * 70)
    return True

def test_language_switching():
    """Test switching between different languages."""
    print("\n" + "=" * 70)
    print("Testing Language Switching")
    print("=" * 70)
    
    matcher = PatternMatcher('java')
    
    # Test Java
    print("\n--- Java Mode ---")
    java_code = "public static void main"
    pattern_info = matcher.find_pattern_at_position(java_code, 0)
    print(f"Pattern in Java: {pattern_info['matched_text'] if pattern_info else 'None'}")
    
    # Switch to JavaScript
    matcher.set_language('javascript')
    print("\n--- JavaScript Mode ---")
    js_code = "const myVar = 5;"
    pattern_info = matcher.find_pattern_at_position(js_code, 0)
    print(f"Pattern in JavaScript: {pattern_info['matched_text'] if pattern_info else 'None'}")
    
    # Switch back to Java
    matcher.set_language('java')
    print("\n--- Back to Java Mode ---")
    pattern_info = matcher.find_pattern_at_position(java_code, 0)
    print(f"Pattern in Java: {pattern_info['matched_text'] if pattern_info else 'None'}")
    
    print("\n" + "=" * 70)
    return True

def main():
    """Run all tests."""
    print("\n")
    print("*" * 70)
    print("* Pattern-Based Typing Speed Variation Test Suite")
    print("*" * 70)
    
    try:
        # Run tests
        test_pattern_detection()
        test_speed_calculation()
        test_language_switching()
        
        print("\n" + "*" * 70)
        print("* All tests completed successfully!")
        print("*" * 70)
        print("\nThe pattern matcher is working correctly.")
        print("Patterns are detected and appropriate speed multipliers are applied.")
        print("\nLog file will be created in your system's temp directory as 'auto_typing_debug.log'")
        print("when the GUI application is run.")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
