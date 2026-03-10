# CLI design is based on that of Doorstop

import argparse
import os
import sys
import doorstop

from c5dec import common, settings
from c5dec.frontend.cli import commands
from c5dec.frontend.cli import utils

log = common.logger(__name__)


def run(args=None):
    """Process command-line arguments and run the program."""
    from c5dec import CLI, DESCRIPTION, VERSION

    # Shared options
    project = argparse.ArgumentParser(add_help=False)
    try:
        root = doorstop.builder.vcs.find_root(os.getcwd())
    except doorstop.common.DoorstopError:
        root = None
    project.add_argument(
        "-j",
        "--project",
        metavar="PATH",
        help="set path to project root",
        default=root,
    )
    settings.PROJECT_ROOT = root

    debug = argparse.ArgumentParser(add_help=False)
    debug.add_argument("-V", "--version", action="version", version=VERSION)
    group = debug.add_mutually_exclusive_group()
    group.add_argument(
        "-v", "--verbose", action="count", default=0, help="enable verbose logging"
    )

    shared = {
        "formatter_class": common.HelpFormatter,
        "parents": [project, debug],
    }

    # Build main parser
    parser = argparse.ArgumentParser(
        prog=CLI, description=DESCRIPTION, **shared)
    
    parser.add_argument(
        "-t",
        "--tui",
        action="store_true",
        default=True,
        help="run textual user interface (TUI)",
    )

    parser.add_argument(
        "-g",
        "--gui",
        action="store_true",
        default=False,
        help="run graphical user interface (GUI)",
    )
    
    # Build sub-parsers
    subs = parser.add_subparsers(help="", dest="command", metavar="<command>")
    _new(subs)
    _docengine(subs)
    _timerep(subs)
    _consolidate(subs)
    _costrep(subs)
    _retrieveattr(subs)
    _view(subs)
    _validate(subs)
    _checklist(subs)
    _export(subs)
    _etr(subs)
    _cra_checklist(subs)
    _sbom(subs)
    _publish(subs)
    _transform(subs)
    _cpssa(subs)
    _cryptography(subs)

    # Parse arguments
    args = parser.parse_args(args=args)

    # Configure logging
    utils.configure_logging(args.verbose)

     # Run the program
    function = commands.get(args.command)
    try:
        success = function(args, os.getcwd(), parser.error)
    except common.C5decError as exc:
        log.error(exc)
        success = False
    except KeyboardInterrupt:
        log.debug("command cancelled")
        success = False
    if success:
        log.debug("command succeeded")
    else:
        log.debug("command failed")
        sys.exit(1)

common.feature_flag("ON")
def _new(subs):
    info = "ssdlc - create new C5-DEC project with containerization, scripts, templates and configuration"
    sub = subs.add_parser(
        "new", description=info.capitalize() + ".", help=info
    )
    sub.add_argument("-p", "--project", help="New project name", default="myproject")
    sub.add_argument("-u", "--user", help="Username in the Dockerized GNU/Linux environment", default="user")

@common.feature_flag("ON")
def _docengine(subs):
    info = "docengine - create new DocEngine report, presentation, or CRA technical documentation template"
    sub = subs.add_parser(
        "docengine", description=info.capitalize() + ".", help=info
    )
    sub.add_argument("template_type", choices=["report", "presentation", "cra-tech-doc"], 
                     help="Type of template to create")
    sub.add_argument("-n", "--name", required=True, 
                     help="Name of the template instance")
    sub.add_argument("-d", "--destination", 
                     help="Override default destination path (default: ./docengine/<name>/)")

@common.feature_flag("ON")
def _timerep(subs):
    info = "pm - convert OpenProject xls time report to C5-DEC time sheet"
    sub = subs.add_parser(
        "timerep", description=info.capitalize() + ".", help=info
    )
    sub.add_argument("name", help="Full name (.xls) of OpenProject time report stored in c5dec/input")

