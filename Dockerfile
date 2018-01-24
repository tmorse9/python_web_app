FROM python:2.7
ADD . /prlmos_app
WORKDIR /prlmos_app
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]
