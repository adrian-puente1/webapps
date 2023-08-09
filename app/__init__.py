from flask import Flask
import pathlib
import uuid

app = Flask(__name__)
pathlib.Path(f"files/{str(uuid.uuid4())}"[::-1].split('/',1)[-1][::-1]).mkdir(parents=True, exist_ok=True)