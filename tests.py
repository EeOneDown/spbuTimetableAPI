import unittest
from datetime import datetime, timedelta

import spbu


class TestSpbu(unittest.TestCase):
    def test_addresses(self):
        assert spbu.get_addresses()
        assert spbu.get_addresses(seating="theater")
        assert spbu.get_addresses(seating="amphitheater", capacity=100)
        assert spbu.get_addresses(seating="roundtable", capacity=50,
                                  equipment="1")
        assert spbu.get_addresses(seating="sofa")

    @unittest.expectedFailure
    def test_addresses_fail(self):
        assert spbu.get_addresses(seating="roundtable", capacity=50,
                                  equipment="pc")

    def test_classrooms(self):
        oid = "6572bd45-973c-4075-9d23-9dc728b37828"
        assert spbu.get_classrooms(oid=oid)
        assert spbu.get_classrooms(oid=oid, seating="amphitheater")
        assert spbu.get_classrooms(oid=oid, seating="theater", capacity=5000)

    @unittest.expectedFailure
    def test_classrooms_fail(self):
        assert spbu.get_classrooms(oid="asdaawdqge")

    def test_classroom_id_busy(self):
        oid = "43c30746-7ac2-430d-b820-088373d73130"
        assert spbu.is_classroom_busy(oid=oid,
                                      start=datetime.today() - timedelta(3),
                                      end=datetime.today())

    @unittest.expectedFailure
    def test_classroom_id_busy_fail(self):
        oid = "43c30746-7ac2-430d-b820-088373d73130"
        assert spbu.is_classroom_busy(oid=oid, start=datetime.today(),
                                      end=datetime.today() - timedelta(8))

    # TODO Educators and more...


if __name__ == '__main__':
    unittest.main()
