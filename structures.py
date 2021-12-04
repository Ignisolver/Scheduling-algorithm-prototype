from abc import abstractmethod
from typing import Iterable, List, Dict, NewType, Tuple


class ClassesID(int):
    pass

class RoomID(int):
    pass

class Hour:
    def __init__(self,hour, minute):
        self.hour = hour
        self.minute = minute

    def __add__(self, other):
        if isinstance(other, int):
            hours2add = int(other/60)
            mins2add = int(other%60)

            hour = self.hour+hours2add
            minute = self.minute + mins2add

            if minute > 60:
                minute = minute % 60
                over_hours = int(minute/60)
                hour += over_hours

            if hour > 24:
                raise Exception

            return Hour(hour, minute)


class Time:
    def __init__(self, day_nr, start: Hour, duration_mins: int):
        self.day_nr = day_nr
        self.start = start
        self.end = start + duration_mins
        self.duration = duration_mins


class Classes:  # zajęcia - ogólnie
    def __init__(self):
        self.id_ = ...
        self.lecturer_id = ...
        self.time: Time = ...
        self.available_room_ids = ...

    def assign(self):
        """
        znajdź pierwsze minimum funkcji celu
        sprawdź czy może prowadzący
            jak nie weź kolejne minimum
        wybierze najlepszą salę
            jak nie ma wolnych weź kolejne minimum
        przypisz
        """

    @abstractmethod
    def _get_best_time(self) -> Time:
        pass

    def _is_lecturer_available(self) -> bool:
        pass

    @abstractmethod
    def _assign(self):
        pass


class Student:
    def __init__(self):
        self.id_ = ...
        self.group_id = ...


class Lecturer:
    def __init__(self):
        self.id_ = ...
        self.subject_id = ...
        self.amount_of_hours = ...
        self.group_id = ...
        self.week_schedule: WeekSchedule = ...


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
        self.priority = (self.availability-self.current_occupation) / self.predicted_occupation

    def assign(self):
        self._assign()
        self._update()
        pass

    def _assign(self):
        pass


class Registrar:
    def __init__(self):
        self.assignments = ...

    def register_assignment(self):
        pass

    def revert_assignment(self):
        pass


class Group:  # grupa
    def __init__(self):
        self.id_ = ...
        self.students_ids = ...
        self.subjects_ids = ...
        self.week_schedule: WeekSchedule = ...


class Subject:  # przedmiot
    def __init__(self):
        self.id_ = ...
        self.week_classes_duration = ...
        self.week_lecture_duration = ...
        self.lecturers_ids = ...
        self.groups_ids = ...

    def generate_classes(self) -> List[Classes]:
        pass


class Lecture(Classes):  # wykład
    def __init__(self):
        super().__init__()
        self.field_id = ...


class Exercises(Classes):  # ćwiczenia
    def __init__(self):
        super().__init__()
        self.group_id = ...


class Field:  # kierunek
    def __init__(self):
        self.groups_ids = ...
        self.subjects_ids = ...


class WeekSchedule:
    def __init__(self):
        self.day_schedules = ...

    def get_best_place(self, duration, next_=True):
        pass

    def is_time_available(self) -> bool:
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


class RoomManager:
    def __init__(self, rooms: Tuple[Room]):
        self.rooms = rooms

    def _get_best_room(self, ids: Tuple[RoomID]) -> RoomID:
        """
        weź dostępne sale
        sprawdź które mają dostępny ten czas
        sprawdź które mało tracą (z buforem)
        wybierz tą która ma największy priorytet
            ostatnie dwie można zamienić
        """
        pass
