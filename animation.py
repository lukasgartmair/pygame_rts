#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:42:52 2024

@author: lukasgartmair
"""

import pygame
import colors
import base_animation
import connection_manager
import game_font
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

game_font = game_font.GameFont(
    game_font.font_style, game_font.font_size)


animation_queue = base_animation.AnimationQueue()


class PlaceSettlementAnimation(base_animation.BaseAnimation):
    def __init__(self, animation_object, camera,  animation_end_mode=base_animation.AnimationEndMode.N_TRIGGERS):
        super().__init__(camera)

        self.animation_object = animation_object

        self.animation_end_mode = base_animation.AnimationEndMode.N_TRIGGERS

        self.particle.color = colors.settlement_stats_colors[0]

        self.alpha_fully_transparent = 0
        self.alpha_transparency = 75
        self.alpha_non_transparent = 190

        self.animation_duration = 150
        self.animation_delay = 100

        self.length_cycle = len(self.animation_object.images)
        self.current_cycle = 0
        self.number_of_cycles = 1

    def animate_image_sequence(self):

        self.check_animation_trigger()

        if self.animation_index >= len(self.animation_object.images) - 1:

            self.increase_cycle_counter()

            self.animation_object.image = self.animation_object.images["main_image"]
            self.animation_object.image.set_alpha(
                self.alpha_non_transparent)

            if self.current_cycle == self.number_of_cycles:
                self.kill()
                return
        else:
            if self.triggered:
                next_key = list(self.animation_object.images.keys())[
                    self.animation_index]
                self.animation_object.image = self.animation_object.images[next_key]
                self.animation_object.image.set_alpha(self.alpha_transparency)

    def animate(self, animation_object):

        super().animate(animation_object)

        self.particle.position = self.animation_object.render_center

        self.particle.max_animation_duration = self.animation_delay * \
            self.length_cycle * self.number_of_cycles

        self.animate_particle_effect()

        self.animate_image_sequence()


class SoldAndReceivedTradingGood(base_animation.BaseAnimation):
    def __init__(self, camera, animation_end_mode=base_animation.AnimationEndMode.DURATION, mode="received"):
        super().__init__(camera)
        self.offset = 0
        self.animation_duration = 1500
        self.velocity = 2
        self.color = (0, 0, 0)
        self.string = ""
        self.mode = mode
        self.position = (0, 0)

    def animate(self, animation_object):
        super().animate(animation_object)
        price = animation_object.magnitude*animation_object.price

        if self.mode == "received":
            self.string = "+ {} {} for {} $"
            self.color = (0, 255, 0)

            self.position = self.animation_object.bidder.center
            
        elif self.mode == "sold":
            self.string = "- {} {} for {} $"
            self.color = (255, 0, 0)

            self.position = self.animation_object.asker.center

        text = game_font.render(self.string.format(
            animation_object.magnitude, animation_object.good, price), True, self.color)
        screen_position = self.camera.get_relative_screen_position(
            self.position)
        self.camera.camera_screen.blit(
            text, (screen_position[0]+self.offset, screen_position[1]-self.offset))
        self.offset += self.velocity


class TradeAnimation(base_animation.BaseAnimation):
    def __init__(self, camera, connection_manager, animation_end_mode=base_animation.AnimationEndMode.CUSTOM):
        super().__init__(camera)

        self.animation_end_mode = animation_end_mode
        self.connection_manager = connection_manager

        self.particle.color = (0, 255, 0)
        self.particle.max_animation_duration = -1
        self.particle.max_velocity = 20
        self.particle.delta_radius = 0.4
        self.particle.radius = 4

        self.colors = colors.get_gradients()
        self.trades = {}
        self.trading_velocity = SCREEN_WIDTH // 75
        self.path_counter = 0
        self.color = (0, 0, 0)
        self.trading_direction = 0

        self.path = None

    def custom_kill_function(self):
        if self.path_counter >= len(self.path):

            animation_queue.add_to_animation_loop(
                self.animation_object, SoldAndReceivedTradingGood(self.camera, mode="received"), base_animation.AnimationQueueType.MAIN)

            self.kill()

            return True

    def animate(self, animation_object):

        self.path = self.connection_manager.settlement_connections.get_path(
            animation_object.asker.id, animation_object.bidder.id)
        super().animate(animation_object)

        if self.custom_kill_function():
            return
        else:
            position = self.path[self.path_counter]
            if self.camera.is_within_current_view(position):

                relative_position = self.camera.get_relative_screen_position(
                    position)
                self.color = colors.get_trading_good_color(
                    animation_object.good)

                self.particle.position = relative_position
                self.particle.color = self.color
                self.animate_particle_effect()

                self.path_counter += 1 * self.trading_velocity
