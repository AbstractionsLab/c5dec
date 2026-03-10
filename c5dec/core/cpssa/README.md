# CPSSA — developer guide

This document is aimed at developers working on or integrating with the
**Cyber-Physical System Security Assessment (CPSSA)** package located at
`c5dec/core/cpssa/`.  It covers the package layout, the TARA integration
helpers, and end-to-end usage examples.

---

## Package layout

```
cpssa/
├── __init__.py                # Public re-exports (see "Public API" below)
├── cpssa.py                   # TARA integration helpers
├── threagile-mappings.yml     # Doorstop → Threagile schema value mappings
├── threagile-schema.json      # Threagile JSON schema reference
└── examples/
    └── water-treatment/       # Self-contained ICS / SCADA demo (with README)
```

---

## Public API

All TARA helper functions are re-exported from `c5dec.core.cpssa`:

```python
from c5dec.core.cpssa import (
    create_threat_model,
    generate_cpssa_report,
    generate_dfd,
    generate_fair_input_template,
    run_quantitative_risk_analysis,
)
```

---

## TARA integration helpers

`cpssa.py` provides five standalone functions that bridge C5-DEC SSDLC
projects with external TARA tooling (Threagile, OWASP pytm, pyfair).
They require no external engine state and can be called independently.

### Function overview

| # | Function | Input | Output |
|---|----------|-------|--------|
| 1 | `create_threat_model` | Doorstop project path | Threagile YAML / pytm Python script / pytm JSON |
| 2 | `generate_cpssa_report` | Threagile YAML | CPSSA Markdown report skeleton |
| 3 | `generate_dfd` | Doorstop project path | PlantUML DFD |
| 4 | `generate_fair_input_template` | Threagile YAML / pytm JSON | FAIR calibration YAML template |
| 5 | `run_quantitative_risk_analysis` | Threagile YAML / pytm JSON | FAIR/pyfair ALE summary + CSV |

All functions follow the same convention: they accept `Path`-like inputs,
write output to disk, and return the **absolute path string** of the
written file.  They raise `common.C5decError` on unrecoverable errors.

### 1. `create_threat_model`

Reads Doorstop architecture (ARC/HARC/LARC) items from a C5-DEC project
and produces a threat-model template.  Only ARC items are processed for
all output formats; SWD items are intentionally excluded.

```python
from c5dec.core.cpssa import create_threat_model
from pathlib import Path

project = Path("/path/to/my-project")

# Threagile YAML (default)
out = create_threat_model(project)
print(out)  # /path/to/my-project/threat-model.yml

# Executable pytm Python script
out = create_threat_model(project, format="pytm-python")

# JSON representation of the pytm model
out = create_threat_model(project, format="pytm-json",
                          output_path=project / "out" / "model.json")

# Explicit architecture folder (bypasses auto-discovery)
out = create_threat_model(project, arc_folder="/path/to/arc-items")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_path` | `Path` | Root directory of a C5-DEC SSDLC project |
| `output_path` | `Path`, optional | Destination file (default depends on format) |
| `format` | `str` | `"threagile"` (default), `"pytm-python"`, or `"pytm-json"` |
| `arc_folder` | `str`, optional | Full path to architecture item files (no `.doorstop.yml` required) |

**Architecture folder discovery:** when `arc_folder` is omitted the
function searches the Doorstop specs root for the first subdirectory named
`arc`, `harc`, or `larc` (case-insensitive) that contains a
`.doorstop.yml` file.  When `arc_folder` is provided it is used directly.

**Doorstop item conventions used:**

Core fields:

| Field | Doorstop attribute | Notes |
|-------|--------------------|-------|
| Node label | `header` or UID | Falls back to UID, then first 60 chars of `text` |
| Asset type | `type` | `server`, `plc`, `database`, `actor`, `firewall`, … (mapped via `threagile-mappings.yml`) |
| Trust zone | `zone` | Maps to Threagile trust boundary / pytm Boundary |
| Data flows | `flows` | Primary mechanism (see below); falls back to ARC-prefixed `links` |

Threagile-specific fields (mapped via `threagile-mappings.yml`):

