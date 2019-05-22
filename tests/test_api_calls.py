import unittest
from datetime import datetime, timedelta, date

import spbu


class TestApiCalls(unittest.TestCase):
    def _assertIsListOfInstances(self, lst: list, cls: type):
        for obj in lst:
            self.assertIsInstance(obj, cls)

    def test_addresses(self):
        params_list = [
            dict(),
            dict(seating=spbu.consts.SeatingTypes.THEATER),
            dict(
                seating=spbu.consts.SeatingTypes.AMPHITHEATER,
                capacity=100
            ),
            dict(
                seating=spbu.consts.SeatingTypes.ROUNDTABLE,
                capacity=50,
                equipment="1"
            ),
            dict(
                seating=spbu.consts.SeatingTypes.ROUNDTABLE,
                capacity=50,
                equipment="pc"
            ),
        ]
        for params in params_list:
            self._assertIsListOfInstances(
                spbu.get_addresses(**params),
                spbu.types.Address
            )

    def test_classrooms(self):
        oid = "6572bd45-973c-4075-9d23-9dc728b37828"
        params_list = [
            dict(oid=oid, seating=spbu.consts.SeatingTypes.AMPHITHEATER),
            dict(oid=oid, seating=spbu.consts.SeatingTypes.THEATER,
                 capacity=5000)
        ]
        for params in params_list:
            self._assertIsListOfInstances(
                spbu.get_classrooms(**params),
                spbu.types.Classroom
            )

    def test_classroom_id_busy(self):
        oid = "43c30746-7ac2-430d-b820-088373d73130"
        self.assertIsInstance(
            spbu.is_classroom_busy(
                oid=oid,
                start=datetime.today() - timedelta(3),
                end=datetime.today()
            ),
            spbu.types.ClassroomBusyness
        )

    def test_classroom_events(self):
        oid = "43c30746-7ac2-430d-b820-088373d73130"
        self.assertIsInstance(
            spbu.get_classroom_events(
                oid=oid,
                _from=datetime.today() - timedelta(3),
                _to=datetime.today()
            ),
            spbu.types.ClassroomEvents
        )

    def test_educator_events(self):
        for educator_id in (1891, 3070, 4358, 1193, 10927, 5345):
            self.assertIsInstance(
                spbu.get_educator_term_events(educator_id),
                spbu.types.EducatorEventsTerm
            )

    def test_search_educator(self):
        queries = ("Абабков", "Горбунов Иван", "Мамкаева Мария Алексеевна",
                   "None")
        for query in queries:
            self._assertIsListOfInstances(
                spbu.search_educator(query),
                spbu.types.Educator
            )

    def test_extracur_divisions(self):
        self._assertIsListOfInstances(
            spbu.get_extracur_divisions(),
            spbu.types.ExtracurDivision
        )

    def test_extracur_events(self):
        params_list = [
            dict(alias="Billboard"),
            dict(alias="Science", from_date=datetime.today().date()),
            dict(alias="PhysTraining", from_date=date.today() + timedelta(999))
        ]
        for params in params_list:
            self.assertIsInstance(
                spbu.get_extracur_events(**params),
                spbu.types.ExtracurEvents
            )

    def test_group_events(self):
        group_ids = (14887, 13722, 15158)
        params_list = [
            dict(),
            dict(lessons_type=spbu.consts.LessonsTypes.PRIMARY),
            dict(from_date=date.today(),
                 lessons_type=spbu.consts.LessonsTypes.FINAL),
            dict(from_date=date.today(),
                 to_date=date.today() + timedelta(days=10),
                 lessons_type=spbu.consts.LessonsTypes.ALL)
        ]
        for group_id in group_ids:
            for params in params_list:
                self.assertIsInstance(
                    spbu.get_group_events(group_id, **params),
                    spbu.types.GroupEvents
                )

    def test_groups(self):
        program_ids = (9478, 8076, 2504)
        for program_id in program_ids:
            self._assertIsListOfInstances(
                spbu.get_groups(program_id),
                spbu.types.PGGroup
            )

    def test_study_divisions(self):
        self._assertIsListOfInstances(
            spbu.get_study_divisions(),
            spbu.types.SDStudyDivision
        )

    def test_program_levels(self):
        aliases = ("POLS", "SOCL", "INTD", "GSOM")
        for alias in aliases:
            self._assertIsListOfInstances(
                spbu.get_programs(alias),
                spbu.types.SDPLStudyLevel
            )

    @unittest.expectedFailure
    def test_classrooms_fail(self):
        spbu.get_classrooms(oid="TEST")

    @unittest.expectedFailure
    def test_classroom_id_busy_fail(self):
        oid = "43c30746-7ac2-430d-b820-088373d73130"
        spbu.is_classroom_busy(
            oid=oid, start=datetime.today(), end=datetime.today() - timedelta(8)
        )

    @unittest.expectedFailure
    def test_educator_events_fail(self):
        spbu.get_educator_term_events(11)

    @unittest.expectedFailure
    def test_search_educator_fail(self):
        spbu.search_educator("Смирнов А. В.")

    @unittest.expectedFailure
    def test_search_educator_timeout_fail(self):
        spbu.search_educator("_")

    @unittest.expectedFailure
    def test_extracur_events_fail(self):
        spbu.get_extracur_events("TEST")

    @unittest.expectedFailure
    def test_group_events_fail_id(self):
        spbu.get_group_events(5545)

    @unittest.expectedFailure
    def test_group_events_fail_dates(self):
        spbu.get_group_events(
            15158, from_date=date.today() + timedelta(99), to_date=date.today()
        )

    @unittest.expectedFailure
    def test_groups_fail(self):
        spbu.get_groups(1)

    @unittest.expectedFailure
    def test_program_levels_fail(self):
        spbu.get_programs("TEST")


if __name__ == '__main__':
    unittest.main()
