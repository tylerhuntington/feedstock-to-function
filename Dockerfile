FROM debian:bullseye-slim

# Install runtime dependencies
WORKDIR /ftf-django
ADD requirements.txt /ftf-django
RUN apt-get update \
 && apt-get install -yq --no-install-recommends \
    libboost-all-dev \
    libcairo2-dev \
    python3-dev \
    python3-pip \
    python3-rdkit \
    build-essential \
 && apt-get update && apt-get install -y \
    curl \
 && python3 -m pip install  --upgrade pip setuptools wheel  \
 && python3 -m pip install  -r requirements.txt \
 && python3 -m pip cache purge \
 && apt-get remove --purge -y \
    build-essential \
    libboost-all-dev \
    libcairo2-dev \
 && apt-get autoremove -y \
 && apt-get clean -y \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /root/.cache \
 && find /usr/local/lib/ -name __pycache__ | xargs rm -rf

ADD . /ftf-django

# Define build arguments
ARG django_settings_module=production

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE=ftf_web.settings.${django_settings_module}


