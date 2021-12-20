from typing import Tuple, List, Any, Union

from structures import Room, Classes, Group, Lecturer
from basic_structures import Lecture
from constans import UTIME, STARTOFDAY, ENDOFDAY


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

    :return  zajęcia posortowane w pierwszej kolejności: wykłady, zajęcia o małej dostępności sal, najdłuższe zajęcia
    """
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
                room.potential_occupation_probability[classes.id_] = classes.time.duration / X


def fun_of_gap(gap_length: int, num_of_class: bool = False) -> int:
    """
    Funkcja zwraca wartość zależną od rozmiaru okienka między zajęciami #TODO zobacz czy ma to sens
    :param gap_length: długość okienka
    :param num_of_class ponieważ liczba oceny długości wpisana ręcznie, może być przydatne określenie ile ich może być
            trzeba niestety zmieniać ręcznie - mało profesjonalne, ale znacznie ułatwia
            jeśli True zwraca tylko liczbę klas
    :return: wartość oceny długości zakres [0,5)
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


def generate_groups(file: str) -> Tuple[Group]:
    pass


def generate_lecturers(file: str) -> Tuple[Lecturer]:
    pass


def generate_classes(file: str) -> Tuple[Classes]:
    pass


def generate_rooms(file: str) -> Tuple[Room]:
    pass
