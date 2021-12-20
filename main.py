from typing import Tuple

from scheduler.abstract_structures import RoomManager, ClassesManager
from structures import Classes, Group, Lecturer, Room
from utils import sort_classes, add_occupation, generate_groups, generate_classes, generate_lecturers, generate_rooms
from parameters import SECTIONS_AMOUNT, GROUPS_FILE, CLASSES_FILE, ROOMS_FILE, LECTURERS_FILE

lecturers: Tuple[Lecturer] = generate_lecturers(LECTURERS_FILE)
groups: Tuple[Group] = generate_groups(GROUPS_FILE)
rooms: Tuple[Room] = generate_rooms(ROOMS_FILE)
classes: Tuple[Classes] = generate_classes(CLASSES_FILE)

classes = sort_classes(classes, SECTIONS_AMOUNT)
add_occupation(rooms, classes)

room_manager = RoomManager(rooms)
classes_manager = ClassesManager(classes)


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











