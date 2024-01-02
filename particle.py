#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 08:21:42 2024

@author: lukasgartmair
"""
import pygame
import particlepy
import random
import time

class Particle:
    def __init__(self):

        self.particle_system = particlepy.particle.ParticleSystem()
        self.max_vel = 15
        self.last_tick = time.time()
        self.delta_time = 0

    def update_time_delta(self):

        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_tick
        self.last_tick = self.current_time

    def update(self):

        self.update_time_delta()

        self.particle_system.update(delta_time=self.delta_time)
        for particle in self.particle_system.particles:
            particle.shape.color = particlepy.math.fade_color(
                particle=particle, color=(58, 81, 104), progress=particle.inverted_progress)
            particle.shape.alpha = particlepy.math.fade_alpha(
                particle=particle, alpha=125, progress=particle.inverted_progress)

    def emit_particles(self):

        mouse_pos = pygame.mouse.get_pos()

        for _ in range(8):
            self.particle_system.emit(
                particle=particlepy.particle.Particle(
                    shape=particlepy.shape.Circle(
                        radius=9 + random.uniform(0, 1.35),
                        color=(240, 84, 84),
                    ),
                    position=mouse_pos,
                    velocity=(random.uniform(-self.max_vel, self.max_vel), random.uniform(-self.max_vel, self.max_vel)),
                    delta_radius=0.28,
                )
                )
            
    def render(self, screen):

        self.particle_system.make_shape()
        self.particle_system.render(surface=screen)