| Field | Doorstop attribute | Default |
|-------|--------------------|---------|
| Technology | `type` | `unknown-technology` |
| Encryption | `encryption` or `is_encrypted` | `none` (or `transparent` if `is_encrypted` is true) |
| Machine | `machine` | `physical` for PLC/RTU/HMI/workstation, `virtual` otherwise |
| Size | `size` | `component` |
| Confidentiality | `confidentiality` | `confidential` |
| Integrity | `integrity` | `critical` |
| Availability | `availability` | `critical` |
| Data formats | `data_formats_accepted` | `["json"]` |
| Data assets processed | `data_assets` or `data_assets_processed` | `[]` |
| Data assets stored | `data_assets_stored` | `[]` |
| Owner | `vendor` | `TBD` |
| Internet-facing | `internet` | `false` |
| Out of scope | `out_of_scope` | `false` |
| Multi-tenant | `multi_tenant` | `false` |
| Redundant | `redundancy` or `redundant` | `false` |
| Custom developed | `custom_developed_parts` | `false` |

pytm-specific fields:

| Field | Doorstop attribute | Notes |
|-------|--------------------|-------|
| OS | `os` or `os_version` | Operating system |
| Port | `port` | Listening port |
| Protocol | `protocol` | Communication protocol |
| Vendor/Model | `vendor`, `model` | Asset metadata |
| Security controls | `is_encrypted`, `has_access_control`, `authenticates_source` | Boolean flags |
| Data sensitivity | `stores_pii`, `is_sql`, `safety_rated` | Boolean flags |

**Data flows (`flows` field):**

The `flows` field is the primary mechanism for defining data-flow edges
between ARC items.  Each entry must have at least a `target` key; all other
keys are optional:

```yaml
flows:
  - target: ARC-006
    protocol: OPC-UA
    port: 4840
    encrypted: false
    authentication: none
    authorization: none
    vpn: false
    readonly: false
    data_assets_sent: [sensor-readings]
    data_assets_received: [control-commands]
```

When `flows` is absent, the function falls back to legacy behaviour: it
reads every entry in the Doorstop `links` field whose UID starts with an
architecture-document prefix (`ARC-`, `HARC-`, `LARC-`) and constructs a
minimal flow dict using the item-level `protocol` and `port` fields.

**Sidecar files:**

The function reads two optional sidecar files from the ARC item directory:

- `threat-actors.yml` — threat actor definitions (included in the Threagile
  `threat_actors` section and the CPSSA report)
- `assumptions.yml` — documented assumptions (included in the Threagile
  `assumptions` section and the CPSSA report)

**Threagile value mappings:**

Doorstop field values (e.g. protocol names, authentication types) are
mapped to Threagile-compatible schema values via the external
`threagile-mappings.yml` file.  Supported mapping sections:
`protocol`, `authentication`, `authorization`, `technology`, `asset_type`,
`encryption`, `machine`, `size`, `confidentiality`, `integrity`,
`availability`, `trust_boundary_type`, `data_format`.

**Processing limits:** at most 40 architecture items are processed.

### 2. `generate_cpssa_report`

Consumes a Threagile-compatible YAML and produces a structured Markdown
report with the following numbered sections:

1. Executive summary
2. System description (business + technical overview)
3. Assets and dependencies (technical assets, data assets, trust boundaries)
4. Threat landscape (STRIDE categories, threat actors, documented assumptions)
5. Attack scenarios (from abuse cases)
6. Risk assessment (placeholder table)
7. Security requirements (extracted from the `security_requirements` map in the threat model YAML)
8. Recommended controls (placeholder table)
9. Residual risk
10. Conclusion

When `threat_actors` or `assumptions` are present in the threat model YAML
(populated via the sidecar files), they are rendered in section 4.

```python
from c5dec.core.cpssa import generate_cpssa_report

out = generate_cpssa_report(
    threat_model_path="threat-model.yml",
    output_path="reports/cpssa-report.md",   # optional
)
```

The generated file contains placeholder prompts (`_[Complete this
section.]_`) for fields that require human review.

### 3. `generate_dfd`

Derives a PlantUML Data Flow Diagram from Doorstop architecture
(ARC/HARC/LARC) items.  SWD items are not processed.  Zone-based trust
boundaries become `rectangle` groupings.  At most 40 items are processed
(same cap as `create_threat_model`).

Element IDs, asset-type classification, trust-boundary IDs, and data-flow
labels all match the Threagile output produced by `create_threat_model` so
that the two artefacts are cross-referenceable.  Specifically:

- Element IDs use `_safe_threagile_id` (lowercase, hyphens, max 31 chars).
- Asset types follow Threagile's `ta_type` logic: `datastore`, `external-entity`,
  or `process`; rendered in PlantUML as `database`, `actor`, or `component`.
- Trust-boundary rectangle IDs use `_safe_threagile_id("<zone>-zone")`.
- Flow arrows are labelled `flow-N [protocol / enc-status / auth]` matching
  Threagile `communication_links` keys and annotations.

