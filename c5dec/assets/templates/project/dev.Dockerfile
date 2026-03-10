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
        git python3-pip graphviz sudo curl gnupg2 chromium && \
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

# Install Doorstop
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath

# Create a non-root user with no password; grant passwordless sudo via sudoers.d
RUN useradd -ms /bin/bash ${user} && \
    usermod -aG sudo ${user} && \
    echo "alab ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/alab && \
    chmod 440 /etc/sudoers.d/alab

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