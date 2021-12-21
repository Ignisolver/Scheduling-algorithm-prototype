from typing import Tuple, List
from random import randint

from scheduler.basic_structures import Time, NoRoomAvailable, AssignError
from scheduler.constans import STARTOFDAY, ENDOFDAY, UTIME
from scheduler.structures import Classes, Room
from utils import fun_of_gap


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
        available_rooms_sections = [[] for _ in range(fun_of_gap(0, True))]
        for room in available_rooms:
            fgap = fun_of_gap(sum(self.availability_of_room_around_time(room, time)))
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

    def availability_of_room_around_time(self, room, time):
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
        return time - last_end_before, first_start_after - time


# todo sprawdzić
class ClassesManager:
    def __init__(self, classes: Tuple[Classes]):
        self.assignments: List[Classes] = []
        self.classes2assign: List[Classes] = list(classes)
        self.not_assigned: List[Classes] = []

    def get_next_classes(self) -> Classes:
        return self.classes2assign.pop(-1)

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
        Funkcja cofa określoną liczbę przypisań i dokonuje drobnej zmiany kolejności przy ponownym konstruowaniu rozwiązania
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
                a, b = randint(-step, -1), randint(-step, -1)
            else:
                a, b = randint(-len(self.assignments), -1), randint(-len(self.assignments), -1)
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
            assigned_classes.revert_assign()
            best_time_generator = classes_.get_best_time_generator()
            for time in best_time_generator:
                avl_rooms = classes_.get_rooms()
                room = room_manager.get_best_room(avl_rooms, time)
                if room is not None:
                    classes_.assign(time, room)
                    self.register_assignment(classes_)
                    self.classes2assign.append(self.assignments.pop(-1 - idx))
                    break
