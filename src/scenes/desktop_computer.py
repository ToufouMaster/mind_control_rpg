"""
This scene is for the start of the game, this computer is the first that the user can use.
"""

# ------------------------------------------------------------------------------
#  This file is part of Universal Sandbox.
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

import curses
import os
import pygame

from pathlib import Path
from pydub import AudioSegment
from pydub import playback

from src.animations import start_computer_bios, start_computer_boot
from src.core.scene import Scene

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
WINDOW_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "window"
WINDOWS_NAME_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "windows_name"
DESKTOP_BUTTON_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "desktop_program_button"
AUDIO_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "audio"

audio = []
audio_names = []

with WINDOW_PATH.open("r") as f:
    window_logo = [line.strip() for line in f]
    WINDOW = "\n".join(window_logo)

with WINDOWS_NAME_PATH.open("r") as f:
    window_name_logo = [line.strip() for line in f]
    WINDOW_NAME = "\n".join(window_name_logo)

with DESKTOP_BUTTON_PATH.open("r") as f:
    desktop_button_logo = [line.strip() for line in f]
    DESKTOP_BUTTON = "\n".join(window_name_logo)

for f in os.listdir(AUDIO_PATH):
    audio_names.append(f)
    audio.append(AUDIO_PATH / f)

pygame.mixer.init()

class Windows(Scene):
    """
    The classic window the user can use.
    """
    min_x_size = 10
    min_y_size = 5
    windows = []
    desktop_buttons = [0,1,2]
    desktop_icons_loc = []
    desktop_icon_can_open = [False, 0]

    def add_window(self, apk_nmb = 0, x_pos = 0, y_pos = 0, x_size = 40, y_size = 14):
        self.windows.append([apk_nmb, x_pos, y_pos, x_size, y_size])

    def remove_window(self, window_nmb):
        del self.windows[window_nmb]

    def check_on_click_close(self, mouse_x : int, mouse_y : int, pos_x : int, pos_y : int, x_size : int):
        if mouse_x == pos_x+x_size-3:
            if mouse_y == pos_y:
                return True
            return False
        return False

    def check_on_click_move(self, mouse_x : int, mouse_y : int, pos_x : int, pos_y : int, x_size : int):
        if mouse_x > pos_x:
            if mouse_x < pos_x+x_size-9:
                if mouse_y == pos_y:
                    return True
                return False
            return False
        return False

    def generate_program_icons_desktop_location(self):
        tmp = []
        for x in range(15):
            for y in range(10):
                tmp.append([(x*10)+4,(y*7)+1,7,5])
            y = 0
        self.desktop_icons_loc = tmp

    def check_on_desktop_icon_open(self, mouse_x : int, mouse_y : int, pos_x : int, pos_y : int, x_size : int, y_size : int, apk_id : int):
        if mouse_x >= pos_x:
            if mouse_x <= pos_x + x_size:
                if mouse_y >= pos_y:
                    if mouse_y <= pos_y + y_size:
                        if self.desktop_icon_can_open[0] == False:
                            self.desktop_icon_can_open[1] = self.desktop_buttons[apk_id]
                            self.desktop_icon_can_open[0] = True
                            return False
                        elif self.desktop_icon_can_open[0] == True:
                            if self.desktop_icon_can_open[1] == self.desktop_buttons[apk_id]:
                                self.desktop_icon_can_open[0] = False
                                return True
                            else:
                                self.desktop_icon_can_open[1] = self.desktop_buttons[apk_id]
                                return False
                            return False
                        return False
                    return False
                return False
            return False
        return False