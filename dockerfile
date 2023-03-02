FROM python:3.9.6

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN libcudnn8 \
    apt-get clean     &&  \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

EXPOSE 8000
ENV PYHTONUNBUFFERED=1

COPY ./ /code
RUN python -m pip install --upgrade pip
RUN pip install -U --no-cache-dir -r /code/requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]