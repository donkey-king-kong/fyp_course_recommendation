# Pull Request Template

## Description

Briefly explain what this PR adds or changes.

```text
Example: Adds the minimal FastAPI backend with a /health endpoint.
```

## Why This Change Is Needed

- 

## How To Test

List the exact commands or steps used to verify the change.

```bash
# Example
source .venv/bin/activate
uvicorn backend.main:app --reload
curl http://127.0.0.1:8000/health
```

## Expected Result

Describe the expected output.

```json
{"status":"ok"}
```

## Checklist

- [x] The PR title follows the convention: `<type>: <short description>`.
- [x] I tested the change locally.
- [x] I checked that no secrets or virtual environment files are committed.
