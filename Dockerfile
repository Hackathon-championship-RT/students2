FROM ubuntu:24.04 AS base_image
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /home/sveta
ENV WORKDIR=/home/sveta

RUN apt-get update && apt-get -y --no-install-recommends install software-properties-common

RUN apt-get -y --no-install-recommends install \
    make git sudo curl wget build-essential unattended-upgrades \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev python3-full tree python3-pip

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

RUN groupadd -g 1001 sveta && useradd -u 1001 -m sveta -g sveta -d ${WORKDIR}


ENV POETRY_VERSION 1.6.1
ENV POETRY_HOME=/home/sveta/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python - --version $POETRY_VERSION
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
