from typing import Tuple

from scheduler.abstract_structures import RoomManager, ClassesManager
from structures import Classes, Group, Lecturer, Room
from utils import sort_classes, add_occupation

SECTIONS_AMOUNT = 3

lecturers: Tuple[Lecturer] = ...
groups: Tuple[Group] = ...
rooms: Tuple[Room] = ...
classes: Tuple[Classes] = ...

classes = sort_classes(classes, SECTIONS_AMOUNT)
add_occupation(rooms, classes)

room_manager = RoomManager(rooms)
classes_manager = ClassesManager()


"""
znajdź pierwsze minimum funkcji celu
sprawdź czy może prowadzący
    jak nie weź kolejne minimum
wybierze najlepszą salę
    jak nie ma wolnych weź kolejne minimum
przypisz
"""


while classes_ := classes_manager.get_next_classes():
    best_time_generator = classes_.get_best_time_generator()
    for time in best_time_generator:
        avl_rooms = classes_.get_rooms()
        room = room_manager.get_best_room(rooms, time)
        if room is not None:
            classes_.assign(time, room)
            classes_manager.register_assignment(classes_)
            break
    else:
        classes_manager.can_not_assign(classes_)











