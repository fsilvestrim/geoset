import numpy as np

from augmentation.effect import Effect


class ImageEffect(Effect):
    __texture_count = 0

    def __init__(self, image: np.array = None):
        super().__init__()
        self.set_image(image)

    def _set_texture(self, name: str, texture: np.array):
        size = texture.shape[:2]
        image = np.frombuffer(texture, dtype='uint8').reshape((size[1], size[0], 3)).tobytes()
        texture_idx = self.__texture_count

        self._program[name] = texture_idx
        self._context.texture(size, 3, image).use(texture_idx)
        self.__texture_count = self.__texture_count + 1

    def set_image(self, image: np.array):
        self._image = image

    def setup(self):
        if self._image is not None:
            self._set_texture('image', self._image)
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
