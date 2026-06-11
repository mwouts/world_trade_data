# Pending GitHub Actions workflows

These workflows could not be pushed to `.github/workflows/` directly because
the credential used in the remote session lacked the `workflow` scope.

To activate them, run:

```bash
git mv .github/workflows-pending/ci.yml .github/workflows-pending/publish-pypi.yml .github/workflows/
git rm .github/workflows-pending/README.md
git commit -m "Activate GitHub Actions workflows"
```
