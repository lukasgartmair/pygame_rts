#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 20:38:15 2024

@author: lukasgartmair
"""

import pygame
import moderngl
import ctypes

vertex_shader_sprite = """
#version 330
in vec2 in_position;
in vec2 in_uv;
out vec2 v_uv;
void main()
{
    v_uv = in_uv;
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

fragment_shader_sprite = """
#version 330
out vec4 fragColor;
uniform sampler2D u_texture;
in vec2 v_uv;
void main() 
{
    fragColor = texture(u_texture, v_uv);
}
"""


class ModernGLGroup(pygame.sprite.Group):

    gl_context = None
    gl_program = None
    gl_buffer = None
    gl_vao = None
    sampler = None
    gl_textures = {}

    def __init__(self, sprites=None):
        if sprites == None:
            super().__init__()
        else:
            super().__init__(sprites)

    def get_program():
        if ModernGLGroup.gl_program == None:
            ModernGLGroup.gl_program = ModernGLGroup.gl_context.program(
                vertex_shader=vertex_shader_sprite,
                fragment_shader=fragment_shader_sprite)
        return ModernGLGroup.gl_program

    def get_buffer():
        if ModernGLGroup.gl_buffer == None:
            ModernGLGroup.gl_buffer = ModernGLGroup.gl_context.buffer(
                None, reserve=6*4*4)
        return ModernGLGroup.gl_buffer

    def get_vao():
        if ModernGLGroup.gl_vao == None:
            ModernGLGroup.gl_vao = ModernGLGroup.gl_context.vertex_array(
                ModernGLGroup.get_program(), [(ModernGLGroup.get_buffer(), "2f4 2f4", "in_position", "in_uv")])
        return ModernGLGroup.gl_vao

    def get_sampler():
        if ModernGLGroup.sampler == None:
            ModernGLGroup.sampler = ModernGLGroup.gl_context.sampler()
        return ModernGLGroup.sampler

    def get_texture(image):
        if not image in ModernGLGroup.gl_textures:
            rgba_image = image.convert_alpha()
            texture = ModernGLGroup.gl_context.texture(
                rgba_image.get_size(), 4, rgba_image.get_buffer())
            texture.swizzle = 'BGRA'
            ModernGLGroup.gl_textures[image] = texture
        return ModernGLGroup.gl_textures[image]

    def convert_vertex(pt, surface):
        return pt[0] / surface.get_width() * 2 - 1, 1 - pt[1] / surface.get_height() * 2

    def render(sprite, surface):
        corners = [
            ModernGLGroup.convert_vertex(sprite.rect.bottomleft, surface),
            ModernGLGroup.convert_vertex(sprite.rect.bottomright, surface),
            ModernGLGroup.convert_vertex(sprite.rect.topright, surface),
            ModernGLGroup.convert_vertex(sprite.rect.topleft, surface)]
        vertices_quad_2d = (ctypes.c_float * (6*4))(
            *corners[0], 0.0, 1.0,
            *corners[1], 1.0, 1.0,
            *corners[2], 1.0, 0.0,
            *corners[0], 0.0, 1.0,
            *corners[2], 1.0, 0.0,
            *corners[3], 0.0, 0.0)

        ModernGLGroup.get_buffer().write(vertices_quad_2d)
        ModernGLGroup.get_texture(sprite.image).use(0)
        ModernGLGroup.get_vao().render()

    def draw_gl(self, surface):
        for sprite in self:
            ModernGLGroup.render(sprite, surface)
