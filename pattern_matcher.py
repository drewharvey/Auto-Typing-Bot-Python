"""
Pattern Matcher Module
Detects code patterns in text to apply appropriate typing speed variations.
"""

import re
from code_patterns import LANGUAGE_PATTERNS, OPERATOR_PATTERNS, PUNCTUATION_PATTERNS


class PatternMatcher:
    """Matches text patterns to determine appropriate typing behavior."""
    
    def __init__(self, language='java'):
        """Initialize the pattern matcher for a specific language.
        
        Args:
            language: Programming language name (default: 'java')
        """
        self.language = language.lower()
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile patterns for the selected language."""
        self.compiled_patterns = []
        
        # Get language-specific patterns
        lang_patterns = LANGUAGE_PATTERNS.get(self.language, {})
        
        # Add language-specific patterns
        for category_name, category_data in lang_patterns.items():
            patterns = category_data.get('patterns', [])
            speed_multiplier = category_data.get('speed_multiplier', 1.0)
            pause_before = category_data.get('pause_before', 0)
            pause_after = category_data.get('pause_after', 0)
            
            for pattern in patterns:
                # Skip empty patterns
                if not pattern:
                    continue
                    
                # Escape special regex characters and create word boundary pattern
                escaped_pattern = re.escape(pattern)
                # Use word boundaries for alphanumeric patterns, exact match for symbols
                if pattern[0].isalnum():
                    regex_pattern = r'\b' + escaped_pattern + r'\b'
                else:
                    regex_pattern = escaped_pattern
                
                self.compiled_patterns.append({
                    'regex': re.compile(regex_pattern),
                    'pattern': pattern,
                    'speed_multiplier': speed_multiplier,
                    'pause_before': pause_before,
                    'pause_after': pause_after,
                    'category': category_name
                })
        
        # Add operator patterns (language-agnostic)
        for category_name, category_data in OPERATOR_PATTERNS.items():
            patterns = category_data.get('patterns', [])
            speed_multiplier = category_data.get('speed_multiplier', 1.0)
            pause_before = category_data.get('pause_before', 0)
            pause_after = category_data.get('pause_after', 0)
            
            for pattern in patterns:
                escaped_pattern = re.escape(pattern)
                self.compiled_patterns.append({
                    'regex': re.compile(escaped_pattern),
                    'pattern': pattern,
                    'speed_multiplier': speed_multiplier,
                    'pause_before': pause_before,
                    'pause_after': pause_after,
                    'category': f'operator_{category_name}'
                })
        
        # Add punctuation patterns (language-agnostic)
        for category_name, category_data in PUNCTUATION_PATTERNS.items():
            patterns = category_data.get('patterns', [])
            speed_multiplier = category_data.get('speed_multiplier', 1.0)
            pause_before = category_data.get('pause_before', 0)
            pause_after = category_data.get('pause_after', 0)
            
            for pattern in patterns:
                escaped_pattern = re.escape(pattern)
                self.compiled_patterns.append({
                    'regex': re.compile(escaped_pattern),
                    'pattern': pattern,
                    'speed_multiplier': speed_multiplier,
                    'pause_before': pause_before,
                    'pause_after': pause_after,
                    'category': f'punctuation_{category_name}'
                })
        
        # Sort patterns by length (longest first) to match longer patterns first
        self.compiled_patterns.sort(key=lambda x: len(x['pattern']), reverse=True)
    
    def find_pattern_at_position(self, text, position):
        """Find a matching pattern at the given position in text.
        
        Args:
            text: The full text string
            position: Current character position in the text
            
        Returns:
            dict: Pattern info with speed_multiplier, pause_before, pause_after, and length
                  or None if no pattern matches
        """
        # Try to match each compiled pattern at this position
        for pattern_info in self.compiled_patterns:
            match = pattern_info['regex'].match(text, position)
            if match:
                matched_text = match.group(0)
                return {
                    'pattern': pattern_info['pattern'],
                    'matched_text': matched_text,
                    'length': len(matched_text),
                    'speed_multiplier': pattern_info['speed_multiplier'],
                    'pause_before': pattern_info['pause_before'],
                    'pause_after': pattern_info['pause_after'],
                    'category': pattern_info['category']
                }
        
        return None
    
    def set_language(self, language):
        """Change the language and recompile patterns.
        
        Args:
            language: Programming language name
        """
        self.language = language.lower()
        self._compile_patterns()
