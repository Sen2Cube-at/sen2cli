FROM python:3.8-slim
ARG SEN2CLI_VERSION="v0.2.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
		git \
	&& rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash sen2cli

USER sen2cli
WORKDIR /home/sen2cli

RUN cd /home/sen2cli  \
    && python3 -m venv /home/sen2cli/.venv/sen2cli \
    && . /home/sen2cli/.venv/sen2cli/bin/activate \
    && echo "source /home/sen2cli/.venv/sen2cli/bin/activate" >> /home/sen2cli/.bashrc \
    && pip install wheel \
    && pip install "git+https://github.com/Sen2Cube-at/sen2cli.git@${SEN2CLI_VERSION}"

CMD . /home/sen2cli/.venv/sen2cli/bin/activate && exec python