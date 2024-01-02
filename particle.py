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
from colors import settlement_stats_colors


class Particle:
    def __init__(self):

        self.particle_system = particlepy.particle.ParticleSystem()
        self.max_vel = 180
        self.last_tick = time.time()
        self.delta_time = 0
        self.int_amount = 3
        self.radius = 5
        self.min_rnd_radius = 0
        self.max_rnd_radius = 10
        self.color = settlement_stats_colors[0]
        self.delta_radius = 0.1
        self.alpha = 0.2
        self.animate = True
        self.animation_duration = 0
        self.max_animation_duration = 0
        
    def set_max_animation_duration(self, max_animation_duration):
        self.max_animation_duration = max_animation_duration

    def update_time_delta(self):

        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_tick
        self.animation_duration += self.delta_time
        self.last_tick = self.current_time
        
        return self.animation_duration <= self.max_animation_duration

    def update_colors(self):

        for particle in self.particle_system.particles:
            particle.shape.color = particlepy.math.fade_color(
                particle=particle, color=self.color, progress=particle.inverted_progress)
            particle.shape.alpha = particlepy.math.fade_alpha(
                particle=particle, alpha=self.alpha, progress=particle.inverted_progress)


    def update(self):

        self.animate = self.update_time_delta()
        if self.animate:
            self.particle_system.update(delta_time=self.delta_time)
        else:
            self.particle_system.clear()

    def emit_particles(self, position):
        
        for _ in range(self.int_amount):
            self.particle_system.emit(
                particle=particlepy.particle.Particle(
                    shape=particlepy.shape.Circle(
                        radius=self.radius + random.uniform(self.min_rnd_radius, self.max_rnd_radius),
                        color=self.color,
                    ),
                    position=position,
                    velocity=(random.gauss(mu=0,sigma=self.max_vel),
                              random.gauss(mu=0,sigma=self.max_vel)),
                    delta_radius=self.delta_radius,
                )
            )


    def render(self, screen):
        
        self.particle_system.make_shape()
        self.particle_system.render(surface=screen)
