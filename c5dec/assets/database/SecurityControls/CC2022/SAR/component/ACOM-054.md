---
AppNotes: ''
Dependencies: |
  ALC_CMS.1 TOE CM coverage, ALC_DVS.1 Identification of security measures, ALC_LCD.1 Developer defined life-cycle processes
Id: ALC_CMC.3
Name: Authorization controls
Objectives: |
  A unique reference is required to ensure that there is no ambiguity in terms of which instance of the TOE is being evaluated. Labelling the TOE with its reference ensures that users of the TOE can be aware of which instance of the TOE they are using. Unique identification of the configuration items leads to a clearer understanding of the composition of the TOE, which in turn helps to determine those items which are subject to the evaluation requirements for the TOE. The use of a CM system increases assurance that the configuration items are maintained in a controlled manner. Providing controls to ensure that unauthorised modifications are not made to the TOE (“CM access control”) and ensuring proper functionality and use of the CM system, helps to maintain the integrity of the TOE.
active: true
derived: false
level: 1.53
links:
- AFML-031: DvtRRt2fY1-7dzrpm3a-U_vpxJEP1_Z_eaJ6dmfugQw=
normative: true
ref: ''
reviewed: XwpHSilIDNc6gZEzT5iOefMmV2H65hX1cJU2cDFoQyU=
---

# ALC_CMC.3 Authorization controls

A life-cycle model encompasses the procedures, tools and techniques used to develop and maintain the TOE. Aspects of the process that may be covered by such a model include design methods, review procedures, project management controls, change control procedures, test methods and acceptance procedures. An effective life-cycle model will address these aspects of the development and maintenance process within an overall management structure that assigns responsibilities and monitors progress. There are different types of acceptance situations that are dealt with at different locations in the criteria: — acceptance of parts delivered by subcontractors (“integration”) should be treated in this family, — Development Life-cycle definition (ALC_LCD), — acceptance subsequent to internal transportations in Developer environment security (ALC_DVS), — acceptance of parts into the CM system in CM capabilities (ALC_CMC), and — acceptance of the delivered TOE by the consumer in Delivery (ALC_DEL). The first three types may overlap. Although life-cycle definition deals with the maintenance of the TOE and hence with aspects becoming relevant after the completion of the evaluation, its evaluation adds assurance through an analysis of the life-cycle information for the TOE provided at the time of the evaluation. A life-cycle model provides for the necessary control over the development and maintenance of the TOE, if the model enables sufficient minimisation of the danger that the TOE will not meet its security requirement. A measurable life-cycle model is a model using some quantitative valuation (arithmetic parameters and/or metrics) of the managed product in order to measure development properties of the product. Typical metrics are source code complexity metrics, defect density (errors per size of code) or mean time to failure. For the security evaluation all those metrics are of relevance, which are used to increase quality by decreasing the probability of faults and thereby in turn increasing assurance in the security of the TOE. One should take into account that there exist standardised life-cycle models on the one hand (like the waterfall model) and standardised metrics on the other hand (like error density), which may be combined. The CC does not require the life-cycle to follow exactly one standard defining both aspects.