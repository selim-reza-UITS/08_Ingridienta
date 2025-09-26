FROM ghcr.io/astral-sh/uv:bookworm
WORKDIR /app

ENV UV_LINK_MODE=hardlink 
ENV UV_CACHE_DIR=/opt/uv-cache/
ENV VIRTUAL_ENV=/opt/env

# MINIMUM BUILD (RE RUNS ONLY WHEN requirements.txt is modified)
COPY ./requirements/production.txt ./requirements.txt

RUN uv venv /opt/env --python 3.11
RUN uv pip install -r requirements.txt

# FULL REPO
COPY ./ /app
# RUN uv pip install -r requirements.txt
RUN chmod +x ./entrypoint.sh
# RUNTIME CMD
CMD ["./entrypoint.sh"]