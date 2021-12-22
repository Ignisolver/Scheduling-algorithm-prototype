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
        self.hour = hour
        self.minute = minute

    def __int__(self):
        return self.hour * 60 + self.minute

    def __add__(self, other):
        if isinstance(other, int):
            hours2add = int(other / 60)
            mins2add = int(other % 60)

            hour = self.hour + hours2add
            minute = self.minute + mins2add

            if minute > 60:
                minute = minute % 60
                over_hours = int(minute / 60)
                hour += over_hours

            if hour > 24:
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


class Time:
    def __init__(self, day_nr, start: Hour, duration_mins: int):
        self.day_nr = day_nr
        self.start = start
        self.end = start + duration_mins
        self.duration = duration_mins

    def cross(self, other: Time, break_=0):
        """
        True jak koliduje ( z przerwami włącznie )
        False jak nie koliduje
        :return:
        """
        if self.start-break_ < other.start < self.end + break_:
            return False
        if self.start-break_ < other.end < self.end + break_:
            return False
        if self.start < other.start and other.end < self.end:
            return False
        if other.start < self.start and self.end < other.end:
            return False
        return True
