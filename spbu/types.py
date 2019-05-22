import abc
import json
from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import TypeVar, Optional, List

from requests import models

from spbu.consts import error_msg

JSON_TYPE = TypeVar('JSON_TYPE', dict, str)


class _JsonDeserializable(abc.ABC):
    """
    Subclasses of this class are guaranteed to be able to be created from a
    json-style dict or json formatted string.
    All subclasses of this class must override de_json.
    """

    @classmethod
    @abc.abstractmethod
    def de_json(cls, json_type: JSON_TYPE) -> '_JsonDeserializable':
        ...

    @staticmethod
    def check_json(json_type: JSON_TYPE) -> dict:
        """
        Checks whether json_type is a dict or a string. If it is already a dict,
        it is returned as-is.
        If it is not, it is converted to a dict by means of
        json.loads(json_type)
        :param json_type:
        :type json_type: dict or str
        :return:
        """
        if isinstance(json_type, dict):
            return json_type
        elif isinstance(json_type, str):
            return json.loads(json_type)
        else:
            raise ValueError("json_type should be a json dict or string.")


@dataclass
class SDStudyDivision(_JsonDeserializable):
    oid: Optional[str]
    alias: Optional[str]
    name: Optional[str]

    @classmethod
    def de_json(cls, json_string: JSON_TYPE) -> 'SDStudyDivision':
        obj = cls.check_json(json_string)
        return cls(
            oid=obj.get('Oid'),
            alias=obj.get('Alias'),
            name=obj.get('Name')
        )


@dataclass
class SDPLAdmissionYear(_JsonDeserializable):
    study_program_id: Optional[int]
    year_name: Optional[str]
    year_number: Optional[int]
    public_division_alias: Optional[str]
    is_empty: bool = True

    @classmethod
    def de_json(cls, json_string: JSON_TYPE) -> 'SDPLAdmissionYear':
        obj = cls.check_json(json_string)
        return cls(
            study_program_id=obj.get('StudyProgramId'),
            year_name=obj.get('YearName'),
            year_number=obj.get('YearNumber'),
            public_division_alias=obj.get('PublicDivisionAlias'),
            is_empty=obj.get('IsEmpty', True),
        )


@dataclass
class SDPLProgramCombination(_JsonDeserializable):
    name: Optional[str]
    name_english: Optional[str]
    admission_years: List[SDPLAdmissionYear] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_string: JSON_TYPE) -> 'SDPLProgramCombination':
        obj = cls.check_json(json_string)
        return cls(
            name=obj.get('Name'),
            name_english=obj.get('NameEnglish'),
            admission_years=[
                SDPLAdmissionYear.de_json(sub_obj)
                for sub_obj in obj.get('AdmissionYears', [])
            ]
        )


@dataclass
class SDPLStudyLevel(_JsonDeserializable):
    study_level_name: Optional[str]
    study_level_name_english: Optional[str]
    has_course6: bool = False
    study_program_combinations: List[SDPLProgramCombination] = field(
        default_factory=list
    )

    @classmethod
    def de_json(cls, json_string: JSON_TYPE) -> 'SDPLStudyLevel':
        obj = cls.check_json(json_string)
        return cls(
            study_level_name=obj.get('StudyLevelName'),
            study_level_name_english=obj.get('StudyLevelNameEnglish'),
            has_course6=obj.get('HasCourse6', False),
            study_program_combinations=[
                SDPLProgramCombination.de_json(sub_obj)
                for sub_obj in obj.get('StudyProgramCombinations', [])
            ]
        )


@dataclass
class PGGroup(_JsonDeserializable):
    student_group_id: Optional[int]
    student_group_name: Optional[str]
    student_group_study_form: Optional[str]
    student_group_profiles: Optional[str]
    public_division_alias: Optional[str]

    @classmethod
    def de_json(cls, json_string: JSON_TYPE) -> 'PGGroup':
        obj = cls.check_json(json_string)
        return cls(
            student_group_id=obj.get('StudentGroupId'),
            student_group_name=obj.get('StudentGroupName'),
            student_group_study_form=obj.get('StudentGroupStudyForm'),
            student_group_profiles=obj.get('StudentGroupProfiles'),
            public_division_alias=obj.get('PublicDivisionAlias')
        )


@dataclass
class EducatorId(_JsonDeserializable):
    eid: Optional[int]
    name: Optional[str]

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EducatorId':
        obj = cls.check_json(json_type)
        return cls(
            eid=obj.get('Item1'),
            name=obj.get('Item2')
        )


