# CRA (Cyber Resilience Act) Compliance Module

## Overview

The CRA module provides comprehensive support for compliance with the **EU Cyber Resilience Act** (Regulation (EU) 2024/2847), enabling manufacturers and developers to meet essential cybersecurity requirements for products with digital elements.

### Regulatory Context

The **Cyber Resilience Act (CRA)** establishes mandatory cybersecurity requirements for products with digital elements placed on the EU market. Key provisions include:

- **Article 31**: Technical Documentation Requirements
- **Annex I**: Essential Cybersecurity Requirements (Part I: Security Properties, Part II: Vulnerability Handling)
- **Annex V**: EU Declaration of Conformity
- **Annex VII**: Technical Documentation Content

C5-DEC's CRA module supports **Tier 1** compliance features for products in different risk classes:

- **Default Class**: Standard products with digital elements
- **Class I**: Products with elevated cybersecurity risks (per Article 6(1))
- **Class II**: Critical products (per Article 6(2)) - *Tier 2 feature*

## Key Features

The CRA module provides three main capabilities:

### 1. CRA Essential Requirements Checklist

Generate structured compliance checklists based on Annex I essential requirements with verdict tracking and automated verification.

**Capabilities:**
- Creates Doorstop-based traceability documents
- Supports all product risk classes (Default, Class I, Class II)
- Verdict tracking (pass/fail/na) with evidence and notes
- Automated SBOM requirement verification
- Excel export with compliance percentage calculation

### 2. CRA Technical Documentation Generator

Automated generation of CRA Annex VII-compliant technical documentation with intelligent auto-population from project artifacts.

**Capabilities:**
- Complete Quarto-based documentation template
- 7 structured chapters per Annex VII requirements
- Automatic population from checklists and SBOMs
- EU Declaration of Conformity (Annex V) generation
- Multi-format output (PDF, HTML, DOCX)

### 3. Software Bill of Materials (SBOM) Management

Comprehensive SBOM lifecycle management for CRA Annex I Part II(1) compliance (vulnerability identification and component transparency).

**Capabilities:**
- SBOM generation using Syft (CycloneDX and SPDX formats)
- Doorstop integration for traceability
- Version comparison and diff reports
- Component inventory validation
- Automatic integration with technical documentation

## Getting Started

### Prerequisites

1. **Syft Installation** (for SBOM generation):
   ```bash
   curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
   ```

2. **Quarto Installation** (for technical documentation):
   ```bash
   # See installation guide at https://quarto.org/docs/get-started/
   ```

3. **C5-DEC Project**: Initialize a C5-DEC project with Doorstop structure:
   ```bash
   c5dec new -p <project_name> -u <user_directory>
   ```

## Workflow: Complete CRA Compliance

This section demonstrates a complete workflow from project initialization to final documentation.

### Step 1: Create CRA checklist

Generate a compliance checklist for your product class:

```bash
# For default class products
c5dec cra --create --prefix CRAC

# For Class I products (elevated risk)
c5dec cra --create --prefix CRAC --category class_i
```

**Output**: Creates `docs/specs/CRAC/` directory with numbered Doorstop items, one per requirement. The `cra_id` attribute inside each item file identifies the corresponding Annex I requirement. An `index.json` maps each CRA requirement ID to its Doorstop UID.

**File structure**:
```
docs/specs/CRAC/
├── .doorstop.yml
├── index.json       # Maps cra_id → Doorstop UID
├── CRAC001.yml      # First requirement item
├── CRAC002.yml      # Second requirement item
└── ...
```

**Example item (`CRAC001.yml`)**:
```yaml
active: true
cra_category: class_i
cra_id: cra_i_1_1
evidence: ''
header: Security by default
notes: ''
text: |
  Products with digital elements shall be designed, developed and produced
  with appropriate security by default.
verdict: not_assessed
```

### Step 2: Complete checklist review

Review and document compliance for each requirement:

```bash
# Or manually edit YAML files
vim docs/specs/CRAC/CRAC001.yml
```

**Edit verdict fields** in each requirement item:
```yaml
active: true
verdict: pass  # Options: pass, fail, partial, na, not_assessed
evidence: |
  Security-by-default configuration implemented in config.yml.
  Default settings enforce:
  - TLS 1.3 minimum
  - Strong password policy (12+ chars, complexity requirements)
  - automatic security updates enabled
notes: |
  Verified through security configuration review (2026-02-15)
```

