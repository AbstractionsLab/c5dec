# Software Bill of Materials (SBOM)

C5-DEC CAD includes a dedicated SBOM module (`c5dec/core/sbom.py`) that
provides full lifecycle management of Software Bills of Materials for
**CRA Annex I Part II(1)** compliance: component transparency and vulnerability
identification.

SBOM artefacts are stored as [Doorstop](https://doorstop.readthedocs.io/)
items, enabling traceability links from components to CRA requirements.

---

## Overview

| Operation | CLI command | Description |
|-----------|-------------|-------------|
| Generate  | `c5dec sbom generate` | Produce a CycloneDX or SPDX SBOM from sources |
| Import    | `c5dec sbom import`   | Load a JSON/XML SBOM into a Doorstop document |
| Diff      | `c5dec sbom diff`     | Compare two versioned SBOMs |
| Validate  | `c5dec sbom validate` | Check SBOM completeness against CRA criteria |

---

## Prerequisites

SBOM **generation** requires [Syft](https://github.com/anchore/syft), which is
pre-installed in the C5-DEC dev container. To verify:

```sh
syft version
```

If Syft is not available, install it following the
[Syft installation guide](https://github.com/anchore/syft#installation).

SBOM **import, diff, and validate** operations use only the Python standard
library and Doorstop; no additional tools are required.

---

## Generating an SBOM

```sh
# CycloneDX JSON (default)
c5dec sbom generate /path/to/project -f cyclonedx -o sbom-v1.0.json

# SPDX JSON
c5dec sbom generate /path/to/project -f spdx -o sbom-v1.0-spdx.json
```

| Argument | Description |
|----------|-------------|
| `target` | Directory, file, or container image to analyse |
| `-f` / `--format` | `cyclonedx` (default) or `spdx` |
| `-o` / `--output` | Output file name (default: `sbom.json`) |

The generated SBOM file is in JSON format and can be opened with any
CycloneDX/SPDX-compatible viewer or directly imported into Doorstop.

---

## Importing an SBOM into Doorstop

```sh
c5dec sbom import sbom-v1.0.json --prefix SBOM-v1.0 --version "1.0"
```

| Argument | Description |
|----------|-------------|
| `sbom_file` | Path to the SBOM JSON file |
| `--prefix` | Doorstop document prefix (default: `SBOM`) |
| `--version` | Version label appended to the prefix |

Each SBOM component becomes a Doorstop YAML item, for example:

```
docs/specs/SBOM-v1.0/
├── .doorstop.yml
├── sbom_index.json
├── SBOM-v1.0-001.yml   # Component: requests 2.31.0
├── SBOM-v1.0-002.yml   # Component: cryptography 41.0.0
└── ...
```

### Component item structure

```yaml
active: true
text: |
  requests 2.31.0
  Type: library
  Language: Python
  PURL: pkg:pypi/requests@2.31.0
  License: Apache-2.0
  CPE: cpe:2.3:a:python-requests:requests:2.31.0:*:*:*:*:*:*:*
links:
  - CRAC015: null   # upward link to CRA checklist requirement (Doorstop UID)
```

---

## Comparing two SBOMs (diff)

To track component changes between software versions:

```sh
c5dec sbom diff SBOM-v1.0 SBOM-v2.0 -o sbom-changes.md
```

| Argument | Description |
|----------|-------------|
| `sbom1` | Doorstop prefix for the older SBOM |
| `sbom2` | Doorstop prefix for the newer SBOM |
| `-o` | Output Markdown report path (optional; prints to console otherwise) |

The diff report groups components into three categories:

- **Added** — new components introduced in `sbom2`
- **Removed** — components present in `sbom1` but absent from `sbom2`
- **Changed** — components whose version or licence changed between versions

### Sample diff report

```markdown
## SBOM Diff: SBOM-v1.0 → SBOM-v2.0

### Summary
- Added:   3 components
- Removed: 1 component
- Changed: 2 components

### Added
+ flask 3.0.3 (pkg:pypi/flask@3.0.3)
...
```

---

## Validating SBOM compliance

```sh
c5dec sbom validate SBOM-v1.0
```

The validation checks:

1. All components have a valid PURL (Package URL).
2. All components have a declared licence.
3. All items are active and contain non-empty text fields.
4. The `sbom_index.json` metadata file is present.

A passing validation confirms basic CRA Annex I Part II(1) transparency
requirements are met.

---

## Traceability to CRA requirements

SBOM Doorstop items can carry upward links to CRA checklist items. This
enables the traceability report to show which SBOM components satisfy which
CRA obligations.

Example link in `SBOM-v1.0-001.yml`:

```yaml
links:
  - CRAC015: null   # Doorstop UID of the corresponding CRA checklist item
```

The link target must be the **Doorstop UID** of the item (e.g., `CRAC015`), not the
CRA regulation ID (e.g., `cra_ii_1_1`). The Doorstop UID can be found in the `index.json`
file at the root of the CRA checklist document directory (`docs/specs/CRAC/index.json`).

See [CRA compliance](cra.md) for further details on the CRA checklist and
its traceability to the CRA regulation.

---

## Python API

```python
from c5dec.core import sbom
from pathlib import Path

# Generate
sbom_path = sbom.generate_sbom(
    target_path=Path("."),
    output_format="cyclonedx-json",
    output_path=Path("sbom.json"),
)

# Import
doc_path = sbom.import_sbom_to_doorstop(
    sbom_path=Path("sbom.json"),
    project_path=Path("."),
    prefix="SBOM-v1.0",
    version="1.0",
)

# Diff
diff = sbom.compare_sboms(
    sbom1_prefix="SBOM-v1.0",
    sbom2_prefix="SBOM-v2.0",
)

# Export diff report
sbom.export_sbom_diff_report(diff, Path("sbom-changes.md"))

# Validate
is_valid = sbom.validate_sbom(sbom_prefix="SBOM-v1.0")
```

---

## Related pages

| Topic | Page |
|-------|------|
| CRA compliance checklists | [CRA](cra.md) |
| SSDLC project structure | [SSDLC](ssdlc.md) |
| Doorstop traceability | [SSDLC — requirements traceability](ssdlc.md) |
| DocEngine publishing | [SSDLC — DocEngine](ssdlc.md) |
