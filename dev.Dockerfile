FROM python:3.8

ARG MY_ENV

ENV MY_ENV=${MY_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.0

ENV user=alab
ENV c5folder=c5dec

# Define an argument for the architecture
ARG ARCH

# Set the default value for the architecture argument
ARG ARCH=amd64

# Update and install dependencies
RUN apt update --fix-missing
RUN apt-get install -y git python3-pip graphviz sudo

# Update the package list and install dependencies
RUN apt-get install -y wget gdebi-core

# Download and install TeX Live
RUN wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz && \
    tar -xzf install-tl-unx.tar.gz && \
    cd install-tl-20* && \
    echo "selected_scheme scheme-basic" > texlive.profile && \
    ./install-tl --profile=texlive.profile

# Set the Quarto version
ENV QUARTO_VERSION=1.6.43

# Download and install the appropriate Quarto package, Kryptor and Cryptomator-CLI binaries based on system architecture
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "arm64" ]; then \
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-arm64.deb && \
        gdebi -n quarto-${QUARTO_VERSION}-linux-arm64.deb && \
        rm quarto-${QUARTO_VERSION}-linux-arm64.deb; \
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
        # chmod +x ./cryptomator-cli-0.6.2-linux-aarch64/cryptomator-cli/cryptomator-cli || { echo "Failed to make Cryptomator CLI executable"; exit 1; } && \
        mv ./cryptomator-cli-0.6.2-linux-aarch64/cryptomator-cli /usr/local/bin/ || { echo "Failed to move Cryptomator CLI"; } && \
        ln -s /usr/local/bin/cryptomator-cli/bin/cryptomator-cli /usr/local/bin/cryptomator || { echo "Failed to create symlink for Cryptomator CLI"; } && \
        rm -rf ./cryptomator-cli-0.6.2-linux-aarch64; \
    elif [ "$ARCH" = "amd64" ]; then \
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb && \
        gdebi -n quarto-${QUARTO_VERSION}-linux-amd64.deb && \
        rm quarto-${QUARTO_VERSION}-linux-amd64.deb; \
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
        # chmod +x ./cryptomator-cli-0.6.2-linux-x64/cryptomator-cli/cryptomator-cli || { echo "Failed to make Cryptomator CLI executable"; exit 1; } && \
        mv ./cryptomator-cli-0.6.2-linux-x64/cryptomator-cli /usr/local/bin/ || { echo "Failed to move Cryptomator CLI"; } && \
        ln -s /usr/local/bin/cryptomator-cli/bin/cryptomator-cli /usr/local/bin/cryptomator || { echo "Failed to create symlink for Cryptomator CLI"; } && \
        rm -rf ./cryptomator-cli-0.6.2-linux-x64; \
    else \
        echo "Unsupported architecture: $ARCH"; \
        exit 1; \
    fi

# Add TeX Live to the PATH
ENV PATH="/usr/local/texlive/2025/bin/aarch64-linux:$PATH"
ENV PATH="/usr/local/texlive/2025/bin/x86_64-linux:$PATH"

# Install the required fonts for Quarto and TeX Live
RUN cd /tmp/ && \
    wget https://assets.ubuntu.com/v1/0cef8205-ubuntu-font-family-0.83.zip && \
    unzip 0cef8205-ubuntu-font-family-0.83.zip -d ubuntu-fonts && \
    mkdir -p /usr/local/share/fonts/ubuntu && \
    cp ./ubuntu-fonts/ubuntu-font-family-0.83/*.ttf /usr/local/share/fonts/ubuntu/ && \
    fc-cache -fv

# Clean up texlive installation files
RUN rm -rf /var/lib/apt/lists/* install-tl-unx.tar.gz install-tl-20*

# Clean up
RUN apt-get remove -y gdebi-core && \
    apt-get autoremove -y && \
    apt-get clean

# Install Doorstop
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath

# Create a non-root user
# RUN useradd -ms /bin/bash ${user} && echo '${user} ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN useradd -ms /bin/bash ${user} && echo 'alab:alab' | chpasswd
RUN echo '${user} ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG sudo ${user}
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

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

# Install Doorstop
RUN pipx install doorstop==3.0b10

# Clean up unnecessary packages
USER root
RUN apt-get autoremove -y && apt-get autoclean -y

RUN chown -R ${user}:${user} /usr/local/texlive

# Set the container starting point, running the project as the user
USER ${user}

# Install the required fonts for Quarto and TeX Live for the non-root user
RUN cp /tmp/0cef8205-ubuntu-font-family-0.83.zip ~ && \
    cd ~ && \
    unzip 0cef8205-ubuntu-font-family-0.83.zip -d ubuntu-fonts && \
    rm 0cef8205-ubuntu-font-family-0.83.zip && \
    mkdir -p /home/${user}/.fonts/ubuntu && \
    cp ./ubuntu-fonts/ubuntu-font-family-0.83/*.ttf /home/${user}/.fonts/ubuntu/ && \
    fc-cache -fv

WORKDIR /home/${user}/${c5folder}/${c5folder}
CMD ["poetry", "shell"]