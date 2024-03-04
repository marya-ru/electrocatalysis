FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        software-properties-common \
        python3.10 \
        python3-pip \
        python3-apt && \
    apt-get clean

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8513

HEALTHCHECK CMD curl --fail http://localhost:8513/_stcode/health

ENTRYPOINT ["streamlit", "run", "app.py"]
