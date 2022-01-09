FROM selenium/standalone-chrome:latest

ENV PATH "$PATH:/home/seluser/.local/bin"
ADD . /home/seluser/autoscab
RUN sudo chown seluser /home/seluser/autoscab

RUN sudo apt-get update -y
RUN sudo apt-get install -y python3-pip

WORKDIR /home/seluser/autoscab
RUN pip install .

CMD autoscab kingsoopers --relentless