#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 14:15:39 2023

@author: lukasgartmair
"""

import pygame
from colors import settlement_colors
from faker import Faker
import pygame.gfxdraw
import image

faker = Faker()


def circleSurface(radius, color):
    shape_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    # pygame.gfxdraw.aacircle(shape_surf, radius, radius, radius, color)
    # pygame.gfxdraw.filled_circle(shape_surf, radius, radius, radius, color)
    return shape_surf


def update_selected_settlements(
    selected_settlements, global_path, game_map, game_sound
):
    if len(selected_settlements) == 2:
        global_path.connect_settlements(selected_settlements, game_map, game_sound)
        for s in selected_settlements:
            s.deselect()
        selected_settlements.empty()
    elif len(selected_settlements) > 2:
        selected_settlements.pop()
    else:
        pass
    return selected_settlements


class Settlement(pygame.sprite.Sprite):
    def __init__(self, center, game_sound):
        super().__init__()
        self.center = center
        self.color = settlement_colors[0]
        self.radius = 10
        self.images, self.selected_image = image.load_settlement_images("settlement_1")
        self.scale_factor = 0.1
        self.images = [
            pygame.transform.scale(
                i,
                (i.get_width() * self.scale_factor, i.get_height() * self.scale_factor),
            )
            for i in self.images
        ]
        self.selected_image = pygame.transform.scale(
            self.selected_image,
            (
                self.selected_image.get_width() * self.scale_factor,
                self.selected_image.get_height() * self.scale_factor,
            ),
        )
        self.image = self.images[0]
        self.surf = self.image
        self.rect = self.surf.get_rect(center=center)
        self.selected = False
        self.callback = self.on_click
        self.clicks = 0
        self.name = faker.city()
        self.image_index = 0

    def next_image(self):
        if self.image_index < len(self.images) - 1:
            self.image_index += 1
        else:
            self.image_index = 0

        self.image = self.images[self.image_index]
        self.surf = self.image

    def placed(self, game_sound):
        print(self.name)
        game_sound.play_place_settlement()

    def connected(self):
        self.next_image()
        self.deselect()

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if self.clicks > 0:
                        self.callback()

                        if self.selected == False:
                            self.next_image()

                    self.clicks += 1

    def check_removal(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    if self.selected:
                        self.kill()
                        return True
        return False

    def select(self):
        self.selected = True
        self.image = self.selected_image

    def deselect(self):
        self.selected = False
        self.image = self.images[self.image_index]

    def on_click(self):
        if self.selected == False:
            self.select()
        else:
            self.deselect()
