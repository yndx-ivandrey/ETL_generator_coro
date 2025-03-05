import json
from json import JSONDecodeError
from logging import Logger
from typing import Any

from .base_storage import BaseStorage


class JsonFileStorage(BaseStorage):
    def __init__(self, logger: Logger, file_path: str = "storage.json"):
        self.file_path = file_path
        self._logger = logger

    def save_state(self, state: dict[str, Any]) -> None:
        with open(self.file_path, "w") as outfile:
            outfile.write(json.dumps(state))

    def retrieve_state(self) -> dict[str, Any]:
        try:
            with open(self.file_path, "r") as json_file:
                state = json.load(json_file)
                return state if type(state) is dict else dict()
        except (FileNotFoundError, JSONDecodeError):
            self._logger.warning("No state file provided. Continue with default file")
            return dict()
