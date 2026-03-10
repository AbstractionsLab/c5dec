#!/usr/bin/env python3
"""
Generate SBOM Table for CRA Technical Documentation

This script reads the SBOM Doorstop document and generates
a markdown table for inclusion in the technical documentation.
"""

import json
import sys
from pathlib import Path

try:
    import doorstop
    import yaml
except ImportError as e:
    print(f"Error: Required module not found: {e}", file=sys.stderr)
    sys.exit(1)


def load_config():
    """Load c5dec_config.yml configuration."""
    config_path = Path("c5dec_config.yml")
    if not config_path.exists():
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def find_sbom_document(tree, product_version):
    """Find the SBOM document for the current product version."""
    # Try version-specific SBOM first
    try:
        return tree.find_document(f"SBOM-v{product_version}")
    except doorstop.DoorstopError:
        pass
    
    # Try generic SBOM
    try:
        return tree.find_document("SBOM")
    except doorstop.DoorstopError:
        print("Warning: No SBOM document found", file=sys.stderr)
        return None


def generate_sbom_table(document):
    """Generate markdown table from SBOM Doorstop items."""
    lines = []
    lines.append("| Component | Version | License | Supplier | Vulnerabilities |")
    lines.append("|-----------|---------|---------|----------|-----------------|")
    
    components = []
    for item in document.items:
        components.append({
            "name": item.get('component_name', ''),
            "version": item.get('component_version', ''),
            "license": item.get('license', ''),
            "supplier": item.get('supplier', ''),
            "vulns": len(item.get('vulnerabilities', []))
        })
    
    # Sort by component name
    components.sort(key=lambda x: x['name'].lower())
    
    for comp in components:
        vuln_text = f"{comp['vulns']} found" if comp['vulns'] > 0 else "None"
        lines.append(
            f"| {comp['name']} | {comp['version']} | {comp['license']} | "
            f"{comp['supplier']} | {vuln_text} |"
        )
    
    return "\n".join(lines)


def generate_sbom_stats(document):
    """Generate SBOM statistics."""
    total_components = len(list(document.items))
    licenses = set()
    total_vulns = 0
    
    for item in document.items:
        license_val = item.get('license', '')
        if license_val:
            licenses.add(license_val)
        vulns = item.get('vulnerabilities', [])
        total_vulns += len(vulns) if isinstance(vulns, list) else 0
    
    return {
        "total_components": total_components,
        "unique_licenses": len(licenses),
        "total_vulnerabilities": total_vulns
    }


def write_generated_sbom(table, stats):
    """Write generated SBOM content to markdown file."""
    output_dir = Path("chapters/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "sbom-table.md", 'w', encoding='utf-8') as f:
        f.write("## Component Summary\n\n")
        f.write(f"- **Total Components:** {stats['total_components']}\n")
        f.write(f"- **Unique Licenses:** {stats['unique_licenses']}\n")
        f.write(f"- **Components with Vulnerabilities:** {stats['total_vulnerabilities']}\n\n")
        f.write("## Component List\n\n")
        f.write(table)
    
    print("✓ Generated SBOM table", file=sys.stderr)


def main():
    """Main pre-render script logic."""
    config = load_config()
    
    # Try to find project root
    project_root = Path.cwd()
    while project_root != project_root.parent:
        if (project_root / "docs" / "specs").exists():
            break
        project_root = project_root.parent
    
    if not (project_root / "docs" / "specs").exists():
        print("Warning: Could not find Doorstop project root", file=sys.stderr)
        print("SBOM table will not be auto-populated", file=sys.stderr)
        return
    
    try:
        tree = doorstop.build(cwd=str(project_root))
        product_version = config.get('meta', {}).get('product', {}).get('version', '1.0.0')
        
        document = find_sbom_document(tree, product_version)
        
        if document:
            table = generate_sbom_table(document)
            stats = generate_sbom_stats(document)
            write_generated_sbom(table, stats)
        else:
            print("Skipping SBOM table generation - no data available", file=sys.stderr)
    
    except Exception as e:
        print(f"Error during SBOM table generation: {e}", file=sys.stderr)
        print("Continuing with render...", file=sys.stderr)


if __name__ == "__main__":
    main()
