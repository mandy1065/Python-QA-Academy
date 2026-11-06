"""Additional beginner lessons with executable practice for Python QA."""
LESSONS = {
"01": [
("Print your first message", "Python uses print() to show text. Text belongs inside quotes. Try changing the message.", 'print("Hello, QA student!")', ["Hello, QA student!"]),
("Print two messages", "Each print call creates a new output line. This is useful when reporting test results.", 'print("Starting test")\nprint("Test finished")', ["Starting test", "Test finished"]),
],
"02": [
("Create a text variable", "A variable gives a value a reusable name. The equals sign assigns the value. Use quotation marks for text.", 'browser = "Chrome"\nprint(browser)', ["Chrome"]),
("Change a variable", "Assignment replaces the old value. This is useful when a test status changes.", 'status = "FAIL"\nstatus = "PASS"\nprint(status)', ["PASS"]),
("Use meaningful names", "Use lowercase letters and underscores. Names like test_status are easier to understand than x.", 'test_status = "PASS"\nprint(test_status)', ["PASS"]),
("Store a number", "Numbers do not need quotation marks. An integer is a whole number.", 'total_tests = 5\nprint(total_tests)', ["5"]),
("Store two names", "A string is text. Create first_name and last_name and print each on a separate line.", 'first_name = "John"\nlast_name = "Doe"\nprint(first_name)\nprint(last_name)', ["John", "Doe"]),
],
"03": [
("Identify a string", "Strings store text and need quotes. Print the value to inspect it.", 'status = "PASS"\nprint(status)', ["PASS"]),
("Use an integer", "Integers store whole numbers, such as the number of tests.", 'tests = 12\nprint(tests)', ["12"]),
("Use a float", "Floats store decimals, such as response times.", 'seconds = 1.5\nprint(seconds)', ["1.5"]),
("Use a Boolean", "Booleans are True or False, useful for validation.", 'passed = True\nprint(passed)', ["True"]),
],
"04": [
("Combine strings", "The plus operator joins strings. Add a space so words do not run together.", 'first = "API"\nsecond = "QA"\nprint(first + " " + second)', ["API QA"]),
("Uppercase text", "The upper method converts lowercase letters to uppercase.", 'status = "pass"\nprint(status.upper())', ["PASS"]),
],
"05": [
("Compare equality", "Use == to compare values; = is for assignment.", 'print(200 == 200)', ["True"]),
("Compare durations", "Use > to ask whether one number is greater than another.", 'print(5 > 2)', ["True"]),
],
"06": [
("Read the first item", "List indexes start at zero, so [0] selects the first item.", 'tests = ["Login", "Search"]\nprint(tests[0])', ["Login"]),
("Count list items", "len() returns the number of items in a list.", 'tests = ["Login", "Search", "Checkout"]\nprint(len(tests))', ["3"]),
],
"07": [
("Read a dictionary field", "Dictionaries store key-value pairs. Access a value using its key.", 'response = {"status": 200}\nprint(response["status"])', ["200"]),
("Update a dictionary", "Assign to a key to add or change a field.", 'result = {"test": "Login"}\nresult["status"] = "PASS"\nprint(result["status"])', ["PASS"]),
],
"08": [
("Test the success case", "if runs a block when a condition is true. Indentation matters.", 'status = 200\nif status == 200:\n    print("PASS")\nelse:\n    print("FAIL")', ["PASS"]),
("Test the failure case", "else handles the alternative when the condition is false.", 'status = 500\nif status == 200:\n    print("PASS")\nelse:\n    print("FAIL")', ["FAIL"]),
],
"09": [
("Loop over test names", "A for loop repeats code for each item in a list.", 'for test in ["Login", "Search"]:\n    print(test)', ["Login", "Search"]),
("Use range", "range(1, 4) produces 1, 2, 3, excluding the endpoint.", 'for number in range(1, 4):\n    print(number)', ["1", "2", "3"]),
],
"10": [
("Retry twice", "A while loop repeats while its condition is true. Update the counter to avoid an infinite loop.", 'attempt = 1\nwhile attempt <= 2:\n    print(attempt)\n    attempt += 1', ["1", "2"]),
("Finish retrying", "The loop ends when the condition becomes false.", 'attempt = 0\nwhile attempt < 3:\n    attempt += 1\nprint("Done")', ["Done"]),
],
"11": [
("Write a function", "A function groups reusable instructions. Call the function to run it.", 'def greet():\n    print("Hello QA")\ngreet()', ["Hello QA"]),
("Return a result", "return gives a value back to the caller.", 'def check(code):\n    return code == 200\nprint(check(200))', ["True"]),
],
"12": [
("Count passing tests", "Combine a list, a loop and a counter to summarize a test run.", 'codes = [200, 500, 200]\npassed = 0\nfor code in codes:\n    if code == 200:\n        passed += 1\nprint(passed)', ["2"]),
("Report each result", "Use conditional logic inside a loop to report PASS or FAIL.", 'for code in [200, 404]:\n    print("PASS" if code == 200 else "FAIL")', ["PASS", "FAIL"]),
],
}

def expanded_steps(module):
    result = []
    for title, explanation, solution, expected in LESSONS[module["id"]]:
        result.append({
            "title": title,
            "type": "code",
            "explanation": explanation + " First study the example, then reproduce it in the editor without copying. Run tests and compare the output.",
            "starter": "# Write your solution below\n",
            "solution": solution,
            "expected": expected,
            "hint": "Use the example shown in the full solution. Notice the punctuation, quotes, and indentation.",
        })
    return result
