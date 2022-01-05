# Structures files .csv
GROUPS_FILE = 'sample data/grupy_baza.csv'
CLASSES_FILE = 'sample data/zajecia_baza.csv'
ROOMS_FILE = 'sample data/sale_baza.csv'
LECTURERS_FILE = 'sample data/prowadzacy_baza.csv'
RESULT_FOLDER_NAME = 'BASE'

# weights
LECTURER_WEIGHT = 20  # waga istotnosci funkcji celu prowadzacego wzgledem studenta (waga studenta = 1)
FUN_WEIGHTS = (1, 1, 1, 1)  # wagi skladowych funkcji celu (FO, FD, FP, FR) 

# other parameters
SECTIONS_AMOUNT = 3
REASSIGN_TYPE = 'backtracking'  # backtracking/reconstruction/replacing
STEP = 15
MAX_ITER = 1000
UTIME = 10  # jednostka czasu
