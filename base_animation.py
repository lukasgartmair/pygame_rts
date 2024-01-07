#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 12:59:36 2024

@author: lukasgartmair
"""

import pygame
import particle

class BaseAnimation:
    def __init__(self, camera):
        self.camera = camera
        self.animation_object = None
        
        self.animation_alive = True
        
    def initialize_animation_object(self, animation_object):
        self.animation_object = animation_object
        
    def animate(self, animation_object):

        if self.animation_object is None:
            self.initialize_animation_object(animation_object)
            
    def kill(self):
        del self
        
    def check_for_self_destruction(self):
        if self.animation_index > self.numer_of_triggers:
            self.kill()
    
class BaseTriggeredAnimation(BaseAnimation):
    def __init__(self, camera):
        super().__init__(camera)
        self.numer_of_triggers = 1

        self.current_time = 0
        self.last_animation_time = 0
        self.triggered = False
        
        self.animation_index = 0
        
    def check_animation_trigger(self):

        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_animation_time >= self.animation_delay:
            self.last_animation_time = self.current_time
            self.triggered = True
            print("triggered")
            self.animation_index += 1
            
            print(self.animation_index)
            
            # self.check_for_self_destruction()
            
        else:
            self.triggered = False

class BaseParticleAnimation(BaseAnimation):
    def __init__(self, camera):
        super().__init__(camera)
        self.particle_system_form = particle.ParticleSystemForm()
        self.particle = particle.Particle(self.particle_system_form)
        
        self.particle.max_animation_duration = 100
        
        self.current_time = 0
        self.last_animation_time = 0
        self.triggered = False
        self.animation_delay = 0
        
        self.animation_index = 0

    def check_animation_trigger(self):

        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_animation_time >= self.animation_delay:
            self.last_animation_time = self.current_time
            self.triggered = True
        else:
            self.triggered = False

    def animate_particle_effect(self):

        self.particle.update()
        self.particle.emit_particles()
        self.particle.render(self.camera.camera_screen)

    def animate(self, animation_object):

        if self.animation_object is None:
            self.initialize_animation_object(animation_object)

    def reset(self):
        self.last_animation_time = 0
        self.current_time = 0
        self.animation_index = 0
