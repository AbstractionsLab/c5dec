FROM python:3.11-bookworm

ARG MY_ENV

ENV MY_ENV=${MY_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.8.3

ENV user=alab
ENV c5folder=c5dec

# Mermaid CLI: use system Chromium instead of downloading its own
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Define an argument for the architecture
ARG ARCH

# Set the default value for the architecture argument
ARG ARCH=amd64

# Update and install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git python3-pip graphviz sudo curl gnupg2 chromium unzip wget && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x via GPG-verified NodeSource repository
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" \
        | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Mermaid CLI for rendering Mermaid diagrams in specs
RUN npm install -g @mermaid-js/mermaid-cli

# Download and install TeX Live
RUN wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz && \
    tar -xzf install-tl-unx.tar.gz && \
    cd install-tl-20* && \
    echo "selected_scheme scheme-basic" > texlive.profile && \
    ./install-tl --profile=texlive.profile && \
    TEXLIVE_YEAR=$(ls /usr/local/texlive/ | grep -E '^[0-9]{4}$' | sort -n | tail -1) && \
    ln -s /usr/local/texlive/${TEXLIVE_YEAR}/bin/$(uname -m)-linux /usr/local/texlive/active-bin && \
    cd / && rm -rf /install-tl-unx.tar.gz /install-tl-20*

# Set the Quarto version
ENV QUARTO_VERSION=1.6.43

# Download and install the appropriate Quarto package, Kryptor and Cryptomator-CLI binaries based on system architecture
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "arm64" ]; then \
        apt-get update && \
        apt-get install -y --no-install-recommends gdebi-core && \
        rm -rf /var/lib/apt/lists/* && \
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-arm64.deb && \
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-checksums.txt && \
        grep "quarto-${QUARTO_VERSION}-linux-arm64.deb" quarto-${QUARTO_VERSION}-checksums.txt | sha256sum -c - && \
        gdebi -n quarto-${QUARTO_VERSION}-linux-arm64.deb && \
        rm quarto-${QUARTO_VERSION}-linux-arm64.deb quarto-${QUARTO_VERSION}-checksums.txt && \
        apt-get remove -y gdebi-core && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*; \
        # Download and install Kryptor for ARM64
        cd /tmp && \
        wget https://github.com/samuel-lucas6/Kryptor/releases/latest/download/kryptor-linux-arm64.zip || { echo "Failed to download Kryptor"; } && \
        unzip kryptor-linux-arm64.zip -d kryptor-linux-arm64 || { echo "Failed to unzip Kryptor"; } && \
        rm kryptor-linux-arm64.zip && \
        chmod +x ./kryptor-linux-arm64/kryptor || { echo "Failed to make Kryptor executable"; exit 1; } && \
        mv ./kryptor-linux-arm64/kryptor /usr/local/bin/kryptor || { echo "Failed to move Kryptor"; exit 1; } && \
        rm -rf ./kryptor-linux-arm64; \
        # Download and install Cryptomator CLI for ARM64
        cd /tmp && \
        wget https://github.com/cryptomator/cli/releases/download/0.6.2/cryptomator-cli-0.6.2-linux-aarch64.zip || { echo "Failed to download Cryptomator CLI"; } && \
        unzip cryptomator-cli-0.6.2-linux-aarch64.zip -d cryptomator-cli-0.6.2-linux-aarch64 || { echo "Failed to unzip Cryptomator CLI"; } && \
        rm cryptomator-cli-0.6.2-linux-aarch64.zip && \
        mv ./cryptomator-cli-0.6.2-linux-aarch64/cryptomator-cli /usr/local/bin/ || { echo "Failed to move Cryptomator CLI"; } && \
        ln -s /usr/local/bin/cryptomator-cli/bin/cryptomator-cli /usr/local/bin/cryptomator || { echo "Failed to create symlink for Cryptomator CLI"; } && \
        rm -rf ./cryptomator-cli-0.6.2-linux-aarch64; \
    elif [ "$ARCH" = "amd64" ]; then \
        apt-get update && \
        apt-get install -y --no-install-recommends gdebi-core && \
        rm -rf /var/lib/apt/lists/* && \
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb && \
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-checksums.txt && \
        grep "quarto-${QUARTO_VERSION}-linux-amd64.deb" quarto-${QUARTO_VERSION}-checksums.txt | sha256sum -c - && \
        gdebi -n quarto-${QUARTO_VERSION}-linux-amd64.deb && \
        rm quarto-${QUARTO_VERSION}-linux-amd64.deb quarto-${QUARTO_VERSION}-checksums.txt && \
        apt-get remove -y gdebi-core && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*; \
        # Download and install Kryptor for AMD64
        cd /tmp && \
        wget https://github.com/samuel-lucas6/Kryptor/releases/latest/download/kryptor-linux-x64.zip || { echo "Failed to download Kryptor"; } && \
        unzip kryptor-linux-x64.zip -d kryptor-linux-x64 || { echo "Failed to unzip Kryptor"; } && \
        rm kryptor-linux-x64.zip && \
        chmod +x ./kryptor-linux-x64/kryptor || { echo "Failed to make Kryptor executable"; exit 1; } && \
        mv ./kryptor-linux-x64/kryptor /usr/local/bin/kryptor || { echo "Failed to move Kryptor"; exit 1; } && \
        rm -rf ./kryptor-linux-x64; \
        # Download and install Cryptomator CLI for AMD64
        cd /tmp && \
        wget https://github.com/cryptomator/cli/releases/download/0.6.2/cryptomator-cli-0.6.2-linux-x64.zip || { echo "Failed to download Cryptomator CLI"; } && \
        unzip cryptomator-cli-0.6.2-linux-x64.zip -d cryptomator-cli-0.6.2-linux-x64 || { echo "Failed to unzip Cryptomator CLI"; } && \
        rm cryptomator-cli-0.6.2-linux-x64.zip && \
        mv ./cryptomator-cli-0.6.2-linux-x64/cryptomator-cli /usr/local/bin/ || { echo "Failed to move Cryptomator CLI"; } && \
        ln -s /usr/local/bin/cryptomator-cli/bin/cryptomator-cli /usr/local/bin/cryptomator || { echo "Failed to create symlink for Cryptomator CLI"; } && \
        rm -rf ./cryptomator-cli-0.6.2-linux-x64; \
    else \
        echo "Unsupported architecture: $ARCH"; \
        exit 1; \
    fi

# Add TeX Live to the PATH
ENV PATH="/usr/local/texlive/active-bin:$PATH"

# Install the required fonts for Quarto and TeX Live
# fc-cache updates the system font cache; luaotfload-tool rebuilds LuaTeX's own
# font DB so that fontspec/luaotfload can resolve "Ubuntu" at render time.
RUN cd /tmp && \
    wget https://assets.ubuntu.com/v1/0cef8205-ubuntu-font-family-0.83.zip && \
    unzip 0cef8205-ubuntu-font-family-0.83.zip -d ubuntu-fonts && \
    mkdir -p /usr/local/share/fonts/ubuntu && \
    cp ./ubuntu-fonts/ubuntu-font-family-0.83/*.ttf /usr/local/share/fonts/ubuntu/ && \
    chmod 644 /usr/local/share/fonts/ubuntu/*.ttf && \
    fc-cache -fv && \
    luaotfload-tool --update --force && \
    rm -rf /tmp/ubuntu-fonts /tmp/0cef8205-ubuntu-font-family-0.83.zip

# Install Doorstop
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath

# Create a non-root user with no password; grant passwordless sudo via sudoers.d
RUN useradd -ms /bin/bash ${user} && \
    usermod -aG sudo ${user} && \
    echo "alab ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/alab && \
    chmod 440 /etc/sudoers.d/alab && \
    chown -R ${user}:${user} /usr/local/texlive

# Add location where pip is installed to the PATH variable
ENV PATH="/home/${user}/.local/bin:${PATH}"

# Copy the files and install the python environment as user alab 
USER ${user}
RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /home/${user}/${c5folder}
COPY poetry.lock pyproject.toml /home/${user}/${c5folder}/

# Create folders, and files for a project
COPY . /home/${user}/${c5folder}

# Project initialization
RUN poetry install

# Install python virtual environment for the project
WORKDIR /home/${user}/${c5folder}/${c5folder}

# Install Doorstop and organize-tool
RUN pipx install doorstop==3.0b10
RUN pipx install organize-tool==2.4.3

WORKDIR /home/${user}/${c5folder}/${c5folder}
CMD ["poetry", "shell"]