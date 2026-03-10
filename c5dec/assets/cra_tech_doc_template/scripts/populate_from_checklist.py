#!/usr/bin/env python3
"""
Populate CRA Technical Documentation from CRA Checklist

This script reads the CRA checklist Doorstop document and generates
summary tables and statistics for inclusion in the technical documentation.
"""

import json
import sys
from pathlib import Path

try:
    import doorstop
    import yaml
except ImportError as e:
    print(f"Error: Required module not found: {e}", file=sys.stderr)
    print("Please install: pip install doorstop pyyaml", file=sys.stderr)
    sys.exit(1)


def load_config():
    """Load c5dec_config.yml configuration."""
    config_path = Path("c5dec_config.yml")
    if not config_path.exists():
        print("Warning: c5dec_config.yml not found, using defaults", file=sys.stderr)
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def find_cra_checklist(tree, prefix="CRAC"):
    """Find the CRA checklist document in the Doorstop tree."""
    try:
        return tree.find_document(prefix)
    except doorstop.DoorstopError:
        print(f"Warning: CRA checklist document '{prefix}' not found", file=sys.stderr)
        return None


def generate_checklist_summary(document):
    """Generate summary statistics from CRA checklist."""
    verdicts = {"pass": 0, "fail": 0, "partial": 0, "na": 0, "not_assessed": 0}
    failed_requirements = []
    
    for item in document.items:
        verdict = str(item.get('verdict', 'not_assessed'))
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        
        if verdict == "fail":
            failed_requirements.append({
                "id": item.get('cra_id', ''),
                "name": item.get('header', ''),
                "notes": item.get('notes', '')
            })
    
    total = sum(verdicts.values())
    compliance_pct = (verdicts["pass"] / total * 100) if total > 0 else 0
    
    return {
        "verdicts": verdicts,
        "total": total,
        "compliance_pct": round(compliance_pct, 1),
        "failed_requirements": failed_requirements
    }


def generate_requirements_table(document):
    """Generate markdown table of CRA requirements and verdicts."""
    lines = []
    lines.append("| CRA ID | Requirement | Verdict | Evidence |")
    lines.append("|--------|-------------|---------|----------|")
    
    for item in document.items:
        cra_id = item.get('cra_id', '')
        name = item.get('header', '')
        verdict = item.get('verdict', 'not_assessed')
        evidence = item.get('evidence', '')
        
        # Truncate long names
        if len(name) > 50:
            name = name[:47] + "..."
        
        # Truncate evidence
        if len(evidence) > 30:
            evidence = evidence[:27] + "..."
        
        lines.append(f"| {cra_id} | {name} | {verdict} | {evidence} |")
    
    return "\n".join(lines)


def write_generated_content(summary, req_table):
    """Write generated content to markdown files."""
    output_dir = Path("chapters/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write checklist summary
    with open(output_dir / "checklist-summary.md", 'w', encoding='utf-8') as f:
        f.write("## CRA Essential Requirements Compliance Summary\n\n")
        f.write(f"**Total Requirements:** {summary['total']}  \n")
        f.write(f"**Compliance Rate:** {summary['compliance_pct']}%  \n\n")
        f.write("**Verdict Breakdown:**\n\n")
        f.write(f"- ✅ Pass: {summary['verdicts']['pass']}\n")
        f.write(f"- ❌ Fail: {summary['verdicts']['fail']}\n")
        f.write(f"- ⚠️ Partial: {summary['verdicts']['partial']}\n")
        f.write(f"- N/A: {summary['verdicts']['na']}\n")
        f.write(f"- Not Assessed: {summary['verdicts']['not_assessed']}\n\n")
        
        if summary['failed_requirements']:
            f.write("### Failed Requirements\n\n")
            for req in summary['failed_requirements']:
                f.write(f"**{req['id']}** - {req['name']}\n\n")
                if req['notes']:
                    f.write(f"*Notes:* {req['notes']}\n\n")
    
    # Write requirements table
    with open(output_dir / "checklist-results.md", 'w', encoding='utf-8') as f:
        f.write(req_table)
    
    print("✓ Generated checklist summary and results table", file=sys.stderr)


def main():
    """Main pre-render script logic."""
    config = load_config()
    
    # Try to find project root (look for docs/specs directory)
    project_root = Path.cwd()
    while project_root != project_root.parent:
        if (project_root / "docs" / "specs").exists():
            break
        project_root = project_root.parent
    
    if not (project_root / "docs" / "specs").exists():
        print("Warning: Could not find Doorstop project root", file=sys.stderr)
        print("Checklist data will not be auto-populated", file=sys.stderr)
        return
    
    try:
        # Build Doorstop tree
        tree = doorstop.build(cwd=str(project_root))
        
        # Find CRA checklist
        checklist_prefix = config.get('cra', {}).get('checklist_prefix', 'CRAC')
        document = find_cra_checklist(tree, checklist_prefix)
        
        if document:
            summary = generate_checklist_summary(document)
            req_table = generate_requirements_table(document)
            write_generated_content(summary, req_table)
        else:
            print("Skipping checklist population - no data available", file=sys.stderr)
    
    except Exception as e:
        print(f"Error during checklist population: {e}", file=sys.stderr)
        print("Continuing with render...", file=sys.stderr)


if __name__ == "__main__":
    main()
