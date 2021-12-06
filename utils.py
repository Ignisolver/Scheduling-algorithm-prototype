from typing import Tuple

from structures import Room, Subject, Classes, Lecture, Exercises


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
    """
    0 - najpierw wykłady
    1 - podziel na grupy
    wewnątrz grup
        2 - posortuj na n sekcji po ilości dostępnych sal
        wewnątrz sekcji
            3 - posortuj według długości
    4 scal wszystko dla każdej grupy
    5 bierz po jednej z każdej grupy na zmianę

    Funkcja zakłada, że id to kolejne naturalne bez pomijania wartości

    Później mogę poprawić dzielenie na sekcje (sekcje różnej długości po ilości sal)

    :return  zajęcia posortowane w pierwszej kolejności: wykłady, zajęcia o małej dostępności sal, najdłuższe zajęcia
    """
    # sortowanie zajęć wg id grupy (id grupy wykładu = -1) i dzielenie
    sorted_by_groups = list(classes_).sort(key=group_sort_)
    group_division = [[], []]
    gid = 0
    for classes in sorted_by_groups:
        try:
            if classes.group_id == gid:
                group_division[gid + 1].append(classes)
            else:
                group_division.append([classes])
        except AttributeError:
            group_division[0].append(classes)

    sorted_groups = []
    # sortowanie wewnątrz grup
    for group in group_division:
        sorted_group = []
        # sortowanie wg dostępności sal i dzielenie na sekcje
        group.sort(key=lambda classes: len(classes.available_rooms))
        section_division = [group[i * len(group) // n_sections: (i + 1) * len(group) // n_sections] for i in range(n_sections)]
        # sortowanie w sekcjach po długości
        for section in section_division:
            section.sort(key=lambda classes: classes.time.duration, reverse=True)
            sorted_group.extend(section)
        #scalenie wewnątrz grupy
        sorted_groups.append(sorted_group)

    # biorę po jednej z każdej grupy na zmianę
    sorted_classes = sorted_groups[0][:]
    while len(sorted_groups) > 0:
        for group in sorted_groups:
            if len(group) > 1:
                sorted_classes.append(group.pop(group[0]))
            else:
                sorted_classes.append(group.pop(group[0]))
                sorted_groups.remove(group)

    return tuple(sorted_classes)


def group_sort_(classes):
    """
    Pomocnicza funkcja do sortowania grup
    :param classes:
    :return: id grupy lub -1 gdy wykład
    """
    if isinstance(classes, Lecture):
        return -1
    else:
        return classes.group_id


def add_occupation(rooms_: Tuple[Room], classes_: Tuple[Classes]):
    """
    X = Policz w ilu salach mogą się odbywać dane zajęcia
    każdej sali przypisz dla każdych zajęć szansę że akurat w niej się odbędą 1/X*czas_zajeć
    """
    for classes in classes_:
        X = len(classes.available_rooms)
        for room in rooms_:
            if room in classes.available_rooms:
                room.potential_occupation_probability[classes.id_] = classes.time.duration / X
