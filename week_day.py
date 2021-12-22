from typing import Callable, List, TYPE_CHECKING

from scheduler.basic_structures import Time
from constans import UTIME, MAX_FD, MAX_FO, MAX_FR, MAX_FP
from parameters import WEIGHTS_FD, FUN_WEIGHTS
from utils import weights_FP

if TYPE_CHECKING:
    from structures import Classes


class WeekSchedule:
    def __init__(self):
        self.day_schedules = [DaySchedule()] * 5

    def is_time_available(self, time, brake_time_) -> bool:
        for classes in self.day_schedules[time.day_nr].classes:
            if time.cross(classes.time, brake_time_):
                return False
        return True

    def calc_goal_function(self) -> float:
        return FUN_WEIGHTS[0] * self._calc_week_FO() + \
               FUN_WEIGHTS[1] * self._calc_week_FD() + \
               FUN_WEIGHTS[2] * self._calc_week_FP(self._get_week_classes_time()) + \
               FUN_WEIGHTS[3] * self._calc_week_FR(self._get_week_classes_time(), self._get_amount_of_free_days())

    def assign(self, classes):
        self.day_schedules[classes.time.day_nr].assign(classes)

    def revert_assign(self, classes):
        self.day_schedules[classes.time.day_nr].revert_assign(classes)

    def _get_week_classes_time(self):
        time: int = 0
        for day in self.day_schedules:
            time += day.get_day_classes_time()
        return time

    def _get_amount_of_free_days(self) -> int:
        free_days: int = 0
        for day in self.day_schedules:
            if day.is_day_free():
                free_days += 1
        return free_days

    def _calc_week_FO(self) -> float:
        return sum([day.calc_day_FO() for day in self.day_schedules])

    def _calc_week_FD(self) -> float:
        satisfaction: int = 0
        for i in range(5):
            satisfaction += int(self.day_schedules[i].is_day_free()) * WEIGHTS_FD[i]
        return satisfaction / MAX_FD

    def _calc_week_FP(self, week_classes_time: int) -> float:
        return sum([day.calc_day_FP(week_classes_time) for day in self.day_schedules])

    def _calc_week_FR(self, week_classes_time: int, num_of_free_days: int) -> float:
        return sum([day.calc_day_FR(week_classes_time, num_of_free_days) for day in self.day_schedules])


class DaySchedule:
    def __init__(self):
        self.classes: List[Classes] = []
        self.weights_FP: Callable[[Time], float] = ...  # todo wagi z constans.py

    def assign(self, classes: Classes):
        self.classes.append(classes)

    def revert_assign(self, classess: Classes):
        self.classes.remove(classess)

    def get_day_classes_time(self) -> int:
        time = 0
        for classes_ in self.classes:
            time += classes_.time.duration
        return time

    def is_day_free(self) -> bool:
        return not bool(self.classes)

    def calc_day_FO(self) -> float:
        if len(self.classes) < 2:
            return 0
        self.classes.sort(key=lambda c: c.time.start)
        break_time: int = 0
        for i in range(len(self.classes) - 1):
            break_time += abs(self.classes[i+1].time.start-self.classes[i].time.end - UTIME)
        return break_time / len(self.classes) / MAX_FO

    def calc_day_FP(self, week_classes_time: int) -> float:
        satisfaction: int = 0
        for classes in self.classes:
            satisfaction += weights_FP(classes.time)
        return satisfaction / week_classes_time / MAX_FP

    def calc_day_FR(self, week_classes_time: int, num_of_free_days: int) -> float:
        return abs(week_classes_time / (5 - num_of_free_days) - self.get_day_classes_time()) / MAX_FR
