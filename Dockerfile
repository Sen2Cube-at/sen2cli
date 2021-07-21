FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
		git \
		tk-dev \
		uuid-dev \
	&& rm -rf /var/lib/apt/lists/*