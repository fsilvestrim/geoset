import numpy as np
from moderngl import Texture

from augmentation.effect import Effect


class ImageEffect(Effect):
    def __init__(self, image: np.array = None):
        super().__init__()
        self._textures = []
        self.set_image(image)

    def set_texture(self, name: str, texture: np.array):
        size = texture.shape[:2]
        image = np.frombuffer(texture, dtype='uint8').reshape((size[1], size[0], 3)).tobytes()
        texture_idx = len(self._textures)

        self._program[name] = texture_idx
        texture = self._context.texture(size, 3, image)
        texture.use(texture_idx)

        self._textures.append(texture)

        return texture

    def release(self):
        texture: Texture
        for texture in self._textures:
            texture.release()

        self._textures = None

        super().release()

    def set_image(self, image: np.array):
        self._image = image

    def setup(self):
        if self._image is not None:
            texture = self.set_texture('image', self._image)
            texture.repeat_x = False
            texture.repeat_y = False
        else:
            raise Exception("No Image was given!")

    def get_fragment_shader(self):
        return '''
            #version 330

            uniform sampler2D image;

            in vec2 uv;
            out vec4 f_color;

            void main() {
                f_color = texture(image, uv);
            }
        '''
