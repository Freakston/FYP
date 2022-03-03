FROM python:3
ADD IDK-Fuzz/ /src
ENV RAB=192.168.56.107
ENV POD=192.168.56.107
RUN pip install -r src/requirements.txt

CMD [ "python", "/src/dep.py"]