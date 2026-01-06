#!/usr/bin/env python3
"""
Demo script to demonstrate typing speed variations.
This simulates what the auto-typer does but outputs to console instead of GUI.
"""

import time
import random
from pattern_matcher import PatternMatcher

# Sample Java code to demonstrate
JAVA_CODE = """public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World");
        int count = 0;
        for (int i = 0; i < 10; i++) {
            count++;
        }
    }
}"""

def simulate_typing(text, min_wpm=40, max_wpm=60, language='java', show_timing=True):
    """Simulate typing with pattern-based speed variation.
    
    Args:
        text: Text to type
        min_wpm: Minimum words per minute
        max_wpm: Maximum words per minute
        language: Programming language
        show_timing: Whether to show timing information
    """
    matcher = PatternMatcher(language)
    position = 0
    total_time = 0
    
    print(f"\n{'=' * 70}")
    print(f"Simulating typing for {language.upper()} code")
    print(f"Base speed: {min_wpm}-{max_wpm} WPM")
    print(f"{'=' * 70}\n")
    
    if show_timing:
        print("Timing breakdown:\n")
    
    while position < len(text):
        # Check for pattern at current position
        pattern_info = matcher.find_pattern_at_position(text, position)
        
        if pattern_info:
            # Calculate timing
            base_delay = 60 / (random.uniform(min_wpm, max_wpm) * 5)
            adjusted_delay = base_delay / pattern_info['speed_multiplier']
            
            # Time for pattern
            pattern_time = (adjusted_delay * pattern_info['length'] + 
                          pattern_info['pause_before'] + 
                          pattern_info['pause_after'])
            total_time += pattern_time
            
            if show_timing:
                print(f"  [{position:3d}] Pattern: '{pattern_info['matched_text']:20s}' | "
                      f"Category: {pattern_info['category']:30s} | "
                      f"Speed: {pattern_info['speed_multiplier']:.1f}x | "
                      f"Time: {pattern_time:.3f}s")
            
            position += pattern_info['length']
        else:
            # Default speed for non-pattern characters
            base_delay = 60 / (random.uniform(min_wpm, max_wpm) * 5)
            total_time += base_delay
            
            # Show only visible characters for debugging
            char = text[position]
            if show_timing and char not in '\n\t ':
                print(f"  [{position:3d}] Char: '{char}' (no pattern) | "
                      f"Time: {base_delay:.3f}s")
            
            position += 1
    
    print(f"\n{'=' * 70}")
    print(f"Total simulated typing time: {total_time:.2f} seconds")
    print(f"Average effective WPM: {len(text.split()) / (total_time / 60):.1f}")
    print(f"{'=' * 70}\n")
    
    # Show the actual code that would be typed
    print("Code that would be typed:\n")
    print(text)
    print()

def main():
    """Run the demonstration."""
    print("\n" + "*" * 70)
    print("* Human-Like Code Typing Speed Demonstration")
    print("*" * 70)
    
    # Simulate typing Java code
    simulate_typing(JAVA_CODE, min_wpm=40, max_wpm=60, language='java', show_timing=True)
    
    # Show comparison with different base speeds
    print("\n" + "=" * 70)
    print("Speed Comparison:")
    print("=" * 70)
    
    print("\n1. Slow typist (30-50 WPM):")
    simulate_typing(JAVA_CODE, min_wpm=30, max_wpm=50, language='java', show_timing=False)
    
    print("\n2. Normal typist (40-60 WPM):")
    simulate_typing(JAVA_CODE, min_wpm=40, max_wpm=60, language='java', show_timing=False)
    
    print("\n3. Fast typist (60-100 WPM):")
    simulate_typing(JAVA_CODE, min_wpm=60, max_wpm=100, language='java', show_timing=False)
    
    print("\n" + "*" * 70)
    print("* Demonstration complete!")
    print("*" * 70)
    print("\nKey observations:")
    print("  - Keywords (public, static, void, etc.) are typed ~1.8x faster")
    print("  - Boilerplate (System.out.println, etc.) is typed ~2.0x faster")
    print("  - Bracket pairs (<>, [], (), {}) are typed ~3.0x faster")
    print("  - Punctuation has natural pauses before/after")
    print("  - Custom variable names maintain base speed")
    print("\nThis creates a more human-like typing experience!\n")

if __name__ == "__main__":
    main()