@common.feature_flag("ON")
def _consolidate(subs):
    info = "pm - consolidate all C5-DEC time sheets from c5dec/input directory"
    sub = subs.add_parser(
        "consolidate", description=info.capitalize() + ".", help=info
    )
    sub.add_argument("name", help="Name of directory under c5dec/input containing time reports")
    sub.add_argument("-l", "--filter", help="Apply filters to consolidated report")
    sub.add_argument("-f", "--fromdate", help="Starting from date, i.e., entries having date after this input")
    sub.add_argument("-t", "--to", help="Up to date, i.e., entries having date before this input")
    sub.add_argument("-d", "--field", help="Field name to filter for, e.g., Domain")
    sub.add_argument("-v", "--value", help="Field value to filter for, e.g., RD")

@common.feature_flag("ON")
def _costrep(subs):
    info = "pm - compute cost report from C5-DEC time sheet"
    sub = subs.add_parser(
        "costrep", description=info.capitalize() + ".", help=info
    )
    sub.add_argument("name", help="Full name (.xlsx) of C5-DEC time report stored in c5dec/input")

@common.feature_flag("OFF")
def _retrieveattr(subs):
    """Configure the `c5dec attribute retrieval` subparser."""
    info = "Invoke the attributes retrieval command from the SSDLC module"
    sub = subs.add_parser(
        "retrieveattr", description=info.capitalize() + ".", help=info)
    sub.add_argument("prefix", help="prefix of artifact repository")

def add_common_args(sub):
    versions_supported = ["3R1", "3R2", "3R3", "3R4", "3R5"]
    sub.add_argument("-v", "--verbose", action="store_true")
    sub.add_argument("--version",
                     help=f"Specify Common Criteria (CC) version: {versions_supported}")

@common.feature_flag("ON")
def _view(subs):
    info = "cct - retrieve Common Criteria (CC) item (class/family/component/element) by ID or name"
    sub = subs.add_parser(
        "view", description=info.capitalize() + ".", help=info)
    sub.add_argument("id", help="CC item ID (case insensitive).")
    add_common_args(sub)

@common.feature_flag("ON")
def _validate(subs):
    info = "cct - run CC component choice validation routine"
    sub = subs.add_parser(
        "validate", description=info.capitalize() + ".", help=info)
    sub.add_argument("id", help="List of CC component IDs.", nargs="+")
    sub.add_argument("-d", "--dependency", action="store_const", const="dep", dest="mode",
                     help="Validate component list for dependencies.")
    add_common_args(sub)

@common.feature_flag("ON")
def _checklist(subs):
    info = "cct - create evaluation checklist in YAML+Markdown, editable via TUI"
    sub = subs.add_parser(
        "checklist", description=f"{info.capitalize()}. NOTE: the <prefix> must appear before the options: c5dec checklist prefix [options]" + ".", help=info)
    sub.add_argument("prefix", help="Identifier/name of checklist used as prefix to name its components.")

    group = sub.add_mutually_exclusive_group()
    group.add_argument("-c", "--create", action="store_true", 
                    help="Create evaluation checklist from component and/or package IDs.")
    group.add_argument("-l", "--list", const=True, default=False,
                    help="List all available checklists.", nargs="?")
    group.add_argument("--edit", help="Edit work unit.")
    group.add_argument("-u", "--update", action="store_true",
                       help="Update evaluation checklist.")
    group.add_argument("--validate", action="store_true",
                       help="Validate evaluation checklist.")
    group.add_argument("-s", "--status", action="store_true",
                       help="Retrieve status of evaluation checklist.")
    group.add_argument("--publish", help="Publish evaluation checklist to path.")

    sub.add_argument("--id", help="List of Component IDs", 
                    required='-c' in sys.argv or '--create' in sys.argv, nargs="+")
    sub.add_argument("--info", help="General information about evaluation project.", nargs="+")
    sub.add_argument("--editor", help="Set editor (defaults to vim).")
    add_common_args(sub)

