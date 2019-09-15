from flask import Flask
from flask_cors import CORS

import conversations

app = Flask(__name__)
CORS(app)
app.register_blueprint(conversations.get_conversations_list_route)
app.register_blueprint(conversations.get_one_conversation_route)
app.register_blueprint(conversations.get_messages_per_hour_route)
app.register_blueprint(conversations.get_users_route)

app.debug = True