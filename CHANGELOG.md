# 1.2 (2026-03-10)

## Added

- **DocEngine CLI** (`c5dec docengine report|presentation -n <name> [-d <dest>]`): `create_docengine_template()` in the SSDLC module copies and customizes report/presentation templates with variable substitution, overwrite protection, Quarto dependency check, and `REPORT_TEMPLATE_PATH` / `PRESENTATION_TEMPLATE_PATH` constants in `c5settings.py`
- **DocEngine enhancements**: `c5dec_config_v2.yml` and `custom_vars_v2.py` pre-render script with automatic LaTeX conversion, support for string/list/dict changelog entry formats, and LaTeX escaping for special characters; Quarto presentation template (`c5dec/assets/presentation/`) with Reveal.js and PowerPoint output, ALab branding, and modular slide organization
- **`docEngine.Dockerfile`**: dedicated DocEngine dev container (Quarto, TeX Live, Kryptor, Cryptomator CLI); separate `.devcontainer/c5dec-dev/` for the lightweight C5-DEC dev container
- **CRA compliance module** (`c5dec/core/cra.py`, EU Regulation 2024/2847 Tier 1): YAML requirements database (35+ Annex I items), Doorstop-integrated checklist with pass/fail/na verdicts and Excel export, CRA Technical Documentation template (Annex VII, seven chapters), EU Declaration of Conformity generator (Annex V); `cra` CLI command (`create`, `verify`, `export`); feature flags and `c5settings.py` constants; test suite `tests/cra_checklist_test.py` (16 methods); user manual `docs/manual/cra.md`
- **SBOM lifecycle management module** (`c5dec/core/sbom.py`): Syft-based generation (CycloneDX/SPDX), parsing, validation, version diff, Doorstop traceability, and `auto_verify_sbom_requirement()` for CRA `cra_ii_1_1`; `sbom` CLI command (`generate`, `import`, `diff`, `validate`); test suite `tests/sbom_test.py` (25+ methods); user manual `docs/manual/sbom.md`
- **Native Python cryptography module** (`c5dec/core/cryptography.py`): SHA-256 file integrity, GnuPG signing/encryption, Shamir's Secret Sharing over GF(2^127−1), NaCl Ed25519 digital signatures; `c5dec crypto` CLI command with 11 subcommands (`hash`, `verify-hash`, `sign`, `verify-sig`, `encrypt`, `decrypt`, `shamir-split`, `shamir-recover`, `nacl-keygen`, `nacl-sign`, `nacl-verify`)
- **CPSSA as a multi-subsystem package** (`c5dec/core/cpssa/`): `create_threat_model()` generating Threagile-compatible YAML from Doorstop SRS/ARC artefacts with auto-discovery of architecture folders; `generate_cpssa_report()` for STRIDE-based Markdown reports; Threagile field-mapping subsystem (`threagile-mappings.yml`, `threagile-schema.json`); sidecar YAML support (`threat-actors.yml`, `assumptions.yml`); `generate_fair_input_template()` and `run_quantitative_risk_analysis()` with `--fair-params` YAML override and PERT distribution support; water-treatment worked example (`c5dec/core/cpssa/examples/water-treatment/`)
- **SpecEngine tools**: `c5graph.py` — interactive Cytoscape.js traceability graph producing a self-contained `specs-graph.html` (dagre layout, expand/collapse, color-coded coverage, offline asset inlining); `prune_bad_links.py` — removes Doorstop links with mismatched target prefix or links on root documents; `doorstop_yml_to_md.py` — migration script converting Doorstop items from pure YAML to Markdown with YAML frontmatter; `c5mermaid.py` — Mermaid diagram pre-processor that scans Doorstop `.md` item files for fenced ` ```mermaid ``` ` blocks, renders each to SVG (or PNG) via the Mermaid CLI (`mmdc`), stores the result in the item's `assets/` directory, and replaces the fenced block with an HTML comment preserving the original source plus a Markdown image reference; transformation is one-way and idempotent (content-hash-based filenames, `c5-mermaid-source` sentinel); supports `render` (default) and `undo` actions, `--dry-run`, and `--format svg|png`; integrated into `publish.sh` (render before publish, undo after); all support `--dry-run`; "Traceability Graph" entry added to `index.html` via `c5publish.py`; automatic item ID linkification in published HTML (`linkify_html_file()` / `_linkify_item_ids()`); per-column filter inputs in `c5browser.py`; section titles in `c5traceability.py` nav bar; `docs/specs/SpecEngine/README.md` and `c5traceability_config_example.yaml` added
- **Specs**: 19 new SRS items; 5 new TCS test cases; grouping items added to `swd/`, `mrs/`, and `arc/`; headings added to all TRP items; SWD-002 updated with full C5-DEC CAD class diagram in Mermaid; SWD-003 updated with Mermaid architecture overview diagram
- **Documentation**: user manuals `docs/manual/isms.md`, `docs/manual/README.md`; updated `cpssa.md`, `cryptography.md`, `ssdlc.md`
- **Project template** (`c5dec/assets/templates/project/`) synchronized with current toolchain: containers, SpecEngine toolkit, DocEngine assets, refreshed `pyproject.toml` and `poetry.lock`
- `SECURITY.md` detailing supported versions, responsible disclosure process, response timeline, scope definition
- `CONTRIBUTING.md` explaining how to set up the development environment, submit changes, and follow project conventions
- **Mermaid resize support** in `c5mermaid.py`: `--width` and `--height` flags passed to `mmdc` for SVG/PNG output dimensions
- TCS and TRP Doorstop document templates added to the project template (`c5dec/assets/templates/project/docs/specs/`); test case and test report spec documents consolidated
- **Common Criteria knowledge base**: completed CC KB (new CC pages) and revisions covering CC:2022

