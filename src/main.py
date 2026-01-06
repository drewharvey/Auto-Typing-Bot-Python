import tkinter as tk
from tkinter import scrolledtext
from pynput.keyboard import Controller
import threading
import random
import time
import logging
import tempfile
import os
from pattern_matcher import PatternMatcher
from pause_directive import PauseDirectiveParser
from help_window import HelpWindow

# Constants
DEFAULT_START_DELAY = 3  # Seconds to wait before starting typing
DEFAULT_MIN_WPM = 100
DEFAULT_MAX_WPM = 250
CHARS_PER_WORD = 5  # Standard typing test assumption
TEXT_WIDGET_WIDTH = 50
TEXT_WIDGET_HEIGHT = 15
LANGUAGE_DROPDOWN_WIDTH = 12

# Globals
start_delay = DEFAULT_START_DELAY
is_typing = False
current_position = 0
min_wpm = DEFAULT_MIN_WPM
max_wpm = DEFAULT_MAX_WPM
typing_thread = None
keyboard = Controller()
pattern_matcher = PatternMatcher('java')  # Default to Java
ignore_leading_whitespace = False  # Toggle for ignoring leading whitespace
pause_parser = PauseDirectiveParser()  # Parser for {{PAUSE:X}} directives

# Configure logging
log_file = os.path.join(tempfile.gettempdir(), 'auto_typing_debug.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logging.info(f"Log file: {log_file}")

def auto_type(text_widget):
    """Simulates typing with human-like speed variation based on code patterns."""
    global is_typing, current_position, min_wpm, max_wpm, pattern_matcher, ignore_leading_whitespace
    text = text_widget.get("1.0", tk.END).strip()  # Get text from the text widget
    
    logging.info(f"Starting auto-type with min_wpm={min_wpm}, max_wpm={max_wpm}, language={pattern_matcher.language}, ignore_leading_whitespace={ignore_leading_whitespace}")
    
    # Track if we're at the beginning of a line
    # When resuming, check if we're actually at line start based on current position
    at_line_start = True
    if current_position > 0:
        # Look backwards to find if we're at the start of a line
        # We're at line start only if the previous character was a newline
        # or if we're at position 0
        at_line_start = (text[current_position - 1] == '\n')
    
    while current_position < len(text):
        if not is_typing:
            break
        
        # Check for pause directive at current position (highest priority)
        pause_directive = pause_parser.find_directive_at_position(text, current_position)
        if pause_directive:
            logging.info(f"Executing pause directive: {pause_directive.duration}s at position {current_position}")
            time.sleep(pause_directive.duration)
            current_position = pause_directive.end_position  # Skip past the directive
            # After a pause directive, check if we're now at line start
            if current_position > 0 and current_position < len(text):
                at_line_start = (text[current_position - 1] == '\n')
            continue
        
        current_char = text[current_position]
        
        # Check if we should skip leading whitespace
        if ignore_leading_whitespace and at_line_start and current_char in ' \t':
            logging.debug(f"Skipping leading whitespace at position {current_position}")
            current_position += 1
            continue
        
        # We're going to type this character, so update line start tracking
        # If we type a non-whitespace char, we're no longer at line start
        if current_char not in ' \t':
            at_line_start = False
        
        # Check if we're at the start of a known pattern
        pattern_info = pattern_matcher.find_pattern_at_position(text, current_position)
        
        if pattern_info:
            # Found a pattern - apply pause before if needed
            if pattern_info['pause_before'] > 0:
                logging.debug(f"Pause before pattern '{pattern_info['matched_text']}': {pattern_info['pause_before']}s")
                time.sleep(pattern_info['pause_before'])
            
            # Type each character of the pattern with adjusted speed
            pattern_length = pattern_info['length']
            base_delay = 60 / (random.uniform(min_wpm, max_wpm) * CHARS_PER_WORD)
            adjusted_delay = base_delay / pattern_info['speed_multiplier']
            
            logging.info(f"Typing pattern '{pattern_info['matched_text']}' (category: {pattern_info['category']}) "
                        f"with speed_multiplier={pattern_info['speed_multiplier']:.2f}, "
                        f"delay={adjusted_delay:.4f}s per char")
            
            # Type the pattern character by character
            for i in range(pattern_length):
                if not is_typing:
                    break
                char = text[current_position]
                keyboard.type(char)
                
                # After typing a newline, next position is at line start
                if char == '\n':
                    at_line_start = True
                
                current_position += 1
                if i < pattern_length - 1:  # Don't delay after the last character
                    time.sleep(adjusted_delay)
            
            # Apply pause after if needed
            if pattern_info['pause_after'] > 0:
                logging.debug(f"Pause after pattern '{pattern_info['matched_text']}': {pattern_info['pause_after']}s")
                time.sleep(pattern_info['pause_after'])
        else:
            # No pattern match - use default speed
            keyboard.type(current_char)
            
            # After typing a newline, next position is at line start
            if current_char == '\n':
                at_line_start = True
            
            current_position += 1
            
            # WPM delay: Convert WPM to delay per character
            delay = 60 / (random.uniform(min_wpm, max_wpm) * CHARS_PER_WORD)
            time.sleep(delay)

def start_typing(text_widget, min_wpm_input, max_wpm_input):
    """Starts the typing process."""
    global is_typing, typing_thread, min_wpm, max_wpm
    if is_typing:
        return  # Prevent starting again if already typing
    try:
        min_wpm = int(min_wpm_input.get())
        max_wpm = int(max_wpm_input.get())
        update_status(f"Starting in {start_delay} seconds...")
        time.sleep(start_delay)  # Delay to allow focusing on another UI
        is_typing = True
        if typing_thread is None or not typing_thread.is_alive():  # Start a new thread
            typing_thread = threading.Thread(
                target=auto_type, args=(text_widget,), daemon=True
            )
            typing_thread.start()
        update_status("Typing started.")
    except ValueError:
        update_status("Please enter valid WPM values.")

def pause_typing():
    """Pauses the typing process."""
    global is_typing
    if is_typing:
        is_typing = False
        update_status("Typing paused.")

def continue_typing():
    """Continues the typing process."""
    global is_typing, typing_thread
    if not is_typing:
        update_status(f"Continuing in {start_delay} seconds...")
        time.sleep(start_delay)  # Delay to allow focusing on another UI
        is_typing = True
        if typing_thread is None or not typing_thread.is_alive():  # Resume the thread
            typing_thread = threading.Thread(
                target=auto_type, args=(text_widget,), daemon=True
            )
            typing_thread.start()
        update_status("Typing continued.")

def stop_typing():
    """Stops the typing process and resets progress."""
    global is_typing, current_position
    is_typing = False
    current_position = 0
    update_status("Typing stopped. Progress reset.")

def update_status(message):
    """Updates the status label."""
    status_label.config(text=message)

def on_language_change(*args):
    """Handle manual language selection change."""
    global pattern_matcher
    selected_language = language_var.get()
    pattern_matcher.set_language(selected_language)
    logging.info(f"Language changed to: {selected_language}")
    update_status(f"Language set to: {selected_language}")

def on_whitespace_toggle():
    """Handle toggle of the ignore leading whitespace checkbox."""
    global ignore_leading_whitespace
    ignore_leading_whitespace = whitespace_var.get()
    logging.info(f"Ignore leading whitespace: {ignore_leading_whitespace}")
    status = "enabled" if ignore_leading_whitespace else "disabled"
    update_status(f"Ignore leading whitespace {status}")

# Create the GUI
root = tk.Tk()
root.title("Auto Typing Tool")

# Help/Info button - placed at top right
help_button = tk.Button(
    root, 
    text="ℹ️ Help",
    command=HelpWindow.open,
    relief=tk.RAISED,
    borderwidth=1
)
help_button.grid(row=0, column=4, padx=10, pady=5, sticky="e")

# Min WPM and Max WPM Inputs
tk.Label(root, text="Min WPM:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
min_wpm_input = tk.Entry(root, width=10)
min_wpm_input.grid(row=0, column=1, padx=10, pady=5)
min_wpm_input.insert(0, min_wpm)

tk.Label(root, text="Max WPM:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
max_wpm_input = tk.Entry(root, width=10)
max_wpm_input.grid(row=0, column=3, padx=10, pady=5)
max_wpm_input.insert(0, max_wpm)

# Text Area for Main Text
tk.Label(root, text="Main Text:").grid(row=1, column=0, columnspan=4, padx=10, pady=5)
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=TEXT_WIDGET_WIDTH, height=TEXT_WIDGET_HEIGHT)
text_widget.grid(row=2, column=0, columnspan=4, padx=10, pady=5)

def focus_handler(event):
    """Ensure editor field gets focus only when explicitly clicked."""
    event.widget.focus_set()

# Bind text widget focus to mouse click
text_widget.bind("<FocusIn>", focus_handler)

# Language Selection
language_frame = tk.Frame(root)
language_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")

tk.Label(language_frame, text="Language:").pack(side=tk.LEFT, padx=(0, 5))

language_var = tk.StringVar(value="Java")
language_dropdown = tk.OptionMenu(
    language_frame, 
    language_var,
    "Java",
    "JavaScript", 
    "TypeScript",
    "React",
    "CSS",
    "Python",
    "C++",
    "C#"
)
language_dropdown.config(width=LANGUAGE_DROPDOWN_WIDTH)
language_dropdown.pack(side=tk.LEFT)

# Bind language change event
language_var.trace_add('write', on_language_change)

# Ignore Leading Whitespace Checkbox
whitespace_var = tk.BooleanVar(value=False)
whitespace_checkbox = tk.Checkbutton(
    root,
    text="Ignore leading whitespace (for IDE auto-indent)",
    variable=whitespace_var,
    command=on_whitespace_toggle
)
whitespace_checkbox.grid(row=4, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")

# Buttons
start_button = tk.Button(
    root, text="Start", command=lambda: start_typing(text_widget, min_wpm_input, max_wpm_input)
)
start_button.grid(row=5, column=0, padx=10, pady=10)

pause_button = tk.Button(root, text="Pause", command=pause_typing)
pause_button.grid(row=5, column=1, padx=10, pady=10)

continue_button = tk.Button(root, text="Continue", command=continue_typing)
continue_button.grid(row=5, column=2, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_typing)
stop_button.grid(row=5, column=3, padx=10, pady=10)

# Status Label
status_label = tk.Label(root, text="Status: Ready", fg="blue")
status_label.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

# Run the GUI
root.mainloop()
