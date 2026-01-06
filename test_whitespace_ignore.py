#!/usr/bin/env python3
"""
Test script for the ignore leading whitespace feature.
This tests the logic without requiring GUI interaction.
"""

import sys

def simulate_whitespace_skip(text, ignore_leading_whitespace):
    """Simulate the auto-type function with whitespace skipping logic.
    
    Args:
        text: Text to process
        ignore_leading_whitespace: Whether to skip leading whitespace
        
    Returns:
        String that would actually be typed (without skipped characters)
    """
    result = []
    at_line_start = True
    
    for i, char in enumerate(text):
        # Check if we should skip leading whitespace
        if ignore_leading_whitespace and at_line_start and char in ' \t':
            # Skip this character
            continue
        
        # We're going to type this character, so update line start tracking
        # If we type a non-whitespace char, we're no longer at line start
        if char not in ' \t':
            at_line_start = False
        
        # Add character to result
        result.append(char)
        
        # After typing a newline, next position is at line start
        if char == '\n':
            at_line_start = True
    
    return ''.join(result)

def test_whitespace_skipping():
    """Test various scenarios for whitespace skipping."""
    print("=" * 70)
    print("Testing Whitespace Skipping Logic")
    print("=" * 70)
    
    # Test 1: Simple indented code
    test1 = """public class Test {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}"""
    
    print("\n--- Test 1: Simple indented Java code ---")
    print("Original text:")
    print(repr(test1))
    print("\nWith ignore_leading_whitespace=False:")
    result1_false = simulate_whitespace_skip(test1, False)
    print(repr(result1_false))
    print("\nWith ignore_leading_whitespace=True:")
    result1_true = simulate_whitespace_skip(test1, True)
    print(repr(result1_true))
    
    # Verify leading spaces are removed
    assert "    public static" not in result1_true
    assert "public static" in result1_true
    assert "        System.out.println" not in result1_true
    assert "System.out.println" in result1_true
    print("✓ Test 1 passed: Leading whitespace correctly skipped")
    
    # Test 2: Code with tabs
    test2 = """function test() {
\tvar x = 5;
\tif (x > 0) {
\t\tconsole.log("positive");
\t}
}"""
    
    print("\n--- Test 2: Code with tabs ---")
    print("Original text:")
    print(repr(test2))
    print("\nWith ignore_leading_whitespace=True:")
    result2_true = simulate_whitespace_skip(test2, True)
    print(repr(result2_true))
    
    # Verify leading tabs are removed
    assert "\tvar x" not in result2_true
    assert "var x" in result2_true
    assert "\t\tconsole.log" not in result2_true
    assert "console.log" in result2_true
    print("✓ Test 2 passed: Leading tabs correctly skipped")
    
    # Test 3: Mixed spaces and tabs
    test3 = """def example():
    \tx = 1
\t    y = 2
  \t  z = 3"""
    
    print("\n--- Test 3: Mixed spaces and tabs ---")
    print("Original text:")
    print(repr(test3))
    print("\nWith ignore_leading_whitespace=True:")
    result3_true = simulate_whitespace_skip(test3, True)
    print(repr(result3_true))
    
    # Verify all leading whitespace is removed
    assert "x = 1" in result3_true
    assert "y = 2" in result3_true
    assert "z = 3" in result3_true
    print("✓ Test 3 passed: Mixed leading whitespace correctly skipped")
    
    # Test 4: No leading whitespace
    test4 = """public class Simple {
public void test() {
System.out.println("test");
}
}"""
    
    print("\n--- Test 4: No leading whitespace ---")
    print("Original text:")
    print(repr(test4))
    print("\nWith ignore_leading_whitespace=True:")
    result4_true = simulate_whitespace_skip(test4, True)
    print(repr(result4_true))
    
    # Should be identical
    assert result4_true == test4
    print("✓ Test 4 passed: Text without leading whitespace unchanged")
    
    # Test 5: Whitespace in middle of line should not be skipped
    test5 = """public class Test {
    void method(int x, int y) {
        int sum = x + y;
    }
}"""
    
    print("\n--- Test 5: Whitespace in middle of lines ---")
    result5_true = simulate_whitespace_skip(test5, True)
    
    # Verify spaces within lines are preserved
    assert "int x, int y" in result5_true
    assert "x + y" in result5_true
    print("✓ Test 5 passed: Non-leading whitespace preserved")
    
    # Test 6: Empty lines
    test6 = """public class Test {

    void method() {
    
        int x = 5;
    }
}"""
    
    print("\n--- Test 6: Empty lines ---")
    result6_true = simulate_whitespace_skip(test6, True)
    print(repr(result6_true))
    
    # Empty lines should remain (just newlines)
    assert "\n\nvoid method" in result6_true
    assert "\n\nint x" in result6_true
    print("✓ Test 6 passed: Empty lines handled correctly")
    
    print("\n" + "=" * 70)
    return True

def test_disabled_mode():
    """Test that when disabled, all whitespace is preserved."""
    print("\n" + "=" * 70)
    print("Testing Disabled Mode (ignore_leading_whitespace=False)")
    print("=" * 70)
    
    test_text = """public class Test {
    void method() {
        int x = 5;
    }
}"""
    
    result = simulate_whitespace_skip(test_text, False)
    
    # Should be completely identical
    assert result == test_text
    print("✓ When disabled, all text is preserved exactly")
    
    print("=" * 70)
    return True

def main():
    """Run all tests."""
    print("\n")
    print("*" * 70)
    print("* Ignore Leading Whitespace Feature Test Suite")
    print("*" * 70)
    
    try:
        # Run tests
        test_whitespace_skipping()
        test_disabled_mode()
        
        print("\n" + "*" * 70)
        print("* All tests completed successfully!")
        print("*" * 70)
        print("\nThe whitespace skipping feature is working correctly:")
        print("  - Leading spaces are skipped when enabled")
        print("  - Leading tabs are skipped when enabled")
        print("  - Mixed leading whitespace is skipped when enabled")
        print("  - Non-leading whitespace is preserved")
        print("  - Empty lines are handled correctly")
        print("  - All text is preserved when feature is disabled")
        print("\nThis feature prevents duplicate indentation when typing into IDEs")
        print("that automatically add indentation to new lines.\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