## Fixed

- TeX rendering issue in DocEngine templates and `cli new` command (malformed `\usepackage` argument in `_quarto.yml`)
- Broken Doorstop link format in 14 SWD items (`ARC003`/`ARC004` → `ARC-003`/`ARC-004`)
- Orphaned TCS-001–TCS-007 with empty `links: []`; all now carry SRS traceability links
- 14 SRS items with placeholder (TBD) text replaced with complete procedural descriptions
- Missing MRS upward traceability links in ARC-003 (MRS-013, MRS-024, MRS-025, MRS-046, MRS-047) and ARC-004 (MRS-040, MRS-041, MRS-044, MRS-060)
- HTML output path in `c5traceability.py` and `c5browser.py` resolved relative to script dir instead of specs dir; corrected to `SCRIPT_DIR.parent / "docs" / "publish"`
- Typos in SRS items

## Modified

- `dev.Dockerfile` and `docEngine.Dockerfile` extended with Node.js 20.x, Chromium, and Mermaid CLI (`mmdc`) for Mermaid diagram rendering in the SpecEngine pipeline
- `dev.Dockerfile` stripped of DocEngine dependencies (Quarto, TeX Live, fonts, cryptographic tools); `.devcontainer/devcontainer.json` updated to use `docEngine.Dockerfile`
- `c5dec crypto` CLI upgraded from stub to full implementation dispatching to the native cryptography module
- `c5dec cpssa` CLI extended with `fair-input` and `risk-analysis` subcommands
- `c5traceability.py`: generalized to YAML-configurable, project-agnostic Doorstop traceability analyser; added `--config`, `--discover`, `--discover-write` flags and auto-discovery of document hierarchy from `.doorstop.yml` files
- `c5browser.py`: extended to support both `.md` (Markdown frontmatter) and `.yml` (pure YAML) Doorstop item formats; document type list auto-discovered at runtime; numeric field detection for proper column sorting
- All 246 Doorstop item files in `arc`, `mrs`, `srs`, `swd`, `tra`, `trb`, `tst` converted from pure YAML to Markdown with YAML frontmatter; `.doorstop.yml` configs updated to `itemformat: markdown`
- ARC item files renamed to hyphenated format (`ARC001.yml` → `ARC-001.yml`); SWD items likewise (`SWD001.yml`–`SWD014.yml` → `SWD-001.yml`–`SWD-014.yml`)
- PlantUML schematics relocated to `docs/specs/swd/assets/PlantUML/`; obsolete `classes.puml` and `subsystems.puml` removed
- SpecEngine folder renamed from `docs/specs/c5dec-SpecEngine/` to `docs/specs/SpecEngine/`; `publish.sh` updated with linkification step, `c5graph.py` generation, and Mermaid render/undo steps
- `c5publish.py` tooling-reports block moved to `<body>` top with "Traceability Graph" link added
- DocEngine pre-render script updated from `custom_vars.py` to `custom_vars_v2.py`; default approval signatures set to placeholder (`"---"`)
- **Docker security hardening**: non-root user, dropped Linux capabilities, `--no-install-recommends`, and package pinning applied to `Dockerfile`, `dev.Dockerfile`, and `docEngine.Dockerfile`; `.dockerignore` added to limit build context
- **Unit test coverage significantly extended**: new test files for CLI (`cli_test.py`, 298 lines), ISMS (`isms_test.py`, 268 lines), SSDLC (`ssdlc_test.py`, 251 lines), Transformer (`transformer_test.py`, 176 lines), CPSSA (`cpssa_test.py`, 1175 lines), and cryptography (`cryptography_test.py`, 380 lines); existing CCT test files improved
- Mermaid SVGs pre-rendered for SWD-002 and SWD-003; stored in `docs/specs/swd/assets/`
- README, `docs/manual/README.md`, `docs/specs/README.md` 