@dataclass
class EventLocation(_JsonDeserializable):
    display_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    latitude_value: Optional[str]
    longitude_value: Optional[str]
    educators_display_text: Optional[str]
    is_empty: bool = True
    has_geographic_coordinates: bool = False
    has_educators: bool = False
    educator_ids: List[EducatorId] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EventLocation':
        obj = cls.check_json(json_type)
        return cls(
            is_empty=obj.get("IsEmpty", True),
            display_name=obj.get("DisplayName"),
            has_geographic_coordinates=obj.get(
                "HasGeographicCoordinates", False
            ),
            latitude=obj.get("Latitude"),
            longitude=obj.get("Longitude"),
            latitude_value=obj.get("LatitudeValue"),
            longitude_value=obj.get("LongitudeValue"),
            educators_display_text=obj.get("EducatorsDisplayText"),
            has_educators=obj.get("HasEducators", False),
            educator_ids=[
                EducatorId.de_json(sub_obj)
                for sub_obj in obj.get("EducatorIds", [])
            ]
        )


@dataclass
class GEEvent(_JsonDeserializable):
    study_events_timetable_kind_code: Optional[int]
    start: Optional[datetime]
    end: Optional[datetime]
    subject: Optional[str]
    time_interval_string: Optional[str]
    date_with_time_interval_string: Optional[str]
    display_date_and_time_interval_string: Optional[str]
    locations_display_text: Optional[str]
    educators_display_text: Optional[str]
    contingent_unit_name: Optional[str]
    division_and_course: Optional[str]
    elective_disciplines_count: Optional[int]
    contingent_units_display_test: Optional[str]
    has_educators: bool = False
    is_cancelled: bool = False
    is_assigned: bool = False
    time_was_changed: bool = False
    locations_were_changed: bool = False
    educators_were_reassigned: bool = False
    is_elective: bool = False
    has_the_same_time_as_previous_item: bool = False
    is_study: bool = False
    all_day: bool = False
    within_the_same_day: bool = False
    event_locations: List[EventLocation] = field(default_factory=list)
    educator_ids: List[EducatorId] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'GEEvent':
        obj = cls.check_json(json_type)
        start = obj.get("Start")
        if start:
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        end = obj.get("End")
        if end:
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        return cls(
            study_events_timetable_kind_code=obj.get(
                "StudyEventsTimeTableKindCode"
            ),
            start=start,
            end=end,
            subject=obj.get("Subject"),
            time_interval_string=obj.get("TimeIntervalString"),
            date_with_time_interval_string=obj.get(
                "DateWithTimeIntervalString"
            ),
            display_date_and_time_interval_string=obj.get(
                "DisplayDateAndTimeIntervalString"
            ),
            locations_display_text=obj.get("LocationsDisplayText"),
            educators_display_text=obj.get("EducatorsDisplayText"),
            has_educators=obj.get("HasEducators", False),
            is_cancelled=obj.get("IsCancelled", False),
            contingent_unit_name=obj.get("ContingentUnitName"),
            division_and_course=obj.get("DivisionAndCourse"),
            is_assigned=obj.get("IsAssigned", False),
            time_was_changed=obj.get("TimeWasChanged", False),
            locations_were_changed=obj.get("LocationsWereChanged", False),
            educators_were_reassigned=obj.get("EducatorsWereReassigned", False),
            elective_disciplines_count=obj.get("ElectiveDisciplinesCount"),
            is_elective=obj.get("IsElective", False),
            has_the_same_time_as_previous_item=obj.get(
                "HasTheSameTimeAsPreviousItem", False
            ),
            contingent_units_display_test=obj.get("ContingentUnitsDisplayTest"),
            is_study=obj.get("IsStudy", False),
            all_day=obj.get("AllDay", False),
            within_the_same_day=obj.get("WithinTheSameDay", False),
            event_locations=[
                EventLocation.de_json(sub_obj)
                for sub_obj in obj.get("EventLocations", [])
            ],
            educator_ids=[
                EducatorId.de_json(sub_obj)
                for sub_obj in obj.get("EducatorIds", [])
            ]
        )


