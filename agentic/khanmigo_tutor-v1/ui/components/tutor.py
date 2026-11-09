
import streamlit as st


def render_tutor(
    text: dict,
    language: str,
    messages: list,
) -> str | None:

    st.markdown(
        f"### 🤖 {text['ai_tutor']}"
    )

    st.caption(
        text["educational_assistant"]
    )

    for message in messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"],
                unsafe_allow_html=False,
            )

    user_message = st.chat_input(
        text["ask_tutor"]
    )

    return user_message
