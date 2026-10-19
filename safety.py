# safety.py
"""Keyword-based safety detection. Pure functions, no Streamlit dependency."""
import re

SAFETY_PATTERNS = [
    # Self-harm / suicide
    r"kill myself", r"killing myself", r"suicid", r"end (my|it all) (life|now)",
    r"want to die", r"don'?t want to (live|be here)", r"hurt myself",
    r"self[- ]?harm", r"cut myself", r"cutting myself", r"overdose",
    r"no reason to live", r"better off dead",
        # Self-harm / suicide
    r"kill myself", r"killing myself", r"suicid", r"end (my|it all) (life|now)",
    r"want to die", r"don'?t want to (live|be here)", r"harm(ing)? myself", 
    r"hurt(ing)? myself", r"self[- ]?harm", r"cut(ting)? myself", r"overdose",
    r"no reason to live", r"better off dead",
    # Harm to others
    r"kill (him|her|them|someone|people)", r"hurt (him|her|them|someone|people)",
    r"harm (him|her|them|someone|people)", r"shoot (him|her|them|up|people)",
    r"stab (him|her|them|someone)",
    # Immediate danger
    r"immediate danger", r"in danger right now", r"unsafe right now",
    r"someone is (attacking|threatening) me", r"being attacked",
    r"i have a (weapon|gun|knife)",
]
_SAFETY_RE = re.compile("|".join(SAFETY_PATTERNS), re.IGNORECASE)


def is_urgent(text: str) -> bool:
    """Return True if the text matches any safety pattern."""
    return bool(text and _SAFETY_RE.search(text))


SAFETY_MESSAGE = """⚠️ It sounds like you may be in a serious or unsafe situation.

I am an AI and cannot help with emergencies. Please stop the conversation with me
and reach out to a real person right now:

• A trusted friend, family member, or nearby person.
• A local crisis line or mental-health professional (see the Human Support page
  for your own verified contacts).
• Your local emergency services if you or someone else is in immediate danger.

You deserve immediate human support. If you can, please contact someone now."""