#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:42:52 2024

@author: lukasgartmair
"""

import pygame
import particle
import colors
import itertools
import camera


class Animation:
    def __init__(self, camera):

        self.camera = camera
        self.screen = self.camera.camera_screen
        self.animation_object = None
        self.particle_animation = True
        self.particle_system_form = particle.ParticleSystemForm()
        if self.particle_animation:
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
        self.triggered = False

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
        self.particle.render(self.screen)

    def initialize_animation_object(self, animation_object):
        self.animation_object = animation_object

    def animate(self, animation_object):

        if self.animation_object is None:
            self.initialize_animation_object(animation_object)
        pass

    def reset(self):
        self.last_animation_time = 0
        self.current_time = 0
        self.animation_index = 0
        
class PlaceSettlementAnimation(Animation):
    def __init__(self, camera):
        super().__init__(camera)

        self.animation_delay = 150
        self.particle.color = colors.settlement_stats_colors[0]

    def animate_image_sequence(self):

        self.check_animation_trigger()
        if self.triggered:
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

    def animate(self, animation_object):

        super().initialize_animation_object(animation_object)

        self.particle.position = animation_object.render_center

        self.particle.max_animation_duration = self.animation_delay * \
            len(self.animation_object.images)

        self.animate_particle_effect()

        self.animate_image_sequence()
    
class TradeAnimation(Animation):
    def __init__(self, camera):
        super().__init__(camera)

        self.particle.color = (0, 255, 0)
        self.particle.max_animation_duration = -1
        self.particle.max_velocity = 20
        self.particle.delta_radius = 0.4
        self.particle.radius = 2

        self.colors = colors.get_gradients()
        self.trades = {}
        self.trading_velocity = 5
        self.path_counter = 0
        self.color = (0,0,0)
        self.trading_direction = 0

    def animate(self, animation_object):
        
        super().initialize_animation_object(animation_object)
        
        for node_a, node_b, data in self.animation_object.get_connections(
            include_data=True
        ):
            if (node_a, node_b) not in self.trades:
                self.trades[node_a, node_b] = TradeRouteAnimation(self.camera, node_a, node_b, data)
                
        for trade_route in self.trades.values():
            trade_route.animate(None)
            
    def update_trade_routes(self):
        # only relevant if you are able to delete connected settlements
        current_connections = self.animation_object.get_connections()
        for trade_route in self.trades:
            if (trade_route.node_a, trade_route.node_b) not in current_connections:
                del self.trades[trade_route.node_a, trade_route.node_b]
                
class TradeRouteAnimation(TradeAnimation):
    def __init__(self, camera, node_a, node_b, data):
        super().__init__(camera)
        self.node_a = node_a
        self.node_b = node_b
        self.data = data

    def animate(self, animation_object):
        
        if self.particle_animation:
            if self.trading_direction == 0:
                self.path_counter += 1 * self.trading_velocity
            else:
                self.path_counter -= 1 * self.trading_velocity

            if self.path_counter >= len(self.data["path"])-1:
                self.trading_direction = 1
                self.path_counter = len(self.data["path"])-1
            elif self.path_counter < 0:
                self.trading_direction = 0
                self.path_counter = 0

            position = self.data["path"][self.path_counter]
            if self.camera.is_within_current_view(position[0], position[1]):
            
                relative_position = self.camera.get_relative_screen_position(position)
                color_index = (self.path_counter // len(self.colors))-1
                if color_index >= len(self.colors) - 1:
                    color_index = len(self.colors)-1
                self.color = self.colors[color_index]
    
                self.particle.position = relative_position
                self.particle.color = self.color
                self.animate_particle_effect()
