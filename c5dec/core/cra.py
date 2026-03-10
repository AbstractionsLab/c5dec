"""
CRA (Cyber Resilience Act) Module

This module provides functionality for CRA essential requirements checklist generation,
self-assessment, and compliance documentation following EU Regulation 2024/2847.

Author: Abstractions Lab
Date: 2026-02-13
"""

import doorstop
import json
import os
import yaml
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
import c5dec.settings as c5settings
import c5dec.common as common
import c5dec.core.transformer as c5transformer

# Configure logging
log = common.logger(__name__)
log.setLevel(common.logging.DEBUG)
logHandler = common.logging.FileHandler(c5settings.CRA_LOG_FILE, mode='a')
formatter = common.logging.Formatter(
    "%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
logHandler.setFormatter(formatter)
log.addHandler(logHandler)


class CRARequirement:
    """
    Represents a single CRA essential requirement from Annex I.
    """
    
    def __init__(self, id: str, name: str, text: str, applies_to: List[str]):
        """
        Initialize a CRA requirement.
        
        :param id: Unique identifier (e.g., "cra_i_1_1")
        :param name: Short name of the requirement
        :param text: Full requirement text
        :param applies_to: List of product categories this applies to
        """
        self.id = id
        self.name = name
        self.text = text
        self.applies_to = applies_to
        
    def __repr__(self):
        return f"CRARequirement(id={self.id}, name={self.name})"
    
    def applies_to_category(self, category: str) -> bool:
        """
        Check if this requirement applies to a specific product category.
        
        :param category: Category to check (default, class_i, class_ii, critical)
        :return: True if requirement applies to this category
        """
        return category in self.applies_to


class CRASection:
    """
    Represents a section within a CRA category (e.g., "Security by Design").
    """
    
    def __init__(self, id: str, name: str, requirements: List[CRARequirement]):
        """
        Initialize a CRA section.
        
        :param id: Section identifier
        :param name: Section name
        :param requirements: List of requirements in this section
        """
        self.id = id
        self.name = name
        self.requirements = requirements
        
    def __repr__(self):
        return f"CRASection(id={self.id}, name={self.name}, reqs={len(self.requirements)})"
    
    def get_applicable_requirements(self, category: str) -> List[CRARequirement]:
        """
        Get requirements from this section that apply to a category.
        
        :param category: Product category
        :return: List of applicable requirements
        """
        return [req for req in self.requirements if req.applies_to_category(category)]


class CRACategory:
    """
    Represents a major category (Part I or Part II) from CRA Annex I.
    """
    
    def __init__(self, id: str, name: str, description: str, sections: List[CRASection]):
        """
        Initialize a CRA category.
        
        :param id: Category identifier (part_i or part_ii)
        :param name: Category name
        :param description: Category description
        :param sections: List of sections in this category
        """
        self.id = id
        self.name = name
        self.description = description
        self.sections = sections
        
    def __repr__(self):
        return f"CRACategory(id={self.id}, name={self.name}, sections={len(self.sections)})"
    
    def get_applicable_requirements(self, category: str) -> List[CRARequirement]:
        """
        Get all requirements from this category that apply to a product category.
        
        :param category: Product category
        :return: List of applicable requirements
        """
        reqs = []
        for section in self.sections:
            reqs.extend(section.get_applicable_requirements(category))
        return reqs


class CRADatabase:
    """
    Manages the CRA requirements database, loading from YAML.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one database instance."""
        if cls._instance is None:
            cls._instance = super(CRADatabase, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the database (only once due to singleton)."""
        if self._initialized:
            return
            
        self.categories: Dict[str, CRACategory] = {}
        self.requirements_by_id: Dict[str, CRARequirement] = {}
        self.version = None
        self.regulation = None
        self._load_database()
        self._initialized = True
        
    def _load_database(self):
        """Load CRA requirements from YAML file."""
        try:
            db_path = Path(c5settings.CRA_DATABASE_PATH)
            if not db_path.exists():
                raise common.C5decError(f"CRA database not found at {db_path}")
            
            with open(db_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            self.version = data.get('version')
            self.regulation = data.get('regulation')
            log.info(f"Loading CRA database version {self.version} ({self.regulation})")
            
            # Parse categories
            categories_data = data.get('categories', {})
            for cat_key, cat_data in categories_data.items():
                sections = []
                
                # Parse sections
                for sec_data in cat_data.get('sections', []):
                    requirements = []
                    
                    # Parse requirements
                    for req_data in sec_data.get('requirements', []):
                        req = CRARequirement(
                            id=req_data['id'],
                            name=req_data['name'],
                            text=req_data['text'],
                            applies_to=req_data['applies_to']
                        )
                        requirements.append(req)
                        self.requirements_by_id[req.id] = req
                    
                    section = CRASection(
                        id=sec_data['id'],
                        name=sec_data['name'],
                        requirements=requirements
                    )
                    sections.append(section)
                
                category = CRACategory(
                    id=cat_data['id'],
                    name=cat_data['name'],
                    description=cat_data['description'],
                    sections=sections
                )
                self.categories[cat_key] = category
            
            log.info(f"Loaded {len(self.requirements_by_id)} CRA requirements")
            
        except Exception as e:
            log.error(f"Failed to load CRA database: {e}")
            raise common.C5decError(f"CRA database loading error: {e}")
    
    def get_requirement(self, req_id: str) -> Optional[CRARequirement]:
        """
        Get a requirement by its ID.
        
        :param req_id: Requirement ID
        :return: CRARequirement or None
        """
        return self.requirements_by_id.get(req_id)
    
    def get_applicable_requirements(self, category: str) -> List[CRARequirement]:
        """
        Get all requirements applicable to a product category.
        
        :param category: Product category (default, class_i, class_ii, critical)
        :return: List of applicable requirements
        """
        reqs = []
        for cat in self.categories.values():
            reqs.extend(cat.get_applicable_requirements(category))
        return reqs
    
    def get_all_requirements(self) -> List[CRARequirement]:
        """Get all requirements."""
        return list(self.requirements_by_id.values())


class CRAChecklistBuilder:
    """
    Builds CRA essential requirements checklists as Doorstop documents.
    """
    
    def __init__(self):
        """Initialize the checklist builder."""
        self.db = CRADatabase()
        log.info("CRA Checklist Builder initialized")
    
    def create_cra_checklist(
        self,
        category: str,
        project_path: Optional[Path] = None,
        prefix: Optional[str] = None
    ) -> str:
        """
        Create a CRA essential requirements checklist for a product category.
        
        :param category: Product category (default, class_i, class_ii, critical)
        :param project_path: Path to project root (defaults to current directory)
        :param prefix: Doorstop document prefix (defaults to CRA_CHECKLIST_PREFIX)
        :return: Path to created checklist document
        """
        if category not in ['default', 'class_i', 'class_ii', 'critical']:
            raise common.C5decError(
                f"Invalid CRA category: {category}. "
                "Must be one of: default, class_i, class_ii, critical"
            )
        
        if project_path is None:
            project_path = Path.cwd()
        
        if prefix is None:
            prefix = c5settings.CRA_CHECKLIST_PREFIX
        
        log.info(f"Creating CRA checklist for category '{category}' with prefix '{prefix}'")
        
        # Get applicable requirements
        requirements = self.db.get_applicable_requirements(category)
        log.info(f"Found {len(requirements)} applicable requirements for category '{category}'")
        
        # Create Doorstop document
        specs_path = project_path / "docs" / "specs" / prefix
        
        try:
            # Build tree and find or create document
            tree = doorstop.build(cwd=str(project_path))
            
            # Check if document already exists
            try:
                document = tree.find_document(prefix)
                log.warning(f"Document {prefix} already exists, will add items to it")
            except doorstop.DoorstopError:
                # Create new document
                document = tree.create_document(
                    specs_path,
                    prefix,
                    parent=c5settings.DOORSTOP_ROOT
                )
                log.info(f"Created new Doorstop document: {prefix}")
            
            # Create index tracking structure
            index_data = {
                "DoorstopInfo": {
                    "prefix": prefix,
                    "parent": c5settings.DOORSTOP_ROOT,
                    "created": common.get_timestamp()
                },
                "GeneralInfo": {
                    "cra_category": category,
                    "cra_version": self.db.version,
                    "regulation": self.db.regulation,
                    "total_requirements": len(requirements)
                },
                "Requirements": {}
            }
            
            # Add requirements as Doorstop items
            for idx, req in enumerate(requirements, start=1):
                try:
                    item = document.add_item()
                    item.level = (idx, 0)
                    item.set('header', req.name)
                    item.set('text', req.text)
                    
                    # Add CRA-specific attributes
                    item.set('cra_id', req.id)
                    item.set('verdict', 'not_assessed')  # pass, fail, partial, na, not_assessed
                    item.set('evidence', '')
                    item.set('notes', '')
                    item.set('cra_category', category)
                    
                    item.save()
                    
                    # Add to index
                    index_data["Requirements"][req.id] = {
                        "UID": str(item.uid),
                        "name": req.name,
                        "verdict": "not_assessed"
                    }
                    
                    log.debug(f"Added requirement {req.id} as item {item.uid}")
                    
                except Exception as e:
                    log.error(f"Failed to add requirement {req.id}: {e}")
                    raise
            
            # Save index file
            index_path = specs_path / "index.json"
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2)
            log.info(f"Saved index file: {index_path}")
            
            log.info(f"Successfully created CRA checklist with {len(requirements)} requirements")
            return str(specs_path)
            
        except Exception as e:
            log.error(f"Failed to create CRA checklist: {e}")
            raise common.C5decError(f"CRA checklist creation failed: {e}")
    
    def export_cra_checklist(
        self,
        checklist_prefix: str,
        output_path: Path,
        project_path: Optional[Path] = None
    ) -> str:
        """
        Export CRA checklist to Excel workbook with verdicts.
        
        :param checklist_prefix: Doorstop document prefix
        :param output_path: Path for output Excel file
        :param project_path: Path to project root
        :return: Path to exported file
        """
        if project_path is None:
            project_path = Path.cwd()
        
        log.info(f"Exporting CRA checklist '{checklist_prefix}' to {output_path}")
        
        try:
            # Build tree and get document
            tree = doorstop.build(cwd=str(project_path))
            document = tree.find_document(checklist_prefix)
            
            # Load index file
            specs_path = project_path / "docs" / "specs" / checklist_prefix
            index_path = specs_path / "index.json"
            
            if index_path.exists():
                with open(index_path, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
            else:
                log.warning(f"Index file not found at {index_path}")
                index_data = {"Requirements": {}}
            
            # Collect items data
            items_data = []
            verdicts_count = {"pass": 0, "fail": 0, "partial": 0, "na": 0, "not_assessed": 0}
            
            for item in document.items:
                try:
                    cra_id = item.get('cra_id', '')
                    verdict = item.get('verdict', 'not_assessed')
                    # Ensure verdict is a string
                    if verdict is None:
                        verdict = 'not_assessed'
                    verdict_str = str(verdict)
                    if verdict_str not in verdicts_count:
                        verdicts_count[verdict_str] = 0
                    verdicts_count[verdict_str] += 1
                    
                    items_data.append({
                        'CRA ID': cra_id,
                        'Requirement': item.get('header', ''),
                        'Text': item.get('text', ''),
                        'Verdict': verdict,
                        'Evidence': item.get('evidence', ''),
                        'Notes': item.get('notes', ''),
                        'Doorstop UID': str(item.uid)
                    })
                except Exception as e:
                    log.warning(f"Failed to process item {item.uid}: {e}")
            
            # Create DataFrame
            df_requirements = pd.DataFrame(items_data)
            
            # Create summary DataFrame
            general_info = index_data.get('GeneralInfo', {})
            summary_data = [{
                'Product Category': general_info.get('cra_category', 'unknown'),
                'CRA Version': general_info.get('cra_version', 'unknown'),
                'Total Requirements': len(items_data),
                'Pass': verdicts_count['pass'],
                'Fail': verdicts_count['fail'],
                'Partial': verdicts_count['partial'],
                'Not Applicable': verdicts_count['na'],
                'Not Assessed': verdicts_count['not_assessed'],
                'Compliance %': round(
                    (verdicts_count['pass'] / len(items_data) * 100) if len(items_data) > 0 else 0,
                    2
                )
            }]
            df_summary = pd.DataFrame(summary_data)
            
            # Write to Excel
            output_path = Path(output_path)
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df_summary.to_excel(writer, sheet_name='Summary', index=False)
                df_requirements.to_excel(writer, sheet_name='Requirements', index=False)
            
            log.info(f"Successfully exported checklist to {output_path}")
            return str(output_path)
            
        except Exception as e:
            log.error(f"Failed to export CRA checklist: {e}")
            raise common.C5decError(f"CRA checklist export failed: {e}")


def verify_sbom_exists(
    project_path: Optional[Path] = None,
    sbom_prefix: Optional[str] = None
) -> bool:
    """
    Verify if an SBOM document exists in the project (for CRA compliance).
    
    :param project_path: Path to project root
    :param sbom_prefix: SBOM document prefix (defaults to CRA_SBOM_PREFIX)
    :return: True if SBOM exists, False otherwise
    """
    if project_path is None:
        project_path = Path.cwd()
    
    if sbom_prefix is None:
        sbom_prefix = c5settings.CRA_SBOM_PREFIX
    
    try:
        tree = doorstop.build(cwd=str(project_path))
        # Try to find SBOM document (with or without version suffix)
        try:
            tree.find_document(sbom_prefix)
            return True
        except doorstop.DoorstopError:
            # Try with wildcard - check if any SBOM-* exists
            for doc in tree.documents:
                if doc.prefix.startswith(sbom_prefix):
                    return True
            return False
    except Exception as e:
        log.warning(f"Error checking for SBOM: {e}")
        return False


def link_sbom_to_cra_requirement(
    sbom_item_uid: str,
    cra_requirement_id: str,
    project_path: Optional[Path] = None
) -> bool:
    """
    Create a traceability link from an SBOM item to a CRA requirement.
    
    :param sbom_item_uid: Doorstop UID of SBOM item
    :param cra_requirement_id: CRA requirement ID (e.g., "cra_ii_1_1")
    :param project_path: Path to project root
    :return: True if link created successfully
    """
    if project_path is None:
        project_path = Path.cwd()
    
    try:
        tree = doorstop.build(cwd=str(project_path))
        
        # Find SBOM item
        sbom_item = None
        for doc in tree.documents:
            if doc.prefix.startswith(c5settings.CRA_SBOM_PREFIX):
                for item in doc.items:
                    if item.uid == sbom_item_uid:
                        sbom_item = item
                        break
                if sbom_item:
                    break
        
        if not sbom_item:
            log.error(f"SBOM item {sbom_item_uid} not found")
            return False
        
        # Find CRA checklist item with matching requirement ID
        checklist_prefix = c5settings.CRA_CHECKLIST_PREFIX
        try:
            cra_doc = tree.find_document(checklist_prefix)
            cra_item = None
            for item in cra_doc.items:
                if item.get('cra_id') == cra_requirement_id:
                    cra_item = item
                    break
            
            if not cra_item:
                log.error(f"CRA requirement {cra_requirement_id} not found in checklist")
                return False
            
            # Create link
            sbom_item.link(cra_item.uid)
            sbom_item.save()
            log.info(f"Linked SBOM item {sbom_item_uid} to CRA requirement {cra_requirement_id}")
            return True
            
        except doorstop.DoorstopError as e:
            log.error(f"CRA checklist not found: {e}")
            return False
    
    except Exception as e:
        log.error(f"Error creating traceability link: {e}")
        return False


def auto_verify_sbom_requirement(
    checklist_prefix: Optional[str] = None,
    project_path: Optional[Path] = None
) -> bool:
    """
    Automatically verify and update the SBOM-related CRA requirement
    (cra_ii_1_1) verdict based on whether SBOM exists.
    
    :param checklist_prefix: CRA checklist document prefix
    :param project_path: Path to project root
    :return: True if requirement was updated
    """
    if project_path is None:
        project_path = Path.cwd()
    
    if checklist_prefix is None:
        checklist_prefix = c5settings.CRA_CHECKLIST_PREFIX
    
    log.info("Auto-verifying CRA SBOM requirement")
    
    try:
        # Check if SBOM exists
        sbom_exists = verify_sbom_exists(project_path)
        
        # Find the SBOM requirement in checklist (cra_ii_1_1)
        tree = doorstop.build(cwd=str(project_path))
        cra_doc = tree.find_document(checklist_prefix)
        
        for item in cra_doc.items:
            if item.get('cra_id') == 'cra_ii_1_1':
                # Update verdict based on SBOM existence
                current_verdict = item.get('verdict', 'not_assessed')
                new_verdict = 'pass' if sbom_exists else 'fail'
                
                if current_verdict != new_verdict:
                    item.set('verdict', new_verdict)
                    
                    # Update evidence
                    if sbom_exists:
                        evidence_text = f"SBOM document exists in project (verified {common.get_timestamp()})"
                    else:
                        evidence_text = f"SBOM document not found (verified {common.get_timestamp()})"
                    
                    item.set('evidence', evidence_text)
                    item.save()
                    
                    log.info(f"Updated CRA requirement cra_ii_1_1 verdict: {new_verdict}")
                    return True
                else:
                    log.info(f"CRA requirement cra_ii_1_1 already has correct verdict: {current_verdict}")
                    return False
        
        log.warning("CRA requirement cra_ii_1_1 not found in checklist")
        return False
    
    except doorstop.DoorstopError as e:
        log.error(f"Error accessing Doorstop documents: {e}")
        return False
    except Exception as e:
        log.error(f"Error in auto-verification: {e}")
        return False


def get_cra_database() -> CRADatabase:
    """
    Get the CRA requirements database instance (singleton).
    
    :return: CRADatabase instance
    """
    return CRADatabase()
