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
from pathlib import Path

from src.animations import start_computer_bios, start_computer_boot
from src.core.scene import Scene

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
WINDOW_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "window"
WINDOWS_NAME_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "windows_name"

with WINDOW_PATH.open("r") as f:
    window_logo = [line.strip() for line in f]
    WINDOW = "\n".join(window_logo)

with WINDOWS_NAME_PATH.open("r") as f:
    window_name_logo = [line.strip() for line in f]
    WINDOW_NAME = "\n".join(window_name_logo)

class Windows(Scene):
    """
    The classic window the user can use.
    """
    min_x_size = 10
    min_y_size = 5
    windows = []

    def add_window(self, apk_name = "File Manager", x_pos = 0, y_pos = 0, x_size = 40, y_size = 15):
        z = len(self.windows)
        self.windows.append((apk_name, x_pos, y_pos, x_size, y_size))

    def check_on_click_close(self, mouse_x : int, mouse_y : int, pos_x : int, pos_y : int, x_size : int):
        if mouse_x == pos_x+x_size-3:
            if mouse_y == pos_y+1:
                return True
            return False
        return False