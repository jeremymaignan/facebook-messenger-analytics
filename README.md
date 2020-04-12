# Facebook Messenger Analytics


## Purpose

This project allows you get insights from your Facebook Messenger data.  
Facebook allows you to download all your personal data (posts, likes, friends, messages, etc).  
When you launch the code, 4 steps are processing:
- A MySQL database is built on your laptop
- An ETL loads all messages in the local database
- An API (Python/Flask) is started to provide data to the front
- A website is launched (React) to display the insights

```
 Everthing runs localy. Nothing, including your messages are ever uploaded on an external server.
```

## Quick start

### Download your data on Facebook

1. Go on Facebook website
2. Settings > Your facebook Information > Download Your Information
3. Select: **Date Range:** All my data **Format:** Json **Media Quality:** Low
4. Press Create file
5. You will now receive an email (with *"Facebook information file requested"* as subject) telling you Facebook is processing your requests  
![text](https://github.com/jeremymaignan/facebook-messenger-analytics/blob/master/screenshots/download_facebook_data.png)

6. A few hours later your will receive another email (with *"Your Facebook information file is ready"* as subject)
7. Follow the link in the email, click on download to download your data

### Install Docker

## Examples
