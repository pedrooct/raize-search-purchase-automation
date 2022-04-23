FROM python:3.8

WORKDIR /raize-automation/

RUN pip3 install selenium==4.1.3

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
RUN tar -xvf geckodriver-v0.31.0-linux64.tar.gz

COPY ./ /raize-automation/

RUN cat credentials.json
RUN ls -l

ENTRYPOINT ["python3", "raizeSearchPurchase.py"]
