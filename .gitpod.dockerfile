FROM continuumio/miniconda3

SHELL ["/bin/bash", "--login", "-c"]

# Move dep requirements to temp folder
COPY requirements.txt /tmp/requirements.txt
COPY conda_requirements.txt /tmp/conda_requirements.txt

# Add channel conda-forge
RUN conda config --add channels conda-forge
# Create conda env
RUN conda create --name telegram --file /tmp/conda_requirements.txt
# Init conda for shell
RUN conda init bash
# Install pip-based dependencies
RUN conda activate telegram \
    && pip install -r /tmp/requirements.txt

ENV PATH /opt/conda/envs/telegram/bin:$PATH

# Set the default conda environment
RUN echo "conda activate telegram" >> ~/.bashrc