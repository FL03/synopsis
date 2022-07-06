FROM jo3mccain/poetic

ENV DB_URI="sqlite://./app.db" \
    DEV_MODE=false \
    SERVER_PORT=8080

ADD . /app
WORKDIR /app

COPY . .
RUN poetry install

EXPOSE 5432/tcp
EXPOSE $SERVER_PORT/tcp

ENTRYPOINT ["./scripts/run.sh"]