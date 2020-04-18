.PHONY: clean
clean:
	rm -rf etl/messages/*/*/files; \
	rm -rf etl/messages/*/*/photos; \
	rm -rf etl/messages/*/*/gifs; \
	rm -rf etl/messages/*/*/audio; \
	rm -rf etl/messages/*/*/videos; \
	rm -rf etl/messages/*/facebookuser*; \
	rm -rf etl/messages/stickers_used; \
	echo "Clean files";

.PHONY: build
build:
	docker-compose up --build -d
