from build123d import *
from ocp_vscode import *
from multiconnect.multiconnect import Multiconnect

picture_width = 110
picture_length = 160
picture_tolerance = 3

picture_width += picture_tolerance
picture_length += picture_tolerance

horizontal_mounting = False
vertical_mounting = True

edge_width = 40
edge_length = 27
edge_pts= [
    (0,0),
    (edge_length,0),
    (edge_length,edge_width),
    #(edge_length-6,edge_width),
    #(0,6),
    (0,0)
]

frame_height=5.5
holding_height= 5
holding_width = 6

notch_remaining_holding_width = 1.5

with BuildLine() as notch_line:
        p = Polyline([(holding_width,0), (notch_remaining_holding_width,-holding_height), (holding_width, -holding_height), (holding_width,0)])

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
    long_face_plane = Plane(origin=notch_start_edge + (-holding_width,0), x_dir=(0,1,0), z_dir=long_face.normal_at())
    
    with BuildSketch(long_face_plane) as picture_notch:
        with BuildLine() as lfline:
            add(notch_line)
        make_face()
    n1 = extrude(amount=-(edge_length), mode=Mode.SUBTRACT)

    short_face = edge.faces().sort_by(Axis.Y)[0]
    short_face_plane = Plane(origin=notch_start_edge + (0,holding_width), x_dir=(-1,0,0), z_dir=-short_face.normal_at())
    with BuildSketch(short_face_plane) as picture_notch:
        with BuildLine() as sfline:
            add(notch_line)
        make_face()
    n2 = extrude(amount=(edge_width), mode=Mode.SUBTRACT)

#TODO: Ugly code duplication from above - didn't know how to else combine the needed subtraction / intersection operations
#      necessary to get a proper notch edge
with BuildPart() as notch_edge:
    long_face_plane = Plane(origin=notch_start_edge , x_dir=(0,1,0), z_dir=long_face.normal_at())
    short_face_plane = Plane(origin=notch_start_edge, x_dir=(-1,0,0), z_dir=-short_face.normal_at())
    with BuildSketch(long_face_plane) as picture_notch:
        with BuildLine() as lfline:
            add(notch_line)
        make_face()
    n1 = extrude(amount=-(edge_length), mode=Mode.ADD)
    with BuildSketch(short_face_plane) as picture_notch:
        with BuildLine() as sfline:
            add(notch_line)
        make_face()
    n2 = extrude(amount=(edge_width), mode=Mode.INTERSECT)


with edge:
    add(notch_edge, mode=Mode.SUBTRACT)
    
  



cross_length = 100
cross_width = 25

#TODO: Remove hardcoded 1.5 (aka notch_wall)
distance_to_edge_x=picture_length/2 - (edge_length-1.5)
distance_to_edge_y=picture_width/2 + 1.5
print(distance_to_edge_x)
print(distance_to_edge_y)
with BuildPart() as frame:
    if(horizontal_mounting):
        Box(100, 25, frame_height, align=((Align.CENTER, Align.CENTER, Align.MIN)))
    if(vertical_mounting):
        vmount_box = Box(25, 100, frame_height, align=((Align.CENTER, Align.CENTER, Align.MIN)))
    top_face = frame.faces().sort_by(Axis.Z)[0]
    cross_conn_vtx = frame.edges().group_by(Axis.X)[-1].sort_by(Axis.Y)[0].vertices()[0]
    #TODO: This needs to auto calculate depending on picture size. Probably by using the outer face (via align?) and subtracting
    # the disctance to the inner notch edge
    with Locations((distance_to_edge_x,-distance_to_edge_y)):
        e = add(edge)
        mirror(e, about=Plane.XZ)
        e2 = mirror(e, about=Plane.YZ)
        mirror(e2, about=Plane.XZ)
    #TODO: find the face properly, instead of selection magic 2
    edge_face = e.faces().sort_by_distance((distance_to_edge_x/2,0,frame_height/2))[0]
    edge_conn = edge_face.center()
    print(edge_conn)
    print(frame_height)
    
    connector_width = 10
    with BuildLine() as cline:
        if(horizontal_mounting):
            #Connect to the edge of the cross but move point 5 "inwards" to take care of slant.
            l = Line((cross_conn_vtx.X-connector_width/2-5,cross_conn_vtx.Y+5), (edge_conn.X,edge_conn.Y))
        else:
            conn_target_face = vmount_box.faces().sort_by(Axis.X)[-1]
            l = Line((conn_target_face.center().X-10, conn_target_face.center().Y+5), (edge_conn.X,edge_conn.Y))
    #TODO: Fix this manual subtraction. shouldn't be necessary.
    with BuildSketch(Plane(origin=edge_face.center() - (0,0,1), z_dir=edge_face.normal_at())) as crect:
        r = Rectangle(connector_width, frame_height)
    connector = sweep()
    mirror(connector, about=Plane.XZ)
    c2 = mirror(connector, about=Plane.YZ)
    mirror(c2, about=Plane.XZ)


    with Locations(top_face):
        with Locations((0,5,0)):
            if(horizontal_mounting):
                Multiconnect(47, mode=Mode.SUBTRACT, rotation=(0,0,0))
            if(vertical_mounting):
                Multiconnect(47, mode=Mode.SUBTRACT, rotation=(0,0,90))
        




show(frame)
#show(edge_plate)
#show(picture_notch)
#show_all()
export_step(frame.part, "picture_frame.step")