from typing import Tuple, List
from csv import reader

from structures import Room, Classes, Group, Lecturer
from basic_structures import Lecture, Exercises, ClassesID


def sort_classes(classes_: Tuple[Classes], n_sections: int) -> Tuple[Classes]:
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

    :return  zajęcia posortowane w ostatniej kolejności: wykłady, zajęcia o małej dostępności sal, najdłuższe zajęcia
    """
    if n_sections > len(classes_):
        raise ValueError(" n_sections must be lesser or equal length of classes tuple")
    # sortowanie zajęć wg id grupy (id grupy wykładu = -1) i dzielenie
    sorted_by_groups: List[Classes] = list(classes_)
    sorted_by_groups.sort(key=group_sort_id)
    group_division: List[List[Classes]] = [[]] * (sorted_by_groups[-1].get_groups()[-1].id_ + 2)
    for classes in sorted_by_groups:
        group_division[group_sort_id(classes) + 1].append(classes)

    sorted_groups = []
    # sortowanie wewnątrz grup
    for group in group_division:
        sorted_group = []
        # sortowanie wg dostępności sal i dzielenie na sekcje
        group.sort(key=lambda classes__: len(classes__.available_rooms))
        section_division = [group[i * len(group) // n_sections: (i + 1) * len(group) // n_sections] for i in
                            range(n_sections)]
        # sortowanie w sekcjach po długości
        for section in section_division:
            section.sort(key=lambda classes__: classes__.get_duration(), reverse=True)
            sorted_group.extend(section)
        # scalenie wewnątrz grupy
        sorted_groups.append(sorted_group)

    # biorę po jednej z każdej grupy na zmianę
    sorted_classes: List[Classes] = sorted_groups[0][:]
    while len(sorted_groups) > 0:
        for group in sorted_groups:
            if len(group) > 1:
                sorted_classes.append(group.pop(0))
            else:
                sorted_classes.append(group.pop(0))
                sorted_groups.remove(group)

    sorted_classes.reverse()
    return tuple(sorted_classes)


def group_sort_id(classes: Classes) -> int:
    """
    Pomocnicza funkcja do sortowania grup
    :param classes:
    :return: id grupy lub -1 gdy wykład
    """
    if len(classes.get_groups()) > 1:
        return -1
    else:
        return classes.get_groups()[0].id_


def add_occupation(rooms_: Tuple[Room], classes_: Tuple[Classes]):
    """
    X = Policz w ilu salach mogą się odbywać dane zajęcia
    każdej sali przypisz dla każdych zajęć szansę że akurat w niej się odbędą 1/X*czas_zajeć
    """
    for classes in classes_:
        X: int = len(classes.available_rooms)
        for room in rooms_:
            if room in classes.available_rooms:
                room.potential_occupation_probability[classes.id_] = classes.duration / X
    for room in rooms_:
        room.add_const_potential_occupation_probability()


def generate_groups(file: str) -> Tuple[Group]:
    """
    Pobiera dane o grupach: id - indeksy, liczebność grupy
    :param file:
    :return:
    """
    groups = []
    with open(file) as f:
        read = reader(f)
        for re in read:
            if re[0] != '':
                groups.append(Group(int(re[0]), int(re[1])))
    return tuple(groups)


def generate_lecturers(file: str) -> Tuple[Lecturer]:
    """
    Pobiera dane o prowadzących: id - indeksy
    :param file:
    :return:
    """
    lecturers = []
    with open(file) as f:
        read = reader(f)
        for re in read:
            if re[0] != '':
                lecturers.append(Lecturer(int(re[0])))
    return tuple(lecturers)


def generate_classes(file: str, lecturers: Tuple[Lecturer], groups: Tuple[Group], rooms: Tuple[Room]) -> Tuple[Classes]:
    """
    Pobiera dane o zajęciach: id - indeksy, id prowadzącego, typ, czas trwania, sale, grupy
    Zakłada się, że rooms, groups, lecturers są posortowane wg. id!
    :param rooms:
    :param groups:
    :param lecturers:
    :param file:
    :return:
    """
    classes = []
    with open(file) as f:
        read = reader(f)
        for re in read:
            if re[0] != '':
                classes_room_id = [int(room) for room in (re[4][1:-1]).split(", ")]
                classes_group_id = [int(group) for group in (re[5][1:-1]).split(", ")]
                if re[2] == "Lecture":
                    class_type = Lecture()
                if re[2] == Exercises:
                    class_type = Exercises()

                classes.append(Classes(ClassesID(re[0]),          # id_
                                       lecturers[int(re[1])],    # lecturer
                                       int(re[3]),          # duration
                                       tuple([rooms[rid] for rid in classes_room_id]),  # rooms
                                       class_type,          # type
                                       [groups[rid] for rid in classes_group_id]  # groups
                                       ))
    return tuple(classes)


def generate_rooms(file: str) -> Tuple[Room]:
    """
    Pobiera dane o salach: id - indeksy, availability
    :param file:
    :return:
    """
    rooms = []
    with open(file) as f:
        read = reader(f)
        for re in read:
            if re[0] != '':
                rooms.append(Room(int(re[0]), int(re[1])))
    return tuple(rooms)
