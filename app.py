import ast
import io
import json
import contextlib
from datetime import datetime

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Python QA Academy", page_icon="🐍", layout="wide")

MODEL = st.secrets.get("OPENAI_MODEL", "gpt-5.4-nano")
PASS_SCORE = 70

# ---------------- UI ----------------
st.markdown(
    """
    <style>
    .stApp {background:radial-gradient(circle at 8% 0%,rgba(16,185,129,.12),transparent 27%),radial-gradient(circle at 95% 8%,rgba(59,130,246,.10),transparent 24%),#f7fafc;}
    .block-container {max-width:1250px;padding-top:1.3rem;padding-bottom:3rem;}
    .hero {background:linear-gradient(135deg,#052e2b 0%,#064e3b 50%,#0f172a 100%);border-radius:24px;padding:24px 28px;color:white;box-shadow:0 18px 45px rgba(15,23,42,.18);margin-bottom:16px;}
    .hero-title {font-size:30px;font-weight:850;letter-spacing:-.02em;}
    .hero-copy {color:#cbd5e1;font-size:14px;margin-top:3px;}
    .chip-row {display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;}
    .chip {padding:6px 10px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);font-size:12px;font-weight:700;color:#e2e8f0;}
    .kicker {color:#059669;font-size:12px;font-weight:850;text-transform:uppercase;letter-spacing:.08em;}
    .title {font-size:23px;font-weight:850;color:#0f172a;margin:2px 0 5px 0;}
    .copy {color:#64748b;font-size:13px;margin-bottom:12px;}
    .note {background:#ecfdf5;border:1px solid #a7f3d0;border-radius:14px;padding:13px 15px;margin:8px 0 12px 0;}
    .mental {background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:12px 14px;margin:8px 0 12px 0;}
    .console {background:#0f172a;color:#e2e8f0;border-radius:14px;padding:14px 16px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap;min-height:58px;}
    .rubric {background:#fff;border:1px solid #e5e7eb;border-radius:15px;padding:13px 15px;height:100%;box-shadow:0 4px 15px rgba(15,23,42,.04);}
    div[data-testid="stMetric"] {background:#fff;border:1px solid #e5e7eb;padding:12px 14px;border-radius:15px;box-shadow:0 4px 15px rgba(15,23,42,.04);}
    .stTabs [data-baseweb="tab-list"] {gap:7px;background:#edf2f7;padding:6px;border-radius:14px;}
    .stTabs [data-baseweb="tab"] {border-radius:10px;height:42px;font-weight:750;}
    .stTabs [aria-selected="true"] {background:#fff!important;box-shadow:0 2px 8px rgba(15,23,42,.08);}
    .stButton>button,.stDownloadButton>button {border-radius:12px;font-weight:750;}
    div[data-testid="stTextArea"] textarea {font-family:ui-monospace,SFMono-Regular,Menlo,monospace;border-radius:12px!important;}
    footer {visibility:hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Course content ----------------
MODULES = [
    {
        "id": "01",
        "title": "print() — Your First Python Code",
        "goal": "Show text and values on the screen.",
        "notes": "print() tells Python to display something. Text must be inside quotes. This is useful in QA when you want to display a test result or debug value.",
        "mental": 'Think: print("PASS") means “show PASS on the screen.”',
        "example": 'print("Hello QA")\nprint("PASS")',
        "practice_prompt": 'Write code that prints exactly: I am learning Python',
        "practice_start": 'print("I am learning Python")',
        "practice_expected": "I am learning Python",
        "hint": 'Use print("...") and keep text inside quotes.',
        "assignment": "Write two print statements. First print: My name is Alex. Second print: I want to become an Automation QA Engineer.",
        "assignment_start": '# Write your answer here\n',
        "assignment_expected": ["My name is Alex", "I want to become an Automation QA Engineer"],
        "rubric": ["Uses print() correctly", "Uses quoted strings", "Produces both required lines", "Readable code"],
    },
    {
        "id": "02",
        "title": "Variables — Store Test Data",
        "goal": "Save values and reuse them later.",
        "notes": "A variable is a named box that stores a value. In QA you might store an expected status code, username, URL, or test result.",
        "mental": "expected_status = 200 means: store 200 inside a box named expected_status.",
        "example": 'expected_status = 200\nactual_status = 200\nprint(expected_status)\nprint(actual_status)',
        "practice_prompt": "Create a variable named browser with value Chrome, then print it.",
        "practice_start": 'browser = "Chrome"\nprint(browser)',
        "practice_expected": "Chrome",
        "hint": 'Use browser = "Chrome" and then print(browser).',
        "assignment": "Create variables test_name = Login Test and status = PASS. Print both values on separate lines.",
        "assignment_start": '# Create test_name and status\n',
        "assignment_expected": ["Login Test", "PASS"],
        "rubric": ["Creates both variables", "Correct values", "Prints both values", "Readable names"],
    },
    {
        "id": "03",
        "title": "Data Types — Text, Numbers and True/False",
        "goal": "Understand string, integer, float and boolean values.",
        "notes": "Common automation data types: str for text, int for whole numbers, float for decimals, bool for True/False. Python decides the type from the value you assign.",
        "mental": '"PASS" is text, 200 is a number, 1.5 is a decimal, True is a boolean.',
        "example": 'test_name = "Login"\nstatus_code = 200\nresponse_time = 1.25\nis_passed = True\nprint(type(test_name).__name__)\nprint(type(status_code).__name__)',
        "practice_prompt": "Create status_code = 404 and is_failed = True. Print both.",
        "practice_start": 'status_code = 404\nis_failed = True\nprint(status_code)\nprint(is_failed)',
        "practice_expected": "404\nTrue",
        "hint": "404 has no quotes. True starts with a capital T and has no quotes.",
        "assignment": "Create qa_name as text, total_tests as 10, pass_rate as 95.5, and automation_ready as True. Print all four.",
        "assignment_start": '# Create the four variables\n',
        "assignment_expected": ["qa_name", "10", "95.5", "True"],
        "rubric": ["Uses four requested data types", "Correct values", "Prints all values", "No unnecessary conversions"],
    },
    {
        "id": "04",
        "title": "Strings — Work With Text",
        "goal": "Combine and inspect text values.",
        "notes": "Strings are text. QA automation uses strings for URLs, names, messages and JSON values. You can combine strings and use methods such as lower() and upper().",
        "mental": 'If result = "PASS", result.lower() becomes "pass".',
        "example": 'test_name = "Login"\nresult = "PASS"\nprint(test_name + " - " + result)\nprint(result.lower())',
        "practice_prompt": "Create message = API TEST PASSED and print it in lowercase.",
        "practice_start": 'message = "API TEST PASSED"\nprint(message.lower())',
        "practice_expected": "api test passed",
        "hint": "Use .lower() after the variable name.",
        "assignment": "Create first = API and second = Automation. Print: API Automation. Then print the same text in uppercase.",
        "assignment_start": '# Work with first and second\n',
        "assignment_expected": ["API Automation", "API AUTOMATION"],
        "rubric": ["Creates both strings", "Combines them correctly", "Uses uppercase operation", "Correct output"],
    },
    {
        "id": "05",
        "title": "Operators — Compare Expected vs Actual",
        "goal": "Compare values and perform simple calculations.",
        "notes": "Automation depends on comparisons. == asks whether two values are equal. != means not equal. > and < compare numbers.",
        "mental": "actual == expected is the basic idea behind an assertion.",
        "example": 'expected = 200\nactual = 200\nprint(actual == expected)\nprint(actual != expected)',
        "practice_prompt": "Set expected = 200 and actual = 404. Print whether they are equal.",
        "practice_start": 'expected = 200\nactual = 404\nprint(actual == expected)',
        "practice_expected": "False",
        "hint": "Use == to compare. A single = assigns a value.",
        "assignment": "Set expected_time = 2 and actual_time = 3. Print whether actual_time is greater than expected_time and whether the values are equal.",
        "assignment_start": '# Compare expected_time and actual_time\n',
        "assignment_expected": ["True", "False"],
        "rubric": ["Uses comparison operators", "Correct variables", "Correct boolean results", "Clear code"],
    },
    {
        "id": "06",
        "title": "Lists — Store Multiple Test Cases",
        "goal": "Keep several values in one ordered collection.",
        "notes": "A list stores multiple values. QA engineers use lists for test names, expected results, browsers, or user IDs.",
        "mental": '["Login", "Search"] is one list containing two test names.',
        "example": 'tests = ["Login", "Search", "Checkout"]\nprint(tests[0])\nprint(len(tests))',
        "practice_prompt": "Create a list with Chrome, Firefox, Edge. Print Firefox.",
        "practice_start": 'browsers = ["Chrome", "Firefox", "Edge"]\nprint(browsers[1])',
        "practice_expected": "Firefox",
        "hint": "List positions start at 0, so the second item is index 1.",
        "assignment": "Create tests = [Login, Search, Checkout]. Print the first test, the last test, and the number of tests.",
        "assignment_start": '# Create and inspect the tests list\n',
        "assignment_expected": ["Login", "Checkout", "3"],
        "rubric": ["Correct list", "Uses indexes correctly", "Uses len()", "Correct output"],
    },
    {
        "id": "07",
        "title": "Dictionaries — Store API-Like Data",
        "goal": "Store values using key/value pairs.",
        "notes": "Dictionaries look like simple JSON objects. This is very important for API automation because response.json() commonly gives you dictionary-like data.",
        "mental": '{"status": 200} means key status has value 200.',
        "example": 'response = {"status": 200, "result": "PASS"}\nprint(response["status"])\nprint(response["result"])',
        "practice_prompt": "Create user with name Sam and role QA. Print the role.",
        "practice_start": 'user = {"name": "Sam", "role": "QA"}\nprint(user["role"])',
        "practice_expected": "QA",
        "hint": 'Use user["role"] to read the value for the role key.',
        "assignment": "Create response with id = 2, name = Alex, active = True. Print id, name and active.",
        "assignment_start": '# Create the response dictionary\n',
        "assignment_expected": ["2", "Alex", "True"],
        "rubric": ["Creates dictionary", "Correct keys and values", "Reads keys correctly", "Correct output"],
    },
    {
        "id": "08",
        "title": "if / else — Decide PASS or FAIL",
        "goal": "Run different code depending on a condition.",
        "notes": "if/else is the foundation of test decisions. If the expected and actual values match, we can mark PASS; otherwise FAIL.",
        "mental": "IF condition is True → do this. ELSE → do something different.",
        "example": 'status_code = 200\nif status_code == 200:\n    print("PASS")\nelse:\n    print("FAIL")',
        "practice_prompt": "Set status_code to 404. Print PASS only for 200, otherwise print FAIL.",
        "practice_start": 'status_code = 404\nif status_code == 200:\n    print("PASS")\nelse:\n    print("FAIL")',
        "practice_expected": "FAIL",
        "hint": "Remember the colon : and indentation under if and else.",
        "assignment": "Set expected = 201 and actual = 201. Print PASS if they match, otherwise FAIL.",
        "assignment_start": '# Add your if/else validation\n',
        "assignment_expected": ["PASS"],
        "rubric": ["Correct expected/actual values", "Correct == comparison", "Correct if/else", "Correct indentation"],
    },
    {
        "id": "09",
        "title": "for Loops — Run Through Test Data",
        "goal": "Repeat work for every item in a collection.",
        "notes": "A for loop is useful when the same test logic must run for many inputs, users, browsers or endpoints.",
        "mental": "for test in tests means: take each item from tests one at a time.",
        "example": 'tests = ["Login", "Search", "Checkout"]\nfor test in tests:\n    print(test)',
        "practice_prompt": "Loop through [200, 201, 204] and print each status code.",
        "practice_start": 'codes = [200, 201, 204]\nfor code in codes:\n    print(code)',
        "practice_expected": "200\n201\n204",
        "hint": "Use for item in list: and indent the print statement.",
        "assignment": "Create results = [PASS, PASS, FAIL]. Use a for loop to print each result.",
        "assignment_start": '# Loop through the results\n',
        "assignment_expected": ["PASS", "PASS", "FAIL"],
        "rubric": ["Correct list", "Uses for loop", "Prints each item", "Correct indentation"],
    },
    {
        "id": "10",
        "title": "while Loops — Repeat Until a Condition Changes",
        "goal": "Repeat code while a condition remains true.",
        "notes": "while loops repeat until their condition becomes False. They must update something inside the loop or they can run forever.",
        "mental": "while attempt < 3 means keep going while attempt is 0, 1 or 2.",
        "example": 'attempt = 1\nwhile attempt <= 3:\n    print(attempt)\n    attempt = attempt + 1',
        "practice_prompt": "Use a while loop to print 1, 2, 3.",
        "practice_start": 'count = 1\nwhile count <= 3:\n    print(count)\n    count = count + 1',
        "practice_expected": "1\n2\n3",
        "hint": "Increase the counter inside the loop so it eventually stops.",
        "assignment": "Create retry = 1. While retry <= 2, print Retry followed by the number, then increase retry.",
        "assignment_start": '# Write the retry loop\n',
        "assignment_expected": ["Retry 1", "Retry 2"],
        "rubric": ["Correct initial counter", "Correct while condition", "Updates counter", "Stops correctly"],
    },
    {
        "id": "11",
        "title": "Functions — Build Reusable QA Logic",
        "goal": "Put reusable validation logic into a named function.",
        "notes": "Functions prevent duplicate code. API automation frameworks use functions for requests, validation, setup and reusable helpers.",
        "mental": "A function is a small reusable machine: give it inputs → it gives you a result.",
        "example": 'def validate_status(actual, expected):\n    if actual == expected:\n        return "PASS"\n    return "FAIL"\n\nprint(validate_status(200, 200))',
        "practice_prompt": "Create add(a, b) that returns a + b. Print add(2, 3).",
        "practice_start": 'def add(a, b):\n    return a + b\n\nprint(add(2, 3))',
        "practice_expected": "5",
        "hint": "Use def name(parameters): and return the result.",
        "assignment": "Create validate_status(actual, expected). Return PASS when values match and FAIL otherwise. Print the result for (200, 200) and (404, 200).",
        "assignment_start": '# Build validate_status()\n',
        "assignment_expected": ["PASS", "FAIL"],
        "rubric": ["Defines function with two parameters", "Correct comparison", "Returns PASS/FAIL", "Tests both matching and non-matching values"],
    },
    {
        "id": "12",
        "title": "Final Mini Project — QA Result Evaluator",
        "goal": "Combine variables, lists, loops, conditions and functions.",
        "notes": "This mini project connects the Python basics you need before API automation. You will evaluate several status codes and print PASS or FAIL for each one.",
        "mental": "This is the bridge from Python basics to automated API assertions.",
        "example": 'def validate(actual, expected):\n    return "PASS" if actual == expected else "FAIL"\n\ncodes = [200, 404, 200]\nfor code in codes:\n    print(code, validate(code, 200))',
        "practice_prompt": "Run the example and explain which status code fails.",
        "practice_start": 'def validate(actual, expected):\n    return "PASS" if actual == expected else "FAIL"\n\ncodes = [200, 404, 200]\nfor code in codes:\n    print(code, validate(code, 200))',
        "practice_expected": "200 PASS\n404 FAIL\n200 PASS",
        "hint": "The expected code is 200, so any other code should fail.",
        "assignment": "Create validate_status(actual, expected). Use it to evaluate [200, 201, 500] against expected 200. Print each code and PASS/FAIL. Then print Total tests: 3.",
        "assignment_start": '# Final Python QA mini project\n',
        "assignment_expected": ["200 PASS", "201 FAIL", "500 FAIL", "Total tests: 3"],
        "rubric": ["Reusable validation function", "Loops over all codes", "Correct PASS/FAIL decisions", "Prints total test count"],
    },
]

# ---------------- Safe beginner runner ----------------
ALLOWED_BUILTINS = {
    "print": print,
    "len": len,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "range": range,
    "type": type,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
}

BLOCKED_AST = (
    ast.Import,
    ast.ImportFrom,
    ast.ClassDef,
    ast.Lambda,
    ast.With,
    ast.AsyncWith,
    ast.AsyncFunctionDef,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
    ast.Global,
    ast.Nonlocal,
    ast.Delete,
)

BLOCKED_NAMES = {"eval", "exec", "open", "compile", "__import__", "globals", "locals", "vars", "input", "help", "dir", "getattr", "setattr", "delattr", "breakpoint"}


def validate_beginner_code(code: str):
    if len(code) > 5000:
        return False, "Code is too long for this beginner practice area."
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return False, f"Syntax error on line {exc.lineno}: {exc.msg}"

    for node in ast.walk(tree):
        if isinstance(node, BLOCKED_AST):
            return False, f"{type(node).__name__} is not needed in this beginner course."
        if isinstance(node, ast.Name) and (node.id.startswith("__") or node.id in BLOCKED_NAMES):
            return False, f"'{node.id}' is not allowed in the practice runner."
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return False, "Special Python attributes are not allowed in the practice runner."
    return True, ""


def run_beginner_code(code: str):
    ok, message = validate_beginner_code(code)
    if not ok:
        return False, message

    output = io.StringIO()
    env = {"__builtins__": ALLOWED_BUILTINS}
    try:
        with contextlib.redirect_stdout(output):
            exec(compile(code, "<student_code>", "exec"), env, env)
        text = output.getvalue().rstrip()
        if len(text) > 4000:
            text = text[:4000] + "\n... output shortened ..."
        return True, text or "(No output — your code ran successfully.)"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def normalize(text):
    return "\n".join(line.rstrip() for line in str(text).strip().splitlines())


def practice_feedback(actual, expected):
    if normalize(actual) == normalize(expected):
        return True, "Perfect — your output matches the expected result."
    return False, "Your code ran, but the output is different from the expected result. Compare the two outputs and try again."


def local_assignment_score(module, code, output, ran_ok):
    if not ran_ok:
        return 25, ["Code does not run yet."], ["Fix the runtime or syntax error first."]
    expected = [str(x).lower() for x in module["assignment_expected"]]
    out = str(output).lower()
    hits = sum(1 for item in expected if item.lower() in out)
    output_score = round((hits / max(len(expected), 1)) * 55)
    structure_score = 0
    ok, _ = validate_beginner_code(code)
    if ok:
        structure_score += 15
    if len(code.strip().splitlines()) >= 2:
        structure_score += 10
    if "#" in code:
        structure_score += 5
    score = min(100, output_score + structure_score + 15)
    strengths = []
    improvements = []
    if hits == len(expected):
        strengths.append("Your output covers the required assignment results.")
    else:
        improvements.append("Some required output is missing or different.")
    if ok:
        strengths.append("Your code uses beginner-safe Python syntax.")
    return score, strengths, improvements


def ai_grade(module, code, output):
    key = st.secrets.get("OPENAI_API_KEY")
    if not key:
        score, strengths, improvements = local_assignment_score(module, code, output, True)
        return {
            "score": score,
            "result": "PASS" if score >= PASS_SCORE else "KEEP PRACTICING",
            "strengths": strengths,
            "improvements": improvements,
            "feedback": "Local evaluator used because OPENAI_API_KEY is not configured.",
        }

    prompt = f"""
You are a patient Python instructor grading a beginner QA automation student.
Grade ONLY the assignment below. Do not reward unrelated advanced code.
Be encouraging but accurate.

MODULE: {module['title']}
LEARNING GOAL: {module['goal']}
ASSIGNMENT: {module['assignment']}
RUBRIC: {json.dumps(module['rubric'])}
EXPECTED OUTPUT IDEAS: {json.dumps(module['assignment_expected'])}

STUDENT CODE:
{code}

ACTUAL OUTPUT:
{output}

Return ONLY valid JSON with this exact structure:
{{
  "score": 0-100 integer,
  "result": "PASS" or "KEEP PRACTICING",
  "strengths": ["short point", "short point"],
  "improvements": ["short point", "short point"],
  "feedback": "2-4 sentence beginner-friendly explanation"
}}
A score of 70 or more is PASS.
""".strip()

    client = OpenAI(api_key=key)
    response = client.responses.create(model=MODEL, input=prompt)
    raw = response.output_text.strip()
    raw = raw.removeprefix("```json").removesuffix("```").strip()
    try:
        data = json.loads(raw)
        data["score"] = max(0, min(100, int(data.get("score", 0))))
        data["result"] = "PASS" if data["score"] >= PASS_SCORE else "KEEP PRACTICING"
        return data
    except Exception:
        score, strengths, improvements = local_assignment_score(module, code, output, True)
        return {
            "score": score,
            "result": "PASS" if score >= PASS_SCORE else "KEEP PRACTICING",
            "strengths": strengths,
            "improvements": improvements,
            "feedback": "The AI response could not be parsed, so the local evaluator provided the score.",
        }

# ---------------- State ----------------
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "completed" not in st.session_state:
    st.session_state.completed = {}
if "assignment_results" not in st.session_state:
    st.session_state.assignment_results = {}

# ---------------- Header ----------------
st.markdown(
    f"""
    <div class="hero">
      <div class="hero-title">🐍 Python QA Academy</div>
      <div class="hero-copy">Learn Python from print() to reusable functions — with QA examples, live practice, assignments and AI evaluation.</div>
      <div class="chip-row"><span class="chip">Beginner friendly</span><span class="chip">▶ Run code</span><span class="chip">🧪 QA examples</span><span class="chip">🤖 AI feedback</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 🎓 Student")
    st.session_state.student_name = st.text_input("Name", value=st.session_state.student_name)
    st.session_state.student_id = st.text_input("Student ID / Email", value=st.session_state.student_id)
    st.divider()
    st.markdown("### 📚 Learning Path")
    module_labels = [f"{m['id']}. {m['title'].split(' — ')[0]}" for m in MODULES]
    selected_label = st.radio("Choose module", module_labels, label_visibility="collapsed")
    selected_index = module_labels.index(selected_label)
    done = sum(1 for m in MODULES if st.session_state.completed.get(m["id"]))
    st.progress(done / len(MODULES), text=f"Progress: {done}/{len(MODULES)} modules passed")

module = MODULES[selected_index]

# Top progress metrics
m1, m2, m3 = st.columns(3)
m1.metric("Current Module", f"{module['id']} / {len(MODULES):02d}")
m2.metric("Modules Passed", sum(1 for v in st.session_state.completed.values() if v))
best = max([r.get("score", 0) for r in st.session_state.assignment_results.values()] or [0])
m3.metric("Best Assignment Score", f"{best}%")

st.markdown(f'<div class="kicker">Module {module["id"]}</div><div class="title">{module["title"]}</div><div class="copy">Goal: {module["goal"]}</div>', unsafe_allow_html=True)

learn_tab, practice_tab, assignment_tab, progress_tab = st.tabs(["📘 Learn", "🧪 Practice", "📝 Assignment", "📊 Progress"])

with learn_tab:
    st.markdown("### Easy notes")
    st.markdown(f'<div class="note">{module["notes"]}</div>', unsafe_allow_html=True)
    st.markdown("### Think about it this way")
    st.markdown(f'<div class="mental">💡 {module["mental"]}</div>', unsafe_allow_html=True)
    st.markdown("### Working example")
    st.code(module["example"], language="python")
    ok, example_output = run_beginner_code(module["example"])
    if ok:
        st.caption("Example output")
        st.markdown(f'<div class="console">{example_output}</div>', unsafe_allow_html=True)
    st.info("Next: open **🧪 Practice**, edit the code and run it yourself.")

with practice_tab:
    st.markdown("### Practice it yourself")
    st.write(module["practice_prompt"])
    practice_key = f"practice_code_{module['id']}"
    if practice_key not in st.session_state:
        st.session_state[practice_key] = module["practice_start"]
    practice_code = st.text_area("Your practice code", key=practice_key, height=190)
    c1, c2 = st.columns([1, 1])
    run_practice = c1.button("▶ Run Practice", type="primary", use_container_width=True, key=f"runp_{module['id']}")
    show_hint = c2.button("💡 Show Hint", use_container_width=True, key=f"hint_{module['id']}")
    if show_hint:
        st.info(module["hint"])
    if run_practice:
        ok, result = run_beginner_code(practice_code)
        st.markdown("#### Your result")
        st.markdown(f'<div class="console">{result}</div>', unsafe_allow_html=True)
        if ok:
            matched, feedback = practice_feedback(result, module["practice_expected"])
            if matched:
                st.success("✅ " + feedback)
            else:
                st.warning("🟡 " + feedback)
                with st.expander("Compare with expected output"):
                    st.code(module["practice_expected"], language="text")
        else:
            st.error("❌ Your code did not run. Read the error, adjust the code, and try again.")

with assignment_tab:
    st.markdown("### Assignment")
    st.write(module["assignment"])
    with st.expander("What will be evaluated?"):
        for item in module["rubric"]:
            st.write("• " + item)
    assignment_key = f"assignment_code_{module['id']}"
    if assignment_key not in st.session_state:
        st.session_state[assignment_key] = module["assignment_start"]
    assignment_code = st.text_area("Your assignment code", key=assignment_key, height=230)
    a1, a2 = st.columns(2)
    run_assignment = a1.button("▶ Run Assignment", type="primary", use_container_width=True, key=f"runa_{module['id']}")
    evaluate = a2.button("🤖 Evaluate Assignment", use_container_width=True, key=f"eval_{module['id']}")

    output_key = f"assignment_output_{module['id']}"
    ok_key = f"assignment_ok_{module['id']}"
    if run_assignment:
        ok, result = run_beginner_code(assignment_code)
        st.session_state[output_key] = result
        st.session_state[ok_key] = ok

    if output_key in st.session_state:
        st.markdown("#### Assignment output")
        st.markdown(f'<div class="console">{st.session_state[output_key]}</div>', unsafe_allow_html=True)
        if not st.session_state.get(ok_key, False):
            st.error("Fix the code error before requesting evaluation.")

    if evaluate:
        if not st.session_state.student_name.strip():
            st.error("Enter your name in the sidebar before evaluation.")
        else:
            ok, result = run_beginner_code(assignment_code)
            st.session_state[output_key] = result
            st.session_state[ok_key] = ok
            if not ok:
                evaluation = {
                    "score": 20,
                    "result": "KEEP PRACTICING",
                    "strengths": ["You attempted the assignment."],
                    "improvements": ["Fix the code so it runs before focusing on the final result."],
                    "feedback": f"Your current code returns: {result}",
                }
            else:
                with st.spinner("Instructor agent is reviewing your code and result..."):
                    evaluation = ai_grade(module, assignment_code, result)
            st.session_state.assignment_results[module["id"]] = {
                **evaluation,
                "module": module["title"],
                "code": assignment_code,
                "output": result,
                "evaluated_at": datetime.now().isoformat(timespec="seconds"),
            }
            if evaluation["score"] >= PASS_SCORE:
                st.session_state.completed[module["id"]] = True
            st.rerun()

    saved = st.session_state.assignment_results.get(module["id"])
    if saved:
        st.divider()
        st.markdown("### Instructor evaluation")
        e1, e2 = st.columns(2)
        e1.metric("Score", f"{saved['score']}%")
        e2.metric("Result", saved["result"])
        if saved["score"] >= PASS_SCORE:
            st.success("✅ Module passed")
        else:
            st.warning("Keep practicing, then evaluate again.")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Strengths**")
            for item in saved.get("strengths", []):
                st.write("✅ " + item)
        with col2:
            st.markdown("**Improve next**")
            for item in saved.get("improvements", []):
                st.write("➡️ " + item)
        st.info(saved.get("feedback", ""))

with progress_tab:
    st.markdown("### Your course progress")
    rows = []
    for m in MODULES:
        result = st.session_state.assignment_results.get(m["id"], {})
        rows.append({
            "Module": f"{m['id']} — {m['title']}",
            "Score": result.get("score", "—"),
            "Status": "PASS" if st.session_state.completed.get(m["id"]) else ("Attempted" if result else "Not started"),
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)
    report = {
        "student_name": st.session_state.student_name,
        "student_id": st.session_state.student_id,
        "modules_passed": sum(1 for v in st.session_state.completed.values() if v),
        "total_modules": len(MODULES),
        "assignment_results": st.session_state.assignment_results,
    }
    st.download_button(
        "↓ Download Progress Report",
        json.dumps(report, indent=2).encode(),
        f"{st.session_state.student_name or 'student'}_python_qa_progress.json",
        "application/json",
        use_container_width=True,
    )

st.caption("Practice runner is intentionally restricted to beginner Python features. Course progress is stored only in the current Streamlit session unless you download the report.")
