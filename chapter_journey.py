"""Chapter journey: theory, examples, exercises, debugging and assessment."""
def build_journey(m):
    from expanded_lessons import expanded_steps
    examples=m["examples"]
    result=[]
    result.append({"title":"Learning objectives and prerequisites","type":"read","explanation":"By the end of this chapter you should be able to: "+m["goal"]+". You will practice concepts using QA automation examples. First review the key ideas: "+"; ".join(m["key_points"])+".","code":m["syntax"],"hint":m["mental"]})
    for i,(name,code,explanation) in enumerate(examples,1):
        result.append({"title":f"Worked example {i}: {name}","type":"read","explanation":explanation+" Read the example from top to bottom, identify the variables and operations, and predict its output before continuing.","code":code,"hint":"Explain each line aloud and run it in the next practice step."})
        result.append({"title":f"Try example {i} yourself","type":"code","explanation":f"Recreate the {name} example in main.py. Run it, then change one input and observe the result. This is guided practice; successful execution completes the step.","starter":"# Recreate the example here\n","solution":code,"expected":None,"hint":explanation})
    result.extend(expanded_steps(m))
    for i,mistake in enumerate(m["mistakes"],1):
        result.append({"title":f"Debugging clinic {i}","type":"read","explanation":"Common mistake: "+mistake+". Read the working example. Describe what error would happen if this rule were broken, then correct the mistake in your own editor.","code":examples[min(i-1,len(examples)-1)][1],"hint":"Compare your punctuation, variable names and indentation with the correct example."})
    result.append({"title":"Knowledge check","type":"quiz","explanation":m["quiz"][0],"options":m["quiz"][1],"answer":m["quiz"][2],"hint":m["mental"]})
    result.append({"title":"Independent chapter challenge","type":"code","explanation":m["assignment"]+" This is a practice submission. For your graded submission, open Final Assignment.","starter":m["a_start"],"solution":None,"expected":m["a_expected"],"hint":m["hint"]})
    result.append({"title":"Review and prepare to submit","type":"read","explanation":"You have completed the chapter journey. Review the assessment criteria: "+"; ".join(m["rubric"])+". Try the final assignment without hints first. Download your submission after evaluation.","code":examples[-1][1],"hint":"If you get stuck, revisit the examples and debugging clinics."})
    return result
