# CRA Technical Documentation Template

This directory contains the **CRA (Cyber Resilience Act) Technical Documentation** template for generating EU Regulation 2024/2847 compliant documentation using Quarto.

## Overview

The template generates technical documentation as required by:
- **CRA Article 31** - Technical documentation requirements
- **CRA Annex VII** - Content of technical documentation
- **CRA Annex V** - EU Declaration of Conformity

## Quick Start

1. **Create a new CRA technical documentation project:**
   ```bash
   c5dec docengine cra-tech-doc -n my-product
   ```

2. **Navigate to the generated project:**
   ```bash
   cd docengine/my-product
   ```

3. **Edit `c5dec_config.yml`** with your product information

4. **Render the documentation:**
   ```bash
   quarto render
   ```

## Template Structure

```
cra_tech_doc_template/
├── _quarto.yml           # Quarto configuration
├── c5dec_config.yml      # Product/manufacturer metadata
├── index.qmd             # Introduction
├── chapters/             # Documentation chapters
│   ├── 01-product-description.qmd
│   ├── 02-design-development.qmd
│   ├── 03-risk-assessment.qmd
│   ├── 04-applied-standards.qmd
│   ├── 05-eu-declaration.qmd
│   ├── 06-sbom.qmd
│   └── references.qmd
├── scripts/              # Pre-render automation
│   ├── populate_from_checklist.py
│   ├── generate_sbom_table.py
│   └── generate_doc.py
├── references.bib        # Bibliography
└── README.md             # This file
```

## Configuration

Edit `c5dec_config.yml` to customize:

- **Product Information**: Name, identifier, version, category
- **Manufacturer Details**: Name, address, contact information
- **Conformity Assessment**: Route, applied standards
- **Support Commitment**: Update period, vulnerability contact

## Workflow Integration

### 1. Create CRA Checklist

```bash
c5dec cra-checklist --create --category class_i
```

### 2. Complete Assessment

Edit checklist items in `docs/specs/CRAC/*.yml` and set verdicts.

### 3. Generate SBOM

```bash
c5dec sbom generate . -f cyclonedx -o sbom.json
c5dec sbom import sbom.json
```

### 4. Generate Documentation

```bash
c5dec docengine cra-tech-doc -n my-product
cd docengine/my-product
quarto render
```

The scripts in `scripts/` automatically pull data from your CRA checklist and SBOM to populate the documentation.

## Output Formats

The template supports multiple output formats:

- **PDF**: Professional document for submission
- **HTML**: Web-viewable documentation
- **DOCX**: Editable Microsoft Word format

## Auto-Population

The pre-render scripts automatically populate:

- **Checklist Results** (from CRA checklist Doorstop document)
- **SBOM Component List** (from SBOM Doorstop document)
- **Compliance Statistics**
- **Metadata** (from `c5dec_config.yml`)

## Customization

### Adding Content

Edit the `.qmd` files in `chapters/` to add product-specific information.

### Modifying Structure

Edit `_quarto.yml` to:
- Add/remove chapters
- Change output formats
- Add custom pre-render scripts

### Styling

- **PDF**: Customize LaTeX templates in `tex/`
- **HTML**: Modify theme in `_quarto.yml`
- **DOCX**: Update `custom-docx-format-ref.docx`

## CRA Compliance Checklist

Ensure your documentation includes:

- [ ] Product description and intended use
- [ ] Design and development information
- [ ] Cybersecurity risk assessment
- [ ] Applied harmonised standards/common specifications
- [ ] EU Declaration of Conformity (Annex V format)
- [ ] Software Bill of Materials (SBOM)
- [ ] Evidence of conformity assessment
- [ ] Support period commitment (min 5 years)
- [ ] Vulnerability disclosure policy

## Requirements

- **Quarto** (>= 1.3)
- **Python** (>= 3.8)
  - `doorstop`
  - `pyyaml`
- **LaTeX** (for PDF output)
  - LuaLaTeX recommended

## References

- [Cyber Resilience Act - Official Text](https://eur-lex.europa.eu/)
- [ENISA CRA Resources](https://www.enisa.europa.eu/)
- [Quarto Documentation](https://quarto.org/)

## Support

For issues or questions:
- **C5-DEC Documentation**: `docs/manual/cra.md`
- **Project Issues**: GitHub issues
- **Contact**: info@abstractionslab.lu
