from datetime import datetime
import mysql.connector 

class Messages():
    def __init__(self, sender, timestamp_ms, content, gifs, photos, share, sticker, video, type_, title, is_still_participant, participants, thread_type, thread_path):
        participants = [x["name"].encode('latin1').decode('utf8') for x in participants]
        self.sender = sender.encode('latin1').decode('utf8')
        self.sent_at = datetime.fromtimestamp(timestamp_ms/1000).strftime('%Y-%m-%d %H:%M:%S')
        self.content = content.encode('latin1').decode('utf8')
        self.gifs = str(gifs)
        self.photos = str(photos)
        self.share = str(share)
        self.sticker = str(sticker)
        self.video = str(video)
        self.type = type_
        self.title = title.encode('latin1').decode('utf8')
        self.is_still_participant = is_still_participant
        self.participants = str(participants)
        self.thread_type = thread_type
        self.thread_path = thread_path

    def __repr__(self):
        return "[DEBUG] {}\t{} {}".format(
            self.sent_at,
            self.sender,
            self.content
        )