## Removed

- DocEngine-specific dependencies from `dev.Dockerfile` (moved to `docEngine.Dockerfile`)
- `c5traceability_v2.py`; merged into `c5traceability.py`
- Stale Doorstop Bootstrap CSS/JS assets from `docs/assets/doorstop/`; replaced by CDN references
- `docs/manual/overview.md`; content merged into `docs/manual/start.md`


# 1.1 (2025-05-12)

## Added

- The open-source `organize-tool` to the `C5-DEC dev container` for automated file/folder management
- Custom workspace management (e.g., a user-defined path to directory residing outside project folder) via the C5-DEC interactive session: `c5dec.sh session <workspace>`
- Table of contents to the SSDLC manual page

## Modified

- User manual pages related to SSDLC to detail the new workspace management feature, AI-enabled design and specification for the C5-DEC method, the new `organize-tool`, and integrated the Transformer page
- README to detail the roadmap items related to including privacy-aware local GenAI models and RAG capabilities and the inclusion of verified implementations of cryptographic algorithms

## Removed

- The manual pages for the deprecated ISMS feature
- The Transformer manual page that has been moved to the SSDLC manual page

# 1.0 (2025-05-07)

Version 1.0 marks the stable release of C5-DEC.

## Added

- C5-DEC new project creation feature and command added to the CLI: `c5dec.sh new`
- C5-DEC DocEngine enhancement: new templates, automation scripts, LaTeX enhancements
- ETR evaluation spreadsheet formulas for automatic work unit verdict computation from atomic work item
- LaTeX commands for dynamic and color-coded ETR verdict encoding: pass, fail, inconclusive
- ETR evaluation overview templates, spreadsheets and compilation into Markdown for DocEngine
- Doorstop source processing code for C5-DEC keyword handling in test reports
- CPSSA, Cryptography, and Transformer commands to the CLI
- Cryptographic software to the containerized `C5-DEC cryptography dev container`: Kryptor, Cryptomator CLI
- Fully containerized DocEngine and dependencies within the `C5-DEC CAD dev container`
- OQS-OpenSSL provider container to `.devcontainer` and allow selection between C5-DEC containers
- Abstract to DocEngine report template cover pages
- Interactive session mode with the C5-DEC container accessed via `c5dec.sh session`
- Interactive session mode with the OQS-OpenSSL container for PQC accessed via `c5dec.sh pqc`
- Publish function isolation in `docs/specs`
- C5-DEC project template with placeholders used as input by the CLI `new` command
- Validation test cases (`TSS`) and test report (`TRS`) for the stable release

## Fixed

- Header and footer logo placement offset bugs in DocEngine report compilation

## Modified