### Step 3: Generate SBOM

Create a Software Bill of Materials for your product:

```bash
# Generate SBOM from source directory
c5dec sbom generate /path/to/source -o sbom_v1.0.json -f cyclonedx

# Import into Doorstop for traceability
c5dec sbom import sbom_v1.0.json --prefix SBOM-v1.0 --version "1.0"
```

**SBOM Doorstop Structure**:
```
docs/specs/SBOM-v1.0/
├── .doorstop.yml
├── sbom_index.json           # SBOM metadata
├── SBOM-v1.0-001.yml         # Component 1
├── SBOM-v1.0-002.yml         # Component 2
└── ...
```

**Example Component Item** (`SBOM-v1.0-001.yml`):
```yaml
active: true
component_name: flask
version: 3.0.3
license: BSD-3-Clause
supplier: Pallets
purl: pkg:pypi/flask@3.0.3
description: A lightweight WSGI web application framework
```

### Step 4: Verify SBOM compliance

Automatically verify that SBOM requirement is met:

```bash
# Verify SBOM existence and update checklist
c5dec cra --verify
```

**Effect**: Finds the item with `cra_id: cra_ii_1_1` (e.g., `docs/specs/CRAC/CRAC015.yml`) and updates it:
```yaml
verdict: pass
evidence: |
  SBOM document 'SBOM-v1.0' exists in project.
  Auto-verified on 2026-02-15 10:30:00.
```

### Step 5: Export compliance report

Generate Excel compliance report with all verdicts:

```bash
c5dec cra --export cra_compliance_report.xlsx
```

**Note**: Auto-verification runs automatically before export.

**Report Structure**:
- **Sheet 1: Requirements** - All requirements with verdicts, evidence, notes
- **Sheet 2: Summary** - Compliance statistics and percentages per category

**Excel Output Example**:
| Requirement ID | Name | Category | Verdict | Evidence | Notes |
|----------------|------|----------|---------|----------|-------|
| cra_i_1_1 | Security by default | Security Properties | pass | Config enforces TLS 1.3... | Verified 2026-02-15 |
| cra_i_2_1 | Security updates | Security Properties | pass | OTA update mechanism... | Automated deployment |
| cra_ii_1_1 | SBOM maintenance | Vulnerability Handling | pass | SBOM-v1.0 exists... | Auto-verified |

### Step 6: Create technical documentation

Generate CRA Annex VII technical documentation template:

```bash
# Create from template
c5dec docengine cra-tech-doc -n cra-tech-doc

# Navigate to documentation directory
cd cra-tech-doc/

# Edit configuration
vim c5dec_config.yml
```

**Configure Product Details** (`c5dec_config.yml`):
```yaml
product:
  name: "SecureIoT Gateway"
  version: "2.1.0"
  manufacturer: "SecureTech GmbH"
  description: "Industrial IoT gateway with edge computing"
  intended_use: "Secure data aggregation and processing for industrial environments"

conformity:
  class: "Class I"  # or "Default", "Class II"
  standards:
    - "EN 303 645"
    - "IEC 62443-4-2"
  notified_body:
    name: "TÜV SÜD"
    number: "0123"

checklist_prefix: "CRAC"
sbom_prefix: "SBOM-v1.0"
```

**Edit Documentation Chapters**:
```bash
# Edit individual chapters
vim chapters/01-product-description.qmd
vim chapters/02-security-risk-assessment.qmd
vim chapters/03-essential-requirements.qmd
vim chapters/04-security-updates.qmd
vim chapters/05-vulnerability-handling.qmd
vim chapters/06-sbom.qmd
vim chapters/07-conformity-assessment.qmd
```

### Step 7: Auto-populate documentation

Pre-render scripts automatically populate content from project artifacts:

**Automatic Population Features**:
1. **Checklist Integration**: Requirement verdicts and evidence pulled into Chapter 3
2. **SBOM Tables**: Component lists generated in Chapter 6
3. **Compliance Metrics**: Pass/fail statistics calculated in Chapter 7
4. **EU Declaration**: Annex V declaration auto-filled from config

### Step 8: Render documentation

Generate final documentation in desired format:

```bash
# Render to PDF (recommended for submission)
quarto render --to pdf

# Render to HTML (for web viewing)
quarto render --to html

# Render to DOCX (for editing)
quarto render --to docx

# Output: cra-tech-doc.pdf, cra-tech-doc.html, cra-tech-doc.docx
```

