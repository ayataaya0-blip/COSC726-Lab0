
import sqlite3
import json
import re
from pathlib import Path
from typing import Any


class ConversationStore:
    """
    Stores student conversations, tool execution history,
    pending quizzes, pending exercises, and exercise history.
    """

    def __init__(self, database_path: str | None = None) -> None:

        if database_path is None:
            project_root = Path(__file__).resolve().parent.parent
            database_path = str(
                project_root / "conversations.db"
            )

        self.database_path = database_path

        self._initialize_database()

    # =====================================================
    # Database Connection
    # =====================================================

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    # =====================================================
    # Database Initialization
    # =====================================================

    def _initialize_database(self) -> None:

        with self._connect() as connection:

            # -------------------------------------------------
            # Conversation Messages
            # -------------------------------------------------

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_student_messages
                ON messages(student_id, id)
                """
            )

            # -------------------------------------------------
            # Tool Execution History
            # -------------------------------------------------

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tool_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    action TEXT,
                    tool TEXT,
                    tool_request TEXT,
                    tool_result TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # -------------------------------------------------
            # Pending Quizzes
            # -------------------------------------------------

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS pending_quizzes (
                    student_id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    expected_answer TEXT NOT NULL,
                    subject TEXT,
                    topic TEXT,
                    language TEXT,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # -------------------------------------------------
            # Pending Exercises
            # -------------------------------------------------

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS pending_exercises (
                    student_id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    expected_answer TEXT NOT NULL,
                    subject TEXT,
                    topic TEXT,
                    language TEXT,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # -------------------------------------------------
            # Exercise History
            # -------------------------------------------------

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS exercise_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    question_key TEXT NOT NULL,
                    subject TEXT,
                    topic TEXT,
                    language TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(student_id, question_key)
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_student_exercise_history
                ON exercise_history(student_id, id)
                """
            )

            # -------------------------------------------------
            # Safe Database Migration: Pending Exercises
            # -------------------------------------------------

            columns = connection.execute(
                "PRAGMA table_info(pending_exercises)"
            ).fetchall()

            column_names = {
                column[1]
                for column in columns
            }

            if "attempts" not in column_names:

                connection.execute(
                    """
                    ALTER TABLE pending_exercises
                    ADD COLUMN attempts INTEGER NOT NULL DEFAULT 0
                    """
                )

            # -------------------------------------------------
            # Safe Database Migration: Pending Quizzes
            # -------------------------------------------------

            columns = connection.execute(
                "PRAGMA table_info(pending_quizzes)"
            ).fetchall()

            column_names = {
                column[1]
                for column in columns
            }

            if "attempts" not in column_names:

                connection.execute(
                    """
                    ALTER TABLE pending_quizzes
                    ADD COLUMN attempts INTEGER NOT NULL DEFAULT 0
                    """
                )

            # -------------------------------------------------
            # Tool History Index
            # -------------------------------------------------

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_student_tool_executions
                ON tool_executions(student_id, id)
                """
            )

    # =====================================================
    # Conversation History
    # =====================================================

    def get_history(
        self,
        student_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT role, content
                FROM messages
                WHERE student_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (student_id, limit),
            ).fetchall()

        rows.reverse()

        return [
            {
                "role": role,
                "content": content,
            }
            for role, content in rows
        ]

    # =====================================================
    # Save Conversation Exchange
    # =====================================================

    def save_exchange(
        self,
        student_id: str,
        user_message: str,
        assistant_response: str,
    ) -> None:

        with self._connect() as connection:

            connection.executemany(
                """
                INSERT INTO messages (
                    student_id,
                    role,
                    content
                )
                VALUES (?, ?, ?)
                """,
                [
                    (student_id, "user", user_message),
                    (student_id, "assistant", assistant_response),
                ],
            )

    # =====================================================
    # Tool Execution History
    # =====================================================

    def save_tool_execution(
        self,
        student_id: str,
        execution: dict[str, Any],
    ) -> None:

        tool_result = execution.get("tool_result") or {}

        tool_request_json = json.dumps(
            execution.get("tool_request"),
            ensure_ascii=False,
            default=str,
        )

        tool_result_json = json.dumps(
            tool_result,
            ensure_ascii=False,
            default=str,
        )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO tool_executions (
                    student_id,
                    action,
                    tool,
                    tool_request,
                    tool_result
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    execution.get("action"),
                    tool_result.get("tool"),
                    tool_request_json,
                    tool_result_json,
                ),
            )

    # =====================================================
    # Get Tool History
    # =====================================================

    def get_tool_history(
        self,
        student_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT
                    action,
                    tool,
                    tool_request,
                    tool_result,
                    created_at
                FROM tool_executions
                WHERE student_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (student_id, limit),
            ).fetchall()

        rows.reverse()

        history = []

        for row in rows:

            action, tool, request, result, created_at = row

            history.append(
                {
                    "action": action,
                    "tool": tool,
                    "tool_request": json.loads(request)
                    if request else None,
                    "tool_result": json.loads(result)
                    if result else None,
                    "created_at": created_at,
                }
            )

        return history

    # =====================================================
    # Exercise Question Normalization
    # =====================================================

    @staticmethod
    def _normalize_exercise_question(
        question: str,
    ) -> str:
        """Create a stable key to detect repeated exercises."""

        cleaned = question.lower()

        cleaned = cleaned.replace("−", "-")
        cleaned = cleaned.replace("×", "*")
        cleaned = cleaned.replace("÷", "/")

        cleaned = re.sub(
            r"\\(?:left|right)",
            "",
            cleaned,
        )

        cleaned = re.sub(
            r"\\[()\[\]]",
            "",
            cleaned,
        )

        equation = re.search(
            r"[0-9x.+\-*/()]+=[0-9x.+\-*/()]+",
            cleaned,
        )

        if equation:
            return (
                "equation:"
                + re.sub(r"\s+", "", equation.group(0))
            )

        return (
            "question:"
            + re.sub(r"[^\w]", "", cleaned)
        )

    # =====================================================
    # Get Exercise History
    # =====================================================

    def get_exercise_history(
        self,
        student_id: str,
        subject: str | None = None,
        topic: str | None = None,
        limit: int = 100,
    ) -> list[str]:
        """Retrieve previously presented exercises."""

        query = """
            SELECT question
            FROM exercise_history
            WHERE student_id = ?
        """

        parameters: list[Any] = [student_id]

        if subject:
            query += " AND subject = ?"
            parameters.append(subject)

        if topic:
            query += " AND topic = ?"
            parameters.append(topic)

        query += """
            ORDER BY id DESC
            LIMIT ?
        """

        parameters.append(limit)

        with self._connect() as connection:

            rows = connection.execute(
                query,
                parameters,
            ).fetchall()

        return [
            row[0]
            for row in rows
        ]

    # =====================================================
    # Pending Quiz Management
    # =====================================================

    def save_pending_quiz(
        self,
        student_id: str,
        quiz: dict[str, Any],
    ) -> None:
        """Save a new pending quiz with a fresh attempt counter."""

        with self._connect() as connection:

            connection.execute(
                """
                INSERT OR REPLACE INTO pending_quizzes (
                    student_id,
                    question,
                    expected_answer,
                    subject,
                    topic,
                    language,
                    attempts
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    quiz["question"],
                    quiz["expected_answer"],
                    quiz.get("subject"),
                    quiz.get("topic"),
                    quiz.get("language"),
                    quiz.get("attempts", 0),
                ),
            )

    def get_pending_quiz(
        self,
        student_id: str,
    ) -> dict[str, Any] | None:
        """Retrieve the pending quiz, including its attempt count."""

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    question,
                    expected_answer,
                    subject,
                    topic,
                    language,
                    attempts
                FROM pending_quizzes
                WHERE student_id = ?
                """,
                (student_id,),
            ).fetchone()

        if row is None:
            return None

        return {
            "question": row[0],
            "expected_answer": row[1],
            "subject": row[2],
            "topic": row[3],
            "language": row[4],
            "attempts": row[5],
        }

    def increment_quiz_attempts(
        self,
        student_id: str,
    ) -> int:
        """Increment and return the number of quiz attempts."""

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE pending_quizzes
                SET attempts = attempts + 1
                WHERE student_id = ?
                """,
                (student_id,),
            )

            row = connection.execute(
                """
                SELECT attempts
                FROM pending_quizzes
                WHERE student_id = ?
                """,
                (student_id,),
            ).fetchone()

        return row[0] if row is not None else 0

    def clear_pending_quiz(
        self,
        student_id: str,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM pending_quizzes
                WHERE student_id = ?
                """,
                (student_id,),
            )

    # =====================================================
    # Pending Exercise Management
    # =====================================================

    def save_pending_exercise(
        self,
        student_id: str,
        exercise: dict[str, Any],
    ) -> None:
        """Save the pending exercise and record its history."""

        question = exercise["question"]

        question_key = self._normalize_exercise_question(
            question
        )

        with self._connect() as connection:

            # Save the active exercise.
            connection.execute(
                """
                INSERT OR REPLACE INTO pending_exercises (
                    student_id,
                    question,
                    expected_answer,
                    subject,
                    topic,
                    language,
                    attempts
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    question,
                    exercise["expected_answer"],
                    exercise.get("subject"),
                    exercise.get("topic"),
                    exercise.get("language"),
                    exercise.get("attempts", 0),
                ),
            )

            # Record the presented exercise permanently.
            connection.execute(
                """
                INSERT OR IGNORE INTO exercise_history (
                    student_id,
                    question,
                    question_key,
                    subject,
                    topic,
                    language
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    question,
                    question_key,
                    exercise.get("subject"),
                    exercise.get("topic"),
                    exercise.get("language"),
                ),
            )

    def get_pending_exercise(
        self,
        student_id: str,
    ) -> dict[str, Any] | None:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    question,
                    expected_answer,
                    subject,
                    topic,
                    language,
                    attempts
                FROM pending_exercises
                WHERE student_id = ?
                """,
                (student_id,),
            ).fetchone()

        if row is None:
            return None

        return {
            "question": row[0],
            "expected_answer": row[1],
            "subject": row[2],
            "topic": row[3],
            "language": row[4],
            "attempts": row[5],
        }

    # =====================================================
    # Increment Exercise Attempts
    # =====================================================

    def increment_exercise_attempts(
        self,
        student_id: str,
    ) -> int:

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE pending_exercises
                SET attempts = attempts + 1
                WHERE student_id = ?
                """,
                (student_id,),
            )

            row = connection.execute(
                """
                SELECT attempts
                FROM pending_exercises
                WHERE student_id = ?
                """,
                (student_id,),
            ).fetchone()

        return row[0] if row is not None else 0

    # =====================================================
    # Clear Pending Exercise
    # =====================================================

    def clear_pending_exercise(
        self,
        student_id: str,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM pending_exercises
                WHERE student_id = ?
                """,
                (student_id,),
            )
