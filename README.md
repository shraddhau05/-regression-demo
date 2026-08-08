# -regression-demo
=======
# Regression Test Suite Generator — Local Demo

A small local app that turns a user story + acceptance criteria into a structured, prioritized regression test suite, generated live by Claude. Matches the "Requirements → Regression Test Suite" flow: paste input on the left, Claude processes it, structured output table appears on the right.

## Setup

1. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Add your API key:**
   ```
   cp .env.example .env
   ```
   Open `.env` and paste your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
   Get a key at [console.anthropic.com](https://console.anthropic.com) → API Keys.
   `.env` is already in `.gitignore` — never commit it or paste the key anywhere public.

4. **Run it:**
   ```
   python app.py
   ```

5. Open **http://localhost:5000** in your browser.

## Using it

A sample password-reset story is pre-filled as placeholder text — type your own or use it as-is. Click **Generate Test Suite** and Claude returns 5–10 prioritized scenarios (Positive / Negative / Edge) with preconditions and expected results, rendered as a table.

## For your LinkedIn demo

- Screen-record the flow end to end: paste a real user story from one of your projects → click Generate → let the table populate live. The spinning connector icon speeds up while the request is in flight, so it visibly reads as "processing."
- Try 2–3 different stories (e.g. password reset, OTP verification, fund transfer) to show range.
- Worth calling out in the post: this is a live call to the Anthropic API, not a static mockup — the badges and priorities are model-generated per input, not hardcoded.

## Project structure

```
app.py                Flask backend + Claude API call
templates/index.html  Page markup
static/style.css      Styling
static/script.js      Frontend logic
requirements.txt      Python dependencies
.env.example           Template for your API key — copy to .env
.gitignore             Keeps .env and venv/ out of version control
```

## VS Code Copilot Chat agent

This workspace includes a custom Copilot Chat agent definition at `.github/agents/regression-suite.agent.md`.

To use it in VS Code:

1. Open Copilot Chat.
2. Open the agent dropdown in the left corner.
3. Select `Regression Suite Agent`.

If the agent does not appear immediately, reload VS Code or restart the Copilot Chat session.
## Push to GitHub

If this workspace is not yet a Git repository, run:

```bash
git init
git add .
git commit -m "Initial project files"
```

Then add your GitHub repo and push:

```bash
git branch -M main
git remote add origin https://github.com/shraddhau05/-regression-demo.git
git push -u origin main
```

If you already have the repo initialized, just stage and commit your changes:

```bash
git add .
git commit -m "Update regression suite demo and custom agent"
git push
```

Use a GitHub PAT or SSH key if prompted for authentication.
>>>>>>> 04eb0cd (Update regression suite demo and custom agent)
