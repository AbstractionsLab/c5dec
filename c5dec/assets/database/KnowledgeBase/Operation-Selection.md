# Operation - Selection

**Acronym:** None

The selection operation occurs where a given [component](./SecurityComponent.md) contains an element where a choice from several items has to be made by the author.
Whenever an element in a [PP](./ProtectionProfile.md), [PP-Module](./PP-Module.md) or[Package](./Package.md) contains a selection, the author may do one of three things:
1. leave the selection uncompleted;
2. complete the selection by choosing one or more items;
3. restrict the selection by removing some of the choices but leaving two or more.
Whenever an element in a PP, PP-Module or package contains a selection, a [ST](./SecurityTarget.md) author shall complete that selection, as indicated in 2. above. Options 1. and 3. are not allowed for STs.
The item or items chosen in 2. and 3. shall be taken from the items provided in the selection.

**Note** - "None" is only available as a choice for the completion of a selection if explicitly provided;
The lists provided for the completion of selections shall be non-empty. If a "None" option is chosen, no additional selection options may be chosen. If "None" is not given as an option in a selection, it is permissible to combine the choices in a selection with "and"s and "or"s, unless the selection explicitly states "choose one of".
Selection operations may be combined by iteration where needed. In this case, the applicability of the option chosen for each iteration should not overlap the subject of the other iterated selection, since they are intended to be exclusive.