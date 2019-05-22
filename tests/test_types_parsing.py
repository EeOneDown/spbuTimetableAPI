import json
import unittest
from datetime import datetime, time
from unittest.mock import patch

import spbu


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
        dataset_addresses = call_api()

        self.assertEqual(len(addresses), len(dataset_addresses))
        for i in range(len(addresses)):
            self.assertEqual(
                addresses[i].oid,
                dataset_addresses[i]['Oid']
            )
            self.assertEqual(
                addresses[i].display_name,
                dataset_addresses[i]['DisplayName1']
            )
            self.assertEqual(
                addresses[i].matches,
                dataset_addresses[i]['matches']
            )
            self.assertEqual(
                addresses[i].wanting_equipment,
                dataset_addresses[i]['wantingEquipment']
            )

    @patch('spbu.util.call_api', return_value=load_dataset('classrooms'))
    def test_classrooms_parsing(self, call_api):
        oid = '6572bd45-973c-4075-9d23-9dc728b37828'
        classrooms = spbu.get_classrooms(oid)
        dataset_classrooms = call_api()

        self.assertEqual(len(classrooms), len(dataset_classrooms))
        for i in range(len(classrooms)):
            self.assertEqual(
                classrooms[i].oid,
                dataset_classrooms[i]['Oid']
            )
            self.assertEqual(
                classrooms[i].display_name,
                dataset_classrooms[i]['DisplayName1']
            )
            self.assertEqual(
                classrooms[i].seating_type,
                dataset_classrooms[i]['SeatingType']
            )
            self.assertEqual(
                classrooms[i].capacity,
                dataset_classrooms[i]['Capacity']
            )
            self.assertEqual(
                classrooms[i].additional_info,
                dataset_classrooms[i]['AdditionalInfo']
            )
            self.assertEqual(
                classrooms[i].wanting_equipment,
                dataset_classrooms[i]['wantingEquipment']
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
        dataset_is_busy = call_api()

        self.assertEqual(
            is_busy.oid,
            dataset_is_busy['Oid']
        )
        self.assertEqual(
            datetime_to_str(is_busy.from_datetime),
            dataset_is_busy['From']
        )
        self.assertEqual(
            datetime_to_str(is_busy.to_datetime),
            dataset_is_busy['To']
        )
        self.assertEqual(
            is_busy.is_busy,
            dataset_is_busy['IsBusy']
        )

    @patch('spbu.util.call_api', return_value=load_dataset('classroom_events'))
    def test_classroom_events_parsing(self, call_api):
        oid = '8ba13bec-5213-4114-bd77-fc202c6aa4e5'
        classroom_events = spbu.get_classroom_events(
            oid,
            datetime(year=2019, month=5, day=20, hour=8, minute=0),
            datetime(year=2019, month=5, day=25, hour=11, minute=0)
        )
        dataset_classroom_events = call_api()
        self.assertEqual(
            classroom_events.oid,
            dataset_classroom_events['Oid']
        )
        self.assertEqual(
            datetime_to_str(classroom_events.from_datetime),
            dataset_classroom_events['From']
        )
        self.assertEqual(
            datetime_to_str(classroom_events.to_datetime),
            dataset_classroom_events['To']
        )
        self.assertEqual(
            classroom_events.display_text,
            dataset_classroom_events['DisplayText']
        )
        self.assertEqual(
            classroom_events.has_events,
            dataset_classroom_events['HasEvents']
        )
        self.assertEqual(
            len(classroom_events.classroom_events_days),
            len(dataset_classroom_events['ClassroomEventsDays'])
        )
        days = classroom_events.classroom_events_days
        dataset_days = dataset_classroom_events['ClassroomEventsDays']
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
