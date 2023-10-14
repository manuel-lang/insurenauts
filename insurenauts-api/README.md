# API

## Prerequesites

- [Installing Python](https://www.python.org/downloads/)
- [Installing Poetry](https://python-poetry.org/docs/)
- Set `SMTP_EMAIL_ADDRESS` and `SMTP_PASSWORD` environment variables to send emails

## Running the API

- Install all the requirements with `poetry install`.
- Start the API with `poetry run api`.

## Deploying the API

- Build the Docker image with `docker build -t manuellang1/insurenauts-api:<tag> .`
- Push the Docker image with `docker push -t manuellang1/insurenauts-api:<tag> .`
- Deploy within [render](https://dashboard.render.com/)
