FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

RUN apt-get update
RUN apt-get install --no-install-recommends -y curl git python3
RUN apt-get install --no-install-recommends -y build-essential python3-dev
RUN apt-get install --no-install-recommends -y uwsgi uwsgi-plugin-python3
RUN apt-get install --no-install-recommends -y libglib2.0-0 libsm6 libxext6 libxrender-dev
RUN apt-get clean

RUN groupadd -r -g 999 appuser && \
    useradd  -r -m -s /bin/sh -g appuser -u 999 appuser
USER appuser
WORKDIR /home/appuser/

# install pip from source
# - there are some problems with system pip while compiling apex and GCNet
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py --user

# prep dirs for planogram-ai-service
RUN mkdir -p /home/appuser/repos/planogram-ai-service/lib

# - large wheels are kept in git-lfs to avoid downloading them from the internet each build

# install numpy
WORKDIR /home/appuser/repos/planogram-ai-service/lib
COPY --chown=appuser:appuser lib/numpy-1.17.4-cp36-cp36m-manylinux1_x86_64.whl .
RUN python3 -m pip install --user numpy-1.17.4-cp36-cp36m-manylinux1_x86_64.whl

# install torch
WORKDIR /home/appuser/repos/planogram-ai-service/lib
COPY --chown=appuser:appuser lib/torch-1.1.0-cp36-cp36m-linux_x86_64.whl .
RUN python3 -m pip install --user torch-1.1.0-cp36-cp36m-linux_x86_64.whl

# install opencv
WORKDIR /home/appuser/repos/planogram-ai-service/lib
COPY --chown=appuser:appuser lib/opencv_python-4.1.2.30-cp36-cp36m-manylinux1_x86_64.whl .
RUN python3 -m pip install --user opencv_python-4.1.2.30-cp36-cp36m-manylinux1_x86_64.whl

# install torchvision
WORKDIR /home/appuser/repos/planogram-ai-service/lib
COPY --chown=appuser:appuser lib/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl .
RUN python3 -m pip install --user torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl

# compile apex
WORKDIR /home/appuser/repos/planogram-ai-service/lib
COPY --chown=appuser:appuser lib/apex.tar.gz .
RUN tar xzf apex.tar.gz
WORKDIR /home/appuser/repos/planogram-ai-service/lib/apex
RUN python3 -m pip install --user -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

# compile GCNet
WORKDIR /home/appuser/repos/planogram-ai-service/lib
COPY --chown=appuser:appuser lib/GCNet.tar.gz .
RUN tar xzf GCNet.tar.gz
WORKDIR /home/appuser/repos/planogram-ai-service/lib/GCNet
RUN python3 -m pip install --user cython
RUN PYTHON=python3 ./compile.sh
RUN python3 -m pip install --user .

# install tensorflow-gpu
WORKDIR /home/appuser/repos/planogram-ai-service/lib
COPY --chown=appuser:appuser lib/tensorflow_gpu-1.13.1-cp36-cp36m-manylinux1_x86_64.whl .
RUN python3 -m pip install --user tensorflow_gpu-1.13.1-cp36-cp36m-manylinux1_x86_64.whl

# install rest of the requirements
WORKDIR /home/appuser/repos/planogram-ai-service
COPY --chown=appuser:appuser requirements.txt ./
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

# setup ai-service
COPY --chown=appuser:appuser ai_service ai_service
COPY --chown=appuser:appuser setup.py .
RUN python3 -m pip install --user --no-cache-dir -e .

# copy runtime config and test
COPY --chown=appuser:appuser config config
COPY --chown=appuser:appuser test test

# do we really need this?
ENV PLANOGRAM_SETTINGS api.settings.ProdConfig

# clean
RUN rm /home/appuser/repos/planogram-ai-service/lib/*.whl

# install experiments if needed
USER root
USER appuser

RUN mkdir -p /home/appuser/logs

WORKDIR /home/appuser/repos/planogram-ai-service
EXPOSE 7552
CMD ["uwsgi", "/home/appuser/repos/planogram-ai-service/config/uwsgi.ini"]
