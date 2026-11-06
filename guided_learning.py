"""Guided, small-step learning flow for Python QA Academy."""
import streamlit as st
from collections import Counter

def steps_for(m):
    example_name, example_code, example_explanation = m["examples"][0]
    return [
        {"title":"Understand the idea","kind":"read","text":m["overview"],"example":m["syntax"],"tip":m["mental"]},
        {"title":"See a real example","kind":"read","text":example_explanation,"example":example_code,"tip":"Read the code line by line and predict the output."},
        {"title":"Check your understanding","kind":"quiz","text":m["quiz"][0],"choices":m["quiz"][1],"answer":m["quiz"][2],"tip":"Revisit the syntax and examples if needed."},
        {"title":"Write your first code","kind":"code","text":m["practice"],"starter":m["start"],"expected":m["expected"],"solution":m["start"],"tip":m["hint"]},
        {"title":"Experiment and debug","kind":"code","text":"Run this working example, then change one value. Explain how the output changes.","starter":m["examples"][-1][1],"expected":None,"solution":m["examples"][-1][1],"tip":"Try running the original example first. A successful run passes this exploratory step."},
        {"title":"Apply your learning","kind":"code","text":m["assignment"],"starter":m["a_start"],"expected":m["a_expected"],"solution":None,"tip":"Check the assignment rubric. You can open the complete reference solution in the Assignment tab."},
    ]

def render_guided(m, run_code, full_solution):
    mid=m["id"]
    steps=steps_for(m)
    index_key=f"guided_index_{mid}"
    done_key=f"guided_done_{mid}"
    st.session_state.setdefault(index_key,0)
    st.session_state.setdefault(done_key,[])
    idx=min(st.session_state[index_key],len(steps)-1)
    step=steps[idx]
    st.markdown("### Interactive Python learning path")
    st.progress(len(st.session_state[done_key])/len(steps),text=f"{len(st.session_state[done_key])} of {len(steps)} steps completed")
    st.caption(f"Step {idx+1} of {len(steps)} · {step['title']}")
    st.subheader(step["title"])
    st.write(step["text"])
    passed=idx in st.session_state[done_key]
    if step["kind"]=="read":
        st.code(step["example"],language="python")
        st.info(step["tip"])
        if st.button("✓ I understand — complete step",key=f"guided_read_{mid}_{idx}"):
            st.session_state[done_key]=sorted(set(st.session_state[done_key]+[idx]))
            st.rerun()
    elif step["kind"]=="quiz":
        selection=st.radio("Choose one answer",step["choices"],index=None,key=f"guided_quiz_{mid}_{idx}")
        if st.button("Check answer",key=f"guided_quiz_check_{mid}_{idx}"):
            if selection==step["answer"]:
                st.session_state[done_key]=sorted(set(st.session_state[done_key]+[idx]))
                st.success("Correct! You can continue.")
            else:
                st.error("Not quite. Try again and compare with the lesson.")
                st.info(step["tip"])
    else:
        code_key=f"guided_code_{mid}_{idx}"
        st.session_state.setdefault(code_key,step["starter"])
        code=st.text_area("Your Python code",key=code_key,height=220)
        with st.expander("💡 Hint"):
            st.info(step["tip"])
        with st.expander("📋 Full working solution — copy and paste"):
            st.code(full_solution(m) if idx==5 else step["solution"],language="python")
        if st.button("▶ Run and check code",type="primary",key=f"guided_run_{mid}_{idx}"):
            ok,out=run_code(code)
            st.code(out,language="text")
            if not ok:
                st.error("Code error. Read the message above, fix it and try again.")
            else:
                expected=step["expected"]
                if expected is None:
                    correct=True
                elif isinstance(expected,list):
                    correct=all(Counter(line.strip().casefold() for line in out.splitlines())[value.strip().casefold()] >= count for value,count in Counter(str(v).strip().casefold() for v in expected).items())
                else:
                    correct=out.strip()==str(expected).strip()
                if correct:
                    st.session_state[done_key]=sorted(set(st.session_state[done_key]+[idx]))
                    st.success("PASS — great work! You can continue.")
                else:
                    st.error("Your code ran, but the result does not match the exercise.")
                    st.caption("Check the expected result and try again.")
                    st.code("\n".join(expected) if isinstance(expected,list) else str(expected),language="text")
    if passed:
        st.success("Step completed ✓")
    back,next_col=st.columns(2)
    if back.button("← Previous",disabled=idx==0,key=f"guided_back_{mid}"):
        st.session_state[index_key]=idx-1
        st.rerun()
    if next_col.button("Next →",disabled=(idx==len(steps)-1 or idx not in st.session_state[done_key]),key=f"guided_next_{mid}"):
        st.session_state[index_key]=idx+1
        st.rerun()
    if len(st.session_state[done_key])==len(steps):
        st.success("🎉 All guided steps completed! Open Assignment for instructor evaluation.")
