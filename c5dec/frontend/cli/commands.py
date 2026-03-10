"""CLI command functions."""

# CLI design is based on that of Doorstop

import os, sys, tempfile
import time
import subprocess
from typing import Set

import c5dec.frontend.tui.main as tui
import c5dec.frontend.gui.app as gui
from c5dec import common
import c5dec.settings as c5settings
import c5dec.core.ssdlc as ssdlc
import c5dec.core.pm as pm
from datetime import datetime
import c5dec.core.cct as cct
import c5dec.core.transformer as transformer
from docx.opc.exceptions import PackageNotFoundError

log = common.logger(__name__)
log.setLevel(common.logging.INFO)

logHandler = common.logging.FileHandler(c5settings.CMD_LOG_FILE, mode='a')
formatter = common.logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s", "%Y-%m-%d %H:%M:%S")
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

def open_editor(editor, filepath):
    if not editor:
        EDITOR = c5settings.DEFAULT_EDITOR
    else:
        EDITOR = os.environ.get('EDITOR', editor)

    if EDITOR in ['vim', 'nano']:
        with open(filepath, "r") as file:
            initial = file.read()

        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
            tf.write(bytes(initial, 'utf--8'))
            tf.flush()
            subprocess.run([EDITOR, tf.name])
            tf.seek(0)
            edited = tf.read()
            
        if edited.decode('utf-8') != initial:
            with open(filepath, "w") as file:
                file.write(edited.decode('utf-8'))
            info_msg = "File successfully saved." 
            log.info(info_msg)
    else:
        try:
            subprocess.run([EDITOR, "-r", filepath], check=True,
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        except subprocess.CalledProcessError as e:
            log.error(f"{e}")
        except FileNotFoundError:
            log.error(f"Editor {EDITOR} not found.")

def get(name):
    """Get a command function by name."""
    if name:
        log.debug("running command '{}'...".format(name))
        return globals()["run_" + name]
    else:
        log.debug("launching main command...")
        return run
    
def run(args, cwd, error, catch=True):  # pylint: disable=W0613
    """Process arguments and run the `c5dec` subcommand.

    :param args: Namespace of CLI arguments
    :param cwd: current working directory
    :param error: function to call for CLI errors
    :param catch: catch and log :class:`~c5dec.common.c5decError`

    """
    if args.gui:
        gui.main(args, cwd)
    else:
        tui.main(args, cwd)
    return True

def run_new(args, cwd, _, catch=True):
    ssdlc.create_new_c5dec_project(project=args.project, user=args.user) 

def run_docengine(args, cwd, _, catch=True):
    """Run the docengine command to create report or presentation templates."""
    try:
        success = ssdlc.create_docengine_template(
            template_type=args.template_type,
            name=args.name,
            destination=args.destination
        )
        return success if success is not None else True
    except Exception as e:
        log.error(f"Failed to create DocEngine template: {e}")
        if not catch:
            raise
        return False

def run_timerep(args, cwd, _, catch=True):
    timerep_assistant = pm.TimeReportAssistant()
    timerep_assistant.input_file_name = args.name
    try:
        timerep_assistant.convert_openproject_time_report_to_IAL_format()
    except Exception as e:
        log.error("Something unexpected went wrong: {}".format(e))

def run_consolidate(args, cwd, _, catch=True):
    timerep_assistant = pm.TimeReportAssistant()
    timerep_assistant.set_tsh_folder_name(args.name)
    date_format = '%d-%m-%Y'
    if args.filter == None:
        timerep_assistant.set_timerep_parameters(source_folder=args.name,apply_filters=False)
    else:
        timerep_assistant.set_timerep_parameters(source_folder=args.name, apply_filters=True, 
                                            from_date=datetime.strptime(args.fromdate, date_format), 
                                            to_date=datetime.strptime(args.to, date_format),
                                            filter_field=args.field,
                                            filter_field_value=args.value)
    try:
        timerep_assistant.consolidate_timesheets()
    except IOError:
        log.error("Missing or bad arguments.")
    except PackageNotFoundError:
        log.error("No xlsx file found at the provided path.")
    except Exception as e:
        log.error("Something unexpected went wrong: {}".format(e))


def run_costrep(args, cwd, _, catch=True):
    timerep_assistant = pm.TimeReportAssistant()
    timerep_assistant.input_file_name = args.name
    try:
        timerep_assistant.compute_cost_report()
    except Exception as e:
        log.error("Something unexpected went wrong: {}".format(e)) 

# This function is no longer used and should be removed
# @deprecated
def run_retrieveattr(args, cwd, _, catch=True):
    ssdlc.get_respository_attributes(args.prefix)

def run_view(args, cwd, _, catch=True):
    c5settings.SELECTED_CC_VERSION = args.version
    if args.verbose:
        cct.get_item(args.id, args.version)
    else:
        cct.get_item(args.id, args.version, silence=True)

def run_validate(args, cwd, _, catch=True):
    c5settings.SELECTED_CC_VERSION = args.version
    if args.verbose:
        cct.validate(args.id, args.version, mode=args.mode)
    else:
        cct.validate(args.id, args.version, mode=args.mode, silence=True)

def run_checklist(args, cwd, _, catch=True):
    c5settings.SELECTED_CC_VERSION = args.version
    if args.create:
        if args.info:
            info_dict = {k: v for k, v in (item.split('=') for item in args.info)}
        else:
            info_dict = {"GeneralInfo": f"{args.version or '3R5'}"}
        cct.CLIChecklistHandler().create(args.version, args.id, args.prefix, info=info_dict)
    if args.list:
        cct.CLIChecklistHandler().list(args.prefix)
    if args.update:
        cct.CLIChecklistHandler().update(args.prefix)
    if args.validate:
        cct.CLIChecklistHandler().validate(args.prefix)
    if args.status:
        cct.CLIChecklistHandler().status(args.prefix)
    if args.edit:
        item = args.edit
        abs_item_path = cct.CLIChecklistHandler().edit(args.prefix, item)
        if abs_item_path:
            rel_item_path = os.path.relpath(abs_item_path, cwd)
            open_editor(args.editor, rel_item_path)
    if args.publish:
        path = os.path.abspath(os.path.join(cwd, args.publish))
        cct.CLIChecklistHandler().publish(args.prefix, path)

def run_cra(args, cwd, _, catch=True):
    """Run CRA checklist command - create or export CRA essential requirements checklist."""
    from c5dec.core import cra
    from pathlib import Path
    
    try:
        if args.create:
            # Create a new CRA checklist
            builder = cra.CRAChecklistBuilder()
            checklist_path = builder.create_cra_checklist(
                category=args.category,
                project_path=Path(cwd) if cwd else None,
                prefix=args.prefix
            )
            print(f"✓ Created CRA checklist for category '{args.category}'")
            print(f"  Location: {checklist_path}")
            print(f"  Edit checklist items in: {checklist_path}/*.yml")
            print(f"  Export to Excel with: c5dec cra --export <filename>.xlsx")
            return True
            
        elif args.verify:
            # Auto-verify SBOM requirement
            prefix = args.prefix or c5settings.CRA_CHECKLIST_PREFIX
            print("Verifying CRA SBOM requirement...")
            updated = cra.auto_verify_sbom_requirement(
                checklist_prefix=prefix,
                project_path=Path(cwd) if cwd else None
            )
            if updated:
                print("✓ CRA SBOM requirement (cra_ii_1_1) verdict updated")
            else:
                print("✓ CRA SBOM requirement already up-to-date")
            return True
            
        elif args.export:
            # Export checklist to Excel
            builder = cra.CRAChecklistBuilder()
            prefix = args.prefix or c5settings.CRA_CHECKLIST_PREFIX
            output_path = Path(args.export)
            
            # Auto-verify before export
            print("Auto-verifying requirements...")
            cra.auto_verify_sbom_requirement(
                checklist_prefix=prefix,
                project_path=Path(cwd) if cwd else None
            )
            
            exported_path = builder.export_cra_checklist(
                checklist_prefix=prefix,
                output_path=output_path,
                project_path=Path(cwd) if cwd else None
            )
            print(f"✓ Exported CRA checklist to: {exported_path}")
            return True
            
        else:
            # No action specified - show help
            print("CRA Checklist Command")
            print("=" * 50)
            print("Usage:")
            print(f"  Create checklist: c5dec cra --create --category <category>")
            print(f"  Verify SBOM req:  c5dec cra --verify")
            print(f"  Export to Excel:  c5dec cra --export <filename>.xlsx")
            print("")
            print("Categories: default, class_i, class_ii, critical")
            print("")
            print("Example:")
            print("  c5dec cra-checklist --create --category class_i")
            print("  c5dec cra-checklist --verify")
            print("  c5dec cra-checklist --export cra-assessment.xlsx")
            return True
            
    except common.C5decError as e:
        log.error(f"CRA checklist error: {e}")
        if not catch:
            raise
        return False
    except Exception as e:
        log.error(f"Unexpected error in CRA checklist: {e}")
        if not catch:
            raise
        return False

def run_sbom(args, cwd, _, catch=True):
    """Run SBOM command - generate, import, compare, or validate SBOMs."""
    from c5dec.core import sbom
    from pathlib import Path
    
    try:
        if not hasattr(args, 'sbom_action') or args.sbom_action is None:
            # No subcommand specified - show help
            print("SBOM Command")
            print("=" * 50)
            print("Usage:")
            print("  Generate SBOM: c5dec sbom generate <target> -f <format> -o <output>")
            print("  Import SBOM:   c5dec sbom import <sbom_file> [--prefix PREFIX]")
            print("  Compare SBOMs: c5dec sbom diff <sbom1> <sbom2> [-o report.md]")
            print("  Validate SBOM: c5dec sbom validate <prefix>")
            print("")
            print("Formats: cyclonedx, spdx")
            print("")
            print("Example:")
            print("  c5dec sbom generate . -f cyclonedx -o sbom.json")
            print("  c5dec sbom import sbom.json --version 1.0")
            print("  c5dec sbom diff SBOM-v1.0 SBOM-v2.0 -o changes.md")
            return True
        
        if args.sbom_action == "generate":
            # Generate SBOM using Syft
            target = Path(args.target)
            output = Path(args.output) if args.output else Path.cwd() / "sbom.json"
            format_name = f"{args.format}-json"
            
            if not sbom.check_syft_installed():
                print("❌ Error: Syft is not installed")
                print("Install from: https://github.com/anchore/syft#installation")
                print("Or in dev container: see dev.Dockerfile")
                return False
            
            print(f"Generating SBOM for {target}...")
            sbom_path = sbom.generate_sbom(
                target_path=target,
                output_format=format_name,
                output_path=output
            )
            print(f"✓ SBOM generated: {sbom_path}")
            print(f"  Import to Doorstop with: c5dec sbom import {sbom_path}")
            return True
        
        elif args.sbom_action == "import":
            # Import SBOM to Doorstop
            sbom_file = Path(args.sbom_file)
            if not sbom_file.exists():
                print(f"❌ Error: SBOM file not found: {sbom_file}")
                return False
            
            print(f"Importing SBOM from {sbom_file}...")
            doc_path = sbom.import_sbom_to_doorstop(
                sbom_path=sbom_file,
                project_path=Path(cwd) if cwd else None,
                prefix=args.prefix,
                version=args.version
            )
            print(f"✓ SBOM imported to Doorstop document: {doc_path}")
            print(f"  View items: ls {doc_path}/*.yml")
            return True
        
        elif args.sbom_action == "diff":
            # Compare two SBOMs
            print(f"Comparing SBOMs: {args.sbom1} vs {args.sbom2}...")
            diff_result = sbom.compare_sboms(
                sbom1_prefix=args.sbom1,
                sbom2_prefix=args.sbom2,
                project_path=Path(cwd) if cwd else None
            )
            
            # Print summary
            print(f"✓ Comparison complete:")
            print(f"  Added:   {diff_result['summary']['added_count']} components")
            print(f"  Removed: {diff_result['summary']['removed_count']} components")
            print(f"  Changed: {diff_result['summary']['changed_count']} components")
            
            # Export to file if requested
            if args.output:
                output_path = Path(args.output)
                sbom.export_sbom_diff_report(diff_result, output_path)
                print(f"  Report: {output_path}")
            else:
                # Print details to console
                if diff_result['added']:
                    print(f"\n  Added components:")
                    for name in sorted(diff_result['added'].keys())[:5]:
                        print(f"    + {name}")
                    if len(diff_result['added']) > 5:
                        print(f"    ... and {len(diff_result['added']) - 5} more")
                
                if diff_result['removed']:
                    print(f"\n  Removed components:")
                    for name in sorted(diff_result['removed'].keys())[:5]:
                        print(f"    - {name}")
                    if len(diff_result['removed']) > 5:
                        print(f"    ... and {len(diff_result['removed']) - 5} more")
                
                if diff_result['changed']:
                    print(f"\n  Changed components:")
                    for name, info in sorted(list(diff_result['changed'].items())[:5]):
                        print(f"    ~ {name}: {info['old_version']} → {info['new_version']}")
                    if len(diff_result['changed']) > 5:
                        print(f"    ... and {len(diff_result['changed']) - 5} more")
            
            return True
        
        elif args.sbom_action == "validate":
            # Validate SBOM
            print(f"Validating SBOM document: {args.prefix}...")
            is_valid = sbom.validate_sbom(
                sbom_prefix=args.prefix,
                project_path=Path(cwd) if cwd else None
            )
            
            if is_valid:
                print(f"✓ SBOM validation passed")
                return True
            else:
                print(f"❌ SBOM validation failed (see warnings above)")
                return False
        
        else:
            print(f"Unknown SBOM action: {args.sbom_action}")
            return False
    
    except common.C5decError as e:
        log.error(f"SBOM error: {e}")
        print(f"❌ Error: {e}")
        if not catch:
            raise
        return False
    except Exception as e:
        log.error(f"Unexpected error in SBOM command: {e}")
        print(f"❌ Unexpected error: {e}")
        if not catch:
            raise
        return False

def run_export(args, cwd, _, catch=True, **kwargs):
    c5settings.SELECTED_CC_VERSION = args.version
    print(c5settings.SELECTED_CC_VERSION)
    try:
        cct.ChecklistBuilder(checklist_name=args.name, cc_version=args.version).export_eval_checklist(class_id_vector=args.classes, component_id_vector=args.components)
    except Exception as e:
        print(e)

def run_etr(args, cwd, _, catch=True, **kwargs):
    if args.name is None:
        cct.ETR().generate_etr(family_list=args.families, tables_list=args.tables)
    else:
        cct.ETR(checklist_name=args.name).generate_etr(family_list=args.families, tables_list=args.tables)

# def run_publish(args, cwd, _, catch=True, **kwargs):
#     if args.directory is None:
#         print(f"Please specify an input directory. See c5dec publish -h for more information.")
#         return
#     if args.format is None:
#         transformer.publish(format=".html", name=args.directory)
#     else:    
#         transformer.publish(format=args.format, name=args.directory)

def run_transform(args, cwd, _, catch=True, **kwargs):
    print("---")
    print("Open C5-DEC CAD dev container in VS Code or run session (./c5dec.sh session) to use the commands below:")
    print("To import, try: doorstop import -h")
    print("To export, try: doorstop export -h")
    print("To render, use: quarto render -h")
    print("To convert, use: quarto pandoc -h")
    print("To automate file management, use: organize -h")
    print("---")
    print("Also see Transformer section of SSDLC page in user manual:")
    print("c5dec/docs/manual/ssdlc.md OR https://github.com/AbstractionsLab/c5dec/blob/main/docs/manual/ssdlc.md")

def run_cpssa(args, cwd, _, catch=True, **kwargs):
    """Run CPSSA command - create threat models, compute risk and generate reports."""
    from c5dec.core import cpssa
    from pathlib import Path

    try:
        if not hasattr(args, "cpssa_action") or args.cpssa_action is None:
            print("CPSSA - Cyber-Physical System Security Assessment")
            print("=" * 50)
            print("Usage:")
            print("  Create threat model:  c5dec cpssa create-threat-model [--project PATH] [-o OUTPUT] [--format FORMAT]")
            print("  Generate report:      c5dec cpssa generate-report [--model MODEL] [-o OUTPUT]")
            print("  Generate DFD:         c5dec cpssa generate-dfd [--project PATH] [-o OUTPUT]")
            print("  FAIR input template:  c5dec cpssa fair-input [--model MODEL] [-o OUTPUT]")
            print("  Quantitative risk:    c5dec cpssa risk-analysis [--model MODEL] [-o DIR] [--simulations N] [--fair-params FILE]")
            print("")
            print("See user manual: docs/manual/cpssa.md")
            return True

        if args.cpssa_action == "create-threat-model":
            project_path = Path(args.project) if args.project else Path(cwd or ".")
            fmt = getattr(args, "format", "threagile") or "threagile"
            output_path = Path(args.output) if args.output else None
            arc_folder = getattr(args, "arc_folder", None)
            model_path = cpssa.create_threat_model(
                project_path, output_path, format=fmt,
                arc_folder=arc_folder,
            )
            print(f"Threat model written to: {model_path}")
            if fmt == "threagile":
                print("Edit the model, then run: c5dec cpssa generate-report --model " + str(model_path))
            elif fmt == "pytm-python":
                print("Run the model:  python " + str(model_path) + " --dfd | dot -Tpng -o dfd.png")
                print("Or list threats: python " + str(model_path) + " --list")
            else:
                print("Use the JSON model with: c5dec cpssa risk-analysis --model " + str(model_path))
            return True

        elif args.cpssa_action == "generate-report":
            model_path = Path(args.model)
            output_path = Path(args.output) if args.output else model_path.parent / "cpssa-report.md"
            report_path = cpssa.generate_cpssa_report(model_path, output_path)
            print(f"CPSSA report written to: {report_path}")
            return True

        elif args.cpssa_action == "generate-dfd":
            project_path = Path(args.project) if args.project else Path(cwd or ".")
            output_path = Path(args.output) if args.output else project_path / "cpssa-dfd.puml"
            arc_folder = getattr(args, "arc_folder", None)
            dfd_path = cpssa.generate_dfd(project_path, output_path, arc_folder=arc_folder)
            print(f"Data Flow Diagram written to: {dfd_path}")
            return True

        elif args.cpssa_action == "fair-input":
            model_path = Path(args.model)
            output_path = Path(args.output) if args.output else None
            template_path = cpssa.generate_fair_input_template(model_path, output_path)
            print(f"FAIR parameters template written to: {template_path}")
            print("Edit the file to calibrate LEF and LM values per scenario, then run:")
            print(f"  c5dec cpssa risk-analysis --model {args.model} --fair-params {template_path}")
            return True

        elif args.cpssa_action == "risk-analysis":
            model_path = Path(args.model)
            output_path = Path(args.output) if args.output else model_path.parent
            simulations = getattr(args, "simulations", 10000)
            fair_params = getattr(args, "fair_params", None)
            fair_params_path = Path(fair_params) if fair_params else None
            summary_path = cpssa.run_quantitative_risk_analysis(
                model_path, output_path, simulations, fair_params_path,
            )
            print(f"Quantitative risk summary written to: {summary_path}")
            return True

        else:
            print(f"Unknown CPSSA action: {args.cpssa_action}")
            return False

    except common.C5decError as exc:
        log.error("CPSSA error: %s", exc)
        print(f"Error: {exc}")
        if not catch:
            raise
        return False
    except Exception as exc:
        log.error("Unexpected error in CPSSA command: %s", exc)
        print(f"Unexpected error: {exc}")
        if not catch:
            raise
        return False

def run_crypto(args, cwd, _, catch=True, **kwargs):
    """Run cryptography command - hash, GPG, Shamir SSS, NaCl."""
    from c5dec.core import cryptography as crypto
    from pathlib import Path

    try:
        if not hasattr(args, "crypto_action") or args.crypto_action is None:
            print("Cryptography")
            print("=" * 50)
            print("Usage:")
            print("  Hash:          c5dec crypto hash <file>")
            print("  Verify hash:   c5dec crypto verify-hash <file> <expected>")
            print("  GPG sign:      c5dec crypto sign <file> [--key KEY] [-o SIG]")
            print("  GPG verify:    c5dec crypto verify-sig <file> <sigfile>")
            print("  GPG encrypt:   c5dec crypto encrypt <file> -r KEYID [KEYID ...] [-o OUT]")
            print("  GPG decrypt:   c5dec crypto decrypt <file> [-o OUT] [--passphrase PASS]")
            print("  Shamir split:  c5dec crypto shamir-split <secret_hex> -n N -k K")
            print("  Shamir recover:c5dec crypto shamir-recover <share1> [share2 ...]")
            print("  NaCl keygen:   c5dec crypto nacl-keygen")
            print("  NaCl sign:     c5dec crypto nacl-sign <message> <signing_key>")
            print("  NaCl verify:   c5dec crypto nacl-verify <signed_hex> <verify_key>")
            print("")
            print("For PQC (Kyber/Dilithium), use the C5-DEC cryptography dev container:")
            print("  ./c5dec.sh pqc  (or reopen container selecting 'pqc' in VS Code)")
            print("  See docs/manual/cryptography.md for details.")
            return True

        if args.crypto_action == "hash":
            digest = crypto.compute_hash(args.file)
            print(digest)
            return True

        elif args.crypto_action == "verify-hash":
            ok = crypto.verify_hash(args.file, args.expected)
            if ok:
                print("OK")
            else:
                print("MISMATCH")
            return ok

        elif args.crypto_action == "sign":
            sig_path = crypto.gpg_sign_file(
                path=args.file,
                key_id=args.key,
                output_path=args.output,
            )
            print(f"Signature written to: {sig_path}")
            return True

        elif args.crypto_action == "verify-sig":
            ok = crypto.gpg_verify_signature(args.file, args.sigfile)
            print("VALID" if ok else "INVALID")
            return ok

        elif args.crypto_action == "encrypt":
            enc_path = crypto.gpg_encrypt_file(
                path=args.file,
                recipients=args.recipients,
                output_path=args.output,
            )
            print(f"Encrypted file: {enc_path}")
            return True

        elif args.crypto_action == "decrypt":
            dec_path = crypto.gpg_decrypt_file(
                path=args.file,
                output_path=args.output,
                passphrase=args.passphrase,
            )
            print(f"Decrypted file: {dec_path}")
            return True

        elif args.crypto_action == "shamir-split":
            shares = crypto.split_secret(args.secret_hex, args.shares, args.threshold)
            for share in shares:
                print(share)
            return True

        elif args.crypto_action == "shamir-recover":
            secret_hex = crypto.recover_secret(args.shares)
            print(secret_hex)
            return True

        elif args.crypto_action == "nacl-keygen":
            vk_hex, sk_hex = crypto.nacl_keygen_signing()
            print(f"verify_key:  {vk_hex}")
            print(f"signing_key: {sk_hex}")
            return True

        elif args.crypto_action == "nacl-sign":
            message_bytes = args.message.encode("utf-8")
            signed = crypto.nacl_sign(message_bytes, args.signing_key)
            print(signed.hex())
            return True

        elif args.crypto_action == "nacl-verify":
            signed_bytes = bytes.fromhex(args.signed_hex)
            message = crypto.nacl_verify(signed_bytes, args.verify_key)
            print(message.decode("utf-8"))
            return True

        else:
            print(f"Unknown crypto action: {args.crypto_action}")
            return False

    except common.C5decError as exc:
        log.error("Crypto error: %s", exc)
        print(f"Error: {exc}")
        if not catch:
            raise
        return False
    except Exception as exc:
        log.error("Unexpected error in crypto command: %s", exc)
        print(f"Unexpected error: {exc}")
        if not catch:
            raise
        return False