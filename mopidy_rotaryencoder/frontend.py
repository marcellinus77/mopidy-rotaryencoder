from __future__ import unicode_literals

import pykka
from mopidy import core

volume_delta = 5

class RotaryEncoderFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RotaryEncoderFrontend, self).__init__()
        self.core = core

        from .gpio_input_manager import GPIOManager
        self.gpio_manager = GPIOManager(self, config['rotaryencoder'])

    def input(self, input_event):
        try:
            if input_event['key'] == 'volume_up':
                if not self.core.mixer.get_mute().get():
                    current = self.core.mixer.get_volume().get()
                    current += volume_delta
                    if current > 100:
                        current = 100
                    self.core.mixer.set_volume(current)
            elif input_event['key'] == 'volume_down':
                if not self.core.mixer.get_mute().get():
                    current = self.core.mixer.get_volume().get()
                    current -= volume_delta
                    if current < 0:
                        current = 0
                    self.core.mixer.set_volume(current)
            elif input_event['key'] == 'mute':
                current = self.core.mixer.get_mute().get()
                self.core.mixer.set_mute(not current)
        except Exception:
            traceback.print_exc()
