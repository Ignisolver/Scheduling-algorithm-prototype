import os
from os import system
from pathlib import Path
from typing import Tuple

from structures import WithSchedule


def get_path(dir_name, file_name, rel_path):
    file_relative_path = f'results/{dir_name}/{file_name}'
    path = rel_path.joinpath(file_relative_path)
    return path


def save_yaml(path: Path, text):
    path = path.with_suffix(".yaml")
    with open(path, 'w') as file:
        file.write(text)


def save_pdf(path: Path):
    yaml_path = path.with_suffix(".yaml")
    pdf_path = path.with_suffix(".pdf")
    ret = system(f'py -3.9 -m pdfschedule --no-weekends "{yaml_path}" "{pdf_path}"')
    if ret != 0:
        print(path)


def create_new_folder_for_result(folder_name):
    sch_path = get_scheduler_path()
    specific_results_path = sch_path.joinpath(f"results/{folder_name}")
    os.mkdir(specific_results_path)
    for name in ("lecturers", "groups", "rooms"):
        path = specific_results_path.joinpath(name)
        os.mkdir(path)
    return specific_results_path


def get_scheduler_path():
    return Path(__file__).parent.resolve()


def _save_report(rooms, lecturers, groups, classes, assign_counter, can_not_assign_counter, not_assigned_number,
                 folder_path):
    fval = 0
    for ro in rooms:
        fval += ro.week_schedule.calc_goal_function()
    for le in lecturers:
        fval += le.week_schedule.calc_goal_function()
    for gr in groups:
        fval += gr.week_schedule.calc_goal_function()
    file_text = "Scheduler report \n" \
                "=============================== \n\n"
    file_text += "Input data info: \n" \
                 "Room number: {0} \n" \
                 "Lecturers number: {1} \n" \
                 "Groups number: {2} \n" \
                 "Classes number: {3} \n\n".format(len(rooms), len(lecturers), len(groups), len(classes))

    file_text += "----------------------------- \n\n" \
                 "Parameters:\n"
    with open('parameters.py') as f:
        lines = f.readlines()
        for line in lines:
            file_text += line

    file_text += "\n-------------------------------\n" \
                 "Solving properties\n" \
                 "assign counter: {0}\n" \
                 "unassign counter: {1}\n" \
                 "final number of unassigned classes: {2}\n" \
                 "final value of goal function: {3}\n".format(assign_counter, can_not_assign_counter,
                                                              not_assigned_number, fval)

    file_path = folder_path.joinpath("report.txt")
    with open(file_path, 'w') as f:
        f.write(file_text)
    return 1


def save_solution(rooms, lecturers, groups, classes, assign_counter, can_not_assign_counter, not_assigned_number,
                  dir_name):
    print("creating report...")
    solution_dir_path = create_new_folder_for_result(dir_name)
    _save_report(rooms, lecturers, groups, classes, assign_counter, can_not_assign_counter, not_assigned_number,
                 solution_dir_path)
    _save_solution(lecturers, solution_dir_path, "lecturers")
    _save_solution(groups, solution_dir_path, "groups")
    _save_solution(rooms, solution_dir_path, "rooms")


def _save_solution(planned_group: Tuple[WithSchedule], solution_dir_path, type_dir_name):

    for planned in planned_group:
        group_folder_path = solution_dir_path.joinpath(type_dir_name)
        file_path = group_folder_path.joinpath(str(planned.id_))
        text = planned.print_schedule()
        save_yaml(file_path, text)
        save_pdf(file_path)


def clean_up_results():
    scheduler_path = get_scheduler_path()
    results_path = scheduler_path.joinpath("results")
    for folder in results_path.iterdir():
        os.remove(folder)


