"""
Code Pattern Recognition Engine
Core pattern definitions and data structures for human-like code typing simulation.
"""

import re


class CodePattern:
    """Represents a code pattern with associated typing behavior."""
    
    def __init__(self, pattern_type, speed_multiplier, pause_before=0, pause_after=0):
        self.pattern_type = pattern_type  # 'keyword', 'boilerplate', 'custom', etc.
        self.speed_multiplier = speed_multiplier  # Multiplier for base WPM
        self.pause_before = pause_before  # Seconds to pause before typing
        self.pause_after = pause_after   # Seconds to pause after typing


# Pattern definitions for each programming language
LANGUAGE_PATTERNS = {
    'java': {
        'keywords': {
            'patterns': [
                'public', 'private', 'protected', 'static', 'final', 'void', 
                'int', 'String', 'boolean', 'class', 'interface', 'extends', 
                'implements', 'import', 'package', 'try', 'catch', 'finally',
                'throw', 'throws', 'new', 'this', 'super', 'return', 'if', 
                'else', 'while', 'for', 'do', 'switch', 'case', 'break', 'continue'
            ],
            'speed_multiplier': 1.8,  # 80% faster than base
            'pause_before': 0,
            'pause_after': 0.1
        },
        'boilerplate': {
            'patterns': [
                'System.out.println', 'public static void main', 'String[] args',
                '@Override', '@Autowired', '@Component', '@Service', '@Repository',
                '@Entity', '@Table', '@Column', '@Id', '@GeneratedValue',
                'ArrayList<>', 'HashMap<>', 'List<>', 'Map<>', 'Set<>'
            ],
            'speed_multiplier': 2.0,  # Very fast, muscle memory
            'pause_before': 0,
            'pause_after': 0.2
        },
        'brackets_pairs': {
            'patterns': ['{}', '[]', '()', '<>'],
            'speed_multiplier': 3.0,  # Very fast, typed together
            'pause_before': 0,
            'pause_after': 0.1
        },
        'annotations': {
            'patterns': [
                '@Override', '@Deprecated', '@SuppressWarnings', '@Test', 
                '@Before', '@After', '@Autowired', '@Component', '@Service'
            ],
            'speed_multiplier': 1.6,
            'pause_before': 0.1,
            'pause_after': 0.2
        }
    },
    
    'javascript': {
        'keywords': {
            'patterns': [
                'function', 'const', 'let', 'var', 'return', 'if', 'else', 
                'for', 'while', 'do', 'switch', 'case', 'break', 'continue',
                'try', 'catch', 'finally', 'throw', 'new', 'this', 'typeof',
                'instanceof', 'in', 'delete', 'void', 'true', 'false', 'null',
                'undefined', 'export', 'import', 'from', 'default', 'as'
            ],
            'speed_multiplier': 1.8,
            'pause_before': 0,
            'pause_after': 0.1
        },
        'boilerplate': {
            'patterns': [
                'console.log', 'document.getElementById', 'addEventListener',
                'querySelector', 'querySelectorAll', 'createElement',
                'setAttribute', 'getAttribute', 'appendChild', 'removeChild',
                'JSON.stringify', 'JSON.parse', 'Object.keys', 'Array.from'
            ],
            'speed_multiplier': 2.0,
            'pause_before': 0,
            'pause_after': 0.2
        },
        'arrow_functions': {
            'patterns': ['=>', '() =>', '(param) =>', 'async () =>'],
            'speed_multiplier': 1.9,
            'pause_before': 0,
            'pause_after': 0.1
        },
        'async_patterns': {
            'patterns': ['async', 'await', 'Promise', '.then', '.catch', '.finally'],
            'speed_multiplier': 1.4,
            'pause_before': 0.1,
            'pause_after': 0.1
        }
    },
    
    'react': {
        'hooks': {
            'patterns': [
                'useState', 'useEffect', 'useContext', 'useCallback', 'useMemo',
                'useRef', 'useReducer', 'useImperativeHandle', 'useLayoutEffect',
                'useDebugValue', 'useId', 'useDeferredValue', 'useTransition'
            ],
            'speed_multiplier': 1.9,
            'pause_before': 0,
            'pause_after': 0.15
        },
        'jsx_attributes': {
            'patterns': [
                'className', 'onClick', 'onChange', 'onSubmit', 'onFocus', 'onBlur',
                'onMouseEnter', 'onMouseLeave', 'onKeyDown', 'onKeyUp', 'value',
                'placeholder', 'disabled', 'checked', 'selected', 'key', 'ref'
            ],
            'speed_multiplier': 1.7,
            'pause_before': 0,
            'pause_after': 0.1
        },
        'component_patterns': {
            'patterns': [
                'import React', 'export default', 'React.Component', 'React.Fragment',
                'PropTypes', 'defaultProps', 'render()', 'componentDidMount',
                'componentDidUpdate', 'componentWillUnmount'
            ],
            'speed_multiplier': 1.8,
            'pause_before': 0,
            'pause_after': 0.15
        },
        'jsx_elements': {
            'patterns': ['<div>', '<span>', '<p>', '<h1>', '<h2>', '<h3>', '<button>', '<input>', '<form>'],
            'speed_multiplier': 2.2,
            'pause_before': 0,
            'pause_after': 0.05
        }
    },
    
    'css': {
        'properties': {
            'patterns': [
                'display:', 'position:', 'top:', 'right:', 'bottom:', 'left:',
                'width:', 'height:', 'margin:', 'padding:', 'border:', 'color:',
                'background:', 'background-color:', 'font-size:', 'font-weight:',
                'font-family:', 'text-align:', 'text-decoration:', 'line-height:',
                'z-index:', 'opacity:', 'visibility:', 'overflow:', 'float:',
                'clear:', 'cursor:', 'box-shadow:', 'border-radius:'
            ],
            'speed_multiplier': 1.6,
            'pause_before': 0,
            'pause_after': 0.1
        },
        'selectors': {
            'patterns': [
                '.class', '#id', ':hover', ':focus', ':active', ':before', ':after',
                ':first-child', ':last-child', ':nth-child', '::placeholder'
            ],
            'speed_multiplier': 1.4,
            'pause_before': 0.05,
            'pause_after': 0.1
        },
        'values': {
            'patterns': [
                'flex', 'block', 'inline', 'inline-block', 'grid', 'none', 'auto',
                'center', 'left', 'right', 'absolute', 'relative', 'fixed', 'sticky',
                'bold', 'normal', 'italic', 'underline', 'transparent', 'inherit'
            ],
            'speed_multiplier': 1.5,
            'pause_before': 0,
            'pause_after': 0.05
        },
        'media_queries': {
            'patterns': ['@media', '@keyframes', '@import', '@font-face'],
            'speed_multiplier': 1.3,
            'pause_before': 0.2,
            'pause_after': 0.3
        }
    }
}

