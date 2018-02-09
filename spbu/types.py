# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime, date

import six
from requests import models

from spbu.consts import error_msg


class _JsonDeserializable:
    """
    Subclasses of this class are guaranteed to be able to be created from a
    json-style dict or json formatted string.
    All subclasses of this class must override de_json.
    """

    @classmethod
    def de_json(cls, json_type):
        """
        Returns an instance of this class from the given json dict or string.

        This function must be overridden by subclasses.
        :return: an instance of this class created from the given json dict or
                 string.
        """
        raise NotImplementedError

    @staticmethod
    def check_json(json_type):
        """
        Checks whether json_type is a dict or a string. If it is already a dict,
        it is returned as-is.
        If it is not, it is converted to a dict by means of
        json.loads(json_type)
        :param json_type:
        :type json_type: dict or str
        :return:
        """
        try:
            str_types = (str, unicode)
        except NameError:
            str_types = (str,)

        if type(json_type) == dict:
            return json_type
        elif type(json_type) in str_types:
            return json.loads(json_type)
        else:
            raise ValueError("json_type should be a json dict or string.")

    def __str__(self):
        d = {}
        for x, y in six.iteritems(self.__dict__):
            if hasattr(y, '__dict__'):
                d[x] = y.__dict__
            else:
                d[x] = y

        return six.text_type(d)


