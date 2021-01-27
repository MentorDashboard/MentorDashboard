FROM nikolaik/python-nodejs:python3.9-nodejs14
RUN apt-get update
RUN apt-get -y install default-libmysqlclient-dev

ARG FLASK_APP
ARG FLASK_ENV
ARG DATABASE_URL
ARG SECRET_KEY
ARG TIMEOUT

# STEP 2: Copy the source code in the current directory to the container.  Store it in a folder named /app.
ADD . /app
WORKDIR /app
COPY package*.json ./
RUN npm ci
RUN npm run css && npm run build

# STEP 3: Set working directory to /app so we can execute commands in it
RUN ["chmod", "+x", "/app/gunicorn.sh"]

# STEP 4: Install necessary requirements (Flask, etc)
RUN pip install -r requirements.txt 

# STEP 5: Declare environment variables
ENV FLASK_APP=$FLASK_APP
ENV FLASK_ENV=$FLASK_ENV
ENV DATABASE_URL=$DATABASE_URL
ENV SECRET_KEY=$SECRET_KEY
ENV TIMEOUT=$TIMEOUT

# STEP 7: Run Flask!
ENTRYPOINT ["./gunicorn.sh"]