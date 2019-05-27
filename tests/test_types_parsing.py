import json
import unittest
from datetime import datetime, date, time
from unittest.mock import patch

import spbu
from typing import Optional, List, Union


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
    def _assertEducators(self, obj: List[spbu.types.EducatorId],
                         jsn: List[dict]):
        self.assertEqual(
            len(obj),
            len(jsn)
        )
        for i in range(len(obj)):
            self.assertEqual(
                obj[i].eid,
                jsn[i]['Item1']
            )
            self.assertEqual(
                obj[i].name,
                jsn[i]['Item2']
            )

    def _assertContingentUnits(self, obj: List[spbu.types.ContingentUnitName],
                               jsn: List[dict]):
        self.assertEqual(
            len(obj),
            len(jsn)
        )
        for i in range(len(obj)):
            self.assertEqual(
                obj[i].groups,
                jsn[i]['Item1']
            )
            self.assertEqual(
                obj[i].courses,
                jsn[i]['Item2']
            )

    def _assertLocations(self, obj: List[Union[spbu.types.AddressLocation,
                                               spbu.types.EventLocation]],
                         jsn: List[dict]):
        self.assertEqual(
            len(obj),
            len(jsn)
        )
        for i in range(len(obj)):
            self.assertEqual(
                obj[i].is_empty,
                jsn[i]['IsEmpty']
            )
            self.assertEqual(
                obj[i].display_name,
                jsn[i]['DisplayName']
            )
            self.assertEqual(
                obj[i].has_geographic_coordinates,
                jsn[i]['HasGeographicCoordinates']
            )
            self.assertEqual(
                obj[i].latitude,
                jsn[i]['Latitude']
            )
            self.assertEqual(
                obj[i].longitude,
                jsn[i]['Longitude']
            )
            self.assertEqual(
                obj[i].latitude_value,
                jsn[i]['LatitudeValue']
            )
            self.assertEqual(
                obj[i].longitude_value,
                jsn[i]['LongitudeValue']
            )
            if isinstance(obj[i], spbu.types.EventLocation):
                self.assertEqual(
                    obj[i].educators_display_text,
                    jsn[i]['EducatorsDisplayText']
                )
                self.assertEqual(
                    obj[i].has_educators,
                    jsn[i]['HasEducators']
                )
                self._assertEducators(
                    obj[i].educator_ids,
                    jsn[i]['EducatorIds']
                )

    def _assertExtracurEventContracts(self, obj: List[spbu.types.ExtracurEvent],
                                      jsn: List[dict]):
        self.assertEqual(
            len(obj),
            len(jsn)
        )
        for i in range(len(obj)):
            obj[i]: spbu.types.ExtracurEvent
            self.assertEqual(
                obj[i].id,
                jsn[i]['Id']
            )
            self.assertEqual(
                datetime_to_str(obj[i].start),
                jsn[i]['Start']
            )
            self.assertEqual(
                datetime_to_str(obj[i].end),
                jsn[i]['End']
            )
            self.assertEqual(
                obj[i].subject,
                jsn[i]['Subject']
            )
            self.assertEqual(
                obj[i].time_interval_string,
                jsn[i]['TimeIntervalString']
            )
            self.assertEqual(
                obj[i].date_with_time_interval_string,
                jsn[i]['DateWithTimeIntervalString']
            )
            self.assertEqual(
                obj[i].locations_display_text,
                jsn[i]['LocationsDisplayText']
            )
            self.assertEqual(
                obj[i].educators_display_text,
                jsn[i]['EducatorsDisplayText']
            )
            self.assertEqual(
                obj[i].has_educators,
                jsn[i]['HasEducators']
            )
            self.assertEqual(
                obj[i].is_cancelled,
                jsn[i]['IsCancelled']
            )
            self.assertEqual(
                obj[i].has_the_same_time_as_previous_item,
                jsn[i]['HasTheSameTimeAsPreviousItem']
            )
            self.assertEqual(
                obj[i].contingent_units_display_test,
                jsn[i]['ContingentUnitsDisplayTest']
            )
            self.assertEqual(
                obj[i].is_study,
                jsn[i]['IsStudy']
            )
            self.assertEqual(
                obj[i].all_day,
                jsn[i]['AllDay']
            )
            self.assertEqual(
                obj[i].within_the_same_day,
                jsn[i]['WithinTheSameDay']
            )
            self.assertEqual(
                obj[i].display_date_and_time_interval_string,
                jsn[i]['DisplayDateAndTimeIntervalString']
            )
            self.assertEqual(
                obj[i].view_kind,
                jsn[i]['ViewKind']
            )
            self.assertEqual(
                obj[i].division_alias,
                jsn[i]['DivisionAlias']
            )
            self.assertEqual(
                obj[i].recurrence_index,
                jsn[i]['RecurrenceIndex']
            )
            self.assertEqual(
                obj[i].full_date_with_time_interval_string,
                jsn[i]['FullDateWithTimeIntervalString']
            )
            self.assertEqual(
                obj[i].year,
                jsn[i]['Year']
            )
            self.assertEqual(
                obj[i].show_year,
                jsn[i]['ShowYear']
            )
            self.assertEqual(
                obj[i].show_immediate,
                jsn[i]['ShowImmediate']
            )
            self.assertEqual(
                obj[i].is_show_immediate_hidden,
                jsn[i]['IsShowImmediateHidden']
            )
            self.assertEqual(
                obj[i].has_agenda,
                jsn[i]['HasAgenda']
            )
            self.assertEqual(
                obj[i].is_recurrence,
                jsn[i]['IsRecurrence']
            )
            self.assertEqual(
                obj[i].subkind_display_name,
                jsn[i]['SubkindDisplayName']
            )
            self.assertEqual(
                obj[i].order_index,
                jsn[i]['OrderIndex']
            )
            self._assertLocations(
                [obj[i].location],
                [jsn[i]['Location']]
            )
            self.assertEqual(
                obj[i].is_empty,
                jsn[i]['IsEmpty']
            )
            self.assertEqual(
                date_to_dt_str(obj[i].from_date),
                jsn[i]['FromDate']
            )
            self.assertEqual(
                obj[i].from_date_string,
                jsn[i]['FromDateString']
            )
            self.assertEqual(
                obj[i].is_phys,
                jsn[i]['IsPhys']
            )
            self.assertEqual(
                obj[i].responsible_person_contacts,
                jsn[i]['ResponsiblePersonContacts']
            )

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
        classrooms = spbu.get_classrooms(oid=oid)
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
            oid=oid,
            start=datetime(year=2019, month=5, day=20, hour=10, minute=0),
            end=datetime(year=2019, month=5, day=20, hour=12, minute=0)
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
            oid=oid,
            _from=datetime(year=2019, month=5, day=20, hour=8, minute=0),
            _to=datetime(year=2019, month=5, day=25, hour=11, minute=0)
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
                self._assertEducators(
                    events[j].educator_ids,
                    dataset_events[j]['EducatorIds']
                )
                self._assertContingentUnits(
                    events[j].contingent_unit_names,
                    dataset_events[j]['ContingentUnitNames']
                )

    @patch('spbu.util.call_api', return_value=load_dataset('educators'))
    def test_educators_parsing(self, call_api):
        query = 'Смирнов'
        educators = spbu.search_educator(query=query)
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
        events_term = spbu.get_educator_term_events(educator_id=educator_id)
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
                self._assertEducators(
                    events[j].educator_ids,
                    dataset_events[j]['EducatorIds']
                )
                self._assertLocations(
                    events[j].event_locations,
                    dataset_events[j]['EventLocations']
                )
                self._assertContingentUnits(
                    events[j].contingent_unit_names,
                    dataset_events[j]['ContingentUnitNames']
                )

    @patch('spbu.util.call_api', return_value=load_dataset('educator_events'))
    def test_educator_events_parsing(self, call_api):
        educator_id = 1420
        from_date = date(2019, 4, 1)
        to_date = date(2019, 4, 8)
        educator_events = spbu.get_educator_events(
            educator_id=educator_id, _from=from_date, _to=to_date
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
                self._assertLocations(
                    events[j].event_locations,
                    dataset_events[j]['EventLocations']
                )

    @patch('spbu.util.call_api',
           return_value=load_dataset('extracur_divisions'))
    def test_extracur_divisions_parsing(self, call_api):
        extracur_divisions = spbu.get_extracur_divisions()
        dataset_extracur_divisions = call_api()

        self.assertEqual(
            len(extracur_divisions),
            len(dataset_extracur_divisions)
        )
        for i in range(len(extracur_divisions)):
            self.assertEqual(
                extracur_divisions[i].alias,
                dataset_extracur_divisions[i]['Alias']
            )
            self.assertEqual(
                extracur_divisions[i].name,
                dataset_extracur_divisions[i]['Name']
            )

    @patch('spbu.util.call_api',
           return_value=load_dataset('extracur_events'))
    def test_extracur_events_parsing(self, call_api):
        alias = 'PhysTraining'
        extracur_events = spbu.get_extracur_events(alias=alias)
        dataset_extracur_events = call_api()

        self.assertEqual(
            extracur_events.alias,
            dataset_extracur_events['Alias']
        )
        self.assertEqual(
            extracur_events.title,
            dataset_extracur_events['Title']
        )
        self.assertEqual(
            extracur_events.has_events_to_show,
            dataset_extracur_events['HasEventsToShow']
        )
        self.assertEqual(
            extracur_events.chosen_month_display_text,
            dataset_extracur_events.get('ChosenMonthDisplayText')
        )
        self.assertEqual(
            extracur_events.previous_month_display_text,
            dataset_extracur_events.get('PreviousMonthDisplayText')
        )
        self.assertEqual(
            extracur_events.previous_month_date,
            dataset_extracur_events.get('PreviousMonthDate')
        )
        self.assertEqual(
            extracur_events.next_month_display_text,
            dataset_extracur_events.get('NextMonthDisplayText')
        )
        self.assertEqual(
            extracur_events.next_month_date,
            dataset_extracur_events.get('NextMonthDate')
        )
        self.assertEqual(
            extracur_events.is_current_month_reference_available,
            dataset_extracur_events.get('IsCurrentMonthReferenceAvailable',
                                        False)
        )
        self.assertEqual(
            extracur_events.show_grouping_captions,
            dataset_extracur_events.get('ShowGroupingCaptions', False)
        )
        self.assertEqual(
            len(extracur_events.event_groupings),
            len(dataset_extracur_events.get('EventGroupings', []))
        )
        events_by_kind = extracur_events.event_groupings
        dataset_events_by_kind = dataset_extracur_events.get('EventGroupings',
                                                             [])
        for i in range(len(events_by_kind)):
            self.assertEqual(
                events_by_kind[i].caption,
                dataset_events_by_kind[i]['Caption']
            )
            self._assertExtracurEventContracts(
                events_by_kind[i].events,
                dataset_extracur_events[i]['Events']
            )
        self.assertEqual(
            extracur_events.is_previous_week_reference_available,
            dataset_extracur_events['IsPreviousWeekReferenceAvailable']
        )
        self.assertEqual(
            extracur_events.is_next_week_reference_available,
            dataset_extracur_events['IsNextWeekReferenceAvailable']
        )
        self.assertEqual(
            extracur_events.is_current_week_reference_available,
            dataset_extracur_events['IsCurrentWeekReferenceAvailable']
        )
        self.assertEqual(
            date_to_str(extracur_events.previous_week_monday),
            dataset_extracur_events['PreviousWeekMonday']
        )
        self.assertEqual(
            date_to_str(extracur_events.next_week_monday),
            dataset_extracur_events['NextWeekMonday']
        )
        self.assertEqual(
            extracur_events.week_display_text,
            dataset_extracur_events['WeekDisplayText']
        )
        self.assertEqual(
            date_to_str(extracur_events.week_monday),
            dataset_extracur_events['WeekMonday']
        )
        self._assertExtracurEventContracts(
            extracur_events.earlier_events,
            dataset_extracur_events['EarlierEvents']
        )
        self.assertEqual(
            len(extracur_events.days),
            len(dataset_extracur_events['Days'])
        )
        days = extracur_events.days
        dataset_days = dataset_extracur_events['Days']
        for i in range(len(days)):
            self.assertEqual(
                date_to_dt_str(days[i].day),
                dataset_days[i]['Day']
            )
            self.assertEqual(
                days[i].day_string,
                dataset_days[i]['DayString']
            )
            self._assertExtracurEventContracts(
                days[i].day_events,
                dataset_days[i]['DayEvents']
            )

    @patch('spbu.util.call_api', return_value=load_dataset('groups_events'))
    def test_groups_events_parsing(self, call_api):
        group_id = 19082
        group_events = spbu.get_group_events(group_id=group_id)
        dataset_group_events = call_api()

        self.assertEqual(
            group_events.student_group_id,
            dataset_group_events['StudentGroupId']
        )
        self.assertEqual(
            group_events.student_group_display_name,
            dataset_group_events['StudentGroupDisplayName']
        )
        self.assertEqual(
            group_events.timetable_display_name,
            dataset_group_events['TimeTableDisplayName']
        )
        self.assertEqual(
            date_to_str(group_events.previous_week_monday),
            dataset_group_events['PreviousWeekMonday']
        )
        self.assertEqual(
            date_to_str(group_events.next_week_monday),
            dataset_group_events['NextWeekMonday']
        )
        self.assertEqual(
            group_events.is_previous_week_reference_available,
            dataset_group_events['IsPreviousWeekReferenceAvailable']
        )
        self.assertEqual(
            group_events.is_next_week_reference_available,
            dataset_group_events['IsNextWeekReferenceAvailable']
        )
        self.assertEqual(
            group_events.is_current_week_reference_available,
            dataset_group_events['IsCurrentWeekReferenceAvailable']
        )
        self.assertEqual(
            group_events.week_display_text,
            dataset_group_events['WeekDisplayText']
        )
        self.assertEqual(
            date_to_str(group_events.week_monday),
            dataset_group_events['WeekMonday']
        )
        days = group_events.days
        dataset_days = dataset_group_events['Days']
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
                    events[j].contingent_units_display_test,
                    dataset_events[j]['ContingentUnitsDisplayTest']
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
                self._assertLocations(
                    events[j].event_locations,
                    dataset_events[j]['EventLocations']
                )
                self._assertEducators(
                    events[j].educator_ids,
                    dataset_events[j]['EducatorIds']
                )

    @patch('spbu.util.call_api', return_value=load_dataset('study_divisions'))
    def test_study_divisions_parsing(self, call_api):
        divisions = spbu.get_study_divisions()
        dataset_divisions = call_api()

        self.assertEqual(
            len(divisions),
            len(dataset_divisions)
        )
        for i in range(len(divisions)):
            self.assertEqual(
                divisions[i].oid,
                dataset_divisions[i]['Oid']
            )
            self.assertEqual(
                divisions[i].alias,
                dataset_divisions[i]['Alias']
            )
            self.assertEqual(
                divisions[i].name,
                dataset_divisions[i]['Name']
            )

    @patch('spbu.util.call_api', return_value=load_dataset('study_levels'))
    def test_study_levels_parsing(self, call_api):
        alias = 'LAWS'
        levels = spbu.get_study_levels(alias=alias)
        dataset_levels = call_api()

        self.assertEqual(
            len(levels),
            len(dataset_levels)
        )
        for i in range(len(levels)):
            self.assertEqual(
                levels[i].study_level_name,
                dataset_levels[i]['StudyLevelName']
            )
            self.assertEqual(
                levels[i].study_level_name_english,
                dataset_levels[i]['StudyLevelNameEnglish']
            )
            self.assertEqual(
                levels[i].has_course6,
                dataset_levels[i]['HasCourse6']
            )
            self.assertEqual(
                len(levels[i].study_program_combinations),
                len(dataset_levels[i]['StudyProgramCombinations'])
            )
            combinations = levels[i].study_program_combinations
            dataset_combinations = dataset_levels[i]['StudyProgramCombinations']
            for j in range(len(combinations)):
                self.assertEqual(
                    combinations[j].name,
                    dataset_combinations[j]['Name']
                )
                self.assertEqual(
                    combinations[j].name_english,
                    dataset_combinations[j]['NameEnglish']
                )
                self.assertEqual(
                    len(combinations[j].admission_years),
                    len(dataset_combinations[j]['AdmissionYears'])
                )
                years = combinations[j].admission_years
                dataset_years = dataset_combinations[j]['AdmissionYears']
                for k in range(len(years)):
                    self.assertEqual(
                        years[k].study_program_id,
                        dataset_years[k]['StudyProgramId']
                    )
                    self.assertEqual(
                        years[k].year_name,
                        dataset_years[k]['YearName']
                    )
                    self.assertEqual(
                        years[k].year_number,
                        dataset_years[k]['YearNumber']
                    )
                    self.assertEqual(
                        years[k].is_empty,
                        dataset_years[k]['IsEmpty']
                    )
                    self.assertEqual(
                        years[k].public_division_alias,
                        dataset_years[k]['PublicDivisionAlias']
                    )


if __name__ == '__main__':
    unittest.main()
