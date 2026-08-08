import unittest

from app import app, parse_test_cases


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_parse_test_cases_strips_code_fences(self):
        raw = '''```json
[
  {
    "id": "TC_001",
    "scenario": "User can reset password",
    "type": "Positive",
    "precondition": "User has a registered email",
    "priority": "High",
    "expected_result": "Password is reset successfully"
  }
]
```'''

        self.assertEqual(parse_test_cases(raw)[0]["id"], "TC_001")

    def test_index_page_includes_learning_section(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"How AI helps QA teams", response.data)


if __name__ == "__main__":
    unittest.main()
