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