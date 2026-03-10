"""
SBOM (Software Bill of Materials) Module

This module provides functionality for generating, managing, and tracking
SBOMs (Software Bill of Materials) using Syft and integrating them with
the Doorstop traceability system for CRA compliance.

Author: Abstractions Lab
Date: 2026-02-13
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import doorstop
import c5dec.settings as c5settings
import c5dec.common as common

# Configure logging
log = common.logger(__name__)
log.setLevel(common.logging.DEBUG)
logHandler = common.logging.FileHandler(c5settings.SBOM_LOG_FILE, mode='a')
formatter = common.logging.Formatter(
    "%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
logHandler.setFormatter(formatter)
log.addHandler(logHandler)


def check_syft_installed() -> bool:
    """
    Check if Syft is installed and available.
    
    :return: True if Syft is installed, False otherwise
    """
    import shutil
    return shutil.which("syft") is not None


def generate_sbom(
    target_path: Path,
    output_format: str = "cyclonedx-json",
    output_path: Optional[Path] = None
) -> Path:
    """
    Generate an SBOM using Syft.
    
    :param target_path: Path to analyze (directory, file, or container image)
    :param output_format: Output format (cyclonedx-json or spdx-json)
    :param output_path: Path for output file (default: sbom.json in current dir)
    :return: Path to generated SBOM file
    """
    if not check_syft_installed():
        raise common.C5decError(
            "Syft is not installed. Install from: "
            "https://github.com/anchore/syft#installation"
        )
    
    log.info(f"Generating SBOM for {target_path} in {output_format} format")
    
    # Default output path
    if output_path is None:
        output_path = Path.cwd() / "sbom.json"
    
    # Map format names
    format_map = {
        "cyclonedx": "cyclonedx-json",
        "cyclonedx-json": "cyclonedx-json",
        "spdx": "spdx-json",
        "spdx-json": "spdx-json"
    }
    syft_format = format_map.get(output_format, output_format)
    
    try:
        # Run Syft command
        cmd = [
            "syft",
            str(target_path),
            "-o", syft_format,
            "--file", str(output_path)
        ]
        
        log.debug(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.returncode == 0:
            log.info(f"SBOM generated successfully: {output_path}")
            return output_path
        else:
            raise common.C5decError(f"Syft failed: {result.stderr}")
    
    except subprocess.CalledProcessError as e:
        log.error(f"Syft command failed: {e.stderr}")
        raise common.C5decError(f"SBOM generation failed: {e.stderr}")
    except Exception as e:
        log.error(f"Error generating SBOM: {e}")
        raise common.C5decError(f"SBOM generation error: {e}")


def parse_cyclonedx_sbom(sbom_path: Path) -> Dict[str, Any]:
    """
    Parse a CycloneDX SBOM file.
    
    :param sbom_path: Path to SBOM JSON file
    :return: Parsed SBOM data structure
    """
    try:
        with open(sbom_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract components
        components = []
        for comp in data.get('components', []):
            components.append({
                'name': comp.get('name', ''),
                'version': comp.get('version', ''),
                'type': comp.get('type', ''),
                'purl': comp.get('purl', ''),
                'licenses': [lic.get('license', {}).get('id', '') 
                           for lic in comp.get('licenses', [])],
                'supplier': comp.get('supplier', {}).get('name', '') if comp.get('supplier') else '',
                'description': comp.get('description', '')
            })
        
        return {
            'format': 'CycloneDX',
            'version': data.get('specVersion', ''),
            'serial_number': data.get('serialNumber', ''),
            'timestamp': data.get('metadata', {}).get('timestamp', ''),
            'component_count': len(components),
            'components': components
        }
    
    except json.JSONDecodeError as e:
        log.error(f"Failed to parse SBOM JSON: {e}")
        raise common.C5decError(f"Invalid SBOM JSON format: {e}")
    except Exception as e:
        log.error(f"Error parsing SBOM: {e}")
        raise common.C5decError(f"SBOM parsing error: {e}")


def import_sbom_to_doorstop(
    sbom_path: Path,
    project_path: Optional[Path] = None,
    prefix: Optional[str] = None,
    version: Optional[str] = None
) -> str:
    """
    Import an SBOM into Doorstop as a document with items for each component.
    
    :param sbom_path: Path to SBOM file
    :param project_path: Path to project root (defaults to current directory)
    :param prefix: Doorstop document prefix (defaults to SBOM_PREFIX)
    :param version: Optional version suffix for prefix (e.g., "v1.0")
    :return: Path to created Doorstop document
    """
    if project_path is None:
        project_path = Path.cwd()
    
    if prefix is None:
        prefix = c5settings.CRA_SBOM_PREFIX
    
    if version:
        prefix = f"{prefix}-v{version}"
    
    log.info(f"Importing SBOM from {sbom_path} to Doorstop document {prefix}")
    
    # Parse SBOM
    sbom_data = parse_cyclonedx_sbom(sbom_path)
    
    # Create Doorstop document
    specs_path = project_path / "docs" / "specs" / prefix
    
    try:
        tree = doorstop.build(cwd=str(project_path))
        
        # Check if document exists
        try:
            document = tree.find_document(prefix)
            log.warning(f"Document {prefix} already exists, items will be added")
        except doorstop.DoorstopError:
            # Create new document
            document = tree.create_document(
                specs_path,
                prefix,
                parent=c5settings.DOORSTOP_ROOT
            )
            log.info(f"Created new Doorstop document: {prefix}")
        
        # Create index file for tracking
        index_data = {
            "DoorstopInfo": {
                "prefix": prefix,
                "parent": c5settings.DOORSTOP_ROOT,
                "created": common.get_timestamp()
            },
            "SBOMInfo": {
                "format": sbom_data['format'],
                "version": sbom_data['version'],
                "serial_number": sbom_data['serial_number'],
                "timestamp": sbom_data['timestamp'],
                "component_count": sbom_data['component_count'],
                "source_file": str(sbom_path)
            },
            "Components": {}
        }
        
        # Add components as Doorstop items
        for idx, comp in enumerate(sbom_data['components'], start=1):
            try:
                item = document.add_item()
                item.level = (idx, 0)
                item.set('header', comp['name'])
                item.set('text', comp.get('description', '') or f"Component: {comp['name']}")
                
                # Add SBOM-specific attributes
                item.set('component_name', comp['name'])
                item.set('component_version', comp['version'])
                item.set('component_type', comp['type'])
                item.set('license', ', '.join(comp['licenses']) if comp['licenses'] else '')
                item.set('supplier', comp['supplier'])
                item.set('purl', comp['purl'])
                item.set('vulnerabilities', [])  # To be populated by vulnerability scanning
                item.set('timestamp', sbom_data['timestamp'])
                
                item.save()
                
                # Add to index
                index_data["Components"][comp['name']] = {
                    "UID": item.uid,
                    "version": comp['version'],
                    "purl": comp['purl']
                }
                
                log.debug(f"Added component {comp['name']} as item {item.uid}")
            
            except Exception as e:
                log.error(f"Failed to add component {comp['name']}: {e}")
                raise
        
        # Save index file
        index_path = specs_path / "sbom_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
        log.info(f"Saved SBOM index file: {index_path}")
        
        log.info(f"Successfully imported {sbom_data['component_count']} components")
        return str(specs_path)
    
    except Exception as e:
        log.error(f"Failed to import SBOM to Doorstop: {e}")
        raise common.C5decError(f"SBOM import failed: {e}")


def compare_sboms(
    sbom1_prefix: str,
    sbom2_prefix: str,
    project_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Compare two SBOM Doorstop documents and identify differences.
    
    :param sbom1_prefix: Prefix of first SBOM document (older)
    :param sbom2_prefix: Prefix of second SBOM document (newer)
    :param project_path: Path to project root
    :return: Dictionary with added, removed, and changed components
    """
    if project_path is None:
        project_path = Path.cwd()
    
    log.info(f"Comparing SBOMs: {sbom1_prefix} vs {sbom2_prefix}")
    
    try:
        tree = doorstop.build(cwd=str(project_path))
        doc1 = tree.find_document(sbom1_prefix)
        doc2 = tree.find_document(sbom2_prefix)
        
        # Build component dictionaries
        components1 = {}
        for item in doc1.items:
            name = item.get('component_name', '')
            if name:
                components1[name] = {
                    'version': item.get('component_version', ''),
                    'purl': item.get('purl', ''),
                    'license': item.get('license', '')
                }
        
        components2 = {}
        for item in doc2.items:
            name = item.get('component_name', '')
            if name:
                components2[name] = {
                    'version': item.get('component_version', ''),
                    'purl': item.get('purl', ''),
                    'license': item.get('license', '')
                }
        
        # Compute differences
        added = {
            name: components2[name]
            for name in set(components2.keys()) - set(components1.keys())
        }
        
        removed = {
            name: components1[name]
            for name in set(components1.keys()) - set(components2.keys())
        }
        
        changed = {}
        for name in set(components1.keys()) & set(components2.keys()):
            if components1[name]['version'] != components2[name]['version']:
                changed[name] = {
                    'old_version': components1[name]['version'],
                    'new_version': components2[name]['version']
                }
        
        result = {
            'sbom1': sbom1_prefix,
            'sbom2': sbom2_prefix,
            'added': added,
            'removed': removed,
            'changed': changed,
            'summary': {
                'added_count': len(added),
                'removed_count': len(removed),
                'changed_count': len(changed)
            }
        }
        
        log.info(
            f"Comparison complete: {len(added)} added, "
            f"{len(removed)} removed, {len(changed)} changed"
        )
        
        return result
    
    except doorstop.DoorstopError as e:
        log.error(f"Doorstop error during comparison: {e}")
        raise common.C5decError(f"SBOM comparison failed: {e}")
    except Exception as e:
        log.error(f"Error comparing SBOMs: {e}")
        raise common.C5decError(f"SBOM comparison error: {e}")


