# Cyber-Physical System Security Assessment (CPSSA)

The CPSSA module provides a series of features that can be combined with existing OSS (Open-Source Software) for TARA (Threat Analysis and Risk Assessment) to carry out efficient and practical CPSSA following a TaC (TARA as Code) paradigm. This involves code-based and/or machine-readable threat model specifications that can, among other things, be easily integrated into CI/CD pipelines. We build on and provide support for [threagile](https://github.com/Threagile/threagile) for DevSecOps oriented threat modelling (TM) and security risk assessment (SRA), OWASP [pytm](https://github.com/OWASP/pytm) for programmatic threat modelling with automatic threat enumeration, and [pyfair](https://pypi.org/project/pyfair/) for quantitative risk analysis following the FAIR (Factor Analysis of Information Risk) approach relying on Monte Carlo simulations.

For more information, we refer the reader to our CPSSA report, published as part of the knowledge base elements of C5-DEC; see the README section on the [C5-DEC knowledge base (KB) reports](https://github.com/AbstractionsLab/c5dec/tree/main?tab=readme-ov-file#overview) to learn about gaining access to these. In our CPSSA report, in addition to providing a literature review, we describe our threat modelling and security risk assessment method adapted to the Common Criteria, while building on best practices and well-established methods such as the hybrid method developed by the software engineering institute (SEI) of Carnegie Mellon University (CMU).

Here we address system-oriented threat modelling and risk assessment, for organization-centric risk assessment requiring comprehensive risk management according to ISO/IEC 27005, we recommend [TRICK Service](https://www.trickservice.com/), enabled by the open-source [OpenTRICK](https://github.com/itrust-consulting/OpenTRICK) software, which supports a detailed quantitative risk assessment approach following a ROSI (Return On Security Investment) method; OpenTRICK has also been further improved and released as open-source software in project [CyFORT](https://abstractionslab.com/index.php/research-and-development/cyfort/).

Finally, we also recommend OWASP [Threat Dragon](https://github.com/OWASP/threat-dragon) for GUI-based TM and [Capella Darc Viewpoint](https://github.com/eclipse/capella-cybersecurity/wiki) for more advanced and detailed TM using [Capella](https://mbse-capella.org/) for model-based systems engineering, following the [ARCADIA method](https://en.wikipedia.org/wiki/Arcadia_(engineering)), and [ADTool](https://github.com/tahti/ADTool2) for attack tree modelling and analysis.

---

## C5-DEC native CPSSA commands

C5-DEC provides built-in commands that automate the initial steps of a CPSSA
engagement directly from Doorstop project artefacts.

### Step 1: create-threat-model

Reads architecture (ARC/HARC/LARC) Doorstop items from a C5-DEC SSDLC
project and generates a threat-model template in one of three formats.
SWD (software-design) items are not processed.

- **threagile** (default) — [Threagile](https://github.com/Threagile/threagile)-compatible YAML.  Uses ARC items only.
- **pytm-python** — executable Python script using the [OWASP pytm](https://github.com/OWASP/pytm) library.  Uses ARC items only.
- **pytm-json** — JSON file consumable by `pytm.load()` or `c5dec cpssa risk-analysis`.  Uses ARC items only.

```sh
# Threagile YAML (default) — auto-discovers arc/harc/larc folder
c5dec cpssa create-threat-model --project /path/to/project -o threat-model.yml

# With an explicit architecture folder path
c5dec cpssa create-threat-model --project /path/to/project \
    --arc-folder /path/to/project/docs/specs/arc

# pytm executable Python script
c5dec cpssa create-threat-model --project /path/to/project --format pytm-python

# pytm JSON
c5dec cpssa create-threat-model --project /path/to/project --format pytm-json
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--project` | `.` (current directory) | C5-DEC SSDLC project root |
| `-o` / `--output` | depends on `--format` | Destination file |
| `--format` | `threagile` | Output format: `threagile`, `pytm-python`, `pytm-json` |
| `--arc-folder` | *(auto-discover)* | Full path to the directory containing architecture item files. When omitted the command searches for a folder named `arc`, `harc`, or `larc` (case-insensitive) with a `.doorstop.yml` file under the Doorstop specs root. A `.doorstop.yml` file is not required when the path is explicitly provided. |

**Default output file names by format:**

| Format | Default output |
|--------|---------------|
| `threagile` | `<project>/threat-model.yml` |
| `pytm-python` | `<project>/threat-model-pytm.py` |
| `pytm-json` | `<project>/threat-model-pytm.json` |

#### Threagile output

- A `title`, `date`, and `author` section pre-populated from the project.
- A `security_requirements` map (empty placeholder — populate manually after generation with the relevant security requirement identifiers and descriptions).
- A `technical_assets` map derived from architecture (ARC/HARC/LARC) Doorstop items
  (up to 40), each with `communication_links` populated from the `flows` field
  (with fallback to ARC-prefixed Doorstop links).
  IDs are Threagile-safe (lowercase, hyphens only, max 31 characters to comply
  with the Excel sheet name limit).
- Each communication link includes `protocol`, `authentication`, `authorization`,
  `vpn`, `ip_filtered`, `readonly`, `data_assets_sent`, and `data_assets_received`
  — all derived from the `flows` entries on the source ARC item.
- Threagile `protocol`, `authentication`, `authorization`, `technology`,
  `encryption`, `machine`, `size`, `confidentiality`, `integrity`, `availability`,
  `trust_boundary_type`, and `data_format` values are normalised through an
  external mapping file (`threagile-mappings.yml`).  Free-text field values on
  ARC items are mapped to Threagile-schema-compatible enumerated values
  (e.g. `OPC-UA` → `unknown-protocol`, `https` → `https`).
- `trust_boundaries` auto-populated from `zone` fields in architecture items, plus an
  internet perimeter entry.  Boundary types are mapped from zone names.
- A `data_assets` section populated from unique `data_assets` field values across
  architecture items, plus a baseline `user-data` entry when not already present.
- `threat_actors` sourced from the `threat-actors.yml` sidecar file in the ARC
  directory (see [Sidecar files](#sidecar-files-in-the-arc-directory)).
- `assumptions` sourced from the `assumptions.yml` sidecar file in the ARC directory.
- `tags_available` list auto-populated as the union of all tags used across
  assets, communication links, and trust boundaries (Threagile validates this).
- A `questions` block and abuse cases covering *Unauthorized Data Access* and
  *Denial of Service*.

**Next steps:**

1. Open `threat-model.yml` and complete all `TBD` fields.
2. Add or refine `communication_links` entries within each technical asset.
3. Run [Threagile](https://github.com/Threagile/threagile) risk analysis:
   ```sh
   docker run --rm -it -v "$(pwd):/app/work" threagile/threagile:latest \
       --model /app/work/threat-model.yml --output /app/work/output
   ```
   alternatively, you can run the threagile server and simply browse the 
   file system, load the threat model and run your analysis:
   ```sh
   docker run --rm -it -p 8080:8080 threagile/threagile -server 8080
   ```

#### pytm Python output

The generated `.py` file is a self-contained executable script. It maps each
architecture item to the correct pytm element class (`Server`, `Process`,
`Datastore`, `Actor`, `ExternalEntity`, `Lambda`) based on the item `type`
field.  Trust boundaries are created from `zone` values.  Security control
properties (`controls.isEncrypted`, `controls.hasAccessControl`,
`controls.authenticatesSource`, etc.) are set from optional architecture item fields.

**Usage after generation:**

```sh
# Generate a DFD diagram
python threat-model-pytm.py --dfd | dot -Tpng -o dfd.png

# List all identified threats
python threat-model-pytm.py --list

# Export to JSON (for risk-analysis or archival)
python threat-model-pytm.py --json threat-model-pytm.json

# Generate a threat report from a Markdown template
python threat-model-pytm.py --report docs/basic_template.md
```

#### pytm JSON output

A machine-readable JSON file containing elements, boundaries, dataflows,
abuse cases and security requirements.  Can be used as input to
`c5dec cpssa risk-analysis` for FAIR-based quantitative risk analysis.

### Step 2: generate-report

Takes a (possibly Threagile-processed) threat model YAML and renders a
structured CPSSA Markdown report ready for review or DocEngine publishing.

```sh
c5dec cpssa generate-report --model threat-model.yml -o cpssa-report.md
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--model` | `threat-model.yml` | Path to threat model YAML |
| `-o` / `--output` | `cpssa-report.md` | Destination Markdown file |

**Report structure:**

1. Executive summary
2. System description (business and technical overview)
3. Assets and dependencies (technical assets, data assets, trust boundaries)
4. Threat landscape (STRIDE categories)
   - 4.1 Threat actors and personas (from `threat-actors.yml` sidecar file)
   - 4.2 Documented assumptions (from `assumptions.yml` sidecar file)
5. Attack scenarios (from `abuse_cases` in the threat model)
6. Risk assessment table (requires manual completion)
7. Security requirements (extracted from `security_requirements` map, up to 20 displayed)
8. Recommended controls (template table)
9. Residual risk
10. Conclusion

The report is a Markdown file that can be published with [Quarto](https://quarto.org/)
via the C5-DEC DocEngine:

```sh
c5dec docengine report -n cpssa-assessment
```

### Step 3: generate-dfd

Generates a PlantUML Data Flow Diagram from Doorstop architecture (ARC/HARC/LARC)
items.  Elements are classified using the `type` field (see
[Doorstop item conventions](#doorstop-item-conventions-for-cpssa)) and grouped
into trust boundaries derived from `zone` values.
SWD items are not processed.  At most 40 architecture items are included
(same cap as `create-threat-model`).

Element IDs, asset-type classification, trust-boundary IDs, and flow labels
are all aligned with the Threagile output produced by `create-threat-model` so
that both artefacts are cross-referenceable:

- Element IDs use the Threagile-safe format (lowercase, hyphens, max 31 chars).
- Flows are labelled `flow-N [protocol / enc|no-enc / auth|no-auth]` matching
  Threagile `communication_links` keys with added encryption status and
  authentication annotations.
- Trust-boundary rectangle IDs follow the `<zone>-zone` convention.

```sh
c5dec cpssa generate-dfd --project /path/to/project -o cpssa-dfd.puml

# With an explicit architecture folder
c5dec cpssa generate-dfd --project /path/to/project \
    --arc-folder /path/to/project/docs/specs/arc
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--project` | `.` (current directory) | C5-DEC SSDLC project root |
| `-o` / `--output` | `<project>/cpssa-dfd.puml` | Destination PlantUML file |
| `--arc-folder` | *(auto-discover)* | Full path to the architecture items directory |

### Step 4: fair-input

Generates a FAIR parameters YAML template from a threat model.  The template
contains per-scenario PERT distribution placeholders for Loss Event Frequency (LEF)
and Loss Magnitude (LM) that the user should calibrate before running
`risk-analysis`.

For pytm JSON models without explicit `abuse_cases`, one scenario per element
is synthesised automatically (e.g. *"Compromise of HMI Console"*).

```sh
c5dec cpssa fair-input --model threat-model.yml -o fair-params.yml
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--model` | `threat-model.yml` | Threagile YAML **or** pytm JSON threat model |
| `-o` / `--output` | `<model_dir>/fair-params.yml` | Destination YAML |

**Template structure:**

The template exposes the **full FAIR model tree**.  Simple `lef` + `lm` inputs are
active by default; advanced decomposition nodes are included as commented-out lines
that can be uncommented to replace their parent node:

```yaml
defaults:
  lef: {low: 1, mode: 5, high: 20}
  # --- Advanced LEF decomposition (uncomment to replace lef) ---
  # tef: {low: 10, mode: 50, high: 200}
  # vulnerability: {low: 0.1, mode: 0.3, high: 0.7}
  # --- Further TEF decomposition ---
  # contact: {low: 100, mode: 500, high: 2000}
  # action: {low: 0.05, mode: 0.1, high: 0.3}
  # --- Further Vulnerability decomposition ---
  # tc: {low: 0.3, mode: 0.5, high: 0.8}
  # cs: {low: 0.2, mode: 0.4, high: 0.6}
  lm: {low: 10000, mode: 100000, high: 1000000}
  # --- Advanced LM decomposition (uncomment to replace lm) ---
  # pl: {low: 5000, mode: 50000, high: 500000}
  # sl: {low: 5000, mode: 50000, high: 500000}
  # --- Further SL decomposition ---
  # slef: {low: 0.1, mode: 0.3, high: 0.7}
  # slem: {low: 10000, mode: 50000, high: 500000}

scenarios:
  "Unauthorized Data Access":
    description: "An attacker gains unauthorized access ..."
    lef: {low: 1, mode: 5, high: 20}
    # ... (same advanced options as defaults, per-scenario)
    lm:  {low: 10000, mode: 100000, high: 1000000}
```

**Usage:**

1. Generate the template: `c5dec cpssa fair-input --model threat-model.yml`
2. Edit the file to calibrate the FAIR parameter values per scenario.
3. Run the analysis: `c5dec cpssa risk-analysis --model threat-model.yml --fair-params fair-params.yml`


### Step 5: risk-analysis (quantitative)

Runs a FAIR-based Monte Carlo simulation for each abuse case using
[pyfair](https://pypi.org/project/pyfair/).  Accepts **both** Threagile YAML
and pytm JSON threat models (auto-detected by file extension).

For pytm JSON models without explicit `abuse_cases`, the function synthesises
one scenario per element (e.g. *"Compromise of HMI Console"*).

#### FAIR calibration sources

Calibration parameters (Loss Event Frequency and Loss Magnitude PERT
distribution bounds) are resolved in the following order of precedence:

1. **Dedicated FAIR parameters file** (`--fair-params`) — a YAML file with
   per-scenario calibration.  Generate a template with
   `c5dec cpssa fair-input --model <model>`.
2. **Inline in threat model** — each abuse case value can be a dict with
   `description`, `lef` (low/mode/high), and `lm` (low/mode/high).
3. **Fallback defaults** — conservative placeholders:
   LEF `{low: 1, mode: 5, high: 20}`, LM `{low: 10000, mode: 100000, high: 1000000}`.
   A warning is emitted for each scenario using defaults.

```sh
# From a Threagile YAML
c5dec cpssa risk-analysis --model threat-model.yml -o results/

# From a pytm JSON
c5dec cpssa risk-analysis --model threat-model-pytm.json -o results/

# With calibrated FAIR parameters
c5dec cpssa risk-analysis --model threat-model.yml \
    --fair-params fair-params.yml -o results/
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--model` | `threat-model.yml` | Threagile YAML **or** pytm JSON |
| `-o` / `--output` | model parent directory | Output directory for results |
| `--simulations` | `10000` | Monte Carlo iteration count |
| `--fair-params` | *(none)* | YAML file with per-scenario FAIR calibration (see `fair-input`) |

**Outputs:**

- `cpssa-risk-summary.md` — human-readable Markdown summary with an input
  parameter table (showing all supplied FAIR nodes), per-scenario ALE
  (mean, 95th percentile, max), and a warning banner for scenarios using
  default parameters.
- `cpssa-risk-results.csv` — raw Monte Carlo results.
- `cpssa-risk-{N}.html` — one interactive pyfair report per scenario (indexed
  from 1), each comparing the individual scenario model against the
  meta-model.

---

## Doorstop item conventions for CPSSA

For `create-threat-model`, `generate-dfd` and `generate-report` to produce
meaningful output, architecture (ARC/HARC/LARC) Doorstop items **must** follow
the conventions described below.  SWD (software-design) items are not scanned
by these commands.  The water-treatment example under
`c5dec/core/cpssa/examples/water-treatment/` demonstrates all conventions.

### Architecture items (ARC / HARC / LARC)

**Mandatory fields:**

| Field | Description | Example |
|-------|-------------|---------|
| `header` | Short human-readable component name | `HMI Console` |
| `type` | Component type (see table below) | `hmi` |
| `zone` | Deployment zone | `IT`, `DMZ`, `SCADA`, `OT`, `CLOUD` |
| `text` | Free-text description of the component | multi-line block scalar |
| `links` | Doorstop UIDs this item depends on or connects to | `[ARC-006, SRS-002]` |

Links to **SRS items** express requirement coverage.  Links to **other
architecture items** express interfaces / data flows and are rendered as arrows
in the DFD and as `Dataflow` objects in the pytm model.  For explicit
control over data flows, use the `flows` field instead (see
[Data flows (`flows` field)](#data-flows-flows-field)).

**Recognised `type` values and pytm mapping:**

| `type` value(s) | pytm class | DFD kind |
|------------------|------------|----------|
| `server`, `web-server`, `app-server`, `scada-server` | `Server` | process |
| `process`, `service`, `api`, `lambda` | `Process` / `Lambda` | process |
| `plc`, `hmi`, `workstation`, `jump-server` | `Process` | process |
| `module`, `library`, `cli` | `Process` | process |
| `datastore`, `database`, `historian`, `repo` | `Datastore` | datastore |
| `actor`, `user`, `operator`, `external` | `Actor` | external |
| `firewall`, `gateway`, `rtu`, `switch`, `router` | `ExternalEntity` | external |

If `type` is absent or unrecognised, keyword heuristics on the `text` field are
used as a fallback.

**Optional fields (improve pytm and Threagile model fidelity):**

| Field | Type | pytm property | Threagile property | Notes |
|-------|------|---------------|--------------------|---------|
| `os` | string | `element.OS` | — | Operating system |
| `os_version` | string | — | — | OS version (informational) |
| `vendor` | string | — | `owner` | Hardware/software vendor |
| `model` | string | — | — | Hardware/appliance model |
| `port` | int | `element.port` | — | Primary listening port |
| `protocol` | string | `element.protocol` | — | Primary network protocol |
| `is_encrypted` | bool | `controls.isEncrypted` | `encryption` (fallback) | Data-in-transit encryption |
| `encryption` | string | — | `encryption` | Encryption scheme (mapped via `threagile-mappings.yml`) |
| `has_access_control` | bool | `controls.hasAccessControl` | `ip_filtered` (on links) | Access control enabled |
| `authenticates_source` | bool | `controls.authenticatesSource` | — | Source authentication |
| `stores_pii` | bool | `element.storesPII` | — | Datastore stores PII |
| `is_sql` | bool | `element.isSQL` | — | SQL database |
| `safety_rated` | bool | — | — | Safety-rated device (PLC/RTU) |
| `machine` | string | — | `machine` | `physical` or `virtual` (mapped) |
| `size` | string | — | `size` | Component size (mapped) |
| `confidentiality` | string | — | `confidentiality` | CIA rating (mapped) |
| `integrity` | string | — | `integrity` | CIA rating (mapped) |
| `availability` | string | — | `availability` | CIA rating (mapped) |
| `justification_cia_rating` | string | — | `justification_cia_rating` | Rationale for CIA ratings |
| `data_assets` | list | — | `data_assets_processed` | Data asset names processed by this component |
| `data_assets_stored` | list | — | `data_assets_stored` | Data asset IDs stored |
| `data_formats_accepted` | list | — | `data_formats_accepted` | Accepted data formats (mapped) |
| `internet` | bool | — | `internet` | Exposed to the internet |
| `out_of_scope` | bool | — | `out_of_scope` | Mark component as out of scope |
| `justification_out_of_scope` | string | — | `justification_out_of_scope` | Rationale for excluding |
| `multi_tenant` | bool | — | `multi_tenant` | Multi-tenant deployment |
| `redundancy` / `redundant` | bool | — | `redundant` | Redundant deployment |
| `custom_developed_parts` | bool | — | `custom_developed_parts` | Contains custom code |

**Example architecture item (`ARC-005.yml`):**

```yaml
active: true
header: HMI Console
type: hmi
zone: SCADA
text: |
  Operator HMI running Wonderware InTouch for process visualisation, alarm
  management, and manual override of pump speeds and chemical dosing rates.
  Located in the control room; access requires badge + PIN.
  Communicates with field PLCs over OPC-UA.
vendor: Schneider Electric
model: Magelis XBTGT7340
os: Windows Embedded Standard 7
port: 4840
protocol: OPC-UA
encryption: none
machine: physical
size: component
confidentiality: restricted
integrity: critical
availability: critical
justification_cia_rating: >-
  Operators issue safety-relevant commands through this console; integrity
  and availability are critical for process safety.
has_access_control: true
authenticates_source: false
links:
  - SRS-002
  - SRS-004
flows:
  - target: ARC-006
    protocol: OPC-UA
    port: 4840
    encrypted: false
    authentication: none
    authorization: none
data_assets:
  - operator-commands
  - process-displays
data_assets_stored: []
data_formats_accepted:
  - serialization
reviewed: false
```

### Data flows (`flows` field)

ARC items support an explicit `flows` field that describes outgoing data-flow
connections to other architecture items.  Each entry must have at least a
`target` key (the destination UID); all other keys are optional:

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
    data_assets_sent:
      - operator-commands
    data_assets_received:
      - process-displays
```

| Flow field | Type | Default | Description |
|------------|------|---------|-------------|
| `target` | string | *(required)* | Destination ARC item UID |
| `protocol` | string | `""` | Network protocol |
| `port` | int | `-1` | Destination port |
| `encrypted` | bool | `false` | Encrypted channel |
| `authentication` | string | `none` | Authentication mechanism |
| `authorization` | string | `none` | Authorization mechanism |
| `vpn` | bool | `false` | VPN tunnel |
| `readonly` | bool | `false` | Read-only data flow |
| `data_assets_sent` | list | `[]` | Data asset IDs sent |
| `data_assets_received` | list | `[]` | Data asset IDs received |

When `flows` is absent, the module falls back to the legacy behaviour: it reads
every entry in the Doorstop `links` field whose UID starts with an
architecture-document prefix (`ARC-`, `HARC-`, `LARC-`) and constructs a
minimal flow using the item-level `protocol` and `port` fields.  Items that
have not yet been migrated to the `flows` field continue to produce data-flow
edges automatically.

### Sidecar files in the ARC directory

Two optional YAML sidecar files can be placed alongside architecture items in
the ARC directory.  They are read by `create-threat-model` (Threagile format)
and `generate-report`, and are automatically skipped by the Doorstop item
loader.

#### `threat-actors.yml`

Defines threat actor profiles relevant to the system.  Each entry becomes a row
in the CPSSA report's "Threat actors and personas" table and is included in the
Threagile `threat_actors` section.

```yaml
threat_actors:
  - id: nation-state-apt
    name: Nation-State APT
    motivation: sabotage, espionage
    capability: high
    access: external
    description: >-
      State-sponsored actor targeting critical infrastructure.
```

| Field | Description |
|-------|-------------|
| `id` | Unique identifier |
| `name` | Human-readable name |
| `motivation` | Comma-separated motivations |
| `capability` | `low`, `medium`, or `high` |
| `access` | `external`, `internal`, or `physical` |
| `description` | Free-text profile description |

#### `assumptions.yml`

Documents security assumptions that must be verified.  Each entry appears in the
CPSSA report's "Documented assumptions" table and is included in the Threagile
`assumptions` section.

```yaml
assumptions:
  - id: ASSUM-001
    text: >-
      All remote access is routed through the jump server.
    verified: false
```

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (e.g. `ASSUM-001`) |
| `text` | Concise statement of the assumption |
| `verified` | `true` or `false` (false = open item) |

### SRS items (security requirements)

SRS items are extracted into the `security_requirements` section of the
Threagile threat model.  The first 30 active items with non-empty `text` are
included.  SRS items are **not** used for pytm formats.

**Mandatory fields:**

| Field | Description |
|-------|-------------|
| `header` | Short requirement title |
| `text` | Requirement statement |
| `links` | Upward links to MRS or parent requirements |

---

## CPSSA workflow overview

### Threagile workflow

```
C5-DEC SSDLC project
        │
        │  c5dec cpssa create-threat-model [--format threagile]
        ▼
threat-model.yml  ──► Manual completion of TBD fields
        │
        │  Threagile (optional) or manual risk analysis
        ▼
(enriched) threat-model.yml
        │
        │  c5dec cpssa generate-report
        ▼
cpssa-report.md  ──► DocEngine (Quarto) ──► cpssa-report.pdf / .html
```

### pytm workflow

```
C5-DEC SSDLC project
        │
        │  c5dec cpssa create-threat-model --format pytm-python
        ▼
threat-model-pytm.py
        │
        ├──► python threat-model-pytm.py --dfd | dot -Tpng -o dfd.png
        ├──► python threat-model-pytm.py --list          (threat list)
        ├──► python threat-model-pytm.py --json out.json (export JSON)
        │
        │  c5dec cpssa create-threat-model --format pytm-json
        ▼
threat-model-pytm.json
        │
        │  c5dec cpssa fair-input --model threat-model-pytm.json
        ▼
fair-params.yml  ──► Manual calibration of LEF/LM values
        │
        │  c5dec cpssa risk-analysis --model threat-model-pytm.json --fair-params fair-params.yml
        ▼
cpssa-risk-summary.md + cpssa-risk-results.csv
```

### Combined workflow

```
C5-DEC SSDLC project
        │
        ├──► c5dec cpssa create-threat-model                    (Threagile YAML)
        ├──► c5dec cpssa create-threat-model --format pytm-python (pytm script)
        ├──► c5dec cpssa create-threat-model --format pytm-json   (pytm JSON)
        ├──► c5dec cpssa generate-dfd                           (PlantUML DFD)
        │
        ▼
   Threat models  ──► Manual review & enrichment
        │
        ├──► c5dec cpssa generate-report --model threat-model.yml
        ├──► c5dec cpssa fair-input --model threat-model.yml      (calibration template)
        ├──► c5dec cpssa risk-analysis --model threat-model.yml --fair-params fair-params.yml
        ├──► c5dec cpssa risk-analysis --model threat-model-pytm.json
        │
        ▼
   Reports & analysis results  ──► DocEngine (Quarto)
```

---

## Related pages

| Topic | Page |
|-------|------|
| Cryptography | [Cryptography](cryptography.md) |
| SSDLC project scaffolding | [SSDLC](ssdlc.md) |
| DocEngine publishing | [SSDLC — DocEngine](ssdlc.md) |
| Common Criteria toolbox | [CCT](cct.md) |
