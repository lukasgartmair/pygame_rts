#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 08:32:11 2023

@author: lukasgartmair
"""
import pygame
import os

VOLUME = 0.3

_sound_library = {}


def play_sound(path, loop=0):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace("/", os.sep).replace("\\", os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play(loop)


class Sound:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(VOLUME)

    def play_place_settlement(self):
        place_settlement_path = "sounds/place_settlement.wav"
        # play_sound(place_settlement_path, loop=0)

    def play_connect_settlement(self):
        place_settlement_path = "sounds/settlements_connect.wav"
        # play_sound(place_settlement_path, loop=0)

    def play_background_music_1(self):
        background_music_1_path = "sounds/background_music_1.wav"
        # play_sound(background_music_1_path, loop=-1)
