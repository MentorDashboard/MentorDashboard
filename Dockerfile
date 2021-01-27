FROM python:3.9
RUN apt-get update
RUN apt-get -y install default-libmysqlclient-dev


# STEP 2: Copy the source code in the current directory to the container.  Store it in a folder named /app.
ADD . /app

# STEP 3: Set working directory to /app so we can execute commands in it
WORKDIR /app

# STEP 4: Install necessary requirements (Flask, etc)
RUN pip install -r requirements.txt 

# STEP 5: Declare environment variables
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production
ENV DATABASE_URL=mysql://mysql:e06f282b4190604d@fairytales.dev:11484/mentordashboard 
ENV SECRET_KEY=base64:YlF0nTSK6tIh6nm9+Pho0cvu9ioTl2rs6zKzGdav7xM=

# STEP 6: Expose the port that Flask is running on
EXPOSE 5000 

# STEP 7: Run Flask!
CMD ["flask", "run", "--host=0.0.0.0"]