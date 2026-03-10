# C5-DEC CAD user manual

Welcome to the C5-DEC CAD (Computer-Aided Design) user manual. This guide covers the full feature set of C5-DEC CAD, a comprehensive suite of AI-enabled tools for secure system design and development following the Common Criteria standards, SSDLC methodologies, and cyber-physical system security assessment.

## What is C5-DEC CAD?

C5-DEC, short for **Common Criteria for Cybersecurity, Cryptography, Clouds – Design, Evaluation and Certification**, is a sub-project of the [CyFORT](https://abstractionslab.com/index.php/research-and-development/cyfort/) project ("Cloud Cybersecurity Fortress of Open Resources and Tools for Resilience"). It combines a software component with a structured knowledge base to provide a coherent set of tools supporting:

- **CC certification** (Common Criteria / ISO/IEC 15408 & ISO/IEC 18045)
- **Secure software development life cycle (SSDLC)** with full artifact traceability, browsing and statistics
- **Cyber Resilience Act (CRA)** features for facilitating your security efforts towards CRA compliance, e.g. SBOM
- **Cyber-physical system security assessment (CPSSA)**
- **Project and resource management**
- **Cryptographic operations** including post-quantum cryptography

C5-DEC CAD is designed around open data formats (Markdown, YAML, JSON, CSV, LaTeX) and integrates with widely used open-source tools such as Doorstop, Quarto, OpenProject, GitLab, OWASP pytm, threagile, and OpenSSL.

The **CCT** makes CC certification and evaluation (ISO/IEC 15408 / ISO/IEC 18045) more accessible by providing a comprehensive CC database, a browser for navigating SFRs and SARs, and tools for creating and tracking evaluation checklists. The **SSDLC** module supports the full development life cycle — requirements, architecture, design, test specifications, and reports — in a single repository with complete traceability. Both modules are backed by the CPSSA methodology and tools module. For cryptographic operations, C5-DEC provides a few commands for commonly used operations (hashing and comparison, payload signature and verification) and also integrates `Kryptor`, `GnuPG`, and `Cryptomator` for classical cryptography into its deployment container, and an `OQS-OpenSSL provider` container for post-quantum cryptography; see the [Cryptography](./cryptography.md) page for details.

## How to use this manual

If you are new to C5-DEC CAD, follow the **getting started path** below in order. Returning users can jump directly to the module reference section.

### Getting started path

| Step | Page | Description |
|------|------|-------------|
| 1 | [Installation](./installation.md) | Deploy C5-DEC CAD via Docker scripts or as a VS Code dev container |
| 2 | [Workspace setup](./installation.md#workspace-setup) | Initialize the git repository and activate the Poetry environment |
| 3 | [Quick start](./start.md) | Launch the CLI, TUI, and GUI; run your first commands |

### Module reference

Once installed and running, consult the relevant module page for detailed usage guidance:

| Module | Page | Summary |
|--------|------|---------|
| **CCT** | [Common Criteria Toolbox](./cct.md) | Browse the CC database, create evaluation checklists, navigate SFRs and SARs |
| **SSDLC** | [Secure software development life cycle](./ssdlc.md) | Manage requirements, architecture, design and test artifacts with full traceability; use the Transformer and DocEngine |
| **PM** | [Project resource management](./pm.md) | Convert and process OpenProject time report exports |
| **CPSSA** | [Cyber-physical system security assessment](./cpssa.md) | Threat modelling (Threagile), STRIDE reporting, PlantUML DFD generation, and FAIR-based quantitative risk analysis |
| **Cryptography** | [Cryptography](./cryptography.md) | Classical and post-quantum cryptographic operations via CLI or OQS-OpenSSL container |
| **ISMS** | [Information security management system](./isms.md) | Verify ISMS documentation completeness and generate activity reports |
| **SBOM** | [Software Bill of Materials](./sbom.md) | Generate, import, diff and validate SBOMs in CycloneDX and SPDX formats |
| **CRA** | [CRA compliance module](./cra.md) | Cyber Resilience Act compliance checklists, technical documentation and SBOM integration |
| **Troubleshooting** | [Troubleshooting](./troubleshooting.md) | Common issues and solutions for installation, containers, Doorstop, and the GUI |

## Interfaces

C5-DEC CAD exposes three interfaces:

- **CLI** (command line interface) — primary interface; run `./c5dec.sh` or `c5dec -h` for usage
- **TUI** (textual user interface) — interactive terminal UI; launch with `./c5dec.sh -t`
- **GUI** (web-based graphical user interface) — browser-based at `localhost:5432`; launch with `./c5dec.sh -g`

See the [quick start](./start.md) page for the full list of runner options including interactive session mode (`c5dec.sh session`) and the post-quantum cryptography entrypoint (`c5dec.sh pqc`).

## Deployment options

| Option | Description | Best for |
|--------|-------------|----------|
| Docker + shell scripts | Build with `./build-c5dec.sh`, run with `./c5dec.sh` | CCT and PM features, lightweight usage |
| VS Code dev container | Open project in container via Dev Containers extension | SSDLC, DocEngine, Transformer, advanced development |

See the [installation](./installation.md) page for step-by-step instructions for both options.

## Knowledge base

In addition to the software modules, C5-DEC includes a structured knowledge base:

- **SSDLC and CPSSA methodology reports**: available via the [C5-DEC GitHub repository](/README.md#knowledge-base)
- **CC wiki**: `c5dec/assets/database/KnowledgeBase/` — navigable map of Common Criteria concepts
- **Security controls**: `c5dec/assets/database/SecurityControls/`
