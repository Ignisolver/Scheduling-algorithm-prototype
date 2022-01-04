from scheduler.basic_structures import Hour, Time
# HOUR -----------------------------

# add
h1 = Hour(8, 20)
h2 = h1 + 40
assert h2 == Hour(9, 0)
h2 = h1 + 130
assert h2 == Hour(10, 30)
# int
assert int(h1) == 8*60+20
# compare
assert Hour(8, 10) < Hour(8, 20)
assert Hour(8, 20) < Hour(9, 10)
assert Hour(8, 10) <= Hour(8, 10)
assert Hour(8, 10) >= Hour(8, 10)
assert Hour(8, 10) == Hour(8, 10)
assert Hour(8, 10) < Hour(9, 10)
assert Hour(8, 10) < Hour(9, 10)
# sub
assert Hour(8, 10) - Hour(8, 10) == 0
assert Hour(9, 10) - Hour(8, 00) == 70
assert Hour(8, 10) - Hour(9, 00) == -50

# TIME --------------------------------
hs = Hour(10, 00)
t1 = Time(1, hs, 60)  # 10 - 11
hours = [(Hour(9, 00),{"cross": [90,120,150], "no_cross": [10,30,60]}),
         (Hour(9, 30),{"cross": [60,90,120,150], "no_cross": [10,30]}),
         (Hour(10, 00),{"cross": [10,30,60,90,120,150], "no_cross": []}),
         (Hour(10, 30),{"cross": [10,30,60,90,120,150], "no_cross": []}),
         (Hour(11, 00),{"cross": [], "no_cross": [10,30,60,90,120,150]}),
         (Hour(11, 30),{"cross": [], "no_cross": [10,30,60,90,120,150]})]

# crossing without brake
for hour, durs in hours:
    for dur in durs["cross"]:
        t2 = Time(1, hour, dur)
        if not t1.cross(t2):
            print(t1, t2)
            assert False
    for dur in durs["no_cross"]:
        t2 = Time(1, hour, dur)
        if t1.cross(t2):
            print(t1, t2)
            assert False

# cross with brake
brake = 30
hours = [(Hour(8, 30),{"cross": [90,120,150,180,210], "no_cross": [10,30,60]}),
         (Hour(9, 00),{"cross": [60,90,120,150,180,210], "no_cross": [10,30]}),
         (Hour(9, 30),{"cross": [10,30,60,90,120,150,180,210], "no_cross": []}),
         (Hour(10, 00),{"cross": [10,30,60,90,120,150,180,210], "no_cross": []}),
         (Hour(10, 30),{"cross": [10,30,60,90,120,150,180,210], "no_cross": []}),
         (Hour(11, 00),{"cross": [10,30,60,90,120,150,180,210], "no_cross": []}),
         (Hour(11, 30),{"cross": [], "no_cross": [10,30,60,90,120,150,180,210]}),
         (Hour(12, 00),{"cross": [], "no_cross": [10,30,60,90,120,150,180,210]})]

for hour, durs in hours:
    for dur in durs["cross"]:
        t2 = Time(1, hour, dur)
        if not t1.cross(t2, brake=brake):
            print(t1, t2)
            assert False
    for dur in durs["no_cross"]:
        t2 = Time(1, hour, dur)
        if t1.cross(t2, brake=brake):
            print(t1, t2)
            assert False


