# Synopsis
[![Docker](https://github.com/FL03/synopsis/actions/workflows/docker.yml/badge.svg)](https://github.com/FL03/synopsis/actions/workflows/docker.yml)

### _Created with FastAPI, PostgreSQL, and Tortoise-ORM_

## Getting Started

### Building from the source
    git clone https://github.com/FL03/synopsis
    poetry install
    poetry run python -m synopsis

### Docker and Docker Compose

    docker pull jo3mccain/synopsis:latest
or

    docker compose -f ".docker/docker-compose.yml" up