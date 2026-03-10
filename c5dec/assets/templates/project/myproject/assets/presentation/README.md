# C5-DEC CAD Presentation Template

A professional Quarto-based presentation template for C5-DEC CAD projects, supporting multiple output formats with ALab branding.

## Supported Formats

- **Reveal.js** (HTML slides) - ✅ Fully working, modern interactive presentations
- **PowerPoint** (PPTX) - ✅ Fully working, traditional format for editing  
- **Beamer** (PDF) - ⚠️ Known compatibility issues (see [BEAMER_NOTES.md](BEAMER_NOTES.md) for workarounds)

**Recommended**: Use **Reveal.js** for presentations and **PowerPoint** for sharing/editing.

## Prerequisites

### Containerized Development Environment (Recommended)

If you are using the C5-DEC containerized development environment in VS Code (as described in the setup documentation), you have everything you need:

- Quarto is pre-installed
- Python environment with Poetry
- All fonts (Ubuntu) are configured
- LaTeX toolchain (for Beamer PDF output)

### Local Non-Containerized Setup

For local use with your own Quarto installation:

1. **Install Quarto**: Download from [quarto.org](https://quarto.org)
2. **Install fonts**: Download and install [Ubuntu font](https://fonts.google.com/specimen/Ubuntu)
3. **Install LaTeX** (for Beamer PDF output): Install TeX Live or similar
4. **Python environment**: For pre-render scripts

## Quick Start

### 1. Activate Poetry Environment

```bash
poetry shell
```

### 2. Render Your Presentation

Choose your desired output format:

```bash
# Reveal.js HTML slides (default, recommended)
quarto render /home/alab/c5dec/c5dec/assets/presentation/index.qmd --to revealjs

# PowerPoint presentation
quarto render /home/alab/c5dec/c5dec/assets/presentation/index.qmd --to pptx

# Beamer PDF slides
quarto render /home/alab/c5dec/c5dec/assets/presentation/index.qmd --to beamer
```

Output files will be in `_output/` directory.

### 3. View Your Presentation

**Reveal.js (HTML)**:
```bash
# Open in browser
quarto preview /home/alab/c5dec/c5dec/assets/presentation/index.qmd
```

**PowerPoint**:
Open `_output/index.pptx` in Microsoft PowerPoint or compatible software

**Beamer (PDF)**:
Open `_output/index.pdf` in any PDF viewer

## Project Structure

```
presentation/
├── index.qmd                  # Main presentation file
├── _quarto.yml                # Quarto configuration
├── c5dec_config.yml           # C5-DEC metadata (title, authors, etc.)
├── _variables.yml             # Shared variables (acronyms, etc.)
├── custom-revealjs.scss       # Reveal.js theme customization
├── references.bib             # Bibliography
├── ieee.csl                   # Citation style
├── README.md                  # This file
├── CHANGELOG.md               # Version history
├── slides/                    # Presentation content
│   ├── intro.qmd              # Introduction slides
│   ├── content.qmd            # Main content slides
│   └── conclusion.qmd         # Conclusion slides
├── figs/                      # Images and logos
│   ├── Alab-logo.png
│   ├── ITR-logo.jpg
│   └── CyFORT-logo.png
├── scripts/                   # Pre-render Python scripts
│   ├── custom_vars_v2.py      # Process c5dec_config.yml
│   ├── restore_tex_files.py   # Manage LaTeX backups
│   └── requirements.txt       # Python dependencies
├── tex/                       # LaTeX customizations (Beamer)
│   ├── beamer-header.tex      # Header with colors/styles
│   └── beamer-title.tex       # Custom title slide
└── _output/                   # Generated output files
```

## Customization

### Update Metadata

Edit `c5dec_config.yml` to customize your presentation:

```yaml
presentation:
  title: "Your Presentation Title"
  subtitle: "Your Subtitle"
  author: "Your Name"
  date: "DD/MM/YYYY"
  company: "Your Organization"
  event: "Conference Name"
```

### Modify Content

1. **Edit slide files** in `slides/` directory:
   - `intro.qmd` - Opening slides
   - `content.qmd` - Main content
   - `conclusion.qmd` - Closing slides

2. **Add new slides**: Create new `.qmd` files and include them in `index.qmd`:
   ```
   {{< include slides/your-new-slides.qmd >}}
   ```

### Change Branding

1. **Replace logos** in `figs/` directory
2. **Update colors** in `custom-revealjs.scss` (Reveal.js) or `tex/beamer-header.tex` (Beamer):
   ```scss
   $alab-red: #E30613;
   $alab-light-blue: #00A8E1;
   ```

### Fonts

Change the main font in `_quarto.yml`:

```yaml
format:
  beamer:
    mainfont: "Your Font Name"
```

For Reveal.js, modify `custom-revealjs.scss`.

## Format-Specific Features

### Reveal.js Features

- **Incremental lists**: Use `::: {.incremental}` blocks
- **Fragments**: Use `::: {.fragment}` for step-by-step reveals
- **Columns**: Use `:::: {.columns}` layout
- **Speaker notes**: Use `::: {.notes}` blocks
- **Chalkboard**: Draw on slides during presentation (press 'c')
- **Navigation**: Arrow keys, or click navigation controls

### PowerPoint Features

- **Editable**: Open in PowerPoint for manual adjustments
- **Custom template**: Modify `custom-pptx-template.pptx` for master slides
- **Compatibility**: Works with Microsoft 365, LibreOffice, etc.

### Beamer (PDF) Features

- **Print-ready**: Professional PDF output
- **Custom colors**: ALab brand colors applied
- **Title page**: Branded with logos
- **Handouts**: Perfect for distribution

## Conditional Content

Show content only in specific formats:

```markdown
::::: {.content-visible when-format="revealjs"}
This appears only in HTML slides
:::::

::::: {.content-visible when-format="beamer"}
This appears only in PDF slides
:::::

::::: {.content-visible when-format="pptx"}
This appears only in PowerPoint
:::::
```

## Advanced Usage

### Render All Formats at Once

```bash
cd /home/alab/c5dec/c5dec/assets/presentation
quarto render index.qmd
```

This generates all configured formats (check `_quarto.yml` for active formats).

### Custom Output Directory

```bash
quarto render index.qmd --output-dir /path/to/output
```

### Watch Mode (Live Preview)

```bash
quarto preview index.qmd
```

Auto-reloads slides as you edit.

## Troubleshooting

### Python Script Errors

If pre-render scripts fail, ensure Poetry environment is active:

```bash
poetry shell
poetry install
```

### Beamer PDF Limitations

The current template has compatibility issues with Beamer due to advanced Reveal.js features. See [BEAMER_NOTES.md](BEAMER_NOTES.md) for:
- Detailed explanation of issues  
- Multiple workaround options
- How to create Beamer-compatible content

**For PDF output**, consider using Reveal.js PDF export (print to PDF from browser) instead.

### Font Issues

**Beamer PDF**: Install Ubuntu font or change `mainfont` in `_quarto.yml`

**Reveal.js**: Fonts are web-based, loaded from `custom-revealjs.scss`

### LaTeX Errors (Beamer)

Ensure TeX Live is installed in container or locally. Check Quarto output for specific LaTeX errors.

### PowerPoint Template Missing

The template will use default PowerPoint styling if `custom-pptx-template.pptx` is missing. Create one by:
1. Generating a basic PPTX
2. Customizing master slides in PowerPoint
3. Saving as `custom-pptx-template.pptx`

## Integration with C5-DEC Workflow

This presentation template integrates with the C5-DEC ecosystem:

- **Variables**: Reuses `_variables.yml` for consistent acronyms across documents
- **Configuration**: Uses same `c5dec_config.yml` pattern as reports
- **Scripts**: Leverages existing report scripts for metadata processing
- **Branding**: Consistent ALab/CyFORT branding with reports and ETRs

## Resources

- **Quarto Presentations**: [quarto.org/docs/presentations](https://quarto.org/docs/presentations/)
- **Reveal.js**: [revealjs.com](https://revealjs.com/)
- **C5-DEC Manual**: `/docs/manual/` directory
- **Report Template**: `c5dec/assets/report/`
- **ETR Template**: `c5dec/assets/etr/etr_template/`

## Support

For questions or issues:
- **Email**: info@abstractionslab.lu
- **Project**: CyFORT (Cloud Cybersecurity Fortress)
- **Organization**: Abstractions Lab

## License

Check the LICENSE file in the project root directory.

---

**Version**: 1.0  
**Last Updated**: 13/02/2026  
**Author**: Abstractions Lab
