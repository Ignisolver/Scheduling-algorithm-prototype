from basic_structures import Lecture, Exercises, ClassesID
from scheduler.structures import Classes, Lecturer, Group, Room

l0 =Lecturer(0)
r0 = Room(0,
          availability=1000)
r1 = Room(1,
          availability=1200)
g0 = Group(0, 30)
g1 = Group(1, 25)

c0 = Classes(ClassesID(0),
             lecturer=l0,
             duration=50,
             rooms=[r0, r1],
             type_=Exercises(),
             groups=[g0, g1])