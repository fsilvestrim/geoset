import numpy as np

from augmentation.effects.image_effect import ImageEffect


class DistortedImageEffect(ImageEffect):
    def __init__(self, noise: np.array, image: np.array = None):
        super().__init__(image)
        self._noise = noise

    def get_fragment_shader(self):
        return '''
            #version 330
    
            uniform sampler2D image;
            uniform sampler2D noise;
    
            in vec2 uv;
            out vec4 f_color;
    
            void main() {
                vec4 noise_color = texture(noise, uv);
                vec2 displaced_uv = uv + noise_color.xy * vec2(0.01, 0.01);
                f_color = texture(image, displaced_uv);
            }
        '''

    def setup(self):
        super().setup()
        self._set_texture('noise', self._noise)
