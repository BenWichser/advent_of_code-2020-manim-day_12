import sys
import random
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
        with open('./input.txt', 'r') as f:
            self.puzzle_input = [line[:-1] for line in f]
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
        self.current_boat = self.boats[self.directions[self.direction_index]]
        self.current_boat.move_to(self.coords_to_point(0, 0))
        # Show confusion:
        #       self.idea_title is left as "N S E W R L F" text
        #       self.title_bar is left as text divider
        self.show_confusion()
        # north description and examples
        #       self.idea_title -> self.north_title  "N"
        #       self.title_bar remains as text divider
        self.north_description()
        # south description and examples
        #       self.north_title -> self.south_title "S"
        #       self.title_bar remains as text divider
        self.south_description()
        # east description and examples
        #       self.south_title -> self.east_title "E"
        #       self.title_bar remains as text divider
        self.east_description()
        # west description and examples
        #       self.east_title -> self.west_title "W"
        #       self.title_bar remains as text divider
        self.west_description()
        # left description and examples
        #       self.west_title -> self.left_title "L"
        #       self.title_bar remains as text divider
        self.left_description()
        # right description and examples
        #       self.left_title -> self.right_title "R"
        #       self.title_bar remains as text divider
        self.right_description()
        # forward description and examples
        #       self.right_title -> self.forward_title "F"
        #       self.title_bar remains as text divider
        self.forward_description()



    def frame_camera_around_group(self, group, border_buffer = 1.2):
        """
        Frame_camera_around_group will recenter the camera around the group of
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
        self.boats = {'east': self.boat_facing_east,
                'south': self.boat_facing_south,
                'west': self.boat_facing_west,
                'north': self.boat_facing_north,
                }

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

    def move_boat(self, boat, direction, movement_dictionary, 
            show_detail = True):
        """
        East_movement selects the correct boat, creates correct graph and 
            correct camera frame.   Optionally also adds explanatory text 
            (camera frame altered to include text).
        Accepts:
            boat (ImageMobject instance): boat
            direction (str): cardinal direction of movement
            movement_dictionary (dict): Format: {
                'start_location' (list of ints): beginning location [x,y],
                'movement' (str): 'E<#>'
                }
            show_detail (bool): Whether or not explanatory detail should be shown
        Returns:
            List of objects added to graph. Also adds video and alters camera frame
        """
        movement = int(movement_dictionary['movement'][1:])
        start_location = movement_dictionary['start_location']
        if direction in ['west', 'south']:
            movement *= -1
        if direction in ['east', 'west']:
            boat_start = [start_location[0],
                    start_location[1] + self.boat_delta]
            (curr_graph, boat_graph, brace) = self.move_boat_horizontal(
                start_location, movement)
            boat_end = [boat_start[0] + movement, boat_start[1]]
        else:
            if direction == 'south':
                boat_start = [start_location[0] - self.boat_delta,
                        start_location[1]]
            else:
                boat_start = [start_location[0] + self.boat_delta,
                        start_location[1]]
            (curr_graph, boat_graph, brace) = self.move_boat_vertical(
                    start_location, movement)
            boat_end = [boat_start[0], boat_start[1] + movement]
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
        self.frame_camera_around_group(frame_group)
        self.wait(1)
        self.play(
                MoveAlongPath(current_boat, boat_graph),
                ShowCreation(curr_graph),
                **animation_parameters
                )
        if show_detail is True:
            self.add(brace)
        return return_objects

    def show_move_examples(self, direction, detail_dictionary):
        """
        East_examples shows the boat moving a certain cardinal direction.
        Accepts:
            direction (str): direction
            detail_dictionary (dictionary): Directions in dictionary form:
                "boat": {
                    "start_location": [ int, int]
                    "movement": str ("E<int>") 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in detail_dictionary:
            this_boat = self.boats[key]
            this_key_objects = self.move_boat(this_boat, direction, 
                    detail_dictionary[key], True)
            this_scene_objects += this_key_objects
            self.wait(2)
        for obj in this_scene_objects:
            self.remove(obj)

    def turn_boat(self, boat, turn_dictionary, show_detail = True):
        """
        Turn_boat turns the boat on the graph.  Optionally, it also shows
            explanatory text.
        Accepts:
            boat (ImageMobject instance): current boat
            turn_dictionary (dict): Dictionary of the form {
                "start_location" (list of ints): [x, y]
                "movement" (str): "L<#>" or "R<#>"
            show_detail (bool): Shows explanatory text
        Returns:
            list of objects on graph -- also moves camera and adds objects to
                graph
        """
        direction = turn_dictionary['movement'][0]
        turn_amount = int(turn_dictionary['movement'][1:])
        if direction == 'R':
            turn_amount *= -1
        location = turn_dictionary["start_location"]
        boat_location = [location[0], location[1] + self.boat_delta]
        animation_parameters = {
                "run_time": 3,
                "rate_func": linear
                }
        boat.move_to(self.coords_to_point(boat_location[0], boat_location[1]))
        return_objects = [boat]
        turned_boat = boat.copy()
        turned_boat.rotate(angle = PI * turn_amount /180,
                about_point = boat.get_center())
        frame_group = Group(boat, turned_boat)
        self.add(boat)
        if show_detail is True:
            rotate_text = Text(turn_dictionary['movement'])
            rotate_text.move_to(boat.get_center() + RIGHT * 1.5)
            rotate_text.set_color(RED)
            rotate_text.bg = SurroundingRectangle(rotate_text, color = BLACK,
                    fill_color = BLACK, fill_opacity = 1)
            return_objects += [rotate_text, rotate_text.bg]
            frame_group = Group(*frame_group, rotate_text, rotate_text.bg)
            self.add(rotate_text.bg, rotate_text)
        self.frame_camera_around_group(frame_group)
        self.wait(1)
        self.play(
                Rotating(boat, radians = PI * turn_amount/ 180,
                    about_point = boat.get_center()),
                **animation_parameters
                )
        self.wait(2)
        return return_objects
        

    def show_turn_examples(self, detail_dictionary):
        """
        Show_turn_examples shows the boat rotating right (clockwise)
        Accepts:
            detail_dictionary (dictionary): Directions in dictionary form:
                "boat": {
                    "start_location": [ int, int]
                    "movement" (str):  "L<int>" or "R<int>" 
                    }
        Returns:
            None
        """
        this_scene_objects = []
        for key in detail_dictionary:
            current_boat = self.boats[key].copy()
            this_key_objects = self.turn_boat(current_boat, 
                    detail_dictionary[key], True)
            self.wait(2)
            this_scene_objects += this_key_objects
        for obj in this_scene_objects:
            self.remove(obj)

    def show_forward_examples(self, directions):
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
        for key in directions:
            this_boat = self.boats[key]
            this_key_objects = self.move_boat(this_boat, key, 
                    directions[key], True)
            this_scene_objects += this_key_objects
            self.wait(2)
        for obj in this_scene_objects:
            self.remove(obj)

    def show_confusion(self):
        """
        Show_confusion shows intro confusion scene: boat on grid, question
            marks, and sample confusing directions
        """
        ## Show confused boat
        self.camera_frame.save_state()
        self.wait(1)
        self.play(FadeIn(self.current_boat))
        self.wait(1)
        question = Text("?", color = RED)
        marks = [ [LEFT, UP], [RIGHT, UP], [LEFT, DOWN], [RIGHT, DOWN]]
        question_group = VGroup()
        for mark in marks:
            this_question = question.copy()
            this_question.move_to(self.current_boat.get_center() + 0.5 * mark[0] + 0.5 * mark[1])
            question_group = VGroup(*question_group, this_question)
        boat_question_group = Group(*question_group, self.current_boat)
        self.frame_camera_around_group(boat_question_group)
        self.play(Write(question_group))
        self.wait(1)
        self.play(Restore(self.camera_frame))
        ## Show confusing input
        self.camera_frame.save_state()
        question_title = Text("? ? ? ? ? ? ?", color = RED)
        question_title.move_to(5*LEFT + 3 * UP)
        self.title_bar = Line(7*LEFT + 2.5 * UP, 3*LEFT + 2.5 * UP, color = RED, 
                stroke_width = 3)
        self.play(Write(VGroup(question_title, self.title_bar)))
        sample_input = self.puzzle_input[:]
        not_displayed = []
        displayed = {}
        random.seed()
        for i in range(20):
            if random.randint(1,3) == 3:
                if len(displayed.keys()) > 0:
                    removal_location = random.choice(list(displayed.keys()))
                    remove_object = displayed[removal_location]
                    not_displayed.append(remove_object)
                    self.play(FadeOut(remove_object))
            else:
                if len(not_displayed) > 0 or len(sample_input) > 0:
                    display_choice = random.randint(1, 
                            len(not_displayed) + len(sample_input))
                    if display_choice <= len(not_displayed):
                        place_object = random.choice(not_displayed)
                    else:
                        place_object = Text(sample_input.pop(random.randint(0, len(sample_input)-1)),
                                color = RED)
                    placement = (random.randint(0,3), random.randint(0,2))
                    place_object.move_to(1.25 * (placement[0]-1.5) * UP + 
                            1.25 * (placement[1] + 3) * LEFT)
                    if placement in displayed:
                        self.play(FadeOut(displayed[placement]))
                    displayed[placement] = place_object 
                    self.play(FadeIn(place_object))
        for placement in displayed:
            self.remove(displayed[placement])
            not_displayed.append(displayed[placement])
        ## Some sense is made        
        self.idea_title = Text("N S E W L R F", color = RED)
        self.idea_title.move_to(5*LEFT + 3 * UP)
        self.play(ReplacementTransform(question_title, self.idea_title))
        for index, ele in enumerate(["N2", "S2", "E1", "W5", "L90", "R90", "F82"]):
            this_text = Text(ele, color = RED)
            this_text.move_to(1.25 * (3-index//3 - 1.5) * UP +
                    1.25 * (2 - index % 3 + 3) * LEFT)
            self.play(FadeIn(this_text))
            boat_question_group = Group(*boat_question_group, this_text)
        for ele in question_group:
            self.play(FadeOut(ele))
        for obj in boat_question_group:
            self.remove(obj)

    def north_description(self):
        """
        North_description shows information about "N" text
        """
        ## Set camera and change title
        self.camera_frame.save_state()
            # change title to "N"
        self.north_title = Text("N", color = RED)
        self.north_title.move_to(5 * LEFT + 3 * UP)
        self.play(ReplacementTransform(self.idea_title, self.north_title))
        ## add descriptions
            # add boats
        self.list_boat_facing_east = self.boat_facing_east.copy()
        self.list_boat_facing_east.move_to(6 * LEFT + 2 * UP)
        self.list_boat_facing_north = self.boat_facing_north.copy()
        self.list_boat_facing_north.move_to(6 * LEFT + 1 * UP)
        self.list_boat_facing_west = self.boat_facing_west.copy()
        self.list_boat_facing_west.move_to(6 * LEFT + 0 * UP)
        self.list_boat_facing_south = self.boat_facing_south.copy()
        self.list_boat_facing_south.move_to(6 * LEFT + -1 * UP)
        instruction_group = Group(
                self.north_title,
                self.title_bar,
                self.list_boat_facing_east,
                self.list_boat_facing_north,
                self.list_boat_facing_west,
                self.list_boat_facing_south
                )
        self.frame_camera_around_group(instruction_group)
        self.add(
                self.list_boat_facing_east,
                self.list_boat_facing_north,
                self.list_boat_facing_west,
                self.list_boat_facing_south
                )
            # add arrows
        first_arrow = Arrow( 4.5*LEFT + 1.5*UP, 4.5*LEFT + 2.5*UP, color = RED)
        self.play(ShowCreation(first_arrow))
        second_arrow = Arrow( 4.5*LEFT + 0.5*UP, 4.5*LEFT + 1.5*UP, 
                color = RED)
        self.play(ShowCreation(second_arrow))
        third_arrow = Arrow( 4.5*LEFT + -0.5* UP, 4.5*LEFT + 0.5*UP, 
                color = RED)
        self.play(ShowCreation(third_arrow))
        fourth_arrow = Arrow( 4.5*LEFT + -1.5 * UP, 4.5*LEFT - 0.5*UP, 
            color = RED)
        self.play(ShowCreation(fourth_arrow))
        self.wait(1)
        arrow_instruction_group = Group(first_arrow, second_arrow, 
            third_arrow, fourth_arrow)
        ## do sample movements
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
                    "start_location" : [10, 8],
                    "movement": "N5"
                },
                "north": {
                    "start_location": [15, 0],
                    "movement": "N3"
                }
            }
        self.show_move_examples('north', north_directions)
        self.play(FadeOut(arrow_instruction_group))
        self.play(Restore(self.camera_frame))
        self.wait(2)

    def south_description(self):
        """
        South_description shows information about "S" text
        """
        ## Set camera and make title
        self.camera_frame.save_state()
            # change title to "S"
        self.south_title = Text("S", color = RED)
        self.south_title.move_to(5 * LEFT + 3 * UP)
        self.play(ReplacementTransform(self.north_title, self.south_title))
        ## add descriptions
        instruction_group = Group(
                self.south_title,
                self.title_bar,
                self.list_boat_facing_east,
                self.list_boat_facing_north,
                self.list_boat_facing_west,
                self.list_boat_facing_south
                )
        self.frame_camera_around_group(instruction_group)
            # add arrows
        first_arrow = Arrow( 4.5*LEFT + 2.5*UP, 4.5*LEFT + 1.5*UP, color = RED)
        self.play(ShowCreation(first_arrow))
        second_arrow = Arrow( 4.5*LEFT + 1.5*UP, 4.5*LEFT + 0.5*UP, 
                color = RED)
        self.play(ShowCreation(second_arrow))
        third_arrow = Arrow( 4.5*LEFT + 0.5* UP, 4.5*LEFT + -0.5*UP, 
                color = RED)
        self.play(ShowCreation(third_arrow))
        fourth_arrow = Arrow( 4.5*LEFT + -0.5* UP, 4.5*LEFT + -1.5*UP, 
            color = RED)
        self.play(ShowCreation(fourth_arrow))
        self.wait(1)
        arrow_instruction_group = Group(first_arrow, second_arrow, 
            third_arrow, fourth_arrow)
        ## do sample movements
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
                    "start_location" : [10, 8],
                    "movement": "S5"
                },
                "north": {
                    "start_location": [15, 3],
                    "movement": "S3"
                }
            }
        self.show_move_examples('south', south_directions)
        self.play(FadeOut(arrow_instruction_group))
        self.play(Restore(self.camera_frame))
        self.wait(2)

    def east_description(self):
        """
        East_description shows information about "E" text
        """
        ## Set camera and make title
        self.camera_frame.save_state()
            # change title to "E"
        self.east_title = Text("E", color = RED)
        self.east_title.move_to(5 * LEFT + 3 * UP)
        self.play(ReplacementTransform(self.south_title, self.east_title))
        ## add descriptions
        instruction_group = Group(
                self.east_title,
                self.title_bar,
                self.list_boat_facing_east,
                self.list_boat_facing_north,
                self.list_boat_facing_west,
                self.list_boat_facing_south
                )
        self.frame_camera_around_group(instruction_group)
            # add arrows
        first_arrow = Arrow( 5*LEFT + 2*UP, 4*LEFT + 2*UP, color = RED)
        self.play(ShowCreation(first_arrow))
        second_arrow = Arrow( 5*LEFT + 1*UP, 4*LEFT + 1*UP, 
                color = RED)
        self.play(ShowCreation(second_arrow))
        third_arrow = Arrow( 5*LEFT + 0* UP, 4*LEFT + 0*UP, 
                color = RED)
        self.play(ShowCreation(third_arrow))
        fourth_arrow = Arrow( 5*LEFT + -1*UP, 4*LEFT + -1*UP, 
            color = RED)
        self.play(ShowCreation(fourth_arrow))
        self.wait(1)
        arrow_instruction_group = Group(first_arrow, second_arrow, 
            third_arrow, fourth_arrow)
        ## do sample movements
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
        self.show_move_examples('east', east_directions)
        self.play(FadeOut(arrow_instruction_group))
        self.play(Restore(self.camera_frame))
        self.wait(2)

    def west_description(self):
        """
        West_description shows information about "W" text
        """
        ## Set camera and make title
        self.camera_frame.save_state()
            # change title to "W"
        self.west_title = Text("W", color = RED)
        self.west_title.move_to(5 * LEFT + 3 * UP)
        self.play(ReplacementTransform(self.east_title, self.west_title))
        ## add descriptions
        instruction_group = Group(
                self.west_title,
                self.title_bar,
                self.list_boat_facing_east,
                self.list_boat_facing_north,
                self.list_boat_facing_west,
                self.list_boat_facing_south
                )
        self.frame_camera_around_group(instruction_group)
            # add arrows
        first_arrow = Arrow( 4*LEFT + 2*UP, 5*LEFT + 2*UP, color = RED)
        self.play(ShowCreation(first_arrow))
        second_arrow = Arrow( 4*LEFT + 1*UP, 5*LEFT + 1*UP, 
                color = RED)
        self.play(ShowCreation(second_arrow))
        third_arrow = Arrow( 4*LEFT + 0* UP, 5*LEFT + 0*UP, 
                color = RED)
        self.play(ShowCreation(third_arrow))
        fourth_arrow = Arrow( 4*LEFT + -1*UP, 5*LEFT + -1*UP, 
            color = RED)
        self.play(ShowCreation(fourth_arrow))
        self.wait(1)
        arrow_instruction_group = Group(first_arrow, second_arrow, 
            third_arrow, fourth_arrow)
        ## do sample movements
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
        self.show_move_examples('west', west_directions)
        self.play(FadeOut(arrow_instruction_group))
        self.play(Restore(self.camera_frame))
        self.wait(2)

    def left_description(self):
        """
        Left_description shows information about "L" text
        """
        ## Set camera and make title
        self.camera_frame.save_state()
            # change title to "L"
        self.left_title = Text("L", color = RED)
        self.left_title.move_to(5 * LEFT + 3 * UP)
        self.play(ReplacementTransform(self.west_title, self.left_title))
        ## add descriptions
        instruction_group = Group(
                self.left_title,
                self.title_bar,
                self.list_boat_facing_east,
                self.list_boat_facing_north,
                self.list_boat_facing_west,
                self.list_boat_facing_south
                )
        self.frame_camera_around_group(instruction_group)
            # add arrows
        first_arrow = CurvedArrow( 4.2*LEFT + 1.7*UP, 4.8*LEFT + 2.3*UP, color = RED)
        self.play(ShowCreation(first_arrow))
        second_arrow = CurvedArrow( 4.2*LEFT + 0.7*UP, 4.8*LEFT + 1.3*UP, 
                color = RED)
        self.play(ShowCreation(second_arrow))
        third_arrow = CurvedArrow( 4.2*LEFT + -0.3* UP, 4.8*LEFT + 0.3*UP, 
                color = RED)
        self.play(ShowCreation(third_arrow))
        fourth_arrow = CurvedArrow( 4.2*LEFT + -1.3*UP, 4.8*LEFT + -0.7*UP, 
            color = RED)
        self.play(ShowCreation(fourth_arrow))
        self.wait(1)
        arrow_instruction_group = Group(first_arrow, second_arrow, 
            third_arrow, fourth_arrow)
        ## do sample movements
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
                    "movement": "L360"
                }
            }
        self.show_turn_examples(left_directions)
        self.play(FadeOut(arrow_instruction_group))
        self.play(Restore(self.camera_frame))
        self.wait(2)
 
    def right_description(self):
        """
        right_description shows information about "R" text
        """
        ## Set camera and make title
        self.camera_frame.save_state()
            # change title to "R"
        self.right_title = Text("R", color = RED)
        self.right_title.move_to(5 * LEFT + 3 * UP)
        self.play(ReplacementTransform(self.left_title, self.right_title))
        ## add descriptions
        instruction_group = Group(
                self.right_title,
                self.title_bar,
                self.list_boat_facing_east,
                self.list_boat_facing_north,
                self.list_boat_facing_west,
                self.list_boat_facing_south
                )
        self.frame_camera_around_group(instruction_group)
            # add arrows
        first_arrow = CurvedArrow(4.8*LEFT + 2.3*UP, 4.2*LEFT + 1.7*UP,
                color = RED, angle = - TAU/4)
        self.play(ShowCreation(first_arrow))
        second_arrow = CurvedArrow(4.8*LEFT + 1.3*UP, 4.2*LEFT + 0.7*UP, 
                color = RED, angle = - TAU/4)
        self.play(ShowCreation(second_arrow))
        third_arrow = CurvedArrow(4.8*LEFT + 0.3*UP, 4.2*LEFT + -0.3* UP, 
                color = RED, angle = -TAU/4)
        self.play(ShowCreation(third_arrow))
        fourth_arrow = CurvedArrow(4.8*LEFT + -0.7*UP, 4.2*LEFT + -1.3*UP, 
            color = RED, angle = -TAU/4)
        self.play(ShowCreation(fourth_arrow))
        self.wait(1)
        arrow_instruction_group = Group(first_arrow, second_arrow, 
            third_arrow, fourth_arrow)
        ## do sample movements
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
                "movement": "R360"
            }
        }
        self.show_turn_examples(right_directions)
        self.play(FadeOut(arrow_instruction_group))
        self.play(Restore(self.camera_frame))
        self.wait(2)

    def forward_description(self):
        """
        Forward_description shows information about "F" text
        """
        ## Set camera and make title
        self.camera_frame.save_state()
            # change title to "F"
        self.forward_title = Text("F", color = RED)
        self.forward_title.move_to(5 * LEFT + 3 * UP)
        self.play(ReplacementTransform(self.right_title, self.forward_title))
        ## add descriptions
        instruction_group = Group(
                self.forward_title,
                self.title_bar,
                self.list_boat_facing_east,
                self.list_boat_facing_north,
                self.list_boat_facing_west,
                self.list_boat_facing_south
                )
        self.frame_camera_around_group(instruction_group)
            # add arrows
        first_arrow = Arrow( 5*LEFT + 2*UP, 4*LEFT + 2*UP, color = RED)
        self.play(ShowCreation(first_arrow))
        second_arrow = Arrow( 4.5*LEFT + 0.5*UP, 4.5*LEFT + 1.5*UP, 
                color = RED)
        self.play(ShowCreation(second_arrow))
        third_arrow = Arrow( 4*LEFT + 0* UP, 5*LEFT + 0*UP, 
                color = RED)
        self.play(ShowCreation(third_arrow))
        fourth_arrow = Arrow( 4.5*LEFT + -0.5*UP, 4.5*LEFT + -1.5*UP, 
            color = RED)
        self.play(ShowCreation(fourth_arrow))
        self.wait(1)
        arrow_instruction_group = Group(first_arrow, second_arrow, 
            third_arrow, fourth_arrow)
        ## do sample movements
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
        self.show_forward_examples(forward_directions)
        self.play(FadeOut(arrow_instruction_group))
        self.play(Restore(self.camera_frame))
        self.wait(2)


