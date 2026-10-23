# Branching and Git Workflow

## Branch strategy

- `main`: stable, working baseline. Keep it runnable.
- `feature/<short-description>`: changes for one feature or task.
- `fix/<short-description>`: targeted bug fixes.

## Workflow for a change

1. Start from the latest `main`.
2. Create a focused branch.
3. Make one logical change at a time.
4. Run the application and tests.
5. Review `git diff` and `git status`.
6. Commit with a clear imperative message.
7. Push the branch to GitHub.
8. Open a pull request into `main`, review the diff, and merge after checks pass.
9. Delete the merged feature branch.

## Example commands

```bash
git switch main
git pull origin main
git switch -c feature/health-endpoint
# make changes
python -m pytest -v
git status
git diff
git add app.py
git commit -m "Add application health endpoint"
git push -u origin feature/health-endpoint
```

Then create a pull request on GitHub and merge it after review. For a solo learning repository, a local merge is also possible, but a pull request demonstrates the review workflow.

## Commit message examples

- `Add Flask monitoring dashboard`
- `Persist health-check results in SQLite`
- `Add tests for HTTP failures`
- `Document local setup and branching workflow`

Avoid vague messages such as `changes`, `final`, or `stuff`.
