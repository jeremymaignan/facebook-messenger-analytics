import logging
import os

from flask import Flask
from flask_cors import CORS

import apis as apis
import models
from utils import errors
from utils.registry import registry

logging.basicConfig(
    level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper()),
    format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s'
)

app = Flask(__name__)
models.init(app)
errors.setup(app)
CORS(app)
registry.discover(apis)
registry.init(app=app)
app.run(debug=True, host="0.0.0.0", port=7000)