class StudyDivision(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        oid = obj['Oid']
        alias = obj['Alias']
        name = obj['Name']
        return cls(oid, alias, name)

    def __init__(self, oid, alias, name):
        """

        :type oid: str
        :type alias: str
        :type name: str
        """
        self.oid = oid
        self.alias = alias
        self.name = name


class StudyProgramLevel(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        study_level_name = obj['StudyLevelName']
        study_level_name_english = obj['StudyLevelNameEnglish']
        has_course6 = obj['HasCourse6']
        study_program_combinations = []
        for sub_obj in obj['StudyProgramCombinations']:
            study_program_combinations.append(
                StudyProgramCombination.de_json(sub_obj)
            )
        return cls(study_level_name, study_level_name_english, has_course6,
                   study_program_combinations)

    def __init__(self, study_level_name, study_level_name_english, has_course6,
                 study_program_combinations):
        """

        :type study_level_name: str
        :type study_level_name_english: str
        :type has_course6: bool
        :type study_program_combinations: list of StudyProgramCombination
        """
        self.study_level_name = study_level_name
        self.study_level_name_english = study_level_name_english
        self.has_course6 = has_course6
        self.study_program_combinations = study_program_combinations


class StudyProgramCombination(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        name = obj['Name']
        name_english = obj['NameEnglish']
        admission_years = []
        for sub_obj in obj['AdmissionYears']:
            admission_years.append(
                AdmissionYear.de_json(sub_obj)
            )
        return cls(name, name_english, admission_years)

    def __init__(self, name, name_english, admission_years):
        """

        :type name: str
        :type name_english: str
        :type admission_years: list of AdmissionYear
        """
        self.name = name
        self.name_english = name_english
        self.admission_years = admission_years


class AdmissionYear(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        study_program_id = obj['StudyProgramId']
        year_name = obj['YearName']
        year_number = obj['YearNumber']
        is_empty = obj['IsEmpty']
        public_division_alias = obj['PublicDivisionAlias']
        return cls(study_program_id, year_name, year_number, is_empty,
                   public_division_alias)

    def __init__(self, study_program_id, year_name, year_number, is_empty,
                 public_division_alias):
        """

        :type study_program_id: int
        :type year_name: str
        :type year_number: int
        :type is_empty: bool
        :type public_division_alias: str
        """
        self.study_program_id = study_program_id
        self.year_name = year_name
        self.year_number = year_number
        self.is_empty = is_empty
        self.public_division_alias = public_division_alias


class Group(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        student_group_id = obj['StudentGroupId']
        student_group_name = obj['StudentGroupName']
        student_group_study_form = obj['StudentGroupStudyForm']
        student_group_profiles = obj['StudentGroupProfiles']
        public_division_alias = obj.get('PublicDivisionAlias')
        return cls(student_group_id, student_group_name,
                   student_group_study_form, student_group_profiles,
                   public_division_alias)

    def __init__(self, student_group_id, student_group_name,
                 student_group_study_form, student_group_profiles,
                 public_division_alias):
        """

        :type student_group_id: int
        :type student_group_name: str
        :type student_group_study_form: str
        :type student_group_profiles: str
        :type public_division_alias: str
        """
        self.student_group_id = student_group_id
        self.student_group_name = student_group_name
        self.student_group_study_form = student_group_study_form
        self.student_group_profiles = student_group_profiles
        self.public_division_alias = public_division_alias


class Events(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        student_group_id = obj["StudentGroupId"]
        student_group_display_name = obj["StudentGroupDisplayName"]
        timetable_display_name = obj["TimeTableDisplayName"]
        previous_week_monday = None
        if obj["PreviousWeekMonday"]:
            previous_week_monday = datetime.strptime(
                obj["PreviousWeekMonday"], "%Y-%m-%d"
            ).date()
        next_week_monday = None
        if obj["NextWeekMonday"]:
            next_week_monday = datetime.strptime(
                obj["NextWeekMonday"], "%Y-%m-%d"
            ).date()
        is_previous_week_reference_available = obj[
            "IsPreviousWeekReferenceAvailable"
        ]
        is_next_week_reference_available = obj["IsNextWeekReferenceAvailable"]
        is_current_week_reference_available = obj[
            "IsCurrentWeekReferenceAvailable"
        ]
        week_display_text = obj["WeekDisplayText"]
        week_monday = None
        if obj["WeekMonday"]:
            week_monday = datetime.strptime(
                obj["WeekMonday"], "%Y-%m-%d"
            ).date()
        days = []
        for sub_obj in obj["Days"]:
            days.append(Day.de_json(sub_obj))
        return cls(student_group_id, student_group_display_name,
                   timetable_display_name, previous_week_monday,
                   next_week_monday, is_previous_week_reference_available,
                   is_next_week_reference_available,
                   is_current_week_reference_available, week_display_text,
                   week_monday, days)

    def __init__(self, student_group_id, student_group_display_name,
                 timetable_display_name, previous_week_monday,
                 next_week_monday, is_previous_week_reference_available,
                 is_next_week_reference_available,
                 is_current_week_reference_available, week_display_text,
                 week_monday, days):
        """

        :type student_group_id: int
        :type student_group_display_name: str
        :type timetable_display_name: str
        :type previous_week_monday: date | None
        :type next_week_monday: date | None
        :type is_previous_week_reference_available: bool
        :type is_next_week_reference_available: bool
        :type is_current_week_reference_available: bool
        :type week_display_text: str
        :type week_monday: date | None
        :type days: list of Day
        """
        self.student_group_id = student_group_id
        self.student_group_display_name = student_group_display_name
        self.timetable_display_name = timetable_display_name
        self.previous_week_monday = previous_week_monday
        self.next_week_monday = next_week_monday
        self.is_previous_week_reference_available = \
            is_previous_week_reference_available
        self.is_next_week_reference_available = is_next_week_reference_available
        self.is_current_week_reference_available = \
            is_current_week_reference_available
        self.week_display_text = week_display_text
        self.week_monday = week_monday
        self.days = days


class Day(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        day = datetime.strptime(obj["Day"], "%Y-%m-%dT%H:%M:%S")
        day_string = obj["DayString"]
        day_study_events = []
        for sub_obj in obj["DayStudyEvents"]:
            day_study_events.append(DayStudyEvent.de_json(sub_obj))
        return cls(day, day_string, day_study_events)

    def __init__(self, day, day_string, day_study_events):
        """

        :type day: datetime
        :type day_string: str
        :type day_study_events: list of DayStudyEvent
        """
        self.day = day
        self.day_string = day_string
        self.day_study_events = day_study_events


class DayStudyEvent(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        study_events_timetable_kind_code = obj["StudyEventsTimeTableKindCode"]
        start = datetime.strptime(obj["Start"], "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(obj["End"], "%Y-%m-%dT%H:%M:%S")
        subject = obj["Subject"]
        time_interval_string = obj["TimeIntervalString"]
        date_with_time_interval_string = obj["DateWithTimeIntervalString"]
        display_date_and_time_interval_string = obj[
            "DisplayDateAndTimeIntervalString"
        ]
        locations_display_text = obj["LocationsDisplayText"]
        educators_display_text = obj["EducatorsDisplayText"]
        has_educators = obj["HasEducators"]
        is_cancelled = obj["IsCancelled"]
        contingent_unit_name = obj["ContingentUnitName"]
        division_and_course = obj["DivisionAndCourse"]
        is_assigned = obj["IsAssigned"]
        time_was_changed = obj["TimeWasChanged"]
        locations_were_changed = obj["LocationsWereChanged"]
        educators_were_reassigned = obj["EducatorsWereReassigned"]
        elective_disciplines_count = obj["ElectiveDisciplinesCount"]
        is_elective = obj["IsElective"]
        has_the_same_time_as_previous_item = obj["HasTheSameTimeAsPreviousItem"]
        contingent_units_display_test = obj["ContingentUnitsDisplayTest"]
        is_study = obj["IsStudy"]
        all_day = obj["AllDay"]
        within_the_same_day = obj["WithinTheSameDay"]
        event_locations = []
        for sub_obj in obj["EventLocations"]:
            event_locations.append(EventLocation.de_json(sub_obj))
        educator_ids = []
        for sub_obj in obj["EducatorIds"]:
            educator_ids.append(EducatorId.de_json(sub_obj))
        return cls(study_events_timetable_kind_code, start, end, subject,
                   time_interval_string, date_with_time_interval_string,
                   display_date_and_time_interval_string,
                   locations_display_text, educators_display_text,
                   has_educators, is_cancelled, contingent_unit_name,
                   division_and_course, is_assigned, time_was_changed,
                   locations_were_changed, educators_were_reassigned,
                   elective_disciplines_count, is_elective,
                   has_the_same_time_as_previous_item,
                   contingent_units_display_test, is_study, all_day,
                   within_the_same_day, event_locations, educator_ids)

    def __init__(self, study_events_timetable_kind_code, start, end, subject,
                 time_interval_string, date_with_time_interval_string,
                 display_date_and_time_interval_string, locations_display_text,
                 educators_display_text, has_educators, is_cancelled,
                 contingent_unit_name, division_and_course, is_assigned,
                 time_was_changed, locations_were_changed,
                 educators_were_reassigned, elective_disciplines_count,
                 is_elective, has_the_same_time_as_previous_item,
                 contingent_units_display_test, is_study, all_day,
                 within_the_same_day, event_locations, educator_ids):
        """

        :type study_events_timetable_kind_code: int
        :type start: datetime
        :type end: datetime
        :type subject: str
        :type time_interval_string: str
        :type date_with_time_interval_string: str
        :type display_date_and_time_interval_string: str
        :type locations_display_text: str
        :type educators_display_text: str
        :type has_educators: bool
        :type is_cancelled: bool
        :type contingent_unit_name: str
        :type division_and_course: str
        :type is_assigned: bool
        :type time_was_changed: bool
        :type locations_were_changed: bool
        :type educators_were_reassigned: bool
        :type elective_disciplines_count: int
        :type is_elective: bool
        :type has_the_same_time_as_previous_item: bool
        :type contingent_units_display_test:
        :type is_study: bool
        :type all_day: bool
        :type within_the_same_day: bool
        :type event_locations: list of EventLocations
        :type educator_ids: list of EducatorId
        """
        self.study_events_timetable_kind_code = study_events_timetable_kind_code
        self.start = start
        self.end = end
        self.subject = subject
        self.time_interval_string = time_interval_string
        self.date_with_time_interval_string = date_with_time_interval_string
        self.display_date_and_time_interval_string = \
            display_date_and_time_interval_string
        self.locations_display_text = locations_display_text
        self.educators_display_text = educators_display_text
        self.has_educators = has_educators
        self.is_cancelled = is_cancelled
        self.contingent_unit_name = contingent_unit_name
        self.division_and_course = division_and_course
        self.is_assigned = is_assigned
        self.time_was_changed = time_was_changed
        self.locations_were_changed = locations_were_changed
        self.educators_were_reassigned = educators_were_reassigned
        self.elective_disciplines_count = elective_disciplines_count
        self.is_elective = is_elective
        self.has_the_same_time_as_previous_item = \
            has_the_same_time_as_previous_item
        self.contingent_units_display_test = contingent_units_display_test
        self.is_study = is_study
        self.all_day = all_day
        self.within_the_same_day = within_the_same_day
        self.event_locations = event_locations
        self.educator_ids = educator_ids


class EventLocation(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        is_empty = obj["IsEmpty"]
        display_name = obj["DisplayName"]
        has_geographic_coordinates = obj["HasGeographicCoordinates"]
        latitude = obj["Latitude"]
        longitude = obj["Longitude"]
        latitude_value = obj["LatitudeValue"]
        longitude_value = obj["LongitudeValue"]
        educators_display_text = obj["EducatorsDisplayText"]
        has_educators = obj["HasEducators"]
        educator_ids = []
        for sub_obj in obj["EducatorIds"]:
            educator_ids.append(EducatorId.de_json(sub_obj))
        return cls(is_empty, display_name, has_geographic_coordinates, latitude,
                   longitude, latitude_value, longitude_value,
                   educators_display_text, has_educators, educator_ids)

    def __init__(self, is_empty, display_name, has_geographic_coordinates,
                 latitude, longitude, latitude_value, longitude_value,
                 educators_display_text, has_educators, educator_ids):
        """

        :type is_empty: bool
        :type display_name: str
        :type has_geographic_coordinates: bool
        :type latitude: float
        :type longitude: float
        :type latitude_value: str
        :type longitude_value: str
        :type educators_display_text: str
        :type has_educators: bool
        :type educator_ids: list of EducatorId
        """
        self.is_empty = is_empty
        self.display_name = display_name
        self.has_geographic_coordinates = has_geographic_coordinates
        self.latitude = latitude
        self.longitude = longitude
        self.latitude_value = latitude_value
        self.longitude_value = longitude_value
        self.educators_display_text = educators_display_text
        self.has_educators = has_educators
        self.educator_ids = educator_ids


class EducatorId(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        item1 = obj["Item1"]
        item2 = obj["Item2"]
        return cls(item1, item2)

    def __init__(self, item1, item2):
        """
        This class has the same property names as in the documentation
        :param item1: id.
        :type item1: int
        :param item2: name.
        :type item2: str
        """
        self.item1 = item1
        self.item2 = item2


class ExtracurDivision(_JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        alias = obj["Alias"]
        name = obj["Name"]
        return cls(alias, name)

    def __init__(self, alias, name):
        """

        :type alias: str
        :type name: str
        """
        self.alias = alias
        self.name = name


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the SPbU TimeTable
    API fails.
    In addition to an informative message, it has a `function_name` and a
    `result` attribute, which respectively contain the name of the failed
    function and the returned result that made the function to be considered
    as failed.
    """
    def __init__(self, msg, function_name, result):
        """
        :param msg: error message
        :type msg: str
        :param function_name: The name of function which raise the exception
        :type function_name: str
        :param result: request response
        :type result: models.Response
        """
        super(ApiException, self).__init__(error_msg.format(msg))
        self.function_name = function_name
        self.result = result
