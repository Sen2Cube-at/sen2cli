FROM python:3.8-slim

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
    && pip install git+https://github.com/ZGIS/sen2cli.git@main

CMD . /home/sen2cli/.venv/sen2cli/bin/activate && exec python