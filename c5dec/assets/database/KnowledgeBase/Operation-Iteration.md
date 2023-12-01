# Operation - Iteration

**Acronym:** None

The iteration operation may be performed on every [component](./SecurityComponent.md). The author performs an iteration operation by including multiple [requirements](./SecurityRequirement.md) based on the same component. Each iteration of a component shall be different from all other iterations of that component, which is realized by completing [assignments](Operation-Assignment.md) and [selections](Operation-Selection.md) in a different way, or by applying [refinements](Operation-Refinement.md) to it in a different way.
Different iterations shall be uniquely identified to allow clear [rationales](./Rationale.md) and tracings to and from these requirements. Iteration identifiers should be meaningful to readers.

**NOTE** - Sometimes an iteration operation can be used with components where it is also possible to perform an assignment operation with a range or list of values instead of iterating them. In that case, the author can select the most appropriate alternative, considering if there is a necessity of providing a whole rationale for the range of values or if it is necessary to have a separate one for each of them. The author considers if individual traces are required for those values.