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

    def draw_all_windows(self, window):

        #BackGround Setup
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        font_window = (curses.color_pair(1))
        font_bg = (curses.color_pair(0) | curses.A_ITALIC | curses.A_BOLD)

        #BackGround Display
        self.addinto_all_centred(LOGO_START, color_pair=font_bg)
        self.addinto_all_centred(LOGO_DONE, color_pair=font_bg)

        #Icons Setup
        window.generate_program_icons_desktop_location()

        #Icons Display
        for d in range(len(window.desktop_buttons)):
            for t in range(len(desktop_computer.desktop_button_logo)):
                self.addinto(window.desktop_icons_loc[d][0], window.desktop_icons_loc[d][1]+t, desktop_computer.desktop_button_logo[t], color_pair=font_window)
            self.addinto(window.desktop_icons_loc[d][0]-1, window.desktop_icons_loc[d][1]+4, desktop_computer.window_name_logo[window.desktop_buttons[d]])
            if desktop_computer.window_name_logo[window.desktop_buttons[d]] == "Sound Box":
                pass

        # Update all Windows
        for w in window.windows:

            for t in range(len(desktop_computer.window_logo)):
                self.addinto(w[1], w[2] + t, desktop_computer.window_logo[t], font_window)

            self.addinto(w[1] + 2, w[2], desktop_computer.window_name_logo[w[0]], font_window)

    def desktop(self) -> None:  # pylint: disable=R0914
        # TODO: Programming language name: Parcel-3
        """
        Shows the desktop of the first computer.

        :return:
        """

        key=0

        window_moving = [False, 0, 0]
        desktop_closed = False

        Window = desktop_computer.Windows(self.renderer)

        Window.add_window(1, x_pos=20, y_pos=1)
        Window.add_window(0, x_pos=55, y_pos=15)
        Window.add_window(2, x_pos=30, y_pos=35)

        self.clear()

        self.draw_all_windows(Window)

        while desktop_closed == False:
            key = self.renderer.stdscr.getch()
            self.renderer.refresh()
            self.draw_all_windows(Window)
            if key == curses.KEY_MOUSE:
                mousepos = curses.getmouse()
            for w in range(len(Window.windows)):
                if Window.windows[w] != None:
                    if key == curses.KEY_MOUSE:
                        if Window.check_on_click_move(mousepos[1],mousepos[2], Window.windows[w][1], Window.windows[w][2], Window.windows[w][3]):
                            window_moving = [True, Window.windows[w], w]
                            self.clear()
                            self.draw_all_windows(Window)

                #This check is at the end because it manage the Deletion of the Window
                if key == curses.KEY_MOUSE:
                    if Window.check_on_click_close(mousepos[1],mousepos[2], Window.windows[w][1], Window.windows[w][2], Window.windows[w][3]):
                        Window.remove_window(w)
                        self.clear()
                        self.draw_all_windows(Window)
                        break

            for di in range(len(Window.desktop_buttons)):
                if key == curses.KEY_MOUSE:
                    if Window.check_on_desktop_icon_open(mousepos[1],mousepos[2],Window.desktop_icons_loc[di][0],Window.desktop_icons_loc[di][1]-1,Window.desktop_icons_loc[di][2],Window.desktop_icons_loc[di][3], Window.desktop_buttons[di]):
                        Window.add_window(Window.desktop_buttons[di], x_pos=mousepos[1], y_pos=mousepos[2])
                        self.clear()
                        self.draw_all_windows(Window)

            while window_moving[0]:
                key = self.renderer.stdscr.getch()
                self.renderer.refresh()
                self.clear()

                mousepos = curses.getmouse()
                window_moving[1][1] = mousepos[1]
                window_moving[1][2] = mousepos[2]

                #Check if too High Coordinate
                if window_moving[1][2]+window_moving[1][4] > self.renderer.max_y:
                    window_moving[1][2] = self.renderer.max_y - window_moving[1][4]
                if window_moving[1][2] < 0:
                    window_moving[1][2] = 0
                if window_moving[1][1]+window_moving[1][3] > self.renderer.max_x:
                    window_moving[1][1] = self.renderer.max_x-window_moving[1][3]
                if window_moving[1][1] < 0:
                    window_moving[1][1] = 0

                if key == curses.KEY_MOUSE:
                    Window.remove_window(window_moving[2])

                    Window.add_window(window_moving[1][0], window_moving[1][1], window_moving[1][2], window_moving[1][3], window_moving[1][4])

                    window_moving = [False, window_moving[1], len(Window.windows)]
                    self.renderer.refresh()
                    self.clear()

                self.draw_all_windows(Window)

            if key==27:
                desktop_closed = True




    def start(self) -> None:  # pylint: disable=R0914
        # TODO: Programming language name: Parcel-3
        """
        Shows the init sequence of the first computer.

        :return:
        """

        animation = start_computer_bios.create_animation(self.renderer)
        #y_pos = animation.start()

        font_logo = (curses.color_pair(0) | curses.A_ITALIC | curses.A_BOLD | curses.A_BLINK)
        self.addinto_all_centred(LOGO_START, 0.05)
        self.addinto_all_centred(LOGO_DONE, color_pair=font_logo)

        animation = start_computer_boot.create_animation(self.renderer)
        #animation.start(y_pos + 1) # leave a blank line

        #desktop_computer.pygame.mixer.music.load("/home/toufoumaster/Bureau/RPG Kaïs/mind_control_rpg/assets/ether_industries/audio/test.mp3")
        #desktop_computer.pygame.mixer.music.play(-1)

        self.clear()

        self.desktop()
