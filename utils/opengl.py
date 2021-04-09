import moderngl
import numpy as np


def get_new_image(size, image):
    ctx = moderngl.create_standalone_context()

    prog = ctx.program(
        vertex_shader='''
            #version 330
    
            in vec2 in_vert;
            in vec2 in_uv;
            out vec2 uv;
        
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                uv = in_uv;
            }
        ''',
        fragment_shader='''
            #version 330
    
            uniform sampler2D texture0;
    
            in vec2 uv;
            out vec4 f_color;
    
            void main() {
                f_color = texture(texture0, uv);
            }
        ''',
    )

    # Parameters
    texture = ctx.texture(size, 3, image)
    # texture = ctx.texture((2, 2), 3, np.array([200, 0, 0] * 4, dtype='f4').tobytes())

    # param_color = prog['Color']
    # param_color.value = (1, 0, 0)

    # Vertexes
    vbo = ctx.buffer(np.array([
        # x, y,         u, v
        1.0, 1.0,      1.0, 1.0,
        1.0, -1.0,     1.0, 0.0,
        -1.0, -1.0,    0.0, 0.0,
        -1.0, 1.0,     0.0, 1.0,
    ], dtype='f4').tobytes())

    vao = ctx.vertex_array(prog, [(vbo, '2f 2f', 'in_vert', 'in_uv')])

    # Frame buffer
    fbo = ctx.simple_framebuffer(size)
    fbo.use()
    fbo.clear(1.0, 1.0, 1.0, 1.0)

    # Render
    texture.use()
    vao.render(mode=moderngl.TRIANGLE_FAN)

    return fbo.read(size, components=4, dtype='f1')
