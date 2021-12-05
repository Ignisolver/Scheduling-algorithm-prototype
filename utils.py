from typing import Tuple

from structures import Room, Subject, Classes


def calc_goal_function(groups):
    goal_fcn_val = 0
    for group in groups:
        gr_gaol_fcn_val = group.week_schedule.calc_goal_function()
        goal_fcn_val += gr_gaol_fcn_val * len(group.students_ids)
    return goal_fcn_val


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
    pass