# Regex patterns for custom code detection
CUSTOM_PATTERNS = {
    'camelCase': r'\b[a-z]+([A-Z][a-z]*)+\b',           # myVariableName, getElementById
    'PascalCase': r'\b[A-Z][a-z]*([A-Z][a-z]*)*\b',     # MyClassName, ComponentName
    'snake_case': r'\b[a-z]+(_[a-z]+)+\b',              # my_variable_name
    'CONSTANT': r'\b[A-Z]+(_[A-Z]+)*\b',                # MY_CONSTANT, API_KEY
    'kebab-case': r'\b[a-z]+(-[a-z]+)+\b',              # my-css-class
    'number': r'\b\d+(\.\d+)?\b',                       # 123, 45.67
    'string_literal': r'["\'].*?["\']',                 # "string" or 'string'
    'hex_color': r'#[0-9a-fA-F]{3,6}\b',               # #fff, #ffffff
    'url': r'https?://[^\s]+',                          # URLs
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # email@example.com
}

# Typing speed configurations for different pattern types
SPEED_CONFIGS = {
    'very_fast': {'speed_multiplier': 2.5, 'pause_before': 0, 'pause_after': 0.05},     # Boilerplate
    'fast': {'speed_multiplier': 1.8, 'pause_before': 0, 'pause_after': 0.1},          # Keywords
    'normal': {'speed_multiplier': 1.0, 'pause_before': 0, 'pause_after': 0},          # Default
    'slow': {'speed_multiplier': 0.6, 'pause_before': 0.1, 'pause_after': 0.05},      # Custom names
    'very_slow': {'speed_multiplier': 0.4, 'pause_before': 0.2, 'pause_after': 0.1},  # Complex logic
    'thinking_pause': {'speed_multiplier': 0.1, 'pause_before': 0.5, 'pause_after': 1.0}  # Major pauses
}

# Special characters and operators with their typing behaviors
OPERATOR_PATTERNS = {
    'assignment': {
        'patterns': ['=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<', '>>'],
        'speed_multiplier': 1.2,
        'pause_before': 0.05,
        'pause_after': 0.05
    },
    'comparison': {
        'patterns': ['==', '===', '!=', '!==', '<', '>', '<=', '>='],
        'speed_multiplier': 1.1,
        'pause_before': 0.05,
        'pause_after': 0.05
    },
    'logical': {
        'patterns': ['&&', '||', '!', '&', '|', '^'],
        'speed_multiplier': 1.0,
        'pause_before': 0.1,
        'pause_after': 0.1
    },
    'arithmetic': {
        'patterns': ['+', '-', '*', '/', '%', '++', '--'],
        'speed_multiplier': 1.3,
        'pause_before': 0.02,
        'pause_after': 0.02
    }
}

# Punctuation patterns for different contexts
PUNCTUATION_PATTERNS = {
    'statement_end': {
        'patterns': [';'],
        'speed_multiplier': 1.5,
        'pause_before': 0,
        'pause_after': 0.2
    },
    'block_structure': {
        'patterns': ['{', '}'],
        'speed_multiplier': 1.4,
        'pause_before': 0.1,
        'pause_after': 0.2
    },
    'function_params': {
        'patterns': ['(', ')'],
        'speed_multiplier': 1.8,
        'pause_before': 0,
        'pause_after': 0.05
    },
    'array_brackets': {
        'patterns': ['[', ']'],
        'speed_multiplier': 1.6,
        'pause_before': 0,
        'pause_after': 0.05
    }
}