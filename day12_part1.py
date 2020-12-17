from manim import *
config.max_files_cached = 1000

class Day12Part1(GraphScene, MovingCameraScene):
    CONFIG = {
            "x_min": 0,
            "x_max": 20,
            "x_axis_width": 8,
            "x_tick_frequency": 1,
            "x_axis_label": None,
            "y_min": 0,
            "y_max": 15,
            "y_axis_height": 6,
            "y_tick_frequency": 1,
            "y_axis_label": None,
            "axes_color": BLACK,
            "graph_origin": 2 * LEFT + 2.5 * DOWN,
            }
    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)
    def construct(self):
        # Setup Grid
        self.camera_frame.save_state()
        self.setup_axes(animate=False)
        self.show_grid(self.x_min, self.x_max, self.x_tick_frequency,
                self.y_min, self.y_max, self.y_tick_frequency)
        self.current_location = [0, 0]
        # setup boats
        self.create_boats()
        self.directions = ['east', 'south', 'west', 'north']
        self.direction_index = 0
        # north examples
        north_directions = {
                "east": {
                    "start_location": [0, 0],
                    "movement": "N4"
                }, 
                "south": {
                    "start_location" : [3, 5],
                    "movement": "N2"
                },
                "west": {
                    "start_location" : [20, 8],
                    "movement": "N5"
                },
                "north": {
                    "start_location": [15, 0],
                    "movement": "N3"
                }
            }
        self.north_examples(north_directions)
         # south examples
        south_directions = {
                "east": {
                    "start_location": [0, 10],
                    "movement": "S4"
                }, 
                "south": {
                    "start_location" : [3, 5],
                    "movement": "S2"
                },
                "west": {
                    "start_location" : [20, 8],
                    "movement": "S5"
                },
                "north": {
                    "start_location": [15, 3],
                    "movement": "S3"
                }
            }
        self.south_examples(south_directions)
        # east examples
        east_directions = {
                "east": {
                    "start_location": [0, 10],
                    "movement": "E4"
                }, 
                "south": {
                    "start_location" : [3, 5],
                    "movement": "E2"
                },
                "west": {
                    "start_location" : [15, 8],
                    "movement": "E5"
                },
                "north": {
                    "start_location": [15, 3],
                    "movement": "E3"
                }
            }
        self.show_east_examples(east_directions)
        # west examples
        west_directions = {
                "east": {
                    "start_location": [4, 10],
                    "movement": "W4"
                }, 
                "south": {
                    "start_location" : [3, 5],
                    "movement": "W2"
                },
                "west": {
                    "start_location" : [15, 8],
                    "movement": "W5"
                },
                "north": {
                    "start_location": [15, 3],
                    "movement": "W3"
                }
            }
        self.west_examples(west_directions)
        # left examples
        left_directions = {
                "east": {
                    "start_location": [0, 0],
                    "movement": "L90"
                }, 
                "north": {
                    "start_location" : [3, 5],
                    "movement": "L180"
                },
                "west": {
                    "start_location" : [10, 8],
                    "movement": "L270"
                },
                "south": {
                    "start_location": [15, 0],
                    "movement": "L90"
                }
            }
        self.left_examples(left_directions)
        # right examples
        right_directions = {
                "east": {
                    "start_location": [0, 0],
                    "movement": "R90"
                }, 
                "south": {
                    "start_location" : [3, 5],
                    "movement": "R180"
                },
                "west": {
                    "start_location" : [10, 8],
                    "movement": "R270"
                },
                "north": {
                    "start_location": [15, 0],
                    "movement": "R180"
                }
            }
        self.right_examples(right_directions)
        # forward examples
        forward_directions = {
                "east": {
                    "start_location": [0, 0],
                    "movement": "F4"
                }, 
                "south": {
                    "start_location" : [3, 5],
                    "movement": "F2"
                },
                "west": {
                    "start_location" : [20, 8],
                    "movement": "F5"
                },
                "north": {
                    "start_location": [15, 0],
                    "movement": "F3"
                }
            }
        self.forward_examples(forward_directions)


    def show_grid(self, start_x, end_x, delta_x, start_y, end_y, delta_y):
        """
        Displays the coordinates of the sea.
        """
        def get_line(s, e):
            return Line(s, e, color=WHITE, stroke_width=1)
        ctp = self.coords_to_point
        v_lines = Group(*
                [get_line(ctp(x, start_y), ctp(x, end_y)) 
                    for x in np.arange(start_x, end_x + delta_x, delta_x)]
                )
        h_lines = Group(*
                [get_line(ctp(start_x, y), ctp(end_x, y)) 
                    for y in np.arange(start_y, end_y + delta_y, delta_y)]
                )
        self.add(v_lines, h_lines)

    def create_boats(self):
        """
        Create_boats creats boat objects facing each of the four cardinal
            directions.  Boats are added as members of object.
        Accepts:
            None
        Returns:
            None
        """
        # svg_boat = SVGMobject('boat.svg')
        # for layer in svg_boat:
            # self.add(layer)
            # self.wait(2)
        # boat = SVGMobject(filename)
        self.boat_facing_west = ImageMobject('boat_left.png')
        self.boat_facing_east = ImageMobject('boat_right.png')
        self.boat_facing_north = ImageMobject('boat_up.png')
        self.boat_facing_south = ImageMobject('boat_down.png')
        for boat in [
                self.boat_facing_west, 
                self.boat_facing_east, 
                self.boat_facing_north,
                self.boat_facing_south
                ]:
            boat.set_color(BLUE_E)
            boat.scale(.2)
            self.boat_delta = 0.0
        self.boats = {'east':
                {
                    'boat': self.boat_facing_east, 
                    'movement': self.update_cam_boat_facing_east
                    }, 'south':
                {
                    'boat': self.boat_facing_south,
                    'movement': self.update_cam_boat_facing_south
                    }, 'west':
                {
                    'boat': self.boat_facing_west,
                    'movement': self.update_cam_boat_facing_west
                    }, 'north':
                {
                    'boat': self.boat_facing_north,
                    'movement': self.update_cam_boat_facing_north
                    }
                }

    def update_cam_boat_facing_east(self, cam):
        """
        Camera updater.  When attached to camera object, it makes camera
            follow east-facing boat
        """
        cam.move_to(self.boat_facing_east.get_center())

    def update_cam_boat_facing_south(self, cam):
        """
        Camera updater.  When attached to camera object, it makes camera
            follow south-facing boat
        """
        cam.move_to(self.boat_facing_south.get_center())

    def update_cam_boat_facing_west(self, cam):
        """
        Camera updater.  When attached to camera object, it makes camera
            follow west-facing boat
        """
        cam.move_to(self.boat_facing_west.get_center())

    def update_cam_boat_facing_north(self, cam):
        """
        Camera updater.  When attached to camera object, it makes camera
            follow north-facing boat
        """
        cam.move_to(self.boat_facing_north.get_center())

    def move_boat_horizontal(self, start_location, movement):
        """
        Move_boat_horizontal takes the current location and returns 
            three graphs:
                graph for line
                graph for boat path
                brace
        Accepts:
            start_location (list of ints): current location
            movement (int): amount of movement
        Returns:
            Tuple of graph objects
        """
        curr_graph = self.get_graph(
                lambda x: start_location[1],
                color = RED,
                x_min = start_location[0],
                x_max = start_location[0] + movement
                )
        boat_graph = self.get_graph(
                lambda x: start_location[1] + self.boat_delta,
                color = RED,
                x_min = start_location[0],
                x_max = start_location[0] + movement
                )
        brace = Brace(curr_graph)
        return (curr_graph, boat_graph, brace)

    def move_boat_vertical(self, start_location, movement):
        """
        Move_boat_vertical takes the current location and returns three 
            objects:
                a graph for the line
                a graph for the boat path
                a brace
        Accepts:
            start_location (list of ints): current location
        Returns:
            Tuple of objects
        """
        ctp = self.coords_to_point
        curr_graph = Line( self.coords_to_point(start_location[0], 
            start_location[1]), self.coords_to_point(start_location[0],
                start_location[1] + movement), color=RED)
        #positive movement means "north", negative means "south" adjust boat
        if movement >= 0:
            brace_direction = RIGHT
            this_boat_delta = -1 * self.boat_delta
        else:
            brace_direction = LEFT
            this_boat_delta = self.boat_delta
        boat_graph = Line( self.coords_to_point(
                    start_location[0] + this_boat_delta, 
                    start_location[1]), 
                self.coords_to_point(start_location[0] + this_boat_delta,
                    start_location[1] + movement))
        brace = Brace(curr_graph, direction=brace_direction)
        return (curr_graph, boat_graph, brace)

    def move_camera_around_group(self, group, border_buffer = 1.2):
        """
        Move_camera_around_group will recenter the camera around the group of
            objects, scaled to fit around the width and the height of the
            object.
        Accepts:
            group (Group): group of MObjects
            border_buffer (int = 1.2): Border around objects.  Defaults to 
                1.2 = 120%
        Returns:
            None -- moves camera
        """
        camera_width = self.camera_frame.get_width()
        camera_height = self.camera_frame.get_height()
        needed_width = group.get_width() * border_buffer
        needed_height = group.get_height() * border_buffer
        width_change = needed_width / camera_width
        height_change = needed_height / camera_height
        if (width_change >= height_change):
            self.play(
                    self.camera_frame.set_width, needed_width,
                    self.camera_frame.move_to, group.get_center()
                    )
        else:
            self.play(
                self.camera_frame.set_height,needed_height,
                self.camera_frame.move_to, group.get_center()
                )

    def north_examples(self, directions):
        """
        North_examples shows the boat moving north.
        Accepts:
            directions (dictionary): Directions in dictionary form:
                "boat": {
                    "start_location": [ int, int]
                    "movement": str ("N<int>") 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in directions.keys():
            self.camera_frame.save_state()
            movement = int(directions[key]["movement"][1:])
            start_location = directions[key]["start_location"]
            boat_location = [start_location[0] - self.boat_delta, 
                    start_location[1]]
            (curr_graph, boat_graph, brace) = self.move_boat_vertical(
                    start_location, movement)
            end_location = [ start_location[0], 
                        start_location[1] + movement]
            animation_parameters = {
                    "run_time": 5,
                    "rate_func": linear
                    }
            current_boat = self.boats[key]['boat'] 
            current_boat.move_to(self.coords_to_point(boat_location[0], boat_location[1]))
            self.current_cam_update = self.boats[key]['movement']
            bracetext=brace.get_text(directions[key]['movement'])
            bracetext.set_color(RED)
            bracetext.bg=SurroundingRectangle(bracetext, color=BLACK, 
                    fill_color=BLACK, fill_opacity=1)
            self.add(current_boat, bracetext.bg, bracetext)
            self.wait(1)
            self.play(self.camera_frame.scale,0.3,self.camera_frame.move_to,current_boat)
            self.camera_frame.add_updater(self.current_cam_update)
            self.play(
                    MoveAlongPath(current_boat, boat_graph),
                    ShowCreation(curr_graph),
                    **animation_parameters
                    )
            self.camera_frame.remove_updater(self.current_cam_update)
            this_group = Group(current_boat, curr_graph, brace, bracetext)
            self.move_camera_around_group(this_group)
            self.add(brace)
            self.wait(2)
            for obj in [current_boat, curr_graph, brace, 
                    bracetext, bracetext.bg]:
                this_scene_objects.append(obj)
            self.play(Restore(self.camera_frame))
        self.wait(5)
        for obj in this_scene_objects:
            self.remove(obj)

    def south_examples(self, directions):
        """
        South_examples shows the boat moving south.
        Accepts:
            directions (dictionary): Directions in dictionary form:
                "boat": {
                    "start_location": [ int, int]
                    "movement": str ("F<int>") 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in directions.keys():
            self.camera_frame.save_state()
            movement = int(directions[key]["movement"][1:])
            start_location = directions[key]["start_location"]
            boat_location = [start_location[0] - self.boat_delta, 
                    start_location[1]]
            (curr_graph, boat_graph, brace) = self.move_boat_vertical(
                    start_location, -1 * movement)
            end_location = [ start_location[0], 
                        start_location[1] + movement]
            animation_parameters = {
                    "run_time": 3,
                    "rate_func": linear
                    }
            current_boat = self.boats[key]['boat'] 
            current_boat.move_to(self.coords_to_point(boat_location[0], boat_location[1]))
            self.current_cam_update = self.boats[key]['movement']
            bracetext=brace.get_text(directions[key]['movement'])
            bracetext.set_color(RED)
            bracetext.bg=SurroundingRectangle(bracetext, color=BLACK, 
                    fill_color=BLACK, fill_opacity=1)
            self.add(current_boat, bracetext.bg, bracetext)
            this_group = Group(current_boat, curr_graph, brace, bracetext)
            self.wait(1)
            self.play(self.camera_frame.scale,0.3,self.camera_frame.move_to,current_boat)
            self.camera_frame.add_updater(self.current_cam_update)
            self.play(
                    MoveAlongPath(current_boat, boat_graph),
                    ShowCreation(curr_graph),
                    **animation_parameters
                    )
            self.camera_frame.remove_updater(self.current_cam_update)
            self.move_camera_around_group(this_group)
            self.add(brace)
            self.wait(2)
            for obj in [current_boat, curr_graph, 
                    brace, bracetext, bracetext.bg]:
                this_scene_objects.append(obj)
            self.play(Restore(self.camera_frame))
        self.wait(5)
        for obj in this_scene_objects:
            self.remove(obj)

    def boat_moves_east(self, boat, movement_dictionary, show_detail = True):
        """
        East_movement selects the correct boat, creates correct graph and correct
            camera frame.   Optionally also adds explanatory text (camera frame 
            altered to include text).
        Accepts:
            boat (ImageMobject instance): boat
            movement_dictionary (dict): Format: {
                'boat' (str): boat object identifier,
                'start_location' (list of ints): beginning location [x,y],
                'movement' (str): 'E<#>'
                }
            show_detail (bool): Whether or not explanatory detail should be shown
        Returns:
            List of objects added to graph. Also adds video and alters camera frame
        """
        movement = int(movement_dictionary['movement'][1:])
        start_location = movement_dictionary['start_location']
        boat_start = [start_location[0] - self.boat_delta,
                start_location[1]]
        (curr_graph, boat_graph, brace) = self.move_boat_horizontal(
                start_location, movement)
        boat_end = [boat_start[0] + movement, boat_start[1]]
        animation_parameters = {
                "run_time": 3,
                "rate_func": linear
                }
        current_boat = boat.copy()
        current_boat.move_to(self.coords_to_point(boat_start[0], boat_start[1]))
        end_boat = current_boat.copy()
        end_boat.move_to(self.coords_to_point(boat_end[0], boat_end[1]))
        return_objects = [current_boat, curr_graph]
        frame_group = Group(current_boat, end_boat, curr_graph)
        if show_detail is True:
            bracetext = brace.get_text(movement_dictionary['movement'])
            bracetext.set_color(RED)
            bracetext.bg=SurroundingRectangle(bracetext, color=BLACK,
                    fill_color=BLACK, fill_opacity=1)
            self.add(current_boat, bracetext.bg, bracetext)
            frame_group = Group (*frame_group, brace, bracetext, bracetext.bg)
            return_objects += [bracetext.bg, brace, bracetext]
        else:
            self.add(current_boat)
        self.move_camera_around_group(frame_group)
        self.wait(1)
        self.play(
                MoveAlongPath(current_boat, boat_graph),
                ShowCreation(curr_graph),
                **animation_parameters
                )
        if show_detail is True:
            self.add(brace)
        self.wait(2)
        return return_objects
    
    def show_east_examples(self, directions):
        """
        East_examples shows the boat moving east.
        Accepts:
            directions (dictionary): Directions in dictionary form:
                "boat": {
                    "start_location": [ int, int]
                    "movement": str ("E<int>") 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in directions.keys():
            self.camera_frame.save_state()
            this_boat = self.boats[key]['boat']
            this_key_objects = self.boat_moves_east(this_boat, directions[key], True)
            this_scene_objects += this_key_objects
            self.play(Restore(self.camera_frame))
        self.wait(5)
        for obj in this_scene_objects:
            self.remove(obj)

    def west_examples(self, directions):
        """
        West_examples shows the boat moving west.
        Accepts:
            directions (dictionary): Directions in dictionary form:
                "boat": {
                    "start_location": [ int, int]
                    "movement": str ("W<int>") 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in directions.keys():
            self.camera_frame.save_state()
            movement = int(directions[key]["movement"][1:])
            start_location = directions[key]["start_location"]
            boat_location = [start_location[0] - self.boat_delta, 
                    start_location[1]]
            (curr_graph, boat_graph, brace) = self.move_boat_horizontal(
                    start_location, -1 * movement)
            end_location = [ start_location[0], 
                        start_location[1] + movement]
            animation_parameters = {
                    "run_time": 3,
                    "rate_func": linear
                    }
            current_boat = self.boats[key]['boat'] 
            current_boat.move_to(self.coords_to_point(boat_location[0], boat_location[1]))
            self.current_cam_update = self.boats[key]['movement']
            bracetext=brace.get_text(directions[key]['movement'])
            bracetext.set_color(RED)
            bracetext.bg=SurroundingRectangle(bracetext, color=BLACK, 
                    fill_color=BLACK, fill_opacity=1)
            self.add(current_boat, bracetext.bg, bracetext)
            self.wait(1)
            self.play(self.camera_frame.scale,0.3,self.camera_frame.move_to,current_boat)
            self.camera_frame.add_updater(self.current_cam_update)
            self.play(
                    MoveAlongPath(current_boat, boat_graph),
                    ShowCreation(curr_graph),
                    **animation_parameters
                    )
            self.camera_frame.remove_updater(self.current_cam_update)
            this_group = Group(current_boat, curr_graph,
                    brace, bracetext)
            self.move_camera_around_group(this_group)
            self.add(brace)
            self.wait(2)
            for obj in [current_boat, curr_graph, 
                    brace, bracetext, bracetext.bg]:
                this_scene_objects.append(obj)
            self.play(Restore(self.camera_frame))
        self.wait(5)
        for obj in this_scene_objects:
            self.remove(obj)

    def left_examples(self, directions):
        """
        Left_examples shows the boat rotating left (counterclockwise)
        Accepts:
            directions (dictionary): Directions in dictionary form:
                "boat": {
                    "start_location": [ int, int]
                    "movement": str ("L<int>") 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in directions.keys():
            self.camera_frame.save_state()
            movement = int(directions[key]["movement"][1:])
            start_location = directions[key]["start_location"]
            boat_location = [start_location[0] - self.boat_delta, 
                    start_location[1]]
            animation_parameters = {
                    "run_time": 3,
                    "rate_func": linear
                    }
            current_boat = self.boats[key]['boat'].copy()
            current_boat.move_to(self.coords_to_point(boat_location[0], boat_location[1]))
            self.play(self.camera_frame.scale,0.3,self.camera_frame.move_to,current_boat)
            rotate_text = Text(directions[key]["movement"])
            rotate_text.move_to(current_boat.get_center() + RIGHT*1.5)
            rotate_text.set_color(RED)
            rotate_text.bg=SurroundingRectangle(rotate_text, color=BLACK, 
                    fill_color=BLACK, fill_opacity=1)
            self.add(current_boat, rotate_text.bg, rotate_text)
            self.wait(1)
            self.play(
                    Rotating(current_boat, radians = PI * movement / 180,
                        about_point=current_boat.get_center()),
                    **animation_parameters
                    )
            self.wait(2)
            for obj in [current_boat, rotate_text, rotate_text.bg]:
                this_scene_objects.append(obj)
            self.play(Restore(self.camera_frame))
        self.wait(5)
        for obj in this_scene_objects:
            self.remove(obj)

    def right_examples(self, directions):
        """
        Left_examples shows the boat rotating right (clockwise)
        Accepts:
            directions (dictionary): Directions in dictionary form:
                "boat": {
                    "start_location": [ int, int]
                    "movement": str ("L<int>") 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in directions.keys():
            self.camera_frame.save_state()
            movement = int(directions[key]["movement"][1:])
            start_location = directions[key]["start_location"]
            boat_location = [start_location[0] - self.boat_delta, 
                    start_location[1]]
            animation_parameters = {
                    "run_time": 3,
                    "rate_func": linear
                    }
            current_boat = self.boats[key]['boat'].copy()
            current_boat.move_to(self.coords_to_point(boat_location[0], boat_location[1]))
            self.play(self.camera_frame.scale,0.3,self.camera_frame.move_to,current_boat)
            rotate_text = Text(directions[key]["movement"])
            rotate_text.move_to(current_boat.get_center() + RIGHT*1.5)
            rotate_text.set_color(RED)
            rotate_text.bg=SurroundingRectangle(rotate_text, color=BLACK, 
                    fill_color=BLACK, fill_opacity=1)
            self.add(current_boat, rotate_text.bg, rotate_text)
            self.wait(1)
            self.play(
                    Rotating(current_boat, radians = -1 * PI * movement / 180,
                        about_point=current_boat.get_center()),
                    **animation_parameters
                    )
            self.wait(2)
            for obj in [current_boat, rotate_text, rotate_text.bg]:
                this_scene_objects.append(obj)
            self.play(Restore(self.camera_frame))
        self.wait(5)
        for obj in this_scene_objects:
            self.remove(obj)



    def forward_examples(self, directions):
        """
        Forward_examples shows the boat moving forward.
        Accepts:
            directions (dictionary): Directions in dictionary form:
                "direction": {
                    "start_location": [ int, int]
                    "movement": str ("F<int>") 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in directions.keys():
            self.camera_frame.save_state()
            movement = int(directions[key]["movement"][1:])
            start_location = directions[key]["start_location"]
            if key in ["east", "west"]:
                if key == "west":
                    movement *= -1
                (curr_graph, boat_graph, brace)  = self.move_boat_horizontal(
                        start_location, movement)
                end_location = [ start_location[0] + movement, 
                        start_location[1]]
                boat_location = [start_location[0], start_location[1] + self.boat_delta]
            else:
                if key == "south":
                    movement *= -1
                    boat_location = [start_location[0] + self.boat_delta, start_location[1]]
                else:
                    boat_location = [start_location[0] - self.boat_delta, start_location[1]]
                (curr_graph, boat_graph, brace) = self.move_boat_vertical(start_location,
                        movement)
                end_location = [ start_location[0], 
                        start_location[1] + movement]
            animation_parameters = {
                    "run_time": 3,
                    "rate_func": linear
                    }
            current_boat = self.boats[key]['boat'] 
            current_boat.move_to(self.coords_to_point(boat_location[0], boat_location[1]))
            self.current_cam_update = self.boats[key]['movement']
            bracetext=brace.get_text(directions[key]['movement'])
            bracetext.set_color(RED)
            bracetext.bg=SurroundingRectangle(bracetext, color=BLACK, 
                    fill_color=BLACK, fill_opacity=1)
            self.add(current_boat, bracetext.bg, bracetext)
            self.wait(1)
            self.play(self.camera_frame.scale,0.3,self.camera_frame.move_to,current_boat)
            self.camera_frame.add_updater(self.current_cam_update)
            self.play(
                    MoveAlongPath(current_boat, boat_graph),
                    ShowCreation(curr_graph),
                    **animation_parameters
                    )
            self.camera_frame.remove_updater(self.current_cam_update)
            this_group = Group(current_boat, curr_graph, brace, bracetext)
            self.move_camera_around_group(this_group)
            self.add(brace)
            self.wait(2)
            for obj in [current_boat, curr_graph, 
                    brace, bracetext, bracetext.bg]:
                this_scene_objects.append(obj)
            self.play(Restore(self.camera_frame))
        self.wait(5)
        for obj in this_scene_objects:
            self.remove(obj)
        self.wait(1)


