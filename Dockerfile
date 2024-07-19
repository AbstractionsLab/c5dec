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

ENV user=root
ENV c5folder=c5dec

# Update and install depencencies
RUN apt update --fix-missing
RUN apt-get install -y git python3-pip graphviz

# Install Doorstop
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath

RUN pipx install doorstop==3.0b10

# Add location where pip is installed to the PATH variable
ENV PATH="/home/${user}/.local/bin:${PATH}"

# Copy the files and install the python environment as user alab 
RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /home/${user}/${c5folder}
COPY poetry.lock pyproject.toml /home/${user}/${c5folder}/

# Create a git repository (needed by Doorstop) at the project root
RUN git init .

# Project initialization
RUN poetry install

# Creating folders, and files for a project
COPY . /home/${user}/${c5folder}

# Switch to project folder
WORKDIR /home/${user}/${c5folder}/${c5folder}

# RUN poetry config virtualenvs.create false

RUN poetry install

# Clean up unnecessary packages
RUN apt-get autoremove -y && apt-get autoclean -y

# Expose port for the GUI (web app)
EXPOSE 5432

ENTRYPOINT ["poetry", "run", "c5dec"]