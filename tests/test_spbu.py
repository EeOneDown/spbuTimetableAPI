import unittest
from datetime import datetime, timedelta, date

import spbu
from spbu.consts import SeatingTypes, LessonsTypes


class TestSpbu(unittest.TestCase):
    def test_addresses(self):
        assert spbu.get_addresses()
        assert spbu.get_addresses(seating=SeatingTypes.THEATER)
        assert spbu.get_addresses(seating=SeatingTypes.AMPHITHEATER,
                                  capacity=100)
        assert spbu.get_addresses(seating=SeatingTypes.ROUNDTABLE, capacity=50,
                                  equipment="1")
        self.assertNotEqual(spbu.get_addresses(seating=SeatingTypes.ROUNDTABLE,
                                               capacity=50, equipment="pc"),
                            None)

    def test_classrooms(self):
        oid = "6572bd45-973c-4075-9d23-9dc728b37828"
        assert spbu.get_classrooms(oid=oid)
        assert spbu.get_classrooms(oid=oid, seating=SeatingTypes.AMPHITHEATER)
        assert spbu.get_classrooms(oid=oid, seating=SeatingTypes.THEATER,
                                   capacity=5000)

    def test_classroom_id_busy(self):
        oid = "43c30746-7ac2-430d-b820-088373d73130"
        assert spbu.is_classroom_busy(oid=oid,
                                      start=datetime.today() - timedelta(3),
                                      end=datetime.today())

    def test_educator_events(self):
        for educator_id in (1891, 3070, 4358, 1193, 10927, 5345):
            assert spbu.get_educator_term_events(educator_id)

    def test_search_educator(self):
        for educator_name in ("Абабков", "Горбунов Иван",
                              "Мамкаева Мария Алексеевна", "None"):
            assert spbu.search_educator(educator_name) is not None

    def test_extracur_divisions(self):
        assert spbu.get_extracur_divisions()

    def test_extracur_events(self):
        assert spbu.get_extracur_events("Billboard")
        assert spbu.get_extracur_events("Science",
                                        from_date=datetime.today().date())
        assert spbu.get_extracur_events("PhysTraining",
                                        from_date=date.today() + timedelta(999))

    def test_group_events(self):
        for group_id in (14887, 13722, 15158):
            assert spbu.get_group_events(group_id)
            assert spbu.get_group_events(group_id,
                                         lessons_type=LessonsTypes.PRIMARY)
            assert spbu.get_group_events(group_id, from_date=date.today(),
                                         lessons_type=LessonsTypes.FINAL)
            assert spbu.get_group_events(group_id, date.today(),
                                         date.today() + timedelta(days=10),
                                         lessons_type=LessonsTypes.ALL)

    def test_groups(self):
        for program_id in (9478, 8076, 2504):
            assert spbu.get_groups(program_id) is not None

    def test_study_divisions(self):
        assert spbu.get_study_divisions()

    def test_program_levels(self):
        for alias in ("POLS", "SOCL", "INTD", "GSOM"):
            assert spbu.get_programs(alias)

    @unittest.expectedFailure
    def test_classrooms_fail(self):
        assert spbu.get_classrooms(oid="TEST")

    @unittest.expectedFailure
    def test_classroom_id_busy_fail(self):
        oid = "43c30746-7ac2-430d-b820-088373d73130"
        assert spbu.is_classroom_busy(oid=oid, start=datetime.today(),
                                      end=datetime.today() - timedelta(8))

    @unittest.expectedFailure
    def test_educator_events_fail(self):
        assert spbu.get_educator_term_events(11)

    @unittest.expectedFailure
    def test_search_educator_fail(self):
        assert spbu.search_educator("Смирнов А. В.")

    @unittest.expectedFailure
    def test_search_educator_timeout_fail(self):
        assert spbu.search_educator("_")

    @unittest.expectedFailure
    def test_extracur_events_fail(self):
        assert spbu.get_extracur_events("TEST")

    @unittest.expectedFailure
    def test_group_events_fail_id(self):
        assert spbu.get_group_events(5545)

    @unittest.expectedFailure
    def test_group_events_fail_dates(self):
        assert spbu.get_group_events(15158,
                                     from_date=date.today() + timedelta(99),
                                     to_date=date.today())

    @unittest.expectedFailure
    def test_groups_fail(self):
        assert spbu.get_groups(1)

    @unittest.expectedFailure
    def test_program_levels_fail(self):
        assert spbu.get_programs("TEST")


if __name__ == '__main__':
    unittest.main()
