from typing import Tuple, TYPE_CHECKING
from logging import getLogger

from parameters import SECTIONS_AMOUNT, GROUPS_FILE, CLASSES_FILE, ROOMS_FILE, LECTURERS_FILE, \
    REASSIGN_TYPE, STEP, MAX_ITER
from solution_saver import save_solution, clean_up_results
from utils import sort_classes, add_occupation, generate_groups, generate_classes, generate_lecturers, generate_rooms
from abstract_structures import RoomManager, ClassesManager

if TYPE_CHECKING:
    from structures import Classes, Group, Lecturer, Room


def main():
    can_not_assign_counter = 0
    assign_counter = 0
    print("Generating data...")
    lecturers: Tuple["Lecturer"] = generate_lecturers(LECTURERS_FILE)
    groups: Tuple["Group"] = generate_groups(GROUPS_FILE)
    rooms: Tuple["Room"] = generate_rooms(ROOMS_FILE)
    classes: Tuple["Classes"] = generate_classes(CLASSES_FILE, lecturers, groups, rooms)
    print("Preparing data...")
    classes = sort_classes(classes, SECTIONS_AMOUNT)
    add_occupation(rooms, classes)
    print("Initializing needed objects")
    room_manager = RoomManager(rooms)
    classes_manager = ClassesManager(classes)
    print("Starting main algorithm loop...")
    while classes_ := classes_manager.get_next_classes():
        print("Assigning classes with id:", classes_.id_)
        print("Obtaining best time generator...")
        best_time_generator = classes_.get_best_time_generator()
        print("Best time generator obtained.")
        for time in best_time_generator:
            print("Got next best time.")
            print("Receiving available rooms...")
            avl_rooms = classes_.get_rooms()
            print("Available rooms received.")
            print("Looking for best room...")
            room = room_manager.get_best_room(avl_rooms, time)
            if room is not None:
                print("Best room found.")
                print("Assigning classes...")
                classes_.assign(time, room)
                print("Classes assigned.")
                print("Registering assignment...")
                classes_manager.register_assignment(classes_)
                print("Assignment registered.")
                assign_counter += 1
                break
        else:
            print("Available room NOT found :(")
            if can_not_assign_counter < MAX_ITER:
                print("Trying again...")
                can_not_assign_counter += 1
            else:
                print("algorithm couldn't find solution in defined number of iteration")
                break
            classes_manager.can_not_assign(classes_, REASSIGN_TYPE, STEP, rm=room_manager)
    print("clean up previous solution")
    clean_up_results()
    print("printing solution...")
    save_solution(lecturers, "lecturers")
    save_solution(groups, "groups")
    save_solution(rooms, "rooms")
    print("ALL DONE!")


if __name__ == "__main__":
    main()
