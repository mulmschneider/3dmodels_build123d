from build123d import *
from ocp_vscode import *

base_length = 300
base_width = 80
base_height = 7

roll_length = 37
roll_width = 33
roll_height = 45
roll_spacing = 2
roll_strength = 3

with BuildPart() as holder:
    base = Box(base_length,base_width,base_height)
    fillet(base.edges().filter_by(Axis.Z), radius=5)
    with Locations(holder.faces().sort_by(Axis.Z)[-1]):
        with GridLocations(roll_length+roll_spacing,0,7,1):
            Box(roll_length,roll_width,roll_height,align=(Align.CENTER, Align.CENTER,Align.MIN))
            Box(roll_length-roll_strength,roll_width-2,roll_height,align=(Align.CENTER, Align.CENTER,Align.MIN),mode=Mode.SUBTRACT)
            fillet(holder.edges(Select.LAST).group_by(Axis.Z)[-1], radius=0.9)


#show_all()
show(holder)
export_stl(holder.part, "holder.stl")