FROM python:3.9.6

WORKDIR /code

RUN apt-get update

ENV PYHTONUNBUFFERED=1

COPY ./ /code
RUN python -m pip install --upgrade pip
RUN pip install -U --no-cache-dir -r /code/requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]