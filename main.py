from typing import Tuple

from structures import Subject, Classes, Group, Lecturer, Room
from utils import generate_classes, sort_classes, add_occupation

lecturers: Tuple[Lecturer] = ...
groups: Tuple[Group] = ...
subjects: Tuple[Subject] = ...
rooms: Tuple[Room] = ...
classes: Tuple[Classes] = generate_classes(subjects)

classes = sort_classes(classes)
add_occupation(rooms, classes)


