---
applyTo: "server/*.py"
---

# Python & Flask Best Practices for Tailspin Shelter

## Code Style
- Follow **PEP 8** conventions: snake_case for variables and functions, PascalCase for classes.
- Always include **type hints** on function signatures and return types.
- Keep functions focused — each function should do one thing.

## Flask Routes
- Always specify the `methods` list explicitly on every `@app.route` decorator.
- Return meaningful HTTP status codes (e.g. `404` for not found, `400` for bad input, `201` for created).
- Use `jsonify()` for all JSON responses — never return raw dicts.

## SQLAlchemy
- Avoid raw SQL strings — always use SQLAlchemy ORM queries.
- Use `.first()` when expecting a single result, `.all()` when expecting multiple.
- Never expose internal SQLAlchemy model objects directly in API responses; convert to dicts first.

## Error Handling
- Validate inputs at route boundaries before querying the database.
- Return structured error responses: `{"error": "descriptive message"}`.

## General
- Do not commit secrets or database credentials — use environment variables.
- Prefer f-strings over `.format()` or `%` string formatting.