import streamlit as st


def render_actions(text: dict) -> str | None:

    st.divider()

    st.subheader(
        f"🧠 {text['practice']}"
    )

    col1, col2, col3, col4 = st.columns(4)

    action = None

    with col1:

        if st.button(
            f"💡 {text['hint']}",
            use_container_width=True,
        ):

            action = "hint"

    with col2:

        if st.button(
            f"📚 {text['explain']}",
            use_container_width=True,
        ):

            action = "explain"

    with col3:

        if st.button(
            f"📝 {text['practice_action']}",
            use_container_width=True,
        ):

            action = "practice"

    with col4:

        if st.button(
            f"❓ {text['quiz']}",
            use_container_width=True,
        ):

            action = "quiz"

    if action == "hint":

        st.info(
            text["hint_message"]
        )

    elif action == "explain":

        st.info(
            text["explain_message"]
        )

    elif action == "practice":

        st.success(
            text["practice_message"]
        )

    elif action == "quiz":

        st.success(
            text["quiz_message"]
        )

    return action