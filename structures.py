from __future__ import annotations
from abc import abstractmethod
from typing import Iterable, List, Dict, NewType, Tuple

UTIME = 5 # jednostka czasu #TODO znaleźć lepsze miejsce na te stałe
STARTOFDAY = Hour(7, 30) # od której mogą zaczynać się zajęcia
ENDOFDAY = Hour(20, 30) # do której najpóźniej mogą być zajęcia


class ClassesID(int):
    pass


class RoomID(int):
    pass


class LecturerError:
    pass


class RoomError:
    pass


class Hour:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def __add__(self, other):
        if isinstance(other, int):
            hours2add = int(other / 60)
            mins2add = int(other % 60)

            hour = self.hour + hours2add
            minute = self.minute + mins2add

            if minute > 60:
                minute = minute % 60
                over_hours = int(minute / 60)
                hour += over_hours

            if hour > 24:
                raise Exception

            return Hour(hour, minute)

    def __sub__(self, other):
        if isinstance(other, Hour):
            return 60 * (self.hour - other.hour) + self.minute - other.minute


    def __lt__(self, other):
        if isinstance(other, Hour):
            if self.hour == other.hour:
                return self.minute < other.minute
            return self.hour < other.minute


class Time:
    def __init__(self, day_nr, start: Hour, duration_mins: int):
        self.day_nr = day_nr
        self.start = start
        self.end = start + duration_mins
        self.duration = duration_mins


class Classes:  # zajęcia - ogólnie
    def __init__(self):
        self.id_: ClassesID = ...
        self.lecturer: Lecturer = ...
        self.time: Time = ...
        self.available_rooms: Tuple[Room] = ...
        self.room: Room = ...

    @abstractmethod
    def get_best_time(self, next_=False) -> Time:
        """
        coś z yield-em
        """
        pass

    def is_lecturer_available(self, time: Time) -> bool:
        pass

    @abstractmethod
    def _assign(self, time: Time, room: Room):
        pass

    def assign(self, time: Time, room: Room):
        self._assign(time, room)
        room.assign(self)
        self.lecturer.assign(self)


class Lecture(Classes):  # wykład
    def __init__(self):
        super().__init__()
        self.field_id = ...

    def get_best_time(self, next_=False) -> Time:
        pass

    def _assign(self, time: Time, room: Room):
        pass


class Exercises(Classes):  # ćwiczenia
    def __init__(self):
        super().__init__()
        self.group_id = ...

    def get_best_time(self, next_=False) -> Time:
        pass

    def _assign(self, time: Time, room: Room):
        pass


class Lecturer:
    def __init__(self):
        self.id_ = ...
        self.subject_id = ...
        self.amount_of_hours = ...
        self.group_id = ...
        self.week_schedule: WeekSchedule = ...

    def is_time_available(self, time) -> bool:
        return self.week_schedule.is_time_available(time)

    def assign(self, classes):
        pass


class Room:  # sala
    def __init__(self):
        self.id_ = ...
        self.capacity = ...
        self.predicted_occupation: int = ...  # szacunkowy współczynnik ile będzie zajęta
        self.current_occupation: int = ...  # ile już jest zajęta minuty
        self.availability: int = ...  # ile ma dostępnego czasu wogóle
        self.priority = ...
        self.week_schedule: WeekSchedule = ...
        self.potential_occupation_probability: Dict[ClassesID, int] = ...

    def _update(self, classes: Classes):
        self.potential_occupation_probability[classes.id_] = 0  # todo cofanie
        self.predicted_occupation = sum(self.potential_occupation_probability.values())
        self.current_occupation += classes.time.duration
        self.priority = (self.availability - self.current_occupation) / self.predicted_occupation

    def assign(self, classes):
        self._assign(classes)
        self._update(classes)
        pass

    def _assign(self, classes: Classes):
        pass

    def is_time_available(self, time) -> bool:
        return self.week_schedule.is_time_available(time)


class Registrar:
    def __init__(self):
        self.assignments = ...

    def register_assignment(self, class_: Classes):
        pass

    def revert_assignments(self, cause):
        pass

    def get_current_class_number(self) -> int:
        pass


class Group:  # grupa
    def __init__(self):
        self.id_ = ...
        self.students_amount = ...
        self.subjects_ids = ...
        self.week_schedule: WeekSchedule = ...


class Subject:  # przedmiot
    def __init__(self):
        self.id_ = ...
        self.week_classes_duration = ...
        self.week_lecture_duration = ...
        self.lecturers = ...
        self.groups = ...

    def generate_classes(self) -> List[Classes]:
        pass


