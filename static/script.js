const btn = document.getElementById('generate-btn');
const sampleBtn = document.getElementById('load-sample-btn');
const userStoryEl = document.getElementById('user-story');
const acEl = document.getElementById('acceptance-criteria');
const errorEl = document.getElementById('error-msg');
const emptyEl = document.getElementById('output-empty');
const summaryEl = document.getElementById('output-summary');
const tableWrap = document.getElementById('output-table-wrap');
const tbody = document.getElementById('output-tbody');
const connector = document.getElementById('connector');

const SAMPLE_STORY = 'As a returning customer, I want to update my profile so that I can keep my personal information current.';
const SAMPLE_CRITERIA = '- I can change my name, email, and phone number\n- The system validates the updated information\n- A success message is shown after saving\n- A failure message is shown if validation fails';

const TYPE_CLASS = { Positive: 'badge-pos', Negative: 'badge-neg', Edge: 'badge-edge' };
const PRIORITY_CLASS = { High: 'badge-high', Medium: 'badge-med', Low: 'badge-low' };

sampleBtn.addEventListener('click', () => {
  userStoryEl.value = SAMPLE_STORY;
  acEl.value = SAMPLE_CRITERIA;
  hideError();
  userStoryEl.focus();
});

btn.addEventListener('click', async () => {
  const userStory = userStoryEl.value.trim();
  const acceptanceCriteria = acEl.value.trim();
  hideError();

  if (!userStory || !acceptanceCriteria) {
    showError('Add both a user story and acceptance criteria first.');
    return;
  }

  setLoading(true);

  try {
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_story: userStory, acceptance_criteria: acceptanceCriteria }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Something went wrong.');
    renderTable(data.test_cases);
  } catch (err) {
    showError(err.message);
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  btn.disabled = isLoading;
  btn.textContent = isLoading ? 'Generating…' : 'Generate Test Suite';
  connector.classList.toggle('active', isLoading);
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.hidden = false;
  summaryEl.hidden = true;
  emptyEl.hidden = false;
  tableWrap.hidden = true;
}

function hideError() {
  errorEl.hidden = true;
}

function renderTable(cases) {
  tbody.innerHTML = '';
  const normalizedCases = Array.isArray(cases) ? cases : [];
  normalizedCases.forEach((tc) => {
    const tr = document.createElement('tr');

    tr.appendChild(cell(tc.id, 'mono'));
    tr.appendChild(cell(tc.scenario));
    tr.appendChild(badgeCell(tc.type, TYPE_CLASS));
    tr.appendChild(cell(tc.precondition));
    tr.appendChild(badgeCell(tc.priority, PRIORITY_CLASS));
    tr.appendChild(cell(tc.expected_result));

    tbody.appendChild(tr);
  });
  emptyEl.hidden = true;
  summaryEl.hidden = false;
  summaryEl.textContent = `Generated ${normalizedCases.length} regression scenario${normalizedCases.length === 1 ? '' : 's'} for review.`;
  tableWrap.hidden = false;
}

function cell(text, className) {
  const td = document.createElement('td');
  if (className) td.className = className;
  td.textContent = text ?? '';
  return td;
}

function badgeCell(text, classMap) {
  const td = document.createElement('td');
  const span = document.createElement('span');
  span.className = `badge ${classMap[text] || ''}`;
  span.textContent = text ?? '';
  td.appendChild(span);
  return td;
}
