from types import Union
from typing import Tuple

from structures import GlobalSchedule, Lecturer, Group, Room, Lecture, Field, Subject, Classes


def get_id():
    i = 0
    while True:
        yield i
        i += 1


def calc_goal_function(schedule: GlobalSchedule):
    goal_fcn_val = 0
    for group in schedule.groups:
        gr_gaol_fcn_val = group.week_schedule.calc_goal_function()
        goal_fcn_val += gr_gaol_fcn_val * len(group.students_ids)

    for lecturer in schedule.lecturers:
        goal_fcn_val += lecturer.week_schedule.calc_goal_function()

    return goal_fcn_val


def check_capacity_sufficiency(group: Group, room: Room):
    pass


def check_all_group_in_lecture(lecture: Lecture, field: Field):
    pass


def generate_classes(subjects_: Tuple[Subject]) -> Tuple[Classes]:
    classes = []
    for subject in subjects_:
        classes.extend(subject.generate_classes())
    classes = tuple(classes)
    return classes


def sort_classes(classes_: Tuple[Classes], n_sections) -> Tuple[Classes]:
    # 0 - najpierw wykłady
    # 1 - podziel na grupy
    # wewnątrz grup
        # 2 - posortuj na n sekcji po ilości dostępnych sal
        # wewnątrz sekcji
            # 3 - posortuj według długości
    # 4 scal wszystko dla każdej grupy
    # 5 bierz po jednej z każdej grupy na zmianę
    pass


def add_occupation(rooms_: Tuple[Room], classes_: Tuple[Classes]):
    """
    X = Policz w ilu salach mogą się odbywać dane zajęcia
    każdej sali przypisz dla każdych zajęć szansę że akurat w niej się odbędą 1/X*czas_zajeć
    """


