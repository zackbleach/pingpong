FROM ubuntu:14.04

# Install Python Setuptools
RUN apt-get install -y python-setuptools

# Install pip
RUN easy_install pip

# Add and install Python modules
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Expose
EXPOSE  8000

ADD app/ app/
ADD config.py config.py
ADD run.py run.py

RUN python run.py db init
RUN python run.py db migrate
RUN python run.py create_db

ADD app.db app.db

# Run
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]

