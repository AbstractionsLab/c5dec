# Cryptography

Cryptography-related features of C5-DEC CAD are not implemented for the current Alpha release, however, the following functions are included in our backlog candidates and are on the roadmap.

- Integration of one or more public-key encryption algorithms using a PQC solution, selected either from the NIST PQC 2022 selected algorithms or the ENISA post-quantum cryptography integration study of October 2022 by Daniel J. Bernstein (djb), Tanja Lange et al.

- Integration of a feature for cryptographically signing individual files and verifying digital signatures, e.g., via OpenPGP, to verify the authenticity of a file, with an additional option to sign using a digital signature algorithm either from NIST PQC 2022 selected algorithms or the ENISA post-quantum cryptography integration study October 2022.

In the meantime, we recommend using the well-known OpenPGP suite, and for the more technically proficient users, we recommend the suite of cryptographic software developed by Daniel J. Bernstein et al., e.g., [NACL](https://nacl.cr.yp.to/), [libpqcrypto](https://libpqcrypto.org/); it is also worth mentioning the [Open Quantum Safe](https://openquantumsafe.org/) project.

Our future implementations will be building on such endeavors, but with a preference for building on top of verified cryptographic implementations, e.g., see [EverCrypt](https://www.microsoft.com/en-us/research/publication/evercrypt-a-fast-veri%EF%AC%81ed-cross-platform-cryptographic-provider/) and [HACL*](https://hacl-star.github.io/HaclValeEverCrypt.html).