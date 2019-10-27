from dataclasses import dataclass

from mashumaro import DataClassDictMixin

from mutapath import Path
from tests.helper import PathTest


@dataclass
class DataClass(DataClassDictMixin):
    path: Path = Path()


class TestSerialization(PathTest):
    def test_empty_serialization(self):
        expected = {'path': ''}
        actual = DataClass().to_dict()
        self.assertEqual(expected, actual)

    def test_serialization(self):
        expected = {'path': "/A/B/test1.txt"}
        actual = DataClass(Path("/A/B/test1.txt", posix=True)).to_dict()
        self.assertEqual(expected, actual)

    def test_empty_deserialization(self):
        expected = DataClass()
        actual = DataClass().from_dict({'path': ''})
        self.assertEqual(expected, actual)

    def test_deserialization(self):
        expected = DataClass(Path("/A/B/test1.txt", posix=True))
        actual = DataClass().from_dict({'path': "/A/B/test1.txt"})
        self.assertEqual(expected, actual)

    def test_deserialization_static(self):
        expected = DataClass(Path("/A/B/test1.txt", posix=True))
        actual = DataClass.from_dict({'path': "/A/B/test1.txt"})
        self.assertEqual(expected, actual)
