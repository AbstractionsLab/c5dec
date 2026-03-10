# Technical specifications aimed at traceability

This folder holds the authoritative, traceable specifications for IDPS-ESCAPE managed with Doorstop following the [C5-DEC](https://github.com/AbstractionsLab/c5dec) methodology and its enhancements to Doorstop via extra custom code and templates. Use it for defining what the system must do and why, not how to operate it.

## What lives here

| Path | Document type | Role in hierarchy |
|------|--------------|-------------------|
| `mrs/` | Mission Requirements Specifications | Root of the tree |
| `srs/` | Software/System Requirements Specifications | Child of MRS |
| `arc/` | Architecture | Child of MRS |
| `swd/` | Software design | Child of ARC |
| `tcs/` | Test case specifications (merged) | Child of SRS |
| `trp/` | Test reports (merged) | Child of TCS |
| `docs/publish/` | Generated HTML output | Produced by `publish.sh` |

### Custom tooling scripts

All scripts below live in `SpecEngine/`.

| Script | Purpose |
|--------|---------|
| `publish.sh` | Orchestrates the full publish pipeline (keyword replacement → HTML generation → traceability stats) |
| `c5publish.py` | Invokes the Doorstop HTML publisher and applies Bootstrap CSS patches to the output; pass `--include-cc-db` to include the CC database (excluded by default) |
| `c5-keyword.py` | Preprocessor/postprocessor that replaces `?c5-defect-X` shorthand keywords with styled HTML spans in TRP files before publishing, then restores originals |
| `c5traceability.py` | Configurable traceability analyser; reads `docs/traceability/traceability.csv` and produces coverage statistics and an optional HTML report; supports YAML-configurable checks, auto-discovery of the document hierarchy from `.doorstop.yml` files, and a `rich`-coloured terminal output (see [below](#traceability-statistics)) |
| `c5traceability_config.yaml` | Configuration file for `c5traceability.py` defining document order, coverage checks, and defect sources |
| `c5browser.py` | Generates an interactive HTML browser (`items_browser.html`) with sortable/filterable DataTables for every document type (see [below](#specification-browser)) |

## Doorstop hierarchy

```
MRS ──┬──> SRS ──> TCS ──> TRP
      └──> ARC ──> SWD
```

Links are **upward-only** (child → parent). Adding downward links causes `RecursionError` during publishing.

## Conventions

- **Numbering**: three digits per prefix (e.g., `SRS-001`) as set in each `.doorstop.yml`.
- **Format**: markdown items with YAML frontmatter followed by a markdown body.
- **Assets**: place supporting files per document under its `assets/` subfolder (e.g., `arc/assets/`, `tcs/assets/`).
- **Diagrams**: prefer PlantUML in assets; avoid Mermaid in specs.
- **Review hashes**: Doorstop fingerprints change when text or reviewed attributes update — re-review after edits with `poetry run doorstop review <uid>`.
- **Named items**: items like `MRS-ADBox` and `SRS-SONAR` are group-summary placeholders used for organisational purposes; they are excluded from numeric coverage statistics by default.

## Working with items

```bash
# Validate the tree
poetry run doorstop

# Add a new item (auto UID)
poetry run doorstop add srs

# Link child to parent (upward-only)
poetry run doorstop link TCS-001 SRS-046

# Review an item after editing it
poetry run doorstop review SRS-001
```

## Publishing

```bash
cd docs/specs
./publish.sh
```

`publish.sh` runs the full pipeline:
1. `c5-keyword.py` — replaces `?c5-defect-X` keywords in TRP files
2. `c5publish.py` — generates Bootstrap-styled HTML into `docs/publish/`; accepts `keep-cc` argument to include the CC database
3. `c5-keyword.py` — restores original TRP files
4. `c5traceability.py --html` — prints coverage statistics to the console and writes `docs/publish/traceability_stats.html`
5. `c5browser.py` — generates the interactive item browser at `docs/publish/items_browser.html`

## Traceability statistics

`c5traceability.py` reads `docs/traceability/traceability.csv` and produces configurable coverage analysis. The output sections are driven by `c5traceability_config.yaml`:

| Section | What it produces |
|---------|----------------|
| 1. Summary totals | Unique item count per document type |
| 2…N. Coverage checks | One section per check defined in `c5traceability_config.yaml`; each reports covered vs. uncovered items for a given parent–child document pair |
| N+1. Defect severity summary | Scans configured source files for `?c5-defect-X` keywords and summarises severity distribution; flags major/critical items (level ≥ 3) |
| N+2. Overall health score | Aggregate coverage percentage across all checks with a progress bar |

Output is color-coded in the terminal using `rich` (falls back to plain text if unavailable). The HTML report uses Bootstrap and is placed at `docs/publish/traceability_stats.html`.

If `c5traceability_config.yaml` is not found, the tool automatically discovers the document hierarchy from `.doorstop.yml` files and infers checks from every parent–child edge.

```bash
cd docs/specs

# Console output only
poetry run python SpecEngine/c5traceability.py

# Console + HTML report (default output path: docs/publish/traceability_stats.html)
poetry run python SpecEngine/c5traceability.py --html

# Custom CSV path and output location
poetry run python SpecEngine/c5traceability.py --csv ../../traceability/traceability.csv --html --output docs/publish/stats.html

# Include named/group items (e.g. MRS-ADBox) in statistics
poetry run python SpecEngine/c5traceability.py --include-named

# Auto-discover document hierarchy from .doorstop.yml files and print resulting config
poetry run python SpecEngine/c5traceability.py --discover

# Auto-discover and write the result to c5traceability_config.yaml, then run analysis
poetry run python SpecEngine/c5traceability.py --discover --discover-write

# Use a custom config file
poetry run python SpecEngine/c5traceability.py --config custom_config.yaml
```

**Note:** The default `c5traceability_config.yaml` may reference outdated document types after structural changes to the spec tree; regenerate it with `--discover --discover-write` if errors occur.

## Specification browser

`c5browser.py` scans all Doorstop subdirectories, parses each item's YAML frontmatter and H1 heading, and produces a standalone Bootstrap + DataTables HTML page at `docs/publish/items_browser.html`.

Features:
- **One tab per document type** — MRS, ARC, SRS, SWD, TCS, TRP
- **Sortable columns** — click any header to sort ascending/descending
- **Per-tab filter** — DataTables search box filters rows by any visible column (e.g. type "RADAR" to show only RADAR items)
- **Numeric fields colour-coded** — urgency, importance, risk etc. are rendered with severity colours (green → red)
- **Defect badges** on TRP rows show severity level at a glance
- Named/group items (e.g. `MRS-ADBox`) are shown muted; `active: false` items are struck through

```bash
cd docs/specs

# Default output: docs/publish/items_browser.html
poetry run python SpecEngine/c5browser.py

# Custom output path
poetry run python SpecEngine/c5browser.py --output docs/publish/browser.html

# Custom specs directory
poetry run python SpecEngine/c5browser.py --specs-dir /path/to/specs
```

## When to use which document

| Document | Use for |
|----------|---------|
| MRS | Mission and business needs; value and urgency |
| SRS | Software requirements and acceptance criteria |
| ARC | Architecture constraints and decisions |
| SWD | Software design details and diagrams |
| TCS | Test case specifications |
| TRP | Executed test reports with defect categorization |

For detailed rules and examples, see the per-folder `.doorstop.yml` defaults.