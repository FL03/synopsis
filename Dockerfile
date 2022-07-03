FROM jo3mccain/poetic

ENV SERVER_PORT=8080

ADD . /project
WORKDIR /project

COPY . .
RUN poetry install && poetry build

EXPOSE 5432/tcp
EXPOSE $SERVER_PORT/tcp
ENTRYPOINT ["./scripts/run.sh"]