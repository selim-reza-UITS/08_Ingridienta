## Run Specific Tests

```

pytest app/accounts/tests/test_models.py

```
### =================================================

```

pytest -k test_create_user

```

## Extras You’ll Love

Show verbose output: pytest -v

Show print() logs: pytest -s

Run tests in parallel: uv pip install pytest-xdist → pytest -n auto

## CI/CD Ready

You can easily run pytest in GitHub Actions, GitLab CI, etc., with just:

```
- name: Run Tests
  run: pytest
```




# Later add factories.py: upcoming