# Base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install system dependencies and Python dependencies as root user
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    pip install --upgrade pip && \
    pip install --no-warn-script-location --root-user-action=ignore -r requirements.txt

# Set a non-root user and group after installing dependencies
RUN groupadd -r appgroup && useradd -r -m -g appgroup appuser

# Copy the rest of the application code
COPY . .

# Change ownership of the working directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user for application execution
USER appuser

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