@dataclass
class GEEventsDay(_JsonDeserializable):
    day: Optional[date]
    day_string: Optional[str]
    day_study_events: List[GEEvent] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'GEEventsDay':
        obj = cls.check_json(json_type)
        day = obj.get("Day")
        if day:
            day = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S").date()
        return cls(
            day=day,
            day_string=obj.get("DayString"),
            day_study_events=[
                GEEvent.de_json(sub_obj)
                for sub_obj in obj.get("DayStudyEvents")
            ]
        )


@dataclass
class GroupEvents(_JsonDeserializable):
    student_group_id: Optional[int]
    student_group_display_name: Optional[str]
    timetable_display_name: Optional[str]
    previous_week_monday: Optional[date]
    next_week_monday: Optional[date]
    week_display_text: Optional[str]
    week_monday: Optional[date]
    is_previous_week_reference_available: bool = False
    is_next_week_reference_available: bool = False
    is_current_week_reference_available: bool = False
    days: List[GEEventsDay] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'GroupEvents':
        obj = cls.check_json(json_type)
        previous_week_monday = obj.get("PreviousWeekMonday")
        if previous_week_monday:
            previous_week_monday = datetime.strptime(
                previous_week_monday, "%Y-%m-%d"
            ).date()
        next_week_monday = obj.get("NextWeekMonday")
        if next_week_monday:
            next_week_monday = datetime.strptime(
                next_week_monday, "%Y-%m-%d"
            ).date()
        week_monday = obj.get("WeekMonday")
        if week_monday:
            week_monday = datetime.strptime(
                week_monday, "%Y-%m-%d"
            ).date()
        return cls(
            student_group_id=obj.get("StudentGroupId"),
            student_group_display_name=obj.get("StudentGroupDisplayName"),
            timetable_display_name=obj.get("TimeTableDisplayName"),
            is_previous_week_reference_available=obj.get(
                "IsPreviousWeekReferenceAvailable"
            ),
            is_next_week_reference_available=obj.get(
                "IsNextWeekReferenceAvailable"
            ),
            is_current_week_reference_available=obj.get(
                "IsCurrentWeekReferenceAvailable"
            ),
            week_display_text=obj.get("WeekDisplayText"),
            days=[GEEventsDay.de_json(_obj) for _obj in obj.get("Days", [])],
            previous_week_monday=previous_week_monday,
            next_week_monday=next_week_monday,
            week_monday=week_monday
        )


@dataclass
class ExtracurDivision(_JsonDeserializable):
    alias: Optional[str]
    name: Optional[str]

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'ExtracurDivision':
        obj = cls.check_json(json_type)
        return cls(
            alias=obj.get("Alias"),
            name=obj.get("Name")
        )


@dataclass
class AddressLocation(_JsonDeserializable):
    is_empty: Optional[bool]
    display_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    latitude_value: Optional[str]
    longitude_value: Optional[str]
    has_geographic_coordinates: Optional[bool] = False

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'AddressLocation':
        obj = cls.check_json(json_type)
        return cls(
            is_empty=obj.get("IsEmpty"),
            display_name=obj.get("DisplayName"),
            has_geographic_coordinates=obj.get(
                "HasGeographicCoordinates", False
            ),
            latitude=obj.get("Latitude"),
            longitude=obj.get("Longitude"),
            latitude_value=obj.get("LatitudeValue"),
            longitude_value=obj.get("LongitudeValue")
        )


@dataclass
class ExEEventsDay(_JsonDeserializable):
    day: Optional[date]
    day_string: Optional[str]
    day_events: List[ExtracurEvent] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'ExEEventsDay':
        obj = cls.check_json(json_type)
        day = obj.get("Day")
        if day:
            day = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S").date()
        return cls(
            day=day,
            day_string=obj.get("DayString"),
            day_events=[
                ExtracurEvent.de_json(_obj)
                for _obj in obj.get("DayEvents", [])
            ]
        )


