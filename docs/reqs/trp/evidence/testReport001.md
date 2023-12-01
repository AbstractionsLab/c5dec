

# FDP User data protection



## FC-INTRODUCTION

This class contains families specifying requirements related to protecting user data. [fdp]() is split into four groups of families (listed below) that address user data within a TOE, during import, export, and storage as well as security attributes directly related to user data.
The families in this class are organised into four groups:
1. User data protection security function policies:
-  [fdp_acc]() ; and
-  [fdp_ifc]() .
Components in these families permit the PP/ST author to name the user data protection security function policies and define the scope of control of the policy, necessary to address the security objectives. The names of these policies are meant to be used throughout the remainder of the functional components that have an operation that calls for an assignment or selection of an "access control SFP" or an "information flow control SFP". The rules that define the functionality of the named access control and information flow control SFPs will be defined in the [fdp_acf]() and [fdp_iff]() families (respectively).
2. Forms of user data protection:
-  [fdp_acf]() ;
-  [fdp_iff]() ;
-  [fdp_itt]() ;
-  [fdp_rip]() ;
-  [fdp_rol]() ; and
-  [fdp_sdi]() .

3. Off-line storage, import and export:
-  [fdp_dau]() ;
-  [fdp_etc]() ;
-  [fdp_itc]() .
Components in these families address the trustworthy transfer into or out of the TOE.
4. Inter-TSF communication:
-  [fdp_uct]() ; and
-  [fdp_uit]() .
Components in these families address communication between the TSF of the TOE and another trusted IT product.



## FC-INFORMATIVE-NOTES

This class contains families specifying requirements related to protecting user data. This class differs from FIA and FPT in that [fdp]() specifies components to protect user data, FIA specifies components to protect attributes associated with the user, and FPT specifies components to protect TSF information.
The class does not contain explicit requirements for traditional Mandatory Access Controls (MAC) or traditional Discretionary Access Controls (DAC); however, such requirements may be constructed using components from this class.
 [fdp]() does not explicitly deal with confidentiality, integrity, or availability, as all three are most often intertwined in the policy and mechanisms. However, the TOE security policy must adequately cover these three objectives in the PP/ST.
A final aspect of this class is that it specifies access control in terms of ``operations''. An operation is defined as a specific type of access on a specific object. It depends on the level of abstraction of the PP/ST author whether these operations are described as ``read'' and/or ``write'' operations, or as more complex operations such as ``update the database''.
The access control policies are policies that control access to the information container. The attributes represent attributes of the container. Once the information is out of the container, the accessor is free to modify that information, including writing the information into a different container with different attributes. By contrast, an information flow policies controls access to the information, independent of the container. The attributes of the information, which may be associated with the attributes of the container (or may not, as in the case of a multi-level database) stay with the information as it moves. The accessor does not have the ability, in the absence of an explicit authorisation, to change the attributes of the information.
This class is not meant to be a complete taxonomy of IT access policies, as others can be imagined. Those policies included here are simply those for which current experience with actual systems provides a basis for specifying requirements. There may be other forms of intent that are not captured in the definitions here.
For example, one could imagine a goal of having user-imposed (and user-defined) controls on information flow (e.g. an automated implementation of the NO FOREIGN handling caveat). Such concepts could be handled as refinements of, or extensions to the [fdp]() components.
Finally, it is important when looking at the components in [fdp]() to remember that these components are requirements for functions that may be implemented by a mechanism that also serves or could serve another purpose. For example, it is possible to build an access control policy ( [fdp_acc]() ) that uses labels ( [fdp_iff.1]() ) as the basis of the access control mechanism.
A set of SFRs may encompass many security function policies (SFPs), each to be identified by the two policy oriented components [fdp_acc]() , and [fdp_ifc]() . These policies will typically take confidentiality, integrity, and availability aspects into consideration as required, to satisfy the TOE requirements. Care should be taken to ensure that all objects are covered by at least one SFP and that there are no conflicts arising from implementing the multiple SFPs.
When building a PP/ST using components from the [fdp]() class, the following information provides guidance on where to look and what to select from the class.
The requirements in the [fdp]() class are defined in terms of a set of SFRs that will implement a SFP. Since a TOE may implement multiple SFPs simultaneously, the PP/ST author must specify the name for each SFP, so it can be referenced in other families. This name will then be used in each component selected to indicate that it is being used as part of the definition of requirements for that SFP. This allows the author to easily indicate the scope for operations such as objects covered, operations covered, authorised users, etc.
Each instantiation of a component can apply to only one SFP. Therefore if an SFP is specified in a component then this SFP will apply to all the elements in this component. The components may be instantiated multiple times within a PP/ST to account for different policies if so desired.
The key to selecting components from this family is to have a well defined set of TOE security objectives to enable proper selection of the components from the two policy components; [fdp_acc]() and [fdp_ifc]() . In [fdp_acc]() and [fdp_ifc]() respectively, all access control policies and all information flow control policies are named. Furthermore the scope of control of these components in terms of the subjects, objects and operations covered by this security functionality. The names of these policies are meant to be used throughout the remainder of the functional components that have an operation that calls for an assignment or selection of an ``access control SFP'' or an ``information flow control SFP''. The rules that define the functionality of the named access control and information flow control SFPs will be defined in the [fdp_acf]() and [fdp_iff]() families (respectively).
The following steps are guidance on how this class is applied in the construction of a PP/ST:
1. Identify the policies to be enforced from the [fdp_acc]() , and [fdp_ifc]() families. These families define scope of control for the policy, granularity of control and may identify some rules to go with the policy.
2. Identify the components and perform any applicable operations in the policy components. The assignment operations may be performed generally (such as with a statement ``All files'') or specifically (``The files ``A'', ``B'', etc.) depending upon the level of detail known.
3. Identify any applicable function components from the [fdp_acf]() and [fdp_iff]() families to address the named policy families from [fdp_acc]() and [fdp_ifc]() . Perform the operations to make the components define the rules to be enforced by the named policies. This should make the components fit the requirements of the selected function envisioned or to be built.
4. Identify who will have the ability to control and change security attributes under the function, such as only a security administrator, only the owner of the object, etc. Select the appropriate components from [fmt]() and perform the operations. Refinements may be useful here to identify missing features, such as that some or all changes must be done via trusted path.
5. Identify any appropriate components from the [fmt]() for initial values for new objects and subjects.
6. Identify any applicable rollback components from the [fdp_rol]() family.
7. Identify any applicable residual information protection requirements from the [fdp_rip]() family.
8. Identify any applicable import or export components, and how security attributes should be handled during import and export, from the [fdp_itc]() and [fdp_etc]() families.
9. Identify any applicable internal TOE communication components from the [fdp_itt]() family.
10. Identify any requirements for integrity protection of stored information from the [fdp_sdi]() .
11. Identify any applicable inter-TSF communication components from the [fdp_uct]() or [fdp_uit]() families.



