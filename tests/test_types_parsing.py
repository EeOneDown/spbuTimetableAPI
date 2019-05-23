import json
import unittest
from datetime import datetime, date, time
from unittest.mock import patch

import spbu
from typing import Optional


def load_dataset(filename: str):
    with open(f'datasets/{filename}.json', 'r') as f:
        dataset = json.loads(f.read())
    return dataset


def datetime_to_str(dt: Optional[datetime]) -> Optional[str]:
    if not dt:
        return None
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def date_to_dt_str(d: Optional[date]) -> Optional[str]:
    if not d:
        return None
    return d.strftime('%Y-%m-%dT%H:%M:%S')


def date_to_str(d: Optional[date]) -> Optional[str]:
    if not d:
        return None
    return d.strftime('%Y-%m-%d')


def time_to_str(t: Optional[time]) -> Optional[str]:
    if not t:
        return None
    return t.strftime('%H:%M:%S')


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

    @patch('spbu.util.call_api', return_value=load_dataset('educators'))
    def test_educators_parsing(self, call_api):
        query = 'Смирнов'
        educators = spbu.search_educator(query)
        educators_dataset = call_api()['Educators']

        self.assertEqual(
            len(educators),
            len(educators_dataset)
        )
        for i in range(len(educators)):
            self.assertEqual(
                educators[i].id,
                educators_dataset[i]['Id']
            )
            self.assertEqual(
                educators[i].display_name,
                educators_dataset[i]['DisplayName']
            )
            self.assertEqual(
                educators[i].full_name,
                educators_dataset[i]['FullName']
            )
            self.assertEqual(
                len(educators[i].employments),
                len(educators_dataset[i]['Employments'])
            )
            employments = educators[i].employments
            employments_dataset = educators_dataset[i]['Employments']
            for j in range(len(employments)):
                self.assertEqual(
                    len(employments[j].position),
                    len(employments_dataset[j]['Position'])
                )
                self.assertEqual(
                    len(employments[j].department),
                    len(employments_dataset[j]['Department'])
                )

    @patch('spbu.util.call_api',
           return_value=load_dataset('educator_events_term'))
    def test_educator_events_term_parsing(self, call_api):
        educator_id = 2254
        events_term = spbu.get_educator_term_events(educator_id)
        events_term_dataset = call_api()

        self.assertEqual(
            events_term.title,
            events_term_dataset['Title']
        )
        self.assertEqual(
            events_term.educator_display_text,
            events_term_dataset['EducatorDisplayText']
        )
        self.assertEqual(
            events_term.educator_long_display_text,
            events_term_dataset['EducatorLongDisplayText']
        )
        self.assertEqual(
            events_term.date_range_display_text,
            events_term_dataset['DateRangeDisplayText']
        )
        self.assertEqual(
            events_term.educator_master_id,
            events_term_dataset['EducatorMasterId']
        )
        self.assertEqual(
            events_term.is_spring_term,
            events_term_dataset['IsSpringTerm']
        )
        self.assertEqual(
            date_to_dt_str(events_term.from_date),
            events_term_dataset['From']
        )
        self.assertEqual(
            date_to_dt_str(events_term.to_date),
            events_term_dataset['To']
        )
        self.assertEqual(
            events_term.next,
            events_term_dataset['Next']
        )
        self.assertEqual(
            events_term.spring_term_link_available,
            events_term_dataset['SpringTermLinkAvailable']
        )
        self.assertEqual(
            events_term.autumn_term_link_available,
            events_term_dataset['AutumnTermLinkAvailable']
        )
        self.assertEqual(
            events_term.has_events,
            events_term_dataset['HasEvents']
        )
        days = events_term.educator_events_days
        dataset_days = events_term_dataset['EducatorEventsDays']
        self.assertEqual(
            len(days),
            len(dataset_days)
        )
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
                    len(events[j].event_locations),
                    len(dataset_events[j]['EventLocations'])
                )
                locations = events[j].event_locations
                dataset_locations = dataset_events[j]['EventLocations']
                for k in range(len(locations)):
                    self.assertEqual(
                        locations[k].is_empty,
                        dataset_locations[k]['IsEmpty']
                    )
                    self.assertEqual(
                        locations[k].display_name,
                        dataset_locations[k]['DisplayName']
                    )
                    self.assertEqual(
                        locations[k].has_geographic_coordinates,
                        dataset_locations[k]['HasGeographicCoordinates']
                    )
                    self.assertEqual(
                        locations[k].latitude,
                        dataset_locations[k]['Latitude']
                    )
                    self.assertEqual(
                        locations[k].longitude,
                        dataset_locations[k]['Longitude']
                    )
                    self.assertEqual(
                        locations[k].latitude_value,
                        dataset_locations[k]['LatitudeValue']
                    )
                    self.assertEqual(
                        locations[k].longitude_value,
                        dataset_locations[k]['LongitudeValue']
                    )
                    self.assertEqual(
                        locations[k].educators_display_text,
                        dataset_locations[k]['EducatorsDisplayText']
                    )
                    self.assertEqual(
                        locations[k].has_educators,
                        dataset_locations[k]['HasEducators']
                    )
                    self.assertEqual(
                        len(locations[k].educator_ids),
                        len(dataset_locations[k]['EducatorIds'])
                    )
                    educators = locations[k].educator_ids
                    dataset_educators = dataset_locations[k]['EducatorIds']
                    for l in range(len(educators)):
                        self.assertEqual(
                            educators[l].eid,
                            dataset_educators[l]['Item1']
                        )
                        self.assertEqual(
                            educators[l].name,
                            dataset_educators[l]['Item2']
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

    @patch('spbu.util.call_api', return_value=load_dataset('educator_events'))
    def test_1420_parsing(self, call_api):
        educator_id = 1420
        from_date = date(2019, 4, 1)
        to_date = date(2019, 4, 8)
        educator_events = spbu.get_educator_events(
            educator_id, from_date, to_date
        )
        dataset_educator_events = call_api()

        self.assertEqual(
            educator_events.educator_master_id,
            dataset_educator_events['EducatorMasterId']
        )
        self.assertEqual(
            educator_events.educator_display_text,
            dataset_educator_events['EducatorDisplayText']
        )
        self.assertEqual(
            educator_events.educator_long_display_text,
            dataset_educator_events['EducatorLongDisplayText']
        )
        self.assertEqual(
            date_to_str(educator_events.previous_week_monday),
            dataset_educator_events['PreviousWeekMonday']
        )
        self.assertEqual(
            date_to_str(educator_events.next_week_monday),
            dataset_educator_events['NextWeekMonday']
        )
        self.assertEqual(
            educator_events.is_previous_week_reference_available,
            dataset_educator_events['IsPreviousWeekReferenceAvailable']
        )
        self.assertEqual(
            educator_events.is_next_week_reference_available,
            dataset_educator_events['IsNextWeekReferenceAvailable']
        )
        self.assertEqual(
            educator_events.is_current_week_reference_available,
            dataset_educator_events['IsCurrentWeekReferenceAvailable']
        )
        self.assertEqual(
            educator_events.week_display_text,
            dataset_educator_events['WeekDisplayText']
        )
        self.assertEqual(
            date_to_str(educator_events.week_monday),
            dataset_educator_events['WeekMonday']
        )
        days = educator_events.educator_events_days
        dataset_days = dataset_educator_events['EducatorEventsDays']
        self.assertEqual(
            len(days),
            len(dataset_days)
        )
        for i in range(len(days)):
            self.assertEqual(
                date_to_dt_str(days[i].day),
                dataset_days[i]['Day']
            )
            self.assertEqual(
                days[i].day_string,
                dataset_days[i]['DayString']
            )
            events = days[i].day_study_events
            dataset_events = dataset_days[i]['DayStudyEvents']
            self.assertEqual(
                len(events),
                len(dataset_events)
            )
            for j in range(len(events)):
                self.assertEqual(
                    events[j].study_events_timetable_kind_code,
                    dataset_events[j]['StudyEventsTimeTableKindCode']
                )
                self.assertEqual(
                    datetime_to_str(events[j].start),
                    dataset_events[j]['Start']
                )
                self.assertEqual(
                    datetime_to_str(events[j].end),
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
                    events[j].date_with_time_interval_string,
                    dataset_events[j]['DateWithTimeIntervalString']
                )
                self.assertEqual(
                    events[j].display_date_and_time_interval_string,
                    dataset_events[j]['DisplayDateAndTimeIntervalString']
                )
                self.assertEqual(
                    events[j].locations_display_text,
                    dataset_events[j]['LocationsDisplayText']
                )
                self.assertEqual(
                    events[j].educators_display_text,
                    dataset_events[j]['EducatorsDisplayText']
                )
                self.assertEqual(
                    events[j].has_educators,
                    dataset_events[j]['HasEducators']
                )
                self.assertEqual(
                    events[j].is_cancelled,
                    dataset_events[j]['IsCancelled']
                )
                self.assertEqual(
                    events[j].contingent_unit_name,
                    dataset_events[j]['ContingentUnitName']
                )
                self.assertEqual(
                    events[j].division_and_course,
                    dataset_events[j]['DivisionAndCourse']
                )
                self.assertEqual(
                    events[j].is_assigned,
                    dataset_events[j]['IsAssigned']
                )
                self.assertEqual(
                    events[j].time_was_changed,
                    dataset_events[j]['TimeWasChanged']
                )
                self.assertEqual(
                    events[j].locations_were_changed,
                    dataset_events[j]['LocationsWereChanged']
                )
                self.assertEqual(
                    events[j].educators_were_reassigned,
                    dataset_events[j]['EducatorsWereReassigned']
                )
                self.assertEqual(
                    events[j].elective_disciplines_count,
                    dataset_events[j]['ElectiveDisciplinesCount']
                )
                self.assertEqual(
                    events[j].is_elective,
                    dataset_events[j]['IsElective']
                )
                self.assertEqual(
                    events[j].has_the_same_time_as_previous_item,
                    dataset_events[j]['HasTheSameTimeAsPreviousItem']
                )
                self.assertEqual(
                    events[j].is_study,
                    dataset_events[j]['IsStudy']
                )
                self.assertEqual(
                    events[j].all_day,
                    dataset_events[j]['AllDay']
                )
                self.assertEqual(
                    events[j].within_the_same_day,
                    dataset_events[j]['WithinTheSameDay']
                )
                self.assertEqual(
                    len(events[j].event_locations),
                    len(dataset_events[j]['EventLocations'])
                )
                locations = events[j].event_locations
                dataset_locations = dataset_events[j]['EventLocations']
                for k in range(len(locations)):
                    self.assertEqual(
                        locations[k].is_empty,
                        dataset_locations[k]['IsEmpty']
                    )
                    self.assertEqual(
                        locations[k].display_name,
                        dataset_locations[k]['DisplayName']
                    )
                    self.assertEqual(
                        locations[k].has_geographic_coordinates,
                        dataset_locations[k]['HasGeographicCoordinates']
                    )
                    self.assertEqual(
                        locations[k].latitude,
                        dataset_locations[k]['Latitude']
                    )
                    self.assertEqual(
                        locations[k].longitude,
                        dataset_locations[k]['Longitude']
                    )
                    self.assertEqual(
                        locations[k].latitude_value,
                        dataset_locations[k]['LatitudeValue']
                    )
                    self.assertEqual(
                        locations[k].longitude_value,
                        dataset_locations[k]['LongitudeValue']
                    )
                    self.assertEqual(
                        locations[k].educators_display_text,
                        dataset_locations[k]['EducatorsDisplayText']
                    )
                    self.assertEqual(
                        locations[k].has_educators,
                        dataset_locations[k]['HasEducators']
                    )
                    self.assertEqual(
                        len(locations[k].educator_ids),
                        len(dataset_locations[k]['EducatorIds'])
                    )
                    educators = locations[k].educator_ids
                    dataset_educators = dataset_locations[k]['EducatorIds']
                    for l in range(len(educators)):
                        self.assertEqual(
                            educators[l].eid,
                            dataset_educators[l]['Item1']
                        )
                        self.assertEqual(
                            educators[l].name,
                            dataset_educators[l]['Item2']
                        )


if __name__ == '__main__':
    unittest.main()
