# Security policy

## Supported versions

Security fixes are applied to the current stable release only.

| Version | Supported |
|---------|-----------|
| 1.2.x   | Yes       |
| < 1.2   | No        |

## Reporting a vulnerability

**Please do not report security vulnerabilities via public GitHub issues.**

If you believe you have found a security vulnerability in C5-DEC CAD, please disclose it responsibly by sending an email to:

**info@abstractionslab.lu**

Include the following information in your report:

- A clear description of the vulnerability and its potential impact.
- The affected component(s) and version(s).
- Step-by-step instructions to reproduce the issue.
- Any relevant proof-of-concept code, logs, or screenshots (if safe to share).

## Response timeline

| Stage | Target |
|-------|--------|
| Initial acknowledgement | Within 5 business days |
| Vulnerability confirmed or rejected | Within 15 business days |
| Patch released (if confirmed) | Dependent on severity and complexity |

We will keep you informed throughout the process. If a fix requires a coordinated disclosure with third-party maintainers, we will agree on a timeline with you before any public disclosure.

## Scope

The following are **in scope** for vulnerability reports:

- The `c5dec` Python package and all modules under `c5dec/`.
- The Docker container definitions (`Dockerfile`, `dev.Dockerfile`, `docEngine.Dockerfile`).
- The CLI, TUI, and GUI interfaces.
- The cryptography module, including integration with GnuPG, Kryptor, Cryptomator CLI, and OQS-OpenSSL.

The following are **out of scope**:

- Third-party tools integrated by C5-DEC (Doorstop, Quarto, pandoc, Syft, etc.) — report those to the respective upstream projects.
- Vulnerabilities in the local machine or container host environment.
- Denial-of-service attacks on the locally running GUI server (`localhost:5432`).

## Disclosure policy

C5-DEC follows a **coordinated disclosure** model. We ask that you allow a reasonable amount of time for us to address the vulnerability before any public disclosure. We will credit reporters in the release notes unless you prefer to remain anonymous.
