[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-green.svg)](https://shields.io/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![MIT Licence](https://img.shields.io/badge/License-MIT-blue.svg)](https://shields.io/)
[![Python](https://img.shields.io/badge/python-3.7-yellow.svg)](https://shields.io/)
# Facebook Messenger Analytics


## Purpose

This project allows you to get insights from your Facebook Messenger data.  
Facebook allows you to download all your personal data (posts, likes, friends, messages, etc).  
When you launch the code, 4 steps are processing:
- A MySQL database is built on your laptop
- An ETL loads all messages in the local database
- An API (Python/Flask) is started to provide data to the front
- A website is launched (React) to display the insights

```
 Everthing runs locally. Nothing, including your messages are ever uploaded on an external server.
```

## Quick start

### Download your data on Facebook

1. Go on Facebook website
2. Settings > Your facebook Information > Download Your Information
3. Select: **Date Range:** All my data **Format:** Json **Media Quality:** Low
4. Press Create file
5. You will now receive an email (with *"Facebook information file requested"* as subject) telling you Facebook is processing your requests  
![text](https://github.com/jeremymaignan/facebook-messenger-analytics/blob/master/screenshots/download_facebook_data.png)

6. A few hours later, you will receive another email (with *"Your Facebook information file is ready"* as subject)
7. Follow the link in the email, click on download to download your data

### Install Docker

Follow the instructions: https://docs.docker.com/get-docker/  
To ensure docker and docker-compose are correctly installed, run:
```sh
docker -v
docker-compose -v
```
Make sure you don't have any errors.


### Start the project

1. Unzip the archive you downloaded from Facebook.
2. Copy paste the folder **messages** (from the archive) in the project, in the directory **/etl/**.  
You should have a path looking like *"/elt/messages/inbox/{CONVERSATION_NAME}/message_1.json"*.
3. To remove userless files, run: 
```sh
make clean
```
4. To build the project, run:
```sh
make build
```
This command might take several minutes (depending on the volume of messages you have)

5. Browse your data: http://localhost:3000/

## Contact

If you need any support or if you have ideas to improve the project, contact me at **jeremy.maignan@gmail.com**.

## Examples
