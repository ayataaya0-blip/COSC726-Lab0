# AI Educational Tutor
### Khanmigo-Inspired Agentic Educational Tutor

## 1. What It Does

AI Educational Tutor is a Khanmigo-inspired educational tutoring system designed to support students through interactive and personalized learning.

The system uses a local Large Language Model (LLM), an agentic workflow, educational knowledge retrieval, and computational tools to support learning in Mathematics, Algorithms, and Data Structures.

Its main capabilities include:

- Concept explanations.
- Step-by-step educational guidance.
- Hints and practice exercises.
- Quiz generation and answer evaluation.
- Basic mathematical calculations.
- Code and algorithm analysis.
- English and Arabic interface support.
- Conversation and pending activity persistence.

The tutor is designed to guide students through the learning process rather than simply provide direct answers.

## 2. Prerequisites

The following software is required:

- Python 3.12
- Ollama
- Qwen 2.5 3B model
- Git

Install the model:


ollama pull qwen2.5:3b

Ensure that Ollama is running locally.

## 3. Installation

Clone the repository:


git clone YOUR_GITHUB_REPOSITORY_URL


Navigate to the project directory:


cd khanmigo_tutor-v1


Create a virtual environment:


python -m venv .venv


Activate it on Windows:


.venv\Scripts\activate


Install dependencies:


pip install -r requirements.txt


## 4. Configuration

The system uses a local Ollama model.

Default model:

qwen2.5:3b


Default Ollama endpoint:


http://localhost:11434


The model and endpoint are configured in:


llm/model.py


No external API key is required by the reviewed local LLM configuration.

## 5. Run the Application

From the project root directory, run:

python -m streamlit run ui/app.py


Open the application in a browser:

http://localhost:8501

The application provides a bilingual interface with subject and topic selection, educational lessons, conversational tutoring, and learning actions.

## 6. Testing

The project includes an automated offline test suite using pytest.

Run the tests from the project root:

python -m pytest tests/ -v

The test suite contains 9 tests:

| Test file | Tests | Result |
|---|---:|---|
| test_input_schema.py | 5 | Passed |
| test_student_memory.py | 4 | Passed |
| **Total** | **9** | **9 passed** |

Latest recorded result:


9 passed in 0.04s


The tests cover input validation, default values, invalid inputs, and student memory operations.

## 7. Worked Example

Example: Linear Search

Student request:


Give me a practice exercise about Linear Search.

Example generated exercise:


Given the array [4, 2, 5, 1, 3, 6, 7],
find the zero-based index of the target value 5.


Expected answer:




The tutor evaluates the student's submission and provides feedback.

## 8. Evaluation

The project includes an offline component evaluation harness and a JSON evaluation task set.

Evaluation files:


evaluation/
├── tasks.json
└── run_evaluation.py


Run the evaluation from the project root:

python evaluation/run_evaluation.py


The evaluation contains 9 tasks:

| Category | Tasks | Passed |
|---|---:|---:|
| Input Validation | 5 | 5 |
| Student Memory | 4 | 4 |
| **Total** | **9** | **9** |

Recorded evaluation results:

- Total tasks: 9
- Passed: 9
- Failed: 0
- Pass rate: 100.00%

These results apply only to the evaluated input-validation and student-memory components. They do not represent an end-to-end evaluation of the complete tutor, LLM response quality, or pedagogical effectiveness.

## 9. Approval Gate

The current implementation includes input, action, and output validation gates within its LangGraph workflow.

These gates check input conditions, permitted action names, and final response structure.

A separate human approval mechanism for consequential actions has not been implemented.

## 10. Repository Structure

khanmigo_tutor-v1/
│
├── agent/
├── graph/
├── knowledge/
│   └── data/
├── llm/
├── memory/
├── schemas/
├── tools/
├── ui/
│   ├── components/
│   └── localization/
├── prompts/
├── tests/
│   ├── test_input_schema.py
│   └── test_student_memory.py
├── evaluation/
│   ├── tasks.json
│   └── run_evaluation.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

The project also uses a local SQLite database for conversation and activity persistence.

## 11. Limitations

- The language model operates locally through Ollama.
- Knowledge retrieval uses lexical and keyword-based scoring.
- Student mastery tracking is limited.
- Current automated tests cover input validation and student memory only.
- The evaluation framework covers selected components rather than the complete agent.
- A separate human approval gate is not implemented.
- The application has not been verified on a clean, separate machine.
- Some educational content and validation rules are topic-specific.

## Future Work

Future development may include expanded automated testing, end-to-end evaluation, improved student modelling, broader topic validation, and human approval controls.