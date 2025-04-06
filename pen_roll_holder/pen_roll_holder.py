from build123d import *
from ocp_vscode import *

base_length = 250
base_width = 80
base_height = 7

roll_length = 36
roll_width = 33
roll_height = 45
roll_spacing = 2
roll_strength = 3

with BuildPart() as roll:
    Box(roll_length,roll_width,roll_height,align=(Align.CENTER, Align.CENTER,Align.MIN))
    fillet(roll.edges().group_by(Axis.Z)[1], radius=15)
    top_face = roll.faces().sort_by(Axis.Z)[-1]
    bottom_face = roll.faces().sort_by(Axis.Z)[0]
    offset(amount=-roll_strength, openings=[top_face, bottom_face])
    #Get new top_face
    top_face = roll.faces().sort_by(Axis.Z)[-1]
    chamfer(top_face.edges().sort_by_distance((0,0))[0], length= 2.0)


with BuildPart() as holder:
    base = Box(base_length,base_width,base_height)
    fillet(base.edges().filter_by(Axis.Z), radius=5)
    with Locations(holder.faces().sort_by(Axis.Z)[-1]):
        with GridLocations(roll_length+roll_spacing,0,6,1):
            add(roll)


show(holder)
export_stl(holder.part, "holder.stl")