### Step 9: Generate EU declaration of conformity

Include Annex V declaration in documentation:

```bash
# Already integrated in technical documentation template
# Review and customize in:
vim chapters/annexes/eu-declaration-of-conformity.qmd
```

**Output**: Annex V-compliant declaration with:
- Product identification
- Manufacturer details
- Conforming standards
- Signatory information

## CLI command reference

### `c5dec cra`

Manage CRA compliance checklists.

**Create checklist**:
```bash
c5dec cra --create [OPTIONS]

Options:
  --prefix TEXT      Doorstop prefix (default: CRAC)
  --category TEXT    Product category: default, class_i, class_ii, critical
                     (default: default)
```

**Verify SBOM compliance**:
```bash
c5dec cra --verify [--prefix TEXT]
```

**Export to Excel**:
```bash
c5dec cra --export <output_file.xlsx> [--prefix TEXT]

Example:
  c5dec cra --export reports/cra_compliance.xlsx
```

### `c5dec sbom`

SBOM lifecycle management.

**Generate SBOM**:
```bash
c5dec sbom generate <target> [OPTIONS]

Options:
  -o, --output TEXT       Output file path (default: sbom.json)
  -f, --format TEXT       Format: cyclonedx, spdx (default: cyclonedx)
  
Example:
  c5dec sbom generate /path/to/source -o sbom_v1.0.json -f cyclonedx
```

**Import to Doorstop**:
```bash
c5dec sbom import <sbom_file> [OPTIONS]

Options:
  --prefix TEXT     Doorstop prefix (e.g., SBOM-v1.0)
  --version TEXT    Version suffix appended to prefix
  
Example:
  c5dec sbom import sbom_v1.0.json --prefix SBOM-v1.0 --version "1.0"
```

**Compare SBOMs**:
```bash
c5dec sbom diff <sbom1> <sbom2> [OPTIONS]

Options:
  -o, --output TEXT    Output markdown report path
  
Example:
  c5dec sbom diff SBOM-v1.0 SBOM-v2.0 -o sbom_diff_report.md
```

**Validate SBOM**:
```bash
c5dec sbom validate <prefix>

Example:
  c5dec sbom validate SBOM-v1.0
```

### `c5dec docengine`

Generate documentation from templates (includes CRA support).

**Create CRA technical documentation**:
```bash
c5dec docengine cra-tech-doc -n <output_name>

Example:
  c5dec docengine cra-tech-doc -n cra-compliance-2026
```

## Advanced usage

### Version control for SBOMs

Track SBOM changes across product versions:

```bash
# Generate SBOM for version 1.0
c5dec sbom generate /path/to/v1.0 -o sbom_v1.0.json
c5dec sbom import sbom_v1.0.json --prefix SBOM-v1.0 --version "1.0"

# Generate SBOM for version 2.0
c5dec sbom generate /path/to/v2.0 -o sbom_v2.0.json
c5dec sbom import sbom_v2.0.json --prefix SBOM-v2.0 --version "2.0"

# Compare versions
c5dec sbom diff SBOM-v1.0 SBOM-v2.0 -o sbom_v1_to_v2_diff.md
```

**Diff Report Example**:
```markdown
# SBOM Comparison Report

**SBOM 1:** SBOM-v1.0  
**SBOM 2:** SBOM-v2.0

## Summary
- Added: 5 components
- Removed: 2 components
- Changed: 3 components

## Added Components
- **axios** (1.6.0) - MIT
- **lodash** (4.17.21) - MIT

## Changed Components
- **flask**: 2.0.0 → 3.0.3
```

### Traceability linking

Link SBOM components to CRA requirements for audit trails:

```python
from c5dec.core.cra import link_sbom_to_cra_requirement
from pathlib import Path

# Link SBOM component to requirement
link_sbom_to_cra_requirement(
    sbom_item_uid="SBOM-v1.0-042",
    cra_requirement_id="cra_ii_1_1",
    project_path=Path("/path/to/project")
)
```

**Result**: Creates Doorstop link visible in traceability reports:
```
SBOM-v1.0-042 → cra_ii_1_1 (SBOM maintenance requirement)
```

### Custom checklist categories

Create checklists filtered to a specific product risk class:

