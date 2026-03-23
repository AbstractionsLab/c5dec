# C5-DEC CAD documentation

This directory contains all documentation for the C5-DEC CAD (Common Criteria for Cybersecurity, Cryptography, Clouds – Design, Evaluation and Certification, Computer-Aided Design) project, organized into distinct categories to support different audiences and purposes.

See our [technical specification traceability web site](https://abstractionslab.github.io/c5dec/traceability/index.html) for a live view of the [full specification](./specs/README.md) tree and traceability coverage, produced by the C5-DEC [SpecEngine](./specs/SpecEngine/README.md).

## Documentation structure

### `manual/` - User and developer manuals

**Audience**: End users, system administrators, and developers

**Purpose**: Practical, task-oriented documentation explaining **HOW** to use, configure, and operate the system.

**Contents**:
- `README.md` - C5-DEC CAD user manual index, overview, and goals
- `installation.md` - Installation instructions and workspace setup
- `start.md` - Quick start guide
- `cct.md` - Common Criteria Toolbox user guide
- `ssdlc.md` - Secure SDLC and Transformer documentation
- `pm.md` - Project and resource management
- `cpssa.md` - Cyber-Physical System Security Assessment
- `cra.md` - Cyber Resilience Act guidance
- `cryptography.md` - Classical and post-quantum cryptography
- `troubleshooting.md` - Common issues and solutions
- `_figures/` - Images and diagrams for manual documentation

**Characteristics**:
- Narrative, tutorial-style writing
- Step-by-step procedures
- Complete configuration examples
- Frequently updated, living documentation
- Code examples and CLI references

### `specs/` - Requirements and specifications (Doorstop)

**Audience**: System architects, requirements engineers, QA teams, auditors

**Purpose**: Formal, traceable requirements and design decisions defining **WHAT** and **WHY**.

**Contents**:
- `mrs/` - Mission Requirements Specifications (root)
- `srs/` - Software/System Requirements Specifications
- `arc/` - Architecture specifications
- `swd/` - Software Design specifications
- `tcs/` - Test case specifications
- `trp/` - Test reports
- `SpecEngine/c5publish.py` - Custom Doorstop publisher with Bootstrap CSS
- `SpecEngine/c5-keyword.py` - Keyword preprocessor/postprocessor
- `SpecEngine/c5traceability.py` - Configurable coverage statistics analyser
- `SpecEngine/c5traceability_config.yaml` - YAML configuration for coverage checks and document order
- `SpecEngine/c5browser.py` - Interactive HTML browser generator
- `SpecEngine/c5fingerprint.py` - Dependency content fingerprinting for items with `references:` file paths; flags stale items when source files change
- `publish.sh` - Publishing orchestration script

**Characteristics**:
- Formal, structured format (Doorstop YAML frontmatter)
- Focus on acceptance criteria and rationale
- Primarily diagrams, decisions, constraints
- Upward traceability links (child → parent)
- Version-controlled with reviews/approval metadata

### `traceability/` - Published requirements traceability

**Audience**: Stakeholders, auditors, project managers

**Purpose**: Generated HTML documentation showing full requirements traceability matrix.

**Contents**:
- `index.html` - Traceability matrix home page
- `MRS.html`, `SRS.html`, `ARC.html`, `SWD.html`, etc. - Published requirement documents
- `traceability.csv` - Machine-readable traceability export
- `template/` - HTML templates for publishing
- `assets/` - Supporting files for published HTML (CSS, JS)

**Generation**: Run `cd docs/specs && ./publish.sh` to regenerate from Doorstop sources.

---

## Maintaining balance: specs vs. manual

The project uses a clear separation of concerns to avoid content duplication and minimize maintenance burden:

### Separation of concerns

| Aspect | `specs/` (Doorstop) | `manual/` |
|--------|---------------------|-----------|
| **Focus** | WHAT and WHY | HOW |
| **Content** | Requirements, acceptance criteria, design rationale | Setup guides, usage tutorials, configuration references |
| **Audience** | Architects, QA, auditors | Users, operators, developers |
| **Format** | Formal Doorstop documents | Narrative tutorials |
| **Stability** | Versioned, reviewed, formally approved | Living documentation, frequently updated |

### Content ownership matrix

| Content type | Owner | Example |
|-------------|-------|---------|
| User stories | Specs (SRS) | "As a CC evaluator, I want..." |
| Acceptance criteria | Specs (SRS) | "System shall load CC SFR database..." |
| Design rationale | Specs (ARC) | "Selected modular architecture due to..." |
| Architecture diagrams | Specs (ARC) + Schematics | Component relationship diagrams |
| CLI syntax | Manual | `poetry run c5dec cct --filter...` |
| Configuration options | Manual | Field-by-field YAML reference |
| Installation steps | Manual | Numbered procedures |
| Troubleshooting | Manual | Error messages and solutions |
| Code examples | Manual | Complete working examples |
| API documentation | Manual | Function signatures, parameters |