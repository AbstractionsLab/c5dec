---
active: true
derived: false
level: 7.0
links: []
normative: false
ref: ''
reviewed: SPLhH1nIG-45M312cAh31cA9TU1oGUtm5a8hLHMKVrU=
---

# CPSSA TARA integration design

This section specifies the software design of the Cyber-Physical System Security
Assessment (CPSSA) subsystem implemented in `c5dec/core/cpssa/`.

The CPSSA module bridges C5-DEC SSDLC projects with external Threat Analysis
and Risk Assessment (TARA) tooling — Threagile, OWASP pytm, and pyfair — through
five stateless integration functions.

The design is organized into the following modules:

| Sub-section | Function / area | Responsibility |
|:---|:---|:---|
| 7.1 | Doorstop ingestion helpers | Read and normalize Doorstop architecture items |
| 7.2 | Threagile mapping layer | Map Doorstop attributes to Threagile schema values |
| 7.3 | `create_threat_model()` | Generate Threagile YAML, pytm Python, or pytm JSON from ARC items |
| 7.4 | `generate_cpssa_report()` | Produce structured Markdown CPSSA report from threat model |
| 7.5 | `generate_dfd()` | Derive PlantUML Data Flow Diagram from ARC items |
| 7.6 | `generate_fair_input_template()` | Generate FAIR calibration YAML template |
| 7.7 | `run_quantitative_risk_analysis()` | FAIR-based Monte Carlo simulation via pyfair |
| 7.8 | Sidecar files and data conventions | Threat actors, assumptions, and Doorstop field conventions |
| 7.9 | CPSSA orchestration and CLI integration | CLI subcommands and end-to-end workflow |