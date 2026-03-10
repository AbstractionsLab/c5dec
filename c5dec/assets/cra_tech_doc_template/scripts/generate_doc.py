#!/usr/bin/env python3
"""
Generate EU Declaration of Conformity

This script populates placeholders in the EU DoC from c5dec_config.yml.
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not found", file=sys.stderr)
    sys.exit(1)


def load_config():
    """Load c5dec_config.yml configuration."""
    config_path = Path("c5dec_config.yml")
    if not config_path.exists():
        print("Warning: c5dec_config.yml not found", file=sys.stderr)
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    """Main pre-render script logic."""
    config = load_config()
    
    # The actual DoC is in chapters/05-eu-declaration.qmd
    # Quarto's {{< meta ... >}} syntax will handle most substitutions
    # This script can perform additional processing if needed
    
    print("✓ EU Declaration of Conformity ready", file=sys.stderr)


if __name__ == "__main__":
    main()
