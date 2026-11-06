"""Exercise Streamlit widgets across all chapters without launching a browser."""
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

class StreamlitSmokeTests(unittest.TestCase):
    def test_home_and_every_chapter_renders(self):
        app=AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"),default_timeout=20).run()
        self.assertFalse(app.exception, [str(x.message) for x in app.exception])
        self.assertEqual(len(app.sidebar.radio),1)
        labels=app.sidebar.radio[0].options
        self.assertEqual(len(labels),12)
        for label in labels:
            with self.subTest(chapter=label):
                app.sidebar.radio[0].set_value(label).run()
                self.assertFalse(app.exception,[str(x.message) for x in app.exception])
                self.assertGreater(len(app.tabs),0)
                self.assertGreater(len(app.get("button")),0)

if __name__=="__main__":
    unittest.main()
