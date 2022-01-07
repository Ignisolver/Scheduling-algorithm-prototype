from typing import Callable, List, TYPE_CHECKING

from basic_structures import Time
from constans import MAX_FD, MAX_FO, MAX_FR, MAX_FP, STARTOFDAY, ENDOFDAY, DAY_LETTER
from parameters import FUN_WEIGHTS, UTIME

if TYPE_CHECKING:
    from structures import Classes


def weights_FP(time: Time) -> float:
    """
    Funkcja wyznacza wagę pory rozpoczęcia zajęć, funkcja rośnie od 0 do 1 w okresie między STARTOFDAY, ENDOFDAY
    """
    return (time.start - STARTOFDAY) / (ENDOFDAY - STARTOFDAY)


class WeekSchedule:
    def __init__(self):
        self.day_schedules = [DaySchedule() for _ in range(5)]

    def __getitem__(self, item):
        return self.day_schedules[item]

    def is_time_available(self, time: Time, brake_time_) -> bool:
        for classes in self.day_schedules[time.day_nr].classes:
            if time.cross(classes.time, brake_time_):
                return False
        return True

    def calc_goal_function(self) -> float:
        return FUN_WEIGHTS[0] * self.calc_week_FO() + \
               FUN_WEIGHTS[1] * (5 - self.calc_week_FD()) + \
               FUN_WEIGHTS[2] * self.calc_week_FP(self.get_week_classes_time()) + \
               FUN_WEIGHTS[3] * self.calc_week_FR(self.get_week_classes_time(), self.get_amount_of_free_days())

    def assign(self, classes, break_time_):
        if self.is_time_available(classes.time, break_time_):
            self.day_schedules[classes.time.day_nr].assign(classes)
        else:
            raise RuntimeError("Trying to assign to unavailable time")

    def revert_assign(self, classes):
        self.day_schedules[classes.time.day_nr].revert_assign(classes)

    def get_week_classes_time(self):
        time: int = 0
        for day in self.day_schedules:
            time += day.get_day_classes_time()
        return time

    def get_amount_of_free_days(self) -> int:
        free_days: int = 0
        for day in self.day_schedules:
            if day.is_day_free():
                free_days += 1
        return free_days

    def calc_week_FO(self) -> float:
        return sum([day.calc_day_FO() for day in self.day_schedules])

    def calc_week_FD(self) -> float:
        free_days = [1] * 4
        satisfaction = 0
        for i in reversed(range(5)):
            free_days.insert(2, int(self.day_schedules[i].is_day_free()))
        for day in range(2, 7):
            satisfaction += sum([free_days[day] *
                                 (1 +
                                  free_days[day + 1] * (1 + free_days[day + 2]) +
                                  free_days[day - 1] * (1 + free_days[day - 2]))])
        return -satisfaction / MAX_FD

    def calc_week_FP(self, week_classes_time: int) -> float:
        return sum([day.calc_day_FP(week_classes_time) for day in self.day_schedules])

    def calc_week_FR(self, week_classes_time: int, num_of_free_days: int) -> float:
        return sum([day.calc_day_FR(week_classes_time, num_of_free_days) for day in self.day_schedules])

    def print_schedule(self):
        text = ""
        for day_nr, day_sched in enumerate(self.day_schedules):
            text += day_sched.print_schedule()
        return text


class DaySchedule:
    def __init__(self):
        self.classes: List[Classes] = []
        self.weights_FP: Callable[[Time], float] = weights_FP

    def assign(self, classes: "Classes"):
        self.classes.append(classes)

    def revert_assign(self, classes: "Classes"):
        self.classes.remove(classes)

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
            break_time += abs(self.classes[i + 1].time.start - self.classes[i].time.end - UTIME)
        return break_time / len(self.classes) / MAX_FO

    def calc_day_FP(self, week_classes_time: int) -> float:
        if week_classes_time <= 0:
            return 0
        satisfaction: int = 0
        for classes in self.classes:
            satisfaction += weights_FP(classes.time)
        return satisfaction / week_classes_time / MAX_FP

    def calc_day_FR(self, week_classes_time: int, num_of_free_days: int) -> float:
        if num_of_free_days == 5:
            return 0
        return abs(week_classes_time / (5 - num_of_free_days) - self.get_day_classes_time()) / MAX_FR

    def print_schedule(self):
        text = ""
        for classes in self.classes:
            text += classes.print() + "\n\n"
        return text
