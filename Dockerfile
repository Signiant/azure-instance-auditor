FROM python:3.8-slim

RUN pip install azure-mgmt-compute
RUN pip install azure-mgmt-subscription
RUN mkdir /src

COPY audit.py /src/

# To run locally In order for this Dockerfile to work you need to get the credential from sercret server
# then uncomment the following line
# COPY cred.json /src/

WORKDIR /src

ENTRYPOINT ["python","/src/audit.py"]
CMD ["-h"]