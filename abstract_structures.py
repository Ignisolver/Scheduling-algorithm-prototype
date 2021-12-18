from typing import Tuple

from scheduler.basic_structures import Time, NoRoomAvailable
from scheduler.constans import STARTOFDAY, ENDOFDAY, UTIME
from scheduler.structures import Classes, Room

# todo
class ClassesManager:
    def __init__(self):
        self.assignments = ...

    # todo
    def get_next_classes(self) -> Classes:
        pass

    # todo
    def register_assignment(self, class_: Classes):
        pass

    # todo
    def can_not_assign(self, classes_):
        pass

# todo
class RoomManager:
    def __init__(self, rooms: Tuple[Room]):
        self.rooms = rooms

    # todo - czy ok?
    def get_best_room(self, rooms: Tuple[Room], time: Time) -> Room:
        """
        weź dostępne sale
        sprawdź które mają dostępny ten czas
        sprawdź które mało tracą (z buforem)
        wybierz tą która ma największy priorytet
            ostatnie dwie można zamienić
        """
        available_rooms = []
        # sprawdzanie czasu i dodanie do available_rooms
        for room in rooms:
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
        return time-last_end_before, first_start_after-time

    def _fun_of_gap(self, gap_length: int, num_of_class: bool = False) -> int:
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