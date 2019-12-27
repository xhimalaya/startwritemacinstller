class Guideline:
    def __init__(self):
        ''' Default Height & Width Of Main Guideline '''
        self.base_x = [0, (1500 * 12)]
        self.base_y = [0, 0]
        self.median_x = [0, (1500 * 12)]
        self.median_y = [757, 757]
        self.descender_x = [0, (1500 * 12)]
        self.descender_y = [-747, -747]
        self.ascender_x = [0, (1500 * 12)]
        self.ascender_y = [1500, 1500]
        ''' Default Guideline Color '''
        self.base_color = 'red'
        self.median_color = 'blue'
        self.descender_color = 'black'
        self.ascender_color = 'blue'
        ''' Default  Guideline Thickness '''
        self.base_width = 0.7
        self.median_width = 0.7
        self.descender_width = 0.7
        self.ascender_width = 0.7
        ''' Default Guideline Style '''
        self.base_style = '-'
        self.median_style = '--'
        self.descender_style = '-'
        self.ascender_style = '-'
        ''' Default Guideline Background '''
        self.st_bg_color = 'white'
        self.nd_bg_color = 'white'
        self.rd_bg_color = 'white'
        ''' Required Attributes For Maintaining Writting Event '''
        self.recent_input_list = []
        self.kern_list = 0
        self.kern_value_array = []
        self.letters_already_written = []
        ''' Attributes For StartDOT '''
        self.startdot_already_applied_array = []
        self.startdot_flag_pos = 0
        self.startdot_on_off = 0
        self.startdot_color = 'red'
        ''' Attributes For Stoke Arrow '''
        self.stoke_arrow_already_applied_array = []
        self.stoke_arrow_flag_pos = 0
        self.stokearrow_on_off = 0
        self.stokearrow_color_var = 'black'
        ''' Attributes For DecisionDot '''
        self.decisiondot_already_applied_array = []
        self.decision_dot_flag_pos = 0
        self.decisiondot_on_off = 0
        self.decisiondot_color = 'blue'
        ''' Attributes For ConnectDot '''
        self.connectdot_already_applied_array = []
        self.connect_dot_flag_pos = 0
        self.connectdot_on_off = 0
        self.connectingdot_color_var = 'black'
        ''' Attributes For Color Letters '''
        self.color_letter_on_off = 0
        self.color_letter_flag_pos = 0
        self.first_color_letter = 'red'
        self.first_color_letter_already_applied_array = []
        self.second_color_letter = 'blue'
        self.second_color_letter_already_applied_array = []
        self.third_color_letter = 'green'
        self.third_color_letter_already_applied_array = []
        self.forth_color_letter = 'yellow'
        self.forth_color_letter_already_applied_array = []
        ''' Attributes For Letter Shading '''
        self.letter_shading_already_applied_array = []
        self.letter_shading_flag_pos = 0
        ''' Up to This, It Will Automatically Create Guideline Initially '''

    def change_letter_shading(self, dynamic_shading_value):
        pass

    def letter_dot_density(self, dynamic_dot_density_value):
        pass

    ''' GuideLine Height & Width Change '''
    def change_guideline_size(self, size):
        self.base_x = [0, (1500 * size)]
        self.base_y = [0, 0]
        self.median_x = [0, (1500 * size)]
        self.median_y = [757, 757]
        self.descender_x = [0, (1500 * size)]
        self.descender_y = [-747, -747]
        self.ascender_x = [0, (1500 * size)]
        self.ascender_y = [1500, 1500]

    ''' Change GuideLine Color '''
    def change_guideline_color(self, base_color, median_color, descender_color, ascender_color):
        self.base_color = base_color
        self.median_color = median_color
        self.descender_color = descender_color
        self.ascender_color = ascender_color

    def change_guideline_base_color(self, color_base):
        self.base_color = color_base

    def change_guideline_median_color(self, color_median):
        self.median_color = color_median

    def change_guideline_descender_color(self, color_descender):
        self.descender_color = color_descender

    def change_guideline_ascender_color(self, color_ascender):
        self.ascender_color = color_ascender

    ''' Guideline Thickness Change '''
    def change_guideline_thickness(self, base_width, median_width, descender_width, ascender_width):
        self.base_width = base_width
        self.median_width = median_width
        self.descender_width = descender_width
        self.ascender_width = ascender_width

    def change_guideline_base_thickness(self, base_width):
        self.base_width = base_width

    def change_guideline_median_thickness(self, median_width):
        self.median_width = median_width

    def change_guideline_descender_thickness(self, descender_width):
        self.descender_width = descender_width

    def change_guideline_ascender_thickness(self, ascender_width):
        self.ascender_width = ascender_width

    ''' Guideline Style Change '''
    def change_guideline_style(self, st1, st2, st3, st4):
        self.base_style = st1
        self.median_style = st2
        self.descender_style = st3
        self.ascender_style = st4

    def change_guideline_base_style(self, st1):
        self.base_style = st1

    def change_guideline_median_style(self, st2):
        self.median_style = st2

    def change_guideline_descender_style(self, st3):
        self.descender_style = st3

    def change_guideline_ascender_style(self, st4):
        self.ascender_style = st4

    ''' Guideline Background Change '''
    def change_guideline_background(self, st, nd, rd):
        self.st_bg_color = st
        self.nd_bg_color = nd
        self.rd_bg_color = rd

    def change_guideline_st_background(self, st):
        self.st_bg_color = st

    def change_guideline_nd_background(self, nd):
        self.nd_bg_color = nd

    def change_guideline_rd_background(self, rd):
        self.rd_bg_color = rd

    ''' Letter Color Change Function '''
    def letter_color_change(self, color1, color2, color3, color4):
        self.first_color_letter = color1
        self.second_color_letter = color2
        self.third_color_letter = color3
        self.forth_color_letter = color4

    def first_letters_color_change(self, color1):
        self.first_color_letter = color1

    def second_letters_color_change(self, color2):
        self.second_color_letter = color2

    def third_letters_color_change(self, color3):
        self.third_color_letter = color3

    def fourth_letters_color_change(self, color4):
        self.forth_color_letter = color4

