# `python-base` sets up all our shared environment variables
FROM python:3.11 as python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.6.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    DEBIAN_FRONTEND=noninteractive


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
        software-properties-common \ 
        wget \
        ca-certificates \
        gpg 

RUN wget -O - https://apt.corretto.aws/corretto.key | gpg --dearmor -o /usr/share/keyrings/corretto-keyring.gpg && \
echo "deb [signed-by=/usr/share/keyrings/corretto-keyring.gpg] https://apt.corretto.aws stable main" | tee /etc/apt/sources.list.d/corretto.list

RUN apt-get update && apt-get install --no-install-recommends -y java-11-amazon-corretto-jdk

RUN <<EOF

mkdir /opt/maven

maven_version=$(curl -fsSL https://repo1.maven.org/maven2/org/apache/maven/apache-maven/maven-metadata.xml  \
      | grep -Ev "alpha|beta" \
      | grep -oP '(?<=version>).*(?=</version)'  \
      | tail -n1)

maven_download_url="https://repo1.maven.org/maven2/org/apache/maven/apache-maven/$maven_version/apache-maven-${maven_version}-bin.tar.gz"

echo "Downloading [$maven_download_url]..."

curl -fL $maven_download_url | tar zxv -C /opt/maven --strip-components=1

EOF


# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --only main


# `development` image is used during development / testing
FROM python-base as development
# ENV FASTAPI_ENV=development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# COPY --from=builder-base /root/.local /root/.local
# # Copy Java runtime from the builder stage
# COPY --from=builder-base /usr/lib/jvm/java-11-amazon-corretto /usr/lib/jvm/java-11-amazon-corretto
# COPY --from=builder-base /usr/share/maven /usr/share/maven

# # Set up the environment variables
# ENV JAVA_HOME=/usr/lib/jvm/java-11-amazon-corretto
# ENV MAVEN_HOME=/usr/share/maven
# ENV M2_HOME=/usr/share/maven
# ENV PATH=$JAVA_HOME/bin:$MAVEN_HOME/bin:/root/.local/bin:$PATH

# quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --with test,lint

# will become mountpoint of our code
WORKDIR /app

# EXPOSE 8000
# CMD ["uvicorn", "--reload", "main:app"]


# `production` image used for runtime
FROM python-base as production
# ENV FASTAPI_ENV=production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder-base /root/.local /root/.local
# Copy Java runtime from the builder stage
COPY --from=builder-base /usr/lib/jvm/java-11-amazon-corretto /usr/lib/jvm/java-11-amazon-corretto
COPY --from=builder-base /opt/maven /opt/maven

# Set up the environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-amazon-corretto

ENV MAVEN_HOME=/opt/maven
ENV M2_HOME=/opt/maven
ENV PATH="/opt/maven/bin:${PATH}"

ENV MAVEN_CONFIG "/root/.m2"

COPY . /app/
WORKDIR /app
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app"]