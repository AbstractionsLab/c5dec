---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5, CC2022
---

# Conformance Claim

A Conformance Claim serves as an explicit declaration by the develoepr, stipulating the degree and manner to which a [Target of Evaluation (TOE)](./TargetofEvaluation.md) adheres to a specific [Security Target (ST)](./SecurityTarget.md) or [Protection Profiles (PPs)](./ProtectionProfile.md). It delineates the exactness or latitude in compliance with the outlined security functionalities and assurance requirements, offering a structured perspective to evaluators and consumers regarding the TOE's security attributes and the breadth of its evaluation. The claim usually encompasses various conformance types, such as CC Conformance, Package Conformance, and PP Conformance, each offering distinct insights into the TOE’s alignment with the CC, particular [packages](./Package.md), or specific PPs, respectively. Consequently, the Conformance Claim becomes instrumental in establishing transparency and assurance in the TOE's security properties and evaluation scope, thereby facilitating informed decision-making for stakeholders in adopting secure products and solutions.

## CC Conformance Claim

The CC conformance claim specifies the version of CC Part 2 and CC Part 3 to which conformance is claimed. The recognized conformance claims are:

- **CC Part x conformant**: All Security Requirements in the claiming document are based only upon components in CC Part x.
- **CC Part x extended**: At least one Security Requirement in the claiming document is not based upon components in CC Part x.

## Package Conformance Claim

If package conformances are claimed, for each package the claim must be categorized as one of the following:

- **Package conformant**
  - For functional packages, all constituent parts ([SPD](./SecurityProblemdefinition.md), [Security Objectives](./SecurityObjective.md), and [SFRs](./SecurityFunctionalRequirement.md)) of the functional package are present without modification. PPs can restrict some selections of SFRs in a package and still claim to be package conformant.
  - For assurance packages, the [SARs](./SecurityAssuranceRequirement.md) are identical to the SARs in the assurance package.
- **Package augmented**
  - For functional packages, all constituent parts (SPD, security objectives, and SFRs) of the functional package are present but at least one additional SFR or one SFR that is hierarchically higher than an SFR in the package is included;
  - For assurance packages, all SARs in the assurance package are included but also at least one additional SAR or one SAR that is hierarchically higher than an SAR in the assurance package.
- **Package tailored**
  - For functional packages, all constituent parts (SPD, security objectives, and SFRs) are given in the functional package, but shall have additional selection items for an SFR with existing selections in the package, and optionally, at least one additional SFR and/or one SFR that is hierarchically higher than an SFR in the functional package;
  - Not allowed for STs.

## PP Conformance Claim

PPs and PP-Configurations specify the type of conformance that is allowed in a conformance statement. Claiming to be PP Conformant requires compliance according to the conformance statement.