@common.feature_flag("ON")
def _export(subs):
    info = "cct - export work unit (WU) evaluation checklist to spreadsheet: no selection -> all WUs exported."
    usg_note = "Usage note: c5dec export name version [-h] [-p COMPONENT [COMPONENT ...]] [-c CLASS [CLASS ...]]"
    sub = subs.add_parser(
        "export", description=info + " " + usg_note + ".", help=info
    )
    sub.add_argument("name", help="Unique prefix for evaluation checklist")
    sub.add_argument("version", help="Desired CC release version (options: 3R5 or 2022R1)")
    sub.add_argument("-p", "--components", help="List of desired CC component IDs (e.g., ACO_REL.2 ALC_CMC.1); overrides class choices (default: empty)", nargs="+")
    sub.add_argument("-c", "--classes", help="List of desired CC class IDs (e.g., ATE ALC); used only if no CC components provided (default: empty)", nargs="+") 

@common.feature_flag("ON")
def _etr(subs):
    info = "cct - process WU evaluation checklist spreadsheet to generate ETR parts for C5-DEC DocEngine"
    sub = subs.add_parser(
        "etr", description=info + ".", help=info
    )
    eval_checklist_folder = os.path.join(os.getcwd(), settings.ASSETS_FOLDER_NAME, settings.ETR_FOLDER_NAME)
    sub.add_argument("-n", "--name", help="File name of evaluation checklist to load from {} folder; can also be set in c5dec_params.yml (default: etr-eval-checklist)".format(eval_checklist_folder))
    sub.add_argument("-f", "--families", help="List of desired CC family IDs (default: CMC)", nargs="+") 
    sub.add_argument("-t", "--tables", help="List of tables to convert to standard Markdown (default (all options): DocStruct Acronyms Glossary)", nargs="+")

@common.feature_flag("OFF")
def _publish(subs):
    info = "transformer - publish documentation and technical specifications"
    sub = subs.add_parser(
        "publish", description=info + ".", help=info
    )
    sub.add_argument("-f", "--format", help="Publication format: .md .html (default: .html)")
    sub.add_argument("-d", "--directory", help="Name of directory stored in c5dec/input.")

@common.feature_flag("ON")
def _transform(subs):
    info = "transformer - import, export, convert and compile using integrated doorstop, pandoc and quarto"
    sub = subs.add_parser(
        "transform", description=info + ".", help=info
    )

@common.feature_flag("ON")
def _cra_checklist(subs):
    info = "cra - create and export CRA essential requirements checklist for EU Cyber Resilience Act compliance"
    sub = subs.add_parser(
        "cra", description=info + ".", help=info
    )
    sub.add_argument(
        "--category",
        choices=["default", "class_i", "class_ii", "critical"],
        default="default",
        help="Product category (default, class_i, class_ii, critical)"
    )
    sub.add_argument(
        "--create",
        action="store_true",
        help="Create a new CRA essential requirements checklist"
    )
    sub.add_argument(
        "--export",
        metavar="PATH",
        help="Export checklist to Excel file at specified path"
    )
    sub.add_argument(
        "--verify",
        action="store_true",
        help="Auto-verify SBOM requirement based on project state"
    )
    sub.add_argument(
        "--prefix",
        default=None,
        help="Doorstop document prefix (defaults to CRAC)"
    )

@common.feature_flag("ON")
def _sbom(subs):
    info = "cra - generate, import, compare, and manage Software Bill of Materials (SBOM) for CRA compliance"
    sub = subs.add_parser(
        "sbom", description=info + ".", help=info
    )
    subcommands = sub.add_subparsers(dest="sbom_action", help="SBOM operations")
    
    # Generate SBOM
    gen = subcommands.add_parser("generate", help="Generate SBOM using Syft")
    gen.add_argument("target", help="Target path to analyze (directory, file, or image)")
    gen.add_argument("-f", "--format", choices=["cyclonedx", "spdx"], 
                     default="cyclonedx", help="SBOM format")
    gen.add_argument("-o", "--output", help="Output file path (default: sbom.json)")
    
    # Import SBOM
    imp = subcommands.add_parser("import", help="Import SBOM into Doorstop")
    imp.add_argument("sbom_file", help="Path to SBOM file")
    imp.add_argument("--prefix", help="Doorstop document prefix (default: SBOM)")
    imp.add_argument("--version", help="Version suffix for prefix (e.g., v1.0)")
    
    # Diff SBOMs
    diff = subcommands.add_parser("diff", help="Compare two SBOMs")
    diff.add_argument("sbom1", help="First SBOM document prefix (older)")
    diff.add_argument("sbom2", help="Second SBOM document prefix (newer)")
    diff.add_argument("-o", "--output", help="Output markdown report path")
    
    # Validate SBOM
    val = subcommands.add_parser("validate", help="Validate SBOM completeness")
    val.add_argument("prefix", help="SBOM document prefix to validate")

