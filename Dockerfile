FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY ./app /app
RUN pip3 install -r /app/requirements.txt
