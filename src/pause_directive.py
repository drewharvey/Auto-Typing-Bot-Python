"""
Pause Directive Module
Handles parsing and validation of pause directives in text.

Pause directives allow users to insert explicit pauses during auto-typing.
Syntax: {{PAUSE:X}} where X is the duration in seconds (supports decimals).

Examples:
    {{PAUSE:2}}     - Pause for 2 seconds
    {{PAUSE:0.5}}   - Pause for 0.5 seconds
    {{PAUSE:10}}    - Pause for 10 seconds
"""

import re
import logging
from dataclasses import dataclass
from typing import Optional, List

# Constants
PAUSE_DIRECTIVE_PATTERN = r'\{\{PAUSE:(\d+(?:\.\d+)?)\}\}'
MIN_PAUSE_DURATION = 0.0
MAX_PAUSE_DURATION = 60.0  # Maximum 60 seconds to prevent accidental long pauses
DEFAULT_PAUSE_DURATION = 1.0

# Module logger
logger = logging.getLogger(__name__)


@dataclass
class PauseDirective:
    """Represents a pause directive found in text.
    
    Attributes:
        start_position: Starting character position in original text
        end_position: Ending character position in original text (exclusive)
        duration: Pause duration in seconds
        raw_text: The original directive text (e.g., "{{PAUSE:2}}")
    """
    start_position: int
    end_position: int
    duration: float
    raw_text: str
    
    @property
    def length(self) -> int:
        """Returns the length of the directive in characters."""
        return self.end_position - self.start_position


class PauseDirectiveParser:
    """Parses and validates pause directives in text.
    
    This parser finds pause directives using the {{PAUSE:X}} syntax and
    validates that durations are within acceptable bounds.
    
    Attributes:
        min_duration: Minimum allowed pause duration in seconds
        max_duration: Maximum allowed pause duration in seconds
    """
    
    def __init__(self, min_duration: float = MIN_PAUSE_DURATION,
                 max_duration: float = MAX_PAUSE_DURATION):
        """Initialize the pause directive parser.
        
        Args:
            min_duration: Minimum allowed pause duration (default: 0.0)
            max_duration: Maximum allowed pause duration (default: 60.0)
        """
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.pattern = re.compile(PAUSE_DIRECTIVE_PATTERN)
    
    def find_all_directives(self, text: str) -> List[PauseDirective]:
        """Find all pause directives in the given text.
        
        Args:
            text: The text to search for pause directives
            
        Returns:
            List of PauseDirective objects, ordered by position
        """
        directives = []
        
        for match in self.pattern.finditer(text):
            raw_duration = float(match.group(1))
            validated_duration = self.validate_duration(raw_duration)
            
            directive = PauseDirective(
                start_position=match.start(),
                end_position=match.end(),
                duration=validated_duration,
                raw_text=match.group(0)
            )
            directives.append(directive)
            
            logger.debug(
                f"Found pause directive at position {directive.start_position}: "
                f"'{directive.raw_text}' -> {directive.duration}s"
            )
        
        return directives
    
    def find_directive_at_position(self, text: str, position: int) -> Optional[PauseDirective]:
        """Check if there's a pause directive starting at the given position.
        
        Args:
            text: The full text string
            position: The character position to check
            
        Returns:
            PauseDirective if one starts at this position, None otherwise
        """
        # Try to match the pattern starting at the given position
        match = self.pattern.match(text, position)
        
        if match:
            raw_duration = float(match.group(1))
            validated_duration = self.validate_duration(raw_duration)
            
            return PauseDirective(
                start_position=match.start(),
                end_position=match.end(),
                duration=validated_duration,
                raw_text=match.group(0)
            )
        
        return None
    
    def validate_duration(self, duration: float) -> float:
        """Validate and clamp duration to acceptable range.
        
        Args:
            duration: The requested pause duration in seconds
            
        Returns:
            The validated duration, clamped to [min_duration, max_duration]
        """
        if duration < self.min_duration:
            logger.warning(
                f"Pause duration {duration}s is below minimum, "
                f"clamping to {self.min_duration}s"
            )
            return self.min_duration
        
        if duration > self.max_duration:
            logger.warning(
                f"Pause duration {duration}s exceeds maximum, "
                f"clamping to {self.max_duration}s"
            )
            return self.max_duration
        
        return duration
    
    def remove_all_directives(self, text: str) -> str:
        """Remove all pause directives from text.
        
        This is useful for previewing what the typed output will look like,
        or for calculating the actual character count.
        
        Args:
            text: The text containing pause directives
            
        Returns:
            The text with all pause directives removed
        """
        return self.pattern.sub('', text)
    
    def get_total_pause_time(self, text: str) -> float:
        """Calculate the total pause time for all directives in text.
        
        Args:
            text: The text containing pause directives
            
        Returns:
            Total pause time in seconds
        """
        directives = self.find_all_directives(text)
        return sum(d.duration for d in directives)
    
    def get_directive_count(self, text: str) -> int:
        """Count the number of pause directives in text.
        
        Args:
            text: The text to search
            
        Returns:
            Number of pause directives found
        """
        return len(self.pattern.findall(text))


# Convenience function for quick checks
def has_pause_directives(text: str) -> bool:
    """Quick check if text contains any pause directives.
    
    Args:
        text: The text to check
        
    Returns:
        True if text contains at least one pause directive
    """
    pattern = re.compile(PAUSE_DIRECTIVE_PATTERN)
    return bool(pattern.search(text))
