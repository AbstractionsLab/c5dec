# Exact conformance - FAQ

The table below gives a summary of frequently asked questions about the exact confromance case.

  ----------------------------------------------------------------------------------------------------------------------------------
  PP-Configuration                                                                               Allowed/Required
  ---------------------------------------------------------------------------------------------- -----------------------------------
  Can be used in multi-assurance - modular PP-Configuration                                      Yes

  Can be used in single-assurance - modular PP- Configuration                                    Yes

  Can mix EC with strict/demonstrable conformance types                                          No

  Other EC PPs allowed in EC PP-Configuration                                                    Yes

                                                                                                 

  **EC PP**                                                                                      

  Optional/Selection-based SFRs in EC PP                                                         Yes

  Additional SPD elements associated with optional SFRs                                          Yes

  EC PP claim conformance to another EC PP? (Chained)                                            No

  Other EC PPs allowed in EC PP-Configuration                                                    Yes

  PP build upon strict or demonstrable PP?                                                       No

  Can be used in strict or demonstrable PP-Configuration?                                        No

  States which other EC PPs are "Allowed-with"                                                   Yes

  States which other EC PP-Modules are "Allowed-with"                                            Yes

                                                                                                 

  **EC PP-Modules**                                                                              

  Optional/Selection-based SFRs in EC PP-Module                                                  Yes

  EC PP-Module doesn't include components in its PP-Module Base in its allowed-with statement.   Yes

  States other EC PPs and PP-Modules are allowed-with                                            Yes

  All Allowed-with items also EC                                                                 Yes

                                                                                                 

  **EC functional Packages**                                                                     

  Optional/Selection-based SFRs allowed in EC functional Package                                 Yes

  Functional packages can be augmented in the ST                                                 No

  Are claimed in a ST conformance claim                                                          No

                                                                                                 

  **EC STs**                                                                                     

  Contains the SPD of all EC PPs, and/or PP-Configuration components                             Yes

  Additional or hierarchically higher security requirements?                                     No

  Includes only those selection-based requirements that have been selected                       Yes

  Can be used with Direct Rationale approach                                                     Yes
  ----------------------------------------------------------------------------------------------------------------------------------