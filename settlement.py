#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 14:15:39 2023

@author: lukasgartmair
"""

import pygame
from faker import Faker
import pygame.gfxdraw
import image
import random
from settlement_goods import SettlementGoods
from beautifultable import BeautifulTable, BTRowCollection
import re
import itertools

faker = Faker()

class Settlement(pygame.sprite.Sprite):
    id_iterator = itertools.count()
    def __init__(self, center, game_sound, game_trade):
        super().__init__()
        self.id = next(self.id_iterator)
        self.center = center
        self.render_center = center
        self.images = image.load_settlement_images("settlement_1")
        self.population = random.randint(1000, 200000)
        self.scale_factor = 0.15
        self.apply_population_to_scale()
        self.images.update(
            (
                k,
                pygame.transform.scale(
                    v,
                    (
                        v.get_width() * self.scale_factor,
                        v.get_height() * self.scale_factor,
                    ),
                ),
            )
            for k, v in self.images.items()
        )
        self.image = self.images["main_image"]
        self.surf = self.image
        self.rect = self.surf.get_rect(center=self.render_center)
        self.selected = False
        self.callback = self.on_click
        self.clicks = 0
        self.name = faker.city()
        self.hover = False
        self.connected = False

    def apply_population_to_scale(self):
        self.scale_factor = self.scale_factor * self.population ** (1.0 / 3) / 40

    def check_if_still_connected(self, global_path):
        still_connected = False
        for k, v in global_path.subpaths.items():
            if self.name in k:
                still_connected = True
        if still_connected == False:
            self.got_deconnected()

    def render_settlement_stats(self, game_camera, game_font):
        screen = game_camera.camera_screen
        screen_dimensions = game_camera.get_camera_screen_dimensions()
        screen_width, screen_height = screen_dimensions[0], screen_dimensions[1]
        vertical_offset = 25
        horizontal_offset = screen_width // 2

        vertical_offset = 25
        offset = 0

        text = game_font.render(self.name, True, (10, 0, 0))
        screen.blit(text, (horizontal_offset, offset))
        offset += vertical_offset

        text = game_font.render("gold: {}".format(self.gold), True, (10, 0, 0))
        screen.blit(text, (horizontal_offset, offset))
        offset += vertical_offset

        text = game_font.render("-" * 20, True, (10, 0, 0))
        screen.blit(text, (horizontal_offset, offset))
        offset += vertical_offset

        table = BeautifulTable()
        table.set_style(BeautifulTable.STYLE_COMPACT)
        # table.columns.alignment = BeautifulTable.ALIGN_LEFT
        # table.rows.alignment = BeautifulTable.ALIGN_LEFT
        table.columns.header = ["", "good", "magnitude"]
        rows = BTRowCollection(table)
        for k, v in self.trading_goods.items():
            row = ["", k, v]
            rows.append(row)

        splitted_table = re.split("\n", str(table))
        for line in splitted_table:
            text = game_font.render(line, True, (10, 0, 0))
            screen.blit(text, (horizontal_offset, offset))
            offset += vertical_offset

        text = game_font.render("-" * 20, True, (10, 0, 0))
        screen.blit(text, (horizontal_offset, offset))
        offset += vertical_offset
        text = game_font.render(
            "total: {}".format(self.trading_stats["total"]), True, (10, 0, 0)
        )
        screen.blit(text, (horizontal_offset, offset))
        offset += vertical_offset

    def placed(self, game_trade, game_sound):
        self.settlement_goods = SettlementGoods(self, game_trade)
        game_sound.play_place_settlement()

    def got_connected(self):
        self.connected = True
        self.deselect()

    def got_deconnected(self):
        self.connected = False
        self.deselect()

    def is_clicked(self, mouse_position):
        if self.rect.collidepoint(mouse_position[0], mouse_position[1]):
            return True
        return False

    def remove(self, global_path, game_engine):
        self.kill()
        global_path.remove_subpath(self.name)
        game_engine.remove_settlement()

    def update_render_center(self, game_camera):
        self.render_center = game_camera.get_relative_screen_position(self.center)
        self.rect = self.surf.get_rect(center=self.render_center)
        
    def update_rect_center_for_sprite_collision(self):
        
        self.rect = self.surf.get_rect(center=self.center)
        
    def update(self, mouse_position, game_camera, global_path, game_engine):
        self.settlement_goods.update_trading_stats()

        self.check_hover()
        
        if self.is_clicked(mouse_position):
            self.callback()
            self.clicks += 1

        if self.connected:
            self.check_if_still_connected(global_path)

        self.update_render_center(game_camera)

    def check_hover(self):
        self.hover = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False

    def select(self):
        self.selected = True
        self.image = self.images["select_image"]

    def deselect(self):
        self.selected = False
        self.image = self.images["main_image"]

        if self.connected and self.settlement_goods.preferred_good_set:
            self.settlement_goods.restore_last_preferred_good()

    def on_click(self):
        pass