Data flows are derived from the `flows` field (with fallback to
ARC-prefixed `links`), consistent with `create_threat_model`.

```python
from c5dec.core.cpssa import generate_dfd

out = generate_dfd(
    project_path="/path/to/my-project",
    output_path="docs/cpssa-dfd.puml",   # optional
    arc_folder="/path/to/arc-items",     # optional, bypasses auto-discovery
)
```

Render the diagram with PlantUML:

```bash
java -jar plantuml.jar cpssa-dfd.puml
```

### 4. `generate_fair_input_template`

Generates a FAIR parameters YAML template from a threat model so you can
calibrate per-scenario PERT distribution bounds before running the
quantitative risk analysis.

Accepts both Threagile YAML and pytm JSON threat models (auto-detected by
file extension).  For pytm JSON models without explicit `abuse_cases`,
one scenario per element is synthesised.

```python
from c5dec.core.cpssa import generate_fair_input_template

out = generate_fair_input_template(
    threat_model_path="threat-model.yml",
    output_path="fair-params.yml",  # optional
)
```

The generated YAML contains `defaults` (global fallback bounds) and
`scenarios` (per-scenario overrides with placeholder values).

The template exposes the **full FAIR model tree**.  Simple `lef` + `lm`
inputs are active by default; advanced decomposition nodes (`tef`,
`vulnerability`, `contact`, `action`, `tc`, `cs`, `pl`, `sl`, `slef`,
`slem`) are included as commented-out lines.  Uncomment the child nodes
and remove their parent to use a finer decomposition level.

Default PERT bounds (simple path):
- **LEF** (Loss Event Frequency): low=1, mode=5, high=20
- **LM** (Loss Magnitude): low=10 000, mode=100 000, high=1 000 000

### 5. `run_quantitative_risk_analysis`

Runs a FAIR-based Monte Carlo simulation via *pyfair* for each abuse case
and produces an Annualised Loss Expectancy (ALE) summary.

Accepts both Threagile YAML and pytm JSON threat models (auto-detected by
file extension).  For pytm JSON models without explicit `abuse_cases`,
one scenario per element is synthesised.

Calibration parameters are resolved in order of precedence:

1. **Dedicated FAIR parameters file** (`fair_params_path`) — YAML mapping
   scenario names to PERT bounds.  Generate with
   `generate_fair_input_template`.
2. **Inline in threat model** — abuse case values as dicts containing any
   recognised FAIR node keys (`lef`, `lm`, `tef`, `vulnerability`,
   `contact`, `action`, `tc`, `cs`, `pl`, `sl`, `slef`, `slem`).
3. **Fallback defaults** — conservative placeholders (a warning is emitted
   for each scenario that uses defaults).

```python
from c5dec.core.cpssa import run_quantitative_risk_analysis

# Requires: pip install pyfair
out = run_quantitative_risk_analysis(
    threat_model_path="threat-model.yml",
    output_path="reports/",               # optional, output directory
    simulations=10_000,
    fair_params_path="fair-params.yml",    # optional, calibration file
)
```

Outputs (written to `output_path` directory, defaults to threat model's
parent directory):
- `cpssa-risk-summary.md` — Markdown summary with an input parameters
  table (showing all supplied FAIR nodes) and ALE statistics per scenario
- `cpssa-risk-results.csv` — raw Monte Carlo simulation results
- `cpssa-risk-{N}.html` — one interactive pyfair report per scenario
  (indexed from 1), each comparing the individual model against the
  meta-model

---

## End-to-end example

### TARA helpers workflow

```python
from c5dec.core.cpssa import (
    create_threat_model,
    generate_cpssa_report,
    generate_dfd,
    generate_fair_input_template,
    run_quantitative_risk_analysis,
)
from pathlib import Path

project = Path("/path/to/my-ssdlc-project")

# Step 1 — generate threat model from Doorstop artifacts
tm_path = create_threat_model(project)
print(f"Threat model: {tm_path}")

# Step 2 — generate CPSSA report skeleton
report_path = generate_cpssa_report(tm_path)
print(f"Report skeleton: {report_path}")

# Step 3 — generate a PlantUML data flow diagram
dfd_path = generate_dfd(project)
print(f"DFD: {dfd_path}")

# Step 4 — generate FAIR calibration template
fair_tpl = generate_fair_input_template(tm_path)
print(f"FAIR template: {fair_tpl}")
# ... edit fair-params.yml with calibrated values ...

# Step 5 — run quantitative risk analysis
risk_path = run_quantitative_risk_analysis(
    tm_path, fair_params_path=fair_tpl,
)
print(f"Risk summary: {risk_path}")
```