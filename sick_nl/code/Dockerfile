#
FROM nvidia/cuda:11.7.1-base-ubuntu20.04

# install utilities
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl

ENV CONDA_AUTO_UPDATE_CONDA=false \
    PATH=/opt/miniconda/bin:$PATH
RUN curl -sLo ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh \
    && chmod +x ~/miniconda.sh \
    && ~/miniconda.sh -b -p /opt/miniconda \
    && rm ~/miniconda.sh \
    && sed -i "$ a PATH=/opt/miniconda/bin:\$PATH" /etc/environment

# Installing python dependencies
RUN python3 -m pip --no-cache-dir install --upgrade pip && \
    python3 --version && \
    pip3 --version

#FROM python:3.9
#
#RUN nvidia-smi

# 


# # ensure local python is preferred over distribution python
# ENV PATH /usr/local/bin:$PATH

# # http://bugs.python.org/issue19846
# # > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
# ENV LANG C.UTF-8

# # runtime dependencies
# RUN set -eux; \
# 	apt-get update; \
# 	apt-get install -y --no-install-recommends \
# 		libbluetooth-dev \
# 		tk-dev \
# 		uuid-dev \
# 	; \
# 	rm -rf /var/lib/apt/lists/*

# ENV GPG_KEY E3FF2839C048B25C084DEBE9B26995E310250568
# ENV PYTHON_VERSION 3.9.13

# RUN set -eux; \
# 	\
# 	wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz"; \
# 	wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc"; \
# 	GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; \
# 	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$GPG_KEY"; \
# 	gpg --batch --verify python.tar.xz.asc python.tar.xz; \
# 	command -v gpgconf > /dev/null && gpgconf --kill all || :; \
# 	rm -rf "$GNUPGHOME" python.tar.xz.asc; \
# 	mkdir -p /usr/src/python; \
# 	tar --extract --directory /usr/src/python --strip-components=1 --file python.tar.xz; \
# 	rm python.tar.xz; \
# 	\
# 	cd /usr/src/python; \
# 	gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
# 	./configure \
# 		--build="$gnuArch" \
# 		--enable-loadable-sqlite-extensions \
# 		--enable-optimizations \
# 		--enable-option-checking=fatal \
# 		--enable-shared \
# 		--with-system-expat \
# 		--without-ensurepip \
# 	; \
# 	nproc="$(nproc)"; \
# 	make -j "$nproc" \
# 	; \
# 	make install; \
# 	\
# # enable GDB to load debugging data: https://github.com/docker-library/python/pull/701
# 	bin="$(readlink -ve /usr/local/bin/python3)"; \
# 	dir="$(dirname "$bin")"; \
# 	mkdir -p "/usr/share/gdb/auto-load/$dir"; \
# 	cp -vL Tools/gdb/libpython.py "/usr/share/gdb/auto-load/$bin-gdb.py"; \
# 	\
# 	cd /; \
# 	rm -rf /usr/src/python; \
# 	\
# 	find /usr/local -depth \
# 		\( \
# 			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
# 			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \) \) \
# 		\) -exec rm -rf '{}' + \
# 	; \
# 	\
# 	ldconfig; \
# 	\
# 	python3 --version

# # make some useful symlinks that are expected to exist ("/usr/local/bin/python" and friends)
# RUN set -eux; \
# 	for src in idle3 pydoc3 python3 python3-config; do \
# 		dst="$(echo "$src" | tr -d 3)"; \
# 		[ -s "/usr/local/bin/$src" ]; \
# 		[ ! -e "/usr/local/bin/$dst" ]; \
# 		ln -svT "$src" "/usr/local/bin/$dst"; \
# 	done

# # if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
# ENV PYTHON_PIP_VERSION 22.0.4
# # https://github.com/docker-library/python/issues/365
# ENV PYTHON_SETUPTOOLS_VERSION 58.1.0
# # https://github.com/pypa/get-pip
# ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/5eaac1050023df1f5c98b173b248c260023f2278/public/get-pip.py
# ENV PYTHON_GET_PIP_SHA256 5aefe6ade911d997af080b315ebcb7f882212d070465df544e1175ac2be519b4

# RUN set -eux; \
# 	\
# 	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
# 	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; \
# 	\
# 	export PYTHONDONTWRITEBYTECODE=1; \
# 	\
# 	python get-pip.py \
# 		--disable-pip-version-check \
# 		--no-cache-dir \
# 		--no-compile \
# 		"pip==$PYTHON_PIP_VERSION" \
# 		"setuptools==$PYTHON_SETUPTOOLS_VERSION" \
# 	; \
# 	rm -f get-pip.py; \
# 	\
# 	pip --version

# 
WORKDIR /code_docker

# 
COPY ./req_from_conda.txt /code_docker/req_from_conda.txt

#
# ADD ./code/models /code_docker/models

#
ADD ./model_data /code_docker/model_data

# 
RUN pip3 install --no-cache-dir --upgrade -r /code_docker/req_from_conda.txt

#
RUN pip3 install --no-cache-dir psycopg2-binary 

#
RUN pip3 --timeout=500 --no-cache-dir install torch==1.11.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html

# 
COPY ./code/app /code_docker

#
COPY ./code /code_docker

# 
CMD ["uvicorn", "app.api_sopalign:app", "--host", "0.0.0.0", "--port", "8000"]
