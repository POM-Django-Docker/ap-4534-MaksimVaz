FROM python:3.10

ENV PYTHONUNBUFFERED=1

# create a working directory for the project inside the container
WORKDIR /app

# copy the requirements file
COPY requirements.txt /app/

# install necessary libraries
RUN pip install -r requirements.txt

# copy all project files into the container
COPY . /app/



# open port 8000
EXPOSE 8000

# start the django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
