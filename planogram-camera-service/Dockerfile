FROM ubuntu:18.04

# install system dependencies
RUN apt-get update
RUN apt-get install --no-install-recommends -y python3 python3-pip python3-setuptools
RUN apt-get install --no-install-recommends -y uwsgi uwsgi-plugin-python3
# for opencv
RUN apt-get install --no-install-recommends -y libglib2.0-0 && \
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
# create user
RUN groupadd -r -g 999 appuser
RUN useradd  -r -m -s /bin/sh -g appuser -u 999 appuser
USER appuser

# install camera_service
RUN mkdir -p /home/appuser/repos/planogram-camera-service
WORKDIR /home/appuser/repos/planogram-camera-service
COPY --chown=appuser:appuser . .
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt
RUN python3 -m pip install --user --no-cache-dir -e .

EXPOSE 5000
CMD ["/usr/bin/uwsgi", "/home/camserv/repos/planogram-camera-service/config/camera_service.uwsgi.ini"]