@dataclass
class ExtracurEvent(_JsonDeserializable):
    id: Optional[int]
    start: Optional[datetime]
    end: Optional[datetime]
    subject: Optional[str]
    time_interval_string: Optional[str]
    date_with_time_interval_string: Optional[str]
    locations_display_text: Optional[str]
    educators_display_text: Optional[str]
    contingent_units_display_test: Optional[str]
    display_date_and_time_interval_string: Optional[str]
    view_kind: Optional[int]
    division_alias: Optional[str]
    recurrence_index: Optional[int]
    full_date_with_time_interval_string: Optional[str]
    year: Optional[int]
    subkind_display_name: Optional[str]
    order_index: Optional[int]
    location: Optional[AddressLocation]
    from_date: Optional[date]
    from_date_string: Optional[str]
    responsible_person_contacts: Optional[str]
    has_educators: bool = False
    is_cancelled: bool = False
    has_the_same_time_as_previous_item: bool = False
    all_day: bool = False
    within_the_same_day: bool = False
    show_year: bool = False
    show_immediate: bool = False
    is_show_immediate_hidden: bool = False
    has_agenda: bool = False
    is_recurrence: bool = False
    is_empty: bool = True
    is_phys: bool = False
    is_study: bool = False

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'ExtracurEvent':
        obj = cls.check_json(json_type)
        start = obj.get("Start")
        if start:
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        end = obj.get("End")
        if end:
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        from_date = obj.get("FromDate")
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%S").date()
        location = obj.get("Location")
        if location:
            location = AddressLocation.de_json(location)
        return cls(
            id=obj.get("Id"),
            start=start,
            end=end,
            subject=obj.get("Subject"),
            time_interval_string=obj.get("TimeIntervalString"),
            date_with_time_interval_string=obj.get(
                "DateWithTimeIntervalString"
            ),
            locations_display_text=obj.get("LocationsDisplayText"),
            educators_display_text=obj.get("EducatorsDisplayText"),
            contingent_units_display_test=obj.get("ContingentUnitsDisplayTest"),
            display_date_and_time_interval_string=obj.get(
                "DisplayDateAndTimeIntervalString"
            ),
            view_kind=obj.get("ViewKind"),
            division_alias=obj.get("DivisionAlias"),
            recurrence_index=obj.get("RecurrenceIndex"),
            full_date_with_time_interval_string=obj.get(
                "FullDateWithTimeIntervalString"
            ),
            year=obj.get("Year"),
            subkind_display_name=obj.get("SubkindDisplayName"),
            order_index=obj.get("OrderIndex"),
            location=location,
            from_date=from_date,
            from_date_string=obj.get("FromDateString"),
            responsible_person_contacts=obj.get("ResponsiblePersonContacts"),
            has_educators=obj.get("HasEducators", False),
            is_cancelled=obj.get("IsCancelled", False),
            has_the_same_time_as_previous_item=obj.get(
                "HasTheSameTimeAsPreviousItem", False
            ),
            all_day=obj.get("AllDay", False),
            within_the_same_day=obj.get("WithinTheSameDay", False),
            show_year=obj.get("ShowYear", False),
            show_immediate=obj.get("ShowImmediate", False),
            is_show_immediate_hidden=obj.get("IsShowImmediateHidden", False),
            has_agenda=obj.get("HasAgenda", False),
            is_recurrence=obj.get("IsRecurrence", False),
            is_empty=obj.get("IsEmpty", True),
            is_phys=obj.get("IsPhys", False),
            is_study=obj.get("IsStudy", False)
        )


@dataclass
class ExEEventsByKind(_JsonDeserializable):
    caption: Optional[str]
    events: List[ExtracurEvent] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'ExEEventsByKind':
        obj = cls.check_json(json_type)
        return cls(
            caption=obj.get("Caption"),
            events=[
                ExtracurEvent.de_json(_obj)
                for _obj in obj.get("Events", [])
            ]
        )


