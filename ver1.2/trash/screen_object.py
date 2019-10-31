"""An abstract data type which support 2D location search in a relatively efficient way"""
from functions import calc_rel_pos, find_point_loc, calc_offset
from inp_devices import MouseCommand
import math
from config import *


class TwoDLayer(object):
    """class instance should never been made directly
    self.contens = {
        "name": obj, obj_rel_pos, obj_dim
    """

    def __init__(self, **kwargs):
        raise Exception("Root class should be be created directly: {0}".format(self.__class__.__name__))

    def onclick(self, click_command, mouse_pos, offset): # mouse_pos => abs_mouse_pos
        # process mouse_pos
        # assert dynamic object will not have click option
        rel_mouse_pos = calc_rel_pos(mouse_pos, offset)
        if click_command == MouseCommand.command_d["right_clicked"]:
            return None, None
        elif rel_mouse_pos[0] < 0 or rel_mouse_pos[1] < 0 or rel_mouse_pos[0] > self.width or rel_mouse_pos[1] > self.height:
            # return OFF_FOCUS, self
            return RETURN, None
        else:  # otherwise call content button
            row, col = find_point_loc(rel_mouse_pos, self.layout)
            # return one command/ one list of commands
            # recursive call until we see a button
            if self.layout[row][col] in self.contents:
                obj, ref, dim = self.contents[self.layout[row][col]]
                if hasattr(obj, "onclick"):
                    new_offset = calc_offset(offset, ref)
                    return obj.onclick(click_command, mouse_pos, new_offset)

        return None, None

    def build_layout(self):
        # inside static object cannot fo out of the layer
        # otherwise the code will crash
        col = math.ceil(self.width/GRID_WIDTH)
        row = math.ceil(self.height/GRID_HEIGHT)
        layout = [[None for c in range(col)] for r in range(row)]

        if hasattr(self, "contents"):
            for key, (obj, pos, dim) in self.contents.items():  # O(A)
                row_tl, col_tl = find_point_loc(pos, layout)
                dim = dim[0] - GRID_WIDTH, dim[1] - GRID_HEIGHT
                row_br, col_br = find_point_loc(calc_offset(pos, dim), layout)
                assert row_tl <= row_br, "Building layout problem{0}{1}".format(row_tl, row_br)
                assert col_tl <= col_tl, "Building layout problem{0}{1}".format(col_tl, col_br)
                for r in range(row_tl, row_br + 1):
                    for c in range(col_tl, col_br + 1):
                        layout[r][c] = key

            self.layout = layout
        else:
            raise Exception("contents should be created before build_layout method is called, {0}".format(self))

        return None

    def do_hover(self):
        self.hover = True

    def un_hover(self):
        self.hover = False

    def __str__(self):
        out = ""
        for row in self.layout:
            for item in row:
                if item is None:
                    out += '-'
                else:
                    out += item.__str__()[0]
            out += "\n"
        return out
    __repr__ = __str__



