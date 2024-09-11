# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set the OpenAI API key as an environment variable
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Command to run the application
CMD ["python", "scripts/run_simulation.py"]