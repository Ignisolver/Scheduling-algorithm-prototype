# Structures files .csv
GROUPS_FILE = "sample data/grupy.csv"
CLASSES_FILE = "sample data/zajecia.csv"
ROOMS_FILE = "sample data/sale.csv"
LECTURERS_FILE = "sample data/prowadzacy.csv"

# weights
LECTURER_WEIGHT = 20  # waga istotności funkcji celu prowadzącego względem studenta (waga studenta = 1)
FUN_WEIGHTS = (1, 1, 1, 1)  # wagi składowych funkcji celu
WEIGHTS_FD = (3, 2, 1, 2, 3)
PERFECT_TIME = ((8, 00), (12, 00))  # godziny między którymi FP przyjmuje wartość 0

# other parameters
SECTIONS_AMOUNT = 3
REASSIGN_TYPE = "backtracking"  # backtracking/reconstruction/replacing
STEP = 15
MAX_ITER = 10
UTIME = 10  # jednostka czasu