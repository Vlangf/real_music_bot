FROM python:3.9-alpine
RUN apk update && apk upgrade && apk add bash
COPY . ./
RUN pip install -r requirements.txt
CMD ["python", "./server.py"]