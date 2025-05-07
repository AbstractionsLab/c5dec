# Cryptography

## Classical cryptography

Cryptography-related features of C5-DEC CAD are implemented via the integration of cryptographic software into the C5-DEC containerized development environment, i.e., via  the [development Dockerfile](https://github.com/AbstractionsLab/c5dec/blob/main/dev.Dockerfile) along with the VS Code [devcontainer.json](https://github.com/AbstractionsLab/c5dec/blob/main/.devcontainer/devcontainer.json) file. Please see the corresponding user manual [installation instructions](https://github.com/AbstractionsLab/c5dec/blob/main/docs/manual/installation.md#installation-in-a-containerized-development-environment) for more details.

The C5-DEC dev container (loaded in VS Code via the `dev.Dockerfile` specification), currently integrates the following pieces of cryptographic software for both `amd64` and `arm64` architectures:

- [GnuPG](https://gnupg.org/): installed in the C5-DEC dev container and directly accessible via the shell; you can run verify this, e.g., by running `gpg -h`. 
- [Kryptor](https://www.kryptor.co.uk/): installed in the C5-DEC dev container and directly accessible via the shell; you can verify e.g., by running `kryptor -h` for help.
- [Cryptomator CLI](https://github.com/cryptomator/cli): for unlocking and mounting already existing [Cryptomator](https://github.com/cryptomator/cryptomator) vaults (used for secure cloud storage); you can verify e.g., by running `cryptomator -h` for help.

To use the integrated cryptographic software, you can either run an interactive C5-DEC session using the `c5dec.sh` runner script:

```sh
./c5dec.sh session
```

Alternatively, open the the project repository in VS Code and select the "Reopen in Container" option in the notification that pops up in VS Code; or launch the command palette (Cmd/Ctrl+Shift+P) and select "Dev Containers: Reopen in Container" from the list of available commands. You will then be prompted to select a dev container configuration: the `C5-DEC CAD dev container` provides the bulk of the cryptographic functionality except for PQC support (see below).

## Post-quantum cryptography (PQC)

Finally, regarding **post-quantum cryptography (PQC)**, we currently support the use of a dedicated Docker container providing `OpenSSL` coupled with the `OQS-OpenSSL provider` from the [Open Quantum Safe](https://openquantumsafe.org/) project, powered by the `liboqs` library. The runner and its volume mapping provide an environment with [OpenSSL](https://docs.openssl.org/master/man7/ossl-guide-libcrypto-introduction/) and the [OQS-OpenSSL provider](https://github.com/open-quantum-safe/oqs-provider) preinstalled.

To use the PQC-enabled container, you can run an interactive C5-DEC session using the `c5dec.sh` runner script and the `pqc` argument:

```sh
./c5dec.sh pqc
```

Alternatively, you can use the `C5-DEC CAD cryptography dev container` option in VS Code.

See the user manual page providing instructions on how to [run the OQS-OpenSSL dev container in VS Code](./installation.md#c5-dec-post-quantum-cryptography-dev-container) for more details.

Once the container is running, you can use the `openssl` command line tool to generate and verify signatures, encrypt and decrypt messages, etc. This allows you to use post-quantum cryptography algorithms while benefitting from direct access to your host file system (thanks to volume mounting) such that files created or modified while using the `C5-DEC CAD dev container` remain accessible when using the `C5-DEC cryptography dev container`. To use the OQS-OpenSSL provider, we recommend consulting the [OQS-OpenSSL usage documentation](https://github.com/open-quantum-safe/oqs-provider/blob/main/USAGE.md#sample-commands).

For instance, to get a list of the available quantum-safe signature algorithms, you can run the following command in the terminal:

```sh
openssl list -signature-algorithms -provider oqsprovider
```

Similarly, to get a list of the available quantum-safe KEM algorithms, you can run:

```sh
openssl list -kem-algorithms -provider oqsprovider
```

## Post-Quantum end-to-end tunnels

When it comes to PQC-enabled network endpoints, we recommend the [PQConnect](https://www.pqconnect.net/) software developed by Daniel J. Bernstein et al.

Technical details can be found in the [PQConnect paper](https://www.pqconnect.net/pqconnect-20241206.pdf).

## Roadmap

Our future releases are expected to build on improved versions of the above-mentioned dependencies, with a preference for building on top of verified cryptographic implementations, e.g., see [EverCrypt](https://www.microsoft.com/en-us/research/publication/evercrypt-a-fast-veri%EF%AC%81ed-cross-platform-cryptographic-provider/) and [HACL*](https://hacl-star.github.io/HaclValeEverCrypt.html).