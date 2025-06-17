# Dockerfile

# Use a lean Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /pearl

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of your application's code into the working directory
COPY . .

# Expose the port the app will run on
EXPOSE 7000

# The command to start the Uvicorn server when the container launches.
# We add --reload for a better development experience.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]