@dataclass
class ExtracurEvents(_JsonDeserializable):
    alias: Optional[str]
    title: Optional[str]
    chosen_month_display_text: Optional[str]
    previous_month_display_text: Optional[str]
    previous_month_date: Optional[date]
    next_month_display_text: Optional[str]
    next_month_date: Optional[date]
    previous_week_monday: Optional[date]
    next_week_monday: Optional[date]
    week_display_text: Optional[str]
    week_monday: Optional[date]
    has_events_to_show: bool = False
    is_current_month_reference_available: bool = False
    show_grouping_captions: bool = False
    is_previous_week_reference_available: bool = False
    is_next_week_reference_available: bool = False
    is_current_week_reference_available: bool = False
    event_groupings: List[ExEEventsByKind] = field(default_factory=list)
    earlier_events: List[ExtracurEvent] = field(default_factory=list)
    days: List[ExEEventsDay] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'ExtracurEvents':
        obj = cls.check_json(json_type)
        previous_month_date = obj.get("PreviousMonthDate")
        if previous_month_date:
            previous_month_date = datetime.strptime(
                previous_month_date, "%Y-%m-%d"
            ).date()
        next_month_date = obj.get("NextMonthDate")
        if next_month_date:
            next_month_date = datetime.strptime(
                next_month_date, "%Y-%m-%d"
            ).date()
        previous_week_monday = obj.get("PreviousWeekMonday")
        if previous_week_monday:
            previous_week_monday = datetime.strptime(
                previous_week_monday, "%Y-%m-%d"
            ).date()
        next_week_monday = obj.get("NextWeekMonday")
        if next_week_monday:
            next_week_monday = datetime.strptime(
                next_week_monday, "%Y-%m-%d"
            ).date()
        week_monday = obj.get("WeekMonday")
        if week_monday:
            week_monday = datetime.strptime(
                week_monday, "%Y-%m-%d"
            ).date()
        return cls(
            alias=obj.get("Alias"),
            title=obj.get("Title"),
            chosen_month_display_text=obj.get("ChosenMonthDisplayText"),
            previous_month_display_text=obj.get("PreviousMonthDisplayText"),
            previous_month_date=previous_month_date,
            next_month_display_text=obj.get("NextMonthDisplayText"),
            next_month_date=next_month_date,
            previous_week_monday=previous_week_monday,
            next_week_monday=next_week_monday,
            week_display_text=obj.get("WeekDisplayText"),
            week_monday=week_monday,
            has_events_to_show=obj.get("HasEventsToShow", False),
            is_current_month_reference_available=obj.get(
                "IsCurrentMonthReferenceAvailable", False
            ),
            show_grouping_captions=obj.get("ShowGroupingCaptions", False),
            is_previous_week_reference_available=obj.get(
                "IsPreviousWeekReferenceAvailable", False
            ),
            is_next_week_reference_available=obj.get(
                "IsNextWeekReferenceAvailable", False
            ),
            is_current_week_reference_available=obj.get(
                "IsCurrentWeekReferenceAvailable", False
            ),
            event_groupings=[
                ExEEventsByKind.de_json(_obj)
                for _obj in obj.get("EventGroupings", [])
            ],
            earlier_events=[
                ExtracurEvent.de_json(_obj)
                for _obj in obj.get("EarlierEvents", [])
            ],
            days=[
                ExEEventsDay.de_json(_obj)
                for _obj in obj.get("Days", [])
            ]
        )


@dataclass
class Educator(_JsonDeserializable):
    id: Optional[int]
    display_name: Optional[str]
    full_name: Optional[str]
    employments: List[EdEmployment] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'Educator':
        obj = cls.check_json(json_type)
        return cls(
            id=obj.get("Id"),
            display_name=obj.get("DisplayName"),
            full_name=obj.get("FullName"),
            employments=[
                EdEmployment.de_json(_obj)
                for _obj in obj.get("Employments", [])
            ]
        )


@dataclass
class EdEmployment(_JsonDeserializable):
    position: Optional[str]
    department: Optional[str]

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EdEmployment':
        obj = cls.check_json(json_type)
        return cls(
            position=obj.get("Position"),
            department=obj.get("Department")
        )


@dataclass
class ContingentUnitName(_JsonDeserializable):
    groups: Optional[str]
    courses: Optional[str]

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'ContingentUnitName':
        obj = cls.check_json(json_type)
        return cls(
            groups=obj.get("Item1"),
            courses=obj.get("Item2")
        )


@dataclass
class EdETEvent(_JsonDeserializable):
    start: Optional[time]
    end: Optional[time]
    subject: Optional[str]
    time_interval_string: Optional[str]
    educators_display_text: Optional[str]
    study_events_time_table_kind_code: Optional[int]
    is_canceled: bool = False
    dates: List[str] = field(default_factory=list)
    educator_ids: List[EducatorId] = field(default_factory=list)
    event_locations: List[EventLocation] = field(default_factory=list)
    contingent_unit_names: List[ContingentUnitName] = field(
        default_factory=list
    )

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EdETEvent':
        obj = cls.check_json(json_type)
        start = obj.get("Start")
        if start:
            start = datetime.strptime(
                start, "%H:%M:%S"
            ).time()
        end = obj.get("End")
        if end:
            end = datetime.strptime(
                end, "%H:%M:%S"
            ).time()
        return cls(
            start=start,
            end=end,
            subject=obj.get("Subject"),
            time_interval_string=obj.get("TimeIntervalString"),
            educators_display_text=obj.get("EducatorsDisplayText"),
            study_events_time_table_kind_code=obj.get(
                "StudyEventsTimeTableKindCode"
            ),
            is_canceled=obj.get("IsCanceled", False),
            dates=obj.get("Dates", []),
            educator_ids=[
                EducatorId.de_json(_obj)
                for _obj in obj.get("EducatorIds", [])
            ],
            event_locations=[
                EventLocation.de_json(_obj)
                for _obj in obj.get("EventLocations", [])
            ],
            contingent_unit_names=[
                ContingentUnitName.de_json(_obj)
                for _obj in obj.get("ContingentUnitNames", [])
            ]
        )


