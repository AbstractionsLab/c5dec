# Contributing to C5-DEC CAD

Thank you for your interest in contributing to C5-DEC CAD. This document explains how to set up the development environment, submit changes, and follow project conventions.

## Table of contents

- [Prerequisites](#prerequisites)
- [Getting the code](#getting-the-code)
- [Development environment](#development-environment)
- [Branching and workflow](#branching-and-workflow)
- [Commit message convention](#commit-message-convention)
- [Running the test suite](#running-the-test-suite)
- [Code conventions](#code-conventions)
- [Documentation conventions](#documentation-conventions)
- [Opening issues and pull requests](#opening-issues-and-pull-requests)

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Docker Engine](https://docs.docker.com/engine/install/)
- [Visual Studio Code](https://code.visualstudio.com/) with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
- [Git](https://git-scm.com/)
- [Poetry](https://python-poetry.org/) ≥ 1.1 (inside the dev container, Poetry is pre-installed)

---

## Getting the code

```sh
git clone https://github.com/AbstractionsLab/c5dec.git
cd c5dec
```

Open the folder in VS Code and select **Reopen in Container** to start the `C5-DEC CAD dev container`. All Python dependencies are installed automatically via Poetry.

---

## Development environment

Inside the dev container, activate the Poetry virtual environment:

```sh
poetry shell
```

You can then run any `c5dec` command directly:

```sh
c5dec -h
```

If you modify `pyproject.toml`, always validate it before committing:

```sh
poetry check
```

---

## Branching and workflow

| Branch | Purpose |
|--------|---------|
| `main` | Stable release branch; only merged from `develop` via pull request |
| `develop` | Integration branch for ongoing work |
| `feature/<short-description>` | New features or enhancements |
| `fix/<short-description>` | Bug fixes |
| `docs/<short-description>` | Documentation-only changes |

1. Branch off from `develop` (not `main`):
   ```sh
   git checkout develop
   git pull
   git checkout -b feature/my-feature
   ```
2. Make changes in small, focused commits (see below).
3. Push your branch and open a pull request targeting `develop`.

---

## Commit message convention

Use the imperative mood and keep the subject line under 72 characters:

```
<type>: <short summary>

[optional body — wrap at 72 chars]
```

| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation changes only |
| `refactor` | Code restructuring with no functional change |
| `test` | Adding or updating tests |
| `chore` | Tooling, dependencies, CI changes |

Example:

```
feat: add CRA Annex I checklist Excel export

Adds per-category compliance percentage columns to the
exported spreadsheet. Closes #42.
```

---

## Running the test suite

Run all tests from the repository root:

```sh
./run-test-suite.sh
```

Or with pytest directly (inside the Poetry environment):

```sh
pytest
```

Test fixtures live in `tests/content/`. Mock all external services (OpenProject, Doorstop remote) in new tests. 

---

## Code conventions

- Target Python 3.8–3.11; avoid syntax or library features not available in 3.8.
- Use `common.logger(__name__)` for logging; never `print()` for operational output.
- Raise `common.C5decError` for expected error conditions.
- Reference paths via `c5settings` constants — never hard-code file paths.
- Follow NumPy/Google docstring style for all public functions and classes.
- Run `poetry check` after any `pyproject.toml` modification.

---

## Documentation conventions

- All documentation lives under `docs/` (`docs/manual/`, `docs/specs/`). Never place docs alongside source code.
- File names: lowercase with hyphens (`debug-mode.md`). Exception: `README.md`.
- Section headings: sentence case only (`## Getting started`, not `## Getting Started`).
- Formats: Markdown, YAML, JSON, CSV, or LaTeX only.

---

## Opening issues and pull requests

- Search existing issues before opening a new one.
- For bug reports, include: C5-DEC version, deployment model (Docker scripts or dev container), steps to reproduce, expected vs actual behaviour.
- For feature requests, describe the use case and how it fits the C5-DEC methodology.
- Pull requests must include a description of the change and reference any related issue numbers.
- To report a security vulnerability, follow the process in [SECURITY.md](SECURITY.md) instead of opening a public issue.
