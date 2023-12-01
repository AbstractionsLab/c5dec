---
Last Updated: October 4, 2023
Relevant: CC Version 3.1 Revision 5, CC 2022
Tags: [Security Components, Classes, Families, Components, Elements, Security Functional Component, Security Assurance Component, Extended Components, Security Requirements, Security Functional Requirements, Security Assurance Requirements, Extended Security Requirements]
---

# Security Components

**Acronym:** None

The Common Criteria provides a catalogues of security components that serve as the structural foundation for specifying security requirements. These are organized in a hierarchical structure with four levels:
- Classes, consisting of
- Families, consisting of
- Components, consisting of
- Elements.

Security Components are categorized as Security Functional Components and Security Assurance Components for which the Common Criteria provides individual catalogues, CC Part 2 and CC Part 3, respectively. Although, both component categories share the same hierarchical structure their content slightly differs. Below a side by side comparison. 

Hierarchical level | Security Functional Component | Security Assurance Component
--- | --- | ---
Class | Class Name, Class Introduction, Functional Families | Class Name, Class Introduction, Assurance Families
Family | Family Name, Family Behaviour, Components Levelling and Description, Management, Audit, Functional Components | Family Name, Objectives, Component Levelling, Application Notes, Assurance Components
Component | Component Identification, Dependencies, Functional Elements | Component Identification, Objectives, Application Notes, Dependencies, Assurance Elements
Element | Element Identification, Functional Requirement | Element Identification, Element Type (Developer Action, Content and Presentation, Evaluator Action), Assurance Requirement

Dependencies between components may exist if the component is not self-sufficient and relies upon the presence of another component to provide security functionality or assurance. Dependencies also include hierarchical relationships between components, i.e., that a component A that is hierarchical to component B, supersedes component B. 

## Security Functional Components

Security Functional Components (SFCs) within the Common Criteria framework offer a methodologically robust and structured means to navigate the derivation and definition of [Security Functional Requirements (SFRs)](./SecurityFunctionalRequirement.md). Navigated through the hierarchical structure (Class > Family > Component > Element), SFCs facilitate a seamless, top-down progression from generalized security themes to nuanced, explicit functional requirements. Concurrently, this path facilitates the translation of [security objectives](./SecurityObjective.md), which are explicit responses to identified [threats](./Threat.md) and [policies](./OrganizationalSecurityPolicy.md), into tangible, evaluable security functions of a [Target of Evaluation (TOE)](./TargetofEvaluation.md) posing as concrete solutions to the identified [Security Problem](./SecurityProblemdefinition.md). Moreover, this hierarchical structure, while grounding SFRs in an established taxonomy, also provides the necessary scaffold to define user-specific Extended Components, ensuring the SFC's relevance and applicability across varied security contexts and TOEs. This marriage of structured, hierarchical standardization and flexible, tailored applicability underscores the pivotal role of SFCs in enabling, expressing, and validating the security posture of TOEs within the broader CC evaluation landscape.

## Security Assurance Components

Security Assurance Components (SACs) establish a systematic approach to validate the trustworthiness and efficacy of the security functions enacted by a TOE. Whereas Security Functional Components facilitate the definition and expression of security functions, SACs ensure that these are effectively enacted and verifiable, providing a reliable metric to gauge the TOE’s security posture against its claimed functionalities. These components assure that security functionalities, articulated through **Security Functional Requirements** are not only logically coherent but also practically viable and effective in mitigating identified [threats](./Threat.md) and aligning with [organizational security policies](./OrganizationalSecurityPolicy.md), thereby fulfilling Security Objectives.
In contrast to SFCs, at the terminus of SACs hierarchical structure, three distinct assurance elements emerge that collectively represent a [Security Assurance Requirement](./SecurityAssuranceRequirement.md):

- **Developer Action Elements** provide explicit instructions and expectations to developers to ensure security functionality is implemented and verified during development.
- **Content and Presentation Elements** dictate the manner and substance of how the developers should present the evaluation evidence, ensuring coherence, and relevancy to the evaluator. 
- **Evaluator Action Elements** provide a methodological baseline for the evaluators, guiding them on how to verify the evidence presented against the TOE’s claimed security functionality.

Moreover, SACs intrinsically intertwine with [Evaluation Methods and Activities](./EvaluationMethod.md), thereby establishing a symbiotic relationship that streamlines the TOE evaluation process. Particularly, Evaluator Action Elements serve as a nexus, directly linking SACs with Evaluation Methods through the specification of [Evaluation Actions](./EvaluationMethod.md) and corresponding [Work Units](./EvaluationMethod.md). These Work Units, which are either explicitly defined for Content and Presentation Elements or implicitly for Developer Action Elements, are paramount as they concretely delineate the evaluator's task.

In a manner akin to SFCs, SACs also facilitate the provision for Extended Components, enabling adaptability and relevance across multifaceted security landscapes and diverse TOEs.

## Extended Components

For Security Objectives that cannot be translated or only with great difficulty and/or complexity to SFRs using components defined in CC Part 2, or if there are third party requirements that cannot be translated to SARs using component in CC Part 3, new components can be defined. These components are referred to as Extended Components and provide context and meaning to allow the derivation and definition of Extended Security Requirements. Extended Components are evaluated against the [Extended Components Definition](./ExtendedComponentDefinition.md) (APE_ECD) and (ASE_ECD) assurance families (see CC Part 3) to determine their necessity, clearness, and unambiguity.

## Additional Resources

- **Common Criteria Part 1-3**
- **Common Evaluation Methodology**
- **ISO/IEC TR 15446**


## Related Articles

- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Extended Component Definition](./ExtendedComponentDefinition.md)
- [Evaluation Methods and Activities](./EvaluationMethod.md)
- [Security Target (ST)](./SecurityTarget.md)
- [Protection Profile (PP)](./ProtectionProfile.md)