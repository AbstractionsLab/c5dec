# Information Security Management System (ISMS)

The ISMS module (`c5dec/core/isms.py`) provides utilities for managing and
verifying ISMS documentation artefacts within a C5-DEC project. It contains
three main components:

- **`DocListAssistant`** — scans an ISMS folder structure and reports which
  required documents are present, incomplete, or missing.
- **`ActivityReport`** — scans a structured activity folder and generates a
  CSV summary of time-stamped events for each team member.
- **`WordTagProcessor`** — processes Microsoft Word documents (`.docx`), locates
  placeholder tags (regex-matched), and converts them into hyperlinks using a
  CSV mapping file.

---

## DocListAssistant — ISMS folder verification

`DocListAssistant` checks an ISMS folder structure against a reference
document list. It is intended to verify that all required ISMS documents
(e.g., policies, procedures, work instructions) are present.

### Usage

```python
from c5dec.core.isms import DocListAssistant

assistant = DocListAssistant()
assistant.set_path("/path/to/isms-folder")
assistant.set_reference("/path/to/reference-doc-list.csv")
assistant.scandir()
missing = assistant.get_unlisted_docs()
assistant.save_to_csv("isms-verification-report.csv")
```

> **Note**: the ISMS module is a Python API only. There is currently no dedicated
> `c5dec` CLI shortcut for ISMS folder verification. Invoke the Python classes
> directly from a script or from the Poetry shell (`poetry shell`) as shown above.

### Inputs

| Input | Description |
|-------|-------------|
| ISMS folder path | Root directory of the ISMS document collection |
| Reference CSV | List of expected documents (title, document ID, version) |

### Outputs

| Output | Description |
|--------|-------------|
| Console report | Lists present, missing, and unlisted documents |
| CSV report | Machine-readable verification result (`isms-report.csv`) |

### Sample output

```
ISMS Verification Report
========================
Present (12):  IS-POL-001, IS-POL-002, IS-PRO-001, ...
Missing  (3):  IS-PRO-007, IS-WI-002, IS-WI-005
Unlisted (1):  draft-v0.2.docx
```

---

## ActivityReport — ISMS activity log

`ActivityReport` scans a folder of timestamped activity sub-folders (produced
by a structured C5-DEC SSDLC project session) and assembles a per-user
activity CSV that can feed into time reporting or ISMS audit trails.

### Folder structure expected

```
activities/
├── 2024-01-15/
│   ├── alice/
│   │   └── session-log.md
│   └── bob/
│       └── session-log.md
├── 2024-01-16/
│   └── alice/
│       └── session-log.md
```

### Usage

```python
from c5dec.core.isms import ActivityReport

report = ActivityReport()
report.set_path("/path/to/activities")
report.scandir()
df = report.get_activity_report()
report.save_to_csv("activity-report.csv")
```

### Outputs

| Output | Description |
|--------|-------------|
| DataFrame | Rows: (date, user, event, duration) |
| CSV report | `activity-report.csv` for import into time tracking tools |

---

## WordTagProcessor — MS Word tag-to-hyperlink converter

`WordTagProcessor` opens a `.docx` file, identifies placeholder tags (e.g.,
`{REF:SRS-001}`) using a regular expression, and replaces them with styled
hyperlinks based on a CSV mapping of tag → URL.

This is useful for automatically populating cross-references and links in Word
deliverables (e.g., evaluation reports, policy documents) from a Doorstop or
external traceability dataset.

### Usage

```python
from c5dec.core.isms import WordTagProcessor

processor = WordTagProcessor()
processor.set_params(
    doc_path="report-template.docx",
    csv_path="tag-mapping.csv",
    regex_text=r"\{REF:[A-Z]+-\d+\}",
    ignore_missing_tag=True,
)
processor.convert_tags_to_hyperlinks(keep_style=False)
```

### CSV mapping format

```csv
tag,url,display_text
{REF:SRS-001},https://example.com/srs#001,SRS-001
{REF:SRS-002},https://example.com/srs#002,SRS-002
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `doc_path` | str | Path to the `.docx` file to process |
| `csv_path` | str | Path to the CSV file with tag → URL mappings |
| `regex_text` | str | Regular expression to match placeholder tags |
| `ignore_missing_tag` | bool | If `True`, silently skip tags not in the CSV |

### Outputs

The `.docx` file is modified **in place**. A backup is recommended before
processing. The method replaces each matched tag with a Word hyperlink field
using the URL and display text from the CSV mapping.

---

## Integration with Doorstop

The ISMS module is designed to complement the Doorstop-based SSDLC project
structure. For example:

1. Use `DocListAssistant` to verify that all Doorstop-linked policy documents
   are physically present in the repository.
2. Use `ActivityReport` to generate audit-trail evidence from project session
   logs for ISO/IEC 27001 Statement of Applicability (SoA) reviews.
3. Use `WordTagProcessor` to inject Doorstop UID hyperlinks into Word-based
   deliverables produced by the DocEngine.

---

## Related modules

| Module | Description |
|--------|-------------|
| `c5dec/core/pm.py` | Time report processing and timesheet consolidation |
| `c5dec/core/ssdlc.py` | SSDLC project scaffolding and management |
| `c5dec/core/transformer.py` | Document format transformation |
| `c5dec/core/sbom.py` | Software Bill of Materials management |

See also: [Project management](pm.md), [SSDLC](ssdlc.md).
