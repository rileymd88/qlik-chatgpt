FROM python:3.9
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
WORKDIR /code
CMD python -m uvicorn main:app --host 0.0.0.0 --reload