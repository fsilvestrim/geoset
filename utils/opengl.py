import moderngl
import numpy as np

from utils import opencv


def get_new_image(size, image, noise):
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
            uniform sampler2D texture1;
    
            in vec2 uv;
            out vec4 f_color;
    
            void main() {
                vec4 noise = texture(texture1, uv);
                vec2 displaced_uv = uv + noise.xy * vec2(0.01, 0.01);
                vec4 image = texture(texture0, displaced_uv);
                
                f_color = image;
            }
        ''',
    )

    # Parameters
    prog['texture0'] = 0
    ctx.texture(image.shape[:2], 3, opencv.image_to_byte_array(image)).use(0)

    prog['texture1'] = 1
    ctx.texture(noise.shape[:2], 3, opencv.image_to_byte_array(noise)).use(1)

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
    vao.render(mode=moderngl.TRIANGLE_FAN)

    return fbo.read(size, components=4, dtype='f1')
