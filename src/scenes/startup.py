"""
This Scene is responsible for showing the game's title and startup messages.
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
from typing import Any

from src.core.scene import Scene
from src.scenes.start_computer import StartComputer

STARTUP_MESSAGE_PATH = Path(__file__).parent.absolute() / "STARTUP"
FULL_LICENSE_PATH = Path(__file__).parent.parent.parent.absolute() / "LICENCE"

with open(STARTUP_MESSAGE_PATH, "r") as f:
    STARTUP_MESSAGE = f.read()

with FULL_LICENSE_PATH.open("r") as f:
    licence = [line.strip() for line in f]
    FULL_LICENSE = "\n".join(licence)


class StartupScene(Scene):
    """
    This scene is called at the start of the game, in engine.py
    """

    def start(self) -> Any:  # pylint: disable=R1711
        """
        Shows a copyright notice and the game's title.
        """
        self.clear()
        self.sleep_key(0.5)
        self.addinto_all_centred(STARTUP_MESSAGE, delay=0.05, pager_delay=0)

        y_pos = (
            round(
                (self.renderer.max_y / 2) + round(len(STARTUP_MESSAGE.splitlines()) / 2)
            )
            + 2
        )
        # HACK This mess will make the
        # message appear two lines after the startup message.

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.addinto_centred(
            y_pos,
            "  Press any key to start  \n" " Press l for full license ",
            0.1,
            0,
            curses.color_pair(1) | curses.A_BLINK | curses.A_DIM,
        )
        key = self.get_key()
        self.clear()
        if key == "l":
            self.addinto_all_centred(FULL_LICENSE, 0.01, 5)

        return StartComputer(self.renderer)
