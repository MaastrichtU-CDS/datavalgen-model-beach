FROM ghcr.io/mdw-nl/datavalgen:latest

# default model and factory
ENV DATAVALGEN_MODEL=beach_lung
ENV DATAVALGEN_FACTORY=beach_lung

COPY ./src /app/datavalgen-model-beach/src
COPY ./pyproject.toml /app/datavalgen-model-beach/pyproject.toml

# install beach data model package, where already-installed datavalgen can
# find models and factories via python entry-points
RUN pip install --no-cache-dir /app/datavalgen-model-beach
