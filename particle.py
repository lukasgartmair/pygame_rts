#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 08:21:42 2024

@author: lukasgartmair
"""

import particlepy
import random
import time
from dataclasses import dataclass


@dataclass
class ParticleSystemForm:
    position: tuple = (0, 0)
    max_velocity: int = 180
    amount: int = 3
    radius: int = 5
    min_rnd_radius: int = 0
    max_rnd_radius: int = 10
    delta_radius: float = 0.1

    animate: bool = True
    animation_duration: int = 0
    max_animation_duration: int = 1000

    alpha: float = 0.2
    color: tuple = (0, 0, 255)


class Particle:
    def __init__(self, particle_system_form):

        self.particle_system = particlepy.particle.ParticleSystem()
        self.position = particle_system_form.position
        self.last_tick = time.time()
        self.delta_time = 0

        self.max_velocity = particle_system_form.max_velocity
        self.amount = particle_system_form.amount
        self.radius = particle_system_form.radius
        self.min_rnd_radius = particle_system_form.min_rnd_radius
        self.max_rnd_radius = particle_system_form.max_rnd_radius
        self.delta_radius = particle_system_form.delta_radius

        self.animate = particle_system_form.animate
        self.animation_duration = particle_system_form.animation_duration
        self.max_animation_duration = particle_system_form.max_animation_duration

        self.alpha = particle_system_form.alpha
        self.color = particle_system_form.color

    def update_time_delta(self):
        
        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_tick
        self.animation_duration += self.delta_time
        self.last_tick = self.current_time
        if self.max_animation_duration >= 0:         
            return self.animation_duration <= self.max_animation_duration
        else:
            return True

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

    def emit_particles(self):

        for _ in range(self.amount):
            self.particle_system.emit(
                particle=particlepy.particle.Particle(
                    shape=particlepy.shape.Circle(
                        radius=self.radius +
                        random.uniform(self.min_rnd_radius,
                                       self.max_rnd_radius),
                        color=self.color,
                    ),
                    position=self.position,
                    velocity=(random.gauss(mu=0, sigma=self.max_velocity),
                              random.gauss(mu=0, sigma=self.max_velocity)),
                    delta_radius=self.delta_radius,
                )
            )

    def render(self, screen):

        self.particle_system.make_shape()
        self.particle_system.render(surface=screen)
