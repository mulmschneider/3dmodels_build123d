from build123d import *
from ocp_vscode import *
from multiconnect.multiconnect import Multiconnect

edge_pts= [
    (0,0),
    (27,0),
    (27,40),
    (0,0)
]
frame_height=5.5
holding_height= 5
holding_width = 6

with BuildPart() as edge:
    with BuildSketch() as edge_plate:
        with BuildLine() as epline:
            Polyline(edge_pts)
        make_face()
    extrude(amount=frame_height+holding_height)
    #add edgeplate with an offset, and subtract it
    with Locations((-holding_width, holding_width, frame_height)):
        add(edge_plate)
    extrude(amount=holding_height, mode=Mode.SUBTRACT)
    hypotenuse = edge.faces().sort_by(Axis.Y)[-1]
    inner_edge_short=hypotenuse.vertices().group_by(Axis.Z)[-1][1]
    hypo_plane= Plane(hypotenuse)
    
    with Locations(hypo_plane):
        with Locations(hypo_plane.to_local_coords(inner_edge_short)):
            Box(1,1,1, align=(Align.MIN, Align.MAX, Align.MAX), mode=Mode.SUBTRACT )
    with BuildSketch() as picture_notch:
        with BuildLine() as pnline:
            #Polyline([(inner_edge_short.Y,inner_edge_short.Z+5), (inner_edge_short.Y+5,inner_edge_short.Z), (inner_edge_short.Y,inner_edge_short.Z), (inner_edge_short.Y,inner_edge_short.Z+5)])
            Polyline([(0,5), (5,0), (0,0), (0,5)])
        make_face()
    extrude(amount=-2)

    
  



cross_length = 100
cross_width = 25

with BuildPart() as frame:
    Box(100, 25, 5.5)
    Box(25, 100, 5.5)
    with Locations(frame.faces().sort_by(Axis.Z)[0]):
        Multiconnect(50, mode=Mode.SUBTRACT, rotation=(0,0,0))
        Multiconnect(50, mode=Mode.SUBTRACT, rotation=(0,0,90))





show(edge)
#show(picture_notch)
#show_all()
#export_step(frame.part, "picture_frame.step")