common.feature_flag("ON")
def _cpssa(subs):
    info = "cpssa - threat modelling and risk analysis on top of OSS: OWASP pytm, threagile and pyfair"
    sub = subs.add_parser(
        "cpssa", description=info + ".", help=info
    )
    subcommands = sub.add_subparsers(dest="cpssa_action", help="CPSSA operations")

    # Create threat model template from Doorstop project
    ctm = subcommands.add_parser(
        "create-threat-model",
        help="Generate a threat model from Doorstop artifacts (Threagile YAML, pytm Python or JSON)",
    )
    ctm.add_argument(
        "--project", default=".",
        help="Path to C5-DEC project root (default: current directory)",
    )
    ctm.add_argument("-o", "--output", help="Output file path (default depends on --format)")
    ctm.add_argument(
        "--format", default="threagile",
        choices=["threagile", "pytm-python", "pytm-json"],
        help="Output format: threagile (YAML), pytm-python (.py) or pytm-json (.json). Default: threagile",
    )
    ctm.add_argument(
        "--arc-folder",
        metavar="PATH",
        default=None,
        help=(
            "Full path to the directory containing architecture item files "
            "(ARC/HARC/LARC). When omitted, auto-discovery searches for a "
            "folder named 'arc', 'harc', or 'larc' with a .doorstop.yml file "
            "under the project's Doorstop specs root."
        ),
    )

    # Generate CPSSA Markdown report from a threat model
    gr = subcommands.add_parser(
        "generate-report",
        help="Generate a CPSSA Markdown report from a threat model YAML",
    )
    gr.add_argument(
        "--model", default="threat-model.yml",
        help="Path to threat model YAML (default: threat-model.yml)",
    )
    gr.add_argument("-o", "--output", help="Output Markdown path (default: cpssa-report.md)")

    # Generate Data Flow Diagram from Doorstop ARC items
    dfd = subcommands.add_parser(
        "generate-dfd",
        help="Generate a PlantUML Data Flow Diagram from Doorstop ARC items",
    )
    dfd.add_argument(
        "--project", default=".",
        help="Path to C5-DEC project root (default: current directory)",
    )
    dfd.add_argument("-o", "--output", help="Output .puml path (default: cpssa-dfd.puml)")
    dfd.add_argument(
        "--arc-folder",
        metavar="PATH",
        default=None,
        help=(
            "Full path to the directory containing architecture item files. "
            "When omitted, auto-discovery is used."
        ),
    )

    # Generate FAIR input template
    fip = subcommands.add_parser(
        "fair-input",
        help="Generate a FAIR parameters template YAML from a threat model",
    )
    fip.add_argument(
        "--model", default="threat-model.yml",
        help="Path to threat model YAML or JSON (default: threat-model.yml)",
    )
    fip.add_argument("-o", "--output", help="Output YAML path (default: fair-params.yml)")

    # Quantitative risk analysis (FAIR/pyfair)
    qra = subcommands.add_parser(
        "risk-analysis",
        help="Run FAIR-based Monte Carlo quantitative risk analysis using pyfair",
    )
    qra.add_argument(
        "--model", default="threat-model.yml",
        help="Path to threat model YAML (default: threat-model.yml)",
    )
    qra.add_argument("-o", "--output", help="Output directory for results (default: model directory)")
    qra.add_argument(
        "--simulations", type=int, default=10000,
        help="Monte Carlo simulation count (default: 10000)",
    )
    qra.add_argument(
        "--fair-params",
        metavar="FILE",
        default=None,
        help=(
            "Path to a FAIR parameters YAML file with per-scenario LEF/LM "
            "calibration. Generate a template with: c5dec cpssa fair-input --model <model>"
        ),
    )

