#!/usr/bin/env python
# -*- coding: utf-8 -*-
# midi_gen.py in jupyter_notebook
# Created by yetongxue at 2020-12-17
import midi
import random

patten = midi.Pattern()
track = midi.Track()
patten.append(track)



def get_1(pitch):
    on = midi.NoteOnEvent(tick=0, velocity=100, pitch=pitch)
    off = midi.NoteOffEvent(tick=400, pitch=pitch)
    track.extend([on, off])


def get_22(pitch, pitch1):
    on = midi.NoteOnEvent(tick=0, velocity=85, pitch=pitch)
    off = midi.NoteOffEvent(tick=200, pitch=pitch)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=80, pitch=pitch1)
    off = midi.NoteOffEvent(tick=200, pitch=pitch1)
    track.extend([on, off])


def get_211(pitch, pitch1, pitch2):
    on = midi.NoteOnEvent(tick=0, velocity=90, pitch=pitch)
    off = midi.NoteOffEvent(tick=200, pitch=pitch)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=85, pitch=pitch1)
    off = midi.NoteOffEvent(tick=100, pitch=pitch1)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=80, pitch=pitch2)
    off = midi.NoteOffEvent(tick=100, pitch=pitch2)
    track.extend([on, off])


def get_112(pitch, pitch1, pitch2):
    on = midi.NoteOnEvent(tick=0, velocity=90, pitch=pitch)
    off = midi.NoteOffEvent(tick=100, pitch=pitch)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=85, pitch=pitch1)
    off = midi.NoteOffEvent(tick=100, pitch=pitch1)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=80, pitch=pitch2)
    off = midi.NoteOffEvent(tick=200, pitch=pitch2)
    track.extend([on, off])

def get_31(pitch, pitch1):
    on = midi.NoteOnEvent(tick=0, velocity=90, pitch=pitch)
    off = midi.NoteOffEvent(tick=300, pitch=pitch)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=85, pitch=pitch1)
    off = midi.NoteOffEvent(tick=100, pitch=pitch1)
    track.extend([on, off])

def get_13(pitch, pitch1):
    on = midi.NoteOnEvent(tick=0, velocity=85, pitch=pitch)
    off = midi.NoteOffEvent(tick=100, pitch=pitch1)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=90, pitch=pitch1)
    off = midi.NoteOffEvent(tick=300, pitch=pitch)
    track.extend([on, off])


def get_1111(pitch, pitch1, pitch2, patch3):
    on = midi.NoteOnEvent(tick=0, velocity=90, pitch=pitch)
    off = midi.NoteOffEvent(tick=100, pitch=pitch)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=85, pitch=pitch1)
    off = midi.NoteOffEvent(tick=100, pitch=pitch1)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=88, pitch=pitch2)
    off = midi.NoteOffEvent(tick=100, pitch=pitch2)
    track.extend([on, off])
    on = midi.NoteOnEvent(tick=0, velocity=83, pitch=patch3)
    off = midi.NoteOffEvent(tick=100, pitch=patch3)
    track.extend([on, off])


def main():
    container = []
    funcs = [get_1, get_1111, get_112, get_211, get_13, get_31, get_22]
    for index in range(3, 5):
        for name in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
            key = '{}_{}'.format(name, index)
            container.append(getattr(midi, key))
    for i in range(1000):
        func = random.choice(funcs)
        count = func.__code__.co_argcount
        level = random.choices(container, k=count)
        func(*level)
    # on = midi.NoteOnEvent(tick=0, velocity=50, pitch=midi.G_3)
    # off = midi.NoteOffEvent(tick=200, pitch=midi.G_3)
    # track.extend([on, off])
    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)
    midi.write_midifile('/Users/yetongxue/Downloads/example.mid', patten)


if __name__ == '__main__':
    main()
