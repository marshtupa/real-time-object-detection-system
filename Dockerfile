# Original Dockerfile: https://github.com/facebookresearch/detectron2/blob/master/docker/Dockerfile

FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev git wget sudo curl && \
  rm -rf /var/lib/apt/lists/*

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/get-pip.py && \
	python3 get-pip.py --user && \
	rm get-pip.py

ENV FORCE_CUDA="1"
ARG TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"
ENV FVCORE_CACHE="/tmp"
ENV PILLOW_VERSION=7.0.0

RUN mkdir real-time-object-detection-system
WORKDIR /home/appuser/real-time-object-detection-system

COPY requirements-docker.txt /home/appuser/real-time-object-detection-system
COPY requirements-detectron2.txt /home/appuser/real-time-object-detection-system
RUN pip install -r requirements-docker.txt
RUN pip install -r requirements-detectron2.txt

COPY . /home/appuser/real-time-object-detection-system
CMD ["python3", "-u", "/home/appuser/real-time-object-detection-system/Detector.py"]

# #  For developing - infinite process
# ENTRYPOINT ["tail"]
# CMD ["-f","/dev/null"]
