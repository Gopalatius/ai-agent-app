# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
# --no-cache-dir: Prevents pip from saving cache, reducing image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
# This copies the 'app' directory and any other files at the root level
COPY . /app

# Expose port 8000, which is the default port for Uvicorn
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
# `app.main:app` refers to the 'app' instance in 'main.py' inside the 'app' directory.
# `--host 0.0.0.0` makes the server accessible from all network interfaces.
# `--port 8000` specifies the port to listen on.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]