from basic_structures import Exercises, ClassesID, Time, Hour
from structures import Classes, Lecturer, Group, Room

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

duration = 50

c0 = Classes(cid,
             lecturer=l0,
             duration=duration,
             rooms=[r0, r1],
             type_=Exercises(),
             groups=[g0, g1])

rooms = c0.get_rooms()
if len(rooms) != 2:
    assert False
for g in rooms:
    if not id(g) in (id(r1), id(r0)):
        assert False

groups = c0.get_groups()
if len(groups) != 2:
    assert False
for g in groups:
    if not id(g) in (id(g1), id(g0)):
        assert False

assert c0.get_duration() == duration

h1 = Hour(9, 30)
t1 = Time(0, h1, 60)
t2 = Time(0, h1, 50)

print(list(c0.get_best_time_generator()))

try:
    c0.assign(t1, r1)
    assert False
except ValueError:
    pass

c0.assign(t2, r1)
assert c0.time == t2
assert c0.room == r1

assert [0, 1] != c0._get_groups_ids()
print("PRINTING NAME:")
print(c0._get_name_info())
print("\nPRINTING CLASSES:")
print(c0.print("M"))
print("\nPRINTING SCHEDULE:")
print(g1.print_schedule())
c1 = Classes(cid,
             lecturer=l0,
             duration=duration,
             rooms=[r0, r1],
             type_=Exercises(),
             groups=[g0, g1])

print(list(c1.get_best_time_generator()))


c0.revert_assign()
assert c0.time is None
assert c0.room is None

c0.assign(t2, r1)
c0.revert_assign()



