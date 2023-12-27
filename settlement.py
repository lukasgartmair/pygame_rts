#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 14:15:39 2023

@author: lukasgartmair
"""

import pygame
from colors import settlement_stats_colors
from faker import Faker
import pygame.gfxdraw
import image
import random
from settlement_goods import SettlementGoods
import camera

faker = Faker()

class Settlement(pygame.sprite.Sprite):
    def __init__(self, center, game_sound, game_trade):
        super().__init__()
        self.center = center
        self.images = image.load_settlement_images("settlement_1")
        self.population = random.randint(1000,200000)
        self.scale_factor = 0.15
        self.apply_population_to_scale()
        self.images.update((k, pygame.transform.scale(
            v,
            (v.get_width() * self.scale_factor, v.get_height() * self.scale_factor))) for k, v in self.images.items())
        self.image = self.images["main_image"]
        self.surf = self.image
        self.rect = self.surf.get_rect(center=center)
        self.selected = False
        self.callback = self.on_click
        self.clicks = 0
        self.name = faker.city()
        self.hover = False
        self.connected = False
        
        self.settlement_goods = SettlementGoods(self, game_trade)
        
    def apply_population_to_scale(self):
        self.scale_factor = self.scale_factor * self.population ** (1. / 3)/40

    def check_if_still_connected(self, global_path):
        still_connected = False
        for k, v in global_path.subpaths.items():
            if self.name in k:
                still_connected = True
        if still_connected == False:
            self.got_deconnected()

    def render_settlement_stats(self, screen, game_font):
        screen_width, screen_height = camera.get_camera_screen_dimensions(screen)
        offset = 25
        width = screen_width//4
        height = screen_height - offset
        pygame.draw.rect(screen, ((settlement_stats_colors[0])), pygame.Rect(
            screen_width-width, screen_height-height, width, height))
        off = 0
        text = game_font.render(self.name.upper(), True, (30, 0, 0))
        screen.blit(text, (screen_width-width, screen_height-height+off))
        off += offset
        # text = game_font.render("population: " + str(self.population), True, (30, 0, 0))
        # screen.blit(text, (screen_width-width, screen_height-height+off))
        # off += offset
        f = "-----------------"
        text = game_font.render(f, True, (30, 0, 0))
        screen.blit(text, (screen_width-width, screen_height-height+off))
        off += offset
        formatted_stats = []
        for k, v in self.trading_goods.items():
            formatted_stats.append(k + " : " + str(v))
        
        for f in formatted_stats:
            text = game_font.render(f, True, (30, 0, 0))
            screen.blit(text, (screen_width-width, screen_height-height+off))
            off += offset

        f = "-----------------"
        text = game_font.render(f, True, (30, 0, 0))
        screen.blit(text, (screen_width-width, screen_height-height+off))
        off += offset
        f = "TOTAL : " + str(self.trading_stats["total"])
        text = game_font.render(f, True, (30, 0, 0))
        screen.blit(text, (screen_width-width, screen_height-height+off))
        off += offset

    def placed(self, game_sound):
        game_sound.play_place_settlement()

    def got_connected(self):
        self.connected = True
        self.deselect()

    def got_deconnected(self):
        self.connected = False
        self.deselect()
        
    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos[0],event.pos[1]):
                    return True
        return False
    
    def remove(self, global_path, game_engine):
        self.kill()
        global_path.remove_subpath(self.name)
        game_engine.remove_settlement()

    def update(self, events, global_path, game_engine):
        
        self.settlement_goods.update_trading_stats()

        self.check_hover()

        if self.is_clicked(events):
            self.callback()
            self.clicks += 1

        if self.connected:
            self.check_if_still_connected(global_path)
            
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

        if self.settlement_goods.preferred_good_set:
            self.settlement_goods.restore_last_preferred_good()

    def on_click(self):
        pass
            



