import os
import re
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)

MODEL = "claude-sonnet-5"

SYSTEM_PROMPT = """You are a senior QA engineer generating a regression test suite.

Given a user story and its acceptance criteria, produce a structured, prioritized set of test scenarios covering:
- Positive (happy-path) cases
- Negative cases (invalid input, failure conditions)
- Edge cases (boundary conditions, timing, unusual-but-valid states)

For each test case include exactly these fields:
- id: sequential, formatted TC_001, TC_002, ...
- scenario: one clear sentence describing what is being verified
- type: one of "Positive", "Negative", "Edge"
- precondition: the state required before the test can run
- priority: one of "High", "Medium", "Low"
- expected_result: what should happen

Generate between 5 and 10 test cases depending on how much the acceptance criteria supports.

Respond with ONLY a JSON array of objects with exactly these keys: id, scenario, type, precondition, priority, expected_result. No prose, no markdown code fences, no commentary before or after — JSON only."""


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    client = get_client()
    if client is None:
        return jsonify({
            "error": "ANTHROPIC_API_KEY is not set. Copy .env.example to .env, add your key, and restart the server."
        }), 500

    payload = request.get_json(silent=True) or {}
    user_story = (payload.get("user_story") or "").strip()
    acceptance_criteria = (payload.get("acceptance_criteria") or "").strip()

    if not user_story or not acceptance_criteria:
        return jsonify({"error": "user_story and acceptance_criteria are both required."}), 400

    user_message = f"User Story:\n{user_story}\n\nAcceptance Criteria:\n{acceptance_criteria}"

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        raw_text = "".join(block.text for block in response.content if block.type == "text")
        test_cases = parse_test_cases(raw_text)
        return jsonify({"test_cases": test_cases})
    except anthropic.APIStatusError as e:
        return jsonify({"error": f"Claude API error: {e.message}"}), 502
    except (json.JSONDecodeError, ValueError):
        return jsonify({"error": "Claude's response wasn't valid JSON. Try again."}), 502
    except Exception as e:
        return jsonify({"error": f"Could not generate test suite: {str(e)}"}), 500


def parse_test_cases(raw_text: str):
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    data = json.loads(cleaned)
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array")
    return data


if __name__ == "__main__":
    app.run(debug=True, port=5000)
