FROM python:3.9-alpine
RUN apk update && apk upgrade && apk add bash && apk add build-base
COPY . ./
RUN pip install -r requirements.txt
CMD ["uvicorn", "server:app", "--reload"]¬