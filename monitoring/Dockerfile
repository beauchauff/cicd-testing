# Use an official lightweight Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . /app

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define the command to run your app when the container starts
CMD ["streamlit", "run", "app.py"]