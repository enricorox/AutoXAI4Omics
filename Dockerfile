FROM tensorflow/tensorflow:2.4.0

ENV DEBIAN_FRONTEND="noninteractive"
ARG USER_ID=${USER_ID}
ENV R_BASE_VERSION 4.2.0

RUN \
	apt-get -y update && \
	apt upgrade -y && \
	apt-get install -y software-properties-common && \
	apt-get -y update && \
	add-apt-repository universe

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran40/'
RUN apt update

RUN apt update
RUN apt-get update
RUN apt install -y fort77 r-base-core r-base r-base-dev r-recommended swig

RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install git
RUN python3 -m pip install --upgrade pip
RUN useradd -l -m -s /bin/bash -u ${USER_ID} omicsuser

USER omicsuser

WORKDIR /home/omicsuser

ENV PATH "/home/omicsuser/.local/bin:${PATH}"

COPY --chown=omicsuser:omicsuser requirements.txt .

RUN \
	cat requirements.txt | \
	grep -v ^# | \
	xargs -n 1 pip install --no-cache-dir

# --no-build-isolation

COPY --chown=omicsuser:omicsuser install_Python_packages.sh .

# RUN ./install_Python_packages.sh

ENV R_LIBS_USER=/home/omicsuser/.local/R

COPY --chown=omicsuser:omicsuser install_R_packages.sh .

RUN mkdir -p ${R_LIBS_USER}

USER root

RUN ./install_R_packages.sh

USER omicsuser

COPY --chown=omicsuser:omicsuser *.py *.R ./
ADD --chown=omicsuser:omicsuser tabauto ./tabauto

COPY --chown=omicsuser:omicsuser logging.yml ./

ENV PYTHONPATH "/home/omicsuser:${PYTHONPATH}"

ENV TF_CPP_MIN_LOG_LEVEL '2'

CMD ["$@"]
