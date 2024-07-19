---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5, CC 2022
Tags: [Extended Components, Extended Security Requirements]
---

# Extended Component Definition

**Acronym:** ECD

Extended Components play a pivotal role in instances where the existing [security functional](./SecurityComponent.md) or [assurance components](./SecurityComponent.md), catalogued in the CC, do not adequately or accurately encapsulate the specific requirements of a particular [TOE](./TargetofEvaluation.md). In simpler terms, when a [Protection Profile (PP)](./ProtectionProfile.md) or [Security Target (ST)](./SecurityTarget.md) confronts a scenario where the [Security Objectives](./SecurityObjective.md) are not completely addressed by the pre-established components in the CC, the definition of Extended Components is required.

Purposefully, an Extended Component serves to:
- **Fill Gaps:** Address and articulate unique or specialized requirements that are not comprehensively covered by existing CC components.
- **Maintain Rigor:** Ensure that these specialized requirements are subjected to the same level of rigor and structured evaluation as existing components.
- **Facilitate Tailoring:** Enable the tailoring of PPs and STs to more accurately reflect the security landscape and requisites of specific IT products or systems.

The Extended Component Definition (ECD) serves as a container for all Extended Components defined for a specifc TOE and is documented in a corresponding PP or ST. In that context, the ECD is composed of a **statement of security requirements**, identifying all Extended Security Requirements, and definitions of the Extended Components including theses Extended Security Requirements.

## Practical Guidance

Foremost, it is strongly advised to avoid the definition of Extended Components whenever possible. Instead, [requirement Operations](./Operations.md) should be used to tailor requirements to the specifc needs. Usually, such refinements already resolve the issue when no existing Security Component seems to address a particular Security Objective sufficiently. However, in instances where a refinement does not provide ample resolution, the following guidance may be leveraged to define Extended Components. 

### **Part I: Basic Tenets**

1. **Opt for Existing Components**: Explore publicly available PPs and STs for Extended Components that fit your needs. Prioritize utilizing and refining existing components, reserving the definition of Extended Components as a last resort.
2. **Maintain Consistency**: As required by APE_ECD.1.4C and ASE_ECD.1.4C, ensure alignment with existing CC Security Components in style, structure, and abstraction level.
3. **Measurable and Objective Elements**: Facilitate evaluatability by establishing measurable and objective requirements (APE_ECD.1.5C and ASE_ECD.1.5C)

### **Part II: Formulating Extended Security Functional Requirements (SFRs)**

1. **Abstraction Level Adherence**: Preserve a level of abstraction commensurate with ISO/IEC 15408-2 components.
2. **Consistent Style and Phraseology**: Maintain terminological and phraseological consistency, starting functional requirements, for instance, with phrases like “The TSF shall”.
3. **Topological and Nomenclatural Consistency**: Align with ISO/IEC 15408-2 for topology and naming, see Part IV
4. **Application Notes**: Provide application notes in PPs or STs to clarify the usage of the extended component.

### **Part III: Developing Extended Security Assurance Requirements (SARs)**

1. **Defining Actions**: Outline actions for developers and evaluators, ensuring that the former focuses on producing necessary evaluation evidence, while the latter verifies product conformity.
2. **Precise Evidence Requirements**: Establish clear parameters for the content and presentation of developer evidence.
3. **Objective Criteria**: Articulate SARs to offer unequivocal, objective criteria, minimizing the need for subjective evaluator judgement.
4. **Defining Evaluator Work Units for SARs:**
    - **Structural Consistency with ISO/IEC 18045**: Emulate the structure of work units from ISO/IEC 18045 when defining evaluator work units to demonstrate compliance.
    - **Addressing All Aspects**: Ensure work units comprehensively address all facets of the extended assurance component.
    - **Clear Guidance**: Provide unequivocal instructions on assessment execution to evaluators.

### **Part IV: Practical Considerations**

- **Promoting Reusability**: Strive for generic extended components, which allow for operations like [assignment](./Operation-Assignment.md) or [selection](./Operation-Selection.md), enhancing reusability across contexts.
- **Naming Convention**:  

    [Type Identifier: F|A][Class Acronym: 2 characters]_[Family Acronym: 3 characters].[Component Number].[Element Number]


### Example: CC PP Cryptographic Module, Security Level "High" BSI-PP-0042

This Protection Profile was released in 2008 and claims conformance to CC version 2.3. It is immediately apparent just based on the Acronym that the defined Family is considered to be an extension of the Functional Class FCS: Cryptographic Support. 

#### Definition of the Family FCS_RNG

**Family behaviour**

This family defines requirements for the generation random number where the random
numbers are intended to be used for cryptographic purposes. The requirements address the
type of the random number generator as defined in AIS 20/315 and quality of the random
numbers.

**Component levelling:**

FCS_RNG.1 Generation of random numbers requires that random numbers meet a defined quality metric.

*Management:* FCS_RNG.1 There are no management activities foreseen.

*Audit:* FCS_RNG.1 There are no actions defined to be auditable.

**FCS_RNG.1 Random number generation**

Hierarchical to: No other components.

Dependencies: FPT_TST.1.

FCS_RNG.1.1 

The TSF shall provide a [selection: physical, non-physical true,
deterministic, hybrid] random number generator that meet [assignment:
list of security capabilities].

FCS_RNG.1.2 

The TSF shall provide random numbers that meet [assignment: a defined
quality metric]. 


## Additional Resources

- **Common Criteria Part 1-3**
- **Common Evaluation Methodology**
- **ISO/IEC TR 15446**
- **[The Common Criteria Portal](https://commoncriteriaportal.org/pps/)**

## Related Articles

- [Security Target (ST)](./SecurityTarget.md)
- [Protection Profile (PP)](./ProtectionProfile.md)
- [Security Components](./SecurityComponent.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Requirement Operations](./Operations.md)
