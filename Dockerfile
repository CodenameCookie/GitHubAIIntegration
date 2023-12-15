# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the templates directory into the container at /app/templates
COPY templates /app/templates

# Expose port 5000 or another for the Flask app
EXPOSE 5000
ENV FLASK_APP=main.py

# Label the image with the desired tag
LABEL version="0.4"

# Define the command to run your Flask app
#CMD ["python", "main.py"]
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]
