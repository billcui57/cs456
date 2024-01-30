import json
from dataclasses import dataclass

@dataclass
class GetRequestBody:
    file_name: str
    receive_port: int

@dataclass
class PutRequestBody:
    file_name: str

@dataclass
class PutResponseBody:
    receive_port: int

@dataclass
class Request:
    type: str
    body: dict

    # Method to convert the dataclass instance to JSON string
    def to_json(self):
        return json.dumps(self.__dict__)

    # Static method to create a dataclass instance from a JSON string
    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return Request(**data)

@dataclass
class Response:
    code: int
    body: dict

    # Method to convert the dataclass instance to JSON string
    def to_json(self):
        return json.dumps(self.__dict__)

    # Static method to create a dataclass instance from a JSON string
    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return Response(**data)