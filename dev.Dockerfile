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

# Update and install depencencies
RUN apt update --fix-missing
RUN apt-get install -y git python3-pip graphviz

# Install Doorstop
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath

# Create a non-root user
RUN useradd -ms /bin/bash ${user} && echo '${user} ALL=(ALL) NOPASSWD:ALL' >>/etc/sudoers

# Add location where pip is installed to the PATH variable
ENV PATH="/home/${user}/.local/bin:${PATH}"

# Copy the files and install the python environment as user alab 
USER ${user} 
# RUN pip3 install pipenv
RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /home/${user}/${c5folder}
COPY poetry.lock pyproject.toml /home/${user}/${c5folder}/

# Project initialization
# RUN poetry install

# Creating folders, and files for a project
COPY . /home/${user}/${c5folder}

# Project initialization
RUN poetry install

# Install python virtual environment for the project
WORKDIR /home/${user}/${c5folder}/${c5folder}
# RUN pipenv install

# Install Doorstop
RUN pipx install doorstop==3.0b10

# Clean up unnecessary packages
USER root
RUN apt-get autoremove -y && apt-get autoclean -y

# Set the container starting point, running the project as the user
USER ${user} 
WORKDIR /home/${user}/${c5folder}/${c5folder}
CMD ["poetry", "shell"]