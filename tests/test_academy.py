"""Automated curriculum, solution, and grading smoke tests."""
import ast
import collections
import io
import pathlib
import unittest
from pptx import Presentation

ROOT = pathlib.Path(__file__).resolve().parents[1]
source = (ROOT / "app.py").read_text(encoding="utf-8")
tree = ast.parse(source)
names = {"lesson","full_solution","chapter_slides","validate_code","run_code","norm","local_grade"}
nodes = [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
nodes += [n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ("MODULES","ALLOWED","BLOCKED","BAD") for t in n.targets)]
module=ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[]))
scope={"ast":ast,"io":io,"contextlib":__import__("contextlib"),"sys":__import__("sys"),"Counter":collections.Counter}
exec(compile(module,str(ROOT/"app.py"),"exec"),scope)
from guided_learning import steps_for
from workshop import workshop_steps, output_matches
from chapter_journey import build_journey

class AcademyTests(unittest.TestCase):
    def test_all_chapters_have_content(self):
        modules=scope["MODULES"]
        self.assertEqual(len(modules),12)
        self.assertEqual(len({m["id"] for m in modules}),12)
        for m in modules:
            with self.subTest(module=m["id"]):
                self.assertGreaterEqual(len(m["examples"]),2)
                self.assertTrue(m["assignment"])
                self.assertGreaterEqual(len(m["rubric"]),3)
                self.assertEqual(len(steps_for(m)),6)
                self.assertGreaterEqual(len(workshop_steps(m)),12)
                self.assertGreaterEqual(len(build_journey(m)),12)

    def test_all_solutions_run_and_grade_pass(self):
        for m in scope["MODULES"]:
            with self.subTest(module=m["id"]):
                solution=scope["full_solution"](m)
                ok,out=scope["run_code"](solution)
                self.assertTrue(ok,out)
                result=scope["local_grade"](m,solution,out)
                self.assertEqual(result["result"],"PASS",result)

    def test_workshop_expected_outputs(self):
        for m in scope["MODULES"]:
            with self.subTest(module=m["id"]):
                steps=build_journey(m)
                self.assertGreaterEqual(len(steps),12)
                for step in steps:
                    if step["type"]=="code" and step["solution"] is not None:
                        ok,out=scope["run_code"](step["solution"])
                        self.assertTrue(ok,out)
                        self.assertTrue(output_matches(out,step["expected"]),out)
                self.assertFalse(output_matches("WRONG",m["a_expected"]))

    def test_wrong_code_fails(self):
        for m in scope["MODULES"]:
            with self.subTest(module=m["id"]):
                result=scope["local_grade"](m,'print("WRONG")',"WRONG")
                self.assertNotEqual(result["result"],"PASS")

    def test_powerpoints_open(self):
        for m in scope["MODULES"]:
            with self.subTest(module=m["id"]):
                data=scope["chapter_slides"](m)
                self.assertGreater(len(data),1000)
                deck=Presentation(io.BytesIO(data))
                self.assertGreaterEqual(len(deck.slides),8)

    def test_runner_rejects_bad_syntax_and_infinite_loop(self):
        ok,_=scope["run_code"]("if True print('x')")
        self.assertFalse(ok)
        ok,message=scope["run_code"]("while True:\n    pass")
        self.assertFalse(ok)
        self.assertIn("Too many steps",message)

if __name__=="__main__":
    unittest.main()