## FDP_ACC Access control policy



### FF-BEHAVIOUR

This family identifies the access control SFPs (by name) and defines the scope of control of the policies that form the identified access control portion of the SFRs related to the SFP. This scope of control is characterised by three sets: the subjects under control of the policy, the objects under control of the policy, and the operations among controlled subjects and controlled objects that are covered by the policy. The criteria allows multiple policies to exist, each having a unique name. This is accomplished by iterating components from this family once for each named access control policy. The rules that define the functionality of an access control SFP will be defined by other families such as [fdp_acf]() and [fdp_etc]() . The names of the access control SFPs identified here in [fdp_acc]() are meant to be used throughout the remainder of the functional components that have an operation that calls for an assignment or selection of an ``access control SFP.''


### FF-USER-NOTES

This family is based upon the concept of arbitrary controls on the interaction of subjects and objects. The scope and purpose of the controls is based upon the attributes of the accessor (subject), the attributes of the container being accessed (object), the actions (operations) and any associated access control rules.
The components in this family are capable of identifying the access control SFPs (by name) to be enforced by the traditional Discretionary Access Control (DAC) mechanisms. It further defines the subjects, objects and operations that are covered by identified access control SFPs. The rules that define the functionality of an access control SFP will be defined by other families, such as [fdp_acf]() and [fdp_etc]() . The names of the access control SFPs defined in [fdp_acc]() are meant to be used throughout the remainder of the functional components that have an operation that calls for an assignment or selection of an ``access control SFP.''
The access control SFP covers a set of triplets: subject, object, and operations. Therefore a subject can be covered by multiple access control SFPs but only with respect to a different operation or a different object. Of course the same applies to objects and operations.
A critical aspect of an access control function that enforces an access control SFP is the ability for users to modify the attributes involved in access control decisions. The [fdp_acc]() family does not address these aspects. Some of these requirements are left undefined, but can be added as refinements, while others are covered elsewhere in other families and classes such as [fmt]() .
There are no audit requirements in [fdp_acc]() as this family specifies access control SFP requirements. Audit requirements will be found in families specifying functions to satisfy the access control SFPs identified in this family.
This family provides a PP/ST author the capability to specify several policies, for example, a fixed access control SFP to be applied to one scope of control, and a flexible access control SFP to be defined for a different scope of control. To specify more than one access control policy, the components from this family can be iterated multiple times in a PP/ST to different subsets of operations and objects. This will accommodate TOEs that contain multiple policies, each addressing a particular set of operations and objects. In other words, the PP/ST author should specify the required information in the ACC component for each of the access control SFPs that the TSF will enforce. For example, a TOE incorporating three access control SFPs, each covering only a subset of the objects, subjects, and operations within the TOE, will contain one [fdp_acc.1]() component for each of the three access control SFPs, necessitating a total of three [fdp_acc.1]() components.
