
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from main import run_tutor, conversation_store
from schemas.input_schema import TutorInput

from ui.localization.en import TEXT as EN_TEXT
from ui.localization.ar import TEXT as AR_TEXT

from ui.components.sidebar import render_sidebar
from ui.components.lesson import render_lesson
from ui.components.tutor import render_tutor
from ui.components.actions import render_actions


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Educational Tutor",
    page_icon="🎓",
    layout="wide",
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "student_id" not in st.session_state:
    st.session_state.student_id = "default_student"

if "progress" not in st.session_state:
    st.session_state.progress = 0


# --------------------------------------------------
# Localization
# --------------------------------------------------

current_text = (
    EN_TEXT
    if st.session_state.language == "English"
    else AR_TEXT
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

selections = render_sidebar(
    current_text,
    st.session_state.language,
)

st.session_state.language = selections["language"]


# Reload the correct translation dictionary

text = (
    EN_TEXT
    if st.session_state.language == "English"
    else AR_TEXT
)


# --------------------------------------------------
# Language Direction (RTL / LTR)
# --------------------------------------------------

if st.session_state.language == "Arabic":

    st.markdown(
        """
        <style>

        /* Main application direction */
        .stApp {
            direction: rtl;
            text-align: right;
        }

        /* Main content */
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            direction: rtl;
            text-align: right;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            direction: rtl;
            text-align: right;
        }

        [data-testid="stSidebar"] * {
            text-align: right;
        }

        /* Headings and text */
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp p,
        .stApp li,
        .stApp label,
        .stApp [data-testid="stMarkdownContainer"] {
            direction: rtl;
            text-align: right;
        }

        /* Chat messages */
        [data-testid="stChatMessage"] {
            direction: rtl;
            text-align: right;
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            direction: rtl;
            text-align: right;
        }

        /* Text inputs */
        .stTextInput input,
        .stTextArea textarea,
        [data-testid="stChatInput"] textarea {
            direction: rtl;
            text-align: right;
        }

        /* Select boxes */
        [data-testid="stSelectbox"] {
            direction: rtl;
            text-align: right;
        }

        /* Buttons */
        .stButton button {
            direction: rtl;
        }

        /* Preserve left-to-right mathematical expressions */
        .katex,
        .katex-display,
        .stCode,
        pre,
        code {
            direction: ltr !important;
            text-align: left !important;
        }

        .katex-display {
            text-align: center !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

else:

    st.markdown(
        """
        <style>

        /* English application direction */
        .stApp {
            direction: ltr;
            text-align: left;
        }

        [data-testid="stSidebar"] {
            direction: ltr;
            text-align: left;
        }

        [data-testid="stChatMessage"] {
            direction: ltr;
            text-align: left;
        }

        .stTextInput input,
        .stTextArea textarea,
        [data-testid="stChatInput"] textarea {
            direction: ltr;
            text-align: left;
        }

        pre,
        code {
            direction: ltr;
            text-align: left;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Active Subject Selection
# --------------------------------------------------

active_subject_label = st.sidebar.selectbox(
    "Active Subject"
    if st.session_state.language == "English"
    else "المادة الحالية",
    [
        text["mathematics"],
        text["algorithms"],
        text["data_structures"],
    ],
)


# --------------------------------------------------
# Subject and Topic Selection
# --------------------------------------------------

if active_subject_label == text["mathematics"]:

    subject = "Mathematics"
    selected_topic = selections["math_topic"]

elif active_subject_label == text["algorithms"]:

    subject = "Algorithms"
    selected_topic = selections["algorithm_topic"]

else:

    subject = "Data Structures"
    selected_topic = selections["data_structure_topic"]


# --------------------------------------------------
# Topic Mapping
# --------------------------------------------------

topic_mapping = {

    text["linear_equations"]: "Linear Equations",
    text["functions"]: "Functions",
    text["algebra"]: "Algebra",

    text["linear_search"]: "Linear Search",
    text["binary_search"]: "Binary Search",
    text["sorting"]: "Sorting",
    "Big-O Notation": "Big-O Notation",

    text["arrays"]: "Arrays",
    text["stack"]: "Stack",
    text["queue"]: "Queue",
    

}

topic = topic_mapping.get(
    selected_topic,
    selected_topic,
)


# --------------------------------------------------
# New Exercise Button
# --------------------------------------------------

if st.session_state.language == "English":

    button_label = "🆕 New Exercise"
    success_message = (
        "Previous exercise cleared. "
        "You can request a new exercise now."
    )

else:

    button_label = "🆕 تمرين جديد"
    success_message = (
        "تم إلغاء التمرين السابق. "
        "يمكنك طلب تمرين جديد الآن."
    )

if st.sidebar.button(button_label, use_container_width=True):

    conversation_store.clear_pending_exercise(
        st.session_state.student_id
    )

    st.session_state.progress = 0

    st.sidebar.success(success_message)

    st.rerun()


# --------------------------------------------------
# End Pending Quiz Button
# --------------------------------------------------

if st.session_state.language == "English":

    end_quiz_label = "🛑 End Pending Quiz"
    end_quiz_message = "The pending quiz has been ended successfully."

else:

    end_quiz_label = "🛑 إنهاء الاختبار المعلّق"
    end_quiz_message = "تم إنهاء الاختبار المعلّق بنجاح."

if st.sidebar.button(
    end_quiz_label,
    use_container_width=True,
):

    conversation_store.clear_pending_quiz(
        st.session_state.student_id
    )

    st.sidebar.success(end_quiz_message)

    st.rerun()

# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title(f"🎓 {text['app_title']}")
st.caption(text["app_caption"])

st.divider()


# --------------------------------------------------
# Current Lesson
# --------------------------------------------------
# --------------------------------------------------
# Current Lesson
# --------------------------------------------------

render_lesson(
    text,
    st.session_state.language,
    topic,
)


   
    


# --------------------------------------------------
# Tutor Response Handler
# --------------------------------------------------


def ask_agent(message: str, force_new_exercise: bool = False):

    print("DEBUG: Message received:", message)
    print("DEBUG: Force new exercise:", force_new_exercise)
    
    print("DEBUG: Selected subject:", subject)
    print("DEBUG: Selected topic:", topic)
    print("DEBUG: Sidebar selections:", selections)

    request = TutorInput(
        student_id=st.session_state.student_id,
        message=message,
        language=st.session_state.language,
        subject=subject,
        topic=topic,
        force_new_exercise=force_new_exercise,
    )

    try:

        result = run_tutor(request)

        print("DEBUG: Agent returned:", result)

        response = result.response

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
        })

        st.session_state.progress = min(
            100,
            st.session_state.progress + 5,
        )

    except Exception as error:

        print("DEBUG: Agent Error:", error)

        st.error(
            f"Agent Error: {error}"
        )
# --------------------------------------------------
# Chat Interface
# --------------------------------------------------

user_message = render_tutor(
    text,
    st.session_state.language,
    st.session_state.messages,
)


# --------------------------------------------------
# Learning Actions
# --------------------------------------------------

action = render_actions(text)


# --------------------------------------------------
# Process User Input
# --------------------------------------------------

if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message,
    })

    ask_agent(user_message)

    st.rerun()


# --------------------------------------------------
# Process Learning Actions
# --------------------------------------------------

if action:

    if st.session_state.language == "English":

        action_messages = {

            "hint": f"Give me a helpful hint about {topic}.",

            "explain": f"Explain {topic} step by step.",

            "practice": f"Give me a practice exercise about {topic}.",

            "quiz": f"Quiz me about {topic} with a question.",

        }

    else:

        action_messages = {

            "hint": f"أعطني تلميحاً يساعدني في فهم موضوع {topic}.",

            "explain": f"اشرح لي موضوع {topic} خطوة بخطوة.",

            "practice": f"أعطني تمريناً للتدرب على موضوع {topic}.",

            "quiz": f"اختبر فهمي لموضوع {topic} بسؤال.",

        }

    action_message = action_messages[action]

    st.session_state.messages.append({
        "role": "user",
        "content": action_message,
    })

    
    ask_agent(action_message)
    st.rerun()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    text["footer"]
)
