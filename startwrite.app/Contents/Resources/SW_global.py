# ****************************************** Global Variable & Statement ********************************************
page_no = 1
pg_flag = 0
lt_gd_1 = 0.01
btm_gd_1 = 0.83
wd_gd_1 = 0.98
ht_gd_1 = 0.15
scl = 11
gd_sc1 = False

left, right, bottom, top = 0.99,0.01,0.83,0.98
new_left_axes1, new_right_axes1, new_bottom_axes1, new_top_axes1 = 0, 0, 0, 0
new_left_axes2, new_right_axes2, new_bottom_axes2, new_top_axes2 = 0, 0, 0, 0
gdaxes = 0
gd_flag1 = False
gd_flag2 = False
new_gd = 0
imgleft, imgright, imgtop, imgbottom = 0, 0, 0, 0
img_left_axes1, img_right_axes1, img_top_axes1, img_bottom_axes1 = 0, 0, 0, 0
img_left_axes2, img_right_axes2, img_top_axes2, img_bottom_axes2 = 0, 0, 0, 0
imgaxes = 0
img_flag1 = False
img_flag2 = False

count = 0

recent_input_list1 = []
recent_input_list2 = []

kern_list1 = []
kern_list2 = []

kern_x = 0
kern_list1.insert(0, kern_x)
kern_list2.insert(0, kern_x)

xmax = {'A': 1500, 'Y': 1125}

kern_value_array1 = []
kern_value_array2 = []

delete_list1 = []
delete_list2 = []


startDot = []
startDot.insert(0, 0)

connectDot = []
connectDot.insert(0, 0)

compositeDot = []
compositeDot.insert(0, 0)

decisionDot = []
decisionDot.insert(0, 0)

recent_input_list = []
delete_list = []

kern_list = []
kern_x= 0
kern_list.insert(0, kern_x)

kern_value_array = []
kern_value_array.insert(0, kern_x)

# initial color
startdot_color = '#ff0000'
decisiondot_color = '#0000ff'
stokearrow_color_var = '#000000'
connectingdot_color_var = '#000000'


guidelines_background_color_toparea = '#91f46c'
guidelines_background_color_middlearea = '#fbee69'
guidelines_background_color_descenderarea = '#e3b1d8'

# current state of every features
guidelines_toparea = 0
guidelines_middlearea = 0
guidelines_descenderarea = 0


# guidelines colors
guidelines_top_color = '#0100f4'
guidelines_middle_color = '#0100f4'
guidelines_base_color = '#ff0000'
guidelines_bottom_color = '#000000'

# Color Letters
first_letter_background_color = '#ff0000'
second_letter_background_color = '#0000ff'
third_letter_background_color = '#00ff00'
forth_letter_background_color = '#90009c'

firstline_color = False
secondline_color = False
thirdline_color = False
forthline_color = False
letter_out_color_var=None

# Guideline Style
getvar1 = 0
getvar2 = 0
getvar3 = 0
getvar4 = 0
# Guideline Density
get_top_density = 0
get_middle_density = 0
get_base_density = 0
get_descender_density = 0


startdot_on_off = 0
stokearrow_on_off = 0
decisiondot_on_off = 0
connectdot_on_off = 0

# new created
delete_start_dot_array = []
delete_decision_dot_array = []
delete_connecting_dot_array = []

startdot_already_applied_array = []
connectdot_already_applied_array = []
decisiondot_already_applied_array = []
compositedot_already_applied_array = []

guide_line_top_already_applied_array = []
guide_line_middle_already_applied_array = []
guide_line_base_already_applied_array = []
guide_line_descender_already_applied_array = []

#new
letters_already_written = []
cursor_pos=[0]
cursor_data=[]

ba_flag = False
ba_size = 0
viewvalue1 = True
viewvalue2 = True
viewvalue3 = True
figvalue = False
u_r = 0
w_r = 0
axx = 0
gird_flag = False

currentsize = 1
pagesize = 1
r = 7
change_size_count = 100
axhspan_flg = False

currentpage = 5
pagecount = 10

gv = True

g_key = 0
g_val = ''

#### Data for mouse release and click
release_x=-999
release_y=-999
click_x=-999
click_y=-999
copy_string=""
temp_cursor_temp_data=0
selector_data={"1":{"axx":[],"pos":[]}}
axes_data=dict()
count_for_height=0
single_click_data=None
single_click_pos=-999
x_with_bez=[]
y_with_bez=[]
x_without_bez=[]
y_without_bez=[]
recent_axes_with_respect_rectangle_selector=dict()
current_selector=0
click_axes=None
release_axes=None
single_click_axes_data=None
# kChange() for changing axes control
#findPos1() Can be written using oops 
#findPos2() Can be written using oops

current_axes=None
current_pos=None
current_pos_in_number=None
current_page=1
p1=-9999
p2=-9999
entire_delete_list_for_one_page=[]
que_flag=None
once=None
box_data=dict()
axes_against_box_with_respect_to_page=dict()
text_flow_axes1=None
text_flow_axes2=None
temp_axes=None
text_flow_delete_list1=[]
text_flow_delete_list2=[]
text_flow_box_page1=[]
text_flow_box_page2=[]
check_u1=None
check_u=None
left11=None
right11=None
back_axes=None
shift_no=0
delete_list_divide=[]
max_limit=15000
final_array=[]
calculation_array=[]
text_flow_axes=[]
text_flow_pos=[]
box_index_for_text_flow=[]
delete_list_text_flow=[]
next_axes=[]
max_text=0
embed_array=[]
mainselector_value=None
pos1_global=None
pos2_global=None
start_axes_global=None
end_axes_global=None
start_axes_global_temp=None
end_axes_global_temp=None

font_size_vary_dict={"8":{"max_limit":25000,"width":0.08,"scl":23},"192":{"max_limit":8000,"width":0.20,"scl":6}}


unit_value_of_scl=(20-8)/180
unit_value_of_max_limit=(28000-8000)/180
unit_value_of_width=(0.2-0.08)/180


current_font_size=None
current_width=None
##### This will be used for starting position setting  
start_x_for_font_size_change=None
start_y_for_font_size_change=None
global_figure=None
global_canvas=None
page_data_for_entire=dict()