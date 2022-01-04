# Structures files .csv
GROUPS_FILE = 'sample data/grupy.csv'
CLASSES_FILE = 'sample data/zajecia.csv'
ROOMS_FILE = 'sample data/sale.csv'
LECTURERS_FILE = 'sample data/prowadzacy.csv'

# weights
LECTURER_WEIGHT = 20  # waga istotnosci funkcji celu prowadzacego wzgledem studenta (waga studenta = 1)
FUN_WEIGHTS = (1, 1, 1, 1)  # wagi skladowych funkcji celu

# other parameters
SECTIONS_AMOUNT = 3
REASSIGN_TYPE = 'backtracking'  # backtracking/reconstruction/replacing
STEP = 15
MAX_ITER = 10
UTIME = 10  # jednostka czasu
