FROM selenium/standalone-chrome

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium
RUN python3 -m pip install Flask

COPY ./app.py .
COPY ./select_activitesV2.py .

EXPOSE 5000

CMD ["python3", "app.py"]
