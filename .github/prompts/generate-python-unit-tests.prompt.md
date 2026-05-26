---
mode: "ask"
description: "Generate unit tests for a Python Flask API route in this project"
---

## Context

You are writing unit tests for the **Tailspin Shelter** Flask REST API located in `server/app.py`. The existing test suite lives in `server/test_app.py` and uses Python's built-in `unittest` framework with `unittest.mock` for isolation. **No real database should ever be touched by a test.**

## Your Task

Generate unit tests for the Flask route or function that is currently selected or described by the user. Add the new tests to `server/test_app.py` inside the existing `TestApp` class. Do **not** create a new file.

---

## Mandatory Rules

### Framework & Imports
- Use only `unittest` and `unittest.mock` — no third-party test libraries (pytest, etc.).
- Import `patch` and `MagicMock` from `unittest.mock`.
- Import `json` for parsing JSON responses.
- Use `app.test_client()` to make HTTP requests — never call route functions directly.

### Test Class Setup
- All tests belong inside `class TestApp(unittest.TestCase)`.
- `setUp` must create `self.app = app.test_client()` and set `self.app.testing = True` and `app.config['TESTING'] = True`.

### Mocking the Database
- Always patch `app.db.session.query` using `@patch('app.db.session.query')`.
- Build the mock chain to match how the route uses it. For example, if the route calls `.join(...).filter(...).first()`, chain the mock accordingly:
  ```python
  mock_query.return_value.join.return_value.filter.return_value.first.return_value = mock_dog
  ```
- For list endpoints that call `.all()`, configure the chain to end with `.all.return_value = [...]`.
- Return `None` from the final call to simulate a "not found" scenario.

### Helper Methods (reuse the existing ones)
- `_create_mock_dog(dog_id, name, breed)` — creates a `MagicMock` with `.id`, `.name`, `.breed`, and `.to_dict()` pre-configured.
- `_setup_query_mock(mock_query, dogs)` — configures the query mock for list endpoints.
- If the new route needs a different shape of mock data (e.g. includes `age`, `status`, `gender`), create a new `_create_mock_<entity>` helper that follows the same pattern.

### Required Test Cases (write ALL of these per route)
1. **Happy path** — valid input, returns expected status code (200) and correct JSON body.
2. **Empty / no results** — the query returns an empty list or `None`; assert the appropriate response (empty array `[]` or 404 with `{"error": "..."}` body).
3. **Response structure** — assert the response JSON contains exactly the expected keys (use `set(data.keys())`).
4. **Single item detail** (for `GET /<id>` routes) — assert each field value is correct, including enum fields (e.g. `status` returned as a string name).
5. **Error / edge case** — if the route accepts an ID or other path param, test a missing/non-existent value and assert HTTP 404.

### Naming Convention
```
test_<route_function_name>_<scenario>
```
Examples:
- `test_get_dogs_success`
- `test_get_dogs_empty`
- `test_get_dog_not_found`
- `test_get_dog_by_breed_success`

### Arrange–Act–Assert Pattern
Structure every test with clear comments:
```python
# Arrange  — set up mocks and data
# Act      — call self.app.get('/api/...')
# Assert   — check status_code, json body, and mock call counts
```

### Assertions Checklist
- `self.assertEqual(response.status_code, <expected>)` — always check status code first.
- `data = json.loads(response.data)` — parse the response body.
- Assert field values, not just presence.
- For list responses, assert `len(data)` and spot-check at least the first item.
- Use `mock_query.assert_called_once()` to confirm the DB was queried exactly once.
- Use `mock_query.assert_not_called()` where the DB should never be hit.

---

## Reference — Key Route Patterns in This Project

```python
# List endpoint — patches query + join + all
@patch('app.db.session.query')
def test_example_list(self, mock_query):
    mock_q = MagicMock()
    mock_query.return_value = mock_q
    mock_q.join.return_value = mock_q
    mock_q.all.return_value = [...]

# Detail endpoint — patches query + join + filter + first
@patch('app.db.session.query')
def test_example_detail(self, mock_query):
    mock_query.return_value.join.return_value.filter.return_value.first.return_value = mock_dog

# Breed filter endpoint — patches query + join + filter + all
@patch('app.db.session.query')
def test_example_breed_filter(self, mock_query):
    mock_query.return_value.join.return_value.filter.return_value.all.return_value = [...]
```

---

Now read `#file:server/app.py` and `#file:server/test_app.py` for full context, then generate the complete set of tests for the target route.
