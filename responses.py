# responses.py
"""Non-diagnostic, non-medical reply logic. One question at a time."""
import re

DIAGNOSIS_RE = re.compile(r"(depress|anxiety disorder|bipolar|ptsd|adhd|diagnos)", re.I)
MEDICATION_RE = re.compile(
    r"(medication|meds|antidepressant|pills|dose|dosage|stop taking|change my treatment)",
    re.I,
)


def generate_reply(text: str) -> str:
    """Return a short, supportive reply. Never diagnoses or prescribes."""
    t = text.lower()

    # Refusals first
    if DIAGNOSIS_RE.search(t) and "?" in text:
        return (
            "I can't diagnose mental-health conditions — only a qualified "
            "professional can. If you're wondering about this, a doctor or therapist "
            "can help. Would you like to try a grounding exercise while you think "
            "about your next step?"
        )
    if MEDICATION_RE.search(t):
        return (
            "I can't advise on medication or treatment changes — please speak with "
            "the professional who prescribed it. Would you like to talk about how "
            "you're feeling right now instead?"
        )

    # Supportive reflections
    if re.search(r"exam|test|study|school|deadline|work", t):
        return ("That sounds like a lot of pressure. What's one small part of it "
                "you could take a break from for a few minutes?")
    if re.search(r"sleep|insomnia|overthink|awake|tired", t):
        return ("Overthinking at night can feel endless. Would it help to try a "
                "slow-breathing exercise together?")
    if re.search(r"lonely|alone|no one|isolated", t):
        return ("Loneliness is heavy. Is there one person — even a distant one — "
                "you could send a short message to today?")
    if re.search(r"stress|anxious|anxiety|overwhelm|panic", t):
        return ("That sounds uncomfortable. Would you like to describe what's "
                "happening, or try a short grounding exercise?")
    if re.search(r"sad|down|low|empty|hopeless", t):
        return "Thank you for saying that. What's been the hardest part of today?"
    if re.search(r"thank|thanks", t):
        return "You're welcome. Would you like to keep talking, or take a pause?"
    return ("I'm listening. Can you tell me a little more about what's going on "
            "right now?")