from typing import Tuple

import moderngl
import numpy as np


class Effect:
    def __init__(self):
        self._context = moderngl.create_standalone_context()
        self._program = self._context.program(vertex_shader=self.get_vertex_shader(),
                                              fragment_shader=self.get_fragment_shader())

    def get_vertex_shader(self):
        return '''
            #version 330

            in vec2 in_vert;
            in vec2 in_uv;
            out vec2 uv;

            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                uv = in_uv;
            }
        '''

    def get_fragment_shader(self):
        return '''
            #version 330

            in vec2 uv;
            out vec4 f_color;

            void main() {
                f_color = vec4(uv.x, uv.y, 1, 1);
            }
        '''

    def setup(self):
        pass

    def _get_vertex_info(self):
        vbo = self._context.buffer(np.array([
            # x, y,         u, v
            1.0, 1.0,       1.0, 1.0,
            1.0, -1.0,      1.0, 0.0,
            -1.0, -1.0,     0.0, 0.0,
            -1.0, 1.0,      0.0, 1.0,
        ], dtype='f4').tobytes())

        vao = self._context.vertex_array(self._program, [(vbo, '2f 2f', 'in_vert', 'in_uv')])

        return vbo, vao

    def _get_framebuffer(self, size: Tuple[int, int]):
        fbo = self._context.simple_framebuffer(size)
        fbo.use()
        fbo.clear(1.0, 1.0, 1.0, 1.0)

        return fbo

    def render(self, size: Tuple[int, int]):
        _, vao = self._get_vertex_info()
        fbo = self._get_framebuffer(size)

        self.setup()

        vao.render(mode=moderngl.TRIANGLE_FAN)

        return fbo.read(size, components=4, dtype='f1')
