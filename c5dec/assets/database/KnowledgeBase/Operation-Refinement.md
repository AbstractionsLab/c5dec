# Operation - Refinement

**Acronym:** None

The refinement operation may be performed on every [requirement](./SecurityRequirement.md). The author performs a refinement by altering that requirement.

**NOTE 1** A series of refined iteration operations can be used to cover all of the subjects, objects, operations, security attributes and/or external entities, but where each individual refinement does not.

The first rule for a refinement is that a [TOE](TargetofEvaluation.md) meeting the refined requirement also meets the unrefined requirement in the context of the [PP](./ProtectionProfile.md), [PP-Module](./PP-Module.md), [Package](./Package.md) or [ST](./SecurityTarget.md), i.e. a refined requirement shall be "stricter" than the original requirement. If a refinement does not meet this rule, the resulting refined requirement is considered to be an [extended requirement](ExtendedSecurityRequirement.md) and shall be treated as such.

The only exception to this rule is that an author can refine a [SFR](SecurityFunctionalRequirement.md) to apply to some but not all subjects, objects, operations, security attributes and/or external entities. However, this exception does not apply to refining SFRs that are taken from PPs, PP-Modules or package to which [conformance](./ConformanceClaims.md) is being claimed; these SFRs shall not be refined to apply to fewer subjects, objects, operations, security attributes and/or external entities than the SFR in the originating PP, PP-Module or package.

The second rule for a refinement is that the refinement shall be related to the original [component](./SecurityComponent.md).
A special case of refinement is an editorial refinement, where a small change may be made in a requirement, i.e. rephrasing a sentence due to adherence to proper English grammar, or to make it more understandable to the reader. This change is not allowed to modify the meaning of the requirement in any way.