def export_sbom_diff_report(diff_result: Dict[str, Any], output_path: Path) -> str:
    """
    Export SBOM comparison results to markdown report.
    
    :param diff_result: Result from compare_sboms()
    :param output_path: Path for output markdown file
    :return: Path to exported report
    """
    log.info(f"Exporting SBOM diff report to {output_path}")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# SBOM Comparison Report\n\n")
            f.write(f"**Comparison:** {diff_result['sbom1']} → {diff_result['sbom2']}\n\n")
            f.write(f"**Date:** {common.get_timestamp()}\n\n")
            
            f.write(f"## Summary\n\n")
            f.write(f"- **Added Components:** {diff_result['summary']['added_count']}\n")
            f.write(f"- **Removed Components:** {diff_result['summary']['removed_count']}\n")
            f.write(f"- **Changed Components:** {diff_result['summary']['changed_count']}\n\n")
            
            if diff_result['added']:
                f.write(f"## Added Components\n\n")
                f.write(f"| Component | Version |\n")
                f.write(f"|-----------|---------|\n")
                for name, info in sorted(diff_result['added'].items()):
                    f.write(f"| {name} | {info['version']} |\n")
                f.write(f"\n")
            
            if diff_result['removed']:
                f.write(f"## Removed Components\n\n")
                f.write(f"| Component | Version |\n")
                f.write(f"|-----------|---------|\n")
                for name, info in sorted(diff_result['removed'].items()):
                    f.write(f"| {name} | {info['version']} |\n")
                f.write(f"\n")
            
            if diff_result['changed']:
                f.write(f"## Changed Components\n\n")
                f.write(f"| Component | Old Version | New Version |\n")
                f.write(f"|-----------|-------------|-------------|\n")
                for name, info in sorted(diff_result['changed'].items()):
                    f.write(f"| {name} | {info['old_version']} | {info['new_version']} |\n")
                f.write(f"\n")
        
        log.info(f"Exported SBOM diff report: {output_path}")
        return str(output_path)
    
    except Exception as e:
        log.error(f"Failed to export SBOM diff report: {e}")
        raise common.C5decError(f"SBOM diff export failed: {e}")


