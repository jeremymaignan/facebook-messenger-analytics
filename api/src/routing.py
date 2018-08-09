from flask import Flask
import conversations

app = Flask(__name__)
app.register_blueprint(conversations.get_conversations_list_route)
app.register_blueprint(conversations.get_one_conversation_route)
app.debug = True