from enum import Enum


class LessonsTypes(Enum):
    ALL = "All"
    PRIMARY = "Primary"
    ATTESTATION = "Attestation"
    FINAL = "Final"
    UNKNOWN = "Unknown"


class SeatingTypes(Enum):
    THEATER = "theater"
    AMPHITHEATER = "amphitheater"
    ROUNDTABLE = "roundtable"


class APIMethods(Enum):
    SD_DIVISIONS = "/study/divisions"
    SD_PROGRAMS = SD_DIVISIONS + "/{alias}/programs/levels"

    P_GROUPS = "/progams/{id}/groups"

    G_EVENTS = "/groups/{id}/events"
    G_EVENTS_FROM = G_EVENTS + "/{from}"
    G_EVENTS_FROM_TO = G_EVENTS_FROM + "/{to}"

    ED_DIVISIONS = "/extracur/divisions"
    ED_EVENTS = ED_DIVISIONS + "/{alias}/events"

    E_SEARCH = "/educators/search/{query}"
    E_EVENTS = "/educators/{id}/events"
    E_EVENTS_FROM_TO = E_EVENTS + "/{from}/{to}"

    C_IS_BUSY = "/classrooms/{oid}/isbusy/{start}/{end}"
    C_EVENTS = "/classrooms/{oid}/events/{from}/{to}"

    A_ADDRESSES = "/addresses"
    A_CLASSROOMS = A_ADDRESSES + "/{oid}/classrooms"


BASE_URL = "https://timetable.spbu.ru/api/v1"
available_lessons_types = ("All", "Primary", "Attestation", "Final", "Unknown")
available_seating_types = ("theater", "amphitheater", "roundtable")

error_msg = "A request to the SPbU Timetable API was unsuccessful. {0}"
