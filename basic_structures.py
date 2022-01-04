from __future__ import annotations


class ClassesID(int):
    pass


class RoomID(int):
    pass


class LecturerError:
    pass


class RoomError:
    pass


class Lecture:
    pass


class Exercises:
    pass


class NoRoomAvailable(Exception):
    def __init__(self):
        super().__init__()


class NoAvailableTime(Exception):
    def __init__(self):
        super().__init__()


class AssignError(Exception):
    def __init__(self):
        super().__init__()


class CrossException(Exception):
    def __init__(self):
        super().__init__()


class Hour:
    def __init__(self, hour, minute):
        if hour > 23 or minute > 59:
            raise ValueError("Invalid hour format")
        self.hour = hour
        self.minute = minute

    def __int__(self):
        return self.hour * 60 + self.minute

    def __eq__(self, other):
        if isinstance(self, type(other)):
            if self.hour == other.hour:
                if self.minute == other.minute:
                    return True
        return False

    def __add__(self, other):
        if isinstance(other, int):
            hours2add = int(other / 60)
            mins2add = int(other % 60)

            hour = self.hour + hours2add
            minute = self.minute + mins2add

            if minute >= 60:
                over_hours = int(minute / 60)
                minute = minute % 60
                hour += over_hours

            if hour >= 24:
                raise Exception

            return Hour(hour, minute)

    def __lt__(self, other):
        if isinstance(other, Hour):
            if self.hour == other.hour:
                return self.minute < other.minute
            return self.hour < other.hour

    def __le__(self, other):
        if isinstance(other, Hour):
            if self.hour == other.hour:
                return self.minute <= other.minute
            return self.hour <= other.hour

    def __sub__(self, other):
        if isinstance(other, Hour):
            return 60 * (self.hour - other.hour) + self.minute - other.minute

        if isinstance(other, int):
            hours2sub = int(other / 60)
            mins2sub = int(other % 60)

            hour = self.hour
            minute = self.minute

            if mins2sub > minute:
                minute += 60
                hour -= 1

            hour = hour - hours2sub
            minute = minute - mins2sub

            return Hour(hour, minute)

    def __repr__(self):
        return f"{self.hour}:{self.minute:02d}"


class Time:
    def __init__(self, day_nr, start: Hour, duration_mins: int):
        if day_nr not in (0,1,2,3,4):
            raise ValueError("Invalid day nr")
        self.day_nr = day_nr
        self.start = start
        self.end = start + duration_mins
        self.duration = duration_mins
        self.mark = ...

    def __repr__(self):
        return str(self.start) + " - " + str(self.end)

    def cross(self, other: Time, brake=0):
        """
        True jak koliduje ( z przerwami włącznie )
        False jak nie koliduje
        :return:
        """
        if self.start-brake < other.start < self.end + brake:
            return True
        if self.start-brake < other.end < self.end + brake:
            return True
        if self.start <= other.start and other.end <= self.end:
            return True
        if other.start <= self.start and self.end <= other.end:
            return True
        return False
