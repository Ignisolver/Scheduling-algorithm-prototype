from types import Union

from structures import GlobalSchedule, Lecturer, Group, Room, Lecture, Field


def get_id():
    i = 0
    while True:
        yield i
        i += 1


def calc_goal_function(schedule: GlobalSchedule):
    goal_fcn_val = 0
    for group in schedule.groups:
        gr_gaol_fcn_val = group.week_schedule.calc_goal_function()
        goal_fcn_val += gr_gaol_fcn_val * len(group.students_ids)

    for lecturer in schedule.lecturers:
        goal_fcn_val += lecturer.week_schedule.calc_goal_function()

    return goal_fcn_val


def check_capacity_sufficiency(group: Group, room: Room):
    pass


def check_all_group_in_lecture(lecture: Lecture, field: Field):
    pass

