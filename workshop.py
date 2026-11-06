"""Structured, beginner-friendly Python QA workshop with 10 interactive steps per chapter."""
from collections import Counter
import streamlit as st

def workshop_steps(m):
    examples=m["examples"]
    steps=[
        {"title":"Understand the concept","type":"read","explanation":m["overview"],"code":m["syntax"],"hint":m["mental"]},
        {"title":"Why QA engineers need it","type":"read","explanation":"In real software testing, this Python concept helps you: "+". ".join(m["qa_use"])+".","code":examples[0][1],"hint":examples[0][2]},
        {"title":"Read and predict","type":"read","explanation":examples[0][2]+" Study each line and predict the result before running it.","code":examples[0][1],"hint":"Read the code from top to bottom."},
        {"title":"Check your understanding","type":"quiz","explanation":m["quiz"][0],"options":m["quiz"][1],"answer":m["quiz"][2],"hint":m["mental"]},
        {"title":"Practice with guidance","type":"code","explanation":m["practice"],"starter":m["start"],"solution":m["start"],"expected":m["expected"],"hint":m["hint"]},
        {"title":"Study a second example","type":"read","explanation":examples[1][2] if len(examples)>1 else examples[0][2],"code":examples[1][1] if len(examples)>1 else examples[0][1],"hint":"Try explaining the code aloud."},
        {"title":"Modify and experiment","type":"code","explanation":"Run the example. Then change one input value and run it again. Explain the difference in the console output.","starter":examples[-1][1],"solution":examples[-1][1],"expected":None,"hint":"First run the supplied example; then edit a value."},
        {"title":"Debug a common mistake","type":"read","explanation":"Common mistakes: "+". ".join(m["mistakes"])+". Find one mistake in your own code and explain the correction.","code":examples[0][1],"hint":"Compare capitalization, quotes, brackets and indentation."},
        {"title":"Independent QA challenge","type":"code","explanation":m["assignment"],"starter":m["a_start"],"solution":None,"expected":m["a_expected"],"hint":m["hint"]},
        {"title":"Reflect and finish","type":"read","explanation":"You have practiced "+m["title"]+". Review the rubric: "+". ".join(m["rubric"])+". Open the Assignment tab for a graded submission.","code":examples[-1][1],"hint":"Repeat the independent challenge without opening the solution."}
    ]
    return steps

def output_matches(actual,expected):
    if expected is None:return True
    if isinstance(expected,str):
        return actual.strip()==expected.strip()
    need=Counter(str(v).strip().casefold() for v in expected)
    have=Counter(line.strip().casefold() for line in actual.splitlines())
    return all(have[k]>=v for k,v in need.items())

def render_workshop(m,run_code,full_solution):
    steps=workshop_steps(m)
    mid=m["id"]
    poskey=f"workshop_position_{mid}"
    donekey=f"workshop_completed_{mid}"
    st.session_state.setdefault(poskey,0)
    st.session_state.setdefault(donekey,[])
    pos=min(st.session_state[poskey],len(steps)-1)
    step=steps[pos]
    st.progress(len(st.session_state[donekey])/len(steps),text=f"Chapter {mid}: {len(st.session_state[donekey])}/{len(steps)} steps completed")
    st.caption(f"Step {pos+1} of {len(steps)}")
    st.subheader(step["title"])
    left,right=st.columns([1,1],gap="large")
    with left:
        st.markdown("#### Instructions")
        st.write(step["explanation"])
        if step["type"]=="read":
            st.code(step["code"],language="python")
            st.info(step["hint"])
            if st.button("✓ Mark this lesson complete",key=f"ws_read_{mid}_{pos}"):
                st.session_state[donekey]=sorted(set(st.session_state[donekey]+[pos]))
                st.rerun()
        elif step["type"]=="quiz":
            selected=st.radio("Choose the best answer",step["options"],index=None,key=f"ws_quiz_{mid}_{pos}")
            if st.button("Check answer",key=f"ws_check_{mid}_{pos}"):
                if selected==step["answer"]:
                    st.session_state[donekey]=sorted(set(st.session_state[donekey]+[pos]))
                    st.success("PASS — correct answer.")
                else:
                    st.error("Try again. Read the explanation and check the example.")
        else:
            with st.expander("💡 Hint"):
                st.info(step["hint"])
            with st.expander("📋 Full copyable solution"):
                st.code(full_solution(m) if step["solution"] is None else step["solution"],language="python")
            if step["expected"] is not None:
                with st.expander("Expected output"):
                    st.code("\n".join(map(str,step["expected"])) if isinstance(step["expected"],list) else step["expected"],language="text")
    with right:
        st.markdown("#### main.py")
        if step["type"]=="code":
            key=f"ws_code_{mid}_{pos}"
            st.session_state.setdefault(key,step["starter"])
            code=st.text_area("Python editor",key=key,height=240)
            if st.button("▶ Run tests",type="primary",key=f"ws_run_{mid}_{pos}"):
                ok,out=run_code(code)
                st.markdown("#### Console")
                st.code(out,language="text")
                if not ok:
                    st.error("Python error — read the console, correct the code and retry.")
                elif output_matches(out,step["expected"]):
                    st.session_state[donekey]=sorted(set(st.session_state[donekey]+[pos]))
                    st.success("PASS — step completed.")
                else:
                    st.error("FAIL — output does not match. Check the expected output and retry.")
        else:
            st.code(step.get("code",m["syntax"]),language="python")
            st.caption("Read the instructions and complete the activity on the left.")
    previous,nextcol=st.columns(2)
    if previous.button("← Previous step",disabled=pos==0,key=f"ws_prev_{mid}"):
        st.session_state[poskey]=pos-1
        st.rerun()
    if nextcol.button("Next step →",disabled=(pos==len(steps)-1 or pos not in st.session_state[donekey]),key=f"ws_next_{mid}"):
        st.session_state[poskey]=pos+1
        st.rerun()
    if len(st.session_state[donekey])==len(steps):
        st.success("🎉 Chapter complete! Now submit the graded assignment.")
