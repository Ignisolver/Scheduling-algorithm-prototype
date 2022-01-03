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
czt = 2 * int(ENDOFDAY - STARTOFDAY) + 3 * MIN_CLASS_DURATION  # dwa dni od rana do wieczora
MAX_FR = 2 * (int(ENDOFDAY - STARTOFDAY) - czt) + 3 * (MIN_CLASS_DURATION - czt)  # i trzy dni po jednych zajęciach

DAY_LETTER = dict(zip(range(5), "MTWRF"))

COLORS = ['edc9cd', '1d6c2b', '1f08b0', 'a3c1ad', 'e35259', '22b4b7', '4d5d53', 'bcbbff', '4d5d53', '96c8a2',
           'efdfbb', '8fbc8f', 'bdb76b', 'fffdd0', 'eee8cd', '8c92ac', 'f7e7ce', 'ace1af', '78866b', 'a3c1ad',
           '669999', 'eeeed1', 'd8d1b0', '090088', 'c6c1b9', '003da6', '362d17', '01e1ec', '5e8d63', '002060',
           'ffc000', '54d157', 'ff9400', 'c22c4e', '5faca1', 'b1044f', '541d8b', 'e82cb5', '14b437', '7a0c72',
           '79eb00', '412c39']


