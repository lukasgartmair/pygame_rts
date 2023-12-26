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
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import random

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
        
        self.game_trade = game_trade
        self.gold = 20
        self.trading_goods = {}
        self.initialize_trading_goods()
        self.trading_stats = {"total": 0}
        
        self.preferred_good = ""
        self.preferred_good_index = -1
        
        self.number_of_other_selected_settlements = 0
        
    def apply_population_to_scale(self):
        self.scale_factor = self.scale_factor * self.population ** (1. / 3)/40
        
    def update_number_of_other_selected_settlements(self, selected_settlements):
        if self in selected_settlements:
            self.number_of_other_selected_settlements = len(selected_settlements)-1
        else:
            self.number_of_other_selected_settlements = len(selected_settlements)

    def trading_good_available(self, trading_good):
        if self.trading_goods[trading_good] > 0:
            return True
        else:
            return False
        
    def is_affordable(self, price, magnitude):
        if self.gold >= price * magnitude:
            return True
        else:
            return False
        
    def buy_trading_good(self, trading_good, price, magnitude):
        if self.is_affordable(price, magnitude):
            self.gold -= price
            self.trading_goods[trading_good] += magnitude
        
    def sell_trading_good(self, trading_good, price, magnitude):
        self.gold += price*magnitude
        self.trading_goods[trading_good] -= magnitude

    def update_preferred_good(self):
        
        self.preferred_good_index += 1
        if self.preferred_good_index >= len(list(self.trading_goods.keys()))+1:
            self.preferred_good_index = 0
        
        if self.preferred_good_index == len(list(self.trading_goods.keys())):
            self.select()
            return
            
        self.preferred_good = self.game_trade.possible_trading_goods[self.preferred_good_index]
        self.image = self.images[self.preferred_good+"_image"]
        if self.selected:
            self.deselect()
            
        print(self.preferred_good_index)

    def update_trading_stats(self):
        self.trading_stats["total"] = sum(self.trading_goods.values())

    def initialize_trading_goods(self):
        for tg in self.game_trade.possible_trading_goods:
            self.trading_goods[tg] = random.randint(1, 5)
        self.game_trade.update_global_assets(self.trading_goods)

    def check_if_still_connected(self, global_path):
        still_connected = False
        for k, v in global_path.subpaths.items():
            if self.name in k:
                still_connected = True
        if still_connected == False:
            self.got_deconnected()

    def render_settlement_stats(self, screen, game_font):
        width = int(SCREEN_WIDTH//4)
        height = int(SCREEN_HEIGHT//4)
        offset = 25
        pygame.draw.rect(screen, ((settlement_stats_colors[0])), pygame.Rect(
            SCREEN_WIDTH-width, SCREEN_HEIGHT-height, width, height))
        formatted_stats = []
        for k, v in self.trading_goods.items():
            formatted_stats.append(k + " : " + str(v))
        off = 0
        for f in formatted_stats:
            text = game_font.render(f, True, (30, 0, 0))
            screen.blit(text, (SCREEN_WIDTH-width, SCREEN_HEIGHT-height+off))
            off += offset

        f = "-----------------"
        text = game_font.render(f, True, (30, 0, 0))
        screen.blit(text, (SCREEN_WIDTH-width, SCREEN_HEIGHT-height+off))
        off += offset
        f = "TOTAL : " + str(self.trading_stats["total"])
        text = game_font.render(f, True, (30, 0, 0))
        screen.blit(text, (SCREEN_WIDTH-width, SCREEN_HEIGHT-height+off))
        off += offset

    def placed(self, game_sound):
        game_sound.play_place_settlement()

    def got_connected(self):
        self.connected = True
        self.deselect()

    def got_deconnected(self):
        self.connected = False
        self.deselect()
        
    def check_if_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos[0],event.pos[1]):
                    return True
        return False
                    
    def is_clicked(self):
        # if self.clicks > 0:
        self.callback()
        self.clicks += 1

    def check_if_to_remove(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    if self.selected:
                        self.kill()
                        return True
        return False

    def check_if_removed(self, events, global_path, game_engine):

        removed = self.check_if_to_remove(events)
        if removed:
            global_path.remove_subpath(self.name)
            game_engine.remove_settlement()

    def update(self, events, global_path, game_engine):
        
        self.update_trading_stats()

        self.check_hover()

        if self.check_if_clicked(events):
            self.is_clicked()

        if self.connected:
            self.check_if_still_connected(global_path)

        if self.selected:
            self.check_if_removed(events, global_path, game_engine)

    def select(self):
        self.selected = True
        self.image = self.images["select_image"]

    def deselect(self):
        self.selected = False
        
        # if self.connected and self.preferred_good != "":
        #     self.preferred_good_index -= 1
        #     self.update_preferred_good()
        # else:
        self.image = self.images["main_image"]
            
    def on_click(self):
        
        if self.selected:
            self.deselect()
        else:
            self.select()
        
        # if not self.connected and not self.selected:
        #     self.select()
    
        # elif not self.connected and self.selected:
        #     self.deselect()
        
        # elif self.connected and self.number_of_other_selected_settlements == 0:
        #     self.update_preferred_good()
        #     self.deselect()
            
        # elif self.connected and self.number_of_other_selected_settlements == 1:
        #     pass
        # else:
        #     self.deselect()


    def check_hover(self):
        self.hover = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False
