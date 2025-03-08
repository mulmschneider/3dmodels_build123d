from build123d import *
from ocp_vscode import *


outer_gap = 0.4379
angle_length = 2.5
angle_width = 2.5
inner_gap = 1.2121
inner_depth = 20.3
draw_y_offset = (inner_depth / 2.0) - angle_width
pts = [
    (0, 0),
    (0, draw_y_offset),
    (outer_gap, 0 + draw_y_offset),
    (outer_gap + angle_length, angle_width + draw_y_offset),
    (outer_gap + angle_length + inner_gap, angle_width + draw_y_offset),
    (
        outer_gap + angle_length + inner_gap,
        angle_width - (inner_depth / 2.0) + draw_y_offset,
    ),
]


class Multiconnect(BasePartObject):
    def __init__(
        self,
        length,
        rotation=(0, 0, 0),
        align=None,
        mode=Mode.ADD,
    ):
        context = BuildPart._get_context()
        with BuildPart() as multiconnect_bar:
            with BuildSketch(Plane.ZY) as ex8_sk:
                with BuildLine() as ex8_ln:
                    Polyline(pts)
                    mirror(ex8_ln.line, about=Plane.XZ)
                make_face()
            extrude(amount=length, both=True)
        multiconnect_bar.part = multiconnect_bar.part.rotate(Axis.X, 180)

        super().__init__(
            part=multiconnect_bar.part, rotation=rotation, align=align, mode=mode
        )