@dataclass
class EdETEventsDay(_JsonDeserializable):
    day: Optional[int]
    day_string: Optional[str]
    day_study_events_count: Optional[int]
    day_study_events: List[EdETEvent] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EdETEventsDay':
        obj = cls.check_json(json_type)
        return cls(
            day=obj.get("Day"),
            day_string=obj.get("DayString"),
            day_study_events_count=obj.get("DayStudyEventsCount"),
            day_study_events=[
                EdETEvent.de_json(_obj)
                for _obj in obj.get("DayStudyEvents", [])
            ]
        )


@dataclass
class EducatorEventsTerm(_JsonDeserializable):
    title: Optional[str]
    educator_display_text: Optional[str]
    educator_long_display_text: Optional[str]
    date_range_display_text: Optional[str]
    educator_master_id: Optional[int]
    from_date: Optional[date]
    to_date: Optional[date]
    next: Optional[int]
    is_spring_term: bool = False
    spring_term_link_available: bool = False
    autumn_term_link_available: bool = False
    has_events: bool = False
    educator_events_days: List[EdETEventsDay] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EducatorEventsTerm':
        obj = cls.check_json(json_type)
        from_date = obj.get("From")
        if from_date:
            from_date = datetime.strptime(
                from_date, "%Y-%m-%dT%H:%M:%S"
            ).date()
        to_date = obj.get("From")
        if to_date:
            to_date = datetime.strptime(
                to_date, "%Y-%m-%dT%H:%M:%S"
            ).date()
        return cls(
            title=obj.get("Title"),
            educator_display_text=obj.get("EducatorDisplayText"),
            educator_long_display_text=obj.get("EducatorLongDisplayText"),
            date_range_display_text=obj.get("DateRangeDisplayText"),
            educator_master_id=obj.get("EducatorMasterId"),
            from_date=from_date,
            to_date=to_date,
            next=obj.get("Next"),
            is_spring_term=obj.get("IsSpringTerm", False),
            spring_term_link_available=obj.get(
                "SpringTermLinkAvailable", False
            ),
            autumn_term_link_available=obj.get(
                "AutumnTermLinkAvailable", False
            ),
            has_events=obj.get("HasEvents"),
            educator_events_days=[
                EdETEventsDay.de_json(_obj)
                for _obj in obj.get("EducatorEventsDays", [])
            ]
        )


@dataclass
class EdEEvent(_JsonDeserializable):
    study_events_timetable_kind_code: Optional[int]
    start: Optional[datetime]
    end: Optional[datetime]
    subject: Optional[str]
    time_interval_string: Optional[str]
    date_with_time_interval_string: Optional[str]
    display_date_and_time_interval_string: Optional[str]
    locations_display_text: Optional[str]
    educators_display_text: Optional[str]
    contingent_unit_name: Optional[str]
    division_and_course: Optional[str]
    elective_disciplines_count: Optional[int]
    has_educators: bool = False
    is_cancelled: bool = False
    is_assigned: bool = False
    time_was_changed: bool = False
    locations_were_changed: bool = False
    educators_were_reassigned: bool = False
    is_elective: bool = False
    has_the_same_time_as_previous_item: bool = False
    is_study: bool = False
    all_day: bool = False
    within_the_same_day: bool = False
    event_locations: List[EventLocation] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EdEEvent':
        obj = cls.check_json(json_type)
        start = obj.get("Start")
        if start:
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        end = obj.get("End")
        if end:
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        return cls(
            study_events_timetable_kind_code=obj.get(
                "StudyEventsTimeTableKindCode"
            ),
            start=start,
            end=end,
            subject=obj.get("Subject"),
            time_interval_string=obj.get("TimeIntervalString"),
            date_with_time_interval_string=obj.get(
                "DateWithTimeIntervalString"
            ),
            display_date_and_time_interval_string=obj.get(
                "DisplayDateAndTimeIntervalString"
            ),
            locations_display_text=obj.get("LocationsDisplayText"),
            educators_display_text=obj.get("EducatorsDisplayText"),
            has_educators=obj.get("HasEducators", False),
            is_cancelled=obj.get("IsCancelled", False),
            contingent_unit_name=obj.get("ContingentUnitName"),
            division_and_course=obj.get("DivisionAndCourse"),
            is_assigned=obj.get("IsAssigned", False),
            time_was_changed=obj.get("TimeWasChanged", False),
            locations_were_changed=obj.get("LocationsWereChanged", False),
            educators_were_reassigned=obj.get("EducatorsWereReassigned", False),
            elective_disciplines_count=obj.get("ElectiveDisciplinesCount"),
            is_elective=obj.get("IsElective", False),
            has_the_same_time_as_previous_item=obj.get(
                "HasTheSameTimeAsPreviousItem", False
            ),
            is_study=obj.get("IsStudy", False),
            all_day=obj.get("AllDay", False),
            within_the_same_day=obj.get("WithinTheSameDay", False),
            event_locations=[
                EventLocation.de_json(sub_obj)
                for sub_obj in obj.get("EventLocations", [])
            ]
        )


