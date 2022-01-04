from typing import Tuple, TYPE_CHECKING

from parameters import SECTIONS_AMOUNT, GROUPS_FILE, CLASSES_FILE, ROOMS_FILE, LECTURERS_FILE, \
    REASSIGN_TYPE, STEP, MAX_ITER
from solution_saver import save_solution
from utils import sort_classes, add_occupation, generate_groups, generate_classes, generate_lecturers, generate_rooms
from abstract_structures import RoomManager, ClassesManager

if TYPE_CHECKING:
    from structures import Classes, Group, Lecturer, Room


def main():
    can_not_assign_counter = 0
    assign_counter = 0

    lecturers: Tuple["Lecturer"] = generate_lecturers(LECTURERS_FILE)
    groups: Tuple["Group"] = generate_groups(GROUPS_FILE)
    rooms: Tuple["Room"] = generate_rooms(ROOMS_FILE)
    classes: Tuple["Classes"] = generate_classes(CLASSES_FILE, lecturers, groups, rooms)

    classes = sort_classes(classes, SECTIONS_AMOUNT)
    add_occupation(rooms, classes)

    room_manager = RoomManager(rooms)
    classes_manager = ClassesManager(classes)

    while classes_ := classes_manager.get_next_classes():
        best_time_generator = classes_.get_best_time_generator()
        for time in best_time_generator:
            avl_rooms = classes_.get_rooms()
            room = room_manager.get_best_room(avl_rooms, time)
            if room is not None:
                classes_.assign(time, room)
                classes_manager.register_assignment(classes_)
                assign_counter += 1
                break
        else:
            if can_not_assign_counter < MAX_ITER:
                can_not_assign_counter += 1
            else:
                print("algorithm couldn't find solution in defined number of iteration")
                break
            classes_manager.can_not_assign(classes_, REASSIGN_TYPE, STEP, rm=room_manager)

    save_solution(lecturers, "lecturers")
    save_solution(groups, "groups")
    save_solution(rooms, "rooms")


if __name__ == "__main__":
    main()
