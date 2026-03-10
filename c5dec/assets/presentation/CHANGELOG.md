# Changelog

All notable changes to the C5-DEC CAD Presentation Template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-13

### Added
- Initial release of C5-DEC presentation template
- Support for three output formats:
  - Reveal.js (HTML slides with interactive features)
  - PowerPoint (PPTX for editing)
  - Beamer (PDF for distribution)
- ALab brand color scheme and logos
- Sample presentation content demonstrating C5-DEC features
- Pre-configured Quarto project structure
- Custom Reveal.js SCSS theme with ALab branding
- LaTeX customizations for Beamer PDF output
- Python pre-render scripts (reused from report template)
- Comprehensive documentation (README.md)
- Example slides covering:
  - Introduction with logo layout
  - Key features of C5-DEC modules
  - Code examples and demonstrations
  - Traceability matrices and tables
  - Conclusion and contact information
- Format-specific content using conditional visibility
- Bibliography support with IEEE citation style
- Incremental lists and fragments for progressive reveals
- Speaker notes for Reveal.js presentations
- Responsive column layouts
- Custom commands for Common Criteria terminology

### Technical Details
- Quarto configuration with multi-format support
- Metadata system using c5dec_config.yml
- Shared variables via _variables.yml
- Symbolic links to reuse report template scripts
- Modular slide organization in slides/ directory
- Professional title slide with triple-logo layout
- Consistent color palette across all formats

---

**Maintained by**: Abstractions Lab  
**Project**: CyFORT - C5-DEC CAD  
**Contact**: info@abstractionslab.lu