@dataclass
class EdEEventsDay(_JsonDeserializable):
    day: Optional[date]
    day_string: Optional[str]
    day_study_events: List[EdEEvent] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EdEEventsDay':
        obj = cls.check_json(json_type)
        day = obj.get("Day")
        if day:
            day = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S").date()
        return cls(
            day=day,
            day_string=obj.get("DayString"),
            day_study_events=[
                EdEEvent.de_json(sub_obj)
                for sub_obj in obj.get("DayStudyEvents")
            ]
        )


@dataclass
class EducatorEvents(_JsonDeserializable):
    educator_master_id: Optional[int]
    educator_display_text: Optional[str]
    educator_long_display_text: Optional[str]
    previous_week_monday: Optional[date]
    next_week_monday: Optional[date]
    week_display_text: Optional[str]
    week_monday: Optional[date]
    is_previous_week_reference_available: bool = False
    is_next_week_reference_available: bool = False
    is_current_week_reference_available: bool = False
    educator_events_days: List[EdEEventsDay] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'EducatorEvents':
        obj = cls.check_json(json_type)
        previous_week_monday = obj.get("PreviousWeekMonday")
        if previous_week_monday:
            previous_week_monday = datetime.strptime(
                previous_week_monday, "%Y-%m-%d"
            ).date()
        next_week_monday = obj.get("NextWeekMonday")
        if next_week_monday:
            next_week_monday = datetime.strptime(
                next_week_monday, "%Y-%m-%d"
            ).date()
        week_monday = obj.get("WeekMonday")
        if week_monday:
            week_monday = datetime.strptime(
                week_monday, "%Y-%m-%d"
            ).date()
        return cls(
            educator_master_id=obj.get("EducatorMasterId"),
            educator_display_text=obj.get("EducatorDisplayText"),
            educator_long_display_text=obj.get("EducatorLongDisplayText"),
            previous_week_monday=previous_week_monday,
            next_week_monday=next_week_monday,
            week_display_text=obj.get("WeekDisplayText"),
            week_monday=week_monday,
            is_previous_week_reference_available=obj.get(
                "IsPreviousWeekReferenceAvailable", False
            ),
            is_next_week_reference_available=obj.get(
                "IsNextWeekReferenceAvailable", False
            ),
            is_current_week_reference_available=obj.get(
                "IsCurrentWeekReferenceAvailable", False
            ),
            educator_events_days=[
                EdEEventsDay.de_json(_obj)
                for _obj in obj.get("EducatorEventsDays", [])
            ]
        )


@dataclass
class ClassroomBusyness(_JsonDeserializable):
    oid: Optional[str]
    from_datetime: Optional[datetime]
    to_datetime: Optional[datetime]
    is_busy: bool = False

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'ClassroomBusyness':
        obj = cls.check_json(json_type)
        from_datetime = obj.get("From")
        if from_datetime:
            from_datetime = datetime.strptime(
                from_datetime, "%Y-%m-%dT%H:%M:%S"
            )
        to_datetime = obj.get("To")
        if to_datetime:
            to_datetime = datetime.strptime(
                to_datetime, "%Y-%m-%dT%H:%M:%S"
            )
        return cls(
            oid=obj.get("Oid"),
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            is_busy=obj.get("IsBusy", False)
        )


