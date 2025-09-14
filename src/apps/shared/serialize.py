"""
Module for serialize response
"""

from fastapi.encoders import jsonable_encoder


class SerializationFilter:
    """
    Class responsible for filtering the response
    """

    @staticmethod
    def response(_object):
        if isinstance(_object, list):
            return [SerializationFilter.response(item) for item in _object]
        elif isinstance(_object, dict):
            return {
                key: SerializationFilter.response(value)
                for key, value in _object.items()
            }
        elif hasattr(_object, "__dict__"):
            return jsonable_encoder(_object)
        else:
            return _object
