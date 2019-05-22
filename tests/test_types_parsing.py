import unittest
from unittest.mock import patch
from datetime import datetime, time
import spbu
import json


def load_dataset(filename: str):
    with open(f'datasets/{filename}.json', 'r') as f:
        dataset = json.loads(f.read())
    return dataset


def datetime_to_str(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def time_to_str(dt: time) -> str:
    return dt.strftime('%H:%M:%S')


class TestTypesParsing(unittest.TestCase):
    @patch('spbu.util.call_api', return_value=load_dataset('addresses'))
    def test_addresses_parsing(self, call_api):
        addresses = spbu.get_addresses()
        for i in range(len(addresses)):
            self.assertEqual(
                addresses[i].oid,
                call_api()[i]['Oid']
            )
            self.assertEqual(
                addresses[i].display_name,
                call_api()[i]['DisplayName1']
            )
            self.assertEqual(
                addresses[i].matches,
                call_api()[i]['matches']
            )
            self.assertEqual(
                addresses[i].wanting_equipment,
                call_api()[i]['wantingEquipment']
            )

    @patch('spbu.util.call_api', return_value=load_dataset('classrooms'))
    def test_classrooms_parsing(self, call_api):
        oid = '6572bd45-973c-4075-9d23-9dc728b37828'
        classrooms = spbu.get_classrooms(oid)

        self.assertEqual(len(classrooms), len(call_api()))
        for i in range(len(classrooms)):
            self.assertEqual(
                classrooms[i].oid,
                call_api()[i]['Oid']
            )
            self.assertEqual(
                classrooms[i].display_name,
                call_api()[i]['DisplayName1']
            )
            self.assertEqual(
                classrooms[i].seating_type,
                call_api()[i]['SeatingType']
            )
            self.assertEqual(
                classrooms[i].capacity,
                call_api()[i]['Capacity']
            )
            self.assertEqual(
                classrooms[i].additional_info,
                call_api()[i]['AdditionalInfo']
            )
            self.assertEqual(
                classrooms[i].wanting_equipment,
                call_api()[i]['wantingEquipment']
            )

    @patch('spbu.util.call_api',
           return_value=load_dataset('classroom_busyness'))
    def test_classroom_busyness_parsing(self, call_api):
        oid = '8ba13bec-5213-4114-bd77-fc202c6aa4e5'
        is_busy = spbu.is_classroom_busy(
            oid,
            datetime(year=2019, month=5, day=20, hour=10, minute=0),
            datetime(year=2019, month=5, day=20, hour=12, minute=0)
        )
        self.assertEqual(
            is_busy.oid,
            call_api()['Oid']
        )
        self.assertEqual(
            datetime_to_str(is_busy.from_datetime),
            call_api()['From']
        )
        self.assertEqual(
            datetime_to_str(is_busy.to_datetime),
            call_api()['To']
        )
        self.assertEqual(
            is_busy.is_busy,
            call_api()['IsBusy']
        )

    @patch('spbu.util.call_api', return_value=load_dataset('classroom_events'))
    def test_classroom_events_parsing(self, call_api):
        oid = '8ba13bec-5213-4114-bd77-fc202c6aa4e5'
        classroom_events = spbu.get_classroom_events(
            oid,
            datetime(year=2019, month=5, day=20, hour=8, minute=0),
            datetime(year=2019, month=5, day=25, hour=11, minute=0)
        )
        self.assertEqual(
            classroom_events.oid,
            call_api()['Oid']
        )
        self.assertEqual(
            datetime_to_str(classroom_events.from_datetime),
            call_api()['From']
        )
        self.assertEqual(
            datetime_to_str(classroom_events.to_datetime),
            call_api()['To']
        )
        self.assertEqual(
            classroom_events.display_text,
            call_api()['DisplayText']
        )
        self.assertEqual(
            classroom_events.has_events,
            call_api()['HasEvents']
        )
        self.assertEqual(
            len(classroom_events.classroom_events_days),
            len(call_api()['ClassroomEventsDays'])
        )
        days = classroom_events.classroom_events_days
        dataset_days = call_api()['ClassroomEventsDays']
        for i in range(len(days)):
            self.assertEqual(
                days[i].day,
                dataset_days[i]['Day']
            )
            self.assertEqual(
                days[i].day_string,
                dataset_days[i]['DayString']
            )
            self.assertEqual(
                days[i].day_study_events_count,
                dataset_days[i]['DayStudyEventsCount']
            )
            self.assertEqual(
                len(days[i].day_study_events),
                len(dataset_days[i]['DayStudyEvents'])
            )
            events = days[i].day_study_events
            dataset_events = dataset_days[i]['DayStudyEvents']
            for j in range(len(events)):
                self.assertEqual(
                    time_to_str(events[j].start),
                    dataset_events[j]['Start']
                )
                self.assertEqual(
                    time_to_str(events[j].end),
                    dataset_events[j]['End']
                )
                self.assertEqual(
                    events[j].subject,
                    dataset_events[j]['Subject']
                )
                self.assertEqual(
                    events[j].time_interval_string,
                    dataset_events[j]['TimeIntervalString']
                )
                self.assertEqual(
                    events[j].dates,
                    dataset_events[j]['Dates']
                )
                self.assertEqual(
                    events[j].educators_display_text,
                    dataset_events[j]['EducatorsDisplayText']
                )
                self.assertEqual(
                    events[j].is_cancelled,
                    dataset_events[j]['IsCanceled']
                )
                self.assertEqual(
                    events[j].study_events_timetable_kind_code,
                    dataset_events[j]['StudyEventsTimeTableKindCode']
                )
                self.assertEqual(
                    len(events[j].educator_ids),
                    len(dataset_events[j]['EducatorIds'])
                )
                educators = events[j].educator_ids
                dataset_educators = dataset_events[j]['EducatorIds']
                for k in range(len(educators)):
                    self.assertEqual(
                        educators[k].eid,
                        dataset_educators[k]['Item1']
                    )
                    self.assertEqual(
                        educators[k].name,
                        dataset_educators[k]['Item2']
                    )
                self.assertEqual(
                    len(events[j].contingent_unit_names),
                    len(dataset_events[j]['ContingentUnitNames'])
                )
                units = events[j].contingent_unit_names
                dataset_units = dataset_events[j]['ContingentUnitNames']
                for k in range(len(units)):
                    self.assertEqual(
                        units[k].groups,
                        dataset_units[k]['Item1']
                    )
                    self.assertEqual(
                        units[k].courses,
                        dataset_units[k]['Item2']
                    )


if __name__ == '__main__':
    unittest.main()
