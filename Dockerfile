FROM ubuntu:24.04 AS base_image
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /home/project
ENV WORKDIR=/home/project

RUN apt-get update && apt-get -y --no-install-recommends install software-properties-common  \
&& apt-get clean \
&& apt-get -y --no-install-recommends install \
    build-essential  \
    curl  \
    git  \
    libbz2-dev  \
    libreadline-dev  \
    libssl-dev  \
    make  \
    python3-full  \
    python3-pip  \
    sudo  \
    tree  \
    unattended-upgrades \
    wget  \
    zlib1g-dev  \
&& apt-get clean \
&& update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
&& groupadd -g 1001 project && useradd -u 1001 -m project -g project -d ${WORKDIR}


ENV POETRY_VERSION 1.6.1
ENV POETRY_HOME=/home/project/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python - --version "$POETRY_VERSION"
ENV PATH ${POETRY_HOME}/bin:$PATH

RUN ${POETRY_HOME}/bin/poetry config virtualenvs.create false
ENV PIP_BREAK_SYSTEM_PACKAGES 1


FROM base_image AS auth_service

ENV PYTHONPATH=${WORKDIR}:${PYTHONPATH}

COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-root

COPY alembic alembic
COPY alembic.ini alembic.ini
COPY src ${WORKDIR}/src
RUN tree .

CMD ["python", "src/api/webserver.py"]
