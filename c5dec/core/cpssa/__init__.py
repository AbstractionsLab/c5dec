"""
C5-DEC CAD — Cyber-Physical System Security Assessment (CPSSA) package.

"""

# Re-export cpssa public API so ``from c5dec.core.cpssa import …`` still works.
from c5dec.core.cpssa.cpssa import (  # noqa: F401
    create_threat_model,
    generate_cpssa_report,
    generate_dfd,
    generate_fair_input_template,
    run_quantitative_risk_analysis,
)

__all__ = [
    # cpssa
    "create_threat_model",
    "generate_cpssa_report",
    "generate_dfd",
    "parse_adtool_xml",
    "generate_fair_input_template",
    "run_quantitative_risk_analysis",
]