```bash
# Default class products (standard)
c5dec cra --create --prefix CRAC --category default

# Class I products (elevated risk per Article 6(1))
c5dec cra --create --prefix CRAC --category class_i

# Class II products (critical per Article 6(2))
c5dec cra --create --prefix CRAC --category class_ii

# Critical infrastructure products
c5dec cra --create --prefix CRAC --category critical
```

### Programmatic access

Use CRA module in Python scripts:

```python
from c5dec.core.cra import (
    CRADatabase, CRAChecklistBuilder,
    auto_verify_sbom_requirement, link_sbom_to_cra_requirement
)
from pathlib import Path

# Access CRA requirements database (singleton)
db = CRADatabase()
requirements = db.get_applicable_requirements("class_i")
all_reqs = db.get_all_requirements()
one_req = db.get_requirement("cra_i_1_1")

# Create checklist
builder = CRAChecklistBuilder()
checklist_path = builder.create_cra_checklist(
    category="class_i",
    project_path=Path("/path/to/project"),
    prefix="CRAC"
)

# Auto-verify SBOM requirement (cra_ii_1_1)
auto_verify_sbom_requirement(
    checklist_prefix="CRAC",
    project_path=Path("/path/to/project")
)

# Export checklist to Excel
builder.export_cra_checklist(
    checklist_prefix="CRAC",
    output_path=Path("compliance.xlsx"),
    project_path=Path("/path/to/project")
)

# Link an SBOM item to a CRA requirement
link_sbom_to_cra_requirement(
    sbom_item_uid="SBOM-v1.0-042",
    cra_requirement_id="cra_ii_1_1",
    project_path=Path("/path/to/project")
)
```

## Troubleshooting

### SBOM generation fails

**Problem**: `c5dec sbom generate` returns error "Syft not found"

**Solution**:
```bash
# Install Syft
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Verify installation
syft version

# If in Docker, rebuild container with Syft included
```

### Checklist verification fails

**Problem**: `c5dec cra --verify` reports "SBOM document not found"

**Solution**:
```bash
# List Doorstop documents to check what exists
doorstop

# If SBOM is missing, import one
c5dec sbom import sbom.json --prefix SBOM-v1.0 --version "1.0"

# Retry verification
c5dec cra --verify
```

### Documentation rendering fails

**Problem**: `quarto render` fails with missing dependencies

**Solution**:
```bash
# Install Quarto dependencies
quarto install tinytex  # For PDF output

# Check Quarto configuration
quarto check

# Try HTML output first (no LaTeX dependencies)
quarto render --to html
```

### Excel export fails

**Problem**: `c5dec cra --export` fails with "No module named 'openpyxl'"

**Solution**:
```bash
# Install openpyxl (Excel support for pandas)
poetry add openpyxl

# Retry export
c5dec cra --export compliance.xlsx
```

### Doorstop document not found

**Problem**: `DoorstopError: document 'CRAC' not found`

**Solution**:
```bash
# Verify Doorstop structure
ls -la docs/specs/

# Recreate checklist
c5dec cra --create --prefix CRAC
```

## Integration with C5-DEC features

### Common Criteria synergy

Link CRA requirements to Common Criteria SFRs:

```yaml
# In a CRA checklist item (e.g., docs/specs/CRAC/CRAC001.yml)
links:
  - SRS-042  # Security requirement
  - SFR-123  # Common Criteria SFR
  
notes: |
  This CRA requirement is satisfied by implementing CC SFR FIA_AFL.1
  (authentication failure handling) as documented in SRS-042.
```

### SSDLC integration

Connect CRA compliance to SSDLC phases:

```yaml
# Link to design phase artifacts
links:
  - ARC-015  # Architecture decision on security-by-default
  - SWD-089  # Design specification for security features
  
# Link to verification phase
links:
  - TST-234  # Security test case
  - TRB-156  # Test report
```

### Project management

Track CRA compliance tasks in project timeline:

```bash
# Convert an OpenProject export to C5-DEC time sheet format
c5dec timerep timereports.xls

# Filter CRA-specific activities in the converted output
grep "CRA" consolidated-TSH-*.xlsx
```

### Traceability matrices

Generate comprehensive traceability reports:

```bash
# Publish traceability from the specs directory
cd docs/specs && ./publish.sh

# View traceability in browser
$BROWSER docs/traceability/index.html
```

> **Note**: the `c5dec publish` CLI command is currently disabled (feature-flagged off).
> Use the `publish.sh` script in `docs/specs/` directly to publish Doorstop
> specifications to HTML and generate traceability matrices.

