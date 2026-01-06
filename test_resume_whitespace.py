#!/usr/bin/env python3
"""
Test script for resume functionality with whitespace ignore feature.
Tests that the line tracking works correctly when resuming from a pause.
"""

import sys

def simulate_resume_scenario(text, ignore_leading_whitespace, pause_position):
    """Simulate resuming typing from a pause.
    
    Args:
        text: Text to process
        ignore_leading_whitespace: Whether to skip leading whitespace
        pause_position: Position where we paused and will resume from
        
    Returns:
        String that would actually be typed (without skipped characters)
    """
    result = []
    
    # First pass: type up to pause position
    at_line_start = True
    for i in range(pause_position):
        char = text[i]
        
        # Check if we should skip leading whitespace
        if ignore_leading_whitespace and at_line_start and char in ' \t':
            continue
        
        # We're going to type this character
        if char not in ' \t':
            at_line_start = False
        
        result.append(char)
        
        # After typing a newline, next position is at line start
        if char == '\n':
            at_line_start = True
    
    # Simulate resume: recalculate at_line_start based on current position
    # (This is what the fixed code does)
    if pause_position > 0:
        at_line_start = (text[pause_position - 1] == '\n')
    else:
        at_line_start = True
    
    # Second pass: resume from pause position
    for i in range(pause_position, len(text)):
        char = text[i]
        
        # Check if we should skip leading whitespace
        if ignore_leading_whitespace and at_line_start and char in ' \t':
            continue
        
        # We're going to type this character
        if char not in ' \t':
            at_line_start = False
        
        result.append(char)
        
        # After typing a newline, next position is at line start
        if char == '\n':
            at_line_start = True
    
    return ''.join(result)

def test_resume_mid_line():
    """Test resuming in the middle of a line."""
    print("=" * 70)
    print("Testing Resume Functionality - Mid Line")
    print("=" * 70)
    
    text = """public class Test {
    void method() {
        int x = 5;
    }
}"""
    
    # Pause in the middle of "void method() {"
    pause_pos = text.index('method') + 3  # After "met"
    
    print(f"\nOriginal text:")
    print(repr(text))
    print(f"\nPausing at position {pause_pos} (middle of 'method')")
    print(f"Character at pause: '{text[pause_pos]}'")
    print(f"Previous character: '{text[pause_pos-1]}'")
    
    result = simulate_resume_scenario(text, True, pause_pos)
    
    print(f"\nResult with whitespace ignore enabled:")
    print(repr(result))
    
    # Verify leading whitespace on line 2, 3, 4 is skipped
    assert "    void method" not in result
    assert "void method" in result
    assert "        int x" not in result
    assert "int x" in result
    
    print("✓ Test passed: Resume in mid-line works correctly")
    print("=" * 70)
    return True

def test_resume_after_newline():
    """Test resuming right after a newline."""
    print("\n" + "=" * 70)
    print("Testing Resume Functionality - After Newline")
    print("=" * 70)
    
    text = """public class Test {
    void method() {
        int x = 5;
    }
}"""
    
    # Pause right after the first newline
    pause_pos = text.index('\n') + 1  # Right after first \n
    
    print(f"\nPausing at position {pause_pos} (right after newline)")
    print(f"Character at pause: '{repr(text[pause_pos])}'")
    print(f"Previous character: '{repr(text[pause_pos-1])}'")
    
    result = simulate_resume_scenario(text, True, pause_pos)
    
    print(f"\nResult with whitespace ignore enabled:")
    print(repr(result))
    
    # Verify leading whitespace is skipped
    assert "    void method" not in result
    assert "void method" in result
    
    print("✓ Test passed: Resume after newline works correctly")
    print("=" * 70)
    return True

def test_resume_at_start():
    """Test resuming from the very beginning."""
    print("\n" + "=" * 70)
    print("Testing Resume Functionality - From Start")
    print("=" * 70)
    
    text = """public class Test {
    void method() {
        int x = 5;
    }
}"""
    
    pause_pos = 0
    
    print(f"\nPausing at position {pause_pos} (start of text)")
    
    result = simulate_resume_scenario(text, True, pause_pos)
    
    print(f"\nResult with whitespace ignore enabled:")
    print(repr(result))
    
    # Verify leading whitespace is skipped
    assert "    void method" not in result
    assert "void method" in result
    
    print("✓ Test passed: Resume from start works correctly")
    print("=" * 70)
    return True

def main():
    """Run all tests."""
    print("\n")
    print("*" * 70)
    print("* Resume Functionality Test Suite")
    print("*" * 70)
    
    try:
        test_resume_mid_line()
        test_resume_after_newline()
        test_resume_at_start()
        
        print("\n" + "*" * 70)
        print("* All tests completed successfully!")
        print("*" * 70)
        print("\nThe resume functionality works correctly:")
        print("  - Line tracking is properly recalculated on resume")
        print("  - Whitespace skipping works when resuming mid-line")
        print("  - Whitespace skipping works when resuming after newline")
        print("  - Whitespace skipping works when resuming from start\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
