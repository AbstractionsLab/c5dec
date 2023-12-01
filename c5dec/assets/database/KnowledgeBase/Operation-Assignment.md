# Operation - Assignment

**Acronym:** None

An assignment operation occurs where a given [security requirement](./SecurityRequirement.md) contains an element with a parameter that may be set by the author. The parameter may be an unrestricted variable, or a rule that narrows the variable to a specific range of values.
Whenever an element in a [PP](../CoreConstructs/ProtectionProfile.md), [PP-Module](./PP-Module.md) or [Package](./Package.md) within a PP/PP-Module contains an assignment, the author shall do one of four things:
1. leave the assignment uncompleted;
2. complete the assignment;
3. narrow the assignment to further limit the range of values that is allowed;
4. transform the assignment to a selection, thereby narrowing the assignment."

An [ST](./SecurityTarget.md) author shall complete all the assignments.
The values chosen in options 2., and 4. shall conform to the indicated type required by the assignment.
When an assignment is to be completed with a set, an author should provide a description of the set from which the elements of the set may be derived as long as it is clear which subjects are meant.

**Note** - for the completion of assignments, the CC Part 2 annexes shall be consulted in order to determine when "None" would be a valid completion.