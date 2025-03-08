from build123d import *
from ocp_vscode import *
from multiconnect.multiconnect import Multiconnect




plate_length=200
plate_width=100
plate_height=5

with BuildPart() as plate:
    Box(plate_length,plate_width,plate_height)
    fillet(plate.edges().filter_by(Axis.Z), radius=5)
    with Locations(plate.faces().sort_by(Axis.Z)[0]):
        Multiconnect(plate_length, mode=Mode.SUBTRACT)

top_face = plate.faces().sort_by(Axis.Z)[-1]
with BuildPart() as text_part:
    with BuildSketch(top_face) as text_sk:
        #This requires  `cp /mnt/c/Windows/Fonts/AGENCYB.TTF ~/.fonts/` under Linux
        Text("2025", font_size=80, font="Agency FB", align=(Align.CENTER, Align.CENTER))
    extrude(amount=2, mode=Mode.ADD)

plate.part.label="plate"
text_part.part.label="text"
combined = Compound(label="assembly", children=[plate.part, text_part.part])
show(combined)
export_step(combined, "year_number.step")