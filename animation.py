#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:42:52 2024

@author: lukasgartmair
"""

import pygame
import colors
import base_animation

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

        self.particle.max_animation_duration = self.animation_delay * self.length_cycle * self.number_of_cycles

        self.animate_particle_effect()

        self.animate_image_sequence()
        
        

class TradeAnimation(base_animation.BaseAnimation):
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
        
        super().animate(animation_object)
        
        for node_a, node_b, data in self.animation_object.get_connections(
            include_data=True
        ):
            if (node_a, node_b) not in self.trades:
                self.trades[node_a, node_b] = ContinuousTradeRouteAnimation(self.camera, node_a, node_b, data)
                
        for trade_route in self.trades.values():
            trade_route.animate(None)
        
        
        
        
        
        
        
        
        
        
        
        

# class TradeAnimation(BaseAnimation):
#     def __init__(self, camera):
#         super().__init__(camera)

#         self.particle.color = (0, 255, 0)
#         self.particle.max_animation_duration = -1
#         self.particle.max_velocity = 20
#         self.particle.delta_radius = 0.4
#         self.particle.radius = 2

#         self.colors = colors.get_gradients()
#         self.trades = {}
#         self.trading_velocity = 5
#         self.path_counter = 0
#         self.color = (0,0,0)
#         self.trading_direction = 0

#     def animate(self, animation_object):
        
#         super().animate(animation_object)
        
#         for node_a, node_b, data in self.animation_object.get_connections(
#             include_data=True
#         ):
#             if (node_a, node_b) not in self.trades:
#                 self.trades[node_a, node_b] = ContinuousTradeRouteAnimation(self.camera, node_a, node_b, data)
                
#         for trade_route in self.trades.values():
#             trade_route.animate(None)
            
# class ContinuousTradeRouteAnimation(TradeAnimation):
#     def __init__(self, camera, node_a, node_b, data):
#         super().__init__(camera)
#         self.node_a = node_a
#         self.node_b = node_b
#         self.path = data["path"]

#     def animate(self, animation_object):

#         if self.trading_direction == 0:
#             self.path_counter += 1 * self.trading_velocity
#         else:
#             self.path_counter -= 1 * self.trading_velocity

#         if self.path_counter >= len(self.path)-1:
#             self.trading_direction = 1
#             self.path_counter = len(self.path)-1
#         elif self.path_counter < 0:
#             self.trading_direction = 0
#             self.path_counter = 0

#         position = self.path[self.path_counter]
#         if self.camera.is_within_current_view(position):
        
#             relative_position = self.camera.get_relative_screen_position(position)
#             color_index = (self.path_counter // len(self.colors))-1
#             if color_index >= len(self.colors) - 1:
#                 color_index = len(self.colors)-1
#             self.color = self.colors[color_index]

#             self.particle.position = relative_position
#             self.particle.color = self.color
#             self.animate_particle_effect()

                
# class SingleTradeRouteAnimation(TradeAnimation):
#     # def __init__(self, camera, node_a, node_b, data):
#     #     super().__init__(camera)
#     #     self.node_a = node_a
#     #     self.node_b = node_b
#     #     self.path = data["path"]
#     #     self.slow_down_factor = 20

#     # def animate(self, animation_object):
#         # print("here")
#         # if self.path_counter <= len(self.path)-1:
#         #     print(self.path_counter)
#         #     path_position = self.path[self.path_counter]
#     #         if self.camera.is_within_current_view(path_position):
#     #             relative_position = self.camera.get_relative_screen_position(path_position)
#     #             color_index = (self.path_counter // len(self.colors))-1
#     #             if color_index >= len(self.colors) - 1:
#     #                 color_index = len(self.colors)-1
#     #             self.color = self.colors[color_index]
    
#     #             self.particle.position = relative_position
#     #             self.particle.color = self.color
                
#     #             for j in range(self.slow_down_factor):
                    
#     #                 self.animate_particle_effect()
                    
#     #     self.path_counter += 1 
            
#     def __init__(self, camera, node_a, node_b, data):
#         super().__init__(camera)
#         self.node_a = node_a
#         self.node_b = node_b
#         self.data = data

#     def animate(self, animation_object):

#         super().animate(animation_object)        

#         if self.trading_direction == 0:
#             self.path_counter += 1 * self.trading_velocity
#         else:
#             self.path_counter -= 1 * self.trading_velocity

#         if self.path_counter >= len(self.data["path"])-1:
#             self.trading_direction = 1
#             self.path_counter = len(self.data["path"])-1
#         elif self.path_counter < 0:
#             self.trading_direction = 0
#             self.path_counter = 0

#         position = self.data["path"][self.path_counter]
#         if self.camera.is_within_current_view(position):
        
#             relative_position = self.camera.get_relative_screen_position(position)
#             color_index = (self.path_counter // len(self.colors))-1
#             if color_index >= len(self.colors) - 1:
#                 color_index = len(self.colors)-1
#             self.color = self.colors[color_index]

#             self.particle.position = relative_position
#             self.particle.color = self.color
#             self.animate_particle_effect()

