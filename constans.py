from scheduler.basic_structures import Hour

UTIME = 10  # jednostka czasu
STARTOFDAY = Hour(8, 00)  # od której mogą zaczynać się zajęcia
ENDOFDAY = Hour(18, 00)  # do której najpóźniej mogą być zajęcia
MIN_CLASS_DURATION = 90
MIN_OK_BRAKE = 90 + 2 * UTIME

