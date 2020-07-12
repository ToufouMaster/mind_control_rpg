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
from src.scenes import desktop_computer

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
LOGO_START_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "1"
LOGO_DONE_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "2"

with LOGO_START_PATH.open("r") as f:
    logo = [line.strip() for line in f]
    LOGO_START = "\n".join(logo)

with LOGO_DONE_PATH.open("r") as f:
    logo = [line.strip() for line in f]
    LOGO_DONE = "\n".join(logo)


class StartComputer(Scene):
    """
    The first computer the user can use.
    """
    def desktop(self) -> None:  # pylint: disable=R0914
        # TODO: Programming language name: Parcel-3
        """
        Shows the desktop of the first computer.

        :return:  
        """

        key=0

        desktop_closed = False

        Window = desktop_computer.Windows(self.renderer)

        Window.add_window(self.renderer, x_pos = 20, y_pos = 1)

        self.clear()

        for w in Window.windows:

            for t in range(len(desktop_computer.window_logo)):
                self.addinto(w[1], w[2]+t, desktop_computer.window_logo[t])
            
            self.addinto(w[1]+2, w[2]+1, desktop_computer.window_name_logo[1])

        while desktop_closed == False:
            key = self.renderer.stdscr.getch()
            self.renderer.refresh()
            if key == curses.KEY_MOUSE:
                mousepos = curses.getmouse()
                if Window.check_on_click_close(mousepos[1],mousepos[2], w[1], w[2], w[3]):
                    desktop_closed = True
            elif key==27:
                desktop_closed = True


    def start(self) -> None:  # pylint: disable=R0914
        # TODO: Programming language name: Parcel-3
        """
        Shows the init sequence of the first computer.

        :return:  
        """
        animation = start_computer_bios.create_animation(self.renderer)
        y_pos = animation.start()

        font_logo = (curses.color_pair(0) | curses.A_ITALIC | curses.A_BOLD | curses.A_BLINK)
        self.addinto_all_centred(LOGO_START, 0.05)
        self.addinto_all_centred(LOGO_DONE, color_pair=font_logo)

        animation = start_computer_boot.create_animation(self.renderer)
        animation.start(y_pos + 1) # leave a blank line

        self.clear()

        self.desktop()
