import unittest
from dpongpy import Pong
import dpongpy.remote.presentation as presentation
from pygame.event import Event
import json
import pathlib


DIR_CURRENT = pathlib.Path(__file__).parent


class TestPresentation(unittest.TestCase):
    def setUp(self):
        pong = Pong(size=(800, 600))
        pong.ball.speed = (1, 1)
        pong.update(1.5)
        self.event = Event(1, {"state": pong})
        self.serialized_event = (DIR_CURRENT / "expected.json").read_text()

    def test_serialize_event(self):
        actual = json.loads(presentation.serialize(self.event))
        expected = json.loads(self.serialized_event)
        self.assertEqual(actual, expected)

    def test_deserialize_event(self):
        actual = presentation.deserialize(self.serialized_event)
        expected = self.event
        self.assertEqual(actual, expected)