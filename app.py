# app.py
import streamlit as st

from safety import is_urgent, SAFETY_MESSAGE
from responses import generate_reply

st.set_page_config(page_title="Mental Aid Assistant", page_icon="🌿", layout="centered")

# --- Session state -----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello. I'm here to listen. What's on your mind today?",
    }]
if "contacts" not in st.session_state:
    st.session_state.contacts = {k: "" for k in
        ("therapist", "crisis", "emergency", "trusted", "other")}

# --- Sidebar navigation -----------------------------------------------
page = st.sidebar.radio(
    "Navigate",
    ["Welcome", "Check-in", "Chat", "Exercises", "Human Support"],
)

# --- Welcome -----------------------------------------------------------
if page == "Welcome":
    st.title("🌿 Mental Aid Assistant")
    st.write("A calm space for everyday stress, mild anxiety, loneliness, "
             "and sleep difficulties.")
    st.warning(
        "**Please read:** I am an **AI assistant**, not a therapist or "
        "mental-health professional. I do not provide diagnosis, medication "
        "advice, or emergency care. I cannot guarantee safety or replace "
        "human support. If you are in danger, contact local emergency "
        "services or a trusted person right away."
    )
    st.info("Nothing you type is stored on a server. Your conversation lives "
            "only in this browser session and can be deleted from the Chat page.")

# --- Check-in ----------------------------------------------------------
elif page == "Check-in":
    st.title("Emotional Check-in")
    st.caption("One gentle question at a time. You can stop whenever you like.")

    feeling = st.text_input("How are you feeling today?",
                            placeholder="e.g., tired, anxious, okay…")
    distress = st.slider("What is your distress level from 0 to 10?", 0, 10, 5)
    support = st.selectbox(
        "What type of support would you like?",
        ["Just to be heard", "A coping exercise",
         "Help organizing my thoughts", "Contact information for a real person"],
    )

    if st.button("Continue"):
        st.subheader("Thank you for checking in")
        st.write(f"You described feeling: **{feeling or '(not specified)'}**. "
                 f"Distress level: **{distress}/10**.")

        if distress >= 8:
            st.error(
                "That is a high level of distress. Please consider reaching out "
                "to a trusted person or a professional now — see the "
                "**Human Support** page. If you ever feel unsafe, contact your "
                "local emergency services."
            )
            st.info("→ Open the **Human Support** page in the sidebar.")
        elif distress >= 5:
            st.info("That sounds difficult. A short coping exercise may help a "
                    "little, and reaching out to a trusted person is often "
                    "helpful too.")
            st.info("→ Consider the **Exercises** page.")
        else:
            st.success("Thank you for checking in. Gentle steps are often "
                       "enough. Here is one option for you.")
            st.info({
                "Just to be heard": "→ Try the **Chat** page.",
                "A coping exercise": "→ Try the **Exercises** page.",
                "Help organizing my thoughts": "→ Use **Thought Organization** "
                                               "on the Exercises page.",
                "Contact information for a real person": "→ Open **Human Support**.",
            }[support])

# --- Chat --------------------------------------------------------------
elif page == "Chat":
    st.title("Supportive Chat")
    st.caption("This is a brief supportive conversation, not therapy. "
               "Please avoid sharing identifying personal information.")

    # Replay history
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if st.button("🗑️ Delete current conversation"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hello. I'm here to listen. What's on your mind today?",
        }]
        st.rerun()

    user_msg = st.chat_input("Type a message…")
    if user_msg:
        # 1) Append user message
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        # 2) SAFETY CHECK BEFORE ANY CHATBOT RESPONSE
        if is_urgent(user_msg):
            st.session_state.messages.append(
                {"role": "assistant", "content": SAFETY_MESSAGE}
            )
            with st.chat_message("assistant"):
                st.error(SAFETY_MESSAGE)
        else:
            reply = generate_reply(user_msg)
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )
            with st.chat_message("assistant"):
                st.markdown(reply)

# --- Exercises ---------------------------------------------------------
elif page == "Exercises":
    st.title("Coping Exercises")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Slow Breathing")
        st.caption("Inhale 4 · Hold 4 · Exhale 6. Follow the guidance below.")
        st.info("👃 Breathe in… (4)\n\n⏸ Hold… (4)\n\n👄 Breathe out… (6)")
        st.caption("Repeat 4–6 times, at your own pace.")

    with c2:
        st.subheader("Five-Senses Grounding")
        st.markdown(
            "- 👀 **5** things you can see\n"
            "- ✋ **4** things you can touch\n"
            "- 👂 **3** things you can hear\n"
            "- 👃 **2** things you can smell\n"
            "- 👅 **1** thing you can taste"
        )

    with c3:
        st.subheader("Thought Organization")
        st.text_input("A thought that's bothering me:",
                      key="thought_input",
                      placeholder="e.g., I'll fail everything.")
        st.text_area("One fact for it, one fact against it:",
                     key="thought_evidence", height=90)
        st.text_input("One small, doable next step:",
                      key="thought_small",
                      placeholder="e.g., write 3 bullet points")
        st.caption("These notes are not saved anywhere.")

# --- Human Support -----------------------------------------------------
elif page == "Human Support":
    st.title("Human Support")
    st.caption(
        "These fields are **placeholders**. Please fill them in with your own "
        "local, verified contacts. This assistant does not provide or invent "
        "emergency numbers."
    )
    labels = {
        "therapist": "Therapist / counselor (name & phone)",
        "crisis":    "Local crisis line (name & number)",
        "emergency": "Emergency services number (your country)",
        "trusted":   "Trusted person (name & phone)",
        "other":     "Other helpful contact",
    }
    for key, label in labels.items():
        st.session_state.contacts[key] = st.text_input(
            label, value=st.session_state.contacts[key], key=f"field_{key}"
        )
    st.success("Contacts stay in this browser session only — "
               "they are never sent to a server.")