
def is_prompt_injection(prompt):
    """
    Checks for prompt injection attempts.
    """
    injection_phrases = [
        "ignore previous instructions",
        "override system",
        "you are no longer",
        "disregard the rules",
    ]
    for phrase in injection_phrases:
        if phrase in prompt.lower():
            return True
    return False

def is_too_long(prompt):
    """
    Checks if the prompt is too long.
    """
    return len(prompt) > 300

def get_error_message():
    """
    Returns a generic error message.
    """
    return "Sorry, something went wrong. Please try again."

def check_safety(prompt):
    """
    Runs all safety checks on the prompt.
    """
    if is_prompt_injection(prompt):
        return "Error: Prompt injection attempt detected."
    if is_too_long(prompt):
        return "Error: Input is too long. Please keep your question under 300 characters."
    return None
