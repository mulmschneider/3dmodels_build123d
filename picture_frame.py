from build123d import *
from ocp_vscode import *
from multiconnect.multiconnect import Multiconnect

picture_width = 110
picture_length = 160
picture_tolerance = 3

picture_width += picture_tolerance
picture_length += picture_tolerance


edge_width = 27
edge_length = 27
edge_pts= [
    (0,0),
    (edge_length,0),
    (edge_length,edge_width),
 #   (edge_length-6,edge_width),
 #   (0,6),
    (0,0)
]

frame_height=5.5
holding_height= 5
holding_width = 6

with BuildLine() as notch_line:
        p = Polyline([(holding_width,0), (1.5,-holding_height), (holding_width, -holding_height), (holding_width,0)])

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

    long_face = edge.faces().sort_by(Axis.X)[-1]
    notch_start_edge = long_face.vertices().group_by(Axis.Z)[-1].sort_by(Axis.Y)[0]
    long_face_plane = Plane(origin=notch_start_edge + (-6,0), x_dir=(0,1,0), z_dir=long_face.normal_at())
    
    #TODO: strange thingy in the corner. Probably need to design a seperate shape (via intersect) 
    # just for the corner that we subtract here?
    with BuildSketch(long_face_plane) as picture_notch:
        with BuildLine() as lfline:
            add(notch_line)
        make_face()
    extrude(amount=-(edge_length-1.5), mode=Mode.SUBTRACT)

    short_face = edge.faces().sort_by(Axis.Y)[0]
    short_face_plane = Plane(origin=notch_start_edge + (0,1.5), x_dir=(-1,0,0), z_dir=-short_face.normal_at())
    with BuildSketch(short_face_plane) as picture_notch:
        with BuildLine() as sfline:
            add(notch_line)
        make_face()
    extrude(amount=(edge_width-1.5), mode=Mode.SUBTRACT)
    
  



cross_length = 100
cross_width = 25

#TODO: Remove hardcoded 1.5 (aka notch_wall)
distance_to_edge_x=picture_length/2 - (edge_length-1.5)
distance_to_edge_y=picture_width/2 + 1.5
print(distance_to_edge_x)
print(distance_to_edge_y)
with BuildPart() as frame:

# === Create Edges ====

    #TODO: Refactor so that we start with ell, so that all coords are positive (making alignment etc more consistent)
    with Locations((distance_to_edge_x,-distance_to_edge_y)):
        elr = add(edge)
        eur= mirror(elr, about=Plane.XZ)
        ell = mirror(elr, about=Plane.YZ)
        eul = mirror(ell, about=Plane.XZ)
    
# === Create Multiconnect "Cross" ====    

    long_cross_starting_vtx = ell.vertices().group_by(Axis.Y)[-1].group_by(Axis.Z)[0].sort_by(Axis.X)[0]
    short_cross_starting_vtx = eur.vertices().group_by(Axis.Y)[-1].group_by(Axis.Z)[0].sort_by(Axis.X)[0]
    short_cross_starting_vtx += (0,-8,0)
    with Locations(long_cross_starting_vtx):
        Box(100, 23, frame_height, align=((Align.MIN, Align.MIN, Align.MIN)))
        Multiconnect(50, mode=Mode.SUBTRACT, rotation=(0,0,0), align=((Align.MIN, Align.MIN, Align.MIN)))
    with Locations(short_cross_starting_vtx):
        b = Box(23, 60, frame_height, align=((Align.MAX, Align.MAX, Align.MIN)))
        short_cross_bottom = b.faces().sort_by(Axis.Z)[0]
    with Locations(Plane(short_cross_bottom, x_dir=(0,1,0), z_dir=short_cross_bottom.normal_at())):
        m = Multiconnect(100, mode=Mode.SUBTRACT)
    top_face = frame.faces().sort_by(Axis.Z)[0]
    cross_conn_vtx = frame.edges().group_by(Axis.X)[-1].sort_by(Axis.Y)[0].vertices()[0]

# === Connect Edges to "Cross" ====

    #TODO: find the face properly, instead of selection magic 2
    edge_face = elr.faces().sort_by_distance((0,0))[0]
    edge_conn = edge_face.center()
    
    connector_width = 10
    with BuildLine() as cline:
        #Connect to the edge of the cross but move point 5 "inwards" to take care of slant.
        l = Line((cross_conn_vtx.X-connector_width/2-2.5,cross_conn_vtx.Y+5), (edge_conn.X,edge_conn.Y))
    #TODO: Fix this manual subtraction. shouldn't be necessary.
    with BuildSketch(Plane(origin=edge_face.center() - (0,0,1), z_dir=edge_face.normal_at())) as crect:
        r = Rectangle(connector_width, frame_height)
    connector = sweep()
    mirror(connector, about=Plane.XZ)
    c2 = mirror(connector, about=Plane.YZ)
    mirror(c2, about=Plane.XZ)


    #with Locations(top_face):
        
        




show(frame, short_cross_starting_vtx)
#show(edge_plate)
#show(picture_notch)
#show_all()
export_step(frame.part, "picture_frame.step")