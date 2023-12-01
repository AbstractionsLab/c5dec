---
AppNotes: |
  This component requires the PP or ST author to fill in an assignment with the subset of the TSF. This subset may be identified in terms of the internals of the TSF at any layer of abstraction. For example: a) the structural elements of the TSF as identified in the TOE design (e.g. "The developer shall design and implement the audit subsystem such that it has well-structured internals."); b) the implementation (e.g. “The developer shall design and implement the encrypt.c and decrypt.c files such that it has well-structured internals.” or “The developer shall design and implement the 6227 IC chip such that it has well-structured internals.”). It is likely this would not be readily accomplished by referencing the claimed SFRs (e.g. “The developer shall design and implement the portion of the TSF that provide anonymity as defined in FPR_ANO.2 such that it has well-structured internals.”) because this does not indicate where to focus the analysis. This component has limited value and would be suitable in cases where potentially-malicious users/subjects have limited or strictly controlled access to the TSFIs or where there is another means of protection (e.g. domain separation) that ensures the chosen subset of the TSF cannot be adversely affected by the rest of the TSF (e.g. the cryptographic functionality, which is isolated from the rest of the TSF, is well-structured).
Dependencies: |
  ADV_IMP.1 Implementation representation of the TSF, ADV_TDS.3 Basic modular design, ALC_TAT.1 Well-defined development tools
Id: ADV_INT.1
Name: Well-structured subset of TSF internals
Objectives: |
  The objective of this component is to provide a means for requiring specific portions of the TSF to be well-structured. The intent is that the entire TSF has been designed and implemented using sound engineering principles, but the analysis is performed upon only a specific subset.
active: true
derived: false
level: 1.38
links:
- AFML-025: N2dDVSyfxTNh_dRU0zO2XmOPhjrU4yIN7WrRt64odcc=
normative: true
ref: ''
reviewed: 0WbS70bu2UxaBg8fDAujQhwEobP2ZEXS1fI-1KFrZDc=
---

# ADV_INT.1 Well-structured subset of TSF internals