**Traceability Example**:
```
CRA Requirement → Security Requirement → Design → Implementation → Test
cra_i_2_1 → SRS-089 → SWD-123 → (code) → TST-456
```

---

## Configuration

CRA and SBOM module behaviour can be customised via the `cra:` and `sbom:` sections
of `c5dec/assets/c5dec_params.yml`.

### CRA section

```yaml
cra:
  # Product category: default, class_i, class_ii, critical
  category: "default"
  # Set to false to disable CRA checklist integration
  checklist_enabled: true
```

| Key | Values | Description |
|-----|--------|-------------|
| `category` | `default`, `class_i`, `class_ii`, `critical` | Controls which requirement subset is generated when `c5dec cra --create` is called without an explicit `--category` flag. The flag always takes precedence over this setting. |
| `checklist_enabled` | `true` / `false` | When `false`, checklist-related operations in the CRA workflow are skipped. |

### SBOM section

```yaml
sbom:
  format: "cyclonedx"          # cyclonedx or spdx
  include_dev_dependencies: false
```

| Key | Values | Description |
|-----|--------|-------------|
| `format` | `cyclonedx`, `spdx` | Default SBOM output format used by `c5dec sbom generate` when no `-f` flag is given. |
| `include_dev_dependencies` | `true` / `false` | When `true`, development-only dependencies are included in the generated SBOM. |

---

## Best practices

### 1. Version control for artifacts

Track all CRA artifacts in version control:

```bash
git add docs/specs/CRAC/
git add docs/specs/SBOM-v*/
git add sbom*.json
git commit -m "CRA: Update compliance checklist and SBOM for v2.1.0"
```

### 2. Regular SBOM updates

Regenerate SBOMs with each release:

```bash
# Tag SBOM with release version
c5dec sbom generate . -o sbom_v2.1.0.json
c5dec sbom import sbom_v2.1.0.json --prefix SBOM-v2.1.0 --version "2.1.0"

# Compare with previous version
c5dec sbom diff SBOM-v2.0.0 SBOM-v2.1.0 -o release_notes_v2.1.0.md
```

### 3. Periodic verification

Schedule regular compliance verification:

```bash
# Weekly verification script
#!/bin/bash
c5dec cra --verify
c5dec cra --export weekly_compliance_$(date +%Y%m%d).xlsx
c5dec sbom validate SBOM-current
```

### 4. Documentation maintenance

Keep technical documentation synchronized:

```bash
# Update documentation with each major change
c5dec docengine cra-tech-doc -n cra-tech-doc
```

### 5. Audit trail

Maintain clear evidence trails:

```yaml
# Example requirement with comprehensive evidence
active: true
verdict: pass
evidence: |
  1. Security-by-default configuration: config/defaults.yml
  2. Security test results: reports/security_tests_2026-02-15.pdf
  3. Code review: docs/reviews/security_review_2026-02-10.md
  4. External audit: reports/external_audit_TUV_2026-01-15.pdf
notes: |
  Requirement verified through:
  - Internal security testing (2026-02-15)
  - External audit by TÜV SÜD (2026-01-15)
  - Continuous monitoring via security dashboard
  
  Next review scheduled: 2026-08-15
reviewed_by: John Doe
review_date: 2026-02-15
```

## Regulatory references

- **EU Cyber Resilience Act**: [Regulation (EU) 2024/2847](https://eur-lex.europa.eu)
- **Annex I**: Essential cybersecurity requirements
- **Annex V**: EU Declaration of Conformity template
- **Annex VII**: Technical documentation content requirements
- **Article 6**: Classification of products with digital elements
- **Article 31**: Technical documentation obligations

## Additional resources

- **SBOM Standards**: [CycloneDX Specification](https://cyclonedx.org/), [SPDX Specification](https://spdx.dev/)
- **Syft Documentation**: [Anchore Syft](https://github.com/anchore/syft)
- **Quarto Documentation**: [quarto.org](https://quarto.org)
- **Common Criteria**: [CC Portal](https://www.commoncriteriaportal.org/)

## Support

For questions or issues with CRA features:

- **Email**: info@abstractionslab.lu
- **Project**: CyFORT (Cloud Cybersecurity Fortress)
- **Organization**: Abstractions Lab

---

**Document version**: 1.0  
**Last updated**: 2026-02-25  
**CRA module version**: 1.0 (Tier 1 features)
