#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:16:56 2023

@author: lukasgartmair
"""

import pygame
from pygame import surfarray
from scene_base import SceneBase
import settlement
from engine import GameState
import custom_events
import trade
from selection_manager import SelectionManager
from connection_manager import ConnectionManager
import scene_manager
from colors import settlement_stats_colors
import animation
import networkx as nx
import animation


class GameScene(SceneBase):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        print("Game Scene")
        self.game_sound.play_background_music_1()
        custom_events.TRADE = custom_events.register_trade()

        self.connection_manager = ConnectionManager(self.game_map)

        self.game_trade = trade.Trade(
            self.settlements, self.connection_manager)

        self.any_settlement_clicked = False
        self.selection_manager = SelectionManager(
            self.settlements, self.any_settlement_clicked
        )

        self.transactions = []
        self.trade_animation = None

    def remove_selected_settlements(self):
        if self.selection_manager.selected_settlements:
            for s in self.selection_manager.selected_settlements:
                self.connection_manager.remove_settlement(
                    s, self.game_trade, self.game_engine)

    def check_mouse_click_in_bounds(self, mouse_position, game_camera):
        return game_camera.is_in_bounds(mouse_position)

    def check_for_settlement_overlap(self, new_settlement, game_camera):
        new_settlement.update_rect_center_for_sprite_collision()
        for s in self.settlements:
            s.update_rect_center_for_sprite_collision()
        overlap = pygame.sprite.spritecollideany(
            new_settlement, self.settlements)
        new_settlement.update_render_center(game_camera)
        for s in self.settlements:
            s.update_render_center(game_camera)

        return overlap

    def try_new_settlement_placement(self, game_camera, mouse_position):
        mouse_position_translated_to_absolute_map = game_camera.get_absolute_map_position(
            mouse_position)
        valid_placement = self.game_map.check_valid_village_placement(
            mouse_position_translated_to_absolute_map)
        if valid_placement:
            absolute_map_position = game_camera.get_absolute_map_position(
                mouse_position
            )

            tmp_settlement = settlement.Settlement(
                absolute_map_position
            )

            overlap = None
            overlap = self.check_for_settlement_overlap(
                tmp_settlement, game_camera)

            if overlap is None:
                settlement_placed = self.game_engine.place_settlement()

                if settlement_placed:
                    self.settlements.add(tmp_settlement)
                    self.all_sprites.add(tmp_settlement)

                    self.connection_manager.settlement_connections.add_settlement(
                        tmp_settlement
                    )
                    tmp_settlement.placed(self.game_trade, self.game_sound)
                    animation.animation_queue.add_to_main_loop_animations(
                        tmp_settlement, animation.PlaceSettlementAnimation(tmp_settlement, game_camera))

            else:
                tmp_settlement.remove()

    def try_connect_settlements(self):
        already_connected = self.connection_manager.already_connected(
            self.selection_manager.selected_settlements
        )
        successfully_connected = False
        if already_connected == False:
            successfully_connected = self.connection_manager.connect_settlements(
                self.selection_manager.selected_settlements[0],
                self.selection_manager.selected_settlements[1],
                self.game_map,
            )

            if successfully_connected:
                self.selection_manager.handle_successful_connection()

    def process_input(self, events, pressed_keys, game_camera):
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.transactions = self.game_trade.perform_trade()

            self.selection_manager.update_selected_settlements()

            if self.selection_manager.check_connection_condition():
                self.try_connect_settlements()

            self.settlements.update(
                self.connection_manager, event, game_camera, self.game_engine
            )

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    self.remove_selected_settlements()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_position = pygame.mouse.get_pos()

                    if self.check_mouse_click_in_bounds(mouse_position, game_camera):
                        self.selection_manager.check_any_settlement_clicked(
                            mouse_position
                        )

                        if self.selection_manager.selection_and_void_click():
                            break

                        if self.selection_manager.any_settlement_clicked:
                            self.selection_manager.process_settlement_click()

                        if (
                            not self.selection_manager.any_settlement_clicked
                            and self.game_engine.settlements_available > 0
                        ):
                            self.try_new_settlement_placement(
                                game_camera, mouse_position
                            )
                    else:
                        pass

        self.game_engine.check_win_condition(self.settlements)

    def get_scene_data(self):
        return self.connection_manager.settlement_connections

    def update(self):
        pass

    # def render_continuous_trading_routes(self, game_camera):

    #     if self.trade_animation is None:
    #         self.trade_animation = animation.TradeAnimation(game_camera)

    #     trading_paths = self.get_scene_data()

    #     if nx.is_empty(trading_paths) == False:
    #         self.trade_animation.animate(trading_paths)

    def render_single_trades(self, game_camera):

        if self.transactions:
            for transaction in self.transactions:
                bidder = transaction.bidder.id
                asker = transaction.asker.id
                data = self.connection_manager.settlement_connections.get_edge_data(
                    transaction.bidder.id, transaction.asker.id)

                # animation.ContinuousTradeRouteAnimation(
                #     game_camera, bidder, asker, data)
                # single_trade_route_animation = animation.SingleTradeRouteAnimation(
                #     game_camera, bidder, asker, data)
                # single_trade_route_animation.animate(None)

    def render(self, game_camera, game_font):

        screen = game_camera.camera_screen
        surfarray.blit_array(
            screen, game_camera.get_map_cutout(self.game_map.mapped_grid)
        )
        tmp = game_camera.get_map_cutout(self.game_map.mapped_grid)
        surfarray.blit_array(screen, tmp)
        path_map = self.connection_manager.settlement_connections.map_paths_to_grid(
            self.game_map)
        tmp = game_camera.get_map_cutout(path_map)
        surfarray.blit_array(screen, tmp)

        self.settlements.draw(screen)

        self.game_engine.render_settlement_count(screen, game_font)

        if self.game_engine.state == GameState.ENDED:
            self.switch_to_scene(
                scene_manager.get_end_scene(
                    self.game_engine,
                    self.game_map,
                    self.game_sound,
                    self.sprite_groups,
                ))

    def render_second_screen(self, game_camera, game_font):
        screen = game_camera.camera_screen
        screen.get_rect()
        screen_dimensions = game_camera.get_camera_screen_dimensions()
        pygame.draw.rect(
            screen,
            (settlement_stats_colors[0]),
            pygame.Rect(0, 0, screen_dimensions[0], screen_dimensions[1]),
        )

        for s in self.settlements:
            if s.hover:
                s.render_settlement_stats(game_camera, game_font)

        self.game_trade.render_global_assets(screen, game_font)