@dataclass
class CEEvent(_JsonDeserializable):
    start: Optional[time]
    end: Optional[time]
    subject: Optional[str]
    time_interval_string: Optional[str]
    educators_display_text: Optional[str]
    study_events_timetable_kind_code: Optional[int]
    is_cancelled: bool = False
    dates: List[str] = field(default_factory=list)
    educator_ids: List[EducatorId] = field(default_factory=list)
    contingent_unit_names: List[ContingentUnitName] = field(
        default_factory=list
    )

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'CEEvent':
        obj = cls.check_json(json_type)
        start = obj.get("Start")
        if start:
            start = datetime.strptime(start, "%H:%M:%S").time()
        end = obj.get("End")
        if end:
            end = datetime.strptime(end, "%H:%M:%S").time()
        return cls(
            study_events_timetable_kind_code=obj.get(
                "StudyEventsTimeTableKindCode"
            ),
            start=start,
            end=end,
            subject=obj.get("Subject"),
            time_interval_string=obj.get("TimeIntervalString"),
            educators_display_text=obj.get("EducatorsDisplayText"),
            is_cancelled=obj.get("IsCancelled", False),
            dates=obj.get("Dates", []),
            educator_ids=[
                EducatorId.de_json(sub_obj)
                for sub_obj in obj.get("EducatorIds", [])
            ],
            contingent_unit_names=[
                ContingentUnitName.de_json(_obj)
                for _obj in obj.get("ContingentUnitNames", [])
            ]
        )


@dataclass
class CEEventsDay(_JsonDeserializable):
    day: Optional[int]
    day_string: Optional[str]
    day_study_events_count: Optional[int]
    day_study_events: List[CEEvent] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'CEEventsDay':
        obj = cls.check_json(json_type)
        return cls(
            day=obj.get("Day"),
            day_string=obj.get("DayString"),
            day_study_events_count=obj.get("DayStudyEventsCount"),
            day_study_events=[
                CEEvent.de_json(_obj)
                for _obj in obj.get("DayStudyEvents", [])
            ]
        )


@dataclass
class ClassroomEvents(_JsonDeserializable):
    oid: Optional[str]
    from_datetime: Optional[datetime]
    to_datetime: Optional[datetime]
    display_text: Optional[str]
    has_events: bool = False
    classroom_events_days: List[CEEventsDay] = field(default_factory=list)

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'ClassroomEvents':
        obj = cls.check_json(json_type)
        from_datetime = obj.get("From")
        if from_datetime:
            from_datetime = datetime.strptime(
                from_datetime, "%Y-%m-%dT%H:%M:%S"
            )
        to_datetime = obj.get("To")
        if to_datetime:
            to_datetime = datetime.strptime(
                to_datetime, "%Y-%m-%dT%H:%M:%S"
            )
        return cls(
            oid=obj.get("Oid"),
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            display_text=obj.get("DisplayText"),
            has_events=obj.get("HasEvents", False),
            classroom_events_days=[
                CEEventsDay.de_json(_obj)
                for _obj in obj.get("ClassroomEventsDays", [])
            ]
        )


@dataclass
class Address(_JsonDeserializable):
    oid: Optional[str]
    display_name: Optional[str]
    matches: Optional[int]
    wanting_equipment: Optional[str]

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'Address':
        obj = cls.check_json(json_type)
        return cls(
            oid=obj.get("Oid"),
            display_name=obj.get("DisplayName1"),
            matches=obj.get("matches"),
            wanting_equipment=obj.get("wantingEquipment")
        )


@dataclass
class Classroom(_JsonDeserializable):
    oid: Optional[str]
    display_name: Optional[str]
    seating_type: Optional[str]
    capacity: Optional[int]
    additional_info: Optional[str]
    wanting_equipment: Optional[str]

    @classmethod
    def de_json(cls, json_type: JSON_TYPE) -> 'Classroom':
        obj = cls.check_json(json_type)
        return cls(
            oid=obj.get("Oid"),
            display_name=obj.get("DisplayName1"),
            seating_type=obj.get("SeatingType"),
            capacity=obj.get("Capacity"),
            additional_info=obj.get("AdditionalInfo"),
            wanting_equipment=obj.get("wantingEquipment")
        )


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
