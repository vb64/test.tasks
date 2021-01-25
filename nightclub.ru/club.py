"""
Implementation for test task 'nightclub emulator'
(C) 2016 by Vitaly Bogomolov mail@vitaly-bogomolov.ru
python -m flake8 --max-line-length=120 club.py
install (need msgfmt):
> make
run:
> python club.py
> python club.py ru
"""

import sys
import gettext
from random import shuffle, choice, sample, randint


class Movement:
    HALF_CROUNCH = 'half crouch'
    IN_RHYTHM = 'in rhythm'
    SMOOTH = 'smooth move'
    BACK_AND_FORTH = 'back and forth'
    ELBOWS = 'bent at the elbows'
    CIRCULAR = 'circular movements'
    FIXED = 'fixed'
    # FUTURE = 'shakes kokoshnik'


class Dance(object):
    LEGS = "legs"
    HANDS = "hands"
    HEAD = "head"
    BODY = "body"

    def __init__(self, legs=[], hands=[], head=[], body=[]):
        self.movements = {
            Dance.LEGS: legs,
            Dance.HANDS: hands,
            Dance.HEAD: head,
            Dance.BODY: body,
        }


class Dancer(object):

    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

    def __unicode__(self):
        return "%s: %s" % (self.name, ", ".join([_(x) for x in self.skills]))

    def __str__(self):
        return "%s" % self.__unicode__()

    def movements(self, dance_name):
        if dance_name not in self.skills:
            return _("drinking vodka") if self.name != "Vitaly" else _("writing code")

        dance = dances[dance_name]
        keys = dance.movements.keys()
        # we don't need the uniform dances, every dance must be individual
        shuffle(keys)
        result = []
        for key in keys:
            movements = dance.movements[key]
            if movements:
                result.append("%s: %s" % (_(key), ", ".join([_(x) for x in movements])))

        return "; ".join(result)

    @staticmethod
    def group(names, styles):
        l = len(styles)
        for name in names:
            yield Dancer(name, sample(styles, randint(1, l)))


dances = {

    "electrodance": Dance(
        legs=[Movement.IN_RHYTHM],
        hands=[Movement.CIRCULAR],
        head=[Movement.FIXED],
        body=[Movement.BACK_AND_FORTH]
    ),

    "hip-hop": Dance(
        body=[Movement.BACK_AND_FORTH],
        head=[Movement.BACK_AND_FORTH],
        hands=[Movement.ELBOWS],
        legs=[Movement.HALF_CROUNCH]
    ),

    "pop": Dance(
        body=[Movement.SMOOTH],
        head=[Movement.SMOOTH],
        hands=[Movement.SMOOTH],
        legs=[Movement.SMOOTH]
    ),

    # "future": Dance(head=[Movement.FUTURE]),
}


def songs(number, styles):
    for n in xrange(number):
        yield ("Track%d" % (n+1), choice(styles))


def main():

    # need for console output in different locales
    def u(msg):
        # return msg
        return unicode(msg.decode('utf-8'))

    print u(_("let's start the party!")), "\n"

    dancers = []
    styles = dances.keys()
    names = (
        "Vitaly",
        "Aida",
        "Natalya",
        "Ruslan",
        "Konstantin",
        "Adel",
    )

    for dancer in Dancer.group(names, styles):
        print u("%s" % dancer)
        dancers.append(dancer)

    for song, style in songs(3, styles):
        print "\n", u(_("now playing: %s (%s)") % (song, _(style))), "\n"
        for dancer in dancers:
            print dancer.name, u(dancer.movements(style))

    print "\n", u(_("party's over"))


if __name__ == "__main__":

    l = []
    if len(sys.argv) > 1:
        l = [sys.argv[1]]

    try:
        gettext.translation('messages', './locale', languages=l).install()
    except IOError:
        def _(msg):
            return msg

    main()
