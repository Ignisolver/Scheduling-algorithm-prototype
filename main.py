from time import sleep
from typing import Tuple, TYPE_CHECKING
from importlib import reload
import parameters
reload(parameters)
SECTIONS_AMOUNT = parameters.SECTIONS_AMOUNT
GROUPS_FILE = parameters.GROUPS_FILE
CLASSES_FILE = parameters.CLASSES_FILE
ROOMS_FILE = parameters.ROOMS_FILE
LECTURERS_FILE = parameters.LECTURERS_FILE
REASSIGN_TYPE = parameters.REASSIGN_TYPE
STEP = parameters.STEP
MAX_ITER = parameters.MAX_ITER
RESULT_FOLDER_NAME = parameters.RESULT_FOLDER_NAME
FUN_WEIGHTS = parameters.FUN_WEIGHTS

from solution_saver import save_solution
from utils import sort_classes, add_occupation, generate_groups, generate_classes, generate_lecturers, \
    generate_rooms
from abstract_structures import RoomManager, ClassesManager

if TYPE_CHECKING:
    from structures import Classes, Group, Lecturer, Room


def main():
    print("Generating...")
    can_not_assign_counter = 0
    assign_counter = 0
    lecturer_has_no_time = 0
    group_has_no_time = 0

    #print("Generating data...")
    lecturers: Tuple["Lecturer"] = generate_lecturers(LECTURERS_FILE)
    groups: Tuple["Group"] = generate_groups(GROUPS_FILE)
    rooms: Tuple["Room"] = generate_rooms(ROOMS_FILE)
    classes: Tuple["Classes"] = generate_classes(CLASSES_FILE, lecturers, groups, rooms)

    #print("Preparing data...")
    classes = sort_classes(classes, SECTIONS_AMOUNT)
    add_occupation(rooms, classes)

    #print("Initializing needed objects")
    room_manager = RoomManager(rooms)
    classes_manager = ClassesManager(classes)
    print("Algorithm...")
    # print("Starting main algorithm loop...")
    while classes_ := classes_manager.get_next_classes():
        #print("Obtaining best time generator...")
        best_time_generator, flag = classes_.get_best_time_generator()
        if flag == -1:
            lecturer_has_no_time += 1
            #print("Lecturer has no time")
        elif flag == -2:
            group_has_no_time += 1
            #print("Group has no time")
        #print("Best time generator obtained.")
        for time in best_time_generator:
            #print("Got next best time.")
            #print("Receiving available rooms...")
            avl_rooms = classes_.get_rooms()
            #print("Available rooms received.")
            #print("Looking for best room...")
            room = room_manager.get_best_room(avl_rooms, time)
            if room is not None:
                #print("Best room found.")
                #print("Assigning classes...")
                classes_.assign(time, room)
                #print("Classes assigned.")
                #print("Registering assignment...")
                classes_manager.register_assignment(classes_)
                #print("Assignment registered.")
                assign_counter += 1
                #print(assign_counter)
                break
        else:
            #print("Available room NOT found :(")
            if can_not_assign_counter < MAX_ITER:
                #print("Trying again...")
                can_not_assign_counter += 1
                #print(can_not_assign_counter)
            else:
                #print("algorithm couldn't find solution in defined number of iteration")
                break
            classes_manager.can_not_assign(classes_, REASSIGN_TYPE, STEP, rm=room_manager)

    #print("clean up previous solution")
    save_solution(rooms, lecturers, groups, classes, assign_counter, can_not_assign_counter,
                  classes_manager.get_assigned_number(), classes_manager.get_not_assigned_number(),
                  (lecturer_has_no_time, group_has_no_time), RESULT_FOLDER_NAME, FUN_WEIGHTS)
    #print("ALL DONE!")


if __name__ == "__main__":
    main()
