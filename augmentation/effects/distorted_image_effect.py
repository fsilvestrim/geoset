import cv2
import numpy as np

from os import path
from augmentation.effects.image_effect import ImageEffect


class DistortedImageEffect(ImageEffect):
    def __init__(self, factor: float = 0.01, image: np.array = None):
        super().__init__(image)
        self._factor = factor

        noise_image_path = path.join(path.dirname(__file__), '../res/perlin_noise.png')
        self._noise = cv2.imread(noise_image_path, cv2.IMREAD_COLOR)

    def get_fragment_shader(self):
        return '''
            #version 330
    
            uniform float factor;
            uniform sampler2D image;
            uniform sampler2D noise;
    
            in vec2 uv;
            out vec4 f_color;
    
            void main() {
                vec4 noise_color = texture(noise, uv);
                vec2 displaced_uv = uv + (noise_color.xy * vec2(factor, factor));
                f_color = texture(image, displaced_uv);
            }
        '''

    def setup(self):
        super().setup()
        self.set_uniform('factor', self._factor)
        self.set_texture('noise', self._noise)
