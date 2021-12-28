from basic_structures import Hour
from parameters import WEIGHTS_FD, PERFECT_TIME

UTIME = 10  # jednostka czasu
STARTOFDAY = Hour(8, 00)  # od której mogą zaczynać się zajęcia
ENDOFDAY = Hour(18, 00)  # do której najpóźniej mogą być zajęcia
MIN_CLASS_DURATION = 90
MIN_OK_BRAKE = 90 + 2 * UTIME
PERFECT_TIME_A = Hour(PERFECT_TIME[0][0], PERFECT_TIME[0][1])
PERFECT_TIME_B = Hour(PERFECT_TIME[1][0], PERFECT_TIME[1][1])

MAX_FO = 5 * (int(ENDOFDAY - STARTOFDAY) - (2 * MIN_CLASS_DURATION) - (2 * UTIME)) / 2  # jedne zajęcia rano i wieczorem
MAX_FD = sum(WEIGHTS_FD)
MAX_FP = 5 / MIN_CLASS_DURATION  # max funkcji pory / najkrótszy czas zajęć
czt = 2 * int(ENDOFDAY - STARTOFDAY) + 3 * MIN_CLASS_DURATION                     # dwa dni od rana do wieczora
MAX_FR = 2 * (int(ENDOFDAY - STARTOFDAY) - czt) + 3 * (MIN_CLASS_DURATION - czt)  # i trzy dni po jednych zajęciach
