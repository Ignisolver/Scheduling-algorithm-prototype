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
        print("EMPTY:", path)


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


def _save_report(rooms, lecturers, groups, classes, assign_counter, can_not_assign_counter, assigned_number,
                 not_assigned_number, fail_cause, folder_path, fun_weights):
    fval = [0, 0, 0, 0, 0]  # F, FO, FD, FP, FR
    for le in lecturers:
        fval[1] += le.week_schedule.calc_week_FO()
        fval[2] += le.week_schedule.calc_week_FD()
        fval[3] += le.week_schedule.calc_week_FP(le.week_schedule.get_week_classes_time())
        fval[4] += le.week_schedule.calc_week_FR(le.week_schedule.get_week_classes_time(),
                                                 le.week_schedule.get_amount_of_free_days())
    for gr in groups:
        fval[1] += gr.week_schedule.calc_week_FO()
        fval[2] += gr.week_schedule.calc_week_FD()
        fval[3] += gr.week_schedule.calc_week_FP(gr.week_schedule.get_week_classes_time())
        fval[4] += gr.week_schedule.calc_week_FR(gr.week_schedule.get_week_classes_time(),
                                                 gr.week_schedule.get_amount_of_free_days())
    fval[0] = fun_weights[0] * fval[1] + fun_weights[1] * fval[2] + \
              fun_weights[2] * fval[3] + fun_weights[3] * fval[4]

    file_text = "Scheduler report \n" \
                "=============================== \n\n"

    with open('parameters.py') as f:
        lines = f.readlines()
        for line in lines:
            file_text += line

    file_text += "\n# --------------------INPUT DATA-----------------------\n"
    file_text += "Room number: {0} \n" \
                 "Lecturers number: {1} \n" \
                 "Groups number: {2} \n" \
                 "Classes number: {3} \n\n".format(len(rooms), len(lecturers), len(groups), len(classes))

    file_text += "\n# --------------------RESULTS-----------------------\n" \
                 "Assign counter: {0}\n" \
                 "Unassign counter: {1}\n" \
                 "Final number of assigned classes: {2}\n" \
                 "Final number of unassigned classes: {3}\n" \
                 "Final value of goal function: {4}\n" \
                 "FO: {5:.4f}, FD {6:.4f}, FP: {7:.4f}, FR: {8:.4f}\n\n" \
                 "Fail cause:\n" \
                 "Lecturer has no time: {9}\n" \
                 "Group has no time: {10}\n" \
                 "Room has no time: {11}".format(assign_counter, can_not_assign_counter, assigned_number,
                                                 not_assigned_number, fval[0], fval[1], fval[2], fval[3], fval[4],
                                                 fail_cause[0], fail_cause[1], can_not_assign_counter - sum(fail_cause))

    file_path = folder_path.joinpath("report.txt")
    with open(file_path, 'w') as f:
        f.write(file_text)
    return 1


def save_solution(rooms, lecturers, groups, classes, assign_counter, can_not_assign_counter, assign_number,
                  not_assigned_number, fail_cause, dir_name, fun_weights):
    print(f"creating report {dir_name}...")
    solution_dir_path = create_new_folder_for_result(dir_name)
    _save_report(rooms, lecturers, groups, classes, assign_counter, can_not_assign_counter, assign_number,
                 not_assigned_number, fail_cause, solution_dir_path, fun_weights)
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
