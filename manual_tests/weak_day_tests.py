from basic_structures import Exercises, ClassesID, Time, Hour
from structures import Group, Classes, Lecturer, Room
from week_day import WeekSchedule

cid = ClassesID(0)

l0 = Lecturer(0)
r0 = Room(0,
          availability=1000)
r1 = Room(1,
          availability=1200)
r0.potential_occupation_probability[cid] = 1
r1.potential_occupation_probability[cid] = 1

r0.add_const_potential_occupation_probability()
r1.add_const_potential_occupation_probability()

g0 = Group(0, 30)
g1 = Group(1, 25)

duration = 90

c0 = Classes(cid,
             lecturer=l0,
             duration=duration,
             rooms=[r0, r1],
             type_=Exercises(),
             groups=[g0, g1])

h1 = Hour(9, 30)
t1 = Time(0, h1, duration_mins=duration)  # do 11:

c0.assign(t1, r1)

w = WeekSchedule()
# assigning and availability
assert w.is_time_available(t1, 0)
# print(w.calc_goal_function())
w.assign(c0)

h2 = Hour(9, 00)
t2 = Time(0, h2, 30)
assert w.is_time_available(t2, 0)

t2 = Time(0, h2, 60)
assert not w.is_time_available(t2, 0)

t2 = Time(2, h2, 60)
assert w.is_time_available(t2, 0)

h2 = Hour(11, 00)
t2 = Time(0, h2, 60)
assert w.is_time_available(t2, 0)

c1 = Classes(cid,
             lecturer=l0,
             duration=duration,
             rooms=[r0, r1],
             type_=Exercises(),
             groups=[g0, g1])

try:
    c1.assign(t1, r1)
    assert False
except:
    pass

print("BEFORE REVERT:\n", w.print_schedule())

w.revert_assign(c0)

print("AFTER REVERT:\n",w.print_schedule())

h2 = Hour(9, 00)
t2 = Time(0, h2, 30)
assert w.is_time_available(t2, 0)

t2 = Time(0, h2, 60)
assert w.is_time_available(t2, 0)

t2 = Time(2, h2, 60)
assert w.is_time_available(t2, 0)

h2 = Hour(11, 00)
t2 = Time(0, h2, 60)
assert w.is_time_available(t2, 0)

w.assign(c1)







