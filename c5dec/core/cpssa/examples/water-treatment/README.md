# Water-treatment ICS/SCADA — CPSSA example

This self-contained example demonstrates the C5-DEC **CPSSA** (Cyber-Physical
System Security Assessment) workflow on a fictional industrial water-treatment
facility running a Purdue-model network architecture.

---

## System overview

Nine Doorstop ARC items model the major components across four network zones:

| UID | Component | Type | Zone |
|-----|-----------|------|------|
| ARC-001 | Corporate Firewall | firewall | IT |
| ARC-002 | Jump Server | jump-server | DMZ |
| ARC-003 | Engineering Workstation | workstation | IT |
| ARC-004 | Process Data Historian | historian | DMZ |
| ARC-005 | HMI Console | hmi | SCADA |
| ARC-006 | SCADA Application Server | scada-server | SCADA |
| ARC-007 | PLC Chemical Dosing | plc | OT |
| ARC-008 | PLC Pump Station | plc | OT |
| ARC-009 | RTU Sensor Gateway | rtu | OT |

---

## ARC item schema

Each YAML item file uses the following fields. All fields except `active`,
`header`, `type`, `zone`, and `text` are optional.

```yaml
active: true
header: <Human-readable component name>
type: <firewall|jump-server|workstation|historian|hmi|scada-server|plc|rtu|…>
zone: <IT|DMZ|SCADA|OT|CLOUD|…>
text: |
  <Free-text description of the component and its security relevance.>

# Vendor / asset inventory
vendor: <Vendor name>
model: <Model / product name>
os: <Operating system or firmware version>

# Network
port: <Primary service port>
protocol: <Primary application protocol, e.g. OPC-UA, Modbus TCP, SSH>
is_encrypted: <true | false>
has_access_control: <true | false>
authenticates_source: <true | false>

# Data assets processed or stored by this component.
# Each entry becomes a Threagile `data_assets` entry and is listed
# under `data_assets_processed` for this technical asset.
data_assets:
  - <asset-name-1>
  - <asset-name-2>

# Outgoing data flows to other ARC components.
# Use this field — NOT `links` — for component-to-component connectivity.
# `links` is reserved by Doorstop for upward traceability (child → parent).
flows:
  - target: <DESTINATION-UID>      # e.g. ARC-006
    protocol: <Protocol name>      # e.g. OPC-UA, SSH, Modbus TCP
    port: <Destination port>       # e.g. 4840
    encrypted: <true | false>
    authentication: <none | certificate | password | token | …>

# Doorstop upward-traceability links — SRS (or other parent doc) UIDs ONLY.
# Do NOT place ARC-to-ARC UIDs here; use `flows` instead.
links:
  - SRS-001
  - SRS-002

reviewed: false
```

### `flows` vs `links`

| Field | Purpose | Contains |
|-------|---------|---------|
| `flows` | Data-flow edges used by CPSSA to derive DFDs and threat models | ARC-to-ARC directed edges with protocol metadata |
| `links` | Doorstop upward traceability (child → parent document) | Parent-document UIDs (SRS, MRS, …) only |

Mixing ARC UIDs into `links` would cause Doorstop to attempt upward
traceability resolution against the SRS document and produce validation
warnings or errors.

---

## Sidecar files

Two optional YAML files in this directory enrich the generated threat model
with project-wide security context that does not belong to individual
component items.

### `threat-actors.yml`

Defines the threat actors and personas relevant to the system.

```yaml
threat_actors:
  - id: nation-state-apt
    name: Nation-State APT
    motivation: sabotage, espionage
    capability: high       # low | medium | high
    access: external       # external | internal | physical
    description: >
      Narrative description of the actor profile and relevance to this system.
```

### `assumptions.yml`

Documents assumptions about the environment that must be verified before
treating the threat model as accurate. Unverified assumptions are open items.

```yaml
assumptions:
  - id: ASSUM-001
    text: >
      All remote access traverses the jump server (ARC-002).
    verified: false
```

---

## End-to-end commands

Run from the repository root. Replace `<path>` with the absolute path to
this example directory.

```bash
EXAMPLE=c5dec/core/cpssa/examples/water-treatment

# Step 1 — Generate Threagile threat model YAML
poetry run c5dec cpssa create-threat-model --project $EXAMPLE

# Step 2 — Generate CPSSA Markdown report
poetry run c5dec cpssa generate-report --model $EXAMPLE/threat-model.yml

# Step 3 — Generate PlantUML Data Flow Diagram
poetry run c5dec cpssa generate-dfd --project $EXAMPLE

# Render the DFD (requires PlantUML)
java -jar plantuml.jar $EXAMPLE/cpssa-dfd.puml

# (Optional) Generate pytm Python script
poetry run c5dec cpssa create-threat-model --project $EXAMPLE --format pytm-python

# (Optional) Generate FAIR input template and run quantitative risk analysis
# (requires: pip install pyfair)
poetry run c5dec cpssa fair-input   --model $EXAMPLE/threat-model.yml
poetry run c5dec cpssa risk-analysis --model $EXAMPLE/threat-model.yml
```

---

## Data flow topology

```
[Internet]
     |
  ARC-001 Corporate Firewall (IT)
     |
  ARC-002 Jump Server (DMZ) ←── ARC-003 Engineering Workstation (IT)
     |
  ARC-004 Process Data Historian (DMZ)
     ↑
  ARC-006 SCADA Application Server (SCADA) ←── ARC-005 HMI Console (SCADA)
     ↑                   ↑
  ARC-007 PLC Dosing    ARC-008 PLC Pump (OT)
     ↑                     ↑
         ARC-009 RTU Sensor Gateway (OT)
```

Arrows represent the `flows` declared in each ARC item and map directly to
`communication_links` in the Threagile YAML and to directed arrows in the
PlantUML DFD.
