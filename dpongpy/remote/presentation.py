from pygame.event import Event
from dpongpy.model import *
import json


_DEBUG = False


class Serializer:
    primitives = [int, float, str, bool]
    containers = [list, tuple]

    def serialize(self, obj) -> str:
        return json.dumps(self._serialize(obj), indent=2 if _DEBUG else None)

    def _serialize(self, obj):
        if any(isinstance(obj, primitive) for primitive in self.primitives):
            return self._serialize_primitive(obj)
        elif isinstance(obj, dict):
            return self._serialize_dict(obj)
        elif any(isinstance(obj, container) for container in self.containers):
            return self._serialize_iterable(obj)
        else:
            return self._serialize_any(obj)

    def _serialize_iterable(self, obj):
        return [self._serialize(item) for item in obj]

    def _serialize_dict(self, obj):
        return {key: self._serialize(value) for key, value in obj.items()}

    def _serialize_primitive(self, obj):
        return obj

    def _serialize_any(self, obj):
        for klass in type(obj).mro():
            method_name = f"_serialize_{klass.__name__.lower()}"
            if hasattr(self, method_name):
                return getattr(self, method_name)(obj)
        raise NotImplementedError(f"Serialization for {type(obj).__name__} is not implemented")

    def _to_dict(self, obj, *attributes):
        dict = {name : self._serialize(getattr(obj, name)) for name in attributes}
        dict["$type"] = type(obj).__name__
        return dict

    def _serialize_direction(self, direction: Direction):
        return self._to_dict(direction, "name")

    def _serialize_event(self, event: Event):
        return self._to_dict(event, "type", "dict")

    def _serialize_gameobject(self, obj: GameObject):
        return self._to_dict(obj, "position", "speed", "size", "name")

    def _serialize_paddle(self, obj: Paddle):
        return self._to_dict(obj, "position", "speed", "size", "name", "side")

    def _serialize_vector2(self, vector: Vector2):
        return self._to_dict(vector, "x", "y")

    def _serialize_rectangle(self, rectangle: Rectangle):
        return self._to_dict(rectangle, "top_left", "bottom_right")

    def _serialize_config(self, config: Config):
        return self._to_dict(config, 'paddle_ratio', 'ball_ratio', 'ball_speed_ratio', 'paddle_speed_ratio', 'paddle_padding')

    def _serialize_pong(self, pong: Pong):
        return self._to_dict(pong, 'paddles', 'ball', 'config', 'size')


class Deserializer:
    def deserialize(self, input: str):
        return self._deserialize(json.loads(input))

    def _deserialize(self, obj):
        if isinstance(obj, dict):
            if "$type" in obj:
                return self._deserialize_any(obj)
            else:
                return {key: self._deserialize(value) for key, value in obj.items()}
        if isinstance(obj, list):
            return [self._deserialize(item) for item in obj]
        return obj

    def _deserialize_any(self, obj):
        type_name = obj["$type"]
        method_name = f"_deserialize_{type_name.lower()}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(obj)
        raise NotImplementedError(f"Deserialization for {type_name} is not implemented")

    def _from_dict(self, obj: dict, *attributes):
        return [self._deserialize(obj[name]) for name in attributes]

    def _deserialize_vector2(self, obj):
        return Vector2(*self._from_dict(obj, "x", "y"))

    def _deserialize_direction(self, obj):
        return Direction[obj["name"]]

    def _deserialize_event(self, obj):
        return Event(*self._from_dict(obj, "type", "dict"))

    def _deserialize_rectangle(self, obj):
        return Rectangle(*self._from_dict(obj, "top_left", "bottom_right"))

    def _deserialize_paddle(self, obj):
        return Paddle(*self._from_dict(obj, "size", "side", "position", "speed", "name"))

    def _deserialize_ball(self, obj):
        return Ball(*self._from_dict(obj, "size", "position", "speed", "name"))

    def _deserialize_config(self, obj):
        return Config(*self._from_dict(obj, 'paddle_ratio', 'ball_ratio', 'ball_speed_ratio', 'paddle_speed_ratio', 'paddle_padding'))

    def _deserialize_pong(self, obj):
        pong = Pong(*self._from_dict(obj, 'size', 'config'), paddles=[])
        pong.paddles = [self._deserialize(paddle) for paddle in obj['paddles']]
        pong.ball = self._deserialize(obj['ball'])
        return pong


DEFAULT_SERIALIZER = Serializer()
DEFAULT_DESERIALIZER = Deserializer()


def serialize(obj, serializer=DEFAULT_SERIALIZER):
    return serializer.serialize(obj)


def deserialize(input: str, deserializer=DEFAULT_DESERIALIZER):
    return deserializer.deserialize(input)


if __name__ == '__main__':
    _DEBUG = True
    pong = Pong(size=(800, 600))
    e = Event(1, {"state": pong})
    serialized = serialize(e)
    print(serialized)
    deserialized = deserialize(serialized)
    print(deserialized)
