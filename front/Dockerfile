FROM node:12.6.0

COPY . /var/app/front/
# set working directory
WORKDIR /var/app/front/

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

RUN npm update
RUN npm install --silent
#RUN npm install react-scripts@3.0.1 -g --silent

# start app
CMD ["npm", "start"]