common.feature_flag("ON")
def _cryptography(subs):
    info = "cryptography - run crypto operations or launch C5-DEC interactive session to use GnuPG, Kryptor, Cryptomator and OQS-OpenSSL for PQC"
    sub = subs.add_parser(
        "crypto", description=info + ".", help=info
    )
    subcommands = sub.add_subparsers(dest="crypto_action", help="Cryptographic operations")

    # SHA-256 hash
    h = subcommands.add_parser("hash", help="Compute SHA-256 hash of a file")
    h.add_argument("file", help="File to hash")

    # Verify hash
    vh = subcommands.add_parser("verify-hash", help="Verify a file's SHA-256 hash")
    vh.add_argument("file", help="File to verify")
    vh.add_argument("expected", help="Expected hex-encoded SHA-256 digest")

    # GPG sign
    sg = subcommands.add_parser("sign", help="Create a GnuPG detached signature")
    sg.add_argument("file", help="File to sign")
    sg.add_argument("--key", help="GPG key ID or fingerprint (default: GPG default key)")
    sg.add_argument("-o", "--output", help="Output signature file path (default: <file>.sig)")

    # GPG verify signature
    vs = subcommands.add_parser("verify-sig", help="Verify a GnuPG detached signature")
    vs.add_argument("file", help="The signed file")
    vs.add_argument("sigfile", help="The signature file (.sig or .asc)")

    # GPG encrypt
    enc = subcommands.add_parser("encrypt", help="GPG-encrypt a file for one or more recipients")
    enc.add_argument("file", help="File to encrypt")
    enc.add_argument("-r", "--recipients", nargs="+", required=True,
                     metavar="KEYID", help="Recipient GPG key IDs or email addresses")
    enc.add_argument("-o", "--output", help="Output path (default: <file>.gpg)")

    # GPG decrypt
    dec = subcommands.add_parser("decrypt", help="GPG-decrypt an encrypted file")
    dec.add_argument("file", help="Encrypted file (.gpg or .asc)")
    dec.add_argument("-o", "--output", help="Output path for decrypted content")
    dec.add_argument("--passphrase", help="Passphrase for symmetric decryption")

    # Shamir secret split
    ss = subcommands.add_parser("shamir-split", help="Split a secret using Shamir's Secret Sharing")
    ss.add_argument("secret_hex", help="Secret as a hex string (at most 126 bits)")
    ss.add_argument("-n", "--shares", type=int, required=True, help="Total number of shares")
    ss.add_argument("-k", "--threshold", type=int, required=True,
                    help="Minimum shares needed to reconstruct")

    # Shamir secret recover
    sr = subcommands.add_parser("shamir-recover", help="Reconstruct a secret from Shamir shares")
    sr.add_argument("shares", nargs="+", help="Share strings (<index>:<value_hex>)")

    # NaCl keygen
    subcommands.add_parser("nacl-keygen", help="Generate a NaCl Ed25519 signing keypair")

    # NaCl sign
    ns = subcommands.add_parser("nacl-sign", help="Sign a message with a NaCl Ed25519 key")
    ns.add_argument("message", help="Message to sign (UTF-8 string)")
    ns.add_argument("signing_key", help="Hex-encoded Ed25519 signing key")

    # NaCl verify
    nv = subcommands.add_parser("nacl-verify", help="Verify a NaCl Ed25519 signed message")
    nv.add_argument("signed_hex", help="Hex-encoded signed message")
    nv.add_argument("verify_key", help="Hex-encoded Ed25519 verify (public) key")