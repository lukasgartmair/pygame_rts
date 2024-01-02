#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:42:52 2024

@author: lukasgartmair
"""

import pygame
import particle
from colors import settlement_stats_colors

class Animation:
    def __init__(self):

        self.particle_animation = True
        self.particle_system_form = particle.ParticleSystemForm()
        if  self.particle_animation:
            self.particle = particle.Particle(self.particle_system_form)
            self.particle.max_animation_duration = 100
        self.animation_object = None
        self.alpha_fully_transparent = 0
        self.alpha_transparency = 75
        self.alpha_non_transparent = 190

        self.last_animation_time = 0
        self.current_time = 0
        self.animation_index = 0
        self.animation_delay = 0

    def check_animation_trigger(self):
        trigger = False
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_animation_time >= self.animation_delay:
            self.last_animation_time = self.current_time
            trigger = True
        return trigger

    def animate_particle_effect(self):

        self.particle.update()
        self.particle.emit_particles(self.animation_object.render_center)

        self.particle.render(self.screen)

    def animate(self, screen, animation_object):

        self.screen = screen
        self.animation_object = animation_object

        if self.particle_animation:
            self.animate_particle_effect()
            
    def reset(self):
        self.last_animation_time = 0
        self.current_time = 0
        self.animation_index = 0


class PlaceSettlementAnimation(Animation):
    def __init__(self):
        super().__init__()

        self.animation_delay = 80
        # self.particle_system_form.color = settlement_stats_colors[0]


    def animate_image_sequence(self):

        triggered = self.check_animation_trigger()
        if triggered:
            next_key = list(self.animation_object.images.keys())[
                self.animation_index]
            self.animation_object.image = self.animation_object.images[next_key]
            self.animation_object.image.set_alpha(self.alpha_transparency)
            if self.animation_index >= len(self.animation_object.images) - 1:
                self.animation_object.play_placement_animation = False
                self.animation_object.image = self.animation_object.images["main_image"]
                self.animation_object.image.set_alpha(
                    self.alpha_non_transparent)

                self.reset()
                return

            self.animation_index += 1

    def animate(self, screen, animation_object):
        super().animate(screen, animation_object)
        
        self.particle.set_max_animation_duration = self.animation_delay*len(self.animation_object.images)

        self.animate_image_sequence()
