---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5
---

# TOE Boundary

**Acronym:** None

The TOE Boundary determines the physical and logical scope of the [TOE](TargetofEvaluation.md). All parts of an IT product that are not within the TOE Boundary are outside the scope of the evaluation.

## Understanding the TOE Boundary

Defining where your Target of Evaluation (TOE) starts and ends is crucial in the evaluation process. The TOE Boundary encompasses both physical and logical aspects and serves as a demarcation line that outlines the scope of the TOE when it’s handed to the customer.

Imagine you’re evaluating a secure messaging app. The TOE Boundary may include the app itself and its integrated encryption technology but exclude the mobile device or network it operates on.

## Why is it Significant?

Identifying the TOE Boundary is pivotal for a few reasons:

- **Scope Definition**: It clearly establishes what is being evaluated and what is not.
- **Risk Management**: By understanding what's inside the boundary, we can better manage and evaluate the associated risks.
- **Resource Allocation**: Ensures resources are focused on relevant areas during evaluation.

## What’s Inside and Outside?

Everything within the TOE Boundary is subject to evaluation under the Common Criteria. Conversely, elements outside the TOE Boundary are deemed part of the TOE’s operational environment and are considered during the evaluation but not tested.

**Inside the TOE Boundary**:
- Software components actively participating in security functions.
- Hardware that is part of the TOE.
- Security mechanisms employed by the TOE.

**Outside the TOE Boundary**:
- External systems interacting with the TOE.
- Network infrastructure.
- Non-TOE hardware and software components.

## Practical Guidance

### Defining the TOE Boundary:

1. **Clarity is Key**: Ensure that boundaries are defined in a clear and unambiguous manner.
2. **Detailed Documentation**: Provide thorough documentation highlighting what is included and excluded from the TOE, and justify the exclusions.
3. **Security Functions**: Clearly document how each component within the TOE Boundary contributes to the TOE’s security functionality.
4. **External Interaction**: Understand and document how the TOE interacts with elements outside the boundary.


## Additional Resources

- [Understandning TOE Operational Environement](./TOEOperationalEnvironment.md)
- [Understanding Target of Evaluation](./TargetofEvaluation.md)

## Related Articles

- [Security Target (ST)](./SecurityTarget.md)
- [Protection Profile (PP)](./ProtectionProfile.md)