from typing import Tuple

from scheduler.structures import RoomManager, NoRoomAvailable, NoAvailableTime, Registrar, LecturerError, RoomError
from structures import Subject, Classes, Group, Lecturer, Room
from utils import generate_classes, sort_classes, add_occupation

SECTIONS_AMOUNT = 3

lecturers: Tuple[Lecturer] = ...
groups: Tuple[Group] = ...
subjects: Tuple[Subject] = ...
rooms: Tuple[Room] = ...
classes: Tuple[Classes] = generate_classes(subjects)

classes = sort_classes(classes, SECTIONS_AMOUNT)
add_occupation(rooms, classes)

room_manager = RoomManager(rooms)
register = Registrar()



"""
znajdź pierwsze minimum funkcji celu
sprawdź czy może prowadzący
    jak nie weź kolejne minimum
wybierze najlepszą salę
    jak nie ma wolnych weź kolejne minimum
przypisz
"""

class_nr = 0
while True:
    if class_nr > len(classes):
        break

    class_: Classes = classes[class_nr]
    time = class_.get_best_time()
    error_cause = None

    while True:
        try:
            time = class_.get_best_time(next_=True)  # coś nie tak
        except NoAvailableTime:
            register.revert_assignments(error_cause)
            class_nr = register.get_current_class_number()

        if not class_.is_lecturer_available(time):
            error_cause = LecturerError
            continue

        try:
            room = room_manager.get_best_room(class_.available_rooms, time)
        except NoRoomAvailable:
            error_cause = RoomError
            continue

        class_.assign(time, room)
        register.register_assignment(class_)
        class_nr += 1
        break





