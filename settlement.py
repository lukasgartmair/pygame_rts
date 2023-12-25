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
    def __init__(self, center, game_sound, game_trade):
        super().__init__()
        self.center = center
        self.radius = 10
        self.images, self.selected_image = image.load_settlement_images("settlement_1")
        self.scale_factor = 0.15
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
        self.hover = False
        
        self.game_trade = game_trade
        self.trading_goods = {}
        self.trading_stats = {"total":0}
        self.initialize_trading_goods()
        
    def update_trading_stats(self):
        self.trading_stats["total"] = sum(self.trading_goods.values())
        
    def initialize_trading_goods(self):
        trading_goods = {}
        n = random.randint(1,len(self.game_trade.possible_trading_goods))
        trading_goods = sorted(random.sample(self.game_trade.possible_trading_goods,n))
            
        for tg in trading_goods:
            self.trading_goods[tg] = random.randint(1, 5)

    def next_image(self):
        if self.image_index < len(self.images) - 1:
            self.image_index += 1
        else:
            self.image_index = 0

        self.image = self.images[self.image_index]
        self.surf = self.image

    def placed(self, game_sound):
        game_sound.play_place_settlement()

    def connected(self):
        self.next_image()
        self.deselect()

    def update(self, events):
        
        self.update_trading_stats()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if self.clicks > 0:
                        self.callback()

                        if self.selected == False:
                            self.next_image()

                    self.clicks += 1
                    
        self.check_hover()


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
            
    def render_settlement_stats(self, screen, game_font):
        width = int(SCREEN_WIDTH//4)
        height = int(SCREEN_HEIGHT//4)
        offset = 25
        pygame.draw.rect(screen, ((settlement_stats_colors[0])), pygame.Rect(SCREEN_WIDTH-width, SCREEN_HEIGHT-height, width, height))        
        formatted_stats = []
        for k,v in self.trading_goods.items():
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

    def check_hover(self):
        self.hover = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False
