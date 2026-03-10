# Troubleshooting

This page covers the most common issues encountered when installing and running C5-DEC CAD, and how to resolve them.

## Table of contents

- [Container build failures](#container-build-failures)
- [Poetry environment issues](#poetry-environment-issues)
- [Doorstop validation errors](#doorstop-validation-errors)
- [GUI port conflicts](#gui-port-conflicts)
- [General tips](#general-tips)

---

## Container build failures

### The build script fails with "Cannot connect to the Docker daemon"

**Symptom:** `./build-c5dec.sh` exits with `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`.

**Cause:** Docker Engine (Linux) or Docker Desktop (macOS / Windows) is not running.

**Fix:**
- **Linux**: start the Docker service with `sudo systemctl start docker`.
- **macOS / Windows**: open Docker Desktop and wait for it to report "Engine running".

---

### VS Code does not show "Reopen in Container"

**Symptom:** Opening the project folder in VS Code shows no dev container notification.

**Cause:** The Dev Containers extension is not installed, or Docker Desktop is not running.

**Fix:**
1. Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
2. Make sure Docker Desktop is running.
3. Close and reopen the project folder in VS Code, or run **Dev Containers: Reopen in Container** from the command palette (Cmd/Ctrl+Shift+P).

---

### Container build fails mid-way with a network error

**Symptom:** The build stops with `Failed to fetch` or `Could not resolve host`.

**Cause:** A package registry was unreachable during the build (transient network issue).

**Fix:** Re-run the build. Docker caches layers, so only the failed step and those after it will be retried:

```sh
./build-c5dec.sh
```

If the failure recurs on the same layer, check whether the package registry is currently reachable from your network and try again later.

---

### `dev.Dockerfile` build fails on `apt-get install`

**Symptom:** The build exits with `E: Package '<name>' has no installation candidate`.

**Cause:** The Debian/Ubuntu package index inside the build context is stale.

**Fix:** Force a full rebuild without using cached layers:

```sh
docker build --no-cache -f dev.Dockerfile -t c5dec-dev .
```

---

## Poetry environment issues

### `c5dec: command not found` inside the dev container

**Symptom:** Running `c5dec` after opening the dev container terminal returns `command not found`.

**Cause:** The Poetry virtual environment has not been activated.

**Fix:** Activate the environment:

```sh
poetry shell
```

Then retry the command. Alternatively, prefix every command with `poetry run`:

```sh
poetry run c5dec -h
```

---

### `poetry install` fails with a dependency conflict

**Symptom:** `poetry install` exits with `SolverProblemError: …`.

**Cause:** A `pyproject.toml` change introduced an incompatible dependency constraint.

**Fix:**
1. Run `poetry check` to identify the invalid constraint.
2. Review recent changes to `pyproject.toml`.
3. Update the conflicting constraint and re-run `poetry install`.

---

### Missing imports warning in VS Code (yellow squiggles)

**Symptom:** VS Code shows import errors for `c5dec` modules despite the project being open in the dev container.

**Cause:** VS Code is not using the Poetry-managed Python interpreter.

**Fix:** Click the light bulb next to a warning and select the Python interpreter installed by Poetry, or open the command palette → **Python: Select Interpreter** and choose the Poetry environment path (typically `.venv/bin/python` inside the container).

---

## Doorstop validation errors

### `doorstop` reports "Unknown parent document"

**Symptom:** `poetry run doorstop` exits with `unknown parent document`.

**Cause:** A Doorstop document references a parent document that does not exist or has been renamed.

**Fix:**
1. Open the `.doorstop.yml` file of the affected document.
2. Verify the `parent` field matches an existing document prefix.
3. Re-run `poetry run doorstop` to confirm the fix.

---

### `doorstop` reports broken links

**Symptom:** `poetry run doorstop` lists items with `ERR: broken link`.

**Cause:** A requirement item links to an item UID that no longer exists.

**Fix:** Use the SpecEngine pruning utility to identify and remove orphaned links:

```sh
python docs/specs/SpecEngine/prune_bad_links.py
```

Then re-run `poetry run doorstop` to confirm all links are valid.

---

### Doorstop item YAML fails to parse

**Symptom:** `doorstop` reports `yaml.scanner.ScannerError` on a specific item file.

**Cause:** A manual edit introduced invalid YAML syntax in an item `.yml` file.

**Fix:** Open the reported file and check for unescaped special characters (colons, brackets, quotes) in the `text` or `ref` fields. Wrap affected values in single or double quotes.

---

## GUI port conflicts

### The GUI fails to start with "Address already in use"

**Symptom:** `c5dec -g` (or `./c5dec.sh -g`) exits immediately with `OSError: [Errno 98] Address already in use`.

**Cause:** Another process is already bound to port `5432`.

**Fix:**
1. Find the process occupying the port:
   ```sh
   lsof -i :5432
   ```
2. Stop the conflicting process, or use a different port by setting the `C5DEC_GUI_PORT` environment variable before launching:
   ```sh
   C5DEC_GUI_PORT=5433 c5dec -g
   ```
   Then open `http://127.0.0.1:5433` in your browser.

---

### Browser shows "This site can't be reached" after launching the GUI

**Symptom:** The terminal shows the Flask server starting, but the browser cannot connect to `127.0.0.1:5432`.

**Cause (dev container):** The container port is not mapped to the host.

**Fix:** In VS Code, check **Ports** (bottom status bar → Ports tab). If port `5432` is not listed as forwarded, click **Forward a Port**, enter `5432`, then refresh the browser.

---

## General tips

- **Check the C5-DEC version**: run `c5dec --version` (or `./c5dec.sh --version`) to confirm which release you are running before reporting an issue.
- **Rebuild after a git pull**: if behaviour changes unexpectedly after pulling the latest code, rebuild the Docker image with `./build-c5dec.sh` (Docker model) or rebuild the dev container by selecting **Dev Containers: Rebuild Container** from the VS Code command palette.
- **Consult the full log**: many commands support a `--debug` or `-v` flag. Check the command's `--help` for available verbosity options.
- **Open an issue**: if none of the above resolves your problem, open an issue on the [GitHub repository](https://github.com/AbstractionsLab/c5dec/issues) with the C5-DEC version, deployment method, steps to reproduce, and any relevant log output.
