from __future__ import annotations

from abc import abstractmethod, ABCMeta
from copy import deepcopy
from functools import cache
from typing import List, Dict, Tuple, Union, Optional

from parameters import LECTURER_WEIGHT
from basic_structures import ClassesID, Lecture, Exercises, Time
from constans import UTIME, ENDOFDAY, STARTOFDAY
from scheduler.constans import COLORS
from week_day import WeekSchedule


def _color_getter():
    while True:
        for color in COLORS:
            yield color


get_color = _color_getter()


class Classes:  # zajęcia - ogólnie
    def __init__(self,
                 id_: ClassesID,
                 lecturer: Lecturer,
                 duration: int,
                 rooms: Tuple[Room],
                 type_: Union[Lecture, Exercises],
                 groups: List[Group]):
        self.id_ = id_
        self._type = type_
        self._lecturer = lecturer
        self._duration = duration
        self.available_rooms = rooms
        self._groups = groups
        # TO ASSIGN
        self.time: Time = ...
        self.room: Room = ...

    def get_rooms(self) -> Tuple[Room]:
        return self.available_rooms

    def get_groups(self) -> List[Group]:
        return self._groups

    def get_duration(self) -> int:
        return self._duration

    def assign(self, time: Time, room: Room):
        self.time = time
        self.room = room
        self._lecturer.assign(self)
        self.room.assign(self)
        for group in self._groups:
            group.assign(self)

    def revert_assign(self):
        self.time = None
        self.room = None
        self._lecturer.revert_assign(self)
        self.room.revert_assign(self)
        for group in self._groups:
            group.revert_assign(self)

    @staticmethod
    def get_best_time(times, g_f_vals):
        all_ = list(zip(times, g_f_vals))
        while all_:
            best = min(all_, key=lambda x: x[1])
            yield best[0]
            all_.remove(best)

    def get_times(self, duration):
        times = []
        nr = 0
        for day_nr in range(5):
            s_h_g = self._start_hour_generator()
            for start_hour in s_h_g:
                time = Time(day_nr, start_hour, duration)
                times.append((nr, time))
                nr += 1
        return times

    def _start_hour_generator(self):
        end = ENDOFDAY - self._duration
        hour = STARTOFDAY
        while hour <= end:
            yield hour
            hour += UTIME

    def _get_available_times(self, times):
        ok_times = []
        for time in times:
            if self._lecturer.is_time_available(time, UTIME):
                for group in self._groups:
                    if not group.week_schedule.is_time_available(time, UTIME):
                        break
                else:
                    ok_times.append(time)
        return times

    def _get_goal_func_vals(self, times):
        goal_fun_vals = []
        for time in times:
            g_f_val = 0
            self.time = time

            for group in self._groups:
                group.assign(self)
                g_f_val += group.week_schedule.calc_goal_function() * group.students_amount
                group.revert_assign(self)

            self._lecturer.assign(self)
            g_f_val += self._lecturer.week_schedule.calc_goal_function() * LECTURER_WEIGHT
            self._lecturer.revert_assign(self)

            self.time = None

            goal_fun_vals.append(g_f_val)
        return goal_fun_vals

    def get_best_time_generator(self):
        times = self.get_times(self._duration)
        ok_times = self._get_available_times(times)
        goal_fun_vals = self._get_goal_func_vals(ok_times)
        g_b_t_gen = self.get_best_time(times, goal_fun_vals)
        return g_b_t_gen

    def _get_groups_ids(self):
        return ",".join([group.id_ for group in self._groups])

    def _get_name_info(self):
        data_txt = \
            f"""id-{self.id_}
            room-{self.room.id_}
            lecturer-{self._lecturer.id_}
            group-{self._get_groups_ids()}"""
        return data_txt

    @cache
    def print(self, letter):
        txt = f"""- name: |
        {self._get_name_info()}
        days: {letter}
        time: {self.time}
        color: "{next(get_color)}"
        
        """
        return txt


class WithSchedule(metaclass=ABCMeta):
    def __init__(self):
        self.id_ = None

    @abstractmethod
    def print_schedule(self):
        pass


class Lecturer(WithSchedule):
    def __init__(self, id_):
        super().__init__()
        self.id_ = id_
        self.week_schedule = WeekSchedule()

    def is_time_available(self, time, brake_time_) -> bool:
        return self.week_schedule.is_time_available(time, brake_time_)

    def assign(self, classes):
        self.week_schedule.assign(classes)

    def revert_assign(self, classes):
        self.week_schedule.revert_assign(classes)

    def print_schedule(self):
        return self.week_schedule.print_schedule()


class Room(WithSchedule):  # sala
    def __init__(self, id_, availability: int):
        super().__init__()
        self.id_ = id_
        self._predicted_occupation: float = 0  # szacunkowy współczynnik ile będzie zajęta
        self._current_occupation = 0  # ile już jest zajęta minuty
        self._availability: int = availability  # ile ma dostępnego czasu wogóle
        self.priority: float = float("inf")  # na jago podstawie trzeba wybierac, im mniejszy tym lepiej
        self.week_schedule: WeekSchedule = WeekSchedule()
        self.potential_occupation_probability: Dict[ClassesID, float] = {}
        self._const_potential_occupation_probability: Optional[Dict[ClassesID, float]] = None

    def add_const_potential_occupation_probability(self):
        if self._const_potential_occupation_probability is None:
            self._const_potential_occupation_probability = deepcopy(self.potential_occupation_probability)
        else:
            AttributeError("const_potential_occupation_probability already exist!")

    def _update(self, classes: Classes):
        self._predicted_occupation = sum(self.potential_occupation_probability.values())
        self._current_occupation += classes.time.duration
        self.priority = (self._availability - self._current_occupation) / self._predicted_occupation

    def assign(self, classes):
        self.potential_occupation_probability[classes.id_] = 0
        self._update(classes)
        self.week_schedule.assign(classes)
        pass

    def revert_assign(self, classes):
        self.potential_occupation_probability[classes.id_] = self._const_potential_occupation_probability[classes.id_]
        self._update(classes)
        self.week_schedule.revert_assign(classes)
        pass

    def is_time_available(self, time: Time) -> bool:
        return self.week_schedule.is_time_available(time, 0)

    def print_schedule(self):
        return self.week_schedule.print_schedule()


class Group(WithSchedule):  # grupa
    def __init__(self, id_, sa):
        super().__init__()
        self.id_ = id_
        self.students_amount = sa
        self.week_schedule: WeekSchedule = WeekSchedule()

    def assign(self, classes: Classes):
        self.week_schedule.assign(classes)

    def revert_assign(self, classes: Classes):
        self.week_schedule.revert_assign(classes)

    def print_schedule(self):
        return self.week_schedule.print_schedule()
