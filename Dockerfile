# Stage 7 - Recipe for building the serving API image.
# Read top to bottom: each line is a step inside a fresh room;

# (1) Start from a trusted, minimal base image: official Python 3.12 on slim Linux.
#     Same Python version that trained the model, minus OS bloat.
FROM python:3.12-slim

# (2) The working folder inside the room. Everything after this lands here, and
#     the app will start from here. The /app layout mirrors the MLOps_Work folder
#     structure so the app's relative paths keep working.
WORKDIR /app

# (3) Shopping list first, because it changes rarely...
COPY requirements-api.txt .

# (4) ...and installing it is the SLOW step. Putting it early means Docker caches
#     this layer; rebuilds reuse it and only redo what changed below.
#     --no-cache-dir = don't keep downloaded wheels; keeps the room small.
RUN pip install --no-cache-dir -r requirements-api.txt

# (5) Now the frequently-changing application code.
#     features.py is required! serve_model.py loads a pipeline that calls
#     "features.make_features" by module name -> joblib needs features.py on disk
#     when it un-pickles. Forgetting it crashed the first container
#     (ModuleNotFoundError: No module named 'features').
COPY serve_model.py .
COPY features.py .

# (6) The trained model that the API serves. Same folder layout as the repo so
#     the path serve_model.py computes (via __file__) resolves identically.
COPY models/housing_pipeline.joblib models/housing_pipeline.joblib

# (7) Documentation label: the door this app listens on inside the room.
#     The actual opening is done later with: docker run -p 8000:8000 ...
EXPOSE 8000

# (8) The live command: what runs when a container STARTS from this image.
#     0.0.0.0 (not 127.0.0.1) = listen on every interface inside the room, which
#     is what makes the -p port mapping able to reach the server.
CMD ["uvicorn", "serve_model:app", "--host", "0.0.0.0", "--port", "8000"]