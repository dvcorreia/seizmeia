FROM python:3.11-slim-buster as base

RUN apt-get -y update && apt-get install -y --no-install-recommends git

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base as production

COPY . .

# Run as non-root for security posture
USER 1001:1001

EXPOSE 80
ENTRYPOINT [ "python", "-m", "seizmeia" ]

FROM base as devenv

COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

FROM devenv as dev

COPY . .

ENV SEIZMEIA_ENVIRONMENT=development

EXPOSE 80
CMD [ "python", "-m", "seizmeia" ]

FROM devenv as test

COPY . .
RUN tox