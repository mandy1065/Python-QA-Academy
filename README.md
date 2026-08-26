# Python QA Academy

Interactive beginner Python course for QA automation students, built with Streamlit.

## Learning path

1. print()
2. Variables
3. Data Types
4. Strings
5. Operators
6. Lists
7. Dictionaries
8. if / else
9. for loops
10. while loops
11. Functions
12. Final Python QA Mini Project

Each module includes:
- Easy notes
- Working QA-style example
- In-browser practice editor
- Run code / see output
- Hint
- Separate assignment
- AI or local evaluation
- Score and progress tracking

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

- Repository: `mandy1065/Python-QA-Academy`
- Branch: `main`
- Main file: `app.py`

For AI grading, add these Streamlit secrets:

```toml
OPENAI_API_KEY = "YOUR_REAL_OPENAI_API_KEY"
OPENAI_MODEL = "gpt-5.4-nano"
```

If no OpenAI key is configured, the app still runs and uses a simpler local assignment evaluator.

## Safety note

The practice runner is deliberately restricted to beginner Python constructs. Imports and dangerous built-ins are blocked. It is intended for introductory learning only.