- DocEngine default report and ETR layouts for the cover page
- DocEngine for ETR part generation to improve work unit and atomic work item compilation
- `_quarto.yml` files for both DocEngine report and ETR templates
- CLI command descriptions and help instructions
- User manual pages for Cryptography, CPSSA, SSDLC and Transformer
- Runner `c5dec.sh` implementation to provide new modes: `help`, `session`, `pqc`, `c5dec <command>`
- Build script `build-c5dec.sh` to also build the dev container for access via `c5dec.sh session`
- VS Code dev container configuration to include new extensions: Code Spell Checker, Quarto, Jupyter and Data Wrangler

## Removed

- All CLI commands for SSDLC (all have been integrated into the `new` CLI command)
- TUI menus of features migrated to the CLI: SSDLC, CPSSA, Cryptography, Transformer

# 0.3.1 (2024-09-16)

## Added

- A check to the RMT consolidation algorithm to skip invalid file extensions

## Fixed

- The software version in the project TOML

## Modified

- The README to add the C5-DEC (beta) logo

# 0.3 (2024-09-15)

## Added

- A resource management tool (RMT) and cost report computation feature to the project management (PM) module
- A dedicated RMT analysis spreadsheet for obtaining a quick overview: `c5dec/assets/costrep/c5dec-rmt-analysis.xlsx`
- A new command to the CLI for running the cost report computation feature
- RMT parameterization file (`rmt-params.xlsx`) to the `c5dec/assets/tshparams` folder
- An example time sheet input file (`tsh.xlsx`) to the `c5dec/input` folder
- Automation code to the Quarto-based C5-DEC DocEngine for generating Quarto tables from spreadsheets
- Unit tests for the time report assistant component of the PM module
- A unit test suite runner shell script
- A user manual section to the PM page describing the RMT cost report feature
- New software design schematics related to the CCT module

## Fixed

- Deployment scripts bug not allowing modification of specs: docs volume mapping
- Settings module to fix a bug preventing unit test suites to run (relative path)
- Time report assistant unit tests to compute the correct path

## Modified

- Project resource management tool (RMT) module behavior so it always picks up input files/folders from the `c5dec/input` folder
- RMT CLI commands and TUI mini apps accordingly to use the new input retrieval mechanism
- Deployment scripts to improve customization
- Updated the technical specifications and traceability HTML publication following the inclusion of previously missing SWD items

# 0.2 (2024-07-19)

## Added

- Support for parsing Common Criteria 2022 release (CC2022R1)
- Dedicated object-oriented data structures to the CCT module to handle CC 2022
- Graphical user interface (GUI) in the form of a web application
- GUIs for the CCT browser and CC evaluation laboratory submodules
- C5-DEC DocEngine publishing feature based on Quarto for both generic report and ETR generation
- Dedicated data structures and algorithms for handling evaluation checklist creation in a structured format, e.g., csv and spreadsheets
- Feature to create CEM evaluation checklist spreadsheets that can be parsed by the DocEngine (exposed via both the CLI and the GUI)
- Dedicated C5-DEC publish function exposed via the CLI as a wrapper, complementing and improving the underlying Doorstop-based mechanism to publish technical specifications in HTML and Markdown
- Docker-based deployment solution for end-users, along with build and executable scripts
- test reports to the technical specifications (`tra` and `trb` under `docs`).

## Fixed

- Bugs in the CCT module, largely rooted in inconsistent data structure tracking and life cycle management, e.g., CC XML tree loaded several times
- Bugs in the CLI checklist creation function
- Errors in the technical specifications encodings, now stored under `docs/specs`

## Modified

- The CCT module to add support for setting parameters for the ETR CLI handler and CC release selection via user-accessible YAML configuration file
- Heavily refactored and improved the CCT module, e.g., use of constants to handle paths, folders, use of `os.path.join` to ensure cross-platform path management
- The specifications folder name (`reqs` to `specs`)
- Dev container Docker file to include `pipx`, git repo creation and `poetry` installation
- technical specifications under the `docs` folder to update all schematics, requirements and test cases

## Deleted

- Rendered schematics stored under `docs/sdd/images`

# 0.1 (2023-12-01)

- Initial release of C5-DEC CAD