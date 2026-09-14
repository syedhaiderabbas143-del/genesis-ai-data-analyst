# Secure GitHub Setup Checklist

- [ ] Create a private GitHub repository.
- [ ] Add this project without `.env`, databases, credentials, or real datasets.
- [ ] Enable secret scanning and push protection where available.
- [ ] Enable Dependabot alerts and security updates.
- [ ] Protect `main`: pull request required, CI required, force-push disabled.
- [ ] Store production secrets in GitHub Actions/environment secrets, not source code.
- [ ] Review `PUBLICATION_AUDIT.json` before publishing.
- [ ] Rotate any secret that may previously have been exposed.
