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
    system(f'py -3.9 -m pdfschedule --no-weekends"{yaml_path}" "{pdf_path}"')


def save_solution(planned_group: Tuple[WithSchedule], dir_name):
    rel_path = Path(__file__).parent.resolve()  # scheduler
    for planned in planned_group:
        path = get_path(dir_name, str(planned.id_), rel_path)
        text = planned.print_schedule()
        save_yaml(path, text)
        save_pdf(path)


def clean_up_results():
    scheduler_path = Path(__file__).parent.resolve()
    scheduler_path = scheduler_path.joinpath("results")
    for folder in scheduler_path.iterdir():
        for file in folder.iterdir():
            if file.match("*.pdf") or file.match("*.yaml"):
                os.remove(file)
