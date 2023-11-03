# Base images of Python
From python:3.8

# Set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /socialMediaAPI

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /socialMediaAPI/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /Django_Docker/
COPY . /socialMediaAPI/

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]