class Field:  # kierunek
    def __init__(self):
        self.groups_ids = ...
        self.subjects_ids = ...


class WeekSchedule:
    def __init__(self):
        self.day_schedules = ...

    def get_best_place(self, duration, next_=True):
        pass

    def is_time_available(self, time) -> bool:
        pass

    def _calc_goal_function(self):
        pass

    def _calc_week_FO(self):
        pass

    def _calc_week_FD(self):
        pass

    def calc_week_FP(self):
        pass

    def _calc_week_FR(self):
        pass


class DaySchedule:
    def __init__(self):
        self.classes: Iterable[Classes] = ...

    def assign(self):
        pass

    def get_best_time(self):
        pass

    def calc_day_FO(self):
        pass

    def calc_day_FP(self):
        pass

    def calc_day_FR(self):
        pass


class NoRoomAvailable(Exception):
    def __init__(self):
        super().__init__()


class NoAvailableTime(Exception):
    def __init__(self):
        super().__init__()


class RoomManager:
    def __init__(self, rooms: Tuple[Room]):
        self.rooms = rooms

    def get_best_room(self, ids: Tuple[Room], time: Time) -> Room:
        """
        weź dostępne sale
        sprawdź które mają dostępny ten czas
        sprawdź które mało tracą (z buforem)
        wybierz tą która ma największy priorytet
            ostatnie dwie można zamienić
        """
        available_rooms = []
        # sprawdzanie czasu i dodanie do available_rooms
        for room in ids:
            if room.is_time_available(time):
                available_rooms.append(room)

        # sprawdzam czy jest więcej niż jedna sala dostępna
        if len(available_rooms) < 1:
            raise NoRoomAvailable
        if len(available_rooms) == 1:
            return available_rooms[0]

        # podział na sekcje względem długości przerw przed i po czasie
        available_rooms_sections = [[] for _ in range(self._fun_of_gap(0, True))]
        for room in available_rooms:
            fgap = self._fun_of_gap(sum(self._availability_around_time(room, time)))
            available_rooms_sections[fgap] = room

        # Wybór najwyższego priorytetu z uwzględnieniem sekcji
        for section in available_rooms_sections:
            if len(section) > 1:
                max_priority_room = section[0]
                for room in section[1:]:
                    if max_priority_room.priority < room.priority:
                        max_priority_room = room
                return max_priority_room
            elif section:
                return section[0]
        raise InterruptedError("Popsułem funkcję get_best_room")

    def _availability_around_time(self, room, time):
        """
        Funkcja pomocnicza do sprawdzania ile czasu do następnych zajęć i ile czasu od ostatnich zajęć
        :return: (a, b) - a = czas od ostatnich zajęć , b = czas do następnych zajęć
        """
        last_end_before = STARTOFDAY
        first_start_after = ENDOFDAY
        for classes in room.week_schedule[time.day_nr].day_schedule.classes:
            if classes.time.end < time.start:
                if last_end_before < classes.time.end:
                    last_end_before = time
            elif time.end < classes.time.start:
                if classes.time.start < first_start_after:
                    first_start_after = time
        return time - last_end_before, first_start_after - time

    def _fun_of_gap(self, gap_length: int, num_of_class: bool =False):
        """
        Funkcja zwraca wartość zależną od rozmiaru okienka między zajęciami #TODO zobacz czy ma to sens
        :param gap_length: długość okienka
        :param num_of_class ponieważ liczba oceny długości wpisana ręcznie, może być przydatne określenie ile ich może być
                trzeba niestety zmieniać ręcznie - mało profesjonalne, ale znacznie ułatwia
                jeśli True zwraca tylko liczbę klas
        :return: wartość oceny długości zakres [0,5) lub
        """
        if num_of_class:
            return 5

        if gap_length < 0:
            raise ValueError("Długość przerwy mniejsza od zera")
        if gap_length % 90 == (
                gap_length // 90 + 1) * UTIME:  # okienko wielokrotnością 90 min zajęć + 5 przerwy przed i po
            return 0
        if gap_length % 45 == (
                gap_length // 45 + 1) * UTIME:  # okienko wielokrotnością 45 min zajęć + 5 przerwy przed i po
            return 1
        if gap_length % 45 <= (
                gap_length // 45 + 1) * 4 * UTIME:  # przerwa między miejscami na zajęciami <=20min ale dłuższa niż 5 min
            return 2
        if gap_length % 45 == 0:  # braknie przerw między zajęciami
            return 3
        return 4  # pozostałe
