#!/bin/sh

echo 'Clean files'
rm -rf etl/messages/*/*/files
rm -rf etl/messages/*/*/photos
rm -rf etl/messages/*/*/gifs
rm -rf etl/messages/*/*/audio
rm -rf etl/messages/*/*/videos
rm -rf etl/messages/*/facebookuser*
rm -rf etl/messages/stickers_used

echo 'Start building containers'
docker-compose up --build -d

echo "http://localhost:3000/"