def validate_sbom(
    sbom_prefix: str,
    project_path: Optional[Path] = None
) -> bool:
    """
    Validate an SBOM Doorstop document for completeness.
    
    :param sbom_prefix: Doorstop document prefix
    :param project_path: Path to project root
    :return: True if valid, raises exception otherwise
    """
    if project_path is None:
        project_path = Path.cwd()
    
    log.info(f"Validating SBOM document: {sbom_prefix}")
    
    try:
        tree = doorstop.build(cwd=str(project_path))
        document = tree.find_document(sbom_prefix)
        
        issues = []
        
        for item in document.items:
            comp_name = item.get('component_name', '')
            if not comp_name:
                issues.append(f"Item {item.uid} missing component_name")
            
            comp_version = item.get('component_version', '')
            if not comp_version:
                issues.append(f"Component {comp_name} missing version")
        
        if issues:
            log.warning(f"SBOM validation found {len(issues)} issues:")
            for issue in issues:
                log.warning(f"  - {issue}")
            return False
        
        log.info(f"SBOM validation passed: {len(list(document.items))} components")
        return True
    
    except doorstop.DoorstopError as e:
        log.error(f"Doorstop error during validation: {e}")
        raise common.C5decError(f"SBOM validation failed: {e}")
    except Exception as e:
        log.error(f"Error validating SBOM: {e}")
        raise common.C5decError(f"SBOM validation error: {e}")
