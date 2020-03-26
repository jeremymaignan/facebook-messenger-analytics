# develop stage
FROM mhart/alpine-node:13.11.0 AS develop-stage

# set working directory
WORKDIR /app/front/

# install and cache app dependencies
COPY package*.json /app/front/
RUN npm install