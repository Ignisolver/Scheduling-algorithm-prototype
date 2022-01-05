from typing import Tuple, List, Union, Optional
from random import randint

from basic_structures import Time, AssignError
from constans import STARTOFDAY, ENDOFDAY
from parameters import UTIME
from structures import Classes, Room


class RoomManager:
    def __init__(self, rooms: Tuple[Room]):
        self.rooms = rooms

    def get_best_room(self, rooms: List[Room], time: Time) -> Optional[Room]:
        available_rooms = []
        # sprawdzanie czasu i dodanie do available_rooms
        for room in rooms:
            if room.is_time_available(time):
                available_rooms.append(room)

        # sprawdzam czy jest więcej niż jedna sala dostępna
        if len(available_rooms) < 1:
            return None
        if len(available_rooms) == 1:
            return available_rooms[0]

        # podział na sekcje względem długości przerw przed i po czasie
        available_rooms_sections = [[] for _ in range(self.fun_of_gap(0, True) * 2 + 1)]
        for room in available_rooms:
            fgap = sum(self.fun_of_gap(self.availability_of_room_around_time(room, time)))
            available_rooms_sections[fgap].append(room)

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
        raise InterruptedError("function get_best_room is messed up")

    @staticmethod
    def availability_of_room_around_time(room: Room, time: Time) -> Tuple[int, int]:
        """
        Funkcja pomocnicza do sprawdzania ile czasu do następnych zajęć i ile czasu od ostatnich zajęć
        :return: (a, b) - a = czas od ostatnich zajęć , b = czas do następnych zajęć
        """
        last_end_before = STARTOFDAY
        first_start_after = ENDOFDAY
        for classes in room.week_schedule.day_schedules[time.day_nr].classes:
            if classes.time.end < time.start:
                if last_end_before < classes.time.end:
                    last_end_before = time.end
            elif time.end < classes.time.start:
                if classes.time.start < first_start_after:
                    first_start_after = time.start
        return int(time.start - last_end_before), int(first_start_after - time.end)

    @staticmethod
    def fun_of_gap(gap_length: Union[int, Tuple[int, int]], num_of_class: bool = False) -> Union[int, Tuple[int, ...]]:
        """
        Funkcja zwraca wartość zależną od rozmiaru okienka między zajęciami #TODO zobacz czy ma to sens
        :param gap_length: długość okienka
        :param num_of_class ponieważ liczba oceny długości wpisana ręcznie, może być przydatne określenie ile ich
                    może być trzeba niestety zmieniać ręcznie - mało profesjonalne, ale znacznie ułatwia
                jeśli True zwraca tylko liczbę klas
        :return: wartość oceny długości zakres [0,5)
        """
        if num_of_class:
            return 5

        if gap_length is int:
            if gap_length < 0:
                raise ValueError("Break _time must be >= 0")
            if gap_length % 90 == (gap_length // 90 + 1) * UTIME:
                return 0  # okienko wielokrotnością 90 min zajęć + 5 przerwy przed i po
            if gap_length % 45 == (gap_length // 45 + 1) * UTIME:
                return 1  # okienko wielokrotnością 45 min zajęć + 5 przerwy przed i po
            if gap_length % 45 <= (gap_length // 45 + 1) * 4 * UTIME:
                return 2  # przerwa między miejscami na zajęciami <=20min ale dłuższa niż 5 min
            if gap_length % 45 == 0:
                return 3  # braknie przerw między zajęciami
            return 4  # pozostałe
        else:
            rslt = []
            for gap in gap_length:
                if gap < 0:
                    raise ValueError("Break _time must be >= 0")
                elif gap % 90 == (gap // 90 + 1) * UTIME:
                    rslt.append(0)  # okienko wielokrotnością 90 min zajęć + 5 przerwy przed i po
                elif gap % 45 == (gap // 45 + 1) * UTIME:
                    rslt.append(1)  # okienko wielokrotnością 45 min zajęć + 5 przerwy przed i po
                elif gap % 45 <= (gap // 45 + 1) * 4 * UTIME:
                    rslt.append(2)  # przerwa między miejscami na zajęciami <=20min ale dłuższa niż 5 min
                elif gap % 45 == 0:
                    rslt.append(3)  # braknie przerw między zajęciami
                else:
                    rslt.append(4)  # pozostałe
            return tuple(rslt)


class ClassesManager:
    def __init__(self, classes: Tuple[Classes]):
        self.assignments: List[Classes] = []
        self.classes2assign: List[Classes] = list(classes)

    def get_not_assigned_number(self) -> int:
        return len(self.classes2assign)

    def get_next_classes(self) -> Optional[Classes]:
        if bool(self.classes2assign):
            return self.classes2assign.pop(-1)
        else:
            return None

    def register_assignment(self, class_: Classes):
        self.assignments.append(class_)

    def can_not_assign(self, classes_: Classes, sltn_type: str = "backtracking", step: int = 5, rm: RoomManager = None):
        if step <= 0:
            raise ValueError("step must be > 0")
        if sltn_type == "backtracking":
            self._backtracking(classes_, step)
        elif sltn_type == "reconstruction":
            self._reconstruction(classes_, step)
        elif sltn_type == "replacing":
            self._replacing(classes_, rm)
        else:
            raise KeyError("can_not_assign don't recognise parameter '{0}'".format(sltn_type))

    def _backtracking(self, classes_: Classes, step: int = 1):
        """
        Funkcja cofa przypisania do momentu, gdy znajdzie się miejsce dla danych zajęć
        :param classes_: nie przypisane zajęcia,
        :param step: krok o jaki jest prowadzone cofnięcie
        :return:
        """
        if bool(self.assignments):
            if len(self.assignments) < step:
                step = len(self.assignments)
            for _ in range(step):
                self.assignments[-1].revert_assign()
                self.classes2assign.append(self.assignments.pop(-1))
            self.classes2assign.append(classes_)
        else:
            raise AssignError  # nie możliwe do przypisania mimo pustych planów zajęć

    def _reconstruction(self, classes_: Classes, step: int = 5):
        """
        Funkcja cofa określoną liczbę przypisań i dokonuje drobnej zmiany kolejności przy ponownym
         konstruowaniu rozwiązania
        :param classes_: nie przypisane zajęcia
        :param step: krok cofnięcia
        :return:
        """
        if bool(self.assignments):
            # cofnięcie o step przypisań
            self.classes2assign.append(classes_)
            for _ in range(step):
                if bool(self.assignments):
                    self.assignments[-1].revert_assign()
                    self.classes2assign.append(self.assignments.pop(-1))
                else:
                    break
            # zamiana kolejności losowych zajęć z listy do przypisania
            if len(self.assignments) > step:
                a, b = -step, randint(-step, -1)
            else:
                a, b = -len(self.assignments), randint(-len(self.assignments), -1)
            self.classes2assign[a], self.classes2assign[b] = self.classes2assign[b], self.classes2assign[a]
        else:
            raise AssignError

    def _replacing(self, classes_: Classes, room_manager: RoomManager):
        """
        Funkcja próbuje podmienić zajęcia, których nie udało się przypisać z zajęciami już przypisanymi
        :param classes_: zajęcia, których nie udało się przypisać
        :param room_manager: potrzebny do przypisania
        :return:
        """
        for idx, assigned_classes in enumerate(reversed(self.assignments)):
            time_assigned, room_assigned = assigned_classes.time, assigned_classes.room
            assigned_classes.revert_assign()
            best_time_generator = classes_.get_best_time_generator()
            for time in best_time_generator:
                avl_rooms = classes_.get_rooms()
                room = room_manager.get_best_room(avl_rooms, time)
                if room is not None:
                    classes_.assign(time, room)
                    self.register_assignment(classes_)
                    self.classes2assign.append(self.assignments.pop(-1 - idx))
                    return None
            assigned_classes.assign(time_assigned, room_assigned)
