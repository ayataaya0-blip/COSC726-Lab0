import streamlit as st


def render_sidebar(
    text: dict,
    current_language: str,
) -> dict:
    """
    Render the application sidebar.

    Returns the student's current interface and
    learning-path selections.
    """

    # =====================================================
    # Language
    # =====================================================

    with st.sidebar:

        st.markdown(
            "### 🌐 Language / اللغة"
        )

        selected_language = st.selectbox(
            "Interface Language",
            ["English", "العربية"],
            index=(
                0
                if current_language == "English"
                else 1
            ),
            label_visibility="collapsed",
        )

        language = (
            "English"
            if selected_language == "English"
            else "Arabic"
        )

        # =================================================
        # Learning Path
        # =================================================

        st.divider()

        st.header(
            f"📚 {text['learning_path']}"
        )

        # -------------------------------------------------
        # Mathematics
        # -------------------------------------------------

        st.markdown(
            f"**{text['mathematics']}**"
        )

        math_topic = st.selectbox(
            "Mathematics",
            [
                text["linear_equations"],
                text["functions"],
                text["algebra"],
            ],
            index=0,
            label_visibility="collapsed",
        )

        # -------------------------------------------------
        # Algorithms
        # -------------------------------------------------

        st.markdown(
            f"**{text['algorithms']}**"
        )

        algorithm_topic = st.selectbox(
            "Algorithms",
            [
                text["linear_search"],
                text["binary_search"],
                text["sorting"],
                "Big-O Notation",
            ],
            index=0,
            label_visibility="collapsed",
        )

        # -------------------------------------------------
        # Data Structures
        # -------------------------------------------------

        st.markdown(
            f"**{text['data_structures']}**"
        )

        data_structure_topic = st.selectbox(
            "Data Structures",
            [
                text["arrays"],
                text["stack"],
                text["queue"],
            ],
            index=0,
            label_visibility="collapsed",
        )

        # =================================================
        # Student Progress
        # =================================================

        st.divider()

        st.subheader(
            f"📊 {text['student_progress']}"
        )

        progress = st.session_state.get(
            "progress",
            0,
        )

        st.progress(
            progress / 100
        )

        st.caption(
            f"{text['overall_progress']}: "
            f"{progress}%"
        )

    # =====================================================
    # Return Sidebar State
    # =====================================================

    return {
        "language": language,
        "math_topic": math_topic,
        "algorithm_topic": algorithm_topic,
        "data_structure_topic": data_structure_topic,
    }