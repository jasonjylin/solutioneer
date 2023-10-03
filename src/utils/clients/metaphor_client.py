# client.py
import os

from dotenv import load_dotenv
from metaphor_python import Metaphor

load_dotenv()
API_KEY = os.environ["METAPHOR_API_KEY"]


class MetaphorClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetaphorClient, cls).__new__(cls)
            cls._instance._client = Metaphor(api_key=API_KEY)
        return cls._instance

    @property
    def client(self):
        return self._client
