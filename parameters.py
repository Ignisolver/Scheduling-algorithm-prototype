# Structures files .csv
GROUPS_FILE = 'sample data/grupy_baza.csv'
CLASSES_FILE = 'sample data/zajecia_baza.csv'
ROOMS_FILE = 'sample data/sale_baza.csv'
LECTURERS_FILE = 'sample data/prowadzacy_baza.csv'
RESULT_FOLDER_NAME = 'BASE'
GENERATE_REPORT = 2  #  0: nie zwraca nic, 1: generuje tylko raport, 2: generuje raport i rozwiazania

# weights
LECTURER_WEIGHT = 20  # waga istotnosci funkcji celu prowadzacego wzgledem studenta (waga studenta = 1)
FUN_WEIGHTS = (1, 1, 1, 1)  # wagi skladowych funkcji celu (FO, FD, FP, FR) 

# other parameters
SECTIONS_AMOUNT = 3
REASSIGN_TYPE = 'ignore'  # backtracking/reconstruction/replacing/ignore
STEP = 15
MAX_FAIL = 3
UTIME = 10  # jednostka czasu
