#!/usr/local/bin/python3
from SW_lib import *
from brez import font_check
import border_art as brd
import key_generation
import copy
from matplotlib.patches import Rectangle
lin_flag = False
import Sw_db_init
user_id, user_mail, vaild_key, key_status = SWdb.fetching_data_from_license_table()
if key_status == 0:
    lin_flag = True
    import welcomedemo_SW
    SWdb.update_data_into_license_table()
elif key_status == 1:
    lin_flag = True
    import regchk_SW
elif key_status == 2:
    lin_flag = False
    pass
else:
    exit(0)


#### N.B Border art has attached with 18-09-2019-copy6011112222444444.py #######


# ****************************************** Global Variable & Statement     ********************************************
global f_w, f_h
global tem_cursor_x,temp_cursor_y #,temp_cursor_temp_data
global guideline_latest
#SW_global.temp_cursor_temp_data=0
print("This is SW_global temp_cursor_temp_data")
print(SW_global.temp_cursor_temp_data)
try:
    o=SW_global.temp_cursor_temp_data[0]
    o.set_visible(False)


except Exception as e:
    pass
    print(e)

#o=SW_global.temp_cursor_temp_data[0]
#o.set_visible(False)
letter_shadding_on_off = 0
alp = 1
temp_recent_input_list = []
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
kern_x = 0
delete_list = []
letter_out_line_inner_fonts_array=[]
kern_value_array = []
kern_value_array.insert(0, kern_x)
# position storing array
delete_start_dot_array = []
delete_decision_dot_array = []
delete_connecting_dot_array = []
# Features Already on in that case position storing array
startdot_already_applied_array = []
connectdot_already_applied_array = []
decisiondot_already_applied_array = []
compositedot_already_applied_array = []
# Guide line Control Array
guide_line_top_already_applied_array = []
guide_line_middle_already_applied_array = []
guide_line_base_already_applied_array = []
guide_line_descender_already_applied_array = []
# Unnecessary declaration
gsub_list1 = []
gsub_list2 = []
fnl_g = {}
g_c = 0
l = 0

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Bezier Function <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
bernstein = lambda n, k, t: binom(n, k) * t ** k * (1. - t) ** (n - k)

def bezier(points, num=200):
    N = len(points)
    t = np.linspace(0, 1, num=num)
    curve = np.zeros((num, 2))
    for i in range(N):
        curve += np.outer(bernstein(N - 1, i, t), points[i])
    return curve
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# *********************************************** Main Windows ******************************************************
# When you click to exit, this function is called
def on_exit():
    if len(SW_global.recent_input_list) > 0:
        MsgBox = messagebox.askyesnocancel('Exit Application','Do you want to Save the Application')
        if MsgBox:
            filewin_saveas = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                         filetypes=(("Startwrite Files", "*.swd"), ("all files", "*.*")))

            pickle.dump(fig.gca(), open(filewin_saveas+".swd", "wb"))
            plt.close("all")
            SW_Main_UI.destroy()
        elif MsgBox is not None:
            SW_Main_UI.destroy()
            os._exit(0)
        else:
            pass
    else:
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            SW_Main_UI.destroy()
            os._exit(0)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Centers this Tk window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def center():
    SW_Main_UI.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Toolbar Show Hide control <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def toolbarhideshow():
    if vm1.get() == 1:
        maintoolbarframe1.grid_remove()
        vm1.set(0)
    else:
        maintoolbarframe1.grid(row = 1, column = 0)
        vm1.set(1)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def font_increase_automate():
    SW_global.scl
    return 

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Property bar Show Hide control <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def propertybarhideshow():
    if vm2.get() == 1:
        propertybarframe1.grid_remove()
        vm2.set(0)
    else:
        propertybarframe1.grid(row = 2, column = 0)
        vm2.set(1)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Status bar Show Hide control <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def statusbarhideshow():
    if vm3.get() == 1:
        endgridtoolframe1.grid_remove()
        vm3.set(0)
    else:
        endgridtoolframe1.grid(row = 4, column = 0)
        vm3.set(1)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Showing page number <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def raise_frame(frame):
    frame.tkraise()
    if frame == writingareaframe1 and SW_global.pg_flag == 1:
        SW_global.page_no = 1
        pageLabel.config(text="page "+ str(int(SW_global.page_no)) + " of " + str(int(SW_global.page_no) + 1))
    elif frame == writingareaframe2:
        SW_global.page_no = 2
        pageLabel.config(text="page "+ str(int(SW_global.page_no)) + " of " + str(int(SW_global.page_no)))
    if SW_global.pg_flag == 2 and frame == writingareaframe2:
       pageLabel.config(text="page "+ str(int(SW_global.page_no)-1) +" of "+ str(int(SW_global.page_no)))
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Online Purchase Link <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def lin_purchase_wp():
    webbrowser.open_new_tab(r"https://www.startwriteindia.com/buy-the-software-license")
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> License Key Show Function <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def valid_key_wp():
    global lin_flag, user_id, user_mail, vaild_key, key_status
    key_wp = Toplevel()
    key_wp.title("Activation / Purchase StartWrite")
    key_wp.geometry("450x300+330+240")
    key_wp.resizable(width=False, height=False)

    frm1 = Frame(key_wp, width=510, height=100)
    frm1.grid(row=0, column=0)
    frm2 = Frame(key_wp, width=510, height=140)
    frm2.grid(row=1, column=0, ipady=8)
    frm3 = Frame(key_wp, width=510, height=100)
    frm3.grid(row=2, column=0, ipady=8)
    frm4 = Frame(key_wp, width=510, height=100)
    frm4.grid(row=3, column=0, ipady=8)

    lbl2 = Label(frm1, text="IMPORTANT: Enter data exactly as received in your registration email.", justify=CENTER)
    lbl2.pack(pady=15, padx=15)

    lbl2 = Label(frm2, text="Name:", justify=LEFT)
    lbl2.grid(row=0, column=0, sticky=E)
    name_ent = Entry(frm2, width=40)
    name_ent.grid(row=0, column=1)

    lbl2 = Label(frm2, text="E-mail Address:", justify=RIGHT)
    lbl2.grid(row=1, column=0, sticky=E)
    email_ent = Entry(frm2, width=40)
    email_ent.grid(row=1, column=1)

    lbl2 = Label(frm2, text="License Key:", justify=RIGHT)
    lbl2.grid(row=2, column=0, sticky=E)

    linfrm = Frame(frm2)
    linfrm.grid(row=2, column=1, sticky=W)

    key_ent1 = Entry(linfrm, width=5)
    key_ent1.pack(side="left")

    lbl2 = Label(linfrm, text="-", justify=LEFT)
    lbl2.pack(side="left")

    key_ent2 = Entry(linfrm, width=5)
    key_ent2.pack(side="left")

    lblfrm1 = LabelFrame(frm3, text="To get the License key do one of the following:", bd=1, relief='solid', padx=2,
                         pady=2)
    lblfrm1.pack(expand=YES)

    lbl2 = Label(lblfrm1, text="1) Order Online at www.startwriteindia.com." + "\n2) Call +(91) -905-133-1646")
    lbl2.pack(ipadx=40, ipady=30)

    def showresult():
        global lin_flag, user_id, user_mail, vaild_key, key_status
        name = str(name_ent.get())
        email = str(email_ent.get())
        key1 = str(key_ent1.get())
        key2 = str(key_ent2.get())
        validate_key_f = key1 + "-" + key2

        if '@' not in email_ent.get() or '.' not in email_ent.get():
            print('email needs @ and . at the same time')

        updated_key = []
        key = key_generation.key_generation(email, name)

        for i in range(len(key)):
            if i == 4:
                updated_key.append('-')

            if key[i].isdigit():
                updated_key.append(key[i])
                continue
            elif key[i].isalpha():
                updated_key.append(key[i].upper())
                continue
            else:
                pass

        np = ''
        for i in range(len(updated_key)):
            np += updated_key[i]

        if np == validate_key_f:
            key_wp.destroy()
            messagebox.showinfo("Registered", "Licence Key Registered")
            print("Key Matched")
            SWdb.update_data_into_license_table_with_key(name, email, validate_key_f)
            hlp.delete("Purchase Online")
            hlp.delete("Activate License")
            lin_flag = False
            user_id, user_mail, vaild_key, key_status = SWdb.fetching_data_from_license_table()
            hlp.entryconfigure("About Startwrite...",label ="About Startwrite...", command=aboutstartwrite)

        else:
            print("Try Again")
            key_wp.destroy()
            messagebox.showinfo("Warning", "Invalid Licence Key")

    abt_ent_key = ttk.Button(frm4, text="Activate", command=showresult)
    abt_ent_key.pack(side=LEFT, padx=4)

    abt_ord = ttk.Button(frm4, text="Order Online", command=lin_purchase_wp)
    abt_ord.pack(side=LEFT, padx=4)

    abt_ok = ttk.Button(frm4, text="Cancel", command=key_wp.destroy)
    abt_ok.pack(side=RIGHT, padx=4)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# ------------------------------------------------ ToolTip-hover function ------------------------------------------
class CreateToolTip(object):
    # create a tool-tip for a given widget
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 40

        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='right', background='white', relief='solid', borderwidth=1,
                         font=("times new rome", "10", "normal"))
        label.pack(ipadx=1)
        infolbl.configure(text=self.text)

    def close(self, event=None):
        if infolbl['text'] != '':
            infolbl.configure(text='')
        else:
            infolbl.configure(text=self.text)
        if self.tw:
            self.tw.destroy()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# ------------------------------------------- Hover Effect End ----------------------------------------------
class TkInterEx:
    @staticmethod
    def quit_app(event=None):
        SW_Main_UI.quit()

    def __init__(self, SW_Main_UI):
        pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Adding Scrolling Effect on both X,Y axis <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def addScrollingFigure(fig, sub):
    global canvas, mplCanvas, interior, interior_id, cwid
    canvas = Canvas(sub)  # set up a canvas with scrollbars
    canvas.grid(row=0, column=0, sticky=Tkconstants.NSEW)

    xScrollbar = Scrollbar(sub, orient=Tkconstants.HORIZONTAL)
    yScrollbar = Scrollbar(sub)

    xScrollbar.grid(row=1, column=0, sticky=Tkconstants.EW)
    yScrollbar.grid(row=0, column=1, sticky=Tkconstants.NS)

    canvas.config(xscrollcommand=xScrollbar.set)
    xScrollbar.config(command=canvas.xview)
    canvas.config(yscrollcommand=yScrollbar.set)
    yScrollbar.config(command=canvas.yview)
    # plug in the fig
    figAgg = FigureCanvasTkAgg(fig, canvas)
    mplCanvas = figAgg.get_tk_widget()

    cwid = canvas.create_window(0, 0, window=mplCanvas, anchor=Tkconstants.NW)
    canvas.config(scrollregion=canvas.bbox(Tkconstants.ALL), width=(wd-24), height=550)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Zoom Function For Bottom <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def changeSize(fig, factor):
    global canvas, mplCanvas, interior, interior_id, sub, cwid, change_size_count, r
    oldSize = fig.get_size_inches()

    fig.set_size_inches([factor * s for s in oldSize])
    wi, hi = [i * fig.dpi for i in fig.get_size_inches()]

    if wi < SW_global.r:
        SW_global.change_size_count = SW_global.change_size_count - 10
        zoomLabel.config(text = str(SW_global.change_size_count)+"%")
    if wi > SW_global.r:
        SW_global.change_size_count = SW_global.change_size_count + 10
        zoomLabel.config(text = str(SW_global.change_size_count)+"%")

    SW_global.r = wi

    mplCanvas.config(width=wi, height=hi)

    canvas.itemconfigure(cwid, width=wi, height=hi)
    canvas.config(scrollregion=canvas.bbox(Tkconstants.ALL), width=(wd-24), height=550)
    fig.canvas.draw()

def zoom_low():
    SW_global.currentpage -= 1
    if SW_global.currentpage == 0:
        smallerButton.config(state=DISABLED)

    if biggerButton["state"] != "normal":
        biggerButton.config(state=NORMAL)

def zoom_high():
    SW_global.currentpage += 1
    if SW_global.currentpage >= SW_global.pagecount:
        biggerButton.config(state=DISABLED)

    if smallerButton["state"] != "normal":
        smallerButton.config(state=NORMAL)

def zoom_minus():
    zoom_low()
    changeSize(fig, .9)

def zoom_plus():
    zoom_high()
    changeSize(fig, 1.1)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Minimize Windows <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
sub_flag = 0

def close_wn():
    global sub_flag
    if sub_flag == 1:
        sub.destroy()
        fig.canvas.draw()
    else:
        pass

def restaurar_wn():
    global sub_flag
    sub = Toplevel(writingareaframe, bg="gray")
    sub.overrideredirect(True)
    sub.lift()
    sub.wm_title("New Doc")
    sub.geometry("1350x568+0+145")
    sub.wm_transient(writingareaframe)
    addScrollingFigure(fig, sub)
    mainselector.update()
    canvas.configure(background='grey')
    print("This is check point 1")
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event',onclick2)
    fig.canvas.mpl_connect('button_release_event',onrelease)
    sub_flag = 1
    fig.canvas.draw()
    return



def findPos1(axesdata=None,start_point=None):
    print("I am in find pos1")
    print()
    current_cursor_pos=-999
    pos1_local=-999
    cur_temp_start=-999
    print("axesdata",axesdata)
    print("start_point",start_point)
    print("SW_global.guideline_axes",guideline_axes[l])
    print("cursor_pos",SW_global.cursor_pos)


    if(guideline_axes[l]==axesdata):
        for i in range(len(SW_global.cursor_pos)):
            if(start_point<=SW_global.cursor_pos[i]):
                print("This is check point 22")
                pos1_local=i-1
                cur_temp_start=pos1_local+1
                print(pos1_local,cur_temp_start)
                return pos1_local,cur_temp_start
                break
    else:
        for i in range(len(SW_global.axes_data)):
            print("*"*90)
            print(SW_global.axes_data[str(i)])
            print("*"*90)
            if(axesdata==SW_global.axes_data[str(i)]["axis_data"]):
                print(SW_global.axes_data[str(i)]["cursor_pos"])
                current_cursor_pos=[j for j in (SW_global.axes_data[str(i)]["cursor_pos"])]
                for j in range(len(current_cursor_pos)):
                    if(start_point<=current_cursor_pos[j]):
                        print("This is check point 33")
                        pos1_local=j-1
                        cur_temp_start=pos1_local+1
                        print(pos1_local,cur_temp_start)
                        return pos1_local,cur_temp_start
                        break

    ######  This is  for outside letter position #######
    # for outline of click we are sending  speacial value 10000
    if(axesdata==guideline_axes[l]):
        if(start_point>SW_global.cursor_pos[-1]):
            return 10000,1000
    else:
        for i in range(len(SW_global.axes_data)):
            if(axesdata==SW_global.axes_data[str(i)]["axis_data"]):
                if((SW_global.axes_data[str(i)]["cursor_pos"])[-1]<start_point):
                    return 10000,i


def findPos2(axesdata=None,end_point=None):
    print("This is from find pos2")
    print(axesdata)
    print(end_point)
    if(axesdata==guideline_axes[l]):
        print("This is in guide line axes")
        reversed_cursor_pos_local=[i for i in reversed(SW_global.cursor_pos)]
        for i in range(len(reversed_cursor_pos_local)):
            if(end_point>=reversed_cursor_pos_local[i]):
                pos2_local=i-1
                pos2_local=len(reversed_cursor_pos_local)-pos2_local-1-1
                cur_temp_end=pos2_local-1-1
                return pos2_local,cur_temp_end
                break
        #for i in range(len(reversed))
        #print("")
    else:
        for i in range(len(SW_global.axes_data)):
            if(axesdata==SW_global.axes_data[str(i)]["axis_data"]):
                reversed_cursor_pos_local=[j for j in reversed(SW_global.axes_data[str(i)]["cursor_pos"])]
                for j in range(len(reversed_cursor_pos_local)):
                    if(end_point>=reversed_cursor_pos_local[j]):
                        pos2_local=j-1
                        pos2_local=len(reversed_cursor_pos_local)-pos2_local-1-1
                        cur_temp_end=pos2_local-1-1
                        return pos2_local,cur_temp_end
                        break


    if(axesdata==guideline_axes[l]):
        if(end_point>SW_global.cursor_pos[-1]):
            return 10000,1000
    else:
        for i in range(len(SW_global.axes_data)):
            if(SW_global.axes_data[str(i)]["axis_data"]==end_axes):
                if((SW_global.axes_data[str(i)]["cursor_pos"])[-1]<end_point):
                    return 10000,i


def select_string_for_copy_paste(pos1=None,start_axes=None,start_axes_key=None,pos2=None,end_axes=None,end_axes_key=None):
    try:
        copy_string=""
        if(start_axes==end_axes):
            print("check point 555***********************************************")
            if(start_axes==guideline_axes[l]):
                for i in range(pos1,pos2+1):
                    copy_string=copy_string+str(delete_list[i])
            else:
                temp_start_axes=None
                for i in range(len(SW_global.axes_data)):
                    if(SW_global.axes_data[str(i)]["axis_data"]==start_axes):
                        for j in range(pos1,pos2+1):
                            copy_string=copy_string+str((SW_global.axes_data[str(i)]["delete_list"])[j])
        else:
            print("check point 666*************************************************")
            if(start_axes==guideline_axes[l]):
                print("check point 101010 **************************************")
                temp_count=0
                for j in range(len(SW_global.axes_data)):
                    print(end_axes)
                    print(SW_global.axes_data[str(j)]["axis_data"])
                    if(SW_global.axes_data[str(j)]["axis_data"]==end_axes):
                        for k in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                            if((pos2)+1>=k):
                                copy_string=copy_string+str((SW_global.axes_data[str(j)]["delete_list"])[k])
                    if(j>end_axes_key):
                        for k in SW_global.axes_data[str(j)]["delete_list"]:
                            #copy_string=copy_string+str((SW_global.axes_data[str(j)]["delete_list"])[k])
                            copy_string=copy_string+str(k)

                for j in range(len(delete_list)):
                    if(j<=pos1):
                        copy_string=copy_string+str(delete_list[j])
            else:
                print("check point 777************************************************")
                if(end_axes==guideline_axes[l]):
                    for j in range(len(SW_global.axes_data)):
                        if(start_axes==SW_global.axes_data[str(j)]["axis_data"]):
                            for k in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                                if(k>=pos1):
                                    copy_string=copy_string+str((SW_global.axes_data[str(j)]["delete_list"])[k])
                        if(j>start_axes_key):
                            for k in SW_global.axes_data[str(j)]["delete_list"]:
                                copy_string=copy_string+str(k)

                    for j in range(0,pos2+1):
                        copy_string=copy_string+str(delete_list[j])
                else:
                    print("check point 888**************************************************")
                    if(start_axes_key<end_axes_key):
                        for j in range(len(SW_global.axes_data)):
                            if(j==start_axes_key):
                                for k in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                                    if(k>=pos1):
                                        copy_string=copy_string+(SW_global.axes_data[str(j)]["delete_list"])[k]
                            if(j==end_axes_key):
                                for k in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                                    if(k<=pos2):
                                        copy_string=copy_string+str((SW_global.axes_data[str(j)]["delete_list"])[k])
                            if((j>start_axes_key) and (j<end_axes_key)):
                                for k in SW_global.axes_data[str(j)]["delete_list"]:
                                    copy_string=copy_string+str(k)
                    else:
                        print("check point 999 ***********************************************************")
                        if(start_axes_key>end_axes_key):
                            for j in range(len(SW_global.axes_data)):
                                if(i==end_axes_key):
                                    for k in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                                        if(pos2+1>=k):
                                            copy_string=copy_string+((SW_global.axes_data[str(j)]["delete_list"])[k])

                                if(i==start_axes_key):
                                    for k in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                                        if(k<=pos1):
                                            copy_string=copy_string+((SW_global.axes_data[str(j)]["delete_list"])[k])
                                if((j>end_axes_key) and (j<start_axes_key)):
                                    for k in SW_global.axes_data[str(j)]["delete_list"]:
                                        copy_string=copy_string+str(k)

            #temp_end_axes=None


    except Exception as e:
        print(e)
        pass


    return copy_string


def create_new_page_on_box_data(delete_list1=None,kern_value_array1=None):
    print("I am in create_new_page_on_box_data")
    a=dict()
    a["startdot_on_off"]=SW_global.startdot_on_off
    a["decisiondot_on_off"]=SW_global.decisiondot_on_off
    a["stokearrow_on_off"]=SW_global.stokearrow_on_off
    a["connectdot_on_off"]=SW_global.connectdot_on_off
    a["color_letter_features_on_off"]=color_letter_features_on_off
    a["letter_out_line_on_off"]=letter_out_line_on_off
    a["SW_global_axes_data"]=SW_global.axes_data.copy()
    a["SW_global.left"]=SW_global.left
    a["SW_global.right"]=SW_global.right
    a["SW_global.bottom"]=SW_global.bottom
    a["SW_global.top"]=SW_global.top
    a["letters_already_written"]=SW_global.letters_already_written
    a["axes_list"]=[]
    for j in range(len(SW_global.axes_data)):
        a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])
    a["axes_list"].append(guideline_axes[l])
    a["count_for_height"]=SW_global.count_for_height
    a["guideline_axes"]=guideline_axes[l]
    a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
    a["cursor_data"]=SW_global.cursor_data.copy()
    a["cursor_pos"]=SW_global.cursor_pos.copy()
    a["kern_value_array"]=kern_value_array.copy()
    a["kern_list"]=(SW_global.kern_list).copy()
    a["delete_list"]=delete_list.copy()
    a["gl"]=gl
    a["gb"]=gb
    a["sl_t"]=sl_t
    a["sl_b"]=sl_b
    a["l"]=l
    a["key_c"]=key_c
    a["call_g"]=call_g
    a["gl"]=gl
    a["back_axes"]=SW_global.back_axes
    print("check point 1")
    SW_global.box_data[str(len(SW_global.box_data))]=a
    return



def checking_for_which_box_need_to_switch(axesdata=None):
    print("I am in key finding")
    if(axesdata!=None):
        for j in range(len(SW_global.box_data)):
            check_axes_list=SW_global.box_data[str(j)]["axes_list"]
            if(axesdata in check_axes_list):
                return j
                break




def data_Switching2(key=None):
    if(key!=None):
        print("I am in data Switching")
        kern_value_array1=[]
        delete_list1=[]
        print("This is Switching key",key)
        a=SW_global.box_data[str(key)]
        SW_global.startdot_on_off=a["startdot_on_off"]
        SW_global.decisiondot_on_off=a["decisiondot_on_off"]
        SW_global.stokearrow_on_off=a["stokearrow_on_off"]
        SW_global.connectdot_on_off=a["connectdot_on_off"]
        def rt(a):
            color_letter_features_on_off=a["color_letter_features_on_off"]
        rt(a)
        def tr(a):
            letter_out_line_on_off=a["letter_out_line_on_off"]
        tr(a)
        SW_global.left=a["SW_global.left"]
        SW_global.right=a["SW_global.right"]
        SW_global.bottom=a["SW_global.bottom"]
        SW_global.letters_already_written=a["letters_already_written"]
        SW_global.top=a["SW_global.top"]
        SW_global.count_for_height=a["count_for_height"]
        guideline_axes[l]=a["guideline_axes"]
        guideline_axes[l].lines=(a["guideline_axes_lines"]).copy()
        SW_global.cursor_data=a["cursor_data"].copy()
        SW_global.cursor_pos=a["cursor_pos"].copy()
        kern_value_array1.clear()
        SW_global.back_axes=a["back_axes"]
        for j in a["kern_value_array"]:
            kern_value_array1.append(j)
        SW_global.kern_list.clear()
        SW_global.kern_list=a["kern_list"].copy()
        delete_list1.clear()
        for j in a["delete_list"]:
            delete_list1.append(j)
        def cd(a):
          #  delete_list=a["delete_list"].copy()
            gl=a["gl"]
            gb=a["gb"]
            sl_t=a["sl_t"]
            sl_b=a["sl_b"]
            call_g=a["call_g"]
    #        a["key_c"]=key_c
        cd(a)
        SW_global.axes_data=a["SW_global_axes_data"].copy()
        def oi(a):
            l=a["l"]

        print("This is ",delete_list)
        print("This is ",kern_value_array)
        print("This is guideline_axes[l]",guideline_axes[l])

        return delete_list1,kern_value_array1,a["gl"],a["gb"],a["sl_t"],a["sl_b"],a["call_g"]

#     return 

def data_update(key=None,kern_value_array1=None,delete_list1=None):
    print("I am in update data ")
    a=dict()
    if(key!=None):
        a["startdot_on_off"]=SW_global.startdot_on_off
        a["decisiondot_on_off"]=SW_global.decisiondot_on_off
        a["stokearrow_on_off"]=SW_global.stokearrow_on_off
        a["connectdot_on_off"]=SW_global.connectdot_on_off
        a["color_letter_features_on_off"]=color_letter_features_on_off
        a["letter_out_line_on_off"]=letter_out_line_on_off
        a["SW_global_axes_data"]=SW_global.axes_data.copy()
        a["SW_global.left"]=SW_global.left
        a["SW_global.right"]=SW_global.right
        a["SW_global.bottom"]=SW_global.bottom
        a["SW_global.top"]=SW_global.top
        a["letters_already_written"]=SW_global.letters_already_written
        a["axes_list"]=[]
        for j in range(len(SW_global.axes_data)):
            a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])
        a["axes_list"].append(guideline_axes[l])
        a["count_for_height"]=SW_global.count_for_height
        a["guideline_axes"]=guideline_axes[l]
        a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
        a["cursor_data"]=SW_global.cursor_data.copy()
        a["cursor_pos"]=SW_global.cursor_pos.copy()
        a["kern_value_array"]=kern_value_array
        a["kern_list"]=(SW_global.kern_list).copy()
        a["delete_list"]=delete_list.copy()
        a["gl"]=gl
        a["gb"]=gb
        a["sl_t"]=sl_t
        a["sl_b"]=sl_b
        a["l"]=l
        a["key_c"]=key_c
        a["call_g"]=call_g
        a["gl"]=gl
        a["back_axes"]=SW_global.back_axes
        print("check point 1")
        SW_global.box_data[str(key)]=a
        print("This is box_data")
        print(SW_global.box_data)
    return kern_value_array1,delete_list1


# def data_checking_for_need_to_create_new_page_or_update_box(axesdata=None,delete_list1=None,kern_value_array1=None):
#     try:
#         checkflag=-999
#         for j in range(len(SW_global.box_data)):
#             check_axes=SW_global.box_data[str(j)]["axes_list"]
#             if(axesdata in check_axes):
#                 data_update(key=j,delete_list1=delete_list1,kern_value_array1=kern_value_array1)
#                 checkflag=1000

#         if(checkflag<0):
#             create_new_page_on_box_data(delete_list1=delete_list1,kern_value_array1=kern_value_array1)





#     except Exception as e:
#         print(e)


def data_checking_for_need_to_create_or_update_back_page(axes_list=None,delete_list1=None,kern_value_array1=None):
    print("I am in data checking or update part ")
    check_flag=-999
    for k in range(len(SW_global.box_data)):
        for j in axes_list:
            if(j in (SW_global.box_data[str(k)]["axes_list"])):
                data_update(key=k,kern_value_array1=kern_value_array1,delete_list1=delete_list1)
                check_flag=1000
                break
    if(check_flag==-999):
        create_new_page_on_box_data(kern_value_array1=kern_value_array1,delete_list1=delete_list1)


    return 


def data_Switching(key=None,kern_value_array=None,delete_list=None):
    print(key)
    print(kern_value_array)
    print(delete_list)
    if(key!=None):
        print("need to shift")
        try:
            for i in range(len(SW_global.axes_data)):
                for k in SW_global.axes_data[str(i)]["cursor_data"]:
                    k.set_visible(False)
        except Exception as e:
            pass
        check_flag=-1
        if(len(SW_global.box_data)==0):
            print("This is check pouint 22222")
            a=dict()
            a["startdot_on_off"]=SW_global.startdot_on_off
            a["decisiondot_on_off"]=SW_global.decisiondot_on_off
            a["stokearrow_on_off"]=SW_global.stokearrow_on_off
            a["connectdot_on_off"]=SW_global.connectdot_on_off
            a["color_letter_features_on_off"]=color_letter_features_on_off
            a["letter_out_line_on_off"]=letter_out_line_on_off
            a["SW_global_axes_data"]=SW_global.axes_data.copy()
            a["SW_global.left"]=SW_global.left
            a["SW_global.right"]=SW_global.right
            a["SW_global.bottom"]=SW_global.bottom
            a["SW_global.top"]=SW_global.top
            a["letters_already_written"]=SW_global.letters_already_written
            a["axes_list"]=[]
            for j in range(len(SW_global.axes_data)):
                a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])
            a["axes_list"].append(guideline_axes[l])
            a["count_for_height"]=SW_global.count_for_height
            a["guideline_axes"]=guideline_axes[l]
            a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
            a["cursor_data"]=SW_global.cursor_data.copy()
            a["cursor_pos"]=SW_global.cursor_pos.copy()
            a["kern_value_array"]=kern_value_array
            a["kern_list"]=(SW_global.kern_list).copy()
            a["delete_list"]=delete_list.copy()
            a["gl"]=gl
            a["gb"]=gb
            a["sl_t"]=sl_t
            a["sl_b"]=sl_b
            a["l"]=l
            a["key_c"]=key_c
            a["call_g"]=call_g
            a["gl"]=gl
            print("check point 1")
            SW_global.box_data[len(SW_global.box_data)]=a
            SW_global.kern_list.clear()
            kern_value_array.clear()
            SW_global.kern_list.insert(0,0)
            kern_value_array.insert(0,0)
            SW_global.cursor_pos.clear()
            SW_global.cursor_pos.insert(0,0)
            SW_global.cursor_data.clear()
            delete_list.clear()
            SW_global.axes_data.clear()
            SW_global.count_for_height=0
        else:
            print("check point2")
            if(len(SW_global.axes_data)>0):
                check_axis=SW_global.axes_data[str(0)]["axis_data"]
                for j in range(len(SW_global.box_data)):
                    check_array_of_axes=SW_global.box_data[str(j)]["axis_data"]
                    if(check_axis  in check_array_of_axes):
                        a=dict()
                        a["startdot_on_off"]=SW_global.startdot_on_off
                        a["decisiondot_on_off"]=SW_global.decisiondot_on_off
                        a["stokearrow_on_off"]=SW_global.stokearrow_on_off
                        a["connectdot_on_off"]=SW_global.connectdot_on_off
                        a["color_letter_features_on_off"]=color_letter_features_on_off
                        a["letter_out_line_on_off"]=letter_out_line_on_off
                        a["SW_global_axes_data"]=SW_global.axes_data.copy()
                        a["SW_global.left"]=SW_global.left
                        a["SW_global.right"]=SW_global.right
                        a["SW_global.bottom"]=SW_global.bottom
                        a["SW_global.top"]=SW_global.top
                        a["axes_list"]=[]
                        for k in range(len(SW_global.axes_data)):
                            a["axes_list"].append(SW_global.axes_data[str(k)]["axis_data"])

                        a["axes_list"].append(guideline_axes)
                        a["count_for_height"]=SW_global.count_for_height
                        a["guideline_axes"]=guideline_axes[l]
                        a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
                        a["cursor_data"]=SW_global.cursor_data.copy()
                        a["cursor_pos"]=SW_global.cursor_pos.copy()
                        a["kern_value_array"]=kern_value_array
                        a["kern_list"]=(SW_global.kern_list).copy()
                        a["delete_list"]=delete_list.copy()
                        # a["n"]=n
                        # a["old_l"]=old_l
                        a["gl"]=gl
                        a["gb"]=gb
                        a["sl_t"]=sl_t
                        a["sl_b"]=sl_b
                        a["l"]=l
                        a["key_c"]=key_c
                        a["call_g"]=call_g
                        a["gl"]=gl
                        SW_global.box_data[str(j)]=a

                        SW_global.box_data[len(SW_global.box_data)]=a
                        SW_global.kern_list.clear()
                        kern_value_array.clear()
                        SW_global.kern_list.insert(0,0)
                        kern_value_array.insert(0,0)
                        SW_global.cursor_pos.clear()
                        SW_global.cursor_pos.insert(0,0)
                        SW_global.cursor_data.clear()
                        delete_list.clear()
                        SW_global.axes_data.clear()
                       # reset_after()
                        SW_global.count_for_height=0
                      #  newCreateGuideLine(1,None,None,None,None)  
                        check_flag=10 
            else:
                print("check point 3")
                print(SW_global.box_data)
                check_axes=guideline_axes[l]
                for j in range(len(SW_global.box_data)):
                    print(SW_global.box_data[str(j)])
                    check_array_of_axes=SW_global.box_data[str(j)]["guideline_axes"]
                    if(check_axes==check_array_of_axes):
                        a=dict()
                        a["startdot_on_off"]=SW_global.startdot_on_off
                        a["decisiondot_on_off"]=SW_global.decisiondot_on_off
                        a["stokearrow_on_off"]=SW_global.stokearrow_on_off
                        a["connectdot_on_off"]=SW_global.connectdot_on_off
                        a["color_letter_features_on_off"]=color_letter_features_on_off
                        a["letter_out_line_on_off"]=letter_out_line_on_off
                        a["SW_global_axes_data"]=SW_global.axes_data.copy()
                        a["SW_global.left"]=SW_global.left
                        a["SW_global.right"]=SW_global.right
                        a["SW_global.bottom"]=SW_global.bottom
                        a["SW_global.top"]=SW_global.top
                        a["axes_list"]=[]
                        for j in range(len(SW_global.axes_data)):
                            a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])
                        # a["s"]=s
                        a["axes_list"].append(guideline_axes[l])
                        a["count_for_height"]=SW_global.count_for_height
                        a["guideline_axes"]=guideline_axes[l]
                        a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
                        a["cursor_data"]=SW_global.cursor_data.copy()
                        a["cursor_pos"]=SW_global.cursor_pos.copy()
                        a["kern_value_array"]=kern_value_array
                        a["kern_list"]=(SW_global.kern_list).copy()
                        a["delete_list"]=delete_list.copy()
                        delete_list.clear()
                        # a["n"]=n
                        # a["old_l"]=old_l
                        a["gl"]=gl
                        a["gb"]=gb
                        a["sl_t"]=sl_t
                        a["sl_b"]=sl_b
                        a["l"]=l
                        a["key_c"]=key_c
                        a["call_g"]=call_g
                        a["gl"]=gl
                        SW_global.box_data[str(j)]=a
                        SW_global.kern_list.clear()
                        kern_value_array.clear()
                        SW_global.kern_list.insert(0,0)
                        kern_value_array.insert(0,0)
                        SW_global.cursor_pos.clear()
                        SW_global.cursor_pos.insert(0,0)
                        SW_global.cursor_data.clear()
                        delete_list.clear()
                        SW_global.axes_data.clear()
                    #    reset_after()
                        SW_global.count_for_height=0
                     #   newCreateGuideLine(1,None,None,None,None)   
                        check_flag=10

                    #else:
                if(check_flag==-1):
                    print("check point 4")
                    a=dict()
                    a["startdot_on_off"]=SW_global.startdot_on_off
                    a["decisiondot_on_off"]=SW_global.decisiondot_on_off
                    a["stokearrow_on_off"]=SW_global.stokearrow_on_off
                    a["connectdot_on_off"]=SW_global.connectdot_on_off
                    a["color_letter_features_on_off"]=color_letter_features_on_off
                    a["letter_out_line_on_off"]=letter_out_line_on_off
                    a["SW_global_axes_data"]=SW_global.axes_data.copy()
                    a["SW_global.left"]=SW_global.left
                    a["SW_global.right"]=SW_global.right
                    a["SW_global.bottom"]=SW_global.bottom
                    a["SW_global.top"]=SW_global.top
                    a["axes_list"]=[]
                    for j in range(len(SW_global.axes_data)):
                        a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])
                    a["axes_list"].append(guideline_axes[l])
                    # a["s"]=s
                    a["count_for_height"]=SW_global.count_for_height
                    a["guideline_axes"]=guideline_axes[l]
                    a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
                    a["cursor_data"]=SW_global.cursor_data.copy()
                    a["cursor_pos"]=SW_global.cursor_pos.copy()
                    a["kern_value_array"]=kern_value_array
                    a["kern_list"]=(SW_global.kern_list).copy()
                    a["delete_list"]=delete_list.copy()
                    a["gl"]=gl
                    a["gb"]=gb
                    a["sl_t"]=sl_t
                    a["sl_b"]=sl_b
                    a["l"]=l
                    a["key_c"]=key_c
                    a["call_g"]=call_g
                    a["gl"]=gl
                    SW_global.box_data[len(SW_global.box_data)]=a
                    print(SW_global.box_data)
                    SW_global.kern_list.clear()
                    kern_value_array.clear()
                    SW_global.kern_list.insert(0,0)
                    kern_value_array.insert(0,0)
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_pos.insert(0,0)
                    SW_global.cursor_data.clear()
                    delete_list.clear()
                    SW_global.axes_data.clear()
                    SW_global.count_for_height=0

        a=SW_global.box_data[str(key)]
        SW_global.startdot_on_off=a["startdot_on_off"]
        SW_global.decisiondot_on_off=a["decisiondot_on_off"]
        SW_global.stokearrow_on_off=a["stokearrow_on_off"]
        SW_global.connectdot_on_off=a["connectdot_on_off"]
        def rt(a):
            color_letter_features_on_off=a["color_letter_features_on_off"]
        rt(a)
        def tr(a):
            letter_out_line_on_off=a["letter_out_line_on_off"]
        tr(a)
        SW_global.left=a["SW_global.left"]
        SW_global.right=a["SW_global.right"]
        SW_global.bottom=a["SW_global.bottom"]
        SW_global.top=a["SW_global.top"]
        SW_global.count_for_height=a["count_for_height"]
        guideline_axes[l]=a["guideline_axes"]
        guideline_axes[l].lines=(a["guideline_axes_lines"]).copy()
        SW_global.cursor_data=a["cursor_data"].copy()
        SW_global.cursor_pos=a["cursor_pos"].copy()
        kern_value_array.clear()
        for j in a["kern_value_array"]:
            kern_value_array.append(j)
       # def ch(a,kern_value_array=None):
        #    kern_value_array=a["kern_value_array"].copy()
            #kern_value_array=a["kern_value_array"].copy()
        #ch(a,kern_value_array=kern_value_array)
        SW_global.kern_list.clear()

        SW_global.kern_list=a["kern_list"].copy()
        delete_list.clear()
        for j in a["delete_list"]:
            delete_list.append(j)
        def cd(a):
          #  delete_list=a["delete_list"].copy()
            gl=a["gl"]
            gb=a["gb"]
            sl_t=a["sl_t"]
            sl_b=a["sl_b"]
            call_g=a["call_g"]
            a["key_c"]=key_c
        cd(a)
        SW_global.axes_data=a["SW_global_axes_data"].copy()
        def oi(a):
            l=a["l"]

        print("This is ",delete_list)
        print("This is ",kern_value_array)

        
        


    return 


def set_guideLine_variables(kern_value_array1=None,delete_list1=None,kern_list1=None,recent1=None,lines1=None,cursor_pos1=None,cursor_data1=None,letters_already_written=None):
    if((kern_value_array1!=None) and(delete_list1!=None) and(kern_list1!=None) and(recent1!=None) and(lines1!=None) and(cursor_pos1!=None) and(cursor_data1!=None)):
        kern_value_array.clear()
        kern_value_array.extend(kern_value_array1)
        delete_list.clear()
        delete_list.extend(delete_list1)
        SW_global.kern_list.clear()
        SW_global.kern_list.extend(kern_list1.copy())
        SW_global.recent_input_list.clear()
        SW_global.recent_input_list.extend(recent1)
        guideline_axes[l].lines.clear()
        guideline_axes[l].lines.extend(lines1)
        SW_global.cursor_pos.clear()
        SW_global.cursor_pos.extend(cursor_pos1)
        SW_global.cursor_data.clear()
        SW_global.cursor_data.extend(cursor_data1)
        SW_global.letters_already_written.clear()
        SW_global.letters_already_written.extend(letters_already_written)
    return

def paste_on_axes():
    #### paste have some problem 
    ### cut have some style related problem ###
    import pyperclip
    k1=list(pyperclip.paste())
    print("This click x",SW_global.click_x)
    print("This release x",SW_global.release_x)
    print("This is len(k1)",len(k1))
    if(int(SW_global.click_x)==int(SW_global.release_x) and(len(k1)!=0)):
        print("This is possible")
        key=None
        if(SW_global.current_axes==guideline_axes[l]):
            key=len(SW_global.axes_data)
        else:
            for j in range(len(SW_global.axes_data)):
                if(SW_global.current_axes==SW_global.axes_data[str(j)]["axis_data"]):
                    key=j

        pos4=None
        if(int(SW_global.click_x)==0):
            pos4=0
        else:
            for j in range(len(SW_global.axes_data)):
                if(SW_global.current_axes==SW_global.axes_data[str(j)]["axis_data"]):
                    for k1 in range(len(SW_global.axes_data[str(j)]["cursor_pos"])):
                        if((SW_global.axes_data[str(j)]["cursor_pos"])[k1]>SW_global.click_x): #### may need to check 
                            pos4=k1
                            break
            if(pos4==None):
                if(key==len(SW_global.axes_data)):
                    pos4=len(delete_list)
                else:
                    pos4=len(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"])
        #for j in range()
            #elif(pos4==1):
            #    if((len(SW_global.cursor_pos)>2) and(SW_global.cursor_pos[1]>))
        temp_delete_list=[]
        if(len(SW_global.axes_data)>key):
            if(pos4>=len(SW_global.axes_data[str(key)]["delete_list"])):
                temp_delete_list.extend(SW_global.axes_data[str(key)]["delete_list"])
                import pyperclip
                k1=list(pyperclip.paste())
                temp_delete_list.extend(k1)
                clear_digit_from_axes(axesdata=SW_global.axes_data[str(key)]["axis_data"])
                for j in range(len(SW_global.axes_data)):
                    if(j>key):
                        temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                        clear_digit_from_axes(axesdata=SW_global.axes_data[str(key)]["axis_data"])
            else:
                for j in range(len(SW_global.axes_data[str(key)]["delete_list"])):
                    if(j==pos4):
                        import pyperclip
                        k1=list(pyperclip.paste())
                    temp_delete_list.append((SW_global.axes_data[str(key)]["delete_list"])[j])
                clear_digit_from_axes(axesdata=SW_global.axes_data[str(key)]["axis_data"])
                for j in range(len(SW_global.axes_data)):
                    if(j>key):
                        temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                        clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
            clear_digit_from_axes(axesdata=guideline_axes[l])
            temp_delete_list.extend(delete_list.copy())
            temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
            count1=len(SW_global.axes_data)
            temp_count=key
            for j in range(len(temp)):
                if(temp_count<count1):
                    base_array=[]
                    for k1 in range(4):
                        base_array.append((SW_global.axes_data[str(temp_count)]["lines"])[k1])

                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(j)]["axis_data"],baselines_objects_array=base_array)
                    save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=temp_count,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(temp_count)]["axis_data"],lines1=temp_guideline_axes2,kern_list1=temp_kern_list)
                elif(temp_count==count1):
                    base_array=[]
                    for k1 in range(4):
                        base_array.append(guideline_axes[l].lines[k1])
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                    set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=SW_global.kern_list,recent1=SW_global.recent_input_list,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                elif(temp_count>count1):
                    save_data_to_axes_dict(kern_value1=kern_value_array,delete_list1=delete_list,recent_input_list1=SW_global.recent_input_list,cursor_pos1=SW_global.cursor_pos,cursor_data1=SW_global.cursor_data,axes_key_index=None,letters_already_written1=SW_global.letters_already_written,axesdata=guideline_axes[l],lines1=guideline_axes[l].lines,kern_list1=SW_global.kern_list)
                    newCreateGuideLine(1,None,None,None,None)
                    base_array=[]
                    for k1 in range(4):
                        base_array.append(guideline_axes[l].lines[k1])
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                    set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=SW_global.kern_list,recent1=SW_global.recent_input_list,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                temp_count=temp_count+1
        else:
            clear_digit_from_axes(axesdata=guideline_axes[l])
            if(len(delete_list)>=pos4):
                temp_delete_list.extend(delete_list)
                import pyperclip
                k1=list(pyperclip.paste())
                temp_delete_list.extend(k1)
            else:
                for j in range(len(delete_list)):
                    if(j==pos4):
                        import pyperclip
                        k1=list(pyperclip.copy())
                        temp_delete_list.extend(k1)
                    temp_delete_list.append(delete_list[j])
            temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
            count1=len(SW_global.axes_data)
            temp_count=key
            for j in range(len(temp)):
                if(temp_count==count1):
                    base_array=[]
                    for k1 in range(4):
                        base_array.append(guideline_axes[l].lines[k1])
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                    set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=SW_global.kern_list,recent1=SW_global.recent_input_list,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                elif(temp_count>count1):
                    save_data_to_axes_dict(kern_value1=kern_value_array,delete_list1=delete_list,recent_input_list1=SW_global.recent_input_list,cursor_pos1=SW_global.cursor_pos,cursor_data1=SW_global.cursor_data,axes_key_index=None,letters_already_written1=SW_global.letters_already_written,axesdata=guideline_axes[l],lines1=guideline_axes[l].lines,kern_list1=SW_global.kern_list)
                    newCreateGuideLine(1,None,None,None,None)
                    for k1 in range(4):
                        base_array.append(guideline_axes[l].lines[k1])
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                    set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=SW_global.kern_list,recent1=SW_global.recent_input_list,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                temp_count=temp_count+1
            
    else:
        print("This is not possible")
    fig.canvas.draw()

    return



#### Method  for cut operation #####
##### This is method for Ctrl+x #####
def cut_for_single_guideor_multiple_guide(pos1=None,pos2=None,end_axes=None,start_axes=None):
    print("I am from cut")
    temp_delete_list=[]
    if(SW_global.click_x!=SW_global.release_x):
        if((pos1!=None) and (pos2!=None) and(start_axes!=None) and (end_axes!=None)):
            if(start_axes==end_axes):
                print("on same axes")
                if(start_axes==guideline_axes[l]):
                    print("This is on guideline_axes")
                    print("pos1",pos1)
                    print("pos2",pos2)
                    for j in range(len(delete_list)):
                        if((j<pos1) or (j>pos2)):
                            temp_delete_list.append(delete_list[j])
                    clear_digit_from_axes(axesdata=guideline_axes[l])
                    for j in range(4):
                        (guideline_axes[l].lines[j]).set_visible(False)
                    base_array=[]
                    print("Temp delete _list",temp_delete_list)
                    print("This is guideline_axes[l]",guideline_axes[l].lines)
                    for j in range(4):
                        base_array.append(guideline_axes[l].lines[j])
                    #    guideline_axes[l].lines[j].set_visible(True)
                    for j in range(4):
                        (base_array[j]).set_visible(True)
                    
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp_delete_list,spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                    # for j in range(4):
                    #     temp_guideline_axes2[j].set_visible(False)
                    set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=temp_kern_list,recent1=temp_recent,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                    #for j in base_array:
                    #    j.set_visible(True)
                else:
                    temp_delete_list.clear()
                    key=None
                    print("Not in guideline axes ")
                    for j in range(len(SW_global.axes_data)):
                        if(SW_global.axes_data[str(j)]["axis_data"]==start_axes):
                            for k1 in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                                if((k1<pos1) or(k1>pos2)):
                                    temp_delete_list.append((SW_global.axes_data[str(j)]["delete_list"])[k1])
                            clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                            key=j
                        elif((key!=None) and(key>j)):
                            temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                            clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                    clear_digit_from_axes(axesdata=guideline_axes[l])
                    temp_delete_list.extend(delete_list.copy())
                    temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                    count=len(SW_global.axes_data)-1
                    temp_count=key
                    if(temp_count!=None):
                        for j in range(len(temp)):
                            if(temp_count<=count):
                                base_array=[]
                                for k1 in range(4):
                                    base_array.append((SW_global.axes_data[str(temp_count)]["lines"])[k1])
                                temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                            elif(temp_count==count+1):
                                base_array=[]
                                for k in range(4):
                                    base_array.append(guideline_axes[l].lines[k])
                                temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                            temp_count=temp_count+1
                        if temp_count<=count:
                            guideline_axes[l].set_visible(False)
                            #guideline_axes[l]=SW_global.axes_data[str(temp_count)]["axis_data"]
                            for j in range(temp_count,count+1):
                                (SW_global.axes_data[str(j)]["axis_data"]).set_visible(False)
                                del SW_global.axes_data[str(j)]
                            
                            guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                            set_guideLine_variables(kern_value_array1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"],delete_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"],kern_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"],recent1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"],lines1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"],cursor_pos1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"],cursor_data1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"],letters_already_written=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                            #set_guideLine_variables(kern_value_array1=None,delete_list1=None,kern_list1=None,recent1=None,lines1=None,cursor_pos1=None,cursor_data1=None,letter_already_written=SW_global.axes_data[])
                            
                            ### need to attach boder art related conditions ###                   
                    ##### need to add divide letter function #####
            else:
                print("Not on same axes")
                temp_delete_list=[]
                key1=None
                key2=None
                start_erase=None
                end_erase=None
                if(start_axes==guideline_axes):
                    print("check point 1")
                    for j in range(len(SW_global.axes_data)):
                        if(end_axes==SW_global.axes_data[str(j)]["axis_data"]):
                            start_erase=j
                            for k1 in range(pos2,len(SW_global.axes_data[str(j)]["delete_list"])):
                                temp_delete_list.append((SW_global.axes_data[str(j)]["delete_list"])[k1])
                        clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                    clear_digit_from_axes(axesdata=guideline_axes[l])    
                    for j in range(0,pos1):
                        temp_delete_list.append(delete_list[j])
                    temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                    temp_count=start_erase
                    count1=len(SW_global.axes_data)
                    for j in range(len(temp)):
                        if(temp_count<count1):
                            base_array=[]
                            for k1 in range(4):
                                base_array.append((SW_global.axes_data[str(temp_count)]["lines"])[k1])
                            temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                            save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=temp_count,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(temp_count)]["axis_data"],lines1=temp_guideline_axes2,kern_list1=temp_kern_list)
                        elif(temp_count==count1):
                            base_array=[]
                            for k1 in range(4):
                                base_array.append(guideline_axes[l].lines[k1])
                            temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                            set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=temp_kern_list,recent1=temp_recent,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                        temp_count=temp_count+1
                    if(temp_count==count1):
                        guideline_axes[l].set_visible(False)
                        guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                        set_guideLine_variables(kern_value_array1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"],delete_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"],kern_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"],recent1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"],lines1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"],cursor_pos1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"],cursor_data1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"],letters_already_written=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                        # for j in range(temp_count,count1):
                        #     del SW_global.axes_data[str(j)]
                    elif(temp_count<count1):
                        guideline_axes[l].set_visible(False)
                        for j in range(temp_count,count1):
                            (SW_global.axes_data[str(j)]["axis_data"]).set_visible(False)
                            del SW_global.axes_data[str(j)]
                        guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                        set_guideLine_variables(kern_value_array1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"],delete_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"],kern_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"],recent1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"],lines1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"],cursor_pos1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"],cursor_data1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"],letters_already_written=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                    SW_global.current_axes=guideline_axes[l]
                    if(pos1>=len(delete_list)):
                        SW_global.current_pos=len(delete_list)-1
                    else:
                        SW_global.current_pos=SW_global.cursor_pos[pos1]
                    


                elif(end_axes==guideline_axes[l]):
                    print("check point 2")
                    print("This is pos1",pos1)
                    print("This is pos2",pos2)
                    for j in range(len(SW_global.axes_data)):
                        if(start_axes==SW_global.axes_data[str(j)]["axis_data"]):
                            start_erase=j
                            for k1 in range(pos1):
                                temp_delete_list.append((SW_global.axes_data[str(j)]["delete_list"])[k1])
                        clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                    if(pos2-1>=0):
                        pos2=pos2-1

                    for j in range(pos2,len(delete_list)):
                        temp_delete_list.append(delete_list[j])
                    clear_digit_from_axes(axesdata=guideline_axes[l])
                    print("temp_delete_list2",temp_delete_list)
                    temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                    #temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                    temp_count=start_erase
                    count1=len(SW_global.axes_data)
                    for j in range(len(temp)):
                        if(temp_count<count1):
                            base_array=[]
                            for k1 in range(4):
                                base_array.append((SW_global.axes_data[str(temp_count)]["lines"])[k1])
                            temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                            save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=temp_count,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(temp_count)]["axis_data"],lines1=temp_guideline_axes2,kern_list1=temp_kern_list)
                        elif(temp_count==count1):
                            base_array=[]
                            for k1 in range(4):
                                base_array.append(guideline_axes[l].lines[k1])
                            temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                            set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=temp_kern_list,recent1=temp_recent,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                        temp_count=temp_count+1
                    if(temp_count==count1):
                        guideline_axes[l].set_visible(False)
                        guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                        set_guideLine_variables(kern_value_array1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"],delete_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"],kern_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"],recent1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"],lines1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"],cursor_pos1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"],cursor_data1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"],letters_already_written=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                        # for j in range(temp_count,count1):
                        #     del SW_global.axes_data[str(j)]
                    elif(temp_count<count1):
                        guideline_axes[l].set_visible(False)
                        for j in range(temp_count,count1):
                            (SW_global.axes_data[str(j)]["axis_data"]).set_visible(False)
                            del SW_global.axes_data[str(j)]
                        guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                        set_guideLine_variables(kern_value_array1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"],delete_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"],kern_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"],recent1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"],lines1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"],cursor_pos1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"],cursor_data1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"],letters_already_written=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                    SW_global.current_axes=guideline_axes[l]
                    if(pos1>=len(delete_list)):
                        SW_global.current_pos=len(delete_list)-1
                    else:
                        SW_global.current_pos=SW_global.cursor_pos[pos1]



                else:
                    for j in range(len(SW_global.axes_data)):
                        if(start_axes==SW_global.axes_data[str(j)]["axis_data"]):
                            key1=j
                        elif(end_axes==SW_global.axes_data[str(j)]["axis_data"]):
                            key2=j
                    if((key1!=None) and (key2!=None)):
                        if(key1<key2):
                            for j in range(pos1):#,len(SW_global.axes_data[str(key1)]["delete_list"])):
                                temp_delete_list.append((SW_global.axes_data[str(key1)]["delete_list"])[j])
                            clear_digit_from_axes(axesdata=SW_global.axes_data[str(key1)]["axis_data"])
                            for j in range(pos2+1,len(SW_global.axes_data[str(key2)]["delete_list"])):
                                temp_delete_list.append((SW_global.axes_data[str(key2)]["delete_list"])[j])
                            clear_digit_from_axes(axesdata=SW_global.axes_data[str(key2)]["axis_data"])
                            for j in range(len(SW_global.axes_data)):
                                if(j>key2):
                                    temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                                    clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                            clear_digit_from_axes(axesdata=guideline_axes[l])
                            temp_delete_list.extend(delete_list)
                        elif(key1>key2):
                            for j in range(pos2):#,len(SW_global.axes_data[str(key2)]["delete_list"])):
                                temp_delete_list.append(SW_global.axes_data[str(key2)]["delete_list"])
                            for j in range(pos1+1,len(SW_global.axes_data[str(key1)]["delete_list"])):
                                temp_delete_list.append(SW_global.axes_data[str(key1)]["delete_list"])
                            clear_digit_from_axes(axesdata=SW_global.axes_data[str(key1)]["axis_data"])
                            for j in range(len(SW_global.axes_data)):
                                if(key2>j):
                                    temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                                    clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                            clear_digit_from_axes(axesdata=guideline_axes[l])
                            temp_delete_list.extend(delete_list)
                        temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                        start_axes=None
                        if(key1>key2):
                            start_axes=key2
                        elif(key2>key1):
                            start_axes=key1
                        temp_count=start_axes
                        count1=len(SW_global.axes_data)
                        for j in range(len(temp)):
                            if(temp_count<count1):
                                base_array=[]
                                for k1 in range(4):
                                    base_array.append((SW_global.axes_data[str(temp_count)]["lines"])[k1])
                                temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                                save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=temp_count,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(temp_count)]["axis_data"],lines1=temp_guideline_axes2,kern_list1=temp_kern_list)
                            elif(temp_count==count1):
                                base_array=[]
                                for k1 in range(4):
                                    base_array.append(guideline_axes[l].lines[k1])
                                temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                                set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=temp_kern_list,recent1=temp_recent,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                            temp_count=temp_count+1
                            

                        # for j in range(len(temp)):
                        #     if(temp_count<=count1-1):
                        #         print("check point cut11")
                        #         base_array=[]
                        #         for k1 in range(4):
                        #             base_array.append((SW_global.axes_data[str(temp_count)]["lines"])[k1])
                        #         temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                        #         # save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=temp_count,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(temp_count)]["axis_data"],lines1=temp_guideline_axes2,kern_list1=temp_kern_list)
                        #     elif(temp_count==count1):
                        #         print("check point cut22")
                        #         base_array=[]
                        #         for k1 in range(4):
                        #             base_array.append(guideline_axes[l].lines[k1])
                        #         temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                        #         set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=temp_kern_list,recent1=temp_recent,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                        #     temp_count=temp_count+1
                        if(temp_count==count1):
                            guideline_axes[l].set_visible(False)
                            guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                            set_guideLine_variables(kern_value_array1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"],delete_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"],kern_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"],recent1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"],lines1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"],cursor_pos1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"],cursor_data1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"],letters_already_written=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                            # for j in range(temp_count,count1):
                            #     del SW_global.axes_data[str(j)]
                        elif(temp_count<count1):
                            guideline_axes[l].set_visible(False)
                            for j in range(temp_count,count1):
                                (SW_global.axes_data[str(j)]["axis_data"]).set_visible(False)
                                del SW_global.axes_data[str(j)]
                            guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                            set_guideLine_variables(kern_value_array1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"],delete_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"],kern_list1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"],recent1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"],lines1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"],cursor_pos1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"],cursor_data1=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"],letters_already_written=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                        SW_global.current_axes=guideline_axes[l]
                        if(pos1>=len(delete_list)):
                            SW_global.current_pos=len(delete_list)-1
                        else:
                            SW_global.current_pos=SW_global.cursor_pos[pos1]    
                            
                # if(start_axes==guideline_axes[l]):
                #     for j in range(pos1+1):
                #         temp_delete_list.append(delete_list[j])
                #     clear_digit_from_axes(axesdata=guideline_axes[l])
                #     key=None
                #     for j in range(len(SW_global.axes_data)):
                #         if(end_axes==SW_global.axes_data[str(j)]["axis_data"]):
                #             key=j
                #             for k1 in range(pos2,len(SW_global.axes_data[str(j)]["delete_list"])):
                #                 temp_delete_list.append((SW_global.axes_data[str(j)]["delete_list"])[k1])
                #                 clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                #         elif((key!=None) and(key>j)):
                #             temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                #             clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                #     temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                #     count1=len(SW_global.axes_data)-1
                #     temp_key=key

                #     for j in range(len(temp)):
                #         if(temp_key<=count1):
                #             base_array=[]
                #             for k1 in range(4):
                #                 base_array.append(SW_global.axes_data[str(temp_key)]["lines"][k1])
                #             temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                #         elif(temp_key==count1+1):
                #             base_array=[]
                #             for k1 in range(4):
                #                 base_array.append(guideline_axes[l].lines[k1])
                #             temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                # elif(end_axes==guideline_axes[l]):
                #     key=None
                #     for j in range(len(SW_global.axes_data)):
                #         if(start_axes==SW_global.axes_data[str(j)]["axis_data"]):
                #             key=j
                #             for k1 in range(pos1,len(SW_global.axes_data[str(j)]["delete_list"])):
                #                 temp_delete_list.append(SW_global.axes_data[str(j)]["delete_list"][k1])
                #         elif((key!=None) and (key>j)):
                #             temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                #     for j in range(pos2+1):
                #         temp_delete_list.append(guideline_axes[l].lines[j])
                #     divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                #     count1=len(SW_global.axes_data)-1
                #     temp_key=key

                #     for j in range(len(temp)):
                #         if(temp_key<=count1):
                #             base_array=[]
                #             for k1 in range(4):
                #                 base_array.append(SW_global.axes_data[str(temp_key)]["lines"][k1])
                #             temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                #         elif(temp_key==count1+1):
                #             base_array=[]
                #             for k1 in range(4):
                #                 base_array.append(guideline_axes[l].lines[k1])
                #             temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)                    
                #     print()
                # else:
                #     temp_delete_list=[]
                #     print()
                #     key1=None
                #     key2=None
                #     for j in range(len(SW_global.axes_data)):
                #         if(start_axes==SW_global.axes_data[str(j)]["axis_data"]):
                #             key1=j
                #             for k1 in range(pos1,len(SW_global.axes_data[str(j)]["delete_list"])):
                #                 temp_delete_list.append(SW_global.axes_data[str(j)]["delete_list"][k1])
                #         elif(end_axes==SW_global.axes_data[str(j)]["axis_data"]):
                #             key2=j

                #         elif((key1!=None) and(key1>j)and(key2==None)):
                #             temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                #         elif((key1!=None) and(key1>j) and(key2!=None) and(key2>j)):
                #             temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
    if(SW_global.connectdot_on_off==1):
        print("This is check point 2")
        call_connect_dot_for_multipleGuideLine()
        connect_dot_flag_pos=0
        connectdot_already_applied_array.clear()
        connect_dot()
    if(SW_global.decisiondot_on_off==1):
        print("This is check point 3")
        decision_dot_flag_pos=0
        call_decision_dot_for_mul()
        Decision_dot()
    if(SW_global.startdot_on_off==1):
        print("I am in check point 4")
        startdot_flag_pos=0
        call_start_dot_multiple_guideline()
        start_dot()
    if(SW_global.stokearrow_on_off==1):
        print("I am in check point5")
        stoke_arrow_flag_pos=0
        call_composit_dot_multipleGuideline()
        composite_dot()
    #connect_dot()
    fig.canvas.draw()
    #call_connect_dot_for_multipleGuideLine()
    #connect_dot()

    return




#global click_cursor


def onrelease(event):
    print("I am from onrelease Please check ")
    print("I am onrelease"*20)
    print("SW_global.cursor_data",SW_global.cursor_data)
    print("SW_global.cursor_pos",SW_global.cursor_pos)
    print("SW_global.letters_already_written",SW_global.letters_already_written)
    print("guideline_axes[l].lines",guideline_axes[l].lines)
    print("SW_global.axes_data",SW_global.axes_data)
    print("*"*200)
    global pos1i
    global pos2i
    SW_global.temp_axes=event.inaxes
    #if(SW_global.click_x==SW_global.release_x):
    SW_global.pos1_global=None
    SW_global.pos2_global=None
    SW_global.start_axes_global=None
    SW_global.end_axes_global=None
    SW_global.start_axes_global_temp=None
    SW_global.end_axes_global_temp=None


    ##########################################################
    ##### checking for axes #####
    if(guideline_axes[l]==event.inaxes):
        print("Yes1")
    else:
        for j in range(len(SW_global.axes_data)):
            if(event.inaxes==SW_global.axes_data[str(j)]["axis_data"]):
                print("yes2")
            else:
                print("No1")

    list234=[]
    #(event.inaxes).set_visible(False)
    if(len(SW_global.axes_data)>0):
        for j in range(len(SW_global.axes_data)):
            list234.append(SW_global.axes_data[str(j)]["axis_data"])
        #list234.append(SW_global.axes_data[str(j)]["axis_data"] for j in range(len(SW_global.axes_data)))
    print("This is list234",list234)
    if((guideline_axes[l]==event.inaxes) or(event.inaxes in list234)):
        print("ok")
#        if(len(SW_global.axes_data)>0):
#            (SW_global.axes_data[str(0)]["axis_data"]).set_visible(False)
    elif(event.inaxes in list234):
        print("ok6")
    else:
        #(event.inaxes).set_visible(False)

        print("check ok333 due to testinfg point 111")
        flag=False
        if(len(SW_global.axes_data)>0):
            #(event.inaxes).set_visible(False)
            for j in range(len(SW_global.axes_data)):
                if(event.inaxes==SW_global.axes_data[str(j)]["axis_data"]):
                    break
                elif(j==len(SW_global.axes_data)-1):
                    axes_list_for_box=[]
                    for k11 in range(len(SW_global.axes_data)):
                        axes_list_for_box.append(SW_global.axes_data[str(k11)]["axis_data"])
                    axes_list_for_box.append(guideline_axes[l])
                    if(len(SW_global.box_data)>0):
                        data_checking_for_need_to_create_or_update_back_page(axes_list=axes_list_for_box,delete_list1=delete_list,kern_value_array1=kern_value_array)
                    else:
                        create_new_page_on_box_data(delete_list1=delete_list,kern_value_array1=kern_value_array)
            print("This is end of 1")


        else:
            #(event.inaxes).set_visible(False)
            print("This is start 1")
            SW_global.current_axes=event.inaxes
            axes_list_for_box=[]
            for j in range(len(SW_global.axes_data)):
                axes_list_for_box.append(SW_global.axes_data[str(j)]["axis_data"])
            axes_list_for_box.append(guideline_axes[l])
            if(len(SW_global.box_data)>0):
                data_checking_for_need_to_create_or_update_back_page(axes_list=axes_list_for_box,delete_list1=delete_list,kern_value_array1=kern_value_array)
            else:
                create_new_page_on_box_data(delete_list1=delete_list,kern_value_array1=kern_value_array)
            print("This is end1")
        temp_key=checking_for_which_box_need_to_switch(axesdata=event.inaxes)
        temp=data_Switching2(key=temp_key)

        if(temp!=None):
            delete_list.clear()
            kern_value_array.clear()
            #print("temp len:",len(temp_data))
            if(len(temp)==7):
                for j in temp[1]:
                    #print("I am in kern_ temp_1")
                    kern_value_array.append(j)
                for j in temp[0]:
                    #print("I am in kern_temp_1")
                    delete_list.append(j)


    print("*"*100)
    if(SW_global.mainselector_value!=None):
        print()
        SW_global.mainselector_value.set_visible(False)
        #mainselector.set_visible(False)
    else:
        print("ok check one")
    if(SW_global.back_axes!=None):
        print("I am in back_axes")
        if((len(SW_global.axes_data)>0) and (SW_global.axes_data[str(0)]["axis_data"] in SW_global.text_flow_axes)):
            SW_global.left=((SW_global.back_axes).get_position()).x0
            SW_global.right=((SW_global.back_axes).get_position()).x1
            SW_global.top=((SW_global.back_axes).get_position()).y0
            SW_global.bottom=((SW_global.back_axes).get_position()).y1

            reset_main_selector1()
            #mainselector.extents(SW_global.left,SW_global.right,SW_global.top,SW_global.bottom)
        elif(guideline_axes[l] in SW_global.text_flow_axes):
            SW_global.left=((SW_global.back_axes).get_position()).x0
            SW_global.right=((SW_global.back_axes).get_position()).x1
            SW_global.top=((SW_global.back_axes).get_position()).y0
            SW_global.bottom=((SW_global.back_axes).get_position()).y1
            reset_main_selector1()
        else:
            SW_global.left=((SW_global.back_axes).get_position()).x0
            SW_global.right=((SW_global.back_axes).get_position()).x1
            SW_global.top=((SW_global.back_axes).get_position()).y0
            SW_global.bottom=((SW_global.back_axes).get_position()).y1

        mainselector.extents=(SW_global.left,SW_global.right,SW_global.top,SW_global.bottom)
        mainselector.set_visible(True)
        fig.canvas.draw()

        









    print("SW_global.axes_data",SW_global.axes_data)
    print("Print SW_global.cursor",SW_global.cursor_data)
    print("SW_global.cursor_pos",SW_global.cursor_pos)
    print("SW_global.kern_list",SW_global.kern_list)
    print("SW_global.letter_already_written",SW_global.letters_already_written)  
    print("This is delete_list:",delete_list)
    print("This is kern_value_array")  
    print("*"*100)
    print("This is data for :",SW_global.current_axes)
    # for j in range(len(SW_global.axes_data)):
    #     (SW_global.axes_data[str(j)]["axis_data"]).set_visible(False)
    #     fig.canvas.draw()
    #     (SW_global.axes_data[str(j)]["axis_data"]).set_visible(True)
    #     fig.canvas.draw()
    # guideline_axes[l].set_visible(False)
    # fig.canvas.draw()
    # guideline_axes[l].set_visible(True)
    # fig.canvas.draw()






    ##########################################################
    try:
      #  print("I am in click cursor false ")
        #click_cursor.set_visible(False)
        for i in range(len(SW_global.axes_data)):
            for k in SW_global.axes_data[str(i)]["cursor_data"]:
                k.set_visible(False)

        #click_cursor.set_visible(True)
    except Exception as e:
        pass
    if(guideline_axes[l]!=event.inaxes):
        for i in range(len(SW_global.axes_data)):
            if(event.inaxes==SW_global.axes_data[str(i)]["axis_data"]):
                SW_global.release_axes=SW_global.axes_data[str(i)]["axis_data"]
                break
    else:
        SW_global.release_axes=guideline_axes[l]
    global pos11_start
    global pos22_end
    checkFlag=0

    try:

        if(SW_global.single_click_data!=None):
            SW_global.single_click_data.set_visible(False)
    except Exception as e:
        print(e)
        pass

    try:
        #print("I am on set invisible_item")
        item=SW_global.temp_cursor_temp_data[0]
        item.set_visible(False)
        #print(SW_global.temp_cursor_temp_data)
    except Exception as e:
        pass
    try:
        for i in SW_global.cursor_data:
            i.set_visible(False)
    except Exception as e:
        print(e)
        pass
    SW_global.release_x=event.xdata
    SW_global.release_y=event.ydata
    start_point=-999
    end_point=-999
    start_axes=None
    end_axes=None
    if(SW_global.click_x>SW_global.release_x):
        start_point=SW_global.release_x
        end_point=SW_global.click_x
        start_axes=SW_global.release_axes
        end_axes=SW_global.click_axes
    else:
        start_point=SW_global.click_x
        end_point=SW_global.release_x
        start_axes=SW_global.click_axes
        end_axes=SW_global.release_axes

    print("This is start axes",start_axes)
    starting_x=-999
    ending_x=-999
    pos1=-1
    pos2=-1
    cur_temp_start=-999
    cur_temp_end=-999
    pos1,cur_temp_start=findPos1(axesdata=start_axes,start_point=start_point)
    #print("This is after pos1")
    print("this is pos1",pos1)
    SW_global.p1=pos1

    reversed_cursor_pos=[ele for ele in reversed(SW_global.cursor_pos)]
    #print(reversed_cursor_pos)
    ###### CHANGE of cursor #######
    # for i in range(len(reversed_cursor_pos)):
    #     if(end_point>=reversed_cursor_pos[i]):
    #         print("This is onrelease")
    #         print(i)
    #         pos2=i-1
    #         pos2=len(reversed_cursor_pos)-pos2-1-1
    #         cur_temp_end=pos2-1-1
    #         print(pos2)
    #         break
    # print(end_point,end_axes)

    pos2,cur_temp_end=findPos2(axesdata=end_axes,end_point=end_point)

    SW_global.p2=pos2

    print("this is pos2",pos2)

    #print("This is cur temp start",cur_temp_start)
    #print("This is cur temp end",cur_temp_end)
    #print(pos1)
    #print(pos2)

    if((pos1==10000)):
        if(cur_temp_start==1000):
            print("SW_global.cursor_data",SW_global.cursor_data)
            if(len(SW_global.cursor_data)>0):
                SW_global.single_click_data=SW_global.cursor_data[len(SW_global.cursor_data)-1]
            SW_global.current_axes=guideline_axes[l]
            SW_global.current_pos=SW_global.cursor_pos[-1]
            print("this is point2")
            SW_global.current_pos_in_number=len(SW_global.cursor_pos)
            try:
                (SW_global.cursor_data[-1]).set_visible(True)
            except Exception as e:
                print(e)
                pass
            print("I am in return Statement")
            pos1i=pos1
            pos2i=pos2
            fig.canvas.draw()
            return
        else:
            SW_global.single_click_data=(SW_global.axes_data[str(cur_temp_start)]["cursor_pos"])[-1]
            ((SW_global.axes_data[str(cur_temp_start)]["cursor_data"])[-1]).set_visible(True)
            SW_global.current_pos=(SW_global.axes_data[str(cur_temp_start)]["cursor_pos"])[-1]
            SW_global.current_axes=SW_global.axes_data[str(cur_temp_start)]["axis_data"]
            SW_global.current_pos_in_number=(len(SW_global.axes_data[str(cur_temp_start)]["cursor_pos"]))-1
            print("I am in return Statement1")
            pos1i=pos1
            pos2i=pos2
            fig.canvas.draw()
            return

        print("This is check point 17")
        print(pos2)
        print(pos1i)
        print(pos1)
        print(SW_global.current_pos)
        print(SW_global.current_axes)


    #print("This is pos2")
    #print(pos2)




    if(pos1==-1):
        pos1=0
    if(pos2==-1):
        pos2=0
    else:
        if(pos1==pos2):
            pass
        else:
            pos2=pos2-1

    #if(len(delete_list)-1<pos2):
     #   pos2=len(delete_list)-1
    temp_click_axes=-999
    temp_release_axes=-999
    for k in range(len(SW_global.axes_data)):
        if(start_axes==SW_global.axes_data[str(k)]["axis_data"]):
            temp_click_axes=k
        if(end_axes==SW_global.axes_data[str(k)]["axis_data"]):
            temp_release_axes=k
    if(guideline_axes[l]==end_axes):
        temp_release_axes=1000
    if(guideline_axes[l]==start_axes):
        temp_click_axes=1000

#    global pos1i
 #   global pos2i
    pos1i=pos1 ## Major variable for paste
    pos2i=pos2 ## Major variable for paste
    Starting_loop_point=pos1*2
    end_loop_point=pos2*2+1

    pos11_start=Starting_loop_point
    pos22_end=end_loop_point
    try:
        #print("This is new Try for color letter")
        if(color_letter_features_on_off):
            checkFlag=1
        else:
            checkFlag=0
    except Exception as e:
       # print(e)
        pass

    if(checkFlag==0):
    #   print("This is for check point colorwrite")
        for i in range(len(SW_global.g_val.lines)):
            if(i>3):
                SW_global.g_val.lines[i].set_color("black")
        for j in range(len(SW_global.axes_data)):
            for k in range(len(SW_global.axes_data[str(j)]["lines"])):
                if(k>3):
                    ((SW_global.axes_data[str(j)]["lines"])[k]).set_color("black")
        ##### To change color for selection with mouse #########
        if(SW_global.click_axes==SW_global.release_axes):
            try:
                if(SW_global.click_axes==guideline_axes[l]):
                    count_for_select=0
                    print("This is pos1:",pos1)
                    print("This is pos2:",pos2)
                    print(SW_global.letters_already_written)

                    for i in range(SW_global.letters_already_written[pos1*2],SW_global.letters_already_written[pos2*2+1]):
                        (guideline_axes[l].lines[i]).set_color("red")
                else:
                    for j in range(len(SW_global.axes_data)):
                        if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.click_axes):
                            for k in range((SW_global.axes_data[str(j)]["letters_already_written"])[pos1*2],(SW_global.axes_data[str(j)]["letters_already_written"])[(pos2*2)+1]):
                                ((SW_global.axes_data[str(j)]["lines"])[k]).set_color("red")
            except Exception as e:
                print(e)
                pass

        else:
            global start_of_select_temp
            global end_of_select_temp
            start_of_select=-999
            end_of_select=-999
            for k in range(len(SW_global.axes_data)):
                if(start_axes==SW_global.axes_data[str(k)]["axis_data"]):
                    start_of_select=k
                if(end_axes==SW_global.axes_data[str(k)]["axis_data"]):
                    end_of_select=k

            if(SW_global.click_axes==guideline_axes[l]):
                start_of_select=str(1000)
            if(SW_global.release_axes==guideline_axes[l]):
                end_of_select=str(1000)


            ############# Select condition for mouse event   ##############

            if(start_of_select==str(1000)):
                print("check point echo 666666**********************************************************************")
                if(end_of_select!=-999):
                    for h in range(SW_global.letters_already_written[0],SW_global.letters_already_written[pos1*2]):
                        (guideline_axes[l].lines[h]).set_color("red")
                    #if(h<=pos1*2):
                     #   ((guideline_axes[l].lines)[SW_global.letters_already_written[h]]).set_color("red")
                    for i in range(len(SW_global.axes_data)):
                        if(i==end_of_select):
                            print("check point echo 7777777**************************************************")
                            for h in range((SW_global.axes_data[str(i)]["letters_already_written"])[pos2*2+1],(SW_global.axes_data[str(i)]["letters_already_written"])[-1]):
                                ((SW_global.axes_data[str(i)]["lines"])[h]).set_color("red")
                        if(i>end_of_select):
                            print("check point echo 1010101010**********************************************")
                            print(end_of_select)
                            print("check echo1111122222")
                            print("check point echo 8888888*************************************************")
                            for h in range((SW_global.axes_data[str(i)]["letters_already_written"])[0],(SW_global.axes_data[str(i)]["letters_already_written"])[-1]):
                                ((SW_global.axes_data[str(i)]["lines"])[h]).set_color("red")
                else:
                    print("This is ok111111111111111111111111111111")
                    for i in range(len(SW_global.axes_data)):
                        if(SW_global.release_axes==SW_global.axes_data[str(i)]["axis_data"]):
                            end_of_select=i

                    print("check point 783939393")

                    print(pos2*2+1)
                    print(SW_global.letters_already_written[(pos2*2)])

                    print(SW_global.letters_already_written)

                    for i in range(len(guideline_axes[l].lines)):
                        if((i>3) and (i<SW_global.letters_already_written[pos2*2+1])):
                            (guideline_axes[l].lines[i]).set_color("red")




                    for i in range((SW_global.axes_data[str(end_of_select)]["letters_already_written"])[pos1*2],(SW_global.axes_data[str(end_of_select)]["letters_already_written"])[-1]):
                        ((SW_global.axes_data[str(end_of_select)]["lines"])[i]).set_color("red")


                    for i in range(len(SW_global.axes_data)):
                        if(i>end_of_select):
                            for k in range((SW_global.axes_data[str(i)]["letters_already_written"])[0],((SW_global.axes_data[str(i)]["letters_already_written"])[-1])):
                                ((SW_global.axes_data[str(i)]["lines"])[k]).set_color("red")



            else:
                if(end_of_select==str(1000)):
                    print("check point beta ***********************************************")
                    for h in range(SW_global.letters_already_written[0],SW_global.letters_already_written[(pos2*2)+1]):
                        (guideline_axes[l].lines[h]).set_color("red")
                    for i in range(len(SW_global.axes_data)):
                        if(start_of_select==i):
                            for h in range((SW_global.axes_data[str(i)]["letters_already_written"])[pos1*2],(SW_global.axes_data[str(i)]["letters_already_written"])[-1]):
                                ((SW_global.axes_data[str(i)]["lines"])[h]).set_color("red")
                        if(start_of_select<i):

                            count_for_select=0
                            for h in range((SW_global.axes_data[str(i)]["letters_already_written"])[0],(SW_global.axes_data[str(i)]["letters_already_written"])[-1]):
                                ((SW_global.axes_data[str(i)]["lines"])[h]).set_color("red")
                else:
                    print("check point alpha ****************************************************")
                    if(start_of_select>end_of_select):
                        for i in range(len(SW_global.axes_data)):
                            if(i==start_of_select):
                                for j in range((SW_global.axes_data[str(i)]["letters_already_written"])[0],(SW_global.axes_data[str(i)]["letters_already_written"])[(pos1*2)]):
                                    (SW_global.axes_data[str(i)]["lines"]).set_color("red")

                            if(i==end_of_select):
                                for j in range((SW_global.axes_data[str(i)]["letters_already_written"])[(pos2*2)+1],(SW_global.axes_data[str(i)]["letters_already_written"])[-1]):
                                    (SW_global.axes_data[str(i)]["lines"]).set_color("red")
                            ######## have change here , need to test ########
                            if((i<start_of_select) and (i>end_of_select)):
                                for j in range((SW_global.axes_data[str(i)]["lines"])[0],(SW_global.axes_data[str(i)]["lines"])[-1]):
                                    ((SW_global.axes_data[str(i)]["lines"])[j]).set_color("red")
                    else:
                        if(start_of_select<end_of_select):
                           # print("This is eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                            for i in range(len(SW_global.axes_data)):
                                if(i==start_of_select):
                                    for j in range((SW_global.axes_data[str(i)]["letters_already_written"])[pos1*2],(SW_global.axes_data[str(i)]["letters_already_written"])[-1]):
                                        ((SW_global.axes_data[str(i)]["lines"])[j]).set_color("red")
                                if(i==end_of_select):
                                    for j in range((SW_global.axes_data[str(i)]["letters_already_written"])[0],(SW_global.axes_data[str(i)]["letters_already_written"])[(pos2*2)+1]):
                                        ((SW_global.axes_data[str(i)]["lines"])[j]).set_color("red")

                                if((i>start_of_select) and (i<end_of_select)):
                                    print("I am in check point3")
                                    for j in range((SW_global.axes_data[str(i)]["letters_already_written"])[0],(SW_global.axes_data[str(i)]["letters_already_written"])[-1]):
                                        ((SW_global.axes_data[str(i)]["lines"])[j]).set_color("red")

                #fig.canvas.draw()


            #################### Condition where both of axes is not in current guideline axes(guideline_axes[l]) ##############





    #fig.canvas.draw()
    if(temp_release_axes==1000):
        if(len(delete_list)-1<pos2):
            pos2=len(delete_list)-1
    else:
        if(len(SW_global.axes_data[str(temp_release_axes)]["delete_list"])<pos2):
            print(SW_global.axes_data[str(temp_release_axes)]["delete_list"],pos2)
            pos2=len(SW_global.axes_data[str(temp_release_axes)]["delete_list"])-1
    ####################################################################################### part where letter is selected #########
    #print("This is mullyfi part")
    SW_global.copy_string=""
    #print("This is attachment start")
    ##################  function for string selection ###############
    print("check point select_string_for_copy_paste")
   # print(select_string_for_copy_paste(pos1=pos1,start_axes=start_axes,start_axes_key=temp_click_axes,pos2=pos2,end_axes=end_axes,end_axes_key=temp_release_axes))
    print("check point select string for copy paste ")
    #if((pos1!=None) and (start_axes!=None) and())
    SW_global.pos1_global=pos1
    SW_global.pos2_global=pos2
    SW_global.start_axes_global=start_axes
    SW_global.end_axes_global=end_axes
    SW_global.start_axes_global_temp=temp_click_axes
    SW_global.end_axes_global_temp=temp_release_axes
    SW_global.copy_string=select_string_for_copy_paste(pos1=pos1,start_axes=start_axes,start_axes_key=temp_click_axes,pos2=pos2,end_axes=end_axes,end_axes_key=temp_release_axes)
    print(SW_global.copy_string)
    ### This is for global axes data selection
    ###for i in range(pos1,pos2+1):
       ### SW_global.copy_string=SW_global.copy_string+str(delete_list[i])
    ###
    #print("This is will be copy string")
    #print(SW_global.copy_string)
    #print("This is attachment end")
    #print("This is for algorith checking pos1 and pos2 *******************************************************")
    #print(pos1)
    #print(pos2)
    if(SW_global.click_x==SW_global.release_x):
        #### Change color black for entire multiple guide line #####
        if(checkFlag==0):
            print("check point 56")
            #for i in (guideline_axes[l].lines):
             #   print(i.get_color())

            for i in range(len(guideline_axes[l].lines)):
                if(i>3):
                    item=guideline_axes[l].lines[i]
                    print(item.get_color())
                    if(item.get_color()!='#0000ff'):
                        item.set_color('black')

            for j in range(len(decisiondot_already_applied_array)):
                print("I am in loop")
                if(j+1<len(decisiondot_already_applied_array)):
                    k1=decisiondot_already_applied_array[j]
                    k2=decisiondot_already_applied_array[j+1]
                    for k22 in range(k1,k2):
                        guideline_axes[l].lines[k22].set_color("#0000ff")

            print(startdot_already_applied_array)
            print(len(guideline_axes[l].lines))

            for j in range(len(startdot_already_applied_array)-1):
                print(startdot_already_applied_array[j])
                (guideline_axes[l].lines[startdot_already_applied_array[j]]).set_color('red')



            for i in range(len(SW_global.axes_data)):
                for k in range(len(SW_global.axes_data[str(i)]["lines"])):
                    if(k>=4):
                        if(((SW_global.axes_data[str(i)]["lines"])[k]).get_color()!='blue'):
                            ((SW_global.axes_data[str(i)]["lines"])[k]).set_color("black")

                for j in range(len(SW_global.axes_data[str(i)]["startdot_already_applied_array"])-1):
                    (SW_global.axes_data[str(i)]["lines"])[SW_global.axes_data[str(i)]["startdot_already_applied_array"][j]].set_color('red')
                #for j in range(len(SW_global.axes_data[i]))
                for j in range(len(SW_global.axes_data[str(i)]["decisiondot_already_applied_array"])):
                    if(j+1<len(SW_global.axes_data[str(i)]["decisiondot_already_applied_array"])):
                        k1=SW_global.axes_data[str(i)]["decisiondot_already_applied_array"][j]
                        k2=SW_global.axes_data[str(i)]["decisiondot_already_applied_array"][j+1]
                        print(k1)
                        print(k2)
                        for j1 in range(k1,k2):
                            ((SW_global.axes_data[str(i)]["lines"])[j1]).set_color('#0000ff')


            #k=0
            #while(k+1<=len(SW_global.axes_data[])-1):



        #if(SW_global.click_x>0):
         #   if(pos1!=pos2):
          #      pos1=len(delete_list)-1
           #     pos2=len(delete_list)-1
        for de in SW_global.cursor_data:
            de.set_visible(False)

        ########      SWglobal single cursor      for multiple guide line#####
        if((end_axes==guideline_axes[l]) and (start_axes==guideline_axes[l])):
            print("check point 57")
            invisible_item=SW_global.cursor_data[len(SW_global.cursor_data)-1]
            invisible_item.set_visible(False)
            visible_item=SW_global.cursor_data[pos1]
            single_click_cursor_pos=SW_global.cursor_pos[pos1+1]
            cursor_y=list(np.linspace(-900,1500,500))
            SW_global.single_click_pos=SW_global.cursor_pos[pos1+1]
            cursor_x=list(np.full((500),SW_global.single_click_pos-manuscript.x_max[delete_list[pos1]]))
            ##### add new variable current_pos , current_axes   #####
            SW_global.current_pos=SW_global.cursor_pos[pos1+1]
            SW_global.current_axes=guideline_axes[l]
            SW_global.current_pos_in_number=pos1

            if(SW_global.release_x>=SW_global.cursor_pos[-1]):
                print("This is check pint 58")
                SW_global.single_click_data=SW_global.cursor_data[-1]
                ####### add new variable current_pos ,current_axes   ########
                SW_global.current_pos=SW_global.cursor_pos[-1]
                print("check 2344")
                SW_global.current_pos_in_number=len(SW_global.cursor_pos)-1
                SW_global.current_axes=guideline_axes[l]
                SW_global.single_click_data.set_visible(True)
            else:
                print("This is check point 59")
                plot_data=guideline_axes[l].plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                print("check 2555")
                SW_global.single_click_data=plot_data[0]
                ########## add new variable current_pos and current_axes  ##########
                SW_global.current_axes=guideline_axes[l]
                SW_global.current_pos=SW_global.cursor_pos[pos1+1]
                SW_global.current_pos_in_number=pos1
        else:


            for i in range(len(SW_global.axes_data)):
                print("check point 60")
                if((SW_global.axes_data[str(i)]["axis_data"])==end_axes):
                    print("check point 61")
                   # print("I am in axis data")
                    single_click_cursor_pos=(SW_global.axes_data[str(i)]["cursor_pos"])[pos1+1]
                   # print(single_click_cursor_pos)

                    kq1=(SW_global.axes_data[str(i)]["delete_list"])[pos1]
                    kq3=(single_click_cursor_pos)-manuscript.x_max[kq1]
                    print(SW_global.single_click_pos-manuscript.x_max[kq1])
                    print(manuscript.x_max[kq1])
                    print("check point 62")
                    cursor_y=list(np.linspace(-900,1500,500))
                    cursor_x=list(np.full((500),single_click_cursor_pos-manuscript.x_max[kq1]))
                    kq=SW_global.axes_data[str(i)]["axis_data"]
                    print(kq)
                    plot_data=kq.plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                    SW_global.single_click_data=plot_data[0]
                    SW_global.current_axes=kq
                    print("check point 63")
                    SW_global.current_pos=single_click_cursor_pos
                    SW_global.current_pos_in_number=pos1
            fig.canvas.draw()

        print("This is pos1 on single click")
        print("pos1:",pos1)
        print("pos2:",pos2)
        print("current_pos",SW_global.current_pos)
        print("axes_data",SW_global.current_axes)
        print("pos1i:",pos1i)
        print("check 2:",SW_global.current_pos_in_number)
        print("ok1")



        ######### SW_global.single cursor multiple guide line end ############
        try:
            fig.canvas.draw()
        except Exception as e:
            #print(e)
            pass

    else:

        if(pos1>pos2):
            start_ce=pos2
            end_ce=pos1
            start_ce_axes=end_axes
            end_ce_axes=start_axes
        else:
            start_ce=pos1-1
            end_ce=pos2
            start_ce_axes=start_axes
            end_ce_axes=end_axes


        #for j in range(len(SW_global.axes_data)):
         #   if(SW_global.ax)
        if(end_ce_axes==guideline_axes[l]):
            #print("This is check poin echo11")
            if(len(SW_global.cursor_data)>0):
                click_cursor=SW_global.cursor_data[end_ce]
                click_cursor.set_color("black")
                click_cursor.set_visible(True)

        else:
            #print("This is check point echo12")
            for j in range(len(SW_global.axes_data)):
                if(end_ce_axes==SW_global.axes_data[str(j)]["axis_data"]):
                    if(len(SW_global.axes_data[str(j)]["cursor_data"])>0):
                        click_cursor=""
                        click_cursor=(SW_global.axes_data[str(j)]["cursor_data"])[end_ce]
                        print(click_cursor)
                        click_cursor.set_color("black")
                        click_cursor.set_visible(True)
                        try:
                            fig.canvas.draw()
                        except Exception as e:
                            print(e)
                            pass
                        break





        if(start_ce_axes==guideline_axes[l]):
            #print("This is check point22")
            tempcu=SW_global.cursor_pos[start_ce+1]
            cursor_y=list(np.linspace(-900,1500,500))
            if(tempcu==0):
                q1=list(np.full(500,tempcu))
            else:
                q1=list(np.full(500,tempcu+300))
            cursor_x=q1
            try:
                SW_global.temp_cursor_temp_data=guideline_axes[l].plot(cursor_x,cursor_y,color='black',linewidth=0.6,dashes=(3,4))
                fig.canvas.draw()
            except Exception as e:
                pass
        else:
            #print("This is check point23")
            for j in range(len(SW_global.axes_data)):
                if((SW_global.axes_data[str(j)]["axis_data"])==start_ce_axes):
                    tempcu=(SW_global.axes_data[str(j)]["cursor_pos"])[start_ce+1]
                    cursor_y=list(np.linspace(-900,1500,500))
                    if(tempcu==0):
                        q1=list(np.full(500,tempcu))
                    else:
                        q1=list(np.full(500,tempcu+300))
                    cursor_x=q1
                    try:
             #           print("I am in check point 4")
                        SW_global.temp_cursor_temp_data=(SW_global.axes_data[str(j)]["axis_data"]).plot(cursor_x,cursor_y,color='black',linewidth=0.6,dashes=(3,4))
                        fig.canvas.draw()
                    except Exception as e:
              #          print(e)
                        pass


    return

def onclick2(event):
    print("This is onclick")
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    if(guideline_axes[l]!=event.inaxes):
        for i in range(len(SW_global.axes_data)):
            if(event.inaxes==SW_global.axes_data[str(i)]["axis_data"]):
     #           print("I got check point2222222222222222222222222222222222222222222222222222222222")
                SW_global.click_axes=SW_global.axes_data[str(i)]["axis_data"]
                break
    else:
        SW_global.click_axes=guideline_axes[l]
    if(not event.dblclick):
        SW_global.click_x=event.xdata
        SW_global.click_y=event.ydata
   # print("This is release coordinate")
        print(SW_global.click_x)
        print(SW_global.click_y)
    #print("This is click coordinate")
    #print()
    return




def minimize_wn():
    global sub
    if sub.overrideredirect(False):
        sub.overrideredirect(True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# ********************************************** Property-bar ******************************************************

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Grid features >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def gird_on():
    SW_global.gird_flag = True
    fig_axes.xaxis.set_major_locator(plt.MultipleLocator(0.2))
    fig_axes.xaxis.set_minor_locator(plt.MultipleLocator(0.04))
    fig_axes.yaxis.set_major_locator(plt.MultipleLocator(0.2))
    fig_axes.yaxis.set_minor_locator(plt.MultipleLocator(0.04))
    fig_axes.grid(which='major', axis='x', linewidth=0.45, linestyle='-', color='blue')
    fig_axes.grid(which='minor', axis='x', linewidth=0.10, linestyle='-', color='blue')
    fig_axes.grid(which='major', axis='y', linewidth=0.45, linestyle='-', color='blue')
    fig_axes.grid(which='minor', axis='y', linewidth=0.10, linestyle='-', color='blue')
##    fig_axes.axhline(y = SW_global.ht_gd_1, color='red')
    fig.canvas.draw()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def donothing():
    print("I am in do nothing")
    filewin = Toplevel(SW_Main_UI)
    button = Button(filewin, text="Do nothing button")
    button.pack()
    if(SW_global.text_flow_axes1==None):
        if(SW_global.text_flow_axes2==None):
            if(temp_axes!=None):
                SW_global.text_flow_axes1=temp_axes
        else:
            if(temp_axes!=SW_global.text_flow_axes2):
                SW_global.text_flow_axes1=temp_axes
            else:
                SW_global.text_flow_axes2=None
    else:
        if(SW_global.text_flow_axes2==None):
            if(temp_axes!=None):
                SW_global.text_flow_axes2=temp_axes
        else:
            if(SW_global.text_flow_axes1==temp_axes):
                SW_global.text_flow_axes1=None

    print(SW_global.text_flow_axes1)
    print(SW_global.text_flow_axes2)



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Main GUI <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
SW_Main_UI = Tk()

wd = SW_Main_UI.winfo_screenwidth()
ht = SW_Main_UI.winfo_screenheight()


SW_Main_UI.geometry(str(wd)+"x"+str(ht))

if "nt" == os.name:
    SW_Main_UI.state('zoomed')
    SW_Main_UI.wm_iconbitmap(bitmap = "icons/Startwrite.ico")
else:
    SW_Main_UI.iconphoto(True, PhotoImage(file=os.path.join("icons/Startwrite.png")))

SW_Main_UI.title("StartWrite")

SW_Main_UI.protocol("WM_DELETE_WINDOW", on_exit)

maintoolbarframe1 = Frame(SW_Main_UI, width = wd)
maintoolbarframe1.grid(row = 1, column = 0,sticky=E+W)
maintoolbarframe = Frame(maintoolbarframe1, bd=1, relief=RAISED)
maintoolbarframe.pack(side=TOP, fill=X)#, ipadx = wd/3.8)

propertybarframe1 = Frame(SW_Main_UI, width = wd)
propertybarframe1.grid(row = 2, column = 0,sticky=E+W)
propertybarframe = Frame(propertybarframe1, bd=1, relief=RAISED)
propertybarframe.pack(side=TOP, fill=X)#, ipadx = wd/4.8)

writingareaframe1 = Frame(SW_Main_UI, width=(wd-5), height=500)
writingareaframe2 = Frame(SW_Main_UI, width=(wd-5), height=500)

writingareaframe3 = Frame(SW_Main_UI, width=(wd-5), height=500)
writingareaframe4 = Frame(SW_Main_UI, width=(wd-5), height=500)
writingareaframe5 = Frame(SW_Main_UI, width=(wd-5), height=500)

for frame in (writingareaframe1, writingareaframe2, writingareaframe3, writingareaframe4, writingareaframe5):
    frame.grid(row = 3, column = 0,sticky=E+W)

writingareaframe = Frame(writingareaframe1, height=500, bd=1, relief=RAISED)
writingareaframe.pack(side=TOP, fill=X)
writingareaframe.tk_focusFollowsMouse()
endgridtoolframe1 = Frame(SW_Main_UI, width=wd, height=20, bd=1)
endgridtoolframe1.grid(row = 4, column = 0,sticky=E+W)
endgridtoolframe = Frame(endgridtoolframe1, height=20, bd=1, relief=RAISED)
endgridtoolframe.pack(side=TOP, fill=X)#, ipadx = wd/2.31)

###################################################################################################################
all_windows = dict() #MyStack.SW_Stack()
active_window=None

def newfile():
    sub = Toplevel(writingareaframe, bg = "gray")
    sub.wm_title("New Doc")
    sub.geometry("1360x580+0+130")
    sub.wm_transient(writingareaframe)

# ---------------------------------------------- PRESS EVENT ------------------------------------------------

def NewWindow(master):
    global all_windows
    restaurar_wn()
    # def on_exit(cur_window):
    #     print('exit', cur_window.winfo_id(), 'window')
    #     # all_windows.st_remove(cur_window)
    #     all_windows.pop(str(cur_window.winfo_id()))
    #     cur_window.destroy()
    #
    # def getactivewindow(event,arg):
    #     global active_window
    #     print(event.x,event.y)
    #     print(arg.winfo_id())
    #     print(active_window)
    #     active_window=arg
    #     print(active_window)
    #     # print(arg)

    # childWindow = tk.Toplevel(master=master)
    # childWindow.wm_transient(master)
    # childWindow.protocol('WM_DELETE_WINDOW', lambda: on_exit(childWindow))
    # label1 = tk.Label(childWindow, text=str("PP")).pack()
    # all_windows.update({str(childWindow.winfo_id()): childWindow})
    # chd = childWindow
    # childWindow.bind('<Button-1>', lambda event, arg=chd: getactivewindow(event, arg))
    # childWindow.title('child window {}'.format(childWindow.winfo_id()))
    # width, height = 500, 500
    # centre_x, centre_y = childWindow.winfo_screenwidth() / 2 - width / 2, childWindow.winfo_screenheight() / 2 - height / 2
    # childWindow.geometry('{}x{}+{}+{}'.format(width, height, int(centre_x), int(centre_y)))

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Show Pdf <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def ShowManualPdf():
    if platform.platform('darwin'):
        os.system("./StartWriteIndia_Mannual/manual_windows_v6_1511556025.pdf")
    elif platform.platform('linux'):
        subprocess.call(('xdg-open', "./StartWriteIndia_Mannual/manual_windows_v6_1511556025.pdf"))
    elif platform.platform('win32'):
        os.startfile("./StartWriteIndia_Mannual/manual_windows_v6_1511556025.pdf")

cpyrght_var = StringVar()

def aboutstartwrite():
    global lin_flag, user_id, user_mail, vaild_key, key_status
    if lin_flag:
        abt_sw = Toplevel(SW_Main_UI)
        abt_sw.geometry("750x510+150+80")
        abt_sw.title("Trail Version About")
        abt_sw.resizable(width=False, height=False)

        lbl_frm = Frame(abt_sw)
        lbl_frm.pack(side=LEFT, padx=10)

        img = tk.PhotoImage(file = "icons/sw60trial.png")
        img = img.zoom(4)
        img = img.subsample(14)
        lbl1 = Label(lbl_frm, image = img)
        lbl1.image = img
        lbl1.pack(side=LEFT)

        btn_frm = Frame(abt_sw)
        btn_frm.pack(side=RIGHT, padx=10)

        abt_ok = ttk.Button(btn_frm, text="OK", command=abt_sw.destroy, width=20)
        abt_ok.pack()
        lin_agrmnt = ttk.Button(btn_frm, text="Purchase Online", width=20, command=lin_purchase_wp)
        lin_agrmnt.pack()
        abt_ent_key = ttk.Button(btn_frm, text="Activate", width=20, command=valid_key_wp)
        abt_ent_key.pack()
        abt_sw.mainloop()
    else:
        abt_sw = Toplevel(SW_Main_UI)
        abt_sw.geometry("480x580+350+120")
        abt_sw.resizable(height=False, width=False)
        lbl1 = Label(abt_sw, textvariable=cpyrght_var, justify = CENTER)
        cpyrght_var.set("Startwrite™ and The Handwriting Worksheet Wizard™ \n are trademarks of Startwrite LLC.")
        lbl1.pack(side=TOP, ipady=20)

        cntus_var = "Contact us at www.StartwriteIndia.com or \n call +(91)-905-133-1646"
        lbl2 = Label(abt_sw, text = cntus_var , justify = CENTER)
        lbl2.pack(side=TOP, ipady=10)

        u_m = user_id + "(" + user_mail + ")"
        prglin_var = ("This Program Licensed to: "
                      +str(u_m)+" \n Activation Key: "
                      +vaild_key+" \n Any other unauthorized use is violation of the license agreement.")
        lbl3 = Label(abt_sw, text = prglin_var, justify = CENTER)
        lbl3.pack(side=TOP, ipady=10)
        img_var = tk.PhotoImage(file="icons/Startwritelogo.png")
        lblimg = Label(abt_sw, image = img_var, justify = CENTER, width=300, height=300)
        lblimg.image = img_var
        lblimg.pack(side=TOP)
        abt_ok = ttk.Button(abt_sw, text="OK", command=abt_sw.destroy)
        abt_ok.pack(side=TOP, padx=4)


def openfile():
    filewin_filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                  filetypes=(("Startwrite Files", "*.swd"), ("all files", "*.*")))

    data_access = pickle.load(open(filewin_filename,'rb'))
    plt.show()

def saveasfile():
    filewin_saveas = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                  filetypes=(("Startwrite Files", "*.swd"), ("all files", "*.*")))

    pickle.dump(fig.gca(), open(filewin_saveas+".swd", "wb"))

    plt.close("all")
#----------------------------------------------------------------------------------------------------------------#
def print_page():
    pass

def cut_page():
    pass

def copy_page():
    pass

def paste_page():
    pass

def sell_check():
    pass
#----------------------------------------------------------------------------------------------------------------#
# def delguideline():
#     print("I am working on del guideline_axes")
#     print(SW_global.current_axes)
#     #SW_global.text_flow_axes1.set_visible(False)
#     SW_global.text_flow_axes2.set_visible(False)
#     #fig.canvas.show()
#     if(len(SW_global.box_data)>0):
#         for j in range(len(SW_global.box_data)):
#             print(SW_global.box_data)
#             check_axes_list=SW_global.box_data[str(j)]["axes_list"]
#             if(SW_global.text_flow_axes1 in check_axes_list):
#                 print("need to write a function for data Switching")
#                 print(SW_global.box_data)
#                 print(delete_list)
#                 print(kern_value_array)
#                 data_Switching(key=j,kern_value_array=kern_value_array,delete_list=delete_list)
#                 for k in range(len(guideline_axes[l].lines)):
#                     if(k>3):
#                         (guideline_axes[l].lines[k]).set_visible(False)

#                 SW_global.cursor_pos.clear()
#                 SW_global.cursor_pos.insert(0,0)
#                 SW_global.cursor_data.clear()
#                 SW_global.kern_list.clear()
#                 SW_global.kern_list.insert(0,0)
#                 kern_value_array.clear()
#                 kern_value_array.insert(0,0)
#                 delete_list.clear()
#                 SW_global.recent_input_list.clear()
#                 SW_global.letters_already_written.clear()
#                 while(len(guideline_axes[l].lines)>3):
#                     del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
#                 SW_global.recent_input_list.clear()
#                 delete_list.clear()
#                 kern_value_array.clear()
#                 for k5 in SW_global.entire_delete_list_for_one_page:
#                     print(k5)

#                     try:
#                         if(SW_global.kern_list[0]>15500):

#                             print("i am in optimising stage")
#                             #print("This is swgloba gval",SW_global.g_val.lines)
#                             #print(kern_value_array)
#                             #print(SW_global.kern_list)
#                             #print(guideline_axes[0])
#                             #print(SW_global.letters_already_written)
#                             #print(delete_list)
#                             #print("full")
#                             a=dict()
#                             a["letters_already_written"]=[i for i in  SW_global.letters_already_written]
#                             a["kern_value_array"]=[i for i in kern_value_array]
#                             a["delete_list"]=[i for i in delete_list]
#                             a["kern_list"]=[i for i in SW_global.kern_list]
#                             a["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
#                             a["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
#                             a["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
#                             a["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
#                             a["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
#                             a["startdot_flag_pos"]=startdot_flag_pos
#                             a["decision_dot_flag_pos"]=decision_dot_flag_pos
#                             a["connect_dot_flag_pos"]=connect_dot_flag_pos
#                             a["axis_data"]=guideline_axes[l]
#                             print("This is guide line axes .lines",len(guideline_axes[l].lines))
#                             a["lines"]=[i for i in guideline_axes[l].lines]
#                             print("This is check point 3")
#                             a["gval"]=[i for i in SW_global.g_val.lines]
#                             a["cursor_pos"]=[i for i in SW_global.cursor_pos]
#                             a["cursor_data"]=[i for i in SW_global.cursor_data]
#                             print("This is cursor_data")
#                             print(a["cursor_data"])
#                             SW_global.cursor_pos.clear()
#                             SW_global.cursor_data.clear()
#                             SW_global.cursor_pos.insert(0,0)
#                             #print("This is decision dot flag")
#                             #print(decision_dot_flag_pos)
#                             #print("This is axes data")
#                             #print(len(SW_global.axes_data))
#                             SW_global.axes_data[str(len(SW_global.axes_data))]=a
#                             #print(SW_global.axes_data)
#                             #print(guideline_axes[l].lines)
#                             kern_value_array.clear()
#                             SW_global.kern_list.clear()
#                             SW_global.letters_already_written.clear()
#                             SW_global.letters_already_written.clear()
#                             SW_global.kern_list.insert(0,0)
#                             SW_global.kern_value_array.clear()
#                             SW_global.kern_value_array.insert(0,0)
#                             kern_value_array.clear()
#                             kern_value_array.insert(0,0)
#                             #print("This is check point 2")
#                             #print(guideline_axes[l].lines)
#                             compositedot_already_applied_array.clear()
#                             startdot_already_applied_array.clear()
#                             decisiondot_already_applied_array.clear()
#                             connectdot_already_applied_array.clear()
#                             stoke_arrow_flag_pos =0
#                             #print("This is len")
#                             #print(guideline_axes[l].lines)
#                             startdot_flag_pos=0
#                             decision_dot_flag_pos=0
#                             connect_dot_flag_pos=0
#                             delete_list.clear()
#                             #temp=[i for i in guideline_axes[l].lines]
#                             newCreateGuideLine(1,None,None,None,None)
#                             #print("This is after update ")


#                             for i in range(len(SW_global.axes_data)):
#                                 print("8888888888888888888888888888888888888888888888888888888888888888888")
#                                 print(SW_global.axes_data[str(i)])
#                                 print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#                                 #print(SW_global.axes_data[str(i)])
#                                 print("****************************************")
#                             # b=dict()
#                             # b["axes_data"]=guideline_axes[l]
#                             # b["lines"]=guideline_axes[l].lines
#                             # b["compositedot_already_applied_array"]=compositedot_already_applied_array
#                             # b["decisiondot_already_applied_array"]=decisiondot_already_applied_array
#                             # b["startdot_already_applied_array"]=startdot_already_applied_array
#                             # b["connectdot_already_applied_array"]=connectdot_already_applied_array
#                             # b["kern_value_array"]=kern_value_array
#                             # b["kern_list"]=kern_list
#                             # SW_global.recent_axes_with_respect_rectangle_selector[str("0")]=b
#                             ################################## checking for guideline_axes[l]
#                             print("This is guideLine axes_data","*"*60)
#                             print(guideline_axes)
#                             print("**"*60)
             
#                     except Exception as e:
#                         print(e)





#             ############################ End of multiple guide line ################################### 



#                     length12 = len(SW_global.recent_input_list)
#                     event_key=k5
#                     user_input = event_key
#                     x_max = manuscript.x_max[user_input]
#                     kern_x = SW_global.kern_list[0]

#                     if color_letter_features_on_off:
#                         c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
#                     else:
#                         c1, c2 = manuscript.return_manuscript_fonts(user_input)


#                     c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)

#                     kern_x = SW_global.kern_list[0] + x_max + 300
#                     #print("After update kern list")
#                     print("This is before kern_x update")
#                     SW_global.kern_list.insert(0, kern_x)
#                     print("This is after ken_x ")
#                     #print(SW_global.kern_list)
#                     #print("this is kern value array")
#                     #print(kern_value_array)
#                     kern_counter = len(kern_value_array)
#                     kern_value_array.insert(kern_counter, kern_x)
#                     #print(kern_value_array)
#                     SW_global.recent_input_list.insert(length12, event_key)
#                     #print("this is list")
#                     delete_list.insert(length12, event_key)
#                     #print(delete_list)
#                     init_enrty_pos = len(SW_global.letters_already_written)
#                     inti_letter_pos = len(guideline_axes[l].lines)
#                     #print("This is guide line axes length ")
#                     #print(len(guideline_axes[l].lines))
#                     SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
#                     #print(SW_global.letters_already_written)
#                     if draw_type_color_letter == 1:
#                         if letter_dot_density_no_dot_on_off == 1:
#                             alp = 0
#                         else:
#                             alp = temp_alp
#                         if color_letter_features_on_off:
#                             guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                         else:
#                             guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

#                     else:
#                         n = len(c1)
#                         if letter_dot_density_no_dot_on_off == 1:
#                             alp = 0
#                         else:
#                             alp = temp_alp
#                         if color_letter_features_on_off:
#                             for i in range(n):
#                                 if i == 0:
#                                     guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                                 if i == 1:
#                                     guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                                 if i == 2:
#                                     guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                                 if i == 3:
#                                     guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                         else:
#                             for i in range(n):
#                                 guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                     #############################   Cursor part code of inserting ###############################
#                     import numpy as np 
#                     if(len(SW_global.cursor_data)!=0):
#                         print("It is ok")
#                         print(delete_list)
#                         print(SW_global.letters_already_written)
#                        # print(cursor_data)
#                         #cursor_pos(cursor_pos)
#                     else:
#                         print("It is empty")
#                     item_cursor=kern_x-300
#                     cursor_y=list(np.linspace(-900,1500,500))
#                     #cursor_y_neg=list(np.lenspace)
#                     cursor_x=list(np.full((500),item_cursor))
#                     SW_global.cursor_pos.append(item_cursor)
#                     cursor_x1=list(np.full((500),item_cursor))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
#                     plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
#                     SW_global.single_click_data=plot_data[0]
#                     SW_global.single_click_data.set_visible(False)


#                     k=guideline_axes[l].plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
#                     #print(k)
#                     #print(k)
#                     k[0].set_visible(False)
#                     for i in k:
#                         SW_global.cursor_data.append(i)
#                         i.set_visible(False)

#                     SW_global.single_click_data=k[0]
#                     SW_global.single_click_data.set_visible(True)



#                     #SW_global.cursor_data.append(k)
#                     #print(SW_global.cursor_data)
#                     for cur_count in range(len(SW_global.cursor_data)-1):
#                         invisible_item=SW_global.cursor_data[cur_count]
#                         #print("This is invisible_item")
#                         #print(invisible_item)
#                         invisible_item.set_visible(False)
#                     fig.canvas.draw()

#                     #print(guideline_axes[0].lines)

#             # -----------------------------------------------------------------------------------------------------
#                     final_enrty_pos = len(SW_global.letters_already_written)
#                     final_letter_pos = len(guideline_axes[l].lines)
#                     SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
#                     features_checking_function()
#                     #print("checking for data inserting")
#                     # print(delete_list)
#                     # print(SW_global.recent_input_list)
#                     # print(SW_global.letters_already_written)
#                     # print(SW_global.kern_list)
#                     # print("End")











#     fig.canvas.draw()

def text_flow_features_with_third():
    print("This is delguideline")
    checked1=False
    checked2=False
    loop_complete1=False
    loop_complete2=False
    temp_delete1_list=[]
    temp_delete2_list=[]

    if((SW_global.temp_axes!=None) and ((SW_global.temp_axes==SW_global.text_flow_axes2) or(SW_global.temp_axes==SW_global.text_flow_axes1))):
        if(((SW_global.text_flow_axes1!=None) and(SW_global.text_flow_axes2!=None)) and (SW_global.text_flow_axes1!=SW_global.text_flow_axes2)):
    #        temp_delete1_list=[]
    #        temp_delete2_list=[]
            print()
            if(len(SW_global.text_flow_box_page1)>0):
                checklist=[]
                
                for j in range(len(SW_global.axes_data)):
                    checklist.append(SW_global.axes_data[str(j)]["axis_data"])
                checklist.append(guideline_axes[l])
                for j in SW_global.text_flow_box_page1:
                    for k in checklist:
                        if(j==k):
                            for d in range(len(SW_global.axes_data)):
                                for q in SW_global.axes_data[str(d)]["delete_list"]:
                                    temp_delete1_list.append(q)
                            for q in delete_list:
                                temp_delete1_list.append(q)
                            checked1=True
                            loop_complete1=True
                            break
                    if(loop_complete1==True):
                        break

                if(checked1!=True):
                    for j in range(len(SW_global.box_data)):
                        for k in SW_global.text_flow_box_page1:
                            if(k in SW_global.box_data[str(j)]["axes_list"]):
                                axesdata=SW_global.box_data[str(j)]["SW_global_axes_data"]
                                for g in range(len(axesdata)):
                                    for h in axesdata[str(g)]["delete_list"]:
                                        temp_delete1_list.append(h)
                                for h in SW_global.box_data[str(j)]["delete_list"]:
                                    temp_delete1_list.append(h)
                                loop_complete1=True
                                break
                        if(loop_complete1==True):
                            break
            if(len(SW_global.text_flow_box_page2)>0):
                checklist=[]
                for j in range(len(SW_global.axes_data)):
                        checklist.append(SW_global.axes_data[str(j)]["axis_data"])
                checklist.append(guideline_axes[l])
                for j in SW_global.text_flow_box_page2:
                    for k in checklist:
                        if(j==k):
                            for d in range(len(SW_global.axes_data)):
                                for q in SW_global.axes_data[str(d)]["delete_list"]:
                                    temp_delete2_list.append(q)
                            for q in delete_list:
                                temp_delete2_list.append(q)
                            checked2=True
                            loop_complete2=True
                            break
                    if(loop_complete2==True):
                        break
                if(checked2!=True):
                    loop_complete2=False

                    for j in range(len(SW_global.box_data)):
                        for k in SW_global.text_flow_box_page2:
                            if(k in SW_global.box_data[str(j)]["axes_list"]):
                                axesdata=SW_global.box_data[str(j)]["SW_global_axes_data"]
                                for g in range(len(axesdata)):
                                    for h in axesdata[str(g)]["delete_list"]:
                                        temp_delete2_list.append(h)
                                for h in SW_global.box_data[str(j)]["delete_list"]:
                                    temp_delete2_list.append(h)
                                loop_complete2=True
                                break
                        if(loop_complete2==True):
                            break
            print("This is delete_list1",temp_delete1_list)
            print("This is delete_list2",temp_delete2_list)




################################################### text_flow_features_with_third ###############
def delguideline():
    print("This is delguideline")
    checked1=False
    checked2=False
    loop_complete1=False
    loop_complete2=False
    temp_delete1_list=[]
    temp_delete2_list=[]

    if((SW_global.temp_axes!=None) and ((SW_global.temp_axes==SW_global.text_flow_axes2) or(SW_global.temp_axes==SW_global.text_flow_axes1))):
        if(((SW_global.text_flow_axes1!=None) and(SW_global.text_flow_axes2!=None)) and (SW_global.text_flow_axes1!=SW_global.text_flow_axes2)):
    #        temp_delete1_list=[]
    #        temp_delete2_list=[]
            print()
            if(len(SW_global.text_flow_box_page1)>0):
                checklist=[]
                
                for j in range(len(SW_global.axes_data)):
                    checklist.append(SW_global.axes_data[str(j)]["axis_data"])
                checklist.append(guideline_axes[l])
                for j in SW_global.text_flow_box_page1:
                    for k in checklist:
                        if(j==k):
                            for d in range(len(SW_global.axes_data)):
                                for q in SW_global.axes_data[str(d)]["delete_list"]:
                                    temp_delete1_list.append(q)
                            for q in delete_list:
                                temp_delete1_list.append(q)
                            checked1=True
                            loop_complete1=True
                            break
                    if(loop_complete1==True):
                        break

                if(checked1!=True):
                    for j in range(len(SW_global.box_data)):
                        for k in SW_global.text_flow_box_page1:
                            if(k in SW_global.box_data[str(j)]["axes_list"]):
                                axesdata=SW_global.box_data[str(j)]["SW_global_axes_data"]
                                for g in range(len(axesdata)):
                                    for h in axesdata[str(g)]["delete_list"]:
                                        temp_delete1_list.append(h)
                                for h in SW_global.box_data[str(j)]["delete_list"]:
                                    temp_delete1_list.append(h)
                                loop_complete1=True
                                break
                        if(loop_complete1==True):
                            break
            if(len(SW_global.text_flow_box_page2)>0):
                checklist=[]
                for j in range(len(SW_global.axes_data)):
                        checklist.append(SW_global.axes_data[str(j)]["axis_data"])
                checklist.append(guideline_axes[l])
                for j in SW_global.text_flow_box_page2:
                    for k in checklist:
                        if(j==k):
                            for d in range(len(SW_global.axes_data)):
                                for q in SW_global.axes_data[str(d)]["delete_list"]:
                                    temp_delete2_list.append(q)
                            for q in delete_list:
                                temp_delete2_list.append(q)
                            checked2=True
                            loop_complete2=True
                            break
                    if(loop_complete2==True):
                        break
                if(checked2!=True):
                    loop_complete2=False

                    for j in range(len(SW_global.box_data)):
                        for k in SW_global.text_flow_box_page2:
                            if(k in SW_global.box_data[str(j)]["axes_list"]):
                                axesdata=SW_global.box_data[str(j)]["SW_global_axes_data"]
                                for g in range(len(axesdata)):
                                    for h in axesdata[str(g)]["delete_list"]:
                                        temp_delete2_list.append(h)
                                for h in SW_global.box_data[str(j)]["delete_list"]:
                                    temp_delete2_list.append(h)
                                loop_complete2=True
                                break
                        if(loop_complete2==True):
                            break
            print("This is delete_list1",temp_delete1_list)
            print("This is delete_list2",temp_delete2_list)





            if(SW_global.temp_axes==SW_global.text_flow_axes1):
                print("check point 1")
                SW_global.entire_delete_list_for_one_page.clear()
                for j in temp_delete2_list:
                    SW_global.entire_delete_list_for_one_page.append(j)
                for j in temp_delete1_list:
                    SW_global.entire_delete_list_for_one_page.append(j)
                print("This is SW_global.delete_list for second point",SW_global.entire_delete_list_for_one_page)
                checklist=[]
                for j in range(len(SW_global.axes_data)):
                    checklist.append(SW_global.axes_data[str(j)]["axis_data"])
                checklist.append(guideline_axes[l])
                if(SW_global.text_flow_axes2 in checklist):
                    SW_global.check_u=j

                    for j in range(len(SW_global.axes_data)):
                        for k1 in range(len(SW_global.axes_data[str(j)]["gval"])):
                            if(k1>=3):
                                ((SW_global.axes_data[str(j)]["gval"])[k1]).set_visible(False)
                    for k1 in range(len(guideline_axes[l].lines)):
                        ((guideline_axes[l].lines)[k1]).set_visible(False)
                else:
                    for j in range(len(SW_global.box_data)):
                        if(SW_global.text_flow_axes2 in SW_global.box_data[str(j)]["axes_list"]):
                            print("check point 3")
                            temp=data_Switching2(key=j)
                            if(len(temp)==7):
                                delete_list.clear()
                                for o in temp[0]:
                                    delete_list.append(o)
                                kern_value_array.clear()
                                for o in temp[1]:
                                    kern_value_array.append(0)

                                #delete_list=temp[0].copy()
                                #kern_value_array=temp[1].copy()
                            for k1 in range(len(SW_global.axes_data)):
                                for k2 in range(len(SW_global.axes_data[str(k1)]["gval"])):
                                    if(k2>=3):
                                        ((SW_global.axes_data[str(k1)]["gval"])[k2]).set_visible(False)

                            for k2 in range(len(guideline_axes[l].lines)):
                                if(k2>=3):
                                    ((guideline_axes[l].lines)[k2]).set_visible(False)
                            data_write_with_respect_to_box(delete_list1=SW_global.entire_delete_list_for_one_page)
                            if(SW_global.check_u!=None):


                                print("I am in main selector part 2")
                                SW_global.left=SW_global.box_data[str(SW_global.check_u)]["SW_global.left"]
                                SW_global.right=SW_global.box_data[str(SW_global.check_u)]["SW_global.right"]
                                SW_global.top=SW_global.box_data[str(SW_global.check_u)]["SW_global.top"]
                                SW_global.bottom=SW_global.box_data[str(SW_global.check_u)]["SW_global.bottom"]
                                mainselector.extents=(SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
                                #mainselector.update()
                                fig.canvas.draw()

                            # for k in range(len(SW_global.box_data)):
                            #     if(SW_global.text_flow_axes1 in SW_global.box_data[str(k)]["axes_list"]):
                            #         SW_global.left=SW_global.box_data[str(k)]["SW_global.left"]
                            #         SW_global.right=SW_global.box_data[str(k)]["SW_global.right"]
                            #         SW_global.top=SW_global.box_data[str(k)]["SW_global.top"]
                            #         SW_global.bottom=SW_global.box_data[str(k)]["SW_global.bottom"]
                            #         mainselector.extents=(SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
                            #         mainselector.update()
                            #         fig.canvas.draw()

                            break

                    for j in SW_global.text_flow_box_page1:
                        j.set_visible(False)

            elif(SW_global.temp_axes==SW_global.text_flow_axes2):
                SW_global.entire_delete_list_for_one_page.clear()
                for j in temp_delete1_list:
                    SW_global.entire_delete_list_for_one_page.append(j)
                for j in temp_delete2_list:
                    SW_global.entire_delete_list_for_one_page.append(j)
                print("This is delete_list for one page",SW_global.entire_delete_list_for_one_page)
                checklist=[]
                for j in range(len(SW_global.axes_data)):
                    checklist.append(SW_global.axes_data[str(j)]["axis_data"])
                checklist.append(guideline_axes[l])
                if(SW_global.text_flow_axes1 in checklist):
                    print("do nothing")
                    for j in range(len(SW_global.axes_data)):
                        for k1 in range(len(SW_global.axes_data[str(j)]["gval"])):
                            if(k1>=3):
                                ((SW_global.axes_data[str(j)]["gval"])[k1]).set_visible(False)
                    for k1 in range(len(guideline_axes[l].lines)):
                        ((guideline_axes[l].lines)[k1]).set_visible(False)

                else:
                    print("I am in second part ")
                    for j in range(len(SW_global.box_data)):
                        if(SW_global.text_flow_axes1 in SW_global.box_data[str(j)]["axes_list"]):
                            print("I am in tird part")
                            SW_global.check_u1=j
                            temp=data_Switching2(key=j)
                            if(len(temp)==7):
                                delete_list.clear()
                                kern_value_array.clear()
                                #delete_list=temp[0].copy()
                                #kern_value_array=temp[1].copy()
                                for o in temp[0]:
                                    delete_list.append(o)
                                for o in temp[1]:
                                    kern_value_array.append(o)

                                #break
                            for k1 in range(len(SW_global.axes_data)):
                                for k2 in range(len(SW_global.axes_data[str(k1)]["gval"])):
                                    if(k2>=3):
                                        ((SW_global.axes_data[str(k1)]["gval"])[k2]).set_visible(False)

                            for k2 in range(len(guideline_axes[l].lines)):
                                if(k2>=3):
                                    ((guideline_axes[l].lines)[k2]).set_visible(False)
                            data_write_with_respect_to_box(delete_list1=SW_global.entire_delete_list_for_one_page)
                            if(SW_global.check_u1!=None):
                                print("This is main selctor part2 ")
                                SW_global.left=SW_global.box_data[str(SW_global.check_u1)]["SW_global.left"]
                                print(SW_global.left)
                                SW_global.right=SW_global.box_data[str(SW_global.check_u1)]["SW_global.right"]
                                print(SW_global.right)
                                SW_global.top=SW_global.box_data[str(SW_global.check_u1)]["SW_global.top"]
                                print(SW_global.top)
                                SW_global.bottom=SW_global.box_data[str(SW_global.check_u1)]["SW_global.bottom"]
                                print(SW_global.bottom)
                                mainselector.extents =(SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
                                mainselector.update()
                                fig.canvas.draw()

                            # for k in range(len(SW_global.box_data)):
                            #     if(SW_global.text_flow_axes1 in SW_global.box_data[str(k)]["axes_list"]):
                            #         SW_global.left=SW_global.box_data[str(k)]["SW_global.left"]
                            #         SW_global.right=SW_global.box_data[str(k)]["SW_global.right"]
                            #         SW_global.top=SW_global.box_data[str(k)]["SW_global.top"]
                            #         SW_global.bottom=SW_global.box_data[str(k)]["SW_global.bottom"]
                            #         mainselector.extents=(SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
                            #         mainselector.update()
                            #         fig.canvas.draw()


                            break
                    for j in SW_global.text_flow_box_page2:
                        j.set_visible(False)
            fig.canvas.draw()





        else:
            checklist=[]
            for j in range(len(SW_global.axes_data)):
                checklist.append(SW_global.axes_data[str(j)]["axis_data"])
            checklist.append(guideline_axes[l])
            if(SW_global.temp_axes in chcklist):
                for j in checklist:
                    j.set_visible(False)
            else:
                for j in range(len(SW_global.box_data)):
                    if(temp_axes in SW_global.box_data[str(j)]["axes_list"]):
                        for k in SW_global.box_data[str(j)]["axes_list"]:
                            k.set_visible(False)
            fig.canvas.draw()
    return 

def data_write_with_respect_to_box(delete_list1=None):

    SW_global.temp_guideline_axes=None
    g_val2=[]
    if(len(SW_global.axes_data)>0):
        SW_global.temp_guideline_axes=SW_global.axes_data[str(0)]["axis_data"]
        g_val2=[i for i in SW_global.axes_data[str(key)]["lines"]]
    else:
        SW_global.temp_guideline_axes=guideline_axes[l]
        g_val2=[i for i in guideline_axes[l].lines]
    SW_global.recent_input_list.clear()
    SW_global.kern_list.clear()
    SW_global.kern_list.insert(0,0)
    SW_global.letters_already_written.clear()
    SW_global.cursor_pos.clear()
    SW_global.cursor_pos.insert(0,0)
    SW_global.cursor_data.clear()
    delete_list.clear()
    kern_value_array.clear()
    kern_value_array.insert(0,0)
    for j in range(len(SW_global.axes_data)):
        (SW_global.axes_data[str(j)]["cursor_pos"]).clear()
        (SW_global.axes_data[str(j)]["cursor_data"]).clear()
        (SW_global.axes_data[str(j)]["letters_already_written"]).clear()
        (SW_global.axes_data[str(j)]["kern_list"]).clear()
        (SW_global.axes_data[str(j)]["kern_value_array"]).clear()
        (SW_global.axes_data[str(j)]["delete_list"]).clear()
        (SW_global.axes_data[str(j)]["recent_input_list"]).clear()
    count_of_axes=0
    kern_value_array2=[0]
    letters_already_written2=[]
    kern_list2=[0]
    recent_input_list2=[]
    #g_val2=[i for i in SW_global.axes_data[str(key)]["lines"]]
    cursor_data2=[]
    cursor_pos2=[0]
    delete_list2=[]
    guideline_flag=-9999
    print("This is delete list:",delete_list1)
    temp_flag=0
    for k10 in range(len(delete_list1)):
        #print("count_of_axes:",count_of_axes)
        #print("axes is :",SW_global.temp_guideline_axes)
        #temp_guideline_axes=SW_global.axes_data[str(count_of_axes)]["axis_data"]
        #print("axis need to be:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
        if(kern_list2[0]>15500):
            print("check point we*********************************************************")
            if(count_of_axes>len(SW_global.axes_data)-1):
                #print("This is check point 11")
                if(guideline_flag>0):
                    a=dict()
                    a["letters_already_written"]=[j for j in  letters_already_written2]
                    a["kern_value_array"]=[j for j in kern_value_array2]
                    a["delete_list"]=[j for j in delete_list2]
                    a["kern_list"]=[j for j in kern_list2]
                    a["lines"]=[j for j in g_val2]
                    a["gval"]=[j for j in g_val2]
                    a["cursor_pos"]=[j for j in cursor_pos2]
                    a["cursor_data"]=[j for j in cursor_data2]
                    a["axis_data"]=guideline_axes[l]
                    a["compositedot_already_applied_array"]=[]
                    a["decisiondot_already_applied_array"]=[]
                    a["connectdot_already_applied_array"]=[]
                    a["startdot_already_applied_array"]=[]
                    a["recent_input_list"]=[j for j in recent_input_list2]
                    a["connect_dot_flag_pos"]=0
                    a["decision_dot_flag_pos"]=0
                    a["stoke_arrow_flag_pos"]=0
                    a["startdot_flag_pos"]=0
                    SW_global.axes_data[str(len(SW_global.axes_data))]=a
                    newCreateGuideLine(1,None,None,None,None)
                    print("This is check point22")
                    count_of_axes=count_of_axes+1
                    SW_global.current_pos=0
                    SW_global.current_axes=guideline_axes[l]
                else:
                 #   print("This is check point33")
            ##        print("check point delta 2")
                    guideline_axes[l].lines.clear()
                    for j in g_val2:
                        guideline_axes[l].lines.append(j)
                    SW_global.letters_already_written.clear()
                    for j in letters_already_written2:
                        SW_global.letters_already_written.append(j)
                    SW_global.recent_input_list.clear()
                    for j in recent_input_list:
                        SW_global.recent_input_list.append(j)
                    SW_global.cursor_pos.clear()
                    for j in cursor_pos2:
                        SW_global.cursor_pos.append(j)
                    SW_global.cursor_data.clear()
                    for j in cursor_data2:
                        SW_global.cursor_data.append(j)
                    SW_global.kern_list.clear()
                    for j in kern_list2:
                        SW_global.kern_list.append(j)
                    guideline_flag=40
                    #newCreateGuideLine(1,None,None,None)
                    count_of_axes=count_of_axes+1
                  #  print("This is check point44")
              ##  print("check point delta 3")
              #  g_val2.clear()
                delete_list2.clear()
                cursor_data2.clear()
                cursor_pos2.insert(0,0)
                letters_already_written2.clear()
                recent_input_list2.clear()
                kern_value_array2.clear()
                kern_value_array2.insert(0,0)
                kern_list2.clear()
                kern_list2.insert(0,0)
                # guideline_flag=40 #### speacial flag for guide line indication
                SW_global.temp_guide_line_axes=guideline_axes[l]
                #print("This is check point55")



            else:
                #print("check point 66")
                SW_global.axes_data[str(count_of_axes)]["letters_already_written"]=[k for k in letters_already_written2]
                SW_global.axes_data[str(count_of_axes)]["cursor_pos"]=[k for k in cursor_pos2]
                SW_global.axes_data[str(count_of_axes)]["cursor_data"]=[ k for k in cursor_data2]
                SW_global.axes_data[str(count_of_axes)]["recent_input_list"]=[k for k in recent_input_list2]
                SW_global.axes_data[str(count_of_axes)]["delete_list"]=[k for k in delete_list2]
                SW_global.axes_data[str(count_of_axes)]["gval"]=[k for k in g_val2]
                SW_global.axes_data[str(count_of_axes)]["lines"]=[k for k in g_val2]
                SW_global.axes_data[str(count_of_axes)]["kern_value_array"]=[k for k in kern_value_array2]
                SW_global.axes_data[str(count_of_axes)]["kern_list"]=[k for k in kern_list2]
                g_val2.clear()
                delete_list2.clear()
                cursor_data2.clear()
                cursor_pos2.clear()
                cursor_pos2.insert(0,0)
                letters_already_written2.clear()
                recent_input_list2.clear()
                kern_value_array2.clear()
                kern_value_array2.insert(0,0)
                kern_list2.clear()
                print("check point 41")
                kern_list2.insert(0,0)
                print("check point wwwwqqqq")
                print("count_of_axes:",count_of_axes)
                print("len(axes_data):",len(SW_global.axes_data))
                if(count_of_axes>=len(SW_global.axes_data)-1):
                    SW_global.temp_guideline_axes=guideline_axes[l]
                    g_val2.clear()
                    g_val2.append(guideline_axes[l].lines[0])
                    g_val2.append(guideline_axes[l].lines[1])
                    g_val2.append(guideline_axes[l].lines[2])
                    g_val2.append(guideline_axes[l].lines[3])
                else:
                    count_of_axes=count_of_axes+1
                    SW_global.temp_guideline_axes=SW_global.axes_data[str(count_of_axes)]["axis_data"]
                    g_val2.clear()
                    for h1 in SW_global.axes_data[str(count_of_axes)]["lines"]:
                        g_val2.append(h1)
                 #   print("check point 28")
                 #   SW_global.temp_guideline_axes=guideline_axes[l]
        # print("check point 29")
    #     #### Write code for data inserting on speacific axes ####
        length12=len(recent_input_list2)
        user_input=delete_list1[k10]
        print("SW_global.axes_data",SW_global.temp_guideline_axes)
        # print("QWE:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
      #  print("user_input:",user_input)
        x_max=manuscript.x_max[user_input]
        kern_x=kern_list2[0]
      #  print("I am in loop check point1 ")

        ###################################################################################
        skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
        if user_input in skip_list:
            if(color_letter_features_on_off):
                c1,c2=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
            else:
                c1,c2=manuscript.return_manuscript_fonts(user_input)
        else:
            if(color_letter_features_on_off):
                x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                c1,c2=font_check(x,y)
            else:
                x,y=manuscript.return_manuscript_fonts(user_input)
                c1,c2=font_check(x,y)
    ####################################################################################

        c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)


        kern_x=kern_list2[0]+x_max+300
        kern_list2.insert(0,kern_x)
       # print("check point 30")
        # c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)
        kern_counter=len(kern_value_array2)
        kern_value_array2.insert(kern_counter,kern_x)
        recent_input_list2.insert(length12,user_input)
        delete_list2.insert(length12,user_input)
        init_enrty_pos=len(letters_already_written2)
        inti_letter_pos=len(g_val2)
        #print("check point 31")
        print("SW_global.temp_guideline_axes:",SW_global.temp_guideline_axes)
        letters_already_written2.insert(init_enrty_pos,inti_letter_pos)
     #   print("check point 2")
        temp_o=[]

        if(draw_type_color_letter==1):
         #   print("check point 32")
            if(letter_dot_density_no_dot_on_off==1):
                alp=0
            else:
                alp=temp_alp
            if(color_letter_features_on_off):
                temp_o.clear()
          #      print("check point 33")
                temp_o=SW_global.temp_guideline_axes.plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                for k2 in temp_o:
                    g_val2.append(k2)
                print("count of axes:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
                print("temp_guideline_axes",SW_global.temp_guideline_axes)
            else:
           #     print("check point 34")
                temp_o=SW_global.temp_guideline_axes.plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                for k2 in temp_o:
                    g_val2.append(k2)
               # print("count_of_axes",SW_global.axes_data[str(count_of_axes)]["axis_data"])
                print("SW_global",SW_global.temp_guideline_axes)
        else:
           # print("check point 35")
            n=len(c1)
            if letter_dot_density_no_dot_on_off == 1:
                alp=0
            else:
                alp=temp_alp

            #print("check point 36")


            if(color_letter_features_on_off):
             #   print("check point 37")
                for i in range(n):
                    if i==0:
                        temp_o.clear()
                        temp_o=SW_gobal.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        for k2 in temp_o:
                            g_val2.append(k2)
                    if i==1:
                        temp_o.clear()
                        temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        for k2 in temp_o:
                            g_val2.append(k2)
                    if i==2:
                        temp_o.clear()
                        temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        for k2 in temp_o:
                            g_val2.append(k2)
                    if i==3:
                        temp_o.clear()
                        temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        for k2 in temp_o:
                            g_val2.append(k2)
            else:
              #  print("check point 38")
                for i in range(n):
                    temp_o.clear()
                    temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    for k2 in temp_o:
                        g_val2.append(k2)

        fig.canvas.draw()

        import numpy as np
        item_cursor=kern_x-300
        cursor_y=list(np.linspace(-900,1500,500))
        cursor_x=list(np.full(500,item_cursor))
        cursor_pos2.append(item_cursor)
        cursor_x1=list(np.full(500,item_cursor))
        if(SW_global.single_click_data!=None):
           # print("check point 39")
            SW_global.single_click_data.set_visible(False)

        plot_data=SW_global.temp_guideline_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
        SW_global.single_click_data=plot_data[0]
        k2=SW_global.temp_guideline_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))

      #  print("check point 40")

        for j10 in k2:
            cursor_data2.append(j10)
            j10.set_visible(False)

      #  print("check point 41")


        final_enrty_pos = len(letters_already_written2)
        final_letter_pos = len(g_val2)
        letters_already_written2.insert(final_enrty_pos, final_letter_pos)

      #  print("check point 42")
   #     print("I am in for loop end part ")


    # for k1 in SW_global.axes_data[str(key)]["cursor_pos"]:
    #     if k1==SW_global.current_pos_in_number:
    #         if((k1+1)>len(SW_global.axes_data[str(key)]["cursor_pos"])):
    #             #### set next axes of current_axes as current_axes and current_pos =0
    #             #### if there is no axes_data left then make guideline_axes as current_axes
    #             #### else make normal current_pos
    #             if((key+1)>len(SW_global.axes_data)-1):
    #                 SW_global.current_axes=guideline_axes[l]
    #                 SW_global.current_pos=0
    #             else:
    #                 SW_global.current_axes=SW_global.axes_data[str(key+1)]["axis_data"]
    #                 SW_global.current_pos=0

    #         else:
    #             SW_global.current_pos=(SW_global.axes_data[str(key)]["cursor_pos"])[k1+1]
    #             SW_global.current_axes=SW_global.axes_data[str(key)]["axis_data"]
    #             SW_global.current_pos_in_number=k1+1
    SW_global.cursor_pos.clear()
    for k1 in cursor_pos2:
        SW_global.cursor_pos.append(k1)
    for k1 in cursor_data2:
        SW_global.cursor_data.append(k1)
    guideline_axes[l].lines.clear()
    for k1 in g_val2:
        guideline_axes[l].lines.append(k1)

    SW_global.letters_already_written.clear()

    for k1 in letters_already_written2:
        SW_global.letters_already_written.append(k1)

    SW_global.kern_list.clear()
    for k1 in kern_list2:
        SW_global.kern_list.append(k1)
    SW_global.current_axes=guideline_axes[l]
    if(len(SW_global.cursor_pos)>0):
        SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]



    return delete_list2,kern_value_array2





    #for 
    # if SW_global.gdaxes == key_c:
    #     SW_global.gd_flag1 = False
    #     SW_global.g_val.set_position([0.01, 0.01, 0, 0])
    #     SW_global.g_val.set_visible(False)
    #     SW_global.g_val.cla()
    #     fig.canvas.draw()
    #     SW_global.recent_input_list1.clear()
    #     SW_global.kern_list1.clear()
    #     SW_global.kern_list1.insert(0, 0)
    #     kern_value_array1.clear()
    #     delete_list1.clear()
    #     if SW_global.new_gd == 1:
    #         guideline_axes1_1.set_position([0.00001, 0.0001, 0, 0])
    #         guideline_axes1_1.set_visible(False)
    #         guideline_axes1_1.cla()
    #         mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom+0.15, SW_global.top)
    #         mainselector.update()
    #     fig.canvas.draw()

# -----------------------------------insert_page_option_mw------------------------------------------#

def add_user_page(application_frame):
    global my_counter,my_label, wd
    global base_x, median_x, descender_x, ascender_x, base_y, median_y, descender_y, ascender_y

    my_counter = ttk.Frame(application_frame, width=wd, height=600)
    my_counter.pack(side=TOP, fill=X)

    fig = plt.figure()

    fig_axes1 = fig.add_axes([0, 0, 1, 1])

    fig_axes1.patch.set_alpha(0.3)


    guideline_axes[l] = fig.add_axes([SW_global.lt_gd_1, SW_global.btm_gd_1, SW_global.wd_gd_1, SW_global.ht_gd_1])
    guideline_axes[l].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

    img = plt.imread('icons/apple.jpg')
    guideline_axes[l].imshow(img, extent = [0.999,1,0.999,1])

    for ln in ['top','right','left','bottom']:
        guideline_axes[l].spines[ln].set_linewidth(0)
        fig.canvas.draw()
    default_guideline(guideline_axes[l])

    fig.set_size_inches(6, 9)

    fig.text(0.98, 0.009, EtsPyTech.dev_details(),
             fontsize=7, color='black',
             ha='right', va='bottom', alpha=0.090)

    addScrollingFigure(fig, my_counter)
    #from PIL import Image
    import numpy as np
    import matplotlib.image as img
   # m = img.imread("C:/Users/ets_asp 2/Desktop/SW/StartWrite-Desktop/StartWrite-Desktop/Images/Color Pictures/apple1.jpg")

    mainselector = widgets.RectangleSelector(fig_axes1, onselect,
                                   drawtype='box', interactive=True,
                                   spancoords='pixels', minspany=110, maxdist=50, button=1,
                                   rectprops=dict(facecolor='white',linestyle= '--',
                                                  edgecolor='black', alpha=0.45, fill=True))

    # Initial Selector Position is Setting Here
    #mainselector.extents = (0.99,0.01,0.83,0.98)

    print("This is check point 2")
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event',onclick2)
    fig.canvas.mpl_connect('button_release_event',onrelease)
    canvas.configure(background='grey')
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

vv1 = tk.IntVar()  # insert_page_option_mw variable
vv1.set(0)

# insert_page_option_mw ----> Functions
def page_insert_option():
    if vv1.get() == 0:
        SW_global.pg_flag = 1
        add_user_page(writingareaframe2)
        rhtpgButton.configure(command=lambda:raise_frame(writingareaframe2))
        pageLabel.config(text="page "+ str(int(SW_global.page_no)) +"of "+ str(int(SW_global.page_no) +1))
    elif vv1.get() == 1:
        add_user_page(writingareaframe2)
        SW_global.pg_flag = 2
        lftpgButton.config(command=lambda:raise_frame(writingareaframe2))
        SW_global.page_no = 2
        pageLabel.config(text="page "+ str(int(SW_global.page_no)) +"of "+ str(int(SW_global.page_no)))

    print("Page on : ",vv1.get())

def insert_page_option_mw():
    insert_page = Toplevel(SW_Main_UI)
    insert_page.wm_title("Insert Page")
    insert_page.geometry("400x150+200+250")
    insert_page.resizable(width=False, height=False)
    insert_page.wm_transient(SW_Main_UI)
    insert_page_labelframe = LabelFrame(insert_page, text="Insert Page")
    insert_page_labelframe.pack(side=LEFT, fill="both", pady=15, padx=10)

    # initializing the choice
    insert_page_option = [("After current page"),
                          ("Before current page"),
                          ("At beginning of document"),
                          ("At end of document")
                          ]
    for val1, insert_page_option in enumerate(insert_page_option):
        insert_page_option_rb = tk.Radiobutton(insert_page_labelframe, text=insert_page_option, variable=vv1,
                                               value=val1)
        insert_page_option_rb.pack(anchor=W)
    def insert_page_close():
        page_insert_option()
        insert_page.destroy()

    insert_page_button_ok = ttk.Button(insert_page, text="OK", command=insert_page_close)
    insert_page_button_ok.pack(side=TOP, padx=5, pady=18)
    insert_page_button_cancel = ttk.Button(insert_page, text="Cancel", command=insert_page.destroy)
    insert_page_button_cancel.pack(side=TOP, padx=5)

#############################################################################################################

call_g = 1
gl, gb = 0.01, 0.84
sl_t, sl_b = 0.98, 0.83
l = 0
def create_guideline(n):
    global gl, gb, sl_t, sl_b, l,key_c, l


    s = n / 100
    old_l = (0 + s)
    sl = (gb - s)
    old_b = (l + sl)
    guideline_axes[l] = plt.axes([old_l, old_b, 0.98, 0.15])
    img = plt.imread('icons/guideline.PNG')
    guideline_axes[l].imshow(img, extent=[0.0004, 0.0005, 0.0006, 0.002])
    guideline_axes[l].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off',
                                      right='off', left='off', labelleft='off')

    for ln in ['top', 'right', 'left', 'bottom']:
        guideline_axes[l].spines[ln].set_linewidth(0)

    default_guideline(guideline_axes[l])

    SW_global.left = 0.99
    SW_global.right = 0.01
    SW_global.top = sl_t
    SW_global.bottom = sl_b
    mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)

    fig.canvas.draw()


def call_multigudeline():
    global call_g, g_c, fnl_g, gsub_list2, gsub_list1
    global gl, gb, sl_t, sl_b
    newCreateGuideLine(1,None,None,None,None)
    gl, gb = (gl + 0.04), (gb - 0.04)
    sl_t, sl_b = (sl_t - 0.04), (sl_b - 0.04)
    g_c = g_c + 1
    gsub_list1.append(g_c)
    gsub_list2.append(guideline_axes[l])
    fnl_g = dict(zip(gsub_list1, gsub_list2))

#############################################################################################################

def replace_art_box():
    global m, y
    filename = filedialog.askopenfilename(initialdir="Images", title="Select Art",
                                          filetypes=(("Art Files", "*.*"), ("all files", "*.*")))
    image_axes = np.empty([m], dtype=object)
    for y in range(m):
        image_axes[y] = plt.axes([0.04,0.65, 0.14, 0.14])
        image_axes[y].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
        image = plt.imread(filename)
        image_axes[y].imshow(image)
        fig.canvas.draw()

img_v = 1
ll, bb = 0.04, 0.65
z = 0
multiimg_flg = False
pre_l,pre_b = 0, 0
def add_new_art_box():
    global ll, bb, multiimg_flg
    global m, y, img_v, z,pre_l,pre_b
    filename = filedialog.askopenfilename(initialdir="Images", title="Select Art",
                                          filetypes=(("Art Files", "*.*"), ("all files", "*.*")))

    def create_multiartbox(im):
        global ll, bb, multiimg_flg, z,pre_l,pre_b
        image_axes = np.empty([im], dtype=object)
        for z in range(im):
            c = im/100
            o = c + c
            pre_l = (ll + c)
            pre_b = (bb - o)
            image_axes[z] = plt.axes([pre_l,pre_b, 0.14, 0.14])
            image_axes[z].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
            image = plt.imread(filename)
            image_axes[z].imshow(image)
            fig.canvas.draw()
            print("im range : pre_l : pre_b :=",im,pre_l,pre_b)
            multiimg_flg = True
    def call_multiartbox():
        global img_v, ll, bb
        create_multiartbox(img_v)

    if image_axes[y]:

        call_multiartbox()
        ll, bb = (ll + 0.01), (bb - 0.01)
    else:
        for y in range(m):
            image_axes[y] = plt.axes([ll, bb, 0.14, 0.14])
            image_axes[y].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
            image = plt.imread(filename)
            image_axes[y].imshow(image)
            fig.canvas.draw()

##########################################################################################################
#check_flag=-1
def add_text_box():
    print("*"*100)
    print("This is from add text box")
    print("This is SW_global.axes_data",SW_global.axes_data)
    print("This is guideline_axes[l].lines",guideline_axes[l].lines)
    print("kern_value_array",kern_value_array)
    print("This is kern_list",SW_global.kern_list)
    print("*"*100)

    axes_list_for_box=[]
    for j in range(len(SW_global.axes_data)):
        axes_list_for_box.append(SW_global.axes_data[str(j)]["axis_data"])
    axes_list_for_box.append(guideline_axes[l])
    if(len(SW_global.box_data)>0):
        print("I am in axes data")
        print("*"*200)
        data_checking_for_need_to_create_or_update_back_page(axes_list=axes_list_for_box,delete_list1=delete_list,kern_value_array1=kern_value_array)
    else:
        create_new_page_on_box_data(delete_list1=delete_list,kern_value_array1=kern_value_array)



    #SW_global.count_for_height=0
    reset_after()
    new_create_text_box(1,SW_global.shift_no)
    SW_global.shift_no=SW_global.shift_no+1
    print("This is shift no ",SW_global.shift_no)
    return
    #newCreateGuideLine(1,None,None,None,None)

    #global  gl, gb
  #   a=dict()
  #   #check_flag=-1
  #   if(len(SW_global.box_data)==0):
  #       a=dict()
  #       a["startdot_on_off"]=SW_global.startdot_on_off
  #       a["decisiondot_on_off"]=SW_global.decisiondot_on_off
  #       a["stokearrow_on_off"]=SW_global.stokearrow_on_off
  #       a["connectdot_on_off"]=SW_global.connectdot_on_off
  #       a["color_letter_features_on_off"]=color_letter_features_on_off
  #       a["letter_out_line_on_off"]=letter_out_line_on_off
  #       a["SW_global_axes_data"]=SW_global.axes_data.copy()
  #       a["SW_global.left"]=SW_global.left
  #       a["SW_global.right"]=SW_global.right
  #       a["SW_global.bottom"]=SW_global.bottom
  #       a["SW_global.top"]=SW_global.top
  #       a["axes_list"]=[]
  #       for j in range(len(SW_global.axes_data)):
  #           a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])
  #       a["axes_list"].append(guideline_axes[l])
  #       # a["s"]=s
  #       a["count_for_height"]=SW_global.count_for_height
  #       a["guideline_axes"]=guideline_axes[l]
  #       a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
  #       a["cursor_data"]=SW_global.cursor_data.copy()
  #       a["cursor_pos"]=SW_global.cursor_pos.copy()
  #       a["kern_value_array"]=kern_value_array
  #       a["kern_list"]=(SW_global.kern_list).copy()
  #       a["delete_list"]=delete_list.copy()
  #       delete_list.clear()
  #       a["gl"]=gl
  #       a["gb"]=gb
  #       a["sl_t"]=sl_t
  #       a["sl_b"]=sl_b
  #       a["l"]=l
  #       a["key_c"]=key_c
  #       a["call_g"]=call_g
  #       a["gl"]=gl
  #       SW_global.box_data[str(len(SW_global.box_data))]=a
  #       SW_global.kern_list.clear()
  #       kern_value_array.clear()
  #       SW_global.kern_list.insert(0,0)
  #       kern_value_array.insert(0,0)
  #       SW_global.cursor_pos.clear()
  #       SW_global.cursor_pos.insert(0,0)
  #       SW_global.cursor_data.clear()
  #       delete_list.clear()
  #       SW_global.axes_data.clear()
  #       reset_after()
  #       SW_global.count_for_height=0
  #       newCreateGuideLine(1,None,None,None,None)   
  #    #   check_flag=10
  #   else:
  #      # check_flag=-1
  #       if(len(SW_global.axes_data)>0):
  #           check_axis=SW_global.axes_data[str(0)]["axis_data"]
  #           for j in range(len(SW_global.box_data)):
  #               check_array_of_axes=SW_global.box_data[str(j)]["axis_data"]
  #               if(check_axis  in check_array_of_axes):

  #                   a=dict()
  #                   a["startdot_on_off"]=SW_global.startdot_on_off
  #                   a["decisiondot_on_off"]=SW_global.decisiondot_on_off
  #                   a["stokearrow_on_off"]=SW_global.stokearrow_on_off
  #                   a["connectdot_on_off"]=SW_global.connectdot_on_off
  #                   a["color_letter_features_on_off"]=color_letter_features_on_off
  #                   a["letter_out_line_on_off"]=letter_out_line_on_off
  #                   a["SW_global_axes_data"]=SW_global.axes_data.copy()
  #                   a["SW_global.left"]=SW_global.left
  #                   a["SW_global.right"]=SW_global.right
  #                   a["SW_global.bottom"]=SW_global.bottom
  #                   a["SW_global.top"]=SW_global.top
  #                   a["axes_list"]=[]
  #                   for j in range(len(SW_global.axes_data)):
  #                       a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])

  #                   a["axes_list"].append(guideline_axes)
  #                   # a["s"]=s
  #                   a["count_for_height"]=SW_global.count_for_height
  #                   a["guideline_axes"]=guideline_axes[l]
  #                   a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
  #                   a["cursor_data"]=SW_global.cursor_data.copy()
  #                   a["cursor_pos"]=SW_global.cursor_pos.copy()
  #                   a["kern_value_array"]=kern_value_array
  #                   a["kern_list"]=(SW_global.kern_list).copy()
  #                   a["delete_list"]=delete_list.copy()
  #                   # a["n"]=n
  #                   # a["old_l"]=old_l
  #                   a["gl"]=gl
  #                   a["gb"]=gb
  #                   a["sl_t"]=sl_t
  #                   a["sl_b"]=sl_b
  #                   a["l"]=l
  #                   a["key_c"]=key_c
  #                   a["call_g"]=call_g
  #                   a["gl"]=gl
  #                   delete_list.clear()
  #                   SW_global.box_data[str(j)]=a

  #                   SW_global.box_data[len(SW_global.box_data)]=a
  #                   SW_global.kern_list.clear()
  #                   kern_value_array.clear()
  #                   SW_global.kern_list.insert(0,0)
  #                   kern_value_array.insert(0,0)
  #                   SW_global.cursor_pos.clear()
  #                   SW_global.cursor_pos.insert(0,0)
  #                   SW_global.cursor_data.clear()
  #                   delete_list.clear()
  #                   SW_global.axes_data.clear()
  #                   reset_after()
  #                   SW_global.count_for_height=0
  #                   newCreateGuideLine(1,None,None,None,None)  
  #                   check_flag=10 
  #       else:
  #           check_axes=guideline_axes[l]
  #           for j in range(len(SW_global.box_data)):
  #               check_array_of_axes=SW_global.box_data[str(j)]["guideline_axes"]
  #               if(check_axes==check_array_of_axes):
  #                   a=dict()
  #                   a["startdot_on_off"]=SW_global.startdot_on_off
  #                   a["decisiondot_on_off"]=SW_global.decisiondot_on_off
  #                   a["stokearrow_on_off"]=SW_global.stokearrow_on_off
  #                   a["connectdot_on_off"]=SW_global.connectdot_on_off
  #                   a["color_letter_features_on_off"]=color_letter_features_on_off
  #                   a["letter_out_line_on_off"]=letter_out_line_on_off
  #                   a["SW_global_axes_data"]=SW_global.axes_data.copy()
  #                   a["SW_global.left"]=SW_global.left
  #                   a["SW_global.right"]=SW_global.right
  #                   a["SW_global.bottom"]=SW_global.bottom
  #                   a["SW_global.top"]=SW_global.top
  #                   a["axes_list"]=[]
  #                   for j in range(len(SW_global.axes_data)):
  #                       a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])
  #                   # a["s"]=s
  #                   a["axes_list"].append(guideline_axes[l])
  #                   a["count_for_height"]=SW_global.count_for_height
  #                   a["guideline_axes"]=guideline_axes[l]
  #                   a["delete_list"]=delete_list.copy()
  #                   a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
  #                   a["cursor_data"]=SW_global.cursor_data.copy()
  #                   a["cursor_pos"]=SW_global.cursor_pos.copy()
  #                   a["kern_value_array"]=kern_value_array
  #                   a["kern_list"]=(SW_global.kern_list).copy()
  #                   # a["n"]=n
  #                   # a["old_l"]=old_l
  #                   a["gl"]=gl
  #                   a["gb"]=gb
  #                   a["sl_t"]=sl_t
  #                   a["sl_b"]=sl_b
  #                   a["l"]=l
  #                   a["key_c"]=key_c
  #                   a["call_g"]=call_g
  #                   a["gl"]=gl
  #                   SW_global.box_data[str(j)]=a
  #                   delete_list.clear()
  # #      SW_global.box_data[len(SW_global.box_data)]=a
  #                   SW_global.kern_list.clear()
  #                   kern_value_array.clear()
  #                   SW_global.kern_list.insert(0,0)
  #                   kern_value_array.insert(0,0)
  #                   SW_global.cursor_pos.clear()
  #                   SW_global.cursor_pos.insert(0,0)
  #                   SW_global.cursor_data.clear()
  #                   delete_list.clear()
  #                   SW_global.axes_data.clear()
  #                   reset_after()
  #                   SW_global.count_for_height=0
  #                   newCreateGuideLine(1,None,None,None,None)   
  #                   check_flag=10

  #               #else:
  #           if(check_flag==-1):
  #               a=dict()
  #               a["startdot_on_off"]=SW_global.startdot_on_off
  #               a["decisiondot_on_off"]=SW_global.decisiondot_on_off
  #               a["stokearrow_on_off"]=SW_global.stokearrow_on_off
  #               a["connectdot_on_off"]=SW_global.connectdot_on_off
  #               a["color_letter_features_on_off"]=color_letter_features_on_off
  #               a["letter_out_line_on_off"]=letter_out_line_on_off
  #               a["SW_global_axes_data"]=SW_global.axes_data.copy()
  #               a["SW_global.left"]=SW_global.left
  #               a["SW_global.right"]=SW_global.right
  #               a["SW_global.bottom"]=SW_global.bottom
  #               a["SW_global.top"]=SW_global.top
  #               a["axes_list"]=[]
  #               for j in range(len(SW_global.axes_data)):
  #                   a["axes_list"].append(SW_global.axes_data[str(j)]["axis_data"])
  #               a["axes_list"].append(guideline_axes[l])
  #               # a["s"]=s
  #               a["count_for_height"]=SW_global.count_for_height
  #               a["guideline_axes"]=guideline_axes[l]
  #               a["guideline_axes_lines"]=(guideline_axes[l].lines).copy()
  #               a["cursor_data"]=SW_global.cursor_data.copy()
  #               a["cursor_pos"]=SW_global.cursor_pos.copy()
  #               a["kern_value_array"]=kern_value_array
  #               a["kern_list"]=(SW_global.kern_list).copy()
  #               a["delete_list"]=delete_list.copy()
  #               a["gl"]=gl
  #               a["gb"]=gb
  #               a["sl_t"]=sl_t
  #               a["sl_b"]=sl_b
  #               a["l"]=l
  #               a["key_c"]=key_c
  #               a["call_g"]=call_g
  #               a["gl"]=gl
  #               SW_global.box_data[len(SW_global.box_data)]=a
  #               SW_global.kern_list.clear()
  #               kern_value_array.clear()
  #               SW_global.kern_list.insert(0,0)
  #               kern_value_array.insert(0,0)
  #               SW_global.cursor_pos.clear()
  #               SW_global.cursor_pos.insert(0,0)
  #               SW_global.cursor_data.clear()
  #               delete_list.clear()
  #               SW_global.axes_data.clear()
  #               reset_after()
  #               SW_global.count_for_height=0
  #               newCreateGuideLine(1,None,None,None,None)   

    fig.canvas.draw()



def reset_after():
    SW_global.count_for_height=0
    call_g = 1
    gl, gb = 0.01, 0.84
    sl_t, sl_b = 0.98, 0.83
    l=0
    kern_value_array.clear()
    kern_value_array.insert(0,0)
    SW_global.kern_list.clear()
    SW_global.kern_list.insert(0,0)
    SW_global.cursor_data.clear()
    SW_global.cursor_pos.clear()
    SW_global.cursor_pos.insert(0,0)
    SW_global.letters_already_written.clear()
    SW_global.axes_data.clear()
    delete_list.clear()
    SW_global.recent_input_list.clear()
    SW_global.left, SW_global.right, SW_global.bottom, SW_global.top = 0.99,0.01,0.83,0.98
    return #call_g,gl,gb,sl_t,sl_b

#--------------------------------------------------------------------------------------------------------#
def snln0():
    if SW_global.gdaxes == key_c:
        for ln in ['top','right','left','bottom']:
            guideline_axes[l].spines[ln].set_linewidth(0)
            fig.canvas.draw()

def snln1():
    if SW_global.gdaxes == key_c:
        for ln in ['top','right','left','bottom']:
            guideline_axes[l].spines[ln].set_linewidth(1)
            fig.canvas.draw()


def snln2():
    if SW_global.gdaxes == key_c:
        for ln in ['top','right','left','bottom']:
            guideline_axes[l].spines[ln].set_linewidth(1.5)
            fig.canvas.draw()


def snln3():
    if SW_global.gdaxes == key_c:
        for ln in ['top','right','left','bottom']:
            guideline_axes[l].spines[ln].set_linewidth(2)
            fig.canvas.draw()


def snln6():
    if SW_global.gdaxes == key_c:
        for ln in ['top','right','left','bottom']:
            guideline_axes[l].spines[ln].set_linewidth(2.5)
            fig.canvas.draw()


def guidelines_toparea_submenu():
    SW_global.guidelines_toparea = 1
    if SW_global.gdaxes == key_c:
        default_guideline(guideline_axes[l])
    fig.canvas.draw()
def guidelines_middlearea_submenu():
    SW_global.guidelines_middlearea = 1
    if SW_global.gdaxes == key_c:
        default_guideline(guideline_axes[l])
    fig.canvas.draw()
def guidelines_descenderarea_submenu():
    SW_global.guidelines_descenderarea = 1
    if SW_global.gdaxes == key_c:
        default_guideline(guideline_axes[l])
    fig.canvas.draw()

def guideline_del_asenderline():
    if SW_global.gdaxes == key_c:
        guideline_axes[l].lines[0].set_visible(False)
    fig.canvas.draw()

def guideline_del_middleline():
    if SW_global.gdaxes == key_c:
        guideline_axes[l].lines[1].set_visible(False)
    fig.canvas.draw()

def guideline_del_baseline():
    if SW_global.gdaxes == key_c:
        guideline_axes[l].lines[2].set_visible(False)
    fig.canvas.draw()

def guideline_del_descenderline():
    if SW_global.gdaxes == key_c:
        guideline_axes[l].lines[3].set_visible(False)
    fig.canvas.draw()

def show_special_character():
    if SW_global.axx == 1:
        x1,y1 = Insert_Special_Symbol.manuscript_special_1()
        n = len(x1)
        for i in range(n):
            guideline_axes[l].plot(x1[i], y1[i], color='black', linewidth=0.7, linestyle=":")
    elif SW_global.axx == 2:
        x2,y2 = Insert_Special_Symbol.manuscript_special_2()
        n = len(x2)
        for i in range(n):
            guideline_axes[l].plot(x2[i], y2[i], color='black', linewidth=0.7, linestyle=":")
    elif SW_global.axx == 3:
        x3,y3 = Insert_Special_Symbol.manuscript_special_3()
        n = len(x3)
        for i in range(n):
            guideline_axes[l].plot(x3[i], y3[i], color='black', linewidth=0.7, linestyle=":")
    elif SW_global.axx == 4:
        x4,y4 = Insert_Special_Symbol.manuscript_special_4()
        n = len(x4)
        for i in range(n):
            guideline_axes[l].plot(x4[i], y4[i], color='black', linewidth=0.7, linestyle=":")
    elif SW_global.axx == 5:
        x5,y5 = Insert_Special_Symbol.manuscript_special_5()
        n = len(x5)
        for i in range(n):
            guideline_axes[l].plot(x5[i], y5[i], color='black', linewidth=0.7, linestyle=":")
    fig.canvas.draw()

def insert_special_character():
    inst_spl_chr_wp = Toplevel(SW_Main_UI)
    inst_spl_chr_wp.geometry("630x400+250+100")
    inst_spl_chr_wp.title("Insert Special Characters")
    inst_spl_chr_wp.resizable(height=FALSE, width=FALSE)
    frame1 = Frame(inst_spl_chr_wp, width=500, height=300, bd=2, highlightbackground="black", highlightcolor="black",highlightthickness=1)
    frame1.pack(padx=5, pady=20)

    frame2 = Frame(inst_spl_chr_wp, width=450, height=100)
    frame2.pack(padx=4, pady=2)

    frame2child1 = tk.Frame(frame2, height=100, width=450)
    frame2child1.grid(row=0, column=0, padx=6)

    save_button = ttk.Button(frame2child1, text="Insert", command=show_special_character)
    save_button.grid(row=1, column=0, ipadx=7, padx=10, pady=5)

    cancel_button = ttk.Button(frame2child1, text="Cancel", command = inst_spl_chr_wp.destroy)
    cancel_button.grid(row=1, column=1, ipadx=7, padx=10, pady=5)


    fig1 = plt.figure()
    fig1.set_size_inches(6, 3)

    axs = fig1.subplots(7, 16)

    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
    fig1.tight_layout(pad=0)

    a = 0
    for a in range(0,16):
        img = plt.imread('./SpChar/'+str(a)+'.jpg')
        axs[0,a].imshow(img)

    def onclick_select(event):
        if event.inaxes == axs[0,0]:
            SW_global.axx = 1
        elif event.inaxes == axs[0,1]:
            SW_global.axx = 2
        elif event.inaxes == axs[0,2]:
            SW_global.axx = 3
        elif event.inaxes == axs[0,3]:
            SW_global.axx = 4
        elif event.inaxes == axs[0,4]:
            SW_global.axx = 5
        elif event.inaxes == axs[0,5]:
            SW_global.axx = 6
        elif event.inaxes == axs[0,6]:
            SW_global.axx = 7
        elif event.inaxes == axs[0,7]:
            SW_global.axx = 8
        elif event.inaxes == axs[0,8]:
            SW_global.axx = 9
        elif event.inaxes == axs[0,9]:
            SW_global.axx = 10
        elif event.inaxes == axs[0,10]:
            SW_global.axx = 11
        elif event.inaxes == axs[0,11]:
            SW_global.axx = 12
        elif event.inaxes == axs[0,12]:
            SW_global.axx = 13
        elif event.inaxes == axs[0,13]:
            SW_global.axx = 14
        elif event.inaxes == axs[0,14]:
            SW_global.axx = 15
        elif event.inaxes == axs[0,15]:
            SW_global.axx = 16

    canvas = FigureCanvasTkAgg(fig1, master=frame1)
    canvas.get_tk_widget().grid(row=0, column=0)
    print("This is checkpoint4")

    fig1.canvas.mpl_connect("button_press_event",onclick_select)
    fig1.canvas.mpl_connect('button_press_event',onclick2)
    fig1.canvas.mpl_connect('button_release_event',onrelease)


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def popup(event):
    if SW_global.figvalue == False and SW_global.gdaxes == key_c:
        rightclick_menu.post(event.x_root, event.y_root)
    elif SW_global.figvalue == True:
        rightclick_outermenu.post(event.x_root, event.y_root)
        SW_global.figvalue = False
##    SW_global.gdaxes = 0

def popupFocusOut(event=None):
    rightclick_menu.unpost()
    rightclick_outermenu.unpost()

##    SW_global.gdaxes = 0

def motion(event):
    global click_x, click_y
    click_x, click_y = event.x_root, event.y_root

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> letter_shading_Property_window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
v = tk.IntVar()
v.set(0)

def ShowChoice():
    print(v.get())

def letter_shading_option_mw():
    letter_shading = Toplevel(SW_Main_UI)
    letter_shading.wm_title("Letter Shading")
    letter_shading.geometry("380x150+200+250")
    letter_shading.resizable(width=False, height=False)
    letter_shading.wm_transient(SW_Main_UI)
    letter_shading_labelframe = LabelFrame(letter_shading, text="Shading")
    letter_shading_labelframe.pack(side=LEFT, fill="both", pady=15, padx=6)

    # initializing the choice
    shading_option = [("Set by shading property bar button"),
                      ("First letter of every line Black"),
                      ("First letter of every word Black"),
                      ("First letter of every-other word black"),
                      ("Entire first word of every line black")
                      ]
    for val, shading_option in enumerate(shading_option):
        shading_option_rb = tk.Radiobutton(letter_shading_labelframe, text=shading_option, variable=v, value=val)
        shading_option_rb.pack(anchor=W)

    letter_shading_button_ok = ttk.Button(letter_shading, text="OK", command=ShowChoice)
    letter_shading_button_ok.pack(side=TOP, padx=5, pady=18)
    letter_shading_button_cancel = ttk.Button(letter_shading, text="Cancel", command=letter_shading.destroy)
    letter_shading_button_cancel.pack(side=TOP, padx=5)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Letter_Shadding <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def common_help_function_for_letter_shadding():
    global alp
    # coping letter
    temp_recent_input_list = []
    temp_recent_input_list.extend(delete_list)

    while len(delete_list) > 0:
        len1 = len(SW_global.letters_already_written)
        len2 = len1 - 1
        srt_loop = SW_global.letters_already_written[len2 - 1]
        end_loop = SW_global.letters_already_written[len2]
        for i in range(srt_loop, end_loop):
            guideline_axes[l].lines[i].set_visible(False)

        if len(SW_global.letters_already_written) != 0:
            del SW_global.letters_already_written[len1 - 1]
            del SW_global.letters_already_written[len1 - 2]

            last_input_len = len(delete_list)
            last_glyph = delete_list[last_input_len - 1]
            del delete_list[last_input_len - 1]
            l12 = len(kern_value_array)
            del kern_value_array[l12 - 1]

    fig.canvas.draw()

    # clearing List
    SW_global.recent_input_list.clear()
    kern_value_array.clear()
    SW_global.letters_already_written.clear()
    delete_list.clear()

    # making kern value 0 for fresh starting
    SW_global.kern_list.insert(0, 0)
    kern_value_array.insert(0, 0)

    for itr in range(len(temp_recent_input_list)):
        length12 = len(SW_global.recent_input_list)
        user_input = temp_recent_input_list[itr]
        x_max = manuscript.x_max[user_input]
        kern_x = SW_global.kern_list[0]
        skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
        if user_input in skip_list:
            c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
        else:
            x,y= manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
            c1,c2=font_check(x,y)
        c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, kern_x)
        kern_x = SW_global.kern_list[0] + x_max + 300
        SW_global.kern_list.insert(0, kern_x)

        kern_counter = len(kern_value_array)
        kern_value_array.insert(kern_counter, kern_x)
        SW_global.recent_input_list.insert(length12, user_input)
        delete_list.insert(length12, user_input)
        init_enrty_pos = len(SW_global.letters_already_written)
        inti_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)

        if draw_type == 1:
            my_draw_shadding(c1, c2)
        else:
            n = len(c1)
            for i in range(n):
                my_draw_shadding1(c1[i], c2[i], i)

        final_enrty_pos = len(SW_global.letters_already_written)
        final_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
    fig.canvas.draw()
    temp_recent_input_list.clear()
    print("This check point 5")
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event',onclick2)
    fig.canvas.mpl_connect('button_release_event',onrelease)

def letter_shadding_25():
    global init_letter_pos, final_letter_pos
    global letter_shadding_on_off, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_shadding_on_off = 1
    alp = 0.3
    temp_alp = alp
    if letter_dot_density_no_dot_on_off:
        alp = 0
    common_help_function_for_letter_shadding()

def letter_shadding_50():
    global init_letter_pos, final_letter_pos, startdot_flag_pos
    global letter_shadding_on_off, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_shadding_on_off = 1
    alp = 0.5
    temp_alp = alp
    if letter_dot_density_no_dot_on_off:
        alp = 0
    common_help_function_for_letter_shadding()

def letter_shadding_75():
    global init_letter_pos, final_letter_pos, startdot_flag_pos
    global letter_shadding_on_off, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_shadding_on_off = 1
    alp = 0.7
    temp_alp = alp
    if letter_dot_density_no_dot_on_off:
        alp = 0
    common_help_function_for_letter_shadding()

def letter_shadding_100():
    global init_letter_pos, final_letter_pos, startdot_flag_pos
    global letter_shadding_on_off, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_shadding_on_off = 1
    alp = 1
    temp_alp = alp
    if letter_dot_density_no_dot_on_off:
        alp = 0
    common_help_function_for_letter_shadding()

def my_draw_shadding(c1, c2):
    global alp, d1, d2
    global color_letter_features_on_off
    # global letter_dot_density_no_dot_on_off
    # if letter_dot_density_no_dot_on_off:
    #     guideline_axes[l].plot(c1, c2, color='red', linewidth=0.7, dashes=(d1, d2), alpha=alp)
    # else:
    #     guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
    if color_letter_features_on_off:
        guideline_axes[l].plot(c1, c2, color='red', linewidth=0.7, dashes=(d1, d2), alpha=alp)
    else:
        guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)


def my_draw_shadding1(c1, c2, i):
    global alp, d1, d2
    global color_letter_features_on_off
    if color_letter_features_on_off:
        if i == 0:
            guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
        if i == 1:
            guideline_axes[l].plot(c1, c2, color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
        if i == 2:
            guideline_axes[l].plot(c1, c2, color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
        if i == 3:
            guideline_axes[l].plot(c1, c2, color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
    else:
        guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> letter_dot_density_Property_window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
v1 = tk.IntVar()
v1.set(0)

def ShowChoice_1():
    print(v.get())

def letter_dot_density_option_mw():
    letter_dot_density = Toplevel(SW_Main_UI)
    letter_dot_density.wm_title("Letter Dot Density")
    letter_dot_density.geometry("380x150+200+250")
    letter_dot_density.resizable(width=False, height=False)
    letter_dot_density.wm_transient(SW_Main_UI)
    letter_dot_density_labelframe = LabelFrame(letter_dot_density, text="Dot Density")
    letter_dot_density_labelframe.pack(side=LEFT, fill="both", pady=15, padx=6)

    # initializing the choice
    dot_density_option = [("Set by shading property bar button"),
                          ("First letter of every line Black"),
                          ("First letter of every word Black"),
                          ("First letter of every-other word black"),
                          ("Entire first word of every line black")
                          ]
    for val1, dot_density_option in enumerate(dot_density_option):
        dot_density_option_rb = tk.Radiobutton(letter_dot_density_labelframe, text=dot_density_option, variable=v1,
                                               value=val1)
        dot_density_option_rb.pack(anchor=W)

    letter_dot_density_button_ok = ttk.Button(letter_dot_density, text="OK", command=ShowChoice_1)
    letter_dot_density_button_ok.pack(side=TOP, padx=5, pady=18)
    letter_dot_density_button_cancel = ttk.Button(letter_dot_density, text="Cancel", command=letter_dot_density.destroy)
    letter_dot_density_button_cancel.pack(side=TOP, padx=5)

letter_dot_density_on_off = 0
letter_dot_density_no_dot_on_off = 0
d1, d2 = 3, 4
temp_alp = 1

def common_help_function_letter_dot_density(d1, d2):
    global letter_dot_density_on_off, alp
    temp_recent_input_list = []
    temp_recent_input_list.clear()
    temp_recent_input_list.extend(delete_list)
    while len(delete_list) > 0:
        len1 = len(SW_global.letters_already_written)
        len2 = len1 - 1
        srt_loop = SW_global.letters_already_written[len2 - 1]
        end_loop = SW_global.letters_already_written[len2]
        for i in range(srt_loop, end_loop):
            guideline_axes[l].lines[i].set_visible(False)

        if len(SW_global.letters_already_written) != 0:
            del SW_global.letters_already_written[len1 - 1]
            del SW_global.letters_already_written[len1 - 2]
            last_input_len = len(delete_list)
            last_glyph = delete_list[last_input_len - 1]
            del delete_list[last_input_len - 1]
            l12 = len(kern_value_array)
            del kern_value_array[l12 - 1]
    fig.canvas.draw()

    # clearing List
    SW_global.recent_input_list.clear()
    kern_value_array.clear()
    SW_global.letters_already_written.clear()
    delete_list.clear()

    # making kern value 0 for fresh starting
    SW_global.kern_list.insert(0, 0)
    kern_value_array.insert(0, 0)

    for itr in range(len(temp_recent_input_list)):
        length12 = len(SW_global.recent_input_list)
        user_input = temp_recent_input_list[itr]
        x_max = manuscript.x_max[user_input]
        kern_x = SW_global.kern_list[0]
        #himalaya
        skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
        if user_input in skip_list:
            c1,c2=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
        else:
            x,y = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
            c1,c2=font_check(x,y)
        c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, kern_x)
        kern_x = SW_global.kern_list[0] + x_max + 300
        SW_global.kern_list.insert(0, kern_x)

        kern_counter = len(kern_value_array)
        kern_value_array.insert(kern_counter, kern_x)
        SW_global.recent_input_list.insert(length12, user_input)
        delete_list.insert(length12, user_input)
        init_enrty_pos = len(SW_global.letters_already_written)
        inti_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)

        if draw_type == 1:
            my_draw_shadding(c1, c2)
        else:
            n = len(c1)
            for i in range(n):
                letter_dot_density_draw_function(c1[i], c2[i], i, d1, d2)

        final_enrty_pos = len(SW_global.letters_already_written)
        final_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
    fig.canvas.draw()

    temp_recent_input_list.clear()
    print("checkpoint6")
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event',onclick2)
    fig.canvas.mpl_connect('button_release_event',onrelease)


def letter_dot_density_no_dot():
    global d1, d2, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_dot_density_no_dot_on_off = 1
    d1, d2 = 3, 4
    temp_alp = alp
    alp = 0
    common_help_function_letter_dot_density(d1, d2)

def letter_dot_density_25():
    global d1, d2, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_dot_density_no_dot_on_off = 0
    d1, d2 = 3, 9
    alp = temp_alp
    common_help_function_letter_dot_density(d1, d2)

def letter_dot_density_50():
    global d1, d2, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_dot_density_no_dot_on_off = 0
    d1, d2 = 3, 6
    alp = temp_alp
    common_help_function_letter_dot_density(d1, d2)

def letter_dot_density_75():
    global d1, d2, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_dot_density_no_dot_on_off = 0
    alp = temp_alp
    d1, d2 = 3, 3
    common_help_function_letter_dot_density(d1, d2)

def letter_dot_density_100():
    global d1, d2, alp, temp_alp, letter_dot_density_no_dot_on_off
    letter_dot_density_no_dot_on_off = 0
    d1, d2 = 3, 0
    alp = temp_alp
    common_help_function_letter_dot_density(d1, d2)

def letter_dot_density_draw_function(c1, c2, i, d1, d2):
    global alp
    global letter_dot_density_no_dot_on_off
    global color_letter_features_on_off
    # if letter_dot_density_no_dot_on_off:
    #     if i == 0:
    #         guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
    #     if i == 1:
    #         guideline_axes[l].plot(c1, c2, color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
    #     if i == 2:
    #         guideline_axes[l].plot(c1, c2, color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
    #     if i == 3:
    #         guideline_axes[l].plot(c1, c2, color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
    # else:
    #     guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

    if color_letter_features_on_off:
        if i == 0:
            guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
        if i == 1:
            guideline_axes[l].plot(c1, c2, color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
        if i == 2:
            guideline_axes[l].plot(c1, c2, color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
        if i == 3:
            guideline_axes[l].plot(c1, c2, color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
    else:
        guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Guideline Control Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
v9 = tk.IntVar()  # guidelines_menu_wtp variable
v9.set(1)

v3 = tk.IntVar()  # guidelines_menu_wtp variable
v3.set(0)

v8 = tk.IntVar()  # guidelines_menu_wtp variable
v8.set(2)

v5 = tk.IntVar()  # guidelines_menu_wtp variable
v5.set(0)

v6 = tk.IntVar()  # guidelines_menu_wtp variable
v6.set(1)

v7 = tk.IntVar()  # guidelines_menu_wtp variable
v7.set(0)
v10 = tk.IntVar()  # guidelines_menu_wtp variable
v10.set(1)

v11 = tk.IntVar()  # guidelines_menu_wtp variable
v11.set(0)

def on_click_guide_clr_change_help_function_top_0():
    SW_global.getvar1 = 1
    SW_global.get_top_density = 0
    guideline_color_change()


def on_click_guide_clr_change_help_function_top_1():
    SW_global.getvar1 = 1
    SW_global.get_top_density = 1
    guideline_color_change()


def on_click_guide_clr_change_help_function_top_2():
    SW_global.getvar1 = 1
    SW_global.get_top_density = 2
    guideline_color_change()


def on_click_guide_clr_change_help_function_top_3():
    SW_global.getvar1 = 1
    SW_global.get_top_density = 3
    guideline_color_change()


def on_click_guide_clr_change_help_function_middle_0():
    SW_global.getvar2 = 2
    SW_global.get_middle_density = 0
    guideline_color_change()


def on_click_guide_clr_change_help_function_middle_1():
    SW_global.getvar2 = 2
    SW_global.get_middle_density = 1
    guideline_color_change()


def on_click_guide_clr_change_help_function_middle_2():
    SW_global.getvar2 = 2
    SW_global.get_middle_density = 2
    guideline_color_change()


def on_click_guide_clr_change_help_function_middle_3():
    SW_global.getvar2 = 2
    SW_global.get_middle_density = 3
    guideline_color_change()


def on_click_guide_clr_change_help_function_base_0():
    SW_global.getvar3 = 1
    SW_global.get_base_density = 0
    guideline_color_change()


def on_click_guide_clr_change_help_function_base_1():
    SW_global.getvar3 = 1
    SW_global.get_base_density = 1
    guideline_color_change()


def on_click_guide_clr_change_help_function_base_2():
    SW_global.getvar3 = 1
    SW_global.get_base_density = 2
    guideline_color_change()


def on_click_guide_clr_change_help_function_base_3():
    SW_global.getvar3 = 1
    SW_global.get_base_density = 3
    guideline_color_change()


def on_click_guide_clr_change_help_function_descender_0():
    SW_global.getvar4 = 1
    SW_global.get_descender_density = 0
    guideline_color_change()


def on_click_guide_clr_change_help_function_descender_1():
    SW_global.getvar4 = 1
    SW_global.get_descender_density = 1
    guideline_color_change()


def on_click_guide_clr_change_help_function_descender_2():
    SW_global.getvar4 = 1
    SW_global.get_descender_density = 2
    guideline_color_change()


def on_click_guide_clr_change_help_function_descender_3():
    SW_global.getvar4 = 1
    SW_global.get_descender_density = 3
    guideline_color_change()


def guidelines_menu_wtp():
    guidelines_wtp = Toplevel(SW_Main_UI)
    guidelines_wtp.wm_title("Guidelines Styles")
    guidelines_wtp.geometry("444x690+500+10")
    guidelines_wtp.resizable(width=False, height=False)
    guidelines_wtp.wm_transient(SW_Main_UI)

    Top_Line = LabelFrame(guidelines_wtp, text="Top Line")
    Top_Line.pack(pady=3, padx=20)

    TpLn_frame = Frame(Top_Line)
    TpLn_frame.pack(side=TOP)

    Top_Line_Line_type = LabelFrame(TpLn_frame, text="Line Type", font=('manuscript', 9))
    Top_Line_Line_type.pack(side=LEFT, ipady=2, ipadx=20, padx=4, pady=2)

    def tpln1():
        if v9.get() == 2:
            print("<< Dashes >>")
            ax1.plot(ascender_x, ascender_y, color='white', linewidth=0.7, dashes=(3, 4))
            fig.canvas.draw()
            SW_global.getvar1 = 2
        elif v9.get() == 1:
            print("<< Solid >>")
            ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.7)
            fig.canvas.draw()
            SW_global.getvar1 = 1
        elif v9.get() == 0:
            print("<< Off Top-Line >>")
            ax1.lines[12].set_visible(False)
            fig.canvas.draw()
            SW_global.getvar1 = 3
        else:
            pass

    line_type_option_tl = [("Off"), ("Solid"), ("Dashed")]
    for val9, line_type_option_tl in enumerate(line_type_option_tl):
        line_type_option_rb_tl = tk.Radiobutton(Top_Line_Line_type, text=line_type_option_tl, variable=v9, value=val9,
                                                font=('manuscript', 9), command=tpln1)
        line_type_option_rb_tl.pack(side="left")

    Line_Color_Line_Color_tl = LabelFrame(TpLn_frame, text="Line Color", font=('manuscript', 9))
    Line_Color_Line_Color_tl.pack(side=LEFT, ipady=6, ipadx=20, padx=4, pady=2)

    Line_Color_Frame_tl = Frame(Line_Color_Line_Color_tl, bd=1, relief=SUNKEN)
    Line_Color_Frame_tl.pack()

    def setBgColor_Tpln():
        (triple, hexstr1) = askcolor()
        SW_global.guidelines_top_color = hexstr1
        if hexstr1:
            Line_Color1.config(bg=SW_global.guidelines_top_color)
            ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)
            fig.canvas.draw()

    Line_Color1 = tk.Button(Line_Color_Frame_tl, bg=SW_global.guidelines_top_color, text='', width=40, command=setBgColor_Tpln)
    Line_Color1.config(font=('times', 4))
    Line_Color1.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Line_Color_Frame_tl, width=10, height=20, image=down_icon, command=setBgColor_Tpln)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    TpLn_frame1 = Frame(Top_Line)
    TpLn_frame1.pack(ipady=8, ipadx=8)
    Tpln_label = Label(TpLn_frame1, text="Guideline Thickness", font=('manuscript', 9))
    Tpln_label.pack(side=LEFT)

    def top_line_density():
        if v3.get() == 0:
            print("<< Normal >>")
            SW_global.get_top_density = 0

        elif v3.get() == 1:
            print("<< Thick >>")
            SW_global.get_top_density = 1

        elif v3.get() == 2:
            print("<< Thicker >>")
            SW_global.get_top_density = 2

        elif v3.get() == 3:
            print("<< Thickest >>")
            SW_global.get_top_density = 3

        else:
            print("Please Choose a Value For Top Line ")


    top_line_option_tl = [("Normal"), ("Thick"), ("Thicker"), ("Thickest")]
    for val3, top_line_option_tl in enumerate(top_line_option_tl):
        top_line_option_rb_tl = tk.Radiobutton(TpLn_frame1, text=top_line_option_tl, variable=v3, value=val3,
                                               font=('manuscript', 9), command=top_line_density)
        top_line_option_rb_tl.pack(side="left")

    Middle_Line = LabelFrame(guidelines_wtp, text="Middle Line", font=('manuscript', 9))
    Middle_Line.pack(padx=20)

    MpLn_frame = Frame(Middle_Line)
    MpLn_frame.pack(side=TOP)

    Middle_Line_Line_type = LabelFrame(MpLn_frame, text="Line Type", font=('manuscript', 9))
    Middle_Line_Line_type.pack(side=LEFT, ipady=2, ipadx=20, padx=4, pady=2)

    def mdln2():
        if v8.get() == 2:
            ax1.plot(median_x, median_y, color='white', linewidth=0.7, dashes=(3, 4))
            fig.canvas.draw()
            SW_global.getvar2 = 2
        elif v8.get() == 1:
            ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linewidth=0.7)
            fig.canvas.draw()
            SW_global.getvar2 = 1
        elif v8.get() == 0:
            ax1.lines[11].set_visible(False)
            fig.canvas.draw()
            SW_global.getvar2 = 3

    line_type_option_ml = [("Off"), ("Solid"), ("Dashed")]
    for val8, line_type_option_ml in enumerate(line_type_option_ml):
        line_type_option_rb_ml = tk.Radiobutton(Middle_Line_Line_type, text=line_type_option_ml, variable=v8,
                                                value=val8, font=('manuscript', 9), command=mdln2)
        line_type_option_rb_ml.pack(side="left")

    Line_Color_Line_Color_ml = LabelFrame(MpLn_frame, text="Line Color", font=('manuscript', 9))
    Line_Color_Line_Color_ml.pack(side=LEFT, ipady=8, ipadx=20, padx=4, pady=2)

    Line_Color_Frame_ml = Frame(Line_Color_Line_Color_ml, bd=1, relief=SUNKEN)
    Line_Color_Frame_ml.pack()

    def setBgColor_Mpln():
        (triple, hexstr2) = askcolor()
        SW_global.guidelines_middle_color = hexstr2
        if hexstr2:
            Line_Color2.config(bg=SW_global.guidelines_middle_color)
            lineax2 = ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linestyle=':', linewidth=0.5)
            fig.canvas.draw()

    Line_Color2 = tk.Button(Line_Color_Frame_ml, bg=SW_global.guidelines_middle_color, text='', width=40, command=setBgColor_Mpln)
    Line_Color2.config(font=('times', 4))
    Line_Color2.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Line_Color_Frame_ml, width=10, height=20, image=down_icon, command=setBgColor_Mpln)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    MpLn_frame1 = Frame(Middle_Line)
    MpLn_frame1.pack(ipady=8, ipadx=8)
    Mpln_label = Label(MpLn_frame1, text="Guideline Thickness", font=('manuscript', 9))
    Mpln_label.pack(side=LEFT)

    def middle_line_density():
        if v5.get() == 0:
            print("<< Normal >>")
            SW_global.get_middle_density = 0

        elif v5.get() == 1:
            print("<< Thick >>")
            SW_global.get_middle_density = 1

        elif v5.get() == 2:
            print("<< Thicker >>")
            SW_global.get_middle_density = 2

        elif v5.get() == 3:
            print("<< Thickest >>")
            SW_global.get_middle_density = 3

        else:
            print("Please Choose a Value For Middle Line ")

    top_line_option_ml = [("Normal"), ("thick"), ("Thicker"), ("Thickest")]
    for val5, top_line_option_ml in enumerate(top_line_option_ml):
        top_line_option_rb_ml = tk.Radiobutton(MpLn_frame1, text=top_line_option_ml, variable=v5, value=val5,
                                               font=('manuscript', 9), command=middle_line_density)
        top_line_option_rb_ml.pack(side="left")

    Base_Line = LabelFrame(guidelines_wtp, text="Base Line", font=('manuscript', 9))
    Base_Line.pack(padx=20)

    BpLn_frame = Frame(Base_Line)
    BpLn_frame.pack(side=TOP)

    Base_Line_Line_type = LabelFrame(BpLn_frame, text="Line Type", font=('manuscript', 9))
    Base_Line_Line_type.pack(side=LEFT, ipady=2, ipadx=20, padx=4, pady=2)

    def bsln3():
        if v6.get() == 2:
            ax1.plot(base_x, base_y, color='white', linewidth=0.7, dashes=(3, 4))
            fig.canvas.draw()
            SW_global.getvar3 = 2
        elif v6.get() == 1:
            ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.7)
            fig.canvas.draw()
            SW_global.getvar3 = 1
        elif v6.get() == 0:
            ax1.lines[9].set_visible(False)
            fig.canvas.draw()
            SW_global.getvar3 = 3

    line_type_option_bl = [("Off"), ("Solid"), ("Dashed")]
    for val6, line_type_option_bl in enumerate(line_type_option_bl):
        line_type_option_rb_bl = tk.Radiobutton(Base_Line_Line_type, text=line_type_option_bl, variable=v6, value=val6,
                                                font=('manuscript', 9), command=bsln3)
        line_type_option_rb_bl.pack(side="left")

    Line_Color_Line_Color_bl = LabelFrame(BpLn_frame, text="Line Color", font=('manuscript', 9))
    Line_Color_Line_Color_bl.pack(side=LEFT, ipady=8, ipadx=20, padx=4, pady=2)

    Line_Color_Frame_bl = Frame(Line_Color_Line_Color_bl, bd=1, relief=SUNKEN)
    Line_Color_Frame_bl.pack()

    def setBgColor_Bpln():
        (triple, hexstr3) = askcolor()
        SW_global.guidelines_base_color = hexstr3
        if hexstr3:
            Line_Color3.config(bg=SW_global.guidelines_base_color)
            lineax1 = ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
            fig.canvas.draw()

    Line_Color3 = tk.Button(Line_Color_Frame_bl, bg=SW_global.guidelines_base_color, text='', width=40, command=setBgColor_Bpln)
    Line_Color3.config(font=('times', 4))
    Line_Color3.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Line_Color_Frame_bl, width=10, height=20, image=down_icon, command=setBgColor_Bpln)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    BpLn_frame1 = Frame(Base_Line)
    BpLn_frame1.pack(ipady=8, ipadx=8)
    Bpln_label = Label(BpLn_frame1, text="Guideline Thickness")
    Bpln_label.pack(side=LEFT)

    def base_line_density():
        if v7.get() == 0:
            print("<< Normal >>")
            SW_global.get_base_density = 0

        elif v7.get() == 1:
            print("<< Thick >>")
            SW_global.get_base_density = 1

        elif v7.get() == 2:
            print("<< Thicker >>")
            SW_global.get_base_density = 2

        elif v7.get() == 3:
            print("<< Thickest >>")
            SW_global.get_base_density = 3

        else:
            print("Please Choose a Value For Base Line ")

    top_line_option_bl = [("Normal"), ("thick"), ("Thicker"), ("Thickest")]
    for val7, top_line_option_bl in enumerate(top_line_option_bl):
        top_line_option_rb_bl = tk.Radiobutton(BpLn_frame1, text=top_line_option_bl, variable=v7, value=val7,
                                               font=('manuscript', 9), command=base_line_density)
        top_line_option_rb_bl.pack(side="left")

    Bottom_Line = LabelFrame(guidelines_wtp, text="Bottom Line(Descender)", font=('manuscript', 9))
    Bottom_Line.pack(padx=20)

    BtLn_frame = Frame(Bottom_Line)
    BtLn_frame.pack(side=TOP)

    Bottom_Line_Line_type = LabelFrame(BtLn_frame, text="Line Type", font=('manuscript', 9))
    Bottom_Line_Line_type.pack(side=LEFT, ipady=2, ipadx=20, padx=4, pady=2)

    def desln4():
        if v10.get() == 2:
            ax1.plot(descender_x, descender_y, color='white', linewidth=0.7, dashes=(3, 4))
            fig.canvas.draw()
            SW_global.getvar4 = 2
        elif v10.get() == 1:
            ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.7)
            fig.canvas.draw()
            SW_global.getvar4 = 1
        elif v10.get() == 0:
            ax1.lines[8].set_visible(False)
            fig.canvas.draw()
            SW_global.getvar4 = 3

    line_type_option_btl = [("Off"), ("Solid"), ("Dashed")]
    for val10, line_type_option_btl in enumerate(line_type_option_btl):
        line_type_option_rb_btl = tk.Radiobutton(Bottom_Line_Line_type, text=line_type_option_btl, variable=v10,
                                                 value=val10, font=('manuscript', 9), command=desln4)
        line_type_option_rb_btl.pack(side="left")

    Line_Color_Line_Color_btl = LabelFrame(BtLn_frame, text="Line Color", font=('manuscript', 9))
    Line_Color_Line_Color_btl.pack(side=LEFT, ipady=8, ipadx=20, padx=4, pady=2)

    Line_Color_Frame_btl = Frame(Line_Color_Line_Color_btl, bd=1, relief=SUNKEN)
    Line_Color_Frame_btl.pack()

    def setBgColor_Btln():
        (triple, hexstr4) = askcolor()
        SW_global.guidelines_bottom_color = hexstr4
        if hexstr4:
            Line_Color4.config(bg=SW_global.guidelines_bottom_color)
            lineax3 = ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
            fig.canvas.draw()

    Line_Color4 = tk.Button(Line_Color_Frame_btl, bg=SW_global.guidelines_bottom_color, text='', width=40,
                            command=setBgColor_Btln)
    Line_Color4.config(font=('times', 4))
    Line_Color4.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Line_Color_Frame_btl, width=10, height=20, image=down_icon, command=setBgColor_Btln)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    BtLn_frame1 = Frame(Bottom_Line)
    BtLn_frame1.pack(ipady=8, ipadx=8)
    Btln_label = Label(BtLn_frame1, text="Guideline Thickness", font=('manuscript', 9))
    Btln_label.pack(side=LEFT)

    def descender_line_density():
        if v11.get() == 0:
            print("<< Normal >>")
            SW_global.get_descender_density = 0

        elif v11.get() == 1:
            print("<< Thick >>")
            SW_global.get_descender_density = 1

        elif v11.get() == 2:
            print("<< Thicker >>")
            SW_global.get_descender_density = 2

        elif v11.get() == 3:
            print("<< Thickest >>")
            SW_global.get_descender_density = 3
        else:
            print("Please Choose a Value For Descender Line ")

    top_line_option_btl = [("Normal"), ("thick"), ("Thicker"), ("Thickest")]
    for val11, top_line_option_btl in enumerate(top_line_option_btl):
        top_line_option_rb_btl = tk.Radiobutton(BtLn_frame1, text=top_line_option_btl, variable=v11, value=val11,
                                                font=('manuscript', 9), command=descender_line_density)
        top_line_option_rb_btl.pack(side="left")

    ExampleFrame = Frame(guidelines_wtp, width=440)
    ExampleFrame.pack(anchor=W)

    Examplelabel = Label(ExampleFrame, text="Example", font=('manuscript', 9))
    Examplelabel.pack(padx=20)

    FigexFrame = Frame(guidelines_wtp, width=440, bd=2, highlightbackground="black", highlightcolor="black",
                       highlightthickness=1)
    FigexFrame.pack(padx=20)

    fig = plt.figure()
    ax1 = fig.add_axes([0, 0.1, 1, 0.8])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(4, 1)

    base_x = [0, (1500 * 9)]
    base_y = [0, 0]
    median_x = [0, (1500 * 9)]
    median_y = [757, 757]
    descender_x = [0, (1500 * 9)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * 9)]
    ascender_y = [1500, 1500]

    x1 = [[0, 752, 1500], [248, 1251]]
    y1 = [[0, 1501, 0], [496, 495]]
    kern_fix = 1800
    x2 = [[kern_fix + 754, kern_fix + 754],
          [kern_fix + 754, kern_fix + 754],
          [kern_fix + 377], [kern_fix + 0, kern_fix + 0, kern_fix + 222, kern_fix + 377],
          [kern_fix + 377, kern_fix + 221, kern_fix + 0, kern_fix + 0],
          [kern_fix + 755, kern_fix + 755, kern_fix + 640, kern_fix + 528, kern_fix + 377],
          [kern_fix + 377, kern_fix + 528, kern_fix + 755, kern_fix + 755]]
    y2 = [[375, 749],
          [0, 375],
          [749],
          [375, 530, 749, 749],
          [0, 0, 219, 375],
          [376, 530, 641, 749, 749],
          [0, 0, 221, 376]]

    n = len(x1)
    m = len(x2)
    for i in range(n):
        ax1.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
    for j in range(m):
        ax1.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')

    if SW_global.stokearrow_on_off == 1:
        x4 = [[1031, 675, 1031], [1031, 925], [925, 1031], [925, 925],

              [255], [468, 255], [363, 241],

              [255, 363], [241, 255], [1256, 1273], [1039, 1256],

              [1256], [1141, 1256], [1273, 1141],

              [940, 1021, 1021, 940, 940, 1021], [543, 543],

              [492, 572, 572, 492], [572, 572, 492]]

        y4 = [[651, 650, 651], [651, 723], [576, 651], [723, 576], [825], [1237, 825], [872, 945], [825, 872],

              [945, 825], [823, 953], [1216, 823], [823], [879, 823], [953, 879],

              [1462, 1462, 1382, 1382, 1302, 1302], [1461, 1301], [733, 733, 653, 653], [653, 572, 572]]

        x3 = [[kern_fix + 884], [kern_fix + 885, kern_fix + 884],
              [kern_fix + 962, kern_fix + 815], [kern_fix + 884, kern_fix + 962], [kern_fix + 815, kern_fix + 884],
              [kern_fix + 129, kern_fix + 179, kern_fix + 381, kern_fix + 469, kern_fix + 604, kern_fix + 619],
              [kern_fix + 96, kern_fix + 129, kern_fix + 228],
              [kern_fix + 228, kern_fix + 96],
              [kern_fix + 838, kern_fix + 919, kern_fix + 919, kern_fix + 838, kern_fix + 838, kern_fix + 919],
              [kern_fix + 521, kern_fix + 521]]
        y3 = [[124], [485, 124], [213, 213], [124, 213], [213, 124], [404, 641, 641, 641, 528, 445], [513, 404, 460],
              [460, 513], [735, 735, 655, 655, 575, 575], [454, 294]]

        k = len(x3)
        l = len(x4)
        for e in range(l):
            ax1.plot(x4[e], y4[e], color=SW_global.stokearrow_color_var, linewidth=1)
        for f in range(k):
            ax1.plot(x3[f], y3[f], color=SW_global.stokearrow_color_var, linewidth=1)

    if SW_global.startdot_on_off == 1:
        ax1.plot(752, 1501, marker='.', color=SW_global.startdot_color)
        ax1.plot(kern_fix + 754, 375, marker='.', color=SW_global.startdot_color)

    if SW_global.decisiondot_on_off == 1:
        for i in range(n):
            ax1.scatter(x1[i], y1[i], color=SW_global.decisiondot_color, marker='.')
    if SW_global.connectdot_on_off == 1:
        for i in range(n):
            ax1.plot(x1[i], y1[i], color=SW_global.SW_global.connectingdot_color_var, linewidth=0.5)
        for j in range(m):
            ax1.plot(x2[j], y2[j], color=SW_global.SW_global.connectingdot_color_var, linewidth=0.5)

    if SW_global.guidelines_toparea == 1:
        ax1.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea, alpha=0.4)
    if SW_global.guidelines_middlearea == 1:
        ax1.axhspan(25, 730, facecolor=SW_global.guidelines_background_color_middlearea, alpha=0.4)
    if SW_global.guidelines_descenderarea == 1:
        ax1.axhspan(-730, -20, facecolor=SW_global.guidelines_background_color_descenderarea, alpha=0.4)

    if SW_global.getvar1 == 2:
        ax1.plot(ascender_x, ascender_y, color='white', linewidth=0.7, dashes=(3, 4))
    elif SW_global.getvar1 == 1:
        ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.7)
    if SW_global.getvar2 == 2:
        ax1.plot(median_x, median_y, color='white', linewidth=0.7, dashes=(3, 4))
    elif SW_global.getvar2 == 1:
        ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linewidth=0.7)
    fig.canvas.draw()
    if SW_global.getvar3 == 2:
        ax1.plot(base_x, base_y, color='white', linewidth=0.7, dashes=(3, 4))
    elif SW_global.getvar3 == 1:
        ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.7)
    fig.canvas.draw()
    if SW_global.getvar4 == 2:
        ax1.plot(descender_x, descender_y, color='white', linewidth=0.7, dashes=(3, 4))
    elif SW_global.getvar4 == 1:
        ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.7)
    fig.canvas.draw()

    ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
    ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, dashes=(3, 4), linewidth=0.5)
    ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
    ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=FigexFrame)
    canvas.get_tk_widget().grid(row=0, column=1)

    GuidelineEndFrame = Frame(guidelines_wtp)
    GuidelineEndFrame.pack()

    GuidelineEndchkFrame = Frame(GuidelineEndFrame)
    GuidelineEndchkFrame.grid(row=0, column=0)

    GuidelineEndokcnlFrame = Frame(GuidelineEndFrame)
    GuidelineEndokcnlFrame.grid(row=0, column=1)

    guidelines_chkbx = Checkbutton(GuidelineEndchkFrame, text="Set as Default", variable=var, font=('manuscript', 9))
    guidelines_chkbx.pack(side=LEFT, padx=60, pady=20)

    def guideline_close():
        guidelines_wtp.destroy()
        guideline_color_change()

    guidelines_button_cancel = ttk.Button(GuidelineEndokcnlFrame, text="Cancel", command=guidelines_wtp.destroy)
    guidelines_button_cancel.pack(side=RIGHT, padx=15, pady=2, anchor=N)
    guidelines_button_ok = ttk.Button(GuidelineEndokcnlFrame,
                                      text="OK",
                                      command=guideline_close)
    guidelines_button_ok.pack(side=RIGHT, pady=2, anchor=N)


# Helping Function
def guideline_color_change():

    def top_line_dashes_help_function1(lw=0.7):
        guideline_axes[l].plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=lw, dashes=(3, 4))
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_top_already_applied_array)
        guide_line_top_already_applied_array.insert(length11, top_ending_point)

    def top_line_dashes_help_function2(lw=0.7):
        value_to_delete = guide_line_top_already_applied_array[len111 - 1]
        guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
        guide_line_top_already_applied_array.clear()
        guideline_axes[l].plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=lw, dashes=(3, 4))
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_top_already_applied_array)
        guide_line_top_already_applied_array.insert(length11, top_ending_point)

    def top_line_solid_help_function1(lw=0.7):
        guideline_axes[l].plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=lw)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_top_already_applied_array)
        guide_line_top_already_applied_array.insert(length11, top_ending_point)

    def top_line_solid_help_function2(lw=0.7):
        value_to_delete = guide_line_top_already_applied_array[len111 - 1]
        guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
        guide_line_top_already_applied_array.clear()
        guideline_axes[l].plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=lw)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_top_already_applied_array)
        guide_line_top_already_applied_array.insert(length11, top_ending_point)

    # TOP GuideLine
    if SW_global.getvar1 == 2:  # dashes
        len111 = len(guide_line_top_already_applied_array)
        if len111 == 0:
            if SW_global.get_top_density == 0:
                top_line_dashes_help_function1()

            elif SW_global.get_top_density == 1:
                top_line_dashes_help_function1(lw=1.5)

            elif SW_global.get_top_density == 2:
                top_line_dashes_help_function1(lw=2.3)

            elif SW_global.get_top_density == 3:
                top_line_dashes_help_function1(lw=3)

        else:
            if SW_global.get_top_density == 0:
                top_line_dashes_help_function2()

            elif SW_global.get_top_density == 1:
                top_line_dashes_help_function2(lw=1.5)

            elif SW_global.get_top_density == 2:
                top_line_dashes_help_function2(lw=2.3)

            elif SW_global.get_top_density == 3:
                top_line_dashes_help_function2(lw=3)

    elif SW_global.getvar1 == 1:  # solid
        len111 = len(guide_line_top_already_applied_array)
        if len111 == 0:
            if SW_global.get_top_density == 0:
                top_line_solid_help_function1()

            elif SW_global.get_top_density == 1:
                top_line_solid_help_function1(lw=1.5)

            elif SW_global.get_top_density == 2:
                top_line_solid_help_function1(lw=2.3)

            elif SW_global.get_top_density == 3:
                top_line_solid_help_function1(lw=3)

        else:
            if SW_global.get_top_density == 0:
                top_line_solid_help_function2()

            elif SW_global.get_top_density == 1:
                top_line_solid_help_function2(lw=1.5)

            elif SW_global.get_top_density == 2:
                top_line_solid_help_function2(lw=2.3)

            elif SW_global.get_top_density == 3:
                top_line_solid_help_function2(lw=3)

    elif SW_global.getvar1 == 3:  # off
        len111 = len(guide_line_top_already_applied_array)
        if len111 > 0:
            value_to_delete = guide_line_top_already_applied_array[len111 - 1]
            guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
            guide_line_top_already_applied_array.clear()
        else:
            pass

    def middle_line_dashes_help_function1(lw=0.7):
        guideline_axes[l].plot(median_x, median_y, color=SW_global.guidelines_middle_color, linewidth=lw, dashes=(3, 4))
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_middle_already_applied_array)
        guide_line_middle_already_applied_array.insert(length11, top_ending_point)

    def middle_line_dashes_help_function2(lw=0.7):
        value_to_delete = guide_line_middle_already_applied_array[len111 - 1]
        guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
        guide_line_middle_already_applied_array.clear()
        guideline_axes[l].plot(median_x, median_y, color=SW_global.guidelines_middle_color, linewidth=lw, dashes=(3, 4))
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_middle_already_applied_array)
        guide_line_middle_already_applied_array.insert(length11, top_ending_point)

    def middle_line_solid_help_function1(lw=0.7):
        guideline_axes[l].plot(median_x, median_y, color=SW_global.guidelines_middle_color, linewidth=lw)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_middle_already_applied_array)
        guide_line_middle_already_applied_array.insert(length11, top_ending_point)

    def middle_line_solid_help_function2(lw=0.7):
        value_to_delete = guide_line_middle_already_applied_array[len111 - 1]
        guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
        guide_line_middle_already_applied_array.clear()
        guideline_axes[l].plot(median_x, median_y, color=SW_global.guidelines_middle_color, linewidth=lw)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_middle_already_applied_array)
        guide_line_middle_already_applied_array.insert(length11, top_ending_point)

    # Middle GuideLine
    if SW_global.getvar2 == 2:   # dashes
        len111 = len(guide_line_middle_already_applied_array)
        if len111 == 0:
            if SW_global.get_middle_density == 0:
                middle_line_dashes_help_function1()

            elif SW_global.get_middle_density == 1:
                middle_line_dashes_help_function1(lw=1.5)

            elif SW_global.get_middle_density == 2:
                middle_line_dashes_help_function1(lw=2.3)

            elif SW_global.get_middle_density == 3:
                middle_line_dashes_help_function1(lw=3)

        else:
            if SW_global.get_middle_density == 0:
                middle_line_dashes_help_function2()

            elif SW_global.get_middle_density == 1:
                middle_line_dashes_help_function2(lw=1.5)

            elif SW_global.get_middle_density == 2:
                middle_line_dashes_help_function2(lw=2.3)

            elif SW_global.get_middle_density == 3:
                middle_line_dashes_help_function2(lw=3)

    elif SW_global.getvar2 == 1:   # solid
        len111 = len(guide_line_middle_already_applied_array)
        if len111 == 0:
            if SW_global.get_middle_density == 0:
                middle_line_solid_help_function1()

            elif SW_global.get_middle_density == 1:
                middle_line_solid_help_function1(lw=1.5)

            elif SW_global.get_middle_density == 2:
                middle_line_solid_help_function1(lw=2.3)

            elif SW_global.get_middle_density == 3:
                middle_line_solid_help_function1(lw=3)

        else:
            if SW_global.get_middle_density == 0:
                middle_line_solid_help_function2()

            elif SW_global.get_middle_density == 1:
                middle_line_solid_help_function2(lw=1.5)

            elif SW_global.get_middle_density == 2:
                middle_line_solid_help_function2(lw=2.3)

            elif SW_global.get_middle_density == 3:
                middle_line_solid_help_function2(lw=3)

    elif SW_global.getvar2 == 3:   # off
        len111 = len(guide_line_middle_already_applied_array)
        if len111 > 0:
            value_to_delete = guide_line_middle_already_applied_array[len111 - 1]
            guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
            guide_line_middle_already_applied_array.clear()
        else:
            pass

    def base_line_dashes_help_function1(lw=0.7):
        guideline_axes[l].plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=lw, dashes=(3, 4))
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_base_already_applied_array)
        guide_line_base_already_applied_array.insert(length11, top_ending_point)

    def base_line_dashes_help_function2(lw=0.7):
        value_to_delete = guide_line_base_already_applied_array[len111 - 1]
        guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
        guide_line_base_already_applied_array.clear()
        guideline_axes[l].plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=lw, dashes=(3, 4))
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_base_already_applied_array)
        guide_line_base_already_applied_array.insert(length11, top_ending_point)

    def base_line_solid_help_function1(lw=0.7):
        guideline_axes[l].plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=lw)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_base_already_applied_array)
        guide_line_base_already_applied_array.insert(length11, top_ending_point)

    def base_line_dashes_solid_function2(lw=0.7):
        value_to_delete = guide_line_base_already_applied_array[len111 - 1]
        guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
        guide_line_base_already_applied_array.clear()
        guideline_axes[l].plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=lw)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_base_already_applied_array)
        guide_line_base_already_applied_array.insert(length11, top_ending_point)

    # Base GuideLine
    if SW_global.getvar3 == 2:  # dashes
        len111 = len(guide_line_base_already_applied_array)
        if len111 == 0:
            if SW_global.get_base_density == 0:
                base_line_dashes_help_function1()

            elif SW_global.get_base_density == 1:
                base_line_dashes_help_function1(lw=1.5)

            elif SW_global.get_base_density == 2:
                base_line_dashes_help_function1(lw=2.3)

            elif SW_global.get_base_density == 3:
                base_line_dashes_help_function1(lw=3)

        else:
            if SW_global.get_base_density == 0:
                base_line_dashes_help_function2()

            elif SW_global.get_base_density == 1:
                base_line_dashes_help_function2(lw=1.5)

            elif SW_global.get_base_density == 2:
                base_line_dashes_help_function2(lw=2.3)

            elif SW_global.get_base_density == 3:
                base_line_dashes_help_function2(lw=3)

    elif SW_global.getvar3 == 1:  # solid
        len111 = len(guide_line_base_already_applied_array)
        if len111 == 0:
            if SW_global.get_base_density == 0:
                base_line_solid_help_function1()

            elif SW_global.get_base_density == 1:
                base_line_solid_help_function1(lw=1.5)

            elif SW_global.get_base_density == 2:
                base_line_solid_help_function1(lw=2.3)

            elif SW_global.get_base_density == 3:
                base_line_solid_help_function1(lw=3)

        else:
            if SW_global.get_base_density == 0:
                base_line_dashes_solid_function2()

            elif SW_global.get_base_density == 1:
                base_line_dashes_solid_function2(lw=1.5)

            elif SW_global.get_base_density == 2:
                base_line_dashes_solid_function2(lw=2.3)

            elif SW_global.get_base_density == 3:
                base_line_dashes_solid_function2(lw=3)

    elif SW_global.getvar3 == 3:  # off
        len111 = len(guide_line_base_already_applied_array)
        if len111 > 0:
            value_to_delete = guide_line_base_already_applied_array[len111 - 1]
            guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
            guide_line_base_already_applied_array.clear()
        else:
            pass

    def descender_line_dashes_help_function1(lw=0.7):
        guideline_axes[l].plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=lw, dashes=(3, 4))
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_descender_already_applied_array)
        guide_line_descender_already_applied_array.insert(length11, top_ending_point)

    def descender_line_dashes_help_function2(lw=0.7):
        value_to_delete = guide_line_descender_already_applied_array[len111 - 1]
        guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
        guide_line_descender_already_applied_array.clear()
        guideline_axes[l].plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=lw, dashes=(3, 4))
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_descender_already_applied_array)
        guide_line_descender_already_applied_array.insert(length11, top_ending_point)

    def descender_line_solid_help_function1(lw=0.7):
        guideline_axes[l].plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=lw)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_descender_already_applied_array)
        guide_line_descender_already_applied_array.insert(length11, top_ending_point)

    def descender_line_solid_help_function2(lw=0.7):
        value_to_delete = guide_line_descender_already_applied_array[len111 - 1]
        guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
        guide_line_descender_already_applied_array.clear()
        guideline_axes[l].plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=lw)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_descender_already_applied_array)
        guide_line_descender_already_applied_array.insert(length11, top_ending_point)

    # Last(des) GuideLine
    if SW_global.getvar4 == 2:   # dashes
        len111 = len(guide_line_descender_already_applied_array)
        if len111 == 0:
            if SW_global.get_descender_density == 0:
                descender_line_dashes_help_function1()

            elif SW_global.get_descender_density == 1:
                descender_line_dashes_help_function1(lw=1.5)

            elif SW_global.get_descender_density == 2:
                descender_line_dashes_help_function1(lw=2.3)

            elif SW_global.get_descender_density == 3:
                descender_line_dashes_help_function1(lw=3)

        else:
            if SW_global.get_descender_density == 0:
                descender_line_dashes_help_function2()

            elif SW_global.get_descender_density == 1:
                descender_line_dashes_help_function2(lw=1.5)

            elif SW_global.get_descender_density == 2:
                descender_line_dashes_help_function2(lw=2.3)

            elif SW_global.get_descender_density == 3:
                descender_line_dashes_help_function2(lw=3)

    elif SW_global.getvar4 == 1:   # solid
        len111 = len(guide_line_descender_already_applied_array)
        if len111 == 0:
            if SW_global.get_descender_density == 0:
                descender_line_solid_help_function1()

            elif SW_global.get_descender_density == 1:
                descender_line_solid_help_function1(lw=1.5)

            elif SW_global.get_descender_density == 2:
                descender_line_solid_help_function1(lw=2.3)

            elif SW_global.get_descender_density == 3:
                descender_line_solid_help_function1(lw=3)
        else:
            if SW_global.get_descender_density == 0:
                descender_line_solid_help_function2()

            elif SW_global.get_descender_density == 1:
                descender_line_solid_help_function2(lw=1.5)

            elif SW_global.get_descender_density == 2:
                descender_line_solid_help_function2(lw=2.3)

            elif SW_global.get_descender_density == 3:
                descender_line_solid_help_function2(lw=3)

    elif SW_global.getvar4 == 3:   # off
        len111 = len(guide_line_descender_already_applied_array)
        if len111 > 0:
            value_to_delete = guide_line_descender_already_applied_array[len111 - 1]
            guideline_axes[l].lines[value_to_delete - 1].set_visible(False)
            guide_line_descender_already_applied_array.clear()
        else:
            pass

    fig.canvas.draw()


def default_guideline(dynamic_axes):
    global ax_counter
    global filename, imagebox, arr_img
    global base_x, median_x, descender_x, ascender_x, base_y, median_y, descender_y, ascender_y
    global counter
    # Guideline Axes
    if SW_global.gd_sc1 == True or SW_global.ba_flag == True:
        print("size change working")
        print("@#%$^SW_global.scl : ", SW_global.scl)

        img = plt.imread('icons/apple.jpg')
        dynamic_axes.imshow(img, extent=[0.999, 1, 0.999, 1])
        for ln in ['top', 'right', 'left', 'bottom']:
            dynamic_axes.spines[ln].set_linewidth(0)
            fig.canvas.draw()

        SW_global.kern_list1.clear()
        SW_global.kern_list1.insert(0, 0)
        counter = 0

        base_x = [0, (1500 * SW_global.scl)]
        base_y = [0, 0]
        median_x = [0, (1500 * SW_global.scl)]
        median_y = [757, 757]
        descender_x = [0, (1500 * SW_global.scl)]
        descender_y = [-747, -747]
        ascender_x = [0, (1500 * SW_global.scl)]
        ascender_y = [1510, 1510]

        dynamic_axes.set_position([SW_global.lt_gd_1, SW_global.btm_gd_1, SW_global.wd_gd_1, SW_global.ht_gd_1])

        dynamic_axes.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_top_already_applied_array)
        guide_line_top_already_applied_array.insert(length11, top_ending_point)

        ''' 1st Time Middle GuideLine is Drawing Here '''
        dynamic_axes.plot(median_x, median_y, color=SW_global.guidelines_middle_color, dashes=(8, 6), linewidth=0.5)
        middle_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_middle_already_applied_array)
        guide_line_middle_already_applied_array.insert(length11, middle_ending_point)

        ''' 1st Time Base GuideLine is Drawing Here '''
        dynamic_axes.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
        base_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_base_already_applied_array)
        guide_line_base_already_applied_array.insert(length11, base_ending_point)

        ''' 1st Time Descender GuideLine is Drawing Here '''
        dynamic_axes.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
        descender_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_descender_already_applied_array)
        guide_line_descender_already_applied_array.insert(length11, descender_ending_point)

        fig.canvas.draw()
        brd.DrawBorderArt(SW_global.back_axes,SW_global.back_axes.get_figure,filename)
        # arr_img = plt.imread(filename)
        # imagebox = OffsetImage(arr_img, zoom=0.08)
        # imagebox.image.axes = dynamic_axes

        # for xi in range(25, 400, 25):
        #     ab = AnnotationBbox(imagebox, (xi, 1.1),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, 0),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()

        # ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # for yi in range(25, 400, 25):
        #     ab = AnnotationBbox(imagebox, (yi, -0.09),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, 1),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()
        #     ###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #     # Left_BorderArt
        #     ##for xx in np.arange(0,1,0.4):

        #     ab = AnnotationBbox(imagebox, (-0.8, -0.1),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, 1),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()

        #     ab = AnnotationBbox(imagebox, (-0.8, 0.3),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, .5),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()

        #     ab = AnnotationBbox(imagebox, (-0.8, 0.8),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, .5),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()

        #     ab = AnnotationBbox(imagebox, (-0.8, 1.1),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, 0),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()
        #     # =======================================================================================
        #     # Rightside_BorderArt

        #     ab = AnnotationBbox(imagebox, (402, 1.1),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, 0),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()

        #     ab = AnnotationBbox(imagebox, (402, 0.8),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, .5),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()

        #     ab = AnnotationBbox(imagebox, (402, 0.3),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, .5),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()

        #     ab = AnnotationBbox(imagebox, (402, -0.09),
        #                         xycoords=("data", "axes fraction"),
        #                         boxcoords="offset points",
        #                         box_alignment=(1, 1),
        #                         bboxprops={"edgecolor": "none"})

        #     dynamic_axes.add_artist(ab).draggable()
        # # =======================================================================================

        # fig.canvas.draw()

    else:

        ''' 1st Time Top GuideLine is Drawing Here '''
        dynamic_axes.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)
        top_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_top_already_applied_array)
        guide_line_top_already_applied_array.insert(length11, top_ending_point)

        ''' 1st Time Middle GuideLine is Drawing Here '''
        dynamic_axes.plot(median_x, median_y, color=SW_global.guidelines_middle_color, dashes=(8, 6), linewidth=0.5)
        middle_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_middle_already_applied_array)
        guide_line_middle_already_applied_array.insert(length11, middle_ending_point)

        ''' 1st Time Base GuideLine is Drawing Here '''
        dynamic_axes.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
        base_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_base_already_applied_array)
        guide_line_base_already_applied_array.insert(length11, base_ending_point)

        ''' 1st Time Descender GuideLine is Drawing Here '''
        dynamic_axes.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
        descender_ending_point = len(guideline_axes[l].lines)
        length11 = len(guide_line_descender_already_applied_array)
        guide_line_descender_already_applied_array.insert(length11, descender_ending_point)

        if SW_global.guidelines_toparea == 1:
            dynamic_axhtop = dynamic_axes.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea,
                                                  alpha=0.4)
            if SW_global.guidelines_background_color_toparea == '#ffffff':
                dynamic_axhtop = dynamic_axes.axhspan(790, 1460,
                                                      facecolor=SW_global.guidelines_background_color_toparea,
                                                      alpha=0.4)
            else:
                dynamic_axhtop = dynamic_axes.axhspan(790, 1460, facecolor='#ffffff')
                dynamic_axhtop = dynamic_axes.axhspan(790, 1460,
                                                      facecolor=SW_global.guidelines_background_color_toparea,
                                                      alpha=0.4)
        else:
            dynamic_axhtop = dynamic_axes.axhspan(790, 1460, facecolor='#ffffff')

        if SW_global.guidelines_middlearea == 1:
            dynamic_axhmiddle = dynamic_axes.axhspan(25, 730,
                                                     facecolor=SW_global.guidelines_background_color_middlearea,
                                                     alpha=0.4)
            if SW_global.guidelines_background_color_middlearea == '#ffffff':
                dynamic_axhmiddle = dynamic_axes.axhspan(25, 730,
                                                         facecolor=SW_global.guidelines_background_color_middlearea,
                                                         alpha=0.4)
            else:
                dynamic_axhmiddle = dynamic_axes.axhspan(25, 730, facecolor='#ffffff')
                dynamic_axhmiddle = dynamic_axes.axhspan(25, 730,
                                                         facecolor=SW_global.guidelines_background_color_middlearea,
                                                         alpha=0.4)
        else:
            dynamic_axhmiddle = dynamic_axes.axhspan(25, 730, facecolor='#ffffff')

        if SW_global.guidelines_descenderarea == 1:
            dynamic_axhdescender = dynamic_axes.axhspan(-730, -20,
                                                        facecolor=SW_global.guidelines_background_color_descenderarea,
                                                        alpha=0.4)
            if SW_global.guidelines_background_color_descenderarea == '#ffffff':
                dynamic_axhdescender = dynamic_axes.axhspan(-730, -20,
                                                            facecolor=SW_global.guidelines_background_color_descenderarea,
                                                            alpha=0.4)
            else:
                dynamic_axhdescender = dynamic_axes.axhspan(-730, -20, facecolor='#ffffff')
                dynamic_axhdescender = dynamic_axes.axhspan(-730, -20,
                                                            facecolor=SW_global.guidelines_background_color_descenderarea,
                                                            alpha=0.4)
        else:
            dynamic_axhdescender = dynamic_axes.axhspan(-730, -20, facecolor='#ffffff')

        fig.canvas.draw()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> stoke_arrows_Property_window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
v = tk.IntVar()
v.set(0)

def ShowChoice():
    print(v.get())

def stoke_arrows_option_mw():
    stoke_arrows = Toplevel(SW_Main_UI)
    stoke_arrows.wm_title("Letter Stoke Arrows")
    stoke_arrows.geometry("380x150+200+250")
    stoke_arrows.resizable(width=False, height=False)
    stoke_arrows.wm_transient(SW_Main_UI)
    stoke_arrows_labelframe = LabelFrame(stoke_arrows, text="Arrows")
    stoke_arrows_labelframe.pack(side=LEFT, fill="both", pady=15, padx=6)

    # initializing the choice
    arrows_option = [("Arrows On/Off from property bar setting"),
                     ("First letter of every line arrowed"),
                     ("First letter of every word arrowed"),
                     ("First letter of every-other word arrowed"),
                     ("Entire first word of every line arrowed")
                     ]
    for val, arrows_option in enumerate(arrows_option):
        arrows_option_rb = tk.Radiobutton(stoke_arrows_labelframe, text=arrows_option, variable=v, value=val)
        arrows_option_rb.pack(anchor=W)

    stoke_arrows_button_ok = ttk.Button(stoke_arrows, text="OK", command=ShowChoice)
    stoke_arrows_button_ok.pack(side=TOP, padx=5, pady=18)
    stoke_arrows_button_cancel = ttk.Button(stoke_arrows, text="Cancel", command=stoke_arrows.destroy)
    stoke_arrows_button_cancel.pack(side=TOP, padx=5)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Stoke Arrow Color Change Option Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
var = IntVar()  # stroke_arrow_color_mw variable

def stroke_arrow_color_mw():
    stroke_arrow_color = Toplevel(SW_Main_UI)
    stroke_arrow_color.wm_title("Stroke Arrow Color")
    stroke_arrow_color.geometry("310x210+250+200")
    stroke_arrow_color.resizable(width=False, height=False)
    stroke_arrow_color.wm_transient(SW_Main_UI)

    stawcl_frame0 = Frame(stroke_arrow_color)
    stawcl_frame0.pack(pady=10)

    stawcl_lf = LabelFrame(stawcl_frame0, text="Stroke Arrow Color", font=('manuscript', 9), width=150, height=150)
    stawcl_lf.pack(side=LEFT, ipady=42, ipadx=4)

    def setBgColor():
        (triple, hexstr) = askcolor()
        SW_global.stokearrow_color_var = hexstr
        if hexstr:
            # print(hexstr)
            stawcl_Color1.config(bg=SW_global.stokearrow_color_var)
            for e in range(l):
                ax1.plot(x4[e], y4[e], color=SW_global.stokearrow_color_var, linewidth=1)
            for f in range(k):
                ax1.plot(x3[f], y3[f], color=SW_global.stokearrow_color_var, linewidth=1)
            fig.canvas.draw()

    stawcl_Color1 = tk.Button(stawcl_lf, bg=SW_global.stokearrow_color_var, text='', width=40, command=setBgColor)
    stawcl_Color1.config(font=('times', 4))
    stawcl_Color1.pack(side=LEFT, anchor=N)
    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(stawcl_lf, width=10, height=20, image=down_icon, command=setBgColor)
    down_button.image = down_icon
    down_button.pack(side=LEFT, anchor=N)

    stawcl_example = LabelFrame(stawcl_frame0, text="Example", font=('manuscript', 9), width=150, height=150)
    stawcl_example.pack(side=RIGHT, ipadx=8, ipady=4)

    FigexFrame_swcl = Frame(stawcl_example, width=20, bd=2, highlightbackground="black", highlightcolor="black",
                            highlightthickness=1)
    FigexFrame_swcl.pack()

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(1, 1)

    base_x = [0, (1500 * 2)]
    base_y = [0, 0]
    median_x = [0, (1500 * 2)]
    median_y = [757, 757]
    descender_x = [0, (1500 * 2)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * 2)]
    ascender_y = [1500, 1500]

    x1 = [[0, 752, 1500], [248, 1251]]
    y1 = [[0, 1501, 0], [496, 495]]
    kern_fix = 1800
    x2 = [[kern_fix + 754, kern_fix + 754],
          [kern_fix + 754, kern_fix + 754],
          [kern_fix + 377], [kern_fix + 0, kern_fix + 0, kern_fix + 222, kern_fix + 377],
          [kern_fix + 377, kern_fix + 221, kern_fix + 0, kern_fix + 0],
          [kern_fix + 755, kern_fix + 755, kern_fix + 640, kern_fix + 528, kern_fix + 377],
          [kern_fix + 377, kern_fix + 528, kern_fix + 755, kern_fix + 755]]
    y2 = [[375, 749],
          [0, 375],
          [749],
          [375, 530, 749, 749],
          [0, 0, 219, 375],
          [376, 530, 641, 749, 749],
          [0, 0, 221, 376]]

    n = len(x1)
    m = len(x2)

    x4 = [[1031, 675, 1031], [1031, 925], [925, 1031], [925, 925],

          [255], [468, 255], [363, 241],

          [255, 363], [241, 255], [1256, 1273], [1039, 1256],

          [1256], [1141, 1256], [1273, 1141],

          [940, 1021, 1021, 940, 940, 1021], [543, 543],

          [492, 572, 572, 492], [572, 572, 492]]

    y4 = [[651, 650, 651], [651, 723], [576, 651], [723, 576], [825], [1237, 825], [872, 945], [825, 872],

          [945, 825], [823, 953], [1216, 823], [823], [879, 823], [953, 879],

          [1462, 1462, 1382, 1382, 1302, 1302], [1461, 1301], [733, 733, 653, 653], [653, 572, 572]]

    x3 = [[kern_fix + 884], [kern_fix + 885, kern_fix + 884],
          [kern_fix + 962, kern_fix + 815], [kern_fix + 884, kern_fix + 962], [kern_fix + 815, kern_fix + 884],
          [kern_fix + 129, kern_fix + 179, kern_fix + 381, kern_fix + 469, kern_fix + 604, kern_fix + 619],
          [kern_fix + 96, kern_fix + 129, kern_fix + 228],
          [kern_fix + 228, kern_fix + 96],
          [kern_fix + 838, kern_fix + 919, kern_fix + 919, kern_fix + 838, kern_fix + 838, kern_fix + 919],
          [kern_fix + 521, kern_fix + 521]]
    y3 = [[124], [485, 124], [213, 213], [124, 213], [213, 124], [404, 641, 641, 641, 528, 445], [513, 404, 460],

          [460, 513], [735, 735, 655, 655, 575, 575], [454, 294]]

    k = len(x3)
    l = len(x4)
    for e in range(l):
        ax1.plot(x4[e], y4[e], color=SW_global.stokearrow_color_var, linewidth=1)
    for f in range(k):
        ax1.plot(x3[f], y3[f], color=SW_global.stokearrow_color_var, linewidth=1)

    for i in range(n):
        ax1.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
    for j in range(m):
        ax1.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')

    if SW_global.decisiondot_on_off == 1:
        for i in range(n):
            ax1.scatter(x1[i], y1[i], color=SW_global.decisiondot_color, marker='.')

    if SW_global.startdot_on_off == 1:
        ax1.plot(752, 1501, marker='.', color=SW_global.startdot_color)
        ax1.plot(kern_fix + 754, 375, marker='.', color=SW_global.startdot_color)

    if SW_global.guidelines_toparea == 1:
        ax1.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea, alpha=0.4)
    if SW_global.guidelines_middlearea == 1:
        ax1.axhspan(25, 730, facecolor=SW_global.guidelines_background_color_middlearea, alpha=0.4)
    if SW_global.guidelines_descenderarea == 1:
        ax1.axhspan(-730, -20, facecolor=SW_global.guidelines_background_color_descenderarea, alpha=0.4)

    lineax1 = ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
    lineax2 = ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linestyle=':', linewidth=0.5)
    lineax3 = ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
    lineax4 = ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=FigexFrame_swcl)
    canvas.get_tk_widget().grid(row=0, column=1)

    stawcl_frame1 = Frame(stroke_arrow_color)
    stawcl_frame1.pack()

    stawcl_frame2 = Frame(stawcl_frame1)
    stawcl_frame2.grid(row=0, column=0)

    stawcl_chkbx = Checkbutton(stawcl_frame2, text="Set as Default", font=('manuscript', 9), variable=var)
    stawcl_chkbx.pack(side=LEFT)

    stawcl_frame3 = Frame(stawcl_frame1)
    stawcl_frame3.grid(row=0, column=1)

    def stroke_arrow_close():
        stroke_arrow_color.destroy()
        if SW_global.stokearrow_on_off:
            main3()
            compositedot_already_applied_array.clear()
            main3()
        else:
            pass

    stoke_arrows_button_cancel = ttk.Button(stawcl_frame3, text="Cancel", command=stroke_arrow_color.destroy)
    stoke_arrows_button_cancel.pack(side=RIGHT, padx=5)
    stoke_arrows_button_ok = ttk.Button(stawcl_frame3, text="OK", command=stroke_arrow_close)
    stoke_arrows_button_ok.pack(side=RIGHT, padx=5, pady=18)


stoke_arrow_flag_pos = 0


################################################ This is composite dot for multiple guide Line ##########################
def composite_dot_multiple_guideline(a,b,c,d,e,f,g):
    print("I am in stoke arrow please check")
    stoke_arrow_flag_pos1=a
    delete_list_temp=b
    kern_value_array1=c
    guideline_axes1_plot=d
    compositedot_already_applied_array1=e
    print("This is e")
    print(stoke_arrow_flag_pos1)
    print(delete_list_temp)
    print(kern_value_array1)
    print(guideline_axes1_plot)
    print(compositedot_already_applied_array1)
    print()
    guideline_axes1_lines=[i for i in SW_global.axes_data[f]["lines"]]


    #####stoke_arrow_flag_pos1,delete_list_temp,kern_value_array1,guideline_axes_plot,compositedot_already_applied_array1,str(i),None




    if SW_global.stokearrow_on_off == 1:
        delete_list_counter = len(delete_list_temp)

        if stoke_arrow_flag_pos1 == 0:
            for i in range(delete_list_counter):
                glyph = delete_list_temp[i]
                krn = kern_value_array1[i]
                stoke_arrow_flag_pos1 = stoke_arrow_flag_pos1 + 1
                initial_stoke_arrow_pos = len(guideline_axes1_lines)

                c1, c2 = manuscript_stoke_arrow.return_stoke_arrow_manuscript(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    te=guideline_axes1_plot.plot(c1, c2, color=SW_global.stokearrow_color_var, linewidth=1)
                    guideline_axes1_lines.append(te[0])
                else:
                    for ii in range(len(c1)):
                        te=guideline_axes1_plot.plot(c1[ii], c2[ii], color=SW_global.stokearrow_color_var, linewidth=1)
                        guideline_axes1_lines.append(te[0])

                last_stoke_arrow_pos = len(guideline_axes1_lines)
                ltn = len(compositedot_already_applied_array1)
                compositedot_already_applied_array1.insert(ltn, initial_stoke_arrow_pos)
                ltn = len(compositedot_already_applied_array1)
                compositedot_already_applied_array1.insert(ltn, last_stoke_arrow_pos)
            fig.canvas.draw()

        else:
            for i in range(stoke_arrow_flag_pos1, delete_list_counter):
                glyph = delete_list_temp[i]
                krn = kern_value_array1[i]
                stoke_arrow_flag_pos1 = stoke_arrow_flag_pos1 + 1
                initial_stoke_arrow_pos = len(guideline_axes_lines)

                c1, c2 = manuscript_stoke_arrow.return_stoke_arrow_manuscript(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    te=guideline_axes1_plot.plot(c1, c2, color=SW_global.stokearrow_color_var, linewidth=1)
                    guideline_axes1_lines.append(te[0])
                else:
                    for ii in range(len(c1)):
                        te=guideline_axes1_plot.plot(c1[ii], c2[ii], color=SW_global.stokearrow_color_var, linewidth=1)
                        guideline_axes1_lines.append(te[0])

                last_stoke_arrow_pos = len(guideline_axes1_lines)
                ltn = len(compositedot_already_applied_array1)
                compositedot_already_applied_array1.insert(ltn, initial_stoke_arrow_pos)
                ltn = len(compositedot_already_applied_array1)
                compositedot_already_applied_array1.insert(ltn, last_stoke_arrow_pos)

        (SW_global.axes_data[f]["lines"]).clear()
        (SW_global.axes_data[f]["gval"]).clear()
        for i in guideline_axes1_lines:
            (SW_global.axes_data[f]["lines"]).append(i)
            (SW_global.axes_data[f]["gval"]).append(i)

        (SW_global.axes_data[f]["compositedot_already_applied_array"]).clear()

        for i in compositedot_already_applied_array1:
            (SW_global.axes_data[f]["compositedot_already_applied_array"]).append(i)

        SW_global.axes_data[f]["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos1

    return

def call_composit_dot_multipleGuideline():
    for i in range(len(SW_global.axes_data)):
        print("This is from call_composit_dot_multipleGuideline")
        delete_list_temp=SW_global.axes_data[str(i)]["delete_list"]
        kern_value_array1=SW_global.axes_data[str(i)]["kern_value_array"]
        #letters_already_written1=SW_global.axes_data[str(i)]["letters_already_written"]
        kern_list1=SW_global.axes_data[str(i)]["kern_list"]
        stoke_arrow_flag_pos1=SW_global.axes_data[str(i)]["stoke_arrow_flag_pos"]
        compositedot_already_applied_array1=[i for i in  (SW_global.axes_data[str(i)]["compositedot_already_applied_array"])]
        axw=SW_global.axes_data[str(i)]["axis_data"]
        print(delete_list_temp)
        print(kern_value_array1)
        print(kern_list1)
        print(compositedot_already_applied_array1)
        print(axw)
        print(stoke_arrow_flag_pos1)
        composite_dot_multiple_guideline(stoke_arrow_flag_pos1,delete_list_temp,kern_value_array1,axw,compositedot_already_applied_array1,str(i),None)
    return


def eraseCompositeDotFromMultipleGuideLine():
    for i in range(len(SW_global.axes_data)):
        for j in range(len(SW_global.axes_data[str(i)]["compositedot_already_applied_array"])-1):
            st_pos=(SW_global.axes_data[str(i)]["compositedot_already_applied_array"])[j]
            en_pos=(SW_global.axes_data[str(i)]["compositedot_already_applied_array"])[j+1]
            for k7 in range(st_pos,en_pos):
                ((SW_global.axes_data[str(i)]["lines"])[k7]).set_visible(False)
        (SW_global.axes_data[str(i)]["compositedot_already_applied_array"]).clear()
        SW_global.axes_data[str(i)]["stoke_arrow_flag_pos"]=0
    return


############################################### End of composite dot for multiple guide line ##############################

def composite_dot():
    global stoke_arrow_flag_pos
    print("This is composite dot")

    if SW_global.stokearrow_on_off == 1:
        print("I am in check point111")
        print(delete_list)
        delete_list_counter = len(delete_list)
        if stoke_arrow_flag_pos == 0:
            print("I am in stoke arrow flag pos")
            for i in range(delete_list_counter):
                glyph = delete_list[i]
                print(kern_value_array)
                krn = kern_value_array[i]

                stoke_arrow_flag_pos = stoke_arrow_flag_pos + 1
                initial_stoke_arrow_pos = len(guideline_axes[l].lines)
         #       print("This is kern list array")
                print(kern_value_array)
                print(SW_global.kern_list)
          #      print("This is kern list end")
                c1, c2 = manuscript_stoke_arrow.return_stoke_arrow_manuscript(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)
                if draw_type == 1:
                    guideline_axes[l].plot(c1, c2, color=SW_global.stokearrow_color_var, linewidth=1)
                else:
                    for ii in range(len(c1)):
                        guideline_axes[l].plot(c1[ii], c2[ii], color=SW_global.stokearrow_color_var, linewidth=1)
                last_stoke_arrow_pos = len(guideline_axes[l].lines)
                ltn = len(compositedot_already_applied_array)
                compositedot_already_applied_array.insert(ltn, initial_stoke_arrow_pos)
                ltn = len(compositedot_already_applied_array)
                compositedot_already_applied_array.insert(ltn, last_stoke_arrow_pos)
            fig.canvas.draw()

        else:
            for i in range(stoke_arrow_flag_pos, delete_list_counter):
                glyph = delete_list[i]
                krn = kern_value_array[i]
                stoke_arrow_flag_pos = stoke_arrow_flag_pos + 1
                initial_stoke_arrow_pos = len(guideline_axes[l].lines)

                c1, c2 = manuscript_stoke_arrow.return_stoke_arrow_manuscript(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    guideline_axes[l].plot(c1, c2, color=SW_global.stokearrow_color_var, linewidth=1)
                else:
                    for ii in range(len(c1)):
                        guideline_axes[l].plot(c1[ii], c2[ii], color=SW_global.stokearrow_color_var, linewidth=1)

                last_stoke_arrow_pos = len(guideline_axes[l].lines)
                ltn = len(compositedot_already_applied_array)
                compositedot_already_applied_array.insert(ltn, initial_stoke_arrow_pos)
                ltn = len(compositedot_already_applied_array)
                compositedot_already_applied_array.insert(ltn, last_stoke_arrow_pos)
            fig.canvas.draw()
        #print("checkpoint7")

        fig.canvas.mpl_connect('key_press_event', press)
        fig.canvas.mpl_connect('button_press_event',onclick2)
        fig.canvas.mpl_connect('button_release_event',onrelease)






def stoke_arrow_continueous_write():
    composite_dot()


def main3():
    global stoke_arrow_flag_pos
    print("This is soke arrow")
    print("This is stoke arrow 2")
    if SW_global.stokearrow_on_off == 0:
        SW_global.stokearrow_on_off = 1
        print("checkpoint9")
        stoke_arrows_button.configure(background='skyblue')
        call_composit_dot_multipleGuideline()
        composite_dot()
    else:
        SW_global.stokearrow_on_off = 0
        eraseCompositeDotFromMultipleGuideLine()
        print("This is stoke arrow 4")
        stoke_arrows_button.configure(background='#d9d9d9')
        stoke_arrow_flag_pos = 0
        fln = len(compositedot_already_applied_array)
        cntr = 0
        for ii in range(fln - 1):
            if cntr == 0:
                x12 = compositedot_already_applied_array[ii]
                y12 = compositedot_already_applied_array[ii + 1]
                for jj in range(x12, y12):
                    guideline_axes[l].lines[jj].set_visible(False)
                cntr = cntr + 1
            else:
                cntr = cntr - 1
        fig.canvas.draw()
    print("This is stoke arrow 3")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Start_Dot_Property_Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def start_arrow_menu_wtp():
    start_arrow_wtp = Toplevel(SW_Main_UI)
    start_arrow_wtp.wm_title("Start Dot Color")
    start_arrow_wtp.geometry("310x210+250+200")
    start_arrow_wtp.resizable(width=False, height=False)
    start_arrow_wtp.wm_transient(SW_Main_UI)
    stdt_frame0 = Frame(start_arrow_wtp)
    stdt_frame0.pack(pady=10)

    stdt_lf = LabelFrame(stdt_frame0, text="Stroke Dot Color", font=('manuscript', 9), width=150, height=150)
    stdt_lf.pack(side=LEFT, ipady=42, ipadx=4)

    def setBgColor():
        global decisiondot_colors
        global startdot_flag_pos
        (triple, hexstr) = askcolor()
        SW_global.startdot_color = hexstr
        if hexstr:
            stdt_Color1.config(bg=SW_global.startdot_color)
            ax1.plot(752, 1501, marker='.', color=SW_global.startdot_color)
            ax1.plot(kern_fix + 754, 375, marker='.', color=SW_global.startdot_color)
            fig.canvas.draw()

    stdt_Color1 = tk.Button(stdt_lf, bg=SW_global.startdot_color, text='', width=40, command=setBgColor)
    stdt_Color1.config(font=('times', 4))
    stdt_Color1.pack(side=LEFT, anchor=N)
    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(stdt_lf, width=10, height=20, image=down_icon, command=setBgColor)
    down_button.image = down_icon
    down_button.pack(side=LEFT, anchor=N)

    stdt_example = LabelFrame(stdt_frame0, text="Example", font=('manuscript', 9), width=150, height=150)
    stdt_example.pack(side=RIGHT, ipadx=8, ipady=4)

    FigexFrame_swdt = Frame(stdt_example, width=20, bd=2, highlightbackground="black", highlightcolor="black",
                            highlightthickness=1)
    FigexFrame_swdt.pack()

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(1, 1)

    base_x = [0, (1500 * 2)]
    base_y = [0, 0]
    median_x = [0, (1500 * 2)]
    median_y = [757, 757]
    descender_x = [0, (1500 * 2)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * 2)]
    ascender_y = [1500, 1500]

    x1 = [[0, 752, 1500], [248, 1251]]
    y1 = [[0, 1501, 0], [496, 495]]
    kern_fix = 1800
    x2 = [[kern_fix + 754, kern_fix + 754],
          [kern_fix + 754, kern_fix + 754],
          [kern_fix + 377], [kern_fix + 0, kern_fix + 0, kern_fix + 222, kern_fix + 377],
          [kern_fix + 377, kern_fix + 221, kern_fix + 0, kern_fix + 0],
          [kern_fix + 755, kern_fix + 755, kern_fix + 640, kern_fix + 528, kern_fix + 377],
          [kern_fix + 377, kern_fix + 528, kern_fix + 755, kern_fix + 755]]
    y2 = [[375, 749],
          [0, 375],
          [749],
          [375, 530, 749, 749],
          [0, 0, 219, 375],
          [376, 530, 641, 749, 749],
          [0, 0, 221, 376]]

    n = len(x1)
    m = len(x2)
    for i in range(n):
        ax1.plot(752, 1501, marker='.', color=SW_global.startdot_color)
        ax1.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
    for j in range(m):
        ax1.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')
        ax1.plot(kern_fix + 754, 375, marker='.', color=SW_global.startdot_color)

    if SW_global.stokearrow_on_off == 1:
        x4 = [[1031, 675, 1031], [1031, 925], [925, 1031], [925, 925],[255], [468, 255], [363, 241],[255, 363],
              [241, 255], [1256, 1273], [1039, 1256],[1256], [1141, 1256], [1273, 1141],[940, 1021, 1021, 940, 940, 1021],
              [543, 543],[492, 572, 572, 492], [572, 572, 492]]

        y4 = [[651, 650, 651], [651, 723], [576, 651], [723, 576], [825], [1237, 825], [872, 945], [825, 872],[945, 825],
              [823, 953], [1216, 823], [823], [879, 823], [953, 879],[1462, 1462, 1382, 1382, 1302, 1302], [1461, 1301],
              [733, 733, 653, 653], [653, 572, 572]]

        x3 = [[kern_fix + 884], [kern_fix + 885, kern_fix + 884],
              [kern_fix + 962, kern_fix + 815], [kern_fix + 884, kern_fix + 962], [kern_fix + 815, kern_fix + 884],
              [kern_fix + 129, kern_fix + 179, kern_fix + 381, kern_fix + 469, kern_fix + 604, kern_fix + 619],
              [kern_fix + 96, kern_fix + 129, kern_fix + 228],
              [kern_fix + 228, kern_fix + 96],
              [kern_fix + 838, kern_fix + 919, kern_fix + 919, kern_fix + 838, kern_fix + 838, kern_fix + 919],
              [kern_fix + 521, kern_fix + 521]]
        y3 = [[124], [485, 124], [213, 213], [124, 213], [213, 124], [404, 641, 641, 641, 528, 445], [513, 404, 460],
              [460, 513], [735, 735, 655, 655, 575, 575], [454, 294]]

        k = len(x3)
        l = len(x4)
        for e in range(l):
            ax1.plot(x4[e], y4[e], color=SW_global.stokearrow_color_var, linewidth=1)
        for f in range(k):
            ax1.plot(x3[f], y3[f], color=SW_global.stokearrow_color_var, linewidth=1)

    if SW_global.decisiondot_on_off == 1:
        for i in range(n):
            ax1.scatter(x1[i], y1[i], color=SW_global.decisiondot_color, marker='.')
    if SW_global.connectdot_on_off == 1:
        for i in range(n):
            ax1.plot(x1[i], y1[i], color=SW_global.connectingdot_color_var, linewidth=0.5)
        for j in range(m):
            ax1.plot(x2[j], y2[j], color=SW_global.connectingdot_color_var, linewidth=0.5)

    if SW_global.guidelines_toparea == 1:
        ax1.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea, alpha=0.4)
    if SW_global.guidelines_middlearea == 1:
        ax1.axhspan(25, 730, facecolor=SW_global.guidelines_background_color_middlearea, alpha=0.4)
    if SW_global.guidelines_descenderarea == 1:
        ax1.axhspan(-730, -20, facecolor=SW_global.guidelines_background_color_descenderarea, alpha=0.4)

    ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
    ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linestyle=':', linewidth=0.5)
    ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
    ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=FigexFrame_swdt)
    canvas.get_tk_widget().grid(row=0, column=1)

    stdt_frame1 = Frame(start_arrow_wtp)
    stdt_frame1.pack()

    stdt_frame2 = Frame(stdt_frame1)
    stdt_frame2.grid(row=0, column=0)

    stdt_chkbx = Checkbutton(stdt_frame2, text="Set as Default", font=('manuscript', 9), variable=var)
    stdt_chkbx.pack(side=LEFT)

    stdt_frame3 = Frame(stdt_frame1)
    stdt_frame3.grid(row=0, column=1)

    def startdot_wtp_close():
        start_arrow_wtp.destroy()
        if SW_global.startdot_on_off:
            main1()
            startdot_already_applied_array.clear()
            main1()
        else:
            pass

    start_arrow_button_cancel = ttk.Button(stdt_frame3, text="Cancel", command=start_arrow_wtp.destroy)
    start_arrow_button_cancel.pack(side=RIGHT, padx=5)
    start_arrow_button_ok = ttk.Button(stdt_frame3, text="OK", command=startdot_wtp_close)
    start_arrow_button_ok.pack(side=RIGHT, padx=5, pady=18)


startdot_flag_pos = 0

############################################ This is start dot for multiple guide line ###############################
def call_start_dot_multiple_guideline():
    print("This is from call start dot for mul")
    print(len(SW_global.axes_data))
    for i in range(len(SW_global.axes_data)):
        delete_list_temp=[j for j in (SW_global.axes_data[str(i)]["delete_list"])]
        kern_value_array1=[j for j in (SW_global.axes_data[str(i)]["kern_value_array"])]
        letters_already_written1=[j for j in (SW_global.axes_data[str(i)]["letters_already_written"])]
        kern_list1=[j for j in (SW_global.axes_data[str(i)]["kern_list"])]
        startdot_flag_pos1=SW_global.axes_data[str(i)]["startdot_flag_pos"]
        startdot_already_applied_array1=[j for j in (SW_global.axes_data[str(i)]["startdot_already_applied_array"])]
        axw=SW_global.axes_data[str(i)]["axis_data"]
        print("I am in start dot")
        start_dot_for_multipleguideline(startdot_flag_pos1,delete_list_temp,kern_value_array1,axw,startdot_already_applied_array1,str(i),None)
        print("I am in stoke arrow please check")
    return



def start_dot_for_multipleguideline(a,b,c,d,e,f,g):
    print()
    print("I am in stoke arrow please check")
    startdot_flag_pos1=a
    delete_list_temp=b
    kern_value_array1=c
    guideline_axes1_plot=d
    startdot_already_applied_array1=e
    guideline_axes1_plot=d
    print("This is e")
    print(startdot_flag_pos1)
    print(delete_list_temp)
    print(kern_value_array1)
    print(guideline_axes1_plot)
    print(startdot_already_applied_array1)
    print()
    guideline_axes1_lines=[i for i in SW_global.axes_data[f]["lines"]]
    print(guideline_axes1_lines)


    if SW_global.startdot_on_off == 1:
        delete_list_counter = len(delete_list_temp)

        if startdot_flag_pos1 == 0:
            for i in range(delete_list_counter):
                glyph = delete_list_temp[i]
                krn = kern_value_array1[i]
                startdot_flag_pos1 = startdot_flag_pos1 + 1
                initial_start_dot_pos1 = len(guideline_axes1_lines)

                c1, c2 = manuscript_start_dot.return_startdot_manuscript(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                te=guideline_axes1_plot.plot(c1, c2, marker='.', color=SW_global.startdot_color)
                guideline_axes1_lines.append(te[0])

                last_start_dot_pos1 = len(guideline_axes1_lines)
                ltn1 = len(startdot_already_applied_array1)
                startdot_already_applied_array1.insert(ltn1, initial_start_dot_pos1)
                ltn1 = len(startdot_already_applied_array1)
                startdot_already_applied_array1.insert(ltn1, last_start_dot_pos1)

        else:
            for i in range(startdot_flag_pos1, delete_list_counter):
                glyph = delete_list_temp[i]
                krn = kern_value_array1[i]
                startdot_flag_pos1 = startdot_flag_pos1 + 1
                initial_start_dot_pos1 = len(guideline_axes1_lines)

                c1, c2 = manuscript_start_dot.return_startdot_manuscript(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                te=guideline_axes1_plot.plot(c1, c2, marker='.', color=SW_global.startdot_color)
                guideline_axes1_lines.append(te[0])

                last_start_dot_pos1 = len(guideline_axes1_lines)
                ltn1 = len(startdot_already_applied_array1)
                startdot_already_applied_array1.insert(ltn1, initial_start_dot_pos1)
                ltn1 = len(startdot_already_applied_array1)
                startdot_already_applied_array1.insert(ltn1, last_start_dot_pos1)
        (SW_global.axes_data[f]["lines"]).clear()
        (SW_global.axes_data[f]["gval"]).clear()
        for i in guideline_axes1_lines:
            (SW_global.axes_data[f]["lines"]).append(i)
            (SW_global.axes_data[f]["gval"]).append(i)
        (SW_global.axes_data[f]["startdot_already_applied_array"]).clear()
        for i in startdot_already_applied_array1:
            (SW_global.axes_data[f]["startdot_already_applied_array"]).append(i)
        SW_global.axes_data[f]["startdot_flag_pos"]=startdot_flag_pos1
    return


def eraseStartDotFromMultipleGuideLine():
    for i in range(len(SW_global.axes_data)):
        for j in range(len(SW_global.axes_data[str(i)]["startdot_already_applied_array"])-1):
            st_pos=(SW_global.axes_data[str(i)]["startdot_already_applied_array"])[j]
            en_pos=(SW_global.axes_data[str(i)]["startdot_already_applied_array"])[j+1]
            for k7 in range(st_pos,en_pos):
                ((SW_global.axes_data[str(i)]["lines"])[k7]).set_visible(False)
        (SW_global.axes_data[str(i)]["startdot_already_applied_array"]).clear()
        SW_global.axes_data[str(i)]["startdot_flag_pos"]=0

    return


####################################### End of start dot ##########################################


def start_dot():
    global startdot_flag_pos
    if SW_global.startdot_on_off == 1:
        delete_list_counter = len(delete_list)

        if startdot_flag_pos == 0:
            for i in range(delete_list_counter):
                glyph = delete_list[i]
                krn = kern_value_array[i]
                startdot_flag_pos = startdot_flag_pos + 1
                initial_start_dot_pos1 = len(guideline_axes[l].lines)

                c1, c2 = manuscript_start_dot.return_startdot_manuscript(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                guideline_axes[l].plot(c1, c2, marker='.', color=SW_global.startdot_color)

                last_start_dot_pos1 = len(guideline_axes[l].lines)
                ltn1 = len(startdot_already_applied_array)
                startdot_already_applied_array.insert(ltn1, initial_start_dot_pos1)
                ltn1 = len(startdot_already_applied_array)
                startdot_already_applied_array.insert(ltn1, last_start_dot_pos1)
            fig.canvas.draw()

        else:
            for i in range(startdot_flag_pos, delete_list_counter):
                glyph = delete_list[i]
                krn = kern_value_array[i]
                startdot_flag_pos = startdot_flag_pos + 1
                initial_start_dot_pos1 = len(guideline_axes[l].lines)

                c1, c2 = manuscript_start_dot.return_startdot_manuscript(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                guideline_axes[l].plot(c1, c2, marker='.', color=SW_global.startdot_color)

                last_start_dot_pos1 = len(guideline_axes[l].lines)
                ltn1 = len(startdot_already_applied_array)
                startdot_already_applied_array.insert(ltn1, initial_start_dot_pos1)
                ltn1 = len(startdot_already_applied_array)
                startdot_already_applied_array.insert(ltn1, last_start_dot_pos1)
            fig.canvas.draw()
        print("checkpoint8")
        fig.canvas.mpl_connect('key_press_event', press)
        fig.canvas.mpl_connect('button_press_event',onclick2)
        fig.canvas.mpl_connect('button_release_event',onrelease)




def start_dot_continueous_write():
    start_dot()


def main1():
    global startdot_flag_pos

    if SW_global.startdot_on_off == 0:
        SW_global.startdot_on_off = 1
        start_arrow_button.configure(background='skyblue')
        call_start_dot_multiple_guideline()
        start_dot()

    else:
        SW_global.startdot_on_off = 0
        eraseStartDotFromMultipleGuideLine()
        start_arrow_button.configure(background='#d9d9d9')
        startdot_flag_pos = 0
        fln = len(startdot_already_applied_array)
        cntr = 0
        for ii in range(fln-1):
            if cntr == 0:
                x12 = startdot_already_applied_array[ii]
                y12 = startdot_already_applied_array[ii + 1]
                for jj in range(x12, y12):
                    guideline_axes[l].lines[jj].set_visible(False)
                cntr = cntr + 1
            else:
                cntr = cntr - 1
        fig.canvas.draw()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Letter_Outline_Property_Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def letter_outline_menu_wtp():
    letter_outline_wtp = Toplevel(SW_Main_UI)
    letter_outline_wtp.wm_title("Outline Font Color")
    letter_outline_wtp.geometry("310x210+250+200")
    letter_outline_wtp.resizable(width=False, height=False)
    letter_outline_wtp.wm_transient(SW_Main_UI)

    ltolt_frame0 = Frame(letter_outline_wtp)
    ltolt_frame0.pack(pady=10)

    ltolt_lf = LabelFrame(ltolt_frame0, text="Outline Font Color", font=('manuscript', 9), width=150, height=150)
    ltolt_lf.pack(side=LEFT, ipady=42, ipadx=4)

    def draw_outline_again():
        for i in range(len_out_with_border_x_A):
            ax1.plot(lo_x_A[i], lo_y_A[i], color='white', linewidth=0.6)

        for i in range(len_out_normal_x_A):
            ax1.plot(x_A[i], y_A[i], color='white', linewidth=0.8, linestyle=':')

        for i in range(len_out_with_border_x_a):
            ax1.plot(lo_x_a[i], lo_y_a[i], color='white', linewidth=0.6)

        for i in range(len_out_normal_x_a):
            ax1.plot(x_a[i], y_a[i], color='white', linewidth=0.8, linestyle=':')
        fig.canvas.draw()

        for i in range(len_out_with_border_x_A):
            ax1.plot(lo_x_A[i], lo_y_A[i], color=SW_global.letter_out_color_var, linewidth=0.6)

        for i in range(len_out_normal_x_A):
            ax1.plot(x_A[i], y_A[i], color='black', linewidth=0.8, linestyle=':')

        for i in range(len_out_with_border_x_a):
            ax1.plot(lo_x_a[i], lo_y_a[i], color=SW_global.letter_out_color_var, linewidth=0.6)

        for i in range(len_out_normal_x_a):
            ax1.plot(x_a[i], y_a[i], color='black', linewidth=0.8, linestyle=':')
        fig.canvas.draw()


    def setBgColor():
        (triple, hexstr) = askcolor()
        SW_global.letter_out_color_var = hexstr
        print("SW_global.letter_out_color_var", SW_global.letter_out_color_var)
        if hexstr:
            draw_outline_again()

    ltolt_Color1 = tk.Button(ltolt_lf, bg='black', text='', width=40, command=setBgColor)
    ltolt_Color1.config(font=('times', 4))
    ltolt_Color1.pack(side=LEFT, anchor=N)
    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(ltolt_lf, width=10, height=20, image=down_icon, command=setBgColor)
    down_button.image = down_icon
    down_button.pack(side=LEFT, anchor=N)

    ltolt_example = LabelFrame(ltolt_frame0, text="Example", font=('manuscript', 9), width=150, height=150)
    ltolt_example.pack(side=RIGHT, ipadx=8, ipady=4)

    FigexFrame_ltolt = Frame(ltolt_example, width=20, bd=2, highlightbackground="black", highlightcolor="black",
                             highlightthickness=1)
    FigexFrame_ltolt.pack()

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(1, 1)

    base_x = [0, (1500 * 2)]
    base_y = [0, 0]
    median_x = [0, (1500 * 2)]
    median_y = [757, 757]
    descender_x = [0, (1500 * 2)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * 2)]
    ascender_y = [1500, 1500]

    # Normal 'A' and 'a' coordinates
    kern_nor = 1800 + 110
    kern_out = 1800

    lo_x_A = [[681, 555, 1174, 872, 686], [435, 809, 936, 1784, 1547, 1297, 426, 172, -54, 432]]
    lo_y_A = [[865, 620, 620, 1235, 872], [865, 1614, 1614, -114, -114, 376, 376, -112, -114, 856]]

    x_A = [[120 + 0, 120 + 752, 120 + 1500], [120 + 248, 120 + 1251]]
    y_A = [[0, 1501, 0], [496, 495]]

    lo_x_a = [
        [kern_out + 759, kern_out + 759, kern_out + 976, kern_out + 976, kern_out + 759, kern_out + 760, kern_out + 650,
         kern_out + 469, kern_out + 286, kern_out + 138, kern_out + 0, kern_out + 0, kern_out + 0, kern_out + 118,
         kern_out + 274,
         kern_out + 468, kern_out + 648, kern_out + 763],
        [kern_out + 763, kern_out + 766, kern_out + 680, kern_out + 603, kern_out + 497, kern_out + 386, kern_out + 231,
         kern_out + 231, kern_out + 231, kern_out + 387, kern_out + 497, kern_out + 603, kern_out + 760,
         kern_out + 762],
        [kern_out + 763]]
    lo_y_a = [[777, 865, 865, -114, -114, -24, -111, -111, -111, 36, 172, 356, 583, 705, 866, 866, 866, 772],
              [353, 254, 174, 101, 101, 101, 256, 366, 476, 630, 630, 630, 482, 379], [772]]

    x_a = [[kern_nor+754, kern_nor+754], [kern_nor+754, kern_nor+754], [kern_nor+377], [kern_nor+0, kern_nor+0, kern_nor+222, kern_nor+377],
           [kern_nor+377, kern_nor+221, kern_nor+0, kern_nor+0], [kern_nor+755, kern_nor+755, kern_nor+640, kern_nor+528, kern_nor+377],
           [kern_nor+377, kern_nor+528, kern_nor+755, kern_nor+755]]
    y_a = [[375, 749], [0, 375], [749], [375, 530, 749, 749], [0, 0, 219, 375], [376, 530, 641, 749, 749],
           [0, 0, 221, 376]]

    len_out_with_border_x_A = len(lo_x_A)
    len_out_normal_x_A = len(x_A)
    len_out_with_border_x_a = len(lo_x_a)
    len_out_normal_x_a = len(x_a)

    draw_outline_again()

    ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
    ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linestyle=':', linewidth=0.5)
    ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
    ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=FigexFrame_ltolt)
    canvas.get_tk_widget().grid(row=0, column=1)

    ltolt_frame1 = Frame(letter_outline_wtp)
    ltolt_frame1.pack()

    ltolt_frame2 = Frame(ltolt_frame1)
    ltolt_frame2.grid(row=0, column=0)

    ltolt_chkbx = Checkbutton(ltolt_frame2, text="Set as Default", font=('manuscript', 9), variable=var)
    ltolt_chkbx.pack(side=LEFT)

    ltolt_frame3 = Frame(ltolt_frame1)
    ltolt_frame3.grid(row=0, column=1)

    def connect_dot_wtp_close():
        draw_outline_again()
        letter_outline_wtp.destroy()
        print("letter_out_line_on_off", letter_out_line_on_off)
        if letter_out_line_on_off:
            main_out()
        else:
            main_out()

    start_dot_button_cancel = ttk.Button(ltolt_frame3, text="Cancel", command=letter_outline_wtp.destroy)
    start_dot_button_cancel.pack(side=RIGHT, padx=5)
    start_dot_button_ok = ttk.Button(ltolt_frame3, text="OK1", command=connect_dot_wtp_close)
    start_dot_button_ok.pack(side=RIGHT, padx=5, pady=18)

letter_out_line_flag_pos = 0
letter_out_line_on_off = 0
initial_letter_out_line_pos = 0
last_letter_out_line_pos = 0
letter_out_line_already_applied_array = []

def Letter_Out_Line_Apply():
    global letter_out_line_flag_pos, initial_letter_out_line_pos, last_letter_out_line_pos, letter_out_line_on_off
    if letter_out_line_on_off == 1:
        delete_list_counter = len(delete_list)

        if letter_out_line_flag_pos == 0:
            for i in range(delete_list_counter):
                glyph = delete_list[i]
                krn = kern_value_array[i]
                letter_out_line_flag_pos = letter_out_line_flag_pos + 1
                initial_letter_out_line_pos = len(guideline_axes[l].lines)

                c1, c2 = manu_letter_outline.return_outline_fonts(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    guideline_axes[l].plot(c1, c2, color=SW_global.letter_out_color_var, linewidth=0.6)
                    fig.canvas.draw()
                else:
                    for ii in range(len(c1)):
                        guideline_axes[l].plot(c1[ii], c2[ii], color=SW_global.letter_out_color_var,
                                               linewidth=0.6)
                    fig.canvas.draw()

                last_letter_out_line_pos = len(guideline_axes[l].lines)
                ltn = len(letter_out_line_already_applied_array)
                letter_out_line_already_applied_array.insert(ltn, initial_letter_out_line_pos)
                ltn = len(letter_out_line_already_applied_array)
                letter_out_line_already_applied_array.insert(ltn, last_letter_out_line_pos)

        else:
            for i in range(letter_out_line_flag_pos, delete_list_counter):
                glyph = delete_list[i]  # ----> Picking Up 1 glyph
                krn = kern_value_array[i]  # ----> Picking Up it's kern_xvalue
                letter_out_line_flag_pos = letter_out_line_flag_pos + 1
                initial_letter_out_line_pos = len(guideline_axes[l].lines)

                c1, c2 = manu_letter_outline.return_outline_fonts(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    guideline_axes[l].plot(c1, c2, marker='.', color=SW_global.letter_out_color_var, linewidth=0.1)

                    fig.canvas.draw()
                else:
                    for ii in range(len(c1)):
                        guideline_axes[l].plot(c1[ii], c2[ii], marker='.', color=SW_global.letter_out_color_var,
                                               linewidth=0.1)
                    fig.canvas.draw()

                last_letter_out_line_pos = len(guideline_axes[l].lines)
                ltn = len(letter_out_line_already_applied_array)
                letter_out_line_already_applied_array.insert(ltn, initial_letter_out_line_pos)
                ltn = len(letter_out_line_already_applied_array)
                letter_out_line_already_applied_array.insert(ltn, last_letter_out_line_pos)
        print("check point 9")

        fig.canvas.mpl_connect('key_press_event', press)
        fig.canvas.mpl_connect('button_press_event',onclick2)
        fig.canvas.mpl_connect('button_release_event',onrelease)




def Letter_Out_Line_Continuous_writting():
    Letter_Out_Line_Apply()


def main_out():
    global initial_letter_out_line_pos, last_letter_out_line_pos, letter_out_line_flag_pos, letter_out_line_on_off
    if letter_out_line_on_off == 0:
        letter_out_line_on_off = 1
        letter_outline_button.configure(background='skyblue')
        call_letter_out_liner()

        #Letter_Out_Line_Apply()
    else:
        letter_out_line_on_off = 0
        decision_dot_button.configure(background='#d9d9d9')
        letter_out_line_flag_pos = 0
        fln = len(decisiondot_already_applied_array)
        cntr = 0
        for ii in range(fln - 1):
            if cntr == 0:
                x12 = letter_out_line_already_applied_array[ii]
                y12 = letter_out_line_already_applied_array[ii + 1]
                for jj in range(x12, y12):
                    guideline_axes[l].lines[jj].set_visible(False)
                    fig.canvas.draw()
                cntr = cntr + 1
            else:
                cntr = cntr - 1
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Decision_Dot_Propaty_Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def decision_dot_menu_wtp():
    decision_dot_wtp = Toplevel(SW_Main_UI)
    decision_dot_wtp.wm_title("Decision dot")
    decision_dot_wtp.geometry("310x210+250+200")
    decision_dot_wtp.resizable(width=False, height=False)
    decision_dot_wtp.wm_transient(SW_Main_UI)
    decision_dot_frame0 = Frame(decision_dot_wtp)
    decision_dot_frame0.pack(pady=10)

    decision_dot_lf = LabelFrame(decision_dot_frame0, text="Stroke Dot Color", font=('manuscript', 9), width=150,
                                 height=150)
    decision_dot_lf.pack(side=LEFT, ipady=42, ipadx=4)

    def setBgColor():
        (triple, hexstr) = askcolor()
        SW_global.decisiondot_color = hexstr
        if hexstr:
            decision_dot_Color1.config(bg=SW_global.decisiondot_color)
            for i in range(n):
                ax1.scatter(x1[i], y1[i], color=SW_global.decisiondot_color, marker='.')
            for j in range(m):
                ax1.scatter(x2[j], y2[j], color=SW_global.decisiondot_color, marker='.')
            fig.canvas.draw()

    decision_dot_Color1 = tk.Button(decision_dot_lf, bg=SW_global.decisiondot_color, text='', width=40, command=setBgColor)
    decision_dot_Color1.config(font=('times', 4))
    decision_dot_Color1.pack(side=LEFT, anchor=N)
    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(decision_dot_lf, width=10, height=20, image=down_icon, command=setBgColor)
    down_button.image = down_icon
    down_button.pack(side=LEFT, anchor=N)

    decision_dot_example = LabelFrame(decision_dot_frame0, text="Example", font=('manuscript', 9), width=150,
                                      height=150)
    decision_dot_example.pack(side=RIGHT, ipadx=8, ipady=4)

    FigexFrame_decision_dot = Frame(decision_dot_example, width=20, bd=2, highlightbackground="black",
                                    highlightcolor="black", highlightthickness=1)
    FigexFrame_decision_dot.pack()

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(1, 1)

    base_x = [0, (1500 * 2)]
    base_y = [0, 0]
    median_x = [0, (1500 * 2)]
    median_y = [757, 757]
    descender_x = [0, (1500 * 2)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * 2)]
    ascender_y = [1500, 1500]

    x1 = [[0, 752, 1500], [248, 1251]]
    y1 = [[0, 1501, 0], [496, 495]]
    kern_fix = 1800
    x2 = [[kern_fix + 754, kern_fix + 754],
          [kern_fix + 754, kern_fix + 754],
          [kern_fix + 377], [kern_fix + 0, kern_fix + 0, kern_fix + 222, kern_fix + 377],
          [kern_fix + 377, kern_fix + 221, kern_fix + 0, kern_fix + 0],
          [kern_fix + 755, kern_fix + 755, kern_fix + 640, kern_fix + 528, kern_fix + 377],
          [kern_fix + 377, kern_fix + 528, kern_fix + 755, kern_fix + 755]]
    y2 = [[375, 749],
          [0, 375],
          [749],
          [375, 530, 749, 749],
          [0, 0, 219, 375],
          [376, 530, 641, 749, 749],
          [0, 0, 221, 376]]

    n = len(x1)
    m = len(x2)
    for i in range(n):
        ax1.scatter(x1[i], y1[i], color=SW_global.decisiondot_color, marker='.')
        ax1.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
    for j in range(m):
        ax1.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')

    if SW_global.stokearrow_on_off == 1:
        x4 = [[1031, 675, 1031], [1031, 925], [925, 1031], [925, 925],
              [255], [468, 255], [363, 241],[255, 363], [241, 255], [1256, 1273], [1039, 1256],[1256], [1141, 1256], [1273, 1141],
              [940, 1021, 1021, 940, 940, 1021], [543, 543],[492, 572, 572, 492], [572, 572, 492]]
        y4 = [[651, 650, 651], [651, 723], [576, 651], [723, 576], [825], [1237, 825], [872, 945], [825, 872],[945, 825],
              [823, 953], [1216, 823], [823], [879, 823], [953, 879],[1462, 1462, 1382, 1382, 1302, 1302], [1461, 1301],
              [733, 733, 653, 653], [653, 572, 572]]

        x3 = [[kern_fix + 884], [kern_fix + 885, kern_fix + 884],
              [kern_fix + 962, kern_fix + 815], [kern_fix + 884, kern_fix + 962], [kern_fix + 815, kern_fix + 884],
              [kern_fix + 129, kern_fix + 179, kern_fix + 381, kern_fix + 469, kern_fix + 604, kern_fix + 619],
              [kern_fix + 96, kern_fix + 129, kern_fix + 228],
              [kern_fix + 228, kern_fix + 96],
              [kern_fix + 838, kern_fix + 919, kern_fix + 919, kern_fix + 838, kern_fix + 838, kern_fix + 919],
              [kern_fix + 521, kern_fix + 521]]
        y3 = [[124], [485, 124], [213, 213], [124, 213], [213, 124], [404, 641, 641, 641, 528, 445], [513, 404, 460],
              [460, 513], [735, 735, 655, 655, 575, 575], [454, 294]]

        k = len(x3)
        l = len(x4)
        for e in range(l):
            ax1.plot(x4[e], y4[e], color=SW_global.stokearrow_color_var, linewidth=1)
        for f in range(k):
            ax1.plot(x3[f], y3[f], color=SW_global.stokearrow_color_var, linewidth=1)

    if SW_global.startdot_on_off == 1:
        ax1.plot(752, 1501, marker='.', color=SW_global.startdot_color)
        ax1.plot(kern_fix + 754, 375, marker='.', color=SW_global.startdot_color)
    if SW_global.connectdot_on_off == 1:
        for i in range(n):
            ax1.plot(x1[i], y1[i], color=SW_global.connectingdot_color_var, linewidth=0.5)
        for j in range(m):
            ax1.plot(x2[j], y2[j], color=SW_global.connectingdot_color_var, linewidth=0.5)

    if SW_global.guidelines_toparea == 1:
        ax1.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea, alpha=0.4)
    if SW_global.guidelines_middlearea == 1:
        ax1.axhspan(25, 730, facecolor=SW_global.guidelines_background_color_middlearea, alpha=0.4)
    if SW_global.guidelines_descenderarea == 1:
        ax1.axhspan(-730, -20, facecolor=SW_global.guidelines_background_color_descenderarea, alpha=0.4)

    ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
    ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linestyle=':', linewidth=0.5)
    ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
    ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=FigexFrame_decision_dot)
    canvas.get_tk_widget().grid(row=0, column=1)

    decision_dot_frame1 = Frame(decision_dot_wtp)
    decision_dot_frame1.pack()

    decision_dot_frame2 = Frame(decision_dot_frame1)
    decision_dot_frame2.grid(row=0, column=0)

    decision_dot_chkbx = Checkbutton(decision_dot_frame2, text="Set as Default", font=('manuscript', 9), variable=var)
    decision_dot_chkbx.pack(side=LEFT)

    decision_dot_frame3 = Frame(decision_dot_frame1)
    decision_dot_frame3.grid(row=0, column=1)

    def decision_dot_wtp_close():
        decision_dot_wtp.destroy()
        if SW_global.decisiondot_on_off:
            main()
            decisiondot_already_applied_array.clear()
            main()
        else:
            pass

    decision_dot_button_cancel = ttk.Button(decision_dot_frame3, text="Cancel", command=decision_dot_wtp.destroy)
    decision_dot_button_cancel.pack(side=RIGHT, padx=5)
    decision_dot_button_ok = ttk.Button(decision_dot_frame3, text="OK", command=decision_dot_wtp_close)
    decision_dot_button_ok.pack(side=RIGHT, padx=5, pady=18)

decision_dot_flag_pos = 0

def Decision_dot():
    global decision_dot_flag_pos
    if SW_global.decisiondot_on_off == 1:
        delete_list_counter = len(delete_list)

        if decision_dot_flag_pos == 0:
            for i in range(delete_list_counter):
                glyph = delete_list[i]
                krn = kern_value_array[i]
                decision_dot_flag_pos = decision_dot_flag_pos + 1
                initial_decision_dot_pos = len(guideline_axes[l].lines)

                c1, c2 = manuscript_decision_dot.return_manuscript_decision_dot(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    guideline_axes[l].plot(c1, c2, marker='.', color=SW_global.decisiondot_color, linewidth=0.1)

                else:
                    for ii in range(len(c1)):
                        guideline_axes[l].plot(c1[ii], c2[ii], marker='.', color=SW_global.decisiondot_color,
                                             linewidth=0.1)

                last_decision_dot_pos = len(guideline_axes[l].lines)
                ltn = len(decisiondot_already_applied_array)
                decisiondot_already_applied_array.insert(ltn, initial_decision_dot_pos)
                ltn = len(decisiondot_already_applied_array)
                decisiondot_already_applied_array.insert(ltn, last_decision_dot_pos)
            fig.canvas.draw()

        else:
            for i in range(decision_dot_flag_pos, delete_list_counter):
                glyph = delete_list[i]  # ----> Picking Up 1 glyph
                krn = kern_value_array[i]  # ----> Picking Up it's kern_xvalue
                decision_dot_flag_pos = decision_dot_flag_pos + 1
                initial_decision_dot_pos = len(guideline_axes[l].lines)

                c1, c2 = manuscript_decision_dot.return_manuscript_decision_dot(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    guideline_axes[l].plot(c1, c2, marker='.', color=SW_global.decisiondot_color, linewidth=0.1)

                else:
                    for ii in range(len(c1)):
                        guideline_axes[l].plot(c1[ii], c2[ii], marker='.', color=SW_global.decisiondot_color,
                                             linewidth=0.1)

                last_decision_dot_pos = len(guideline_axes[l].lines)
                ltn = len(decisiondot_already_applied_array)
                decisiondot_already_applied_array.insert(ltn, initial_decision_dot_pos)
                ltn = len(decisiondot_already_applied_array)
                decisiondot_already_applied_array.insert(ltn, last_decision_dot_pos)
            fig.canvas.draw()
        print("check point10")

        fig.canvas.mpl_connect('key_press_event', press)
        fig.canvas.mpl_connect('button_press_event',onclick2)
        fig.canvas.mpl_connect('button_release_event',onrelease)



def decision_dot_continueous_write():
    Decision_dot()



#################### This is for decision dot for multiple guide line ################
def call_decision_dot_for_mul():
    print("This is from call decisiondot for mul")
    print(len(SW_global.axes_data))
    for i in range(len(SW_global.axes_data)):
        print("This is starting of start dot")
        delete_list_temp=[j for j in (SW_global.axes_data[str(i)]["delete_list"])]
        kern_value_array1=[j for j in (SW_global.axes_data[str(i)]["kern_value_array"])]
        letters_already_written1=[j for j in (SW_global.axes_data[str(i)]["letters_already_written"])]
        kern_list1=[j for j in (SW_global.axes_data[str(i)]["kern_list"])]
        decision_dot_flag_pos1=SW_global.axes_data[str(i)]["decision_dot_flag_pos"]
        print(decision_dot_flag_pos1)
        decisiondot_already_applied_array1=[j for j in (SW_global.axes_data[str(i)]["decisiondot_already_applied_array"])]
        axw=SW_global.axes_data[str(i)]["axis_data"]
        print("This is decisiondot_flag",decision_dot_flag_pos1)
        print("This is decisiondot_array",decisiondot_already_applied_array1)
        print("This is deleteList",delete_list_temp)
        print("This is lines",SW_global.axes_data[str(i)]["lines"])
        print("This is end of decision dot")
        decision_dot_For_MultiGuideLine(decision_dot_flag_pos1,delete_list_temp,kern_value_array1,axw,decisiondot_already_applied_array1,str(i),None)
       #print("This is end of start dot")
    return


def decision_dot_For_MultiGuideLine(a,b,c,d,e,f,g):
    decision_dot_flag_pos1=a
    delete_list_temp=b
    kern_value_array1=c
    guideline_axes_plot=d
    decisiondot_already_applied_array1=e
    #print("This is e")
    #print(len(e))
    #print(SW_global.axes_data[f]["decision_dot_flag_pos"])
    print("This is from a from decisin")
    print(a)

    counter=f
    guideline_axes1_lines=[i for i in SW_global.axes_data[f]["lines"]]
    #print("This is guide")
    #print(guideline_axes1_lines)

    if SW_global.decisiondot_on_off == 1:
        delete_list_counter1=len(delete_list_temp)
        if decision_dot_flag_pos1 == 0:
            for i in range(delete_list_counter1):
                glyph=delete_list_temp[i]
                krn=kern_value_array1[i]
                decision_dot_flag_pos1=decision_dot_flag_pos1+1
                initial_decision_dot_pos = len(guideline_axes1_lines)
                c1, c2 = manuscript_decision_dot.return_manuscript_decision_dot(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)
                if draw_type==1:
                    te1=guideline_axes_plot.plot(c1, c2, marker='.', color=SW_global.decisiondot_color, linewidth=0.1)
                    guideline_axes1_lines.append(te1[0])
                else:
                    for ii in range(len(c1)):
                        te1=guideline_axes_plot.plot(c1[ii], c2[ii], marker='.', color=SW_global.decisiondot_color,linewidth=0.1)
                        guideline_axes1_lines.append(te1[0])
                last_decision_dot_pos1 = len(guideline_axes1_lines)
                print("This is len(guideline_axes1_lines)",len(guideline_axes1_lines))
                ltn = len(decisiondot_already_applied_array1)
                decisiondot_already_applied_array1.insert(ltn, initial_decision_dot_pos)
                print("This is decison dot 1st ",decisiondot_already_applied_array1)
                ltn = len(decisiondot_already_applied_array1)
       #             print("This is len")
      #              print(ltn)
                decisiondot_already_applied_array1.insert(ltn, last_decision_dot_pos1)
                print("This is decision dot 2nd",decisiondot_already_applied_array1)
            fig.canvas.draw()
        else:
            for i in range(decision_dot_flag_pos1, delete_list_counter1):
                glyph = delete_list_temp[i]
                krn = kern_value_array1[i]
                decision_dot_flag_pos1 = decision_dot_flag_pos1 + 1
                initial_decision_dot_pos = len(guideline_axes1_lines)
                c1, c2 = manuscript_decision_dot.return_manuscript_decision_dot(glyph)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)
                if draw_type == 1:
                    te1=guideline_axes_plot.plot(c1, c2, marker='.', color=SW_global.decisiondot_color, linewidth=0.1)
                    guideline_axes1_lines.append(te1[0])
                else:
                    for ii in range(len(c1)):
                        te1=guideline_axes_plot.plot(c1[ii], c2[ii], marker='.', color=SW_global.decisiondot_color,
                                             linewidth=0.1)
                        guideline_axes1_lines.append(te1[0])

                last_decision_dot_pos = len(guideline_axes1_lines)
                ltn = len(decisiondot_already_applied_array1)
                decisiondot_already_applied_array1.insert(ltn, initial_decision_dot_pos)
                print("This is decision dot3",decisiondot_already_applied_array1)
     #           print("This is decision dot")
                ltn = len(decisiondot_already_applied_array1)
    #            print(ltn)
                decisiondot_already_applied_array1.insert(ltn, last_decision_dot_pos)
                print("This is desicion dot4",decisiondot_already_applied_array1)
            fig.canvas.draw()
   # print(counter)
    (SW_global.axes_data[f]["lines"]).clear()
    (SW_global.axes_data[f]["gval"]).clear()
    for i in guideline_axes1_lines:
        (SW_global.axes_data[f]["lines"]).append(i)
        (SW_global.axes_data[f]["gval"]).append(i)
   # print("This is axes data old")
    ki=guideline_axes[l].lines
   # print(len(ki))
    ki=SW_global.axes_data[f]["decisiondot_already_applied_array"]
   # print(len(ki))
    #SW_global.axes_data[f].clear()
    (SW_global.axes_data[f]["decisiondot_already_applied_array"]).clear()
    SW_global.axes_data[f]["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array1]
    SW_global.axes_data[f]["decision_dot_flag_pos"]=decision_dot_flag_pos1
   # print("This is after update")
    ki=SW_global.axes_data[f]["decisiondot_already_applied_array"]
   # print(len(ki))
   # print(SW_global.axes_data[f]["decision_dot_flag_pos"])

    return


def decisionDotEraseMultiple():

     # a["letters_already_written"]=[i for i in  SW_global.letters_already_written]
     #            a["kern_value_array"]=[i for i in kern_value_array]
     #            a["delete_list"]=[i for i in delete_list]
     #            a["kern_list"]=[i for i in SW_global.kern_list]
     #            a["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
     #            a["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
     #            a["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
     #            a["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
     #            a["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
     #            a["startdot_flag_pos"]=startdot_flag_pos
     #            a["decision_dot_flag_pos"]=decision_dot_flag_pos
     #            a["connect_dot_flag_pos"]=connect_dot_flag_pos
     #            a["axis_data"]=guideline_axes[l]
     #            print("This is guide line axes .lines",len(guideline_axes[l].lines))
     #            a["lines"]=[i for i in guideline_axes[l].lines]
     #            print("This is check point 3")
     #            a["gval"]=[i for i in SW_global.g_val.lines]
     #            a["cusor_pos"]=[i for i in SW_global.cursor_pos]
     #            a["cursor_data"]=[i for i in SW_global.cursor_data]
    for i in range(len(SW_global.axes_data)):
        print("This is lines")
        k_erase=SW_global.axes_data[str(i)]["lines"]
        print(len(k_erase))
        print(max(SW_global.axes_data[str(i)]["decisiondot_already_applied_array"]))
        print("This is end")
        #for j in SW_global.axes_data[str(i)]["decisiondot_already_applied_array"]:
        #    if(len(k_erase)>j):
        #        k_erase[j].set_visible(False)
        count=0
        for k7 in range(len(SW_global.axes_data[str(i)]["decisiondot_already_applied_array"])-1):
            st_pos=(SW_global.axes_data[str(i)]["decisiondot_already_applied_array"])[k7]
            en_pos=(SW_global.axes_data[str(i)]["decisiondot_already_applied_array"])[k7+1]
            for k6 in range(st_pos,en_pos):
                ((SW_global.axes_data[str(i)]["lines"])[k6]).set_visible(False)
            print(k7)
            print(len(SW_global.axes_data[str(i)]["decisiondot_already_applied_array"]))
            print("check 3")

        (SW_global.axes_data[str(i)]["decisiondot_already_applied_array"]).clear()
        SW_global.axes_data[str(i)]["decision_dot_flag_pos"]=0
    return



##################### End of decision dot for multiple ###########################
def main():
    global initial_decision_dot_pos, last_decision_dot_pos, decision_dot_flag_pos
    if SW_global.decisiondot_on_off == 0:
        SW_global.decisiondot_on_off = 1
        decision_dot_button.configure(background='skyblue')
        call_decision_dot_for_mul()
        Decision_dot()

    else:
        SW_global.decisiondot_on_off = 0
        decision_dot_button.configure(background='#d9d9d9')
        decision_dot_flag_pos = 0
        fln = len(decisiondot_already_applied_array)
        cntr = 0
        decisionDotEraseMultiple()
        for ii in range(fln - 1):
            if cntr == 0:
                x12 = decisiondot_already_applied_array[ii]
                y12 = decisiondot_already_applied_array[ii + 1]
                for jj in range(x12, y12):
                    guideline_axes[l].lines[jj].set_visible(False)
                cntr = cntr + 1
            else:
                cntr = cntr - 1
        fig.canvas.draw()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Connect_Dot_Propaty_Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def connect_dot_menu_wtp():
    connect_dot_wtp = Toplevel(SW_Main_UI)
    connect_dot_wtp.wm_title("Connect dot")
    connect_dot_wtp.geometry("310x210+250+200")
    connect_dot_wtp.resizable(width=False, height=False)
    connect_dot_wtp.wm_transient(SW_Main_UI)
    connect_dot_frame0 = Frame(connect_dot_wtp)
    connect_dot_frame0.pack(pady=10)

    connect_dot_lf = LabelFrame(connect_dot_frame0, text="Stroke Dot Color", font=('manuscript', 9), width=150,
                                height=150)
    connect_dot_lf.pack(side=LEFT, ipady=42, ipadx=4)

    def setBgColor():
        (triple, hexstr) = askcolor()
        SW_global.connectingdot_color_var = hexstr
        if hexstr:
            connect_dot_Color1.config(bg=SW_global.connectingdot_color_var)
            for i in range(n):
                ax1.plot(x1[i], y1[i], color=SW_global.connectingdot_color_var, linewidth=0.5, alpha=1)
            for j in range(m):
                ax1.plot(x2[j], y2[j], color=SW_global.connectingdot_color_var, linewidth=0.5 , alpha=0.8)
                SW_global.connectdot_on_off = 1
            fig.canvas.draw()

    connect_dot_Color1 = tk.Button(connect_dot_lf, bg=SW_global.connectingdot_color_var, text='', width=40, command=setBgColor)
    connect_dot_Color1.config(font=('times', 4))
    connect_dot_Color1.pack(side=LEFT, anchor=N)
    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(connect_dot_lf, width=10, height=20, image=down_icon, command=setBgColor)
    down_button.image = down_icon
    down_button.pack(side=LEFT, anchor=N)

    connect_dot_example = LabelFrame(connect_dot_frame0, text="Example", font=('manuscript', 9), width=150, height=150)
    connect_dot_example.pack(side=RIGHT, ipadx=8, ipady=4)

    FigexFrame_connect_dot = Frame(connect_dot_example, width=20, bd=2, highlightbackground="black",
                                   highlightcolor="black", highlightthickness=1)
    FigexFrame_connect_dot.pack()

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(1, 1)

    base_x = [0, (1500 * 2)]
    base_y = [0, 0]
    median_x = [0, (1500 * 2)]
    median_y = [757, 757]
    descender_x = [0, (1500 * 2)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * 2)]
    ascender_y = [1500, 1500]

    x1 = [[0, 752, 1500], [248, 1251]]
    y1 = [[0, 1501, 0], [496, 495]]
    kern_fix = 1800
    x2 = [[kern_fix + 754, kern_fix + 754],
          [kern_fix + 754, kern_fix + 754],
          [kern_fix + 377], [kern_fix + 0, kern_fix + 0, kern_fix + 222, kern_fix + 377],
          [kern_fix + 377, kern_fix + 221, kern_fix + 0, kern_fix + 0],
          [kern_fix + 755, kern_fix + 755, kern_fix + 640, kern_fix + 528, kern_fix + 377],
          [kern_fix + 377, kern_fix + 528, kern_fix + 755, kern_fix + 755]]
    y2 = [[375, 749],
          [0, 375],
          [749],
          [375, 530, 749, 749],
          [0, 0, 219, 375],
          [376, 530, 641, 749, 749],
          [0, 0, 221, 376]]

    n = len(x1)
    m = len(x2)
    for i in range(n):
        ax1.plot(x1[i], y1[i], color=SW_global.connectingdot_color_var, linewidth=0.5)
    for j in range(m):
        ax1.plot(x2[j], y2[j], color=SW_global.connectingdot_color_var, linewidth=0.5)

    if SW_global.stokearrow_on_off == 1:
        x4 = [[1031, 675, 1031], [1031, 925], [925, 1031], [925, 925],[255], [468, 255], [363, 241],[255, 363],
              [241, 255], [1256, 1273], [1039, 1256],[1256], [1141, 1256], [1273, 1141],[940, 1021, 1021, 940, 940, 1021],
              [543, 543],[492, 572, 572, 492], [572, 572, 492]]
        y4 = [[651, 650, 651], [651, 723], [576, 651], [723, 576], [825], [1237, 825], [872, 945], [825, 872],
              [945, 825], [823, 953], [1216, 823], [823], [879, 823], [953, 879],[1462, 1462, 1382, 1382, 1302, 1302],
              [1461, 1301], [733, 733, 653, 653], [653, 572, 572]]

        x3 = [[kern_fix + 884], [kern_fix + 885, kern_fix + 884],
              [kern_fix + 962, kern_fix + 815], [kern_fix + 884, kern_fix + 962], [kern_fix + 815, kern_fix + 884],
              [kern_fix + 129, kern_fix + 179, kern_fix + 381, kern_fix + 469, kern_fix + 604, kern_fix + 619],
              [kern_fix + 96, kern_fix + 129, kern_fix + 228],
              [kern_fix + 228, kern_fix + 96],
              [kern_fix + 838, kern_fix + 919, kern_fix + 919, kern_fix + 838, kern_fix + 838, kern_fix + 919],
              [kern_fix + 521, kern_fix + 521]]
        y3 = [[124], [485, 124], [213, 213], [124, 213], [213, 124], [404, 641, 641, 641, 528, 445], [513, 404, 460],
              [460, 513], [735, 735, 655, 655, 575, 575], [454, 294]]

        k = len(x3)
        l = len(x4)
        for e in range(l):
            ax1.plot(x4[e], y4[e], color=SW_global.stokearrow_color_var, linewidth=1)
        for f in range(k):
            ax1.plot(x3[f], y3[f], color=SW_global.stokearrow_color_var, linewidth=1)

    if SW_global.startdot_on_off == 1:
        ax1.plot(752, 1501, marker='.', color=SW_global.startdot_color)
        ax1.plot(kern_fix + 754, 375, marker='.', color=SW_global.startdot_color)

    if SW_global.decisiondot_on_off == 1:
        for i in range(n):
            ax1.scatter(x1[i], y1[i], color=SW_global.decisiondot_color, marker='.')

    if SW_global.guidelines_toparea == 1:
        ax1.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea, alpha=0.4)
    if SW_global.guidelines_middlearea == 1:
        ax1.axhspan(25, 730, facecolor=SW_global.guidelines_background_color_middlearea, alpha=0.4)
    if SW_global.guidelines_descenderarea == 1:
        ax1.axhspan(-730, -20, facecolor=SW_global.guidelines_background_color_descenderarea, alpha=0.4)

    ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
    ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linestyle=':', linewidth=0.5)
    ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
    ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=FigexFrame_connect_dot)
    canvas.get_tk_widget().grid(row=0, column=1)

    connect_dot_frame1 = Frame(connect_dot_wtp)
    connect_dot_frame1.pack()

    connect_dot_frame2 = Frame(connect_dot_frame1)
    connect_dot_frame2.grid(row=0, column=0)

    connect_dot_chkbx = Checkbutton(connect_dot_frame2, text="Set as Default", font=('manuscript', 9), variable=var)
    connect_dot_chkbx.pack(side=LEFT)

    connect_dot_frame3 = Frame(connect_dot_frame1)
    connect_dot_frame3.grid(row=0, column=1)

    def connect_dot_wtp_close():
        connect_dot_wtp.destroy()
        main4()

    connect_dot_button_cancel = ttk.Button(connect_dot_frame3, text="Cancel", command=connect_dot_wtp.destroy)
    connect_dot_button_cancel.pack(side=RIGHT, padx=5)
    connect_dot_button_ok = ttk.Button(connect_dot_frame3, text="OK", command=connect_dot_wtp_close)
    connect_dot_button_ok.pack(side=RIGHT, padx=5, pady=18)

connect_dot_flag_pos = 0

####### This is for Multiple guide line with connect dot  #########

def connect_dot_for_multipleGuideLine(a,b,c,d,e,f,g):
    print("This is connection dot for multiple guide line")
    connect_dot_flag_pos1=a
    delete_list_temp=b
    kern_value_array1=c
    guideline_axes1_plot=d
    connectdot_already_applied_array1=e
    print("This is connect dot ")
    print(f)
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)

   # print(len(guideline_axes[l].lines))
   # print(SW_global.axes_data[f]["connect_dot_flag_pos"])
   # print(len(SW_global.axes_data[f]["connectdot_already_applied_array"]))
   # print("This is before updated axes data")
   # print(SW_global.axes_data)
    counter=f
   # print(SW_global.axes_data[f]["lines"])
    guideline_axes1_lines=[i for i in SW_global.axes_data[f]["lines"]]
    print(len(SW_global.axes_data[f]["connectdot_already_applied_array"]))

    if SW_global.connectdot_on_off == 1:
        delete_list_counter = len(delete_list_temp)

        if connect_dot_flag_pos1 == 0:
            for i in range(delete_list_counter):
                glyph = delete_list_temp[i]
                krn = kern_value_array1[i]
                connect_dot_flag_pos1 = connect_dot_flag_pos1 + 1
                initial_connect_dot_pos = len(guideline_axes1_lines)
                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if glyph in skip_list:
                    c1, c2 = manuscript_connect_dot.return_manuscript_fonts(glyph)
                else:
                    x,y=manuscript_connect_dot.return_manuscript_fonts(glyph)
                    c1,c2=font_check(x,y)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    te=d.plot(c1, c2, color=SW_global.connectingdot_color_var, linewidth=0.5)
                    guideline_axes1_lines.append(te[0])
                else:
                    for i in range(len(c1)):
                        te=d.plot(c1[i], c2[i], color=SW_global.connectingdot_color_var, linewidth=0.5)
                        guideline_axes1_lines.append(te[0])

                last_connect_dot_pos = len(guideline_axes1_lines)
                ltn = len(connectdot_already_applied_array1)
                connectdot_already_applied_array1.insert(ltn, initial_connect_dot_pos)
                ltn = len(connectdot_already_applied_array1)
                connectdot_already_applied_array1.insert(ltn, last_connect_dot_pos)
          #  fig.canvas.draw()

        else:
            for i in range(connect_dot_flag_pos1, delete_list_counter):
                glyph = delete_list_temp[i]
                krn = kern_value_array1[i]
                connect_dot_flag_pos1 = connect_dot_flag_pos1 + 1
                initial_connect_dot_pos = len(guideline_axes1_lines)

                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if glyph in skip_list:
                    c1, c2 = manuscript_connect_dot.return_manuscript_fonts(glyph)
                else:
                    x,y=manuscript_connect_dot.return_manuscript_fonts(glyph)
                    c1,c2=font_check(x,y)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    te=d.plot(c1, c2, color=SW_global.connectingdot_color_var, linewidth=0.5)
                    guideline_axes1_lines.append(te[0])
                else:
                    for i in range(len(c1)):
                        te=d.plot(c1, c2, color=SW_global.connectingdot_color_var, linewidth=0.5)
                        guideline_axes1_lines.append(te[0])

                last_connect_dot_pos = len(guideline_axes1_lines)
                ltn = len(connectdot_already_applied_array1)
                connectdot_already_applied_array1.insert(ltn, initial_connect_dot_pos)
                ltn = len(connectdot_already_applied_array1)
                connectdot_already_applied_array1.insert(ltn, last_connect_dot_pos)
        print("This is old array")
        print(len(SW_global.axes_data[f]["lines"]))
        (SW_global.axes_data[f]["lines"]).clear()
        (SW_global.axes_data[f]["gval"]).clear()
        for i in guideline_axes1_lines:
            (SW_global.axes_data[f]["lines"]).append(i)
            (SW_global.axes_data[f]["gval"]).append(i)
        #(SW_global.axes_data[f]["g_val"]).clear()
        #for i in guideline_axes1_lines:
         #   (SW_global.axes_data[f]["g_val"]).append(i)
        print("This is after array")
        print(len(SW_global.axes_data[f]["lines"]))
        ki=guideline_axes[l].lines
        ki=SW_global.axes_data[f]["connectdot_already_applied_array"]
        print("this is old connected dot")
        print(SW_global.axes_data[f]["connectdot_already_applied_array"])
        (SW_global.axes_data[f]["connectdot_already_applied_array"]).clear()
        SW_global.axes_data[f]["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array1]
        print(len(SW_global.axes_data[f]["connectdot_already_applied_array"]))
        SW_global.axes_data[f]["connect_dot_flag_pos"]=connect_dot_flag_pos1
        #print("This is after update")
        ki=SW_global.axes_data[f]["connectdot_already_applied_array"]
        print("This is axes data checking**********************************************************************")
        for i in range(len(SW_global.axes_data)):
            print("This is for ",i)
            print(SW_global.axes_data[str(i)])
        print("This is end**************************************************************************************")
        #print(len(guideline_axes[l].lines))
        #print(SW_global.axes_data[f]["connect_dot_flag_pos"])
        #print(len(SW_global.axes_data[f]["connectdot_already_applied_array"]))
        #print(SW_global.axes_data)
    return





def call_connect_dot_for_multipleGuideLine():
    print("This is from call decisiondot for mul")
    for i in range(len(SW_global.axes_data)):
        print("This is starting point")
        delete_list_temp=[j for j in (SW_global.axes_data[str(i)]["delete_list"])]
        kern_value_array1=[j for j in (SW_global.axes_data[str(i)]["kern_value_array"])]
        letters_already_written1=[j for j in (SW_global.axes_data[str(i)]["letters_already_written"])]
        kern_list1=SW_global.axes_data[str(i)]["kern_list"]
        connect_dot_flag_pos1=SW_global.axes_data[str(i)]["connect_dot_flag_pos"]
        connectdot_already_applied_array1=[j for j in (SW_global.axes_data[str(i)]["connectdot_already_applied_array"])]
        axw=SW_global.axes_data[str(i)]["axis_data"]
        print("This is delete_list_temp",delete_list_temp)
        print("This is kern value array",kern_value_array1)
        #print(letters_already_written1)
        print("This is connect dot flag",connect_dot_flag_pos1)
        print("This is connectdot array",connectdot_already_applied_array1)
        print(axw)
        connect_dot_for_multipleGuideLine(connect_dot_flag_pos1,delete_list_temp,kern_value_array1,axw,connectdot_already_applied_array1,str(i),None)
        print("This is end of call function")



    # print("This is from call decisiondot for mul")
    # print(len(SW_global.axes_data))
    # for i in range(len(SW_global.axes_data)):
    #    # print("This is on selllelellle")
    #     #decision_dot_flag_pos_temp=SW_global.axes_data[str(i)]["decision_dot_flag_pos"]
    #     delete_list_temp=SW_global.axes_data[str(i)]["delete_list"]
    #     kern_value_array1=SW_global.axes_data[str(i)]["kern_value_array"]
    #     letters_already_written1=SW_global.axes_data[str(i)]["letters_already_written"]
    #     kern_list1=SW_global.axes_data[str(i)]["kern_list"]
    #     decision_dot_flag_pos1=SW_global.axes_data[str(i)]["decision_dot_flag_pos"]
    #     decisiondot_already_applied_array1=SW_global.axes_data[str(i)]["decisiondot_already_applied_array"]
    #     axw=SW_global.axes_data[str(i)]["axis_data"]
    #     decision_dot_For_MultiGuideLine(decision_dot_flag_pos1,delete_list_temp,kern_value_array1,axw,decisiondot_already_applied_array1,str(i),None)

    return



def eraseConnectDotFromMultipleGuideLine():
    for i in range(len(SW_global.axes_data)):
        for j in range(len(SW_global.axes_data[str(i)]["connectdot_already_applied_array"])-1):
            st_pos=(SW_global.axes_data[str(i)]["connectdot_already_applied_array"])[j]
            en_pos=(SW_global.axes_data[str(i)]["connectdot_already_applied_array"])[j+1]
            for k7 in range(st_pos,en_pos):
                ((SW_global.axes_data[str(i)]["lines"])[k7]).set_visible(False)
        (SW_global.axes_data[str(i)]["connectdot_already_applied_array"]).clear()
        SW_global.axes_data[str(i)]["connect_dot_flag_pos"]=0

    return



############# End of Multiple guide line with connect dot #########

def connect_dot():
    print("delete_list",delete_list)
    print("This is connect dot",SW_global.connectdot_on_off)
    global connect_dot_flag_pos
    if SW_global.connectdot_on_off == 1:
        delete_list_counter = len(delete_list)

        if connect_dot_flag_pos == 0:
            for i in range(delete_list_counter):
                glyph = delete_list[i]
                krn = kern_value_array[i]
                connect_dot_flag_pos = connect_dot_flag_pos + 1
                initial_connect_dot_pos = len(guideline_axes[l].lines)

                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if glyph in skip_list:
                    c1, c2 = manuscript_connect_dot.return_manuscript_fonts(glyph)
                else:
                    x,y=manuscript_connect_dot.return_manuscript_fonts(glyph)
                    c1,c2=font_check(x,y)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    my_draw_connect_dot(c1, c2)
                else:
                    for i in range(len(c1)):
                        my_draw_connect_dot(c1[i], c2[i])

                last_connect_dot_pos = len(guideline_axes[l].lines)
                ltn = len(connectdot_already_applied_array)
                connectdot_already_applied_array.insert(ltn, initial_connect_dot_pos)
                ltn = len(connectdot_already_applied_array)
                connectdot_already_applied_array.insert(ltn, last_connect_dot_pos)
            fig.canvas.draw()

        else:
            for i in range(connect_dot_flag_pos, delete_list_counter):
                glyph = delete_list[i]
                krn = kern_value_array[i]
                connect_dot_flag_pos = connect_dot_flag_pos + 1
                initial_connect_dot_pos = len(guideline_axes[l].lines)

                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if glyph in skip_list:
                    c1, c2 = manuscript_connect_dot.return_manuscript_fonts(glyph)
                else:
                    x,y=manuscript_connect_dot.return_manuscript_fonts(glyph)
                    c1,c2=font_check(x,y)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, krn)

                if draw_type == 1:
                    my_draw_connect_dot(c1, c2)
                else:
                    for i in range(len(c1)):
                        my_draw_connect_dot(c1[i], c2[i])

                last_connect_dot_pos = len(guideline_axes[l].lines)
                ltn = len(connectdot_already_applied_array)
                connectdot_already_applied_array.insert(ltn, initial_connect_dot_pos)
                ltn = len(connectdot_already_applied_array)
                connectdot_already_applied_array.insert(ltn, last_connect_dot_pos)
            fig.canvas.draw()
    print("check point 11")
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event',onclick2)
    fig.canvas.mpl_connect('button_release_event',onrelease)




def connect_dot_continueous_write():
    connect_dot()


def main4():
    global initial_connect_dot_pos, last_connect_dot_pos, connect_dot_flag_pos

    if SW_global.connectdot_on_off == 0:
        SW_global.connectdot_on_off = 1
        connect_dot_button.configure(background='skyblue')
        call_connect_dot_for_multipleGuideLine()
        connect_dot()
    else:
        SW_global.connectdot_on_off = 0
        connect_dot_button.configure(background='#d9d9d9')
        connect_dot_flag_pos = 0
        eraseConnectDotFromMultipleGuideLine()
        fln = len(connectdot_already_applied_array)
        cntr = 0
        for ii in range(fln - 1):
            if cntr == 0:
                x12 = connectdot_already_applied_array[ii]
                y12 = connectdot_already_applied_array[ii + 1]
                for jj in range(x12, y12):
                    guideline_axes[l].lines[jj].set_visible(False)
                cntr = cntr + 1
            else:
                cntr = cntr - 1
        fig.canvas.draw()


def my_draw_connect_dot(c1, c2):
    guideline_axes[l].plot(c1, c2, color=SW_global.connectingdot_color_var, linewidth=0.5)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><< Color_Letter_Propaty_Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def color_letter_menu_wtp():
    color_letter_wtp = Toplevel(SW_Main_UI)
    color_letter_wtp.wm_title("Color letter")
    color_letter_wtp.geometry("250x550+450+50")
    color_letter_wtp.resizable(width=False, height=False)
    color_letter_wtp.wm_transient(SW_Main_UI)

    color_letter_frame1 = Frame(color_letter_wtp)
    color_letter_frame1.pack()

    color_letter_grid_frame1 = Frame(color_letter_frame1, width=250, height=30)
    color_letter_grid_frame1.grid(row=0, column=0, pady=10)
    color_letter_grid_frame2 = Frame(color_letter_frame1, width=250, height=30)
    color_letter_grid_frame2.grid(row=1, column=0, pady=15)
    color_letter_grid_frame3 = Frame(color_letter_frame1, width=250, height=30)
    color_letter_grid_frame3.grid(row=2, column=0, pady=20)
    color_letter_grid_frame4 = Frame(color_letter_frame1, width=250, height=30)
    color_letter_grid_frame4.grid(row=3, column=0, pady=20)
    color_letter_grid_frame5 = Frame(color_letter_frame1, width=250, height=30)
    color_letter_grid_frame5.grid(row=4, column=0, pady=20)

    color_color_name_lbl_Left = Label(color_letter_grid_frame1, text="Stroke", justify="left", font=('manuscript', 10), width=15)
    color_color_name_lbl_Left.pack(side='left')
    color_color_name_lbl_Right = Label(color_letter_grid_frame1, text="Color", font=('manuscript', 10), width=15)
    color_color_name_lbl_Right.pack(side='left')

    # For 1st part of color letter
    Color_firstcolor_Frame_name = Frame(color_letter_grid_frame2)
    Color_firstcolor_Frame_name.pack(side='left')

    color_firstcolor_name_lbl = Label(Color_firstcolor_Frame_name, text="First", font=('manuscript', 10), width=10)
    color_firstcolor_name_lbl.pack(anchor=W)

    Color_firstcolor_Frame_bgwn = Frame(color_letter_grid_frame2, bd=1, relief=SUNKEN)
    Color_firstcolor_Frame_bgwn.pack(side='left')

    def setBgColor_bgwn():
        (triple, hexstr1) = askcolor()
        SW_global.first_letter_background_color = hexstr1

        if hexstr1:
            SW_global.firstline_color = True
            Color_firstarea1.config(bg=SW_global.first_letter_background_color)
            for i in range(len(x)):
                if i == 0:
                    x11 = x[i]
                    y11 = y[i]
                    ax1.plot(x11, y11, color=SW_global.first_letter_background_color, dashes=(4, 2), linewidth=0.7)
            fig.canvas.draw()

    Color_firstarea1 = tk.Button(Color_firstcolor_Frame_bgwn, bg=SW_global.first_letter_background_color, text='', width=40, command=setBgColor_bgwn)
    Color_firstarea1.config(font=('times', 4))
    Color_firstarea1.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Color_firstcolor_Frame_bgwn, width=10, height=20, image=down_icon, command=setBgColor_bgwn)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    # For 2nd part of color letter
    Color_secondcolor_Frame_name = Frame(color_letter_grid_frame3)
    Color_secondcolor_Frame_name.pack(side='left')

    color_secondcolor_name_lbl = Label(Color_secondcolor_Frame_name, text="Second", font=('manuscript', 10), width=10)
    color_secondcolor_name_lbl.pack(anchor=W)

    Color_secondcolor_Frame_bgwn = Frame(color_letter_grid_frame3, bd=1, relief=SUNKEN)
    Color_secondcolor_Frame_bgwn.pack(side='left')

    def setBgColor_bgwn():
        (triple, hexstr1) = askcolor()
        SW_global.second_letter_background_color = hexstr1
        print(SW_global.second_letter_background_color)

        if hexstr1:
            SW_global.secondline_color = True
            Color_secondarea1.config(bg=SW_global.second_letter_background_color)
            for i in range(len(x)):
                if i == 1:
                    x11 = x[i]
                    y11 = y[i]
                    ax1.plot(x11, y11, color=SW_global.second_letter_background_color,dashes=(4, 2), linewidth=0.7)
            fig.canvas.draw()
    Color_secondarea1 = tk.Button(Color_secondcolor_Frame_bgwn, bg=SW_global.second_letter_background_color, text='', width=40
                                ,command=setBgColor_bgwn)
    Color_secondarea1.config(font=('times', 4))
    Color_secondarea1.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Color_secondcolor_Frame_bgwn, width=10, height=20, image=down_icon, command=setBgColor_bgwn)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    # For 3rd part of color letter
    Color_thirdcolor_Frame_name = Frame(color_letter_grid_frame4)
    Color_thirdcolor_Frame_name.pack(side='left')

    color_thirdcolor_name_lbl = Label(Color_thirdcolor_Frame_name, text="Third", font=('manuscript', 10), width=10)
    color_thirdcolor_name_lbl.pack(anchor=W)

    Color_thirdcolor_Frame_bgwn = Frame(color_letter_grid_frame4, bd=1, relief=SUNKEN)
    Color_thirdcolor_Frame_bgwn.pack(side='left')

    def setBgColor_bgwn():
        (triple, hexstr1) = askcolor()
        SW_global.third_letter_background_color = hexstr1
        print(SW_global.third_letter_background_color)

        if hexstr1:
            SW_global.thirdline_color = True
            Color_thirdarea1.config(bg=SW_global.third_letter_background_color)
            for i in range(len(x)):
                if i == 2:
                    x11 = x[i]
                    y11 = y[i]
                    ax1.plot(x11, y11, color=SW_global.third_letter_background_color,dashes=(4, 3), linewidth=0.7)
            fig.canvas.draw()

    Color_thirdarea1 = tk.Button(Color_thirdcolor_Frame_bgwn, bg=SW_global.third_letter_background_color, text='', width=40
                                ,command=setBgColor_bgwn)
    Color_thirdarea1.config(font=('times', 4))
    Color_thirdarea1.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Color_thirdcolor_Frame_bgwn, width=10, height=20, image=down_icon, command=setBgColor_bgwn)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    # For 4th part of color letter
    Color_forthcolor_Frame_name = Frame(color_letter_grid_frame5)
    Color_forthcolor_Frame_name.pack(side='left')

    color_forthcolor_name_lbl = Label(Color_forthcolor_Frame_name, text="Fourth", font=('manuscript', 10), width=10)
    color_forthcolor_name_lbl.pack(anchor=W)

    Color_forthcolor_Frame_bgwn = Frame(color_letter_grid_frame5, bd=1, relief=SUNKEN)
    Color_forthcolor_Frame_bgwn.pack(side='left')

    def setBgColor_bgwn():
        (triple, hexstr1) = askcolor()
        SW_global.forth_letter_background_color = hexstr1
        print(SW_global.forth_letter_background_color)

        if hexstr1:
            SW_global.forthline_color = True
            Color_fortharea1.config(bg=SW_global.forth_letter_background_color)
            for i in range(len(x)):
                if i > 2:
                    x11 = x[i]
                    y11 = y[i]
                    ax1.plot(x11, y11, color=SW_global.forth_letter_background_color,dashes=(4, 2), linewidth=0.7)
            fig.canvas.draw()

    Color_fortharea1 = tk.Button(Color_forthcolor_Frame_bgwn, bg=SW_global.forth_letter_background_color, text='', width=40
                                ,command=setBgColor_bgwn)
    Color_fortharea1.config(font=('times', 4))
    Color_fortharea1.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Color_forthcolor_Frame_bgwn, width=10, height=20, image=down_icon, command=setBgColor_bgwn)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    ExampleFrame1 = Frame(color_letter_wtp, width=250)
    ExampleFrame1.pack(pady=10)

    Examplelabel1 = Label(ExampleFrame1, text="Example", font=('manuscript', 9))
    Examplelabel1.pack(padx=20)

    FigexFrame = Frame(color_letter_wtp, width=250, bd=2, highlightbackground="black", highlightcolor="black",
                       highlightthickness=1)
    FigexFrame.pack(padx=20)

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(2, 1)

    base_x = [0, (1500 * 5)]
    base_y = [0, 0]
    median_x = [0, (1500 * 5)]
    median_y = [757, 757]
    descender_x = [0, (1500 * 5)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * 5)]
    ascender_y = [1500, 1500]

    x = [[0, 0], [0, 751], [751, 1495], [1495, 1495]]
    y = [[0, 1500], [1500, 0], [0, 1500], [1500, 0]]

    for i in range(len(x)):
        if i == 0:
            x11 = x[i]
            y11 = y[i]
            ax1.plot(x11, y11, color=SW_global.first_letter_background_color, dashes=(4, 2), linewidth=0.7)
        elif i == 1:
            x11 = x[i]
            y11 = y[i]
            ax1.plot(x11, y11, color=SW_global.second_letter_background_color, dashes=(4, 2), linewidth=0.7)
        elif i == 2:
            x11 = x[i]
            y11 = y[i]
            ax1.plot(x11, y11, color=SW_global.third_letter_background_color, dashes=(4, 3), linewidth=0.7)
        else:
            x11 = x[i]
            y11 = y[i]
            ax1.plot(x11, y11, color=SW_global.forth_letter_background_color, dashes=(4, 2), linewidth=0.7)


    if SW_global.startdot_on_off == 1:
        ax1.plot(752, 1501, marker='.', color=SW_global.startdot_color)
        ax1.plot(kern_fix + 754, 375, marker='.', color=SW_global.startdot_color)

    if SW_global.decisiondot_on_off == 1:
        for i in range(n):
            ax1.scatter(x1[i], y1[i], color=SW_global.decisiondot_color, marker='.')
    if SW_global.connectdot_on_off == 1:
        for i in range(n):
            ax1.plot(x1[i], y1[i], color=SW_global.connectingdot_color_var, linewidth=0.5)
        for j in range(m):
            ax1.plot(x2[j], y2[j], color=SW_global.connectingdot_color_var, linewidth=0.5)

    ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
    ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linestyle=':', linewidth=0.5)
    ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
    ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)

    if SW_global.guidelines_toparea == 1:
        axhspan_top = ax1.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea, alpha=0.4)

    if SW_global.guidelines_middlearea == 1:
        axhspan_middle = ax1.axhspan(25, 730, facecolor=SW_global.guidelines_background_color_middlearea, alpha=0.4)

    if SW_global.guidelines_descenderarea == 1:
        axhspan_descender = ax1.axhspan(-730, -20, facecolor=SW_global.guidelines_background_color_descenderarea, alpha=0.4)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=FigexFrame)
    canvas.get_tk_widget().grid(row=0, column=1)

    backgroundEndFrame = Frame(color_letter_wtp)
    backgroundEndFrame.pack()

    backgroundEndchkFrame = Frame(backgroundEndFrame)
    backgroundEndchkFrame.grid(row=0, column=0)

    backgroundEndokcnlFrame = Frame(backgroundEndFrame)
    backgroundEndokcnlFrame.grid(row=1, column=0)

    background_chkbx = Checkbutton(backgroundEndchkFrame, text="Set as Default", variable=var, font=('manuscript', 9))
    background_chkbx.pack(padx=10, pady=20)

    def background_close():
        global color_letter_features_on_off, color_letter_flag_pos, color_letter_remove_redraw
        color_letter_wtp.destroy()
        try:
            SW_global.single_click_data.set_visible(True)
        except Exception as e:
            print(e)
            pass
        if color_letter_features_on_off:
            color_letter_remove_redraw = 1
            main12345()
            color_letter_already_applied_array.clear()
            color_letter_flag_pos = 0
            color_letter_remove_redraw = 0
            try:
                SW_global.single_click_data.set_visible(True)
            except Exception as e:
                print(e)
                pass
            main12345()
            try:
                SW_global.single_click_data.set_visible(True)
            except Exception as e:
                print(e)
                pass

    background_button_cancel = ttk.Button(backgroundEndokcnlFrame, text="Cancel", command=color_letter_wtp.destroy)
    background_button_cancel.pack(side=RIGHT, padx=10, pady=2, anchor=E)
    background_button_ok = ttk.Button(backgroundEndokcnlFrame,
                                      text="OK",
                                      command=background_close)
    background_button_ok.pack(side=RIGHT, pady=2, anchor=E)


color_letter_flag_pos = 0
color_letter_features_on_off = 0
color_letter_already_applied_array = []
color_letter_remove_redraw = 0

def color_letters_draw_fun():
    global color_letter_flag_pos, color_letter_features_on_off, d1, d2, alp

    if color_letter_flag_pos == 0:
        temp_recent_input_list = []
        temp_recent_input_list.extend(delete_list)

        while len(delete_list) > 0:
            len1 = len(SW_global.letters_already_written)
            len2 = len1 - 1
            srt_loop = SW_global.letters_already_written[len2 - 1]
            end_loop = SW_global.letters_already_written[len2]
            for i in range(srt_loop, end_loop):
                guideline_axes[l].lines[i].set_visible(False)

            if len(SW_global.letters_already_written) != 0:
                del SW_global.letters_already_written[len1 - 1]
                del SW_global.letters_already_written[len1 - 2]

                last_input_len = len(delete_list)
                last_glyph = delete_list[last_input_len - 1]
                del delete_list[last_input_len - 1]
                l12 = len(kern_value_array)
                del kern_value_array[l12 - 1]
        fig.canvas.draw()

        # clearing List
        SW_global.recent_input_list.clear()
        kern_value_array.clear()
        SW_global.letters_already_written.clear()
        delete_list.clear()

        # making kern value 0 for fresh starting
        SW_global.kern_list.insert(0, 0)
        kern_value_array.insert(0, 0)

        for itr in range(len(temp_recent_input_list)):
            color_letter_flag_pos = color_letter_flag_pos + 1
            length12 = len(SW_global.recent_input_list)
            user_input = temp_recent_input_list[itr]
            x_max = manuscript.x_max[user_input]
            kern_x = SW_global.kern_list[0]
            skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
            if user_input in skip_list:
                c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
            else:
                x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                c1,c2=font_check(x,y)
            c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, kern_x)
            kern_x = SW_global.kern_list[0] + x_max + 300
            SW_global.kern_list.insert(0, kern_x)

            kern_counter = len(kern_value_array)
            kern_value_array.insert(kern_counter, kern_x)
            SW_global.recent_input_list.insert(length12, user_input)
            delete_list.insert(length12, user_input)

            init_enrty_pos = len(SW_global.letters_already_written)
            inti_letter_pos = len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)

            if draw_type == 1:
                guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7,
                                       dashes=(d1, d2), alpha=alp)

            else:
                n = len(c1)
                for i in range(n):
                    if i == 0:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7,
                                               dashes=(d1, d2), alpha=alp)
                    if i == 1:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7,
                                               dashes=(d1, d2), alpha=alp)
                    if i == 2:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7,
                                               dashes=(d1, d2), alpha=alp)
                    if i == 3:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7,
                                               dashes=(d1, d2), alpha=alp)

                final_enrty_pos = len(SW_global.letters_already_written)
                final_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)

        fig.canvas.draw()
        temp_recent_input_list.clear()

    else:
        for itr in range(len(SW_global.letters_already_written)):
            color_letter_flag_pos = color_letter_flag_pos + 1
            length12 = len(SW_global.recent_input_list)
            user_input = SW_global.letters_already_written[itr]
            x_max = manuscript.x_max[user_input]
            kern_x = SW_global.kern_list[0]
            skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
            if user_input in skip_list:
                c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
            else:
                x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                c1.c2=font_check(x,y)
            c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, kern_x)
            kern_x = SW_global.kern_list[0] + x_max + 300
            SW_global.kern_list.insert(0, kern_x)

            kern_counter = len(kern_value_array)
            kern_value_array.insert(kern_counter, kern_x)
            SW_global.recent_input_list.insert(length12, user_input)
            delete_list.insert(length12, user_input)

            init_enrty_pos = len(SW_global.letters_already_written)
            inti_letter_pos = len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)

            if draw_type == 1:
                guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7,
                                       dashes=(d1, d2), alpha=alp)

            else:
                n = len(c1)
                for i in range(n):
                    if i == 0:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color,
                                               linewidth=0.7,
                                               dashes=(d1, d2), alpha=alp)
                    if i == 1:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color,
                                               linewidth=0.7,
                                               dashes=(d1, d2), alpha=alp)
                    if i == 2:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color,
                                               linewidth=0.7,
                                               dashes=(d1, d2), alpha=alp)
                    if i == 3:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color,
                                               linewidth=0.7,
                                               dashes=(d1, d2), alpha=alp)

                final_enrty_pos = len(SW_global.letters_already_written)
                final_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
   # visible=SW_global.cursor_data[len(SW_global.cursor_data)-1]
   # print(visible)
    #visible.set_visible(True)
    for i in SW_global.cursor_data:
        i.set_visible(False)
    if(SW_global.single_click_data!=None):
        SW_global.single_click_data.set_visible(True)
    fig.canvas.draw()
    print("check point12")
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event',onclick2)
    fig.canvas.mpl_connect('button_release_event',onrelease)



def color_letter_continues_write():
    color_letters_draw_fun()
    try:
        SW_global.single_click_data.set_visible(True)
    except Exception as e:
        print(e)
        pass

def main12345():
    global color_letter_flag_pos, color_letter_features_on_off
    global d1, d2, letter_dot_density_no_dot_on_off, alp, temp_alp
    global color_letter_remove_redraw
    print("This is main 12345")

    if color_letter_features_on_off == 0:
        color_letter_features_on_off = 1
        color_letter_button.configure(background='skyblue')
        color_letters_draw_fun()
        try:
            SW_global.single_click_data.set_visible(True)
        except Exception as e:
            print(e)
            pass

    else:
        color_letter_features_on_off = 0
        color_letter_button.configure(background='#d9d9d9')
        color_letter_flag_pos = 0
        fln = len(color_letter_already_applied_array)
        cntr = 0
        for ii in range(fln - 1):
            if cntr == 0:
                x12 = color_letter_already_applied_array[ii]
                y12 = color_letter_already_applied_array[ii + 1]
                for jj in range(x12, y12):
                    guideline_axes[l].lines[jj].set_visible(False)
                fig.canvas.draw()
                cntr = cntr + 1
            else:
                cntr = cntr - 1

        if color_letter_remove_redraw == 0:
            # Redraw all letters in black after color letter features is Off
            temp_recent_input_list = []
            temp_recent_input_list.extend(delete_list)

            while len(delete_list) > 0:
                len1 = len(SW_global.letters_already_written)
                len2 = len1 - 1
                srt_loop = SW_global.letters_already_written[len2 - 1]
                end_loop = SW_global.letters_already_written[len2]
                for i in range(srt_loop, end_loop):
                    guideline_axes[l].lines[i].set_visible(False)

                if len(SW_global.letters_already_written) != 0:
                    del SW_global.letters_already_written[len1 - 1]
                    del SW_global.letters_already_written[len1 - 2]

                    last_input_len = len(delete_list)
                    last_glyph = delete_list[last_input_len - 1]
                    del delete_list[last_input_len - 1]
                    l12 = len(kern_value_array)
                    del kern_value_array[l12 - 1]
            fig.canvas.draw()

            # clearing List
            SW_global.recent_input_list.clear()
            kern_value_array.clear()
            SW_global.letters_already_written.clear()
            delete_list.clear()

            # making kern value 0 for fresh starting
            SW_global.kern_list.insert(0, 0)
            kern_value_array.insert(0, 0)

            for itr in range(len(temp_recent_input_list)):
                length12 = len(SW_global.recent_input_list)
                user_input = temp_recent_input_list[itr]
                x_max = manuscript.x_max[user_input]
                kern_x = SW_global.kern_list[0]
                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if user_input in skip_list:
                    c1, c2 = manuscript.return_manuscript_fonts(user_input)
                else:
                    x,y=manuscript.return_manuscript_fonts(user_input)
                    c1,c2=font_check(x,y)
                c1, c2, draw_type = Kern_add_help.kern_add_operation(c1, c2, kern_x)
                kern_x = SW_global.kern_list[0] + x_max + 300
                SW_global.kern_list.insert(0, kern_x)

                kern_counter = len(kern_value_array)
                kern_value_array.insert(kern_counter, kern_x)
                SW_global.recent_input_list.insert(length12, user_input)
                delete_list.insert(length12, user_input)
                init_enrty_pos = len(SW_global.letters_already_written)
                inti_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)

                if draw_type == 1:
                    if letter_dot_density_no_dot_on_off == 1:
                        alp = 0
                    else:
                        alp = temp_alp
                    guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

                else:
                    n = len(c1)
                    if letter_dot_density_no_dot_on_off == 1:
                        alp = 0
                    else:
                        alp = temp_alp
                    for i in range(n):
                        guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

                final_enrty_pos = len(SW_global.letters_already_written)
                final_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
            q22=SW_global.cursor_data[len(SW_global.cursor_data)-1]
            #q22.set_visible(True)
                #SW_global.cursor_data[len(SW_global.cursor_data)-1].set_visible(True)

            fig.canvas.draw()
            temp_recent_input_list.clear()
            print("This is end ")
            SW_global.single_click_data.set_visible(True)


        else:
            print("No Need To Draw it with Black !!")
        try:
            SW_global.single_click_data.set_visible(True)
        except Exception as e:
            print(e)
            pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Back_Ground_Color_Propaty_Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
val12 = tk.IntVar()  # background_menu_wtp variable
val12.set(0)

v12 = tk.IntVar()  # background_menu_wtp variable
v12.set(0)

val13 = tk.IntVar()  # background_menu_wtp variable
val13.set(0)

v13 = tk.IntVar()  # background_menu_wtp variable
v13.set(0)

val14 = tk.IntVar()  # background_menu_wtp variable
val14.set(0)

v14 = tk.IntVar()  # background_menu_wtp variable
v14.set(0)

def background_menu_wtp():
    background_wtp = Toplevel(SW_Main_UI)
    background_wtp.wm_title("Area Highlight")
    background_wtp.geometry("310x550+450+50")
    background_wtp.resizable(width=False, height=False)
    background_wtp.wm_transient(SW_Main_UI)

    bgwn_frame0 = Frame(background_wtp)
    bgwn_frame0.pack(pady=10)

    bgwn_lf = LabelFrame(bgwn_frame0, text="Top Area")
    bgwn_lf.pack(side=LEFT, ipady=1, ipadx=10)

    bgwn_frame1 = Frame(bgwn_lf)
    bgwn_frame1.pack(side=LEFT)

    def tpcl1():
        if v12.get() == 0:
            SW_global.guidelines_toparea = 0
            axhspan_top = ax1.axhspan(790, 1460, facecolor='#ffffff')
            fig.canvas.draw()
        elif v12.get() == 1:
            SW_global.guidelines_toparea = 1
            axhspan_top = ax1.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea, alpha=0.4)
            toparea_flag = True
        fig.canvas.draw()

    option_bgwn = [("Off"), ("On")]
    for val12, option_bgwn in enumerate(option_bgwn):
        option_rb_bgwn = tk.Radiobutton(bgwn_frame1, text=option_bgwn, variable=v12, value=val12,
                                        font=('manuscript', 9), command=tpcl1)
        option_rb_bgwn.pack(ipady=10)

    Color_Toparea_bgwn = LabelFrame(bgwn_lf, text="Color", font=('manuscript', 9))
    Color_Toparea_bgwn.pack(side=RIGHT, ipady=6, ipadx=20, padx=4, pady=2)

    Color_Toparea_Frame_bgwn = Frame(Color_Toparea_bgwn, bd=1, relief=SUNKEN)
    Color_Toparea_Frame_bgwn.pack()

    def setBgColor_bgwn():
        (triple, hexstr1) = askcolor()
        SW_global.guidelines_background_color_toparea = hexstr1
        if SW_global.guidelines_background_color_toparea != '#ffffff':
            axhspan_top = ax1.axhspan(790, 1460, facecolor='#ffffff')
            SW_global.guidelines_background_color_toparea = hexstr1
        else:
            SW_global.guidelines_background_color_toparea = hexstr1

        if hexstr1:
            v12.set(0)
            Color_Toparea1.config(bg=SW_global.guidelines_background_color_toparea)

        fig.canvas.draw()

    Color_Toparea1 = tk.Button(Color_Toparea_Frame_bgwn, bg=SW_global.guidelines_background_color_toparea, text='', width=40,
                               command=setBgColor_bgwn)
    Color_Toparea1.config(font=('times', 4))
    Color_Toparea1.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Color_Toparea_Frame_bgwn, width=10, height=20, image=down_icon, command=setBgColor_bgwn)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    bgwn_frame2 = Frame(background_wtp)
    bgwn_frame2.pack(pady=5)

    bgwn_lf1 = LabelFrame(bgwn_frame2, text="Middle Area")
    bgwn_lf1.pack(side=LEFT, ipady=1, ipadx=10)

    bgwn_frame3 = Frame(bgwn_lf1)
    bgwn_frame3.pack(side=LEFT)

    def mdcl1():
        if v13.get() == 0:
            SW_global.guidelines_middlearea = 0
            axhspan_Middle = ax1.axhspan(25, 730, facecolor='#ffffff')
        else:
            SW_global.guidelines_middlearea = 1
            axhspan_Middle = ax1.axhspan(25, 730, facecolor=SW_global.guidelines_background_color_middlearea, alpha=0.4)
        fig.canvas.draw()

    option_bgwn = [("Off"), ("On")]
    for val13, option_bgwn in enumerate(option_bgwn):
        option_rb_bgwn = tk.Radiobutton(bgwn_frame3, text=option_bgwn, variable=v13, value=val13,
                                        font=('manuscript', 9),command=mdcl1)
        option_rb_bgwn.pack(ipady=10)

    Color_Middlearea_bgwn = LabelFrame(bgwn_lf1, text="Color", font=('manuscript', 9))
    Color_Middlearea_bgwn.pack(side=RIGHT, ipady=6, ipadx=20, padx=4, pady=2)

    Color_Middlearea_Frame_bgwn = Frame(Color_Middlearea_bgwn, bd=1, relief=SUNKEN)
    Color_Middlearea_Frame_bgwn.pack()

    def setBgColor_bgwn():
        (triple, hexstr2) = askcolor()
        SW_global.guidelines_background_color_middlearea = hexstr2
        if hexstr2:
            Color_Middlearea1.config(bg=SW_global.guidelines_background_color_middlearea)
            fig.canvas.draw()

    Color_Middlearea1 = tk.Button(Color_Middlearea_Frame_bgwn, bg=SW_global.guidelines_background_color_middlearea, text='',
                                  width=40, command=setBgColor_bgwn)
    Color_Middlearea1.config(font=('times', 4))
    Color_Middlearea1.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Color_Middlearea_Frame_bgwn, width=10, height=20, image=down_icon, command=setBgColor_bgwn)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    bgwn_frame4 = Frame(background_wtp)
    bgwn_frame4.pack(pady=5)

    bgwn_lf2 = LabelFrame(bgwn_frame4, text="Descender Area")
    bgwn_lf2.pack(side=LEFT, ipady=1, ipadx=10)

    bgwn_frame5 = Frame(bgwn_lf2)
    bgwn_frame5.pack(side=LEFT)

    def dccl1():
        if v14.get() == 0:
            SW_global.guidelines_descenderarea = 0
            axhspan_descender = ax1.axhspan(-730, -20, facecolor='#ffffff')
        else:
            SW_global.guidelines_descenderarea = 1
            axhspan_descender = ax1.axhspan(-730, -20, facecolor=SW_global.guidelines_background_color_descenderarea, alpha=0.4)
        fig.canvas.draw()

    option_bgwn = [("Off"), ("On")]
    for val14, option_bgwn in enumerate(option_bgwn):
        option_rb_bgwn = tk.Radiobutton(bgwn_frame5, text=option_bgwn, variable=v14, value=val14,
                                        font=('manuscript', 9),command=dccl1)
        option_rb_bgwn.pack(ipady=10)

    Color_Descenderarea_bgwn = LabelFrame(bgwn_lf2, text="Color", font=('manuscript', 9))
    Color_Descenderarea_bgwn.pack(side=RIGHT, ipady=6, ipadx=20, padx=4, pady=2)

    Color_Descenderarea_Frame_bgwn = Frame(Color_Descenderarea_bgwn, bd=1, relief=SUNKEN)
    Color_Descenderarea_Frame_bgwn.pack()

    def setBgColor_bgwn():
        (triple, hexstr3) = askcolor()
        SW_global.guidelines_background_color_descenderarea = hexstr3
        if hexstr3:
            Color_Descenderarea1.config(bg=SW_global.guidelines_background_color_descenderarea)
            fig.canvas.draw()

    Color_Descenderarea1 = tk.Button(Color_Descenderarea_Frame_bgwn, bg=SW_global.guidelines_background_color_descenderarea,
                                     text='', width=40,
                                     command=setBgColor_bgwn)
    Color_Descenderarea1.config(font=('times', 4))
    Color_Descenderarea1.pack(side=LEFT)

    down_icon = tk.PhotoImage(file="icons/d11.png")
    down_button = tk.Button(Color_Descenderarea_Frame_bgwn, width=10, height=20, image=down_icon,
                            command=setBgColor_bgwn)
    down_button.image = down_icon
    down_button.pack(side=LEFT)

    ExampleFrame1 = Frame(background_wtp, width=440)
    ExampleFrame1.pack(anchor=W)

    Examplelabel1 = Label(ExampleFrame1, text="Example", font=('manuscript', 9))
    Examplelabel1.pack(padx=20)

    FigexFrame = Frame(background_wtp, width=440, bd=2, highlightbackground="black", highlightcolor="black",
                       highlightthickness=1)
    FigexFrame.pack(padx=20)

    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(2, 1)

    base_x = [0, (1500 * 5)]
    base_y = [0, 0]
    median_x = [0, (1500 * 5)]
    median_y = [757, 757]
    descender_x = [0, (1500 * 5)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * 5)]
    ascender_y = [1500, 1500]

    x1 = [[0, 752, 1500], [248, 1251]]
    y1 = [[0, 1501, 0], [496, 495]]
    kern_fix = 1800
    x2 = [[kern_fix + 754, kern_fix + 754],
          [kern_fix + 754, kern_fix + 754],
          [kern_fix + 377], [kern_fix + 0, kern_fix + 0, kern_fix + 222, kern_fix + 377],
          [kern_fix + 377, kern_fix + 221, kern_fix + 0, kern_fix + 0],
          [kern_fix + 755, kern_fix + 755, kern_fix + 640, kern_fix + 528, kern_fix + 377],
          [kern_fix + 377, kern_fix + 528, kern_fix + 755, kern_fix + 755]]
    y2 = [[375, 749],
          [0, 375],
          [749],
          [375, 530, 749, 749],
          [0, 0, 219, 375],
          [376, 530, 641, 749, 749],
          [0, 0, 221, 376]]

    n = len(x1)
    m = len(x2)
    for i in range(n):
        ax1.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
    for j in range(m):
        ax1.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')

    if SW_global.stokearrow_on_off == 1:
        x4 = [[1031, 675, 1031], [1031, 925], [925, 1031], [925, 925],[255], [468, 255], [363, 241],[255, 363],
              [241, 255], [1256, 1273], [1039, 1256],[1256], [1141, 1256], [1273, 1141],[940, 1021, 1021, 940, 940, 1021],
              [543, 543],[492, 572, 572, 492], [572, 572, 492]]
        y4 = [[651, 650, 651], [651, 723], [576, 651], [723, 576], [825], [1237, 825], [872, 945], [825, 872],
              [945, 825], [823, 953], [1216, 823], [823], [879, 823], [953, 879],[1462, 1462, 1382, 1382, 1302, 1302],
              [1461, 1301], [733, 733, 653, 653], [653, 572, 572]]

        x3 = [[kern_fix + 884], [kern_fix + 885, kern_fix + 884],
              [kern_fix + 962, kern_fix + 815], [kern_fix + 884, kern_fix + 962], [kern_fix + 815, kern_fix + 884],
              [kern_fix + 129, kern_fix + 179, kern_fix + 381, kern_fix + 469, kern_fix + 604, kern_fix + 619],
              [kern_fix + 96, kern_fix + 129, kern_fix + 228],
              [kern_fix + 228, kern_fix + 96],
              [kern_fix + 838, kern_fix + 919, kern_fix + 919, kern_fix + 838, kern_fix + 838, kern_fix + 919],
              [kern_fix + 521, kern_fix + 521]]
        y3 = [[124], [485, 124], [213, 213], [124, 213], [213, 124], [404, 641, 641, 641, 528, 445], [513, 404, 460],
              [460, 513], [735, 735, 655, 655, 575, 575], [454, 294]]

        k = len(x3)
        l = len(x4)
        for e in range(l):
            ax1.plot(x4[e], y4[e], color=SW_global.stokearrow_color_var, linewidth=1)
        for f in range(k):
            ax1.plot(x3[f], y3[f], color=SW_global.stokearrow_color_var, linewidth=1)

    if SW_global.startdot_on_off == 1:
        ax1.plot(752, 1501, marker='.', color=SW_global.startdot_color)
        ax1.plot(kern_fix + 754, 375, marker='.', color=SW_global.startdot_color)

    if SW_global.decisiondot_on_off == 1:
        for i in range(n):
            ax1.scatter(x1[i], y1[i], color=SW_global.decisiondot_color, marker='.')
    if SW_global.connectdot_on_off == 1:
        for i in range(n):
            ax1.plot(x1[i], y1[i], color=SW_global.connectingdot_color_var, linewidth=0.5)
        for j in range(m):
            ax1.plot(x2[j], y2[j], color=SW_global.connectingdot_color_var, linewidth=0.5)

    ax1.plot(base_x, base_y, color=SW_global.guidelines_base_color, linewidth=0.5)
    ax1.plot(median_x, median_y, color=SW_global.guidelines_middle_color, linestyle=':', linewidth=0.5)
    ax1.plot(descender_x, descender_y, color=SW_global.guidelines_bottom_color, linewidth=0.5)
    ax1.plot(ascender_x, ascender_y, color=SW_global.guidelines_top_color, linewidth=0.5)

    if SW_global.guidelines_toparea == 1:
        axhspan_top = ax1.axhspan(790, 1460, facecolor=SW_global.guidelines_background_color_toparea, alpha=0.4)
    if SW_global.guidelines_middlearea == 1:
        axhspan_middle = ax1.axhspan(25, 730, facecolor=SW_global.guidelines_background_color_middlearea, alpha=0.4)
    if SW_global.guidelines_descenderarea == 1:
        axhspan_descender = ax1.axhspan(-730, -20, facecolor=SW_global.guidelines_background_color_descenderarea, alpha=0.4)



    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=FigexFrame)
    canvas.get_tk_widget().grid(row=0, column=1)

    backgroundEndFrame = Frame(background_wtp)
    backgroundEndFrame.pack()

    backgroundEndchkFrame = Frame(backgroundEndFrame)
    backgroundEndchkFrame.grid(row=0, column=0)

    backgroundEndokcnlFrame = Frame(backgroundEndFrame)
    backgroundEndokcnlFrame.grid(row=0, column=1)

    background_chkbx = Checkbutton(backgroundEndchkFrame, text="Set as Default", variable=var, font=('manuscript', 9))
    background_chkbx.pack(side=LEFT, padx=10, pady=20)

    def background_close():
        background_wtp.destroy()
        for k in range(1):
            for l in range(1):
                default_guideline(guideline_axes[l])

    background_button_cancel = ttk.Button(backgroundEndokcnlFrame, text="Cancel", command=background_wtp.destroy)
    background_button_cancel.pack(side=RIGHT, padx=10, pady=2, anchor=N)
    background_button_ok = ttk.Button(backgroundEndokcnlFrame,
                                      text="OK",
                                      command=background_close)
    background_button_ok.pack(side=RIGHT, pady=2, anchor=N)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# ******************************************* WorkSheet Zoom option window **********************************
z1 = tk.StringVar()
z1.set("50%")

def zoom_choices():
    global f_w, f_h, zoom_value

    print("Zoom size")
    if zoom_value == 0:
        SW_global.change_size_count = SW_global.change_size_count - 50
        zoomLabel.config(text=str(SW_global.change_size_count)+"%")
        f_w, f_h = 3, 4
        fig.set_size_inches(f_w, f_h)
        fig.canvas.draw()

def zoom_wp():
    global zoom_value
    zoom_wp = Toplevel(SW_Main_UI)
    zoom_wp.wm_title("Zoom")
    zoom_wp.geometry("300x120+250+200")
    zoom_wp.resizable(width=False, height=False)
    zoom_wp.wm_transient(SW_Main_UI)

    zm_frame0 = Frame(zoom_wp,width = 150,height = 100)
    zm_frame0.grid(row = 0, column = 0, ipady = 15)
    zm_frame1 = Frame(zm_frame0,width = 150,height = 100)
    zm_frame1.grid(row = 0, column = 0)

    zm_frame1_1 = Frame(zm_frame1,width = 50,height = 100)
    zm_frame1_1.grid(row = 0, column = 0)

    zm_frame1_2 = Frame(zm_frame1,width = 50,height = 100)
    zm_frame1_2.grid(row = 0, column = 1)

    zm_frame2 = Frame(zm_frame0,width = 150,height = 100)
    zm_frame2.grid(row = 0, column = 1)
    zm_frame3 = Frame(zoom_wp, width = 300,height = 110)
    zm_frame3.grid(row = 1, column = 0)

    zoom_option_ml1 = ["50%", "75%", "100%"]
    for val5, zoom_option_ml1 in enumerate(zoom_option_ml1):
        zoom_option_rb_ml1 = tk.Radiobutton(zm_frame1_1, text=zoom_option_ml1, variable=str(z1), value=zoom_option_ml1,
                                            font=('manuscript', 9))
        zoom_option_rb_ml1.pack(ipadx=8)

    zoom_option_ml2 = ["125%", "150%", "other:"]
    for val5, zoom_option_ml2 in enumerate(zoom_option_ml2):
        zoom_option_rb_ml2 = tk.Radiobutton(zm_frame1_2, text=zoom_option_ml2, variable=str(z1), value=zoom_option_ml2,
                                            font=('manuscript', 9))
        zoom_option_rb_ml2.pack(ipadx = 8)

    zoom_value = z1.get()

    zoom_chkbx = Checkbutton(zm_frame2, text="Set as Default", variable=var, font=('manuscript', 9))
    zoom_chkbx.pack(ipadx = 8)

    zoom_lbl = Label(zm_frame2)
    zoom_lbl.pack(ipadx = 8)

    zoom_entry = Entry(zm_frame2, width=6, text = "100", state =DISABLED)
    zoom_entry.pack(ipadx = 8)

    def zoom_close():
        zoom_choices()
        zoom_wp.destroy()

    zoom_button_cancel = ttk.Button(zm_frame3, text="Cancel", command=zoom_wp.destroy)
    zoom_button_cancel.pack(side='left', padx=8)
    zoom_button_ok = ttk.Button(zm_frame3, text="OK", command = zoom_close)
    zoom_button_ok.pack(side='left', padx=8)

#*************************************** WorkSheet Zoom option window end**************************
#********************************************* Font option window**********************************

def font_wp():
    global guideline_counter
    global value1, base_x, base_y, median_y, descender_y, ascender_y, median_x, descender_x, ascender_x

    value = ''
    value1 = ''
    font_wp = Toplevel(SW_Main_UI)
    font_wp.geometry("400x480+250+100")
    font_wp.title("Fonts")
    font_wp.resizable(height=FALSE, width=FALSE)
    frame1 = Frame(font_wp, width=400, height=255)
    frame1.pack(padx=5, ipady=20)

    frame1child1 = tk.Frame(frame1, height=255, width=200)
    frame1child1.grid(row=0, column=0, padx=6, ipadx=3)

    lab1 = tk.Label(frame1child1, text="Select Font", width=10)
    lab1.grid(row=0, column=0, sticky=W)

    ftext = tk.Entry(frame1child1, width=18)
    ftext.grid(row=1, column=0, sticky=W)
    ftext.config(text = value)
    ftext.insert(INSERT, "Manuscript")

    def onselect1(event):
        global value
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        print("selection:", value)
        ftext.delete(0, END)
        ftext.insert(tk.END, value)

    val = ["Manuscript", "Arial", "Times New Roman", "Monotype Corsiva", "Forte", "Elephanta", "Handwriting",
           "Manuscript", "Arial", "Times New Roman", "Monotype Corsiva", "Forte", "Elephanta", "Handwriting",
           "Manuscript", "Arial", "Times New Roman", "Monotype Corsiva", "Forte", "Elephanta", "Handwriting",
           "Manuscript", "Arial", "Times New Roman", "Monotype Corsiva", "Forte", "Elephanta", "Handwriting"]
    cbox = tk.Listbox(frame1child1, height=9, width=18, selectmode=SINGLE)
    cbox.insert(END, *val)
    cbox.select_set(0)
    cbox.get(ACTIVE)
    cbox.grid(row=2, column=0, sticky=W)
    cbox.bind('<<ListboxSelect>>', onselect1)

    S1 = Scrollbar(frame1child1)
    S1.grid(row=2, column=1, ipady=54)
    S1.config(command=cbox.yview)
    cbox.config(yscrollcommand=S1.set)

    frame1child2 = tk.Frame(frame1, height=255, width=50)
    frame1child2.grid(row=0, column=1, padx=3, ipadx=6)

    lab2 = tk.Label(frame1child2, text="Size")
    lab2.grid(row=0, column=0, sticky=W)


    stext = tk.Entry(frame1child2, width=4)
    stext.grid(row=1, column=0)
    stext.config(text = value1)
    stext.insert(INSERT, 48)


    def onselect2(event):
        global value1, base_x, base_y, median_y, descender_y, ascender_y, median_x, descender_x, ascender_x
        widget = event.widget
        selection = widget.curselection()
        value1 = widget.get(selection[0])
        fig.text(0.98, 0.009, EtsPyTech.dev_details(),
        fontsize=7, color='black',ha='right', va='bottom', alpha=0.090)
        fig.canvas.draw()

        if selection[0] == 0:
            ax1.clear()
            l,b,w,h = 0.01, 0.6, 0.99, 0.04
            ax1.set_position([l,b,w,h])
            SW_global.scl = 32
            SW_global.btm_gd_1 = 0.93
            SW_global.ht_gd_1 = 0.04
            bottom = 0.93
            top = 0.97
            mainselector.maxdist = 8
            SW_global.gd_sc1 = True
            sizechange_guideline(ax1)
            fig.canvas.draw()
        elif selection[0] == 1:
            ax1.clear()
            ax1.set_position([0.01, 0.6, 0.99, 0.05])
            SW_global.scl = 31
            SW_global.btm_gd_1 = 0.93
            SW_global.ht_gd_1 = 0.05
            bottom = 0.93
            top = 0.98
            mainselector.maxdist = 10
            SW_global.gd_sc1 = True
            sizechange_guideline(ax1)
            fig.canvas.draw()
        else:
            print("selection:", value1)
        stext.delete(0, END)
        stext.insert(tk.END, value1)


    val2 = ['8','10','12','14','16','18','20','22','24','30','36','42','48','54','60','66','72','96','128','144','160','192']
    size_cbox = tk.Listbox(frame1child2, height=9, width=4, selectmode=SINGLE)
    size_cbox.insert(END, *val2)

    size_cbox.select_set(12)
    size_cbox.get(ACTIVE)

    size_cbox.grid(row=2, column=0)
    S = Scrollbar(frame1child2)
    S.grid(row=2, column=1, ipady=54)
    size_cbox.bind('<<ListboxSelect>>', onselect2)
    S.config(command=size_cbox.yview)
    size_cbox.config(yscrollcommand=S.set)

    frame1child3 = tk.Frame(frame1, height=255, width=100)
    frame1child3.grid(row=0, column=2, padx=3, ipadx=6)

    frm3 = tk.Label(frame1child3, width=5)
    frm3.grid(row=0, column=0)

    def font_wp_close():
        if SW_global.gdaxes == key_c:
            guideline_axes[l].cla()
            default_guideline(guideline_axes[l])
        mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
        fig.canvas.draw()
        font_wp.destroy()

    save_button = ttk.Button(frame1child3, text="OK", command = font_wp_close)
    save_button.grid(row=1, column=0, ipadx=7, padx=10, pady=5)

    cancel_button = ttk.Button(frame1child3, text="Cancel", command=font_wp.destroy)
    cancel_button.grid(row=2, column=0, ipadx=7, padx=10, pady=5)

    frm3 = tk.Label(frame1child3, width=5, height=4)
    frm3.grid(row=3, column=0)

    stawcl_chkbx = Checkbutton(frame1child3, text="Set as Default", font=('manuscript', 9))
    stawcl_chkbx.grid(row=4, column=0)

    frame2 = Frame(font_wp, width=400, height=220, bd=2, highlightbackground="black", highlightcolor="black",
                   highlightthickness=1)
    frame2.pack(padx=4, pady=2)

    fig = plt.figure()
    ax1 = fig.add_axes([0.01, 0.46, 0.98, 0.25])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    fig.set_size_inches(3.5, 2.2)

    SW_global.scl = 9

    SW_global.gd_sc1 = False
    ####### Border ART ##########
    def sizechange_guideline(dynamic_axes):
        global base_x, median_x, descender_x, ascender_x, base_y, median_y, descender_y, ascender_y
    # Guideline Axes
        if SW_global.gd_sc1:
            img = plt.imread('icons/apple.jpg')
            dynamic_axes.imshow(img, extent = [0.999,1,0.999,1])
            for ln in ['top','right','left','bottom']:
                dynamic_axes.spines[ln].set_linewidth(0)
            base_x = [0, (1500 * SW_global.scl)]
            base_y = [0, 0]
            median_x = [0, (1500 * SW_global.scl)]
            median_y = [757, 757]
            descender_x = [0, (1500 * SW_global.scl)]
            descender_y = [-747, -747]
            ascender_x = [0, (1500 * SW_global.scl)]
            ascender_y = [1510, 1510]

            dynamic_axes.plot(base_x, base_y, color='red', linewidth=0.5)
            dynamic_axes.plot(median_x, median_y, color='blue', dashes=(8, 6), linewidth=0.5)
            dynamic_axes.plot(descender_x, descender_y, color='black', linewidth=0.5)
            dynamic_axes.plot(ascender_x, ascender_y, color='blue', linewidth=0.5)

            n = len(x1)
            m = len(x2)
            for i in range(n):
                dynamic_axes.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
            for j in range(m):
                dynamic_axes.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')
        else:
            img = plt.imread('icons/apple.jpg')
            dynamic_axes.imshow(img, extent = [0.999,1,0.999,1])
            for ln in ['top','right','left','bottom']:
                dynamic_axes.spines[ln].set_linewidth(0)
            dynamic_axes.plot(base_x, base_y, color='red', linewidth=0.5)
            dynamic_axes.plot(median_x, median_y, color='blue', dashes=(8, 6), linewidth=0.5)
            dynamic_axes.plot(descender_x, descender_y, color='black', linewidth=0.5)
            dynamic_axes.plot(ascender_x, ascender_y, color='blue', linewidth=0.5)

            n = len(x1)
            m = len(x2)
            for i in range(n):
                dynamic_axes.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
            for j in range(m):
                dynamic_axes.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')

    base_x = [0, (1500 * SW_global.scl)]
    base_y = [0, 0]
    median_x = [0, (1500 * SW_global.scl)]
    median_y = [757, 757]
    descender_x = [0, (1500 * SW_global.scl)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * SW_global.scl)]
    ascender_y = [1500, 1500]

    x1 = [[0, 752, 1500], [248, 1251]]
    y1 = [[0, 1501, 0], [496, 495]]
    kern_fix = 1800
    x2 = [[kern_fix + 754, kern_fix + 754],
          [kern_fix + 754, kern_fix + 754],
          [kern_fix + 377], [kern_fix + 0, kern_fix + 0, kern_fix + 222, kern_fix + 377],
          [kern_fix + 377, kern_fix + 221, kern_fix + 0, kern_fix + 0],
          [kern_fix + 755, kern_fix + 755, kern_fix + 640, kern_fix + 528, kern_fix + 377],
          [kern_fix + 377, kern_fix + 528, kern_fix + 755, kern_fix + 755]]

    y2 = [[375, 749],
          [0, 375],
          [749],
          [375, 530, 749, 749],
          [0, 0, 219, 375],
          [376, 530, 641, 749, 749],
          [0, 0, 221, 376]]

    sizechange_guideline(ax1)

    fig.set_size_inches(3.5, 2.2)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.get_tk_widget().grid(row=0, column=0)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GuideLine On/Off <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def Guideline_off():
    if SW_global.gdaxes == key_c and SW_global.gv == True:
        for xi in range(0,4):
            guideline_axes[l].lines[xi].set_visible(False)
        fig.canvas.draw()
        SW_global.gv = False

def Guideline_on():
    print("Working")
    if SW_global.gdaxes == key_c and SW_global.gv == False:
        for xi in range(0,4):
            guideline_axes[l].lines[xi].set_visible(True)
        fig.canvas.draw()
        SW_global.gv = True

def main2():
    if SW_global.count == 0:
        SW_global.count = 1
        Guideline_off()
        guidelines_button.configure(background='#d9d9d9')

    else:
        SW_global.count = 0
        Guideline_on()
        guidelines_button.configure(background='skyblue')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Border_Art_Propaty_Window <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
b1 = tk.IntVar()
b2 = tk.IntVar()
b3 = tk.IntVar()
fcp = tk.StringVar()
b1.set(0)
b1.initialize(0)

def borderart_wp():
    global filename, imagebox, arr_img
    global b1

    borderart_wp = Toplevel(SW_Main_UI)
    borderart_wp.geometry("480x480+250+100")
    borderart_wp.title("Border Art")
    borderart_wp.resizable(height=FALSE, width=FALSE)
    frame1 = Frame(borderart_wp, width=400, height=255)
    frame1.pack(padx=5, ipady=10)
    # ---------------------------------------------------------------------------
    frame1child1 = tk.Frame(frame1, height=255, width=200)
    frame1child1.grid(row=0, column=0, padx=6)

    value1 = '30'

    def sizechange_guideline(dynamic_axes):
        global base_x, median_x, descender_x, ascender_x, base_y, median_y, descender_y, ascender_y
        global filename, imagebox, arr_img, zz, xt
        # Guideline Axes
        # if SW_global.ba_flag == True or SW_global.ba_size == 1:
        #     base_x = [0, (1500 * SW_global.scl)]
        #     base_y = [0, 0]
        #     median_x = [0, (1500 * SW_global.scl)]
        #     median_y = [757, 757]
        #     descender_x = [0, (1500 * SW_global.scl)]
        #     descender_y = [-747, -747]
        #     ascender_x = [0, (1500 * SW_global.scl)]
        #     ascender_y = [1510, 1510]

        #     dynamic_axes.plot(base_x, base_y, color='red', linewidth=0.5)
        #     dynamic_axes.plot(median_x, median_y, color='blue', dashes=(8, 6), linewidth=0.5)
        #     dynamic_axes.plot(descender_x, descender_y, color='black', linewidth=0.5)
        #     dynamic_axes.plot(ascender_x, ascender_y, color='blue', linewidth=0.5)

        #     n = len(x1)
        #     m = len(x2)
        #     for i in range(n):
        #         dynamic_axes.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
        #     for j in range(m):
        #         dynamic_axes.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')
        #     brd.DrawBorderArt(dynamic_axes,fig,filename)
        #     # arr_img = plt.imread(filename)
        #     # imagebox = OffsetImage(arr_img, zoom=zz)

        #     # imagebox.image.axes = dynamic_axes

        #     # for xi in range(25, xt, 25):
        #     #     ab = AnnotationBbox(imagebox, (xi, 1),
        #     #                         xycoords=("data", "axes fraction"),
        #     #                         boxcoords="offset points",
        #     #                         box_alignment=(1, 0),
        #     #                         bboxprops={"edgecolor": "none"})

        #     #     dynamic_axes.add_artist(ab)

        #     # ###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        #     # for yi in range(25, xt, 25):
        #     #     ab = AnnotationBbox(imagebox, (yi, 0),
        #     #                         xycoords=("data", "axes fraction"),
        #     #                         boxcoords="offset points",
        #     #                         box_alignment=(1, 1),
        #     #                         bboxprops={"edgecolor": "none"})

        #     #     dynamic_axes.add_artist(ab)

        #     # ###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        #     # # Rightside_BorderArt
        #     # ##for xx in np.arange(0,1,0.4):

        #     # ab = AnnotationBbox(imagebox, (0, 0),
        #     #                     xycoords=("data", "axes fraction"),
        #     #                     boxcoords="offset points",
        #     #                     box_alignment=(1, 1),
        #     #                     bboxprops={"edgecolor": "none"})

        #     # dynamic_axes.add_artist(ab)

        #     # ab = AnnotationBbox(imagebox, (0, 0.3),
        #     #                     xycoords=("data", "axes fraction"),
        #     #                     boxcoords="offset points",
        #     #                     box_alignment=(1, .5),
        #     #                     bboxprops={"edgecolor": "none"})

        #     # dynamic_axes.add_artist(ab)

        #     # ab = AnnotationBbox(imagebox, (0, 0.8),
        #     #                     xycoords=("data", "axes fraction"),
        #     #                     boxcoords="offset points",
        #     #                     box_alignment=(1, .5),
        #     #                     bboxprops={"edgecolor": "none"})

        #     # dynamic_axes.add_artist(ab)

        #     # ab = AnnotationBbox(imagebox, (0, 1),
        #     #                     xycoords=("data", "axes fraction"),
        #     #                     boxcoords="offset points",
        #     #                     box_alignment=(1, 0),
        #     #                     bboxprops={"edgecolor": "none"})

        #     # dynamic_axes.add_artist(ab)

        #     # # =======================================================================================
        #     # # Left_BorderArt

        #     # ab = AnnotationBbox(imagebox, (300, 1),
        #     #                     xycoords=("data", "axes fraction"),
        #     #                     boxcoords="offset points",
        #     #                     box_alignment=(.5, 0),
        #     #                     bboxprops={"edgecolor": "none"})

        #     # dynamic_axes.add_artist(ab)

        #     # ab = AnnotationBbox(imagebox, (300, 0.8),
        #     #                     xycoords=("data", "axes fraction"),
        #     #                     boxcoords="offset points",
        #     #                     box_alignment=(1, .5),
        #     #                     bboxprops={"edgecolor": "none"})

        #     # dynamic_axes.add_artist(ab)

        #     # ab = AnnotationBbox(imagebox, (300, 0.5),
        #     #                     xycoords=("data", "axes fraction"),
        #     #                     boxcoords="offset points",
        #     #                     box_alignment=(1, .5),
        #     #                     bboxprops={"edgecolor": "none"})

        #     # dynamic_axes.add_artist(ab)

        #     # ab = AnnotationBbox(imagebox, (300, 0.3),
        #     #                     xycoords=("data", "axes fraction"),
        #     #                     boxcoords="offset points",
        #     #                     box_alignment=(1, 1),
        #     #                     bboxprops={"edgecolor": "none"})

        #     # dynamic_axes.add_artist(ab)
        #     # fig.canvas.draw()

        # else:

        #     dynamic_axes.plot(base_x, base_y, color='red', linewidth=0.5)
        #     dynamic_axes.plot(median_x, median_y, color='blue', dashes=(8, 6), linewidth=0.5)
        #     dynamic_axes.plot(descender_x, descender_y, color='black', linewidth=0.5)
        #     dynamic_axes.plot(ascender_x, ascender_y, color='blue', linewidth=0.5)

        #     n = len(x1)
        #     m = len(x2)
        #     for i in range(n):
        #         dynamic_axes.plot(x1[i], y1[i], color='black', linewidth=1, linestyle=':')
        #     for j in range(m):
        #         dynamic_axes.plot(x2[j], y2[j], color='black', linewidth=1, linestyle=':')

        # #for j in range(len(SW_global.axes_data)):
        #  #   dynamic_axes=SW_global.axes_data[str(j)]["axis_data"]
        
        fig.canvas.draw()
        #brd.DrawBorderArt(mainselector,fig,filename)

        #dynamic_axes=guideline_axes


    def onselect1(event):
        global value1, filename, b1
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        print("ba_val1:", value)
        print ("You selected the option " , b1.get())

        if b1.get() == 2:
            if value == "1 Apple":
                filename = "./Images/Color Pictures/apple.jpg"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Banana":
                filename = "./Images/Color Pictures/banana.jpg"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Chair":
                filename = "./Images/Color Pictures/chair.jpg"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Elephant":
                filename = "./Images/Color Pictures/elephant.jpg"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Fire":
                filename = "./Images/Color Pictures/fire.jpg"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Grapes":
                filename = "./Images/Color Pictures/grapes.jpg"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Hat":
                filename = "./Images/Color Pictures/hat.jpg"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

        if b1.get() == 3:
            if value == "1 Apple":
                filename = "./Images/ImageBW/apple.bmp"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Banana":
                filename = "./Images/ImageBW/banana.bmp"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Chair":
                filename = "./Images/ImageBW/chair.bmp"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Elephant":
                filename = "./Images/ImageBW/elephant.bmp"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Fire":
                filename = "./Images/ImageBW/fire.bmp"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Grapes":
                filename = "./Images/ImageBW/grapes.bmp"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

            elif value == "1 Hat":
                filename = "./Images/ImageBW/hat.bmp"
                SW_global.ba_flag = True
                ax1.clear()
                sizechange_guideline(ax1)

        else:
            print("Nothing")
        fig.canvas.draw()

    ba_val1 = ["1 Apple", "1 Banana", "1 Chair", "1 Elephant", "1 Fire", "1 Grapes", "1 Hat",
               "1 Igloo", "1 Jet", "1 Kangaroo", "1 Loin", "1 Monkey", "1 Net", "1 Octopus",
               "1 Parrot", "1 Queen", "1 Rino", "1 Snake", "1 Telephone", "1 Ubremlla", "1 Violin",
               "1 Whale", "1 X-ray", "1 Yarn", "1 Zebra", "Forte", "Elephanta", "Handwriting"]
    cbox = tk.Listbox(frame1child1, height=9, width=18, selectmode=SINGLE)
    cbox.insert(END, *ba_val1)
    cbox.grid(row=2, column=0, sticky=W)
    cbox.bind('<<ListboxSelect>>', onselect1)
    S1 = Scrollbar(frame1child1)
    S1.grid(row=2, column=1, ipady=54)
    S1.config(command=cbox.yview)
    cbox.config(yscrollcommand=S1.set)

    borderart_option_rb1 = tk.Radiobutton(frame1child1, text="No Border Art", variable=b1, value=1)
    borderart_option_rb1.grid(row=0, column=0, sticky=W)

    borderart_option_rb2 = tk.Radiobutton(frame1child1, text="Color", variable=b1, value=2)
    borderart_option_rb2.grid(row=0, column=1, sticky=W)

    lab1 = tk.Label(frame1child1, text="Select BorderArt", width=20)
    lab1.grid(row=1, column=0, sticky=W)

    frame1child2 = tk.Frame(frame1, height=255, width=50)
    frame1child2.grid(row=0, column=1, padx=3)

    value1 = ''

    borderart_option_rb2 = tk.Radiobutton(frame1child2, text="Black & White", variable=b1,  value=3)  # , value=ba_val2
    borderart_option_rb2.grid(row=0, column=0, sticky=W)

    lab2 = tk.Label(frame1child2, text="Size")
    lab2.grid(row=1, column=0, sticky=W)

    def onselect2(event):
        global guideline_counter, zz, xt, value1
        global value1, base_x, base_y, median_y, descender_y, ascender_y, median_x, descender_x, ascender_x
        widget = event.widget
        selection = widget.curselection()
        try:
            value1 = widget.get(selection[0])
        except Exception as e:
            print(e)
            pass
        fig.text(0.98, 0.009, EtsPyTech.dev_details(),
                 fontsize=7, color='black', ha='right', va='bottom', alpha=0.090)
        fig.canvas.draw()
        #print("ba_val2:", value1)
        if value1 == '30':
            SW_global.ba_size = 1
            zz = 0.08
            xt = 300
        elif value1 == '35':
            SW_global.ba_size = 1
            zz = 0.1
            xt = 225

    ba_val2 = ['30', '35', '40', '45', '50', '55', '60', '65', '70']
    size_cbox = tk.Listbox(frame1child2, height=9, width=4, selectmode=SINGLE)
    size_cbox.insert(END, *ba_val2)

    size_cbox.select_set(0)
    size_cbox.get(ACTIVE)
    size_cbox.grid(row=2, column=0)

    size_cbox.bind('<<ListboxSelect>>', onselect2)

    frame1child3 = tk.Frame(frame1, height=255, width=100)
    frame1child3.grid(row=0, column=2, padx=3, ipadx=6)

    frm3 = tk.Label(frame1child3, width=5)
    frm3.grid(row=0, column=0)

    stawcl_chkbx = Checkbutton(frame1child3, text="Set as Default", font=('manuscript', 9))
    stawcl_chkbx.grid(row=4, column=0)

    def borderart_wp_close():
        if SW_global.ba_flag == True and SW_global.gdaxes == key_c:
            default_guideline(guideline_axes[l])
        borderart_wp.destroy()

    save_button = ttk.Button(frame1child3, text="OK", command=borderart_wp_close)
    save_button.grid(row=1, column=0, ipadx=7, padx=10, pady=5)

    cancel_button = ttk.Button(frame1child3, text="Cancel", command=borderart_wp.destroy)
    cancel_button.grid(row=2, column=0, ipadx=7, padx=10, pady=5)

    frm3 = tk.Label(frame1child3, width=5, height=4)
    frm3.grid(row=3, column=0)

    stawcl_chkbx = Checkbutton(frame1child3, text="Set as Default", font=('manuscript', 9))
    stawcl_chkbx.grid(row=4, column=0)

    frame2 = Frame(borderart_wp, width=400, height=220, bd=2, highlightbackground="black", highlightcolor="black",
                   highlightthickness=1)
    frame2.pack(padx=4, pady=2)

    fig = plt.figure()
    ax1 = fig.add_axes([0.05, 0.30, 0.98, 0.50])
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off',
                    labelleft='off')
    fig.set_size_inches(3.5, 2.2)

    SW_global.scl = 9

    SW_global.ba_flag = False

    SW_global.ba_size = 0

    zz = 0.08
    xt = 300

    base_x = [0, (1500 * SW_global.scl)]
    base_y = [0, 0]
    median_x = [0, (1500 * SW_global.scl)]
    median_y = [757, 757]
    descender_x = [0, (1500 * SW_global.scl)]
    descender_y = [-747, -747]
    ascender_x = [0, (1500 * SW_global.scl)]
    ascender_y = [1500, 1500]

    x1 = [[0, 752, 1500], [248, 1251]]
    y1 = [[0, 1501, 0], [496, 495]]
    kern_fix = 1800
    x2 = [[kern_fix + 754, kern_fix + 754],
          [kern_fix + 754, kern_fix + 754],
          [kern_fix + 377], [kern_fix + 0, kern_fix + 0, kern_fix + 222, kern_fix + 377],
          [kern_fix + 377, kern_fix + 221, kern_fix + 0, kern_fix + 0],
          [kern_fix + 755, kern_fix + 755, kern_fix + 640, kern_fix + 528, kern_fix + 377],
          [kern_fix + 377, kern_fix + 528, kern_fix + 755, kern_fix + 755]]

    y2 = [[375, 749],
          [0, 375],
          [749],
          [375, 530, 749, 749],
          [0, 0, 219, 375],
          [376, 530, 641, 749, 749],
          [0, 0, 221, 376]]

    sizechange_guideline(ax1)

    ax1.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.get_tk_widget().grid(row=0, column=0)

    fig.canvas.draw()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
####### function for write data after cut
def cutAddLetter(inputstring):

    try:
        user_input=inputstring
        length12 = len(SW_global.recent_input_list)
        x_max = manuscript.x_max[user_input]
        kern_x = SW_global.kern_list[0]
        skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
        if color_letter_features_on_off:
            if user_input in skip_list:
                c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
            else:
                x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                c1,c2=font_check(x,y)
        else:
            if user_input in skip_list:
                c1, c2 = manuscript.return_manuscript_fonts(user_input)
            else:
                x,y=manuscript.return_manuscript_fonts(user_input)
                c1,c2=font_check(x,y)

        c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)
        kern_x = SW_global.kern_list[0] + x_max + 300
        SW_global.kern_list.insert(0, kern_x)
        kern_counter = len(kern_value_array)
        kern_value_array.insert(kern_counter, kern_x)
        SW_global.recent_input_list.insert(length12, user_input)
        delete_list.insert(length12, user_input)
        init_enrty_pos = len(SW_global.letters_already_written)
        inti_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
        if draw_type_color_letter == 1:
            if letter_dot_density_no_dot_on_off == 1:
                alp = 0
            else:
                alp = temp_alp
            if color_letter_features_on_off:
                guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
            else:
                guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

        else:
            n = len(c1)
            if letter_dot_density_no_dot_on_off == 1:
                alp = 0
            else:
                alp = temp_alp
            if color_letter_features_on_off:
                for i in range(n):
                    if i == 0:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    if i == 1:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    if i == 2:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    if i == 3:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
            else:
                for i in range(n):
                    guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
        #############################   Cursor part code of inserting ###############################
        import numpy as np
        if(len(SW_global.cursor_data)!=0):
            print("It is ok")
            print(delete_list)
            print(SW_global.letters_already_written)
           # print(cursor_data)
            #cursor_pos(cursor_pos)
        else:
            print("It is empty")
        item_cursor=kern_x-300
        cursor_y=list(np.linspace(-900,1500,500))
        #cursor_y_neg=list(np.lenspace)
        cursor_x=list(np.full((500),item_cursor))
        SW_global.cursor_pos.append(item_cursor)
        k=plt.plot(cursor_x, cursor_y, color='red', linewidth=0.6, dashes=(3, 4))
        for i in k:
            SW_global.cursor_data.append(i)
        #SW_global.cursor_data.append(k)
        for cur_count in range(len(SW_global.cursor_data)-1):
            invisible_item=SW_global.cursor_data[cur_count]
            invisible_item.set_visible(False)
        #fig.canvas.draw()
# -----------------------------------------------------------------------------------------------------
        final_enrty_pos = len(SW_global.letters_already_written)
        final_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
    except Exception as e:
        print(e)
        pass


def add_letter_with_mouse_and_from_end2(axesdata=None,delete_list1=None,pos=None,event_key=None,kern_value_array=None):
    try:
        print("This is add letter 2")
        print("current_pos:",SW_global.current_pos)
        print("current_axes:",SW_global.current_axes)
        kern_value_array=list(kern_value_array)
        print("pos:")
        for i in SW_global.cursor_data:
            i.set_visible(False)
        if((axesdata==None) and (SW_global.current_pos==None)):
            print("check point111")
            length12=len(SW_global.recent_input_list)
            print("SW_global.recent_input_list:",SW_global.recent_input_list)
            user_input=event_key
            x_max=manuscript.x_max[user_input]
            kern_x=SW_global.kern_list[0]
            ###################################################################################
            skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
            if user_input in skip_list:
                if(color_letter_features_on_off):
                    c1,c2=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                else:
                    c1,c2=manuscript.return_manuscript_fonts(user_input)
            else:
                if(color_letter_features_on_off):
                    x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    c1,c2=font_check(x,y)
                else:
                    x,y=manuscript.return_manuscript_fonts(user_input)
                    c1,c2=font_check(x,y)
            ####################################################################################
            c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)

            kern_x=SW_global.kern_list[0]+x_max+300
            SW_global.kern_list.insert(0,kern_x)
            kern_counter=len(kern_value_array)
            kern_value_array.insert(kern_counter,kern_x)
            SW_global.recent_input_list.insert(length12,event_key)
            delete_list1.insert(length12,event_key)
            init_enrty_pos=len(SW_global.letters_already_written)
            inti_letter_pos=len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(init_enrty_pos,inti_letter_pos)
            if draw_type_color_letter==1:
                if letter_dot_density_no_dot_on_off==1:
                    alp=0
                else:
                    alp=temp_alp
                if color_letter_features_on_off:
                    guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
            else:
                n=len(c1)
                if letter_dot_density_no_dot_on_off==1:
                    alp=0
                else:
                    alp=temp_alp
                if color_letter_features_on_off:
                    for i in range(n):
                        if i==0:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==1:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==2:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==3:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    for i in range(n):
                        guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

            fig.canvas.draw()

            import numpy as np
            item_cursor=kern_x-300
            cursor_y=list(np.linspace(-900,1500,500))
            cursor_x=list(np.full((500),item_cursor))
            SW_global.cursor_pos.append(item_cursor)
            cursor_x1=list(np.full((500),item_cursor))
            plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            SW_global.single_click_data=plot_data[0]
            k=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))

            for i in k:
                SW_global.cursor_data.append(i)
                i.set_visible(False)

            fig.canvas.draw()

            final_enrty_pos = len(SW_global.letters_already_written)
            final_letter_pos = len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
            #features_checking_function()
            return delete_list1,kern_value_array

        elif(((axesdata==guideline_axes[l]) and (SW_global.current_pos==SW_global.cursor_pos[-1])) or ((axesdata==guideline_axes[l]) and (len(delete_list)==0))):
            print("check point222")
            length12=len(SW_global.recent_input_list)
            print("SW_global.recent_input_list:",SW_global.recent_input_list)
            user_input=event_key
            x_max=manuscript.x_max[user_input]
            kern_x=SW_global.kern_list[0]
            ###################################################################################
            skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
            if user_input in skip_list:
                if(color_letter_features_on_off):
                    c1,c2=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                else:
                    c1,c2=manuscript.return_manuscript_fonts(user_input)
            else:
                if(color_letter_features_on_off):
                    x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    c1,c2=font_check(x,y)
                else:
                    x,y=manuscript.return_manuscript_fonts(user_input)
                    c1,c2=font_check(x,y)
            ####################################################################################


            c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)

            kern_x=SW_global.kern_list[0]+x_max+300
            SW_global.kern_list.insert(0,kern_x)
            kern_counter=len(kern_value_array)
            kern_value_array.insert(kern_counter,kern_x)
            SW_global.recent_input_list.insert(length12,event_key)
            delete_list1.insert(length12,event_key)
            init_enrty_pos=len(SW_global.letters_already_written)
            inti_letter_pos=len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(init_enrty_pos,inti_letter_pos)
            if draw_type_color_letter==1:
                if letter_dot_density_no_dot_on_off==1:
                    alp=0
                else:
                    alp=temp_alp
                if color_letter_features_on_off:
                    guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
            else:
                n=len(c1)
                if letter_dot_density_no_dot_on_off==1:
                    alp=0
                else:
                    alp=temp_alp
                if color_letter_features_on_off:
                    for i in range(n):
                        if i==0:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==1:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==2:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==3:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    for i in range(n):
                        guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

            import numpy as np
            item_cursor=kern_x-300
            cursor_y=list(np.linspace(-900,1500,500))
            cursor_x=list(np.full((500),item_cursor))
            SW_global.cursor_pos.append(item_cursor)
            cursor_x1=list(np.full((500),item_cursor))
            plot_data=guideline_axes[l].plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            SW_global.single_click_data=plot_data[0]
            fig.canvas.draw()
            k=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            SW_global.current_axes=guideline_axes[l]
            SW_global.current_pos=item_cursor


            for i in k:
                SW_global.cursor_data.append(i)
                i.set_visible(False)

            fig.canvas.draw()

            final_enrty_pos = len(SW_global.letters_already_written)
            final_letter_pos = len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
            #features_checking_function()
            fig.canvas.draw()
            return delete_list1,kern_value_array
        elif(axesdata==guideline_axes[l]):
            print("check point 33333")
            for i in range(len(SW_global.cursor_pos)):
                if(SW_global.cursor_pos[i]<SW_global.current_pos):
                    SW_global.current_pos_in_number=i
            print("SW_global.current_pos_in_number",SW_global.current_pos_in_number)
            SW_global.entire_delete_list_for_one_page.clear()
            temp_current_pos_in_number=SW_global.current_pos_in_number
            for i in range(len(delete_list1)):
                if(i==temp_current_pos_in_number):
                    SW_global.entire_delete_list_for_one_page.append(event_key)
                    SW_global.entire_delete_list_for_one_page.append(delete_list1[i])
                    SW_global.current_pos_in_number=SW_global.current_pos_in_number+1
                else:
                    SW_global.entire_delete_list_for_one_page.append(delete_list1[i])

            for i in range(len(guideline_axes[l].lines)):
                if(i>3):
                    ((guideline_axes[l].lines)[i]).set_visible(False)
            print("Entire delete list for one page",SW_global.entire_delete_list_for_one_page)
            fig.canvas.draw()
            set_key=10000
            SW_global.cursor_pos.clear()
            SW_global.cursor_data.clear()
            SW_global.cursor_pos.insert(0,0)
            kern_value_array.clear()
            SW_global.kern_list.clear()
            SW_global.letters_already_written.clear()
            SW_global.letters_already_written.clear()
            SW_global.kern_list.insert(0,0)
            SW_global.kern_value_array.clear()
            SW_global.kern_value_array.insert(0,0)
            kern_value_array.clear()
            kern_value_array.insert(0,0)
            SW_global.recent_input_list.clear()
            compositedot_already_applied_array.clear()
            startdot_already_applied_array.clear()
            decisiondot_already_applied_array.clear()
            connectdot_already_applied_array.clear()
            stoke_arrow_flag_pos=0
            startdot_flag_pos=0
            decision_dot_flag_pos=0
            connect_dot_flag_pos=0
            print("Delete list:",SW_global.entire_delete_list_for_one_page)
            print("SW_global.guideline_axes[l]",guideline_axes[l])
            print("SW_global.kern",SW_global.kern_list)
            print("SW_global.recent_input_list:",SW_global.recent_input_list)
            delete_list1,kern_value_array1=cut_add_letter_from_any_position2(delete_list1=SW_global.entire_delete_list_for_one_page,current_axes=axesdata,key=set_key)
            #return delete_list1,kern_value_array1
            return delete_list1,kern_value_array1
        ### part for if cursor not in guide line xes ####
        elif(axesdata!=guideline_axes[l]):
            print("check point 444444444")
        #    print("I am in axes data != Guide lineaxes part")
            set_key=None
            for i in range(len(SW_global.axes_data)):
                print("This is set key part ")
                if(SW_global.axes_data[str(i)]["axis_data"]==SW_global.current_axes):
                    set_key=i
                    print("set_key:",set_key)
                    break
            if(set_key!=None):
                print("This is check point 33")
                for i in range(len(SW_global.axes_data[str(set_key)]["cursor_pos"])):
                    if((SW_global.axes_data[str(set_key)]["cursor_pos"])[i]<SW_global.current_pos):
                        SW_global.current_pos_in_number=i
                ##### Clear the list #####
                SW_global.entire_delete_list_for_one_page.clear()
                for k in range(len(SW_global.axes_data)):
                    if(k==set_key):
                        for i in range(len(SW_global.axes_data[str(set_key)]["delete_list"])):
                            if(i==SW_global.current_pos_in_number):
                                SW_global.entire_delete_list_for_one_page.append(event_key)
                                SW_global.entire_delete_list_for_one_page.append(SW_global.axes_data[str(set_key)]["delete_list"][i])
                            else:
                                SW_global.entire_delete_list_for_one_page.append(SW_global.axes_data[str(set_key)]["delete_list"][i])
                    elif(k>set_key):
                        for i in SW_global.axes_data[str(k)]["delete_list"]:
                            SW_global.entire_delete_list_for_one_page.append(i)
                for i in delete_list1:
                    SW_global.entire_delete_list_for_one_page.append(i)
                print("This is SW_global.entire_delete_list_for_one_page:",SW_global.entire_delete_list_for_one_page)

                for i in range(len(SW_global.axes_data)):
                    if(i>=set_key):
                        for k5 in range(len(guideline_axes[l].lines)):
                            if(k5>3):
                                ((guideline_axes[l].lines)[k5]).set_visible(False)
                        for j1 in range(len(SW_global.axes_data[str(i)]["lines"])):
                            if(j1>3):
                                ((SW_global.axes_data[str(i)]["lines"])[j1]).set_visible(False)
                        (SW_global.axes_data[str(i)]["letters_already_written"]).clear()
                        (SW_global.axes_data[str(i)]["cursor_pos"]).clear()
                        (SW_global.axes_data[str(i)]["cursor_data"]).clear()
                        (SW_global.axes_data[str(i)]["kern_value_array"]).clear()
                        (SW_global.axes_data[str(i)]["delete_list"]).clear()
                        (SW_global.axes_data[str(i)]["compositedot_already_applied_array"]).clear()
                        (SW_global.axes_data[str(i)]["startdot_already_applied_array"]).clear()
                        (SW_global.axes_data[str(i)]["decisiondot_already_applied_array"]).clear()
                        (SW_global.axes_data[str(i)]["connectdot_already_applied_array"]).clear()
                        SW_global.axes_data[str(i)]["stoke_arrow_flag_pos"]=0
                        SW_global.axes_data[str(i)]["startdot_flag_pos"]=0
                        SW_global.axes_data[str(i)]["decision_dot_flag_pos"]=0
                        SW_global.axes_data[str(i)]["connect_dot_flag_pos"]=0
                      #  while len(SW_global.axes_data[str(i)]["gval"])>3:
                      #      del (SW_global.axes_data[str(i)]["gval"])[len(SW_global.axes_data[str(i)]["gval"])-1]
                      #  while len(SW_global.axes_data[str(i)]["lines"])>3:
                      #      del (SW_global.axes_data[str(i)]["lines"])[len(SW_global.axes_data[str(i)]["gval"])-1]
                       # SW_global.axes_data[str(i)]["lines"].clear()
                       # SW_global.axes_data[str(i)]["gval"].clear()
                        SW_global.axes_data[str(i)]["recent_input_list"].clear()

                SW_global.cursor_pos.clear()
                SW_global.cursor_data.clear()
                kern_value_array.clear()
                compositedot_already_applied_array.clear()
                startdot_already_applied_array.clear()
                decisiondot_already_applied_array.clear()
                connectdot_already_applied_array.clear()
                decision_dot_flag_pos=0
                startdot_flag_pos=0
                connect_dot_flag_pos=0
                stoke_arrow_flag_pos=0
                ##### clearing all the axes which is included in rectangle weigets  #####
                delete_list2,kern_value_array1=cut_add_letter_from_any_position2(delete_list1=SW_global.entire_delete_list_for_one_page,current_axes=SW_global.current_axes,key=set_key)
                print("This is before final sending :",delete_list2)
                print("This is before final sending :",kern_value_array1)
                return delete_list2,kern_value_array1
    except Exception as e:
        print(e)
        pass
    return


def cut_add_letter_from_any_position2(delete_list1=None,current_axes=None,key=None):
    print("I am in second part:",delete_list1)
    temp_count=key
    delete_list=[]
    kern_value_array.clear()
    kern_value_array.insert(0,0)
    print("This is delete_list:",delete_list1)
    print("This is chekc point1")
    try:
        if(key==10000):
            print("check point 555555555")
            previous_axes=guideline_axes[l]
            next_axes=guideline_axes[l]
            for j in range(len(delete_list1)):
                print("kern_value array",kern_value_array)
                print("SW_global.letters_already_written",SW_global.letters_already_written)
                print("delete_list1:",delete_list1[j])
                user_input=delete_list1[j]
                event_key=delete_list1[j]
                if(SW_global.kern_list[0]>15500):
                    print("This is check point 2")
                    a=dict()
                    a["letters_already_written"]=[i for i in  SW_global.letters_already_written]
                    a["kern_value_array"]=[i for i in kern_value_array]
                    a["delete_list"]=[i for i in delete_list]
                    a["kern_list"]=[i for i in SW_global.kern_list]
                    a["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
                    a["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
                    a["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
                    a["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
                    a["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
                    a["startdot_flag_pos"]=startdot_flag_pos
                    a["decision_dot_flag_pos"]=decision_dot_flag_pos
                    a["connect_dot_flag_pos"]=connect_dot_flag_pos
                    a["axis_data"]=guideline_axes[l]
                    #print("This is guide line axes .lines",len(guideline_axes[l].lines))
                    a["lines"]=[i for i in guideline_axes[l].lines]
                    #print("This is check point 3")
                    a["gval"]=[i for i in SW_global.g_val.lines]
                    a["cursor_pos"]=[i for i in SW_global.cursor_pos]
                    a["cursor_data"]=[i for i in SW_global.cursor_data]
                    a["recent_input_list"]=[i for i in SW_global.recent_input_list]
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_data.clear()
                    SW_global.cursor_pos.insert(0,0)
                    SW_global.axes_data[str(len(SW_global.axes_data))]=a
                    newCreateGuideLine(1,None,None,None,None)
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_data.clear()
                    SW_global.cursor_pos.insert(0,0)
                    kern_value_array.clear()
                    SW_global.kern_list.clear()
                    SW_global.letters_already_written.clear()
                    SW_global.letters_already_written.clear()
                    SW_global.kern_list.insert(0,0)
                    SW_global.kern_value_array.clear()
                    SW_global.kern_value_array.insert(0,0)
                    kern_value_array.clear()
                    kern_value_array.insert(0,0)
                    compositedot_already_applied_array.clear()
                    startdot_already_applied_array.clear()
                    decisiondot_already_applied_array.clear()
                    connectdot_already_applied_array.clear()
                    stoke_arrow_flag_pos=0
                    startdot_flag_pos=0
                    delete_list.clear()
                    decision_dot_flag_pos=0
                    next_axes=guideline_axes[l]
                    connect_dot_flag_pos=0
                    guideline_axes[l]=previous_axes
                if(SW_global.current_pos>15500):
                    guideline_axes[l]=next_axes
                    SW_global.current_axes=next_axes
                    SW_global.current_pos=0

                length12=len(SW_global.recent_input_list)
                print("SW_global.recent_input_list:",SW_global.recent_input_list)
                #user_input=delete_list1[j]
                #event_key=delete_list1[j]
                x_max=manuscript.x_max[user_input]
                kern_x=SW_global.kern_list[0]
                ###################################################################################
                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if user_input in skip_list:
                    if(color_letter_features_on_off):
                        c1,c2=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    else:
                        c1,c2=manuscript.return_manuscript_fonts(user_input)
                else:
                    if(color_letter_features_on_off):
                        x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                        c1,c2=font_check(x,y)
                    else:
                        x,y=manuscript.return_manuscript_fonts(user_input)
                        c1,c2=font_check(x,y)
            ####################################################################################

                c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)
             #   print("This is check point3")

                kern_x=SW_global.kern_list[0]+x_max+300
                SW_global.kern_list.insert(0,kern_x)
                kern_counter=len(kern_value_array)
                kern_value_array.insert(kern_counter,kern_x)
                SW_global.recent_input_list.insert(length12,event_key)
                delete_list.insert(length12,event_key)
                init_enrty_pos=len(SW_global.letters_already_written)
                inti_letter_pos=len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(init_enrty_pos,inti_letter_pos)
              #  print("Check point 4")
                if draw_type_color_letter==1:
                    if letter_dot_density_no_dot_on_off==1:
                        alp=0
                    else:
                        alp=temp_alp
                    if color_letter_features_on_off:
                        guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    else:
                        guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    n=len(c1)
                    if letter_dot_density_no_dot_on_off==1:
                        alp=0
                    else:
                        alp=temp_alp
                    if color_letter_features_on_off:
                        for i in range(n):
                            if i==0:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i==1:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i==2:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i==3:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    else:
                        for i in range(n):
                            guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

                fig.canvas.draw()
               # print("check point 5")

                import numpy as np
                item_cursor=kern_x-300
                cursor_y=list(np.linspace(-900,1500,500))
                cursor_x=list(np.full((500),item_cursor))
                SW_global.cursor_pos.append(item_cursor)
                cursor_x1=list(np.full((500),item_cursor))
                plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                if(SW_global.single_click_data!=None):
                    SW_global.single_click_data.set_visible(False)
                SW_global.single_click_data=plot_data[0]
                k2=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                for k5 in SW_global.cursor_data:
                    k5.set_visible(False)


                try:
                    for i in k2:
                        SW_global.cursor_data.append(i)
                        i.set_visible(False)
                except Exception as e:
                    print(e)
                #    print("I am check point22")
                fig.canvas.draw()
                final_enrty_pos = len(SW_global.letters_already_written)
                final_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
                print("This is kern_value_array:",kern_value_array)
                print("check point 77")
            if(guideline_axes[l]==SW_global.current_axes):
                print("check point 666666666")
                print("check point 78")
                print("i",SW_global.cursor_pos)
                for i in range(len(SW_global.cursor_pos)):
                    if(i==SW_global.current_pos_in_number):
                        print(i)
                        print(SW_global.current_pos_in_number)
                        print(SW_global.cursor_pos)
                 #       print("check point 80")
                        #print("pos1:",pos1)
                        #print("pos2:",pos2)
                        #if(len(SW_global.cursor_pos)-1>i+1):  This logic may need for guideline_axes[l]!=axesdata
                        print("check point alpha")
                        SW_global.current_pos_in_number=i+1
                        if(len(SW_global.cursor_pos)>i+1):
                            print("check point beta")
                            SW_global.current_pos=SW_global.cursor_pos[i+1]
                            (SW_global.cursor_data[i]).set_visible(True)
                        return delete_list,kern_value_array
                        break
                #print("check point 79")
               # return delete_list,kern_value_array
                #print("i",i)
                        #SW_global.current_axes=guideline_axes[l]
            else:
                print("check point 7777777")
                for i in range(SW_global.axes_data):
                    if(SW_global.axes_data[str(i)]["axis_data"]==SW_global.current_axes):
                        for k in range(len(SW_global.axes_data[str(i)]["cursor_pos"])):
                            if(k==SW_global.current_pos_in_number):
                                SW_global.current_pos_in_number=k+1
                                SW_global.current_pos=SW_global.axes_data[str(i)]["cursor_pos"][k+1]
                                (SW_global.axes_data[str(i)]["cursor_data"]).set_visible(True)
                        return delete_list,kern_value_array
                        break
            print("check point 7")
            print(kern_value_array)
        elif(guideline_axes[l]!=SW_global.current_axes):
            print("chdekdkk")
            print("check current_pos:",SW_global.current_pos)
            print("check current_axes:",SW_global.current_axes)
            if(guideline_axes[l]==SW_global.current_axes):
                print("current_pos is in guideline_axes")
            else:
                print("Check point 66")
                for k4 in range(len(SW_global.axes_data)):
                    if(SW_global.current_axes==SW_global.axes_data[str(k4)]["axis_data"]):
                        print("I am in axes no:",k4)
                        print("current_pos:",SW_global.current_pos)
                        break


            for k0 in range(len(SW_global.axes_data)):
                if(k0+1<len(SW_global.axes_data)):
                    if(SW_global.axes_data[str(k0)]["axis_data"]==SW_global.axes_data[str(k0+1)]["axis_data"]):
                        print("Yes we have some mistake ")
                    else:
                        print("No issue")



            print("I am in else part")
            print("check point 8888888888888")
            SW_global.temp_guideline_axes=None
            SW_global.temp_guideline_axes=SW_global.axes_data[str(key)]["axis_data"]
            count_of_axes=key
            kern_value_array2=[0]
            letters_already_written2=[]
            kern_list2=[0]
            recent_input_list2=[]
            g_val2=[i for i in SW_global.axes_data[str(key)]["lines"]]
            cursor_data2=[]
            cursor_pos2=[0]
            delete_list2=[]
            guideline_flag=-9999
            print("This is delete list:",delete_list1)
            temp_flag=0
            for k10 in range(len(delete_list1)):
                print("count_of_axes:",count_of_axes)
                print("axes is :",SW_global.temp_guideline_axes)
                #temp_guideline_axes=SW_global.axes_data[str(count_of_axes)]["axis_data"]
                print("axis need to be:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
                if(kern_list2[0]>15500):
                    print("check point we*********************************************************")
                    if(count_of_axes>len(SW_global.axes_data)-1):
                        #print("This is check point 11")
                        if(guideline_flag>0):
                            a=dict()
                            a["letters_already_written"]=[j for j in  letters_already_written2]
                            a["kern_value_array"]=[j for j in kern_value_array2]
                            a["delete_list"]=[j for j in delete_list2]
                            a["kern_list"]=[j for j in kern_list2]
                            a["lines"]=[j for j in g_val2]
                            a["gval"]=[j for j in g_val2]
                            a["cursor_pos"]=[j for j in cursor_pos2]
                            a["cursor_data"]=[j for j in cursor_data2]
                            a["axis_data"]=guideline_axes[l]
                            a["compositedot_already_applied_array"]=[]
                            a["decisiondot_already_applied_array"]=[]
                            a["connectdot_already_applied_array"]=[]
                            a["startdot_already_applied_array"]=[]
                            a["recent_input_list"]=[j for j in recent_input_list2]
                            a["connect_dot_flag_pos"]=0
                            a["decision_dot_flag_pos"]=0
                            a["stoke_arrow_flag_pos"]=0
                            a["startdot_flag_pos"]=0
                            SW_global.axes_data[str(len(SW_global.axes_data))]=a
                            newCreateGuideLine(1,None,None,None,None)
                            print("This is check point22")
                            count_of_axes=count_of_axes+1
                            SW_global.current_pos=0
                            SW_global.current_axes=guideline_axes[l]
                        else:
                         #   print("This is check point33")
                    ##        print("check point delta 2")
                            guideline_axes[l].lines.clear()
                            for j in g_val2:
                                guideline_axes[l].lines.append(j)
                            SW_global.letters_already_written.clear()
                            for j in letters_already_written2:
                                SW_global.letters_already_written.append(j)
                            SW_global.recent_input_list.clear()
                            for j in recent_input_list:
                                SW_global.recent_input_list.append(j)
                            SW_global.cursor_pos.clear()
                            for j in cursor_pos2:
                                SW_global.cursor_pos.append(j)
                            SW_global.cursor_data.clear()
                            for j in cursor_data2:
                                SW_global.cursor_data.append(j)
                            SW_global.kern_list.clear()
                            for j in kern_list2:
                                SW_global.kern_list.append(j)
                            guideline_flag=40
                            #newCreateGuideLine(1,None,None,None)
                            count_of_axes=count_of_axes+1
                          #  print("This is check point44")
                      ##  print("check point delta 3")
                      #  g_val2.clear()
                        delete_list2.clear()
                        cursor_data2.clear()
                        cursor_pos2.insert(0,0)
                        letters_already_written2.clear()
                        recent_input_list2.clear()
                        kern_value_array2.clear()
                        kern_value_array2.insert(0,0)
                        kern_list2.clear()
                        kern_list2.insert(0,0)
                        # guideline_flag=40 #### speacial flag for guide line indication
                        SW_global.temp_guide_line_axes=guideline_axes[l]
                        #print("This is check point55")



                    else:
                        #print("check point 66")
                        SW_global.axes_data[str(count_of_axes)]["letters_already_written"]=[k for k in letters_already_written2]
                        SW_global.axes_data[str(count_of_axes)]["cursor_pos"]=[k for k in cursor_pos2]
                        SW_global.axes_data[str(count_of_axes)]["cursor_data"]=[ k for k in cursor_data2]
                        SW_global.axes_data[str(count_of_axes)]["recent_input_list"]=[k for k in recent_input_list2]
                        SW_global.axes_data[str(count_of_axes)]["delete_list"]=[k for k in delete_list2]
                        SW_global.axes_data[str(count_of_axes)]["gval"]=[k for k in g_val2]
                        SW_global.axes_data[str(count_of_axes)]["lines"]=[k for k in g_val2]
                        SW_global.axes_data[str(count_of_axes)]["kern_value_array"]=[k for k in kern_value_array2]
                        SW_global.axes_data[str(count_of_axes)]["kern_list"]=[k for k in kern_list2]
                        g_val2.clear()
                        delete_list2.clear()
                        cursor_data2.clear()
                        cursor_pos2.clear()
                        cursor_pos2.insert(0,0)
                        letters_already_written2.clear()
                        recent_input_list2.clear()
                        kern_value_array2.clear()
                        kern_value_array2.insert(0,0)
                        kern_list2.clear()
                        print("check point 41")
                        kern_list2.insert(0,0)
                        print("check point wwwwqqqq")
                        print("count_of_axes:",count_of_axes)
                        print("len(axes_data):",len(SW_global.axes_data))
                        if(count_of_axes>=len(SW_global.axes_data)-1):
                            SW_global.temp_guideline_axes=guideline_axes[l]
                            g_val2.clear()
                            g_val2.append(guideline_axes[l].lines[0])
                            g_val2.append(guideline_axes[l].lines[1])
                            g_val2.append(guideline_axes[l].lines[2])
                            g_val2.append(guideline_axes[l].lines[3])
                            #for h1 in guideline_axes[l].lines:
                            #    g_val2.append(h1)




                          #  print("check point 27 wwwwww")
                            # for x in range(len(SW_global.axes_data)):
                            #     print(SW_global.axes_data[str(x)]["axis_data"])
                            # print("count_of_axes:",count_of_axes)
                            # count_of_axes=count_of_axes+1
                            # print("After increment :",count_of_axes)
                            # print("This is previous guideline axes",SW_global.temp_guideline_axes)
                            # print(SW_global.axes_data[str(count_of_axes)]["axis_data"])
                            # SW_global.temp_guide_line_axes=None
                            # SW_global.temp_guide_line_axes=SW_global.axes_data[str(count_of_axes)]["axis_data"]
                            # print("This is after guide",SW_global.temp_guideline_axes)
                        else:
                            count_of_axes=count_of_axes+1
                            SW_global.temp_guideline_axes=SW_global.axes_data[str(count_of_axes)]["axis_data"]
                            g_val2.clear()
                            for h1 in SW_global.axes_data[str(count_of_axes)]["lines"]:
                                g_val2.append(h1)
                         #   print("check point 28")
                         #   SW_global.temp_guideline_axes=guideline_axes[l]
                # print("check point 29")
            #     #### Write code for data inserting on speacific axes ####
                length12=len(recent_input_list2)
                user_input=delete_list1[k10]
                print("SW_global.axes_data",SW_global.temp_guideline_axes)
                print("QWE:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
              #  print("user_input:",user_input)
                x_max=manuscript.x_max[user_input]
                kern_x=kern_list2[0]
              #  print("I am in loop check point1 ")

                ###################################################################################
                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if user_input in skip_list:
                    if(color_letter_features_on_off):
                        c1,c2=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    else:
                        c1,c2=manuscript.return_manuscript_fonts(user_input)
                else:
                    if(color_letter_features_on_off):
                        x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                        c1,c2=font_check(x,y)
                    else:
                        x,y=manuscript.return_manuscript_fonts(user_input)
                        c1,c2=font_check(x,y)
            ####################################################################################

                c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)


                kern_x=kern_list2[0]+x_max+300
                kern_list2.insert(0,kern_x)
               # print("check point 30")
                # c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)
                kern_counter=len(kern_value_array2)
                kern_value_array2.insert(kern_counter,kern_x)
                recent_input_list2.insert(length12,user_input)
                delete_list2.insert(length12,user_input)
                init_enrty_pos=len(letters_already_written2)
                inti_letter_pos=len(g_val2)
                #print("check point 31")
                print("SW_global.temp_guideline_axes:",SW_global.temp_guideline_axes)
                letters_already_written2.insert(init_enrty_pos,inti_letter_pos)
             #   print("check point 2")
                temp_o=[]

                if(draw_type_color_letter==1):
                 #   print("check point 32")
                    if(letter_dot_density_no_dot_on_off==1):
                        alp=0
                    else:
                        alp=temp_alp
                    if(color_letter_features_on_off):
                        temp_o.clear()
                  #      print("check point 33")
                        temp_o=SW_global.temp_guideline_axes.plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        for k2 in temp_o:
                            g_val2.append(k2)
                        print("count of axes:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
                        print("temp_guideline_axes",SW_global.temp_guideline_axes)
                    else:
                   #     print("check point 34")
                        temp_o=SW_global.temp_guideline_axes.plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        for k2 in temp_o:
                            g_val2.append(k2)
                        print("count_of_axes",SW_global.axes_data[str(count_of_axes)]["axis_data"])
                        print("SW_global",SW_global.temp_guideline_axes)
                else:
                   # print("check point 35")
                    n=len(c1)
                    if letter_dot_density_no_dot_on_off == 1:
                        alp=0
                    else:
                        alp=temp_alp

                    #print("check point 36")


                    if(color_letter_features_on_off):
                     #   print("check point 37")
                        for i in range(n):
                            if i==0:
                                temp_o.clear()
                                temp_o=SW_gobal.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                                for k2 in temp_o:
                                    g_val2.append(k2)
                            if i==1:
                                temp_o.clear()
                                temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                                for k2 in temp_o:
                                    g_val2.append(k2)
                            if i==2:
                                temp_o.clear()
                                temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                                for k2 in temp_o:
                                    g_val2.append(k2)
                            if i==3:
                                temp_o.clear()
                                temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                                for k2 in temp_o:
                                    g_val2.append(k2)
                    else:
                      #  print("check point 38")
                        for i in range(n):
                            temp_o.clear()
                            temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            for k2 in temp_o:
                                g_val2.append(k2)

                fig.canvas.draw()

                import numpy as np
                item_cursor=kern_x-300
                cursor_y=list(np.linspace(-900,1500,500))
                cursor_x=list(np.full(500,item_cursor))
                cursor_pos2.append(item_cursor)
                cursor_x1=list(np.full(500,item_cursor))
                if(SW_global.single_click_data!=None):
                   # print("check point 39")
                    SW_global.single_click_data.set_visible(False)

                plot_data=SW_global.temp_guideline_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                SW_global.single_click_data=plot_data[0]
                k2=SW_global.temp_guideline_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))

              #  print("check point 40")

                for j10 in k2:
                    cursor_data2.append(j10)
                    j10.set_visible(False)

              #  print("check point 41")


                final_enrty_pos = len(letters_already_written2)
                final_letter_pos = len(g_val2)
                letters_already_written2.insert(final_enrty_pos, final_letter_pos)

              #  print("check point 42")
           #     print("I am in for loop end part ")


            for k1 in SW_global.axes_data[str(key)]["cursor_pos"]:
                if k1==SW_global.current_pos_in_number:
                    if((k1+1)>len(SW_global.axes_data[str(key)]["cursor_pos"])):
                        #### set next axes of current_axes as current_axes and current_pos =0
                        #### if there is no axes_data left then make guideline_axes as current_axes
                        #### else make normal current_pos
                        if((key+1)>len(SW_global.axes_data)-1):
                            SW_global.current_axes=guideline_axes[l]
                            SW_global.current_pos=0
                        else:
                            SW_global.current_axes=SW_global.axes_data[str(key+1)]["axis_data"]
                            SW_global.current_pos=0

                    else:
                        SW_global.current_pos=(SW_global.axes_data[str(key)]["cursor_pos"])[k1+1]
                        SW_global.current_axes=SW_global.axes_data[str(key)]["axis_data"]
                        SW_global.current_pos_in_number=k1+1
            SW_global.cursor_pos.clear()
            for k1 in cursor_pos2:
                SW_global.cursor_pos.append(k1)
            for k1 in cursor_data2:
                SW_global.cursor_data.append(k1)
            guideline_axes[l].lines.clear()
            for k1 in g_val2:
                guideline_axes[l].lines.append(k1)

            SW_global.letters_already_written.clear()

            for k1 in letters_already_written2:
                SW_global.letters_already_written.append(k1)

            SW_global.kern_list.clear()
            for k1 in kern_list2:
                SW_global.kern_list.append(k1)



            return delete_list2,kern_value_array2




           #return detele_list2,kern_value_array2
    except Exception as e:
        print(e)


    return



def add_letter_with_mouse_and_from_end(axesdata=None,delete_list=None,pos=None,event_key=None,kern_value_array=None):

    ###### Need to change there is some bug ####
    try:
        kern_value_array=list(kern_value_array)
        if((axesdata==None) and (pos==None)):
            length12 = len(SW_global.recent_input_list)
            user_input = event_key
            x_max = manuscript.x_max[user_input]
            kern_x = SW_global.kern_list[0]
            skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
            if color_letter_features_on_off:
                if user_input in skip_list:
                    c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                else:
                    x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    c1,c2=font_check(x,y)
            else:
               # print("check point 4")
                if user_input in skip_list:
                   c1, c2 = manuscript.return_manuscript_fonts(user_input)
                else:
                   x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                   c1,c2=font_check(x,y)
               # print(c1,"-",c2)


            c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)

            kern_x = SW_global.kern_list[0] + x_max + 300
            SW_global.kern_list.insert(0, kern_x)
            kern_counter = len(kern_value_array)
           # print("This is check point 6")
            kern_value_array.insert(kern_counter, kern_x)
           # print("This is check point 7")
            #print(kern_value_array)
            SW_global.recent_input_list.insert(length12, event_key)
            #print("this is list")
            delete_list.insert(length12, event_key)
            #print(delete_list)
            init_enrty_pos = len(SW_global.letters_already_written)
            inti_letter_pos = len(guideline_axes[l].lines)
            #print("This is guide line axes length ")
            #print(len(guideline_axes[l].lines))
            SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
            #print(SW_global.letters_already_written)
            if draw_type_color_letter == 1:
                if letter_dot_density_no_dot_on_off == 1:
                    alp = 0
                else:
                    alp = temp_alp
                if color_letter_features_on_off:
                    guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

            else:
                n = len(c1)
                if letter_dot_density_no_dot_on_off == 1:
                    alp = 0
                else:
                    alp = temp_alp
                if color_letter_features_on_off:
                    for i in range(n):
                        if i == 0:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i == 1:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i == 2:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i == 3:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    for i in range(n):
                        guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
            #############################   Cursor part code of inserting ###############################
            import numpy as np
            item_cursor=kern_x-300
            cursor_y=list(np.linspace(-900,1500,500))
            #cursor_y_neg=list(np.lenspace)
            cursor_x=list(np.full((500),item_cursor))
            SW_global.cursor_pos.append(item_cursor)
            cursor_x1=list(np.full((500),item_cursor))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
            plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            SW_global.single_click_data=plot_data[0]
            ##### Add new two variable for current axes and current pos #####
            SW_global.current_axes=guideline_axes[l]
            SW_global.current_pos=item_cursor
            SW_global.current_pos_in_number=len(delete_list)


            k=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            for i in k:
                SW_global.cursor_data.append(i)
                i.set_visible(False)

            #SW_global.cursor_data.append(k)
            #print(SW_global.cursor_data)
            for cur_count in range(len(SW_global.cursor_data)-1):
                invisible_item=SW_global.cursor_data[cur_count]
                #print("This is invisible_item")
                #print(invisible_item)
                invisible_item.set_visible(False)
            fig.canvas.draw()
            #print(guideline_axes[0].lines)

    # -----------------------------------------------------------------------------------------------------
            final_enrty_pos = len(SW_global.letters_already_written)
            final_letter_pos = len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
            features_checking_function()
            return delete_list,kern_value_array
            #### 1st if condition end  #####
        elif((axesdata==guideline_axes[l]) and (SW_global.current_pos==SW_global.cursor_pos[-1])):
            length12 = len(SW_global.recent_input_list)
            user_input = event_key
            x_max = manuscript.x_max[user_input]
            kern_x = SW_global.kern_list[0]
            skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
            if color_letter_features_on_off:
                if user_input in skip_list:
                    c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                else:
                    x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    c1,c2=font_check(x,y)
            else:
                if user_input in skip_list:
                    c1, c2 = manuscript.return_manuscript_fonts(user_input)
                else:
                    x,y=manuscript.return_manuscript_fonts(user_input)
                    c1,c2=font_check(x,y)
            c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)
            kern_x = SW_global.kern_list[0] + x_max + 300
            SW_global.kern_list.insert(0, kern_x)
            kern_counter = len(kern_value_array)
            kern_value_array.insert(kern_counter, kern_x)
            #print(kern_value_array)
            SW_global.recent_input_list.insert(length12, event_key)
            #print("this is list")
            delete_list.insert(length12, event_key)
            #print(delete_list)
            init_enrty_pos = len(SW_global.letters_already_written)
            inti_letter_pos = len(guideline_axes[l].lines)
            #print("This is guide line axes length ")
            #print(len(guideline_axes[l].lines))
            SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
            #print(SW_global.letters_already_written)
            if draw_type_color_letter == 1:
                if letter_dot_density_no_dot_on_off == 1:
                    alp = 0
                else:
                    alp = temp_alp
                if color_letter_features_on_off:
                    guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

            else:
                n = len(c1)
                if letter_dot_density_no_dot_on_off == 1:
                    alp = 0
                else:
                    alp = temp_alp
                if color_letter_features_on_off:
                    for i in range(n):
                        if i == 0:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i == 1:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i == 2:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i == 3:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    for i in range(n):
                        guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
            #############################   Cursor part code of inserting ###############################
            # import numpy as np
            # if(len(SW_global.cursor_data)!=0):
            #  #   print("It is ok")
            #   #  print(delete_list)
            #   #  print(SW_global.letters_already_written)
            #    # print(cursor_data)
            #     #cursor_pos(cursor_pos)
            #     pass
            # else:
            #     pass
                #print("It is empty")
            item_cursor=kern_x-300
            cursor_y=list(np.linspace(-900,1500,500))
            #cursor_y_neg=list(np.lenspace)
            cursor_x=list(np.full((500),item_cursor))
            SW_global.cursor_pos.append(item_cursor)
            cursor_x1=list(np.full((500),item_cursor))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
            plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            SW_global.single_click_data=plot_data[0]
            ##### Add new two variable for current axes and current pos #####
            SW_global.current_axes=guideline_axes[l]
            SW_global.current_pos=item_cursor
            SW_global.current_pos_in_number=len(delete_list)


            k=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            #print(k)
            #print(k)
            for i in k:
                SW_global.cursor_data.append(i)
                i.set_visible(False)

            #SW_global.cursor_data.append(k)
            #print(SW_global.cursor_data)
            for cur_count in range(len(SW_global.cursor_data)-1):
                invisible_item=SW_global.cursor_data[cur_count]
                #print("This is invisible_item")
                #print(invisible_item)
                invisible_item.set_visible(False)
            fig.canvas.draw()
            #print(guideline_axes[0].lines)

    # -----------------------------------------------------------------------------------------------------
            final_enrty_pos = len(SW_global.letters_already_written)
            final_letter_pos = len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
            features_checking_function()
            return delete_list,kern_value_array
        elif((axesdata==guideline_axes[l])):
            for i in range(len(SW_global.cursor_pos)):
                if(SW_global.cursor_pos[i]<SW_global.current_pos):
                    SW_global.current_pos_in_number=i
            SW_global.entire_delete_list_for_one_page.clear()
            temp_current_pos_in_number=SW_global.current_pos_in_number
            for i in range(len(delete_list)):
                if(i==temp_current_pos_in_number):
                    SW_global.entire_delete_list_for_one_page.append(event_key)
                    SW_global.entire_delete_list_for_one_page.append(delete_list[i])
                    SW_global.current_pos_in_number=SW_global.current_pos_in_number+1
                else:
                    SW_global.entire_delete_list_for_one_page.append(delete_list[i])
            #print("This is after update :", SW_global.entire_delete_list_for_one_page)
            for i in range(len(guideline_axes[l].lines)):
                if(i>3):
                    ((guideline_axes[l].lines)[i]).set_visible(False)
            set_key=10000
            SW_global.cursor_pos.clear()
            SW_global.cursor_data.clear()
            SW_global.cursor_pos.insert(0,0)

            kern_value_array.clear()
            SW_global.kern_list.clear()
            #print("check point 599")
            SW_global.letters_already_written.clear()
            SW_global.letters_already_written.clear()
            SW_global.kern_list.insert(0,0)
            SW_global.kern_value_array.clear()
            SW_global.kern_value_array.insert(0,0)
            kern_value_array.clear()
            kern_value_array.insert(0,0)
            SW_global.recent_input_list.clear()
            #print("This is check point 2")
            #print(guideline_axes[l].lines)
            compositedot_already_applied_array.clear()
            startdot_already_applied_array.clear()
            decisiondot_already_applied_array.clear()
            connectdot_already_applied_array.clear()
            stoke_arrow_flag_pos =0
            #print("This is len")
            #print(guideline_axes[l].lines)
            startdot_flag_pos=0
            decision_dot_flag_pos=0
            connect_dot_flag_pos=0
            print("Delete list:",SW_global.entire_delete_list_for_one_page)
            ####delete_list1,kern_value_array1=cut_add_letter_from_any_position(delete_list1=SW_global.entire_delete_list_for_one_page,current_axes=axesdata,key=set_key)
            print("SW_global.guideline_axes[l]",guideline_axes[l])
            print("SW_global.kern",SW_global.kern_list)
            print("SW_global.recent_input_list:",SW_global.recent_input_list)
            #print("This is kern value array22222:",kern_value_array)
            return delete_list1,kern_value_array1


        elif((axesdata!=guideline_axes[l])):
            #print("This is from addddddddd       letter ****************************")
            temp_flag=-9999
            SW_global.entire_delete_list_for_one_page.clear()
            for i in range(len(SW_global.axes_data)):
                if((SW_global.axes_data[str(i)]["axis_data"])==SW_global.current_axes):
                    print("i am in check point v2222:",i)
                    if(SW_global.current_pos==(SW_global.axes_data[str(i)]["cursor_pos"])[-1]):
             #           print("check point3 946647211")
                        for k in range(len(SW_global.axes_data[str(i)]["delete_list"])):
                            SW_global.entire_delete_list_for_one_page.append((SW_global.axes_data[str(i)]["delete_list"])[k])
                        i=i+1
                        for k in range(len(SW_global.axes_data[str(i)]["delete_list"])):
                            if(k==0):
                                SW_global.entire_delete_list_for_one_page.append(event_key)
                                SW_global.entire_delete_list_for_one_page.append((SW_global.axes_data[str(i)]["delete_list"])[k])
                            else:
                                SW_global.entire_delete_list_for_one_page.append((SW_global.axes_data[str(i)]["delete_list"])[k])
                        SW_global.current_pos_in_number=0
                        SW_global.current_axes=SW_global.axes_data[str(i)]["axis_data"]
                        temp_flag=i
                    else:
                        SW_global.current_pos_in_number
                        print("check point 34")
                        SW_global.entire_delete_list_for_one_page.clear()

                        print("staclldkd:",SW_global.current_pos_in_number)
                        temp=-999
                        ##### Need to write code for that #####
                        for j in range(len(SW_global.axes_data[str(i)]["delete_list"])):
                            print(j)
                            print(int(SW_global.current_pos_in_number))
                            if(j==int(SW_global.current_pos_in_number)):
              #                  print("This is check point 45")
                                SW_global.entire_delete_list_for_one_page.append(event_key)
                                SW_global.entire_delete_list_for_one_page.append((SW_global.axes_data[str(i)]["delete_list"])[j])
                               # SW_global.current_pos_in_number=SW_global.current_pos_in_number+1
                            else:
               #                 print("This is check point 46")
                                SW_global.entire_delete_list_for_one_page.append((SW_global.axes_data[str(i)]["delete_list"])[j])
                                temp_flag=j
                        SW_global.current_pos_in_number=SW_global.current_pos_in_number+1

                                #SW_global.current_pos_in_number=SW_global.current_pos_in_number+1

                        #for j in range(len(SW_global.axes_data[str(i)]["delete_list"])):
                         #   if(j==SW_global.current_pos-1):


                elif(temp_flag>=0):
                    for j in SW_global.axes_data[str(i)]["delete_list"]:
                        SW_global.entire_delete_list_for_one_page.append(j)
                if(i==len(SW_global.axes_data)-1):
                    for j in delete_list:
                        SW_global.entire_delete_list_for_one_page.append(j)
            fl=-99999
            set_key=-9999
           # print("Entire delete list:where current_axes>guideline_axes",SW_global.entire_delete_list_for_one_page)
           # print("check point 590")
            for i in range(len(SW_global.axes_data)):
                if((SW_global.axes_data[str(i)]["axis_data"])==axesdata):
            #        print("check point 591")
                    set_key=i
                    (SW_global.axes_data[str(i)]["letters_already_written"]).clear()
                    (SW_global.axes_data[str(i)]["kern_value_array"]).clear()
                    (SW_global.axes_data[str(i)]["kern_list"]).clear()
                    (SW_global.axes_data[str(i)]["delete_list"]).clear()
                    (SW_global.axes_data[str(i)]["compositedot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(i)]["startdot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(i)]["decisiondot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(i)]["connectdot_already_applied_array"]).clear()
                    SW_global.axes_data[str(i)]["stoke_arrow_flag_pos"]=0
                    SW_global.axes_data[str(i)]["startdot_flag_pos"]=0
                    SW_global.axes_data[str(i)]["stoke_arrow_flag_pos"]=0
                    SW_global.axes_data[str(i)]["connect_dot_flag_pos"]=0
                    (SW_global.axes_data[str(i)]["lines"]).clear()
                    (SW_global.axes_data[str(i)]["gval"]).clear()
                    (SW_global.axes_data[str(i)]["cursor_pos"]).clear()
                    (SW_global.axes_data[str(i)]["cursor_data"]).clear()
                    (SW_global.axes_data[str(i)]["recent_input_list"]).clear()
             #       print("check point 593")
                    #SW_global.cursor_pos.insert(0,0)
                    (SW_global.axes_data[str(i)]["cursor_pos"]).append(0)
                    (SW_global.axes_data[str(i)]["kern_list"]).append(0)
                    (SW_global.axes_data[str(i)]["kern_value_array"]).append(0)
                    fl=i
              #      print("check point 594")
                elif(fl>=0):
              #      print("check point 592")
                    (SW_global.axes_data[str(i)]["letters_already_written"]).clear()
                    (SW_global.axes_data[str(i)]["kern_value_array"]).clear()
                    (SW_global.axes_data[str(i)]["kern_list"]).clear()
                    (SW_global.axes_data[str(i)]["delete_list"]).clear()
                    (SW_global.axes_data[str(i)]["compositedot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(i)]["startdot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(i)]["decisiondot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(i)]["connectdot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(i)]["recent_input_list"]).clear()
                    SW_global.axes_data[str(i)]["stoke_arrow_flag_pos"]=0
                    SW_global.axes_data[str(i)]["startdot_flag_pos"]=0
                    SW_global.axes_data[str(i)]["stoke_arrow_flag_pos"]=0
                    SW_global.axes_data[str(i)]["connect_dot_flag_pos"]=0
                    (SW_global.axes_data[str(i)]["lines"]).clear()
                    (SW_global.axes_data[str(i)]["gval"]).clear()
                    (SW_global.axes_data[str(i)]["cursor_pos"]).clear()
                    (SW_global.axes_data[str(i)]["cursor_data"]).clear()
                    (SW_global.axes_data[str(i)]["recent_input_list"]).clear()
                    #SW_global.cursor_pos.insert(0,0)
                    (SW_global.axes_data[str(i)]["cursor_pos"]).append(0)
                    (SW_global.axes_data[str(i)]["kern_list"]).append(0)
                    (SW_global.axes_data[str(i)]["kern_value_array"]).append(0)
                    fl=i
            SW_global.cursor_pos.clear()
            SW_global.cursor_data.clear()
            SW_global.cursor_pos.insert(0,0)
            #print("This is decision dot flag")
            #print(decision_dot_flag_pos)
            #print("This is axes data")
            #print(len(SW_global.axes_data))
            ##SW_global.axes_data[str(len(SW_global.axes_data))]=a
            #print(SW_global.axes_data)
            #print(guideline_axes[l].lines)
            kern_value_array.clear()
            SW_global.kern_list.clear()
          #  print("check point 599")
            SW_global.letters_already_written.clear()
            SW_global.letters_already_written.clear()
            SW_global.kern_list.insert(0,0)
            SW_global.kern_value_array.clear()
            SW_global.kern_value_array.insert(0,0)
            kern_value_array.clear()
            kern_value_array.insert(0,0)
            SW_global.recent_input_list.clear()
            #print("This is check point 2")
            #print(guideline_axes[l].lines)
            compositedot_already_applied_array.clear()
            startdot_already_applied_array.clear()
            decisiondot_already_applied_array.clear()
            connectdot_already_applied_array.clear()
            stoke_arrow_flag_pos =0
            #print("This is len")
            #print(guideline_axes[l].lines)
            startdot_flag_pos=0
            decision_dot_flag_pos=0
            connect_dot_flag_pos=0
            delete_list.clear()
            if(axesdata==guideline_axes[l]):
                set_key=10000



            delete_list,kern_value_array=cut_add_letter_from_any_position(delete_list1=SW_global.entire_delete_list_for_one_page,current_axes=axesdata,key=set_key)
            SW_global.current_axes=guideline_axes[l]
          #  print(SW_global.current_axes)
          #  print("Thisis deletelist:",delete_list)
          #  print(kern_value_array)
            #SW_global.single_click_cursor_pos=
            return delete_list,kern_value_array
    except Exception as e:
        print(e)
        pass
    return





def new_line_creation_controller(event_key=None):
    if(SW_global.kern_list[0]>15000):
        ##### Checking for space is present or not
        key=None 
        if(" " in delete_list):
            for j in range(len(delete_list)):
                if(delete_list[j]==" "):
                    if(key==None):
                        key=j
                    if(key!=None):
                        if(key<j):
                            key=j
        next_line_start_delete_list=[]
        if((key!=None) and (len(delete_list)-1>key)):
            for j in range(key+1,len(delete_list)-1):
                next_line_start_delete_list.append(delete_list[j])

        #for j in range(key+1,len(delete_list)-1):
        ### Need to change the while loop to for loop for optimization ### 
        while(len(delete_list)>=key+1):
            del delete_list[len(delete_list)-1]


        ### Need to add function  for entire add letter with axes ###






    return 


###### Main checking point is kern value #####
##### We have to check when we enter any letter where is it cross the limit kern value #####
###### if it's crossed the kern limit then then check for any change #######

def delete_list_divide(key_axes=None,key_current_pos=None,key3=None):
    SW_global.delete_list_divide.clear()
    if((key_axes!=None) and(key_current_pos!=None)):
        if(key_axes==guideline_axes[l]):
            print()
            temp_list=[]
            count=0
            for j in delete_list:
                if(j==" "):
                    print()
        else:
            print()

    
    
    return 



def last_word_detection(axesdata=None):
    if((axesdata!=None) and (axesdata==guideline_axes[l])):
        count=None
        if(" " in delete_list):
            for j in range(len(delete_list)):
                if(delete_list[j]==" "):
                    if(count==None):
                        count=j
                    if(count<j):
                        count=j
        if(count==None):
            return None
        if(count==0):
            return 0
        else:
            return count
    elif(axesdata!=None):
        count=None
        key=None
        for j in range(len(SW_global.axes_data)):
            if(SW_global.axes_data[str(j)]["axis_data"]==axesdata):
                key=j
                break

        temp_delete_list=[]
        if(" " in SW_global.axes_data[str(key)]["delete_list"]):
            for j in range(len(SW_global.axes_data[str(key)]["delete_list"])):
                if (SW_global.axes_data[str(key)]["delete_list"])[j]==" ":
                    if(count==None):
                        count=j
                    if(count<j):
                        count=j
            return count
        else:
            return None
    return 





def add_digit_in_axes(list_of_digit=None,spec_axes=None,baselines_objects_array=None):
    print(" I am on add digit in axes")
    if((list_of_digit!=None) and(spec_axes!=None) and (baselines_objects_array!=None)):
        kern_list2=[0]
        kern_value_array2=[0]
        delete_list2=[]
        cursor_pos2=[0]
        cursor_data2=[]
        recent_input_list2=[]
        letters_already_written2=[]

        temp_guideline_axes2=[]
        temp_guideline_axes2.extend(baselines_objects_array)
        temp_line=[]
        temp_axes=[]
        for j in list_of_digit:
            if(j==" "):
               # print("I am for space")
            #    print("This space")
                length12 = len(recent_input_list2)
                user_input = " "
                event_key=" "
                x_max= 0
                kern_x =kern_list2[0]
                c1,c2=[0],[0]
               # print("cchhhhh11233")
                kern_x =kern_list2[0] + 300
                kern_list2.insert(0, kern_x)
                kern_counter = len(kern_value_array2)
                kern_value_array2.insert(kern_counter, kern_x)
                recent_input_list2.insert(length12, event_key)
                delete_list2.insert(length12,event_key)
                init_enrty_pos=len(letters_already_written2)
                init_letter_pos=len(temp_guideline_axes2)
                letters_already_written2.insert(init_enrty_pos,init_letter_pos)
                temp_line.clear()
                temp_line=spec_axes.plot(c1,c2)
                temp_guideline_axes2.append(temp_line[0])
                temp_line[0].set_visible(False)
               # print("checddddd4566")
                item_cursor=kern_x
                cursor_y=list(np.linspace(-900,1500,500))
                cursor_x=list(np.full((500),item_cursor))
                cursor_pos2.append(item_cursor)
                cursor_x1=list(np.full((500),item_cursor))
                plot_data=spec_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                SW_global.single_click_data=plot_data[0]
                k=spec_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                print("cjdhehdhfhfh")
                cursor_data2.append(k[0])
                for cur_count in range(len(cursor_data2)-1):
                    invisible_item=cursor_data2[cur_count]
                    invisible_item.set_visible(False)

                final_enrty_pos = len(letters_already_written2)
                final_letter_pos = len(temp_guideline_axes2)
                letters_already_written2.insert(final_enrty_pos, final_letter_pos)
            if(j!=" "):
                length12 = len(recent_input_list2)
              #  print("I am not for space")
                user_input = j
                event_key=j
                print("list_of_digit:",list_of_digit)
                x_max = manuscript.x_max[user_input]
                kern_x =kern_list2[0]
                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if color_letter_features_on_off:
                    if user_input in skip_list:
                        c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    else:
                        x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                        c1,c2=font_check(x,y)
                else:
                    if user_input in skip_list:
                        c1, c2 = manuscript.return_manuscript_fonts(user_input)
                    else:
                        x,y=manuscript.return_manuscript_fonts(user_input)
                        c1,c2=font_check(x,y)
                c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)
                kern_x = kern_list2[0] + x_max + 300
                kern_list2.insert(0, kern_x)
                kern_counter = len(kern_value_array2)
                kern_value_array2.insert(kern_counter, kern_x)
                #print(kern_value_array)
                recent_input_list2.insert(length12, event_key)
                #print("this is list")
                delete_list2.insert(length12, event_key)
                #print(delete_list)
                init_enrty_pos = len(letters_already_written2)
                inti_letter_pos = len(temp_guideline_axes2)
                #print("This is guide line axes length ")
                #print(len(guideline_axes[l].lines))
                letters_already_written2.insert(init_enrty_pos, inti_letter_pos)
                #print(SW_global.letters_already_written)
                if draw_type_color_letter == 1:
                    if letter_dot_density_no_dot_on_off == 1:
                        alp = 0
                    else:
                        alp = temp_alp
                    if color_letter_features_on_off:
                        temp_axes.clear()
                        temp_axes=spec_axes.plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        temp_guideline_axes2.append(temp_axes[0])
                    else:
                        temp_axes.clear()
                        temp_axes=spec_axes.plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        temp_guideline_axes2.append(temp_axes[0])


                else:
                    n = len(c1)
                    if letter_dot_density_no_dot_on_off == 1:
                        alp = 0
                    else:
                        alp = temp_alp
                    if color_letter_features_on_off:
                        for i in range(n):
                            if i == 0:
                                temp_axes.clear()
                                temp_axes=spec_axes.plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                                temp_guideline_axes2.append(temp_axes[0])
                            if i == 1:
                                temp_axes.clear()
                                temp_axes=spec_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                                temp_guideline_axes2.append(temp_axes[0])
                            if i == 2:
                                temp_axes.clear()
                                temp_axes=spec_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                                temp_guideline_axes2.append(temp_axes[0])
                            if i == 3:
                                temp_axes.clear()
                                temp_axes=spec_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                                temp_guideline_axes2.append(temp_axes[0])
                    else:
                        for i in range(n):
                            temp_axes.clear()
                            temp_axes=spec_axes.plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            temp_guideline_axes2.append(temp_axes[0])
                #############################   Cursor part code of inserting ###############################
                item_cursor=kern_x-300
                cursor_y=list(np.linspace(-900,1500,500))
                #cursor_y_neg=list(np.lenspace)
                cursor_x=list(np.full((500),item_cursor))
                cursor_pos2.append(item_cursor)
                cursor_x1=list(np.full((500),item_cursor))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
                plot_data=spec_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                ##### Add new two variable for current axes and current pos #####
                plot_data[0].set_visible(False)
                k=spec_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                for i in k:
                    cursor_data2.append(i)
                    i.set_visible(False)
                for cur_count in range(len(cursor_data2)-1):
                    invisible_item=cursor_data2[cur_count]
                    invisible_item.set_visible(False)
        # -----------------------------------------------------------------------------------------------------
                final_enrty_pos = len(letters_already_written2)
                final_letter_pos = len(temp_guideline_axes2)
                letters_already_written2.insert(final_enrty_pos, final_letter_pos)
    fig.canvas.draw()
    print("I am on end _of add digit")
    return kern_value_array2,kern_list2,delete_list2,recent_input_list2,cursor_data2,cursor_pos2,letters_already_written2,temp_guideline_axes2





def add_any_letter_with_space_from_rear_side(event_key=None):
    try:
        if(event_key!=None):
            if(event_key!=" "):
                length12 = len(SW_global.recent_input_list)
                user_input = event_key
                x_max = manuscript.x_max[user_input]
                kern_x = SW_global.kern_list[0]
                skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
                if color_letter_features_on_off:
                    if user_input in skip_list:
                        c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    else:
                        x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                        c1,c2=font_check(x,y)
                else:
                    if user_input in skip_list:
                        c1, c2 = manuscript.return_manuscript_fonts(user_input)
                    else:
                        x,y=manuscript.return_manuscript_fonts(user_input)
                        c1,c2=font_check(x,y)
                c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)
                kern_x = SW_global.kern_list[0] + x_max + 300
                SW_global.kern_list.insert(0, kern_x)
                kern_counter = len(kern_value_array)
                kern_value_array.insert(kern_counter, kern_x)
                #print(kern_value_array)
                SW_global.recent_input_list.insert(length12, event_key)
                #print("this is list")
                delete_list.insert(length12, event_key)
                #print(delete_list)
                init_enrty_pos = len(SW_global.letters_already_written)
                inti_letter_pos = len(guideline_axes[l].lines)
                #print("This is guide line axes length ")
                #print(len(guideline_axes[l].lines))
                SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
                #print(SW_global.letters_already_written)
                if draw_type_color_letter == 1:
                    if letter_dot_density_no_dot_on_off == 1:
                        alp = 0
                    else:
                        alp = temp_alp
                    if color_letter_features_on_off:
                        guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    else:
                        guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

                else:
                    n = len(c1)
                    if letter_dot_density_no_dot_on_off == 1:
                        alp = 0
                    else:
                        alp = temp_alp
                    if color_letter_features_on_off:
                        for i in range(n):
                            if i == 0:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i == 1:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i == 2:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i == 3:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    else:
                        for i in range(n):
                            guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                #############################   Cursor part code of inserting ###############################
                item_cursor=kern_x-300
                cursor_y=list(np.linspace(-900,1500,500))
                #cursor_y_neg=list(np.lenspace)
                cursor_x=list(np.full((500),item_cursor))
                SW_global.cursor_pos.append(item_cursor)
                cursor_x1=list(np.full((500),item_cursor))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
                plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                SW_global.single_click_data=plot_data[0]
                ##### Add new two variable for current axes and current pos #####
                SW_global.current_axes=guideline_axes[l]
                SW_global.current_pos=item_cursor
                SW_global.current_pos_in_number=len(delete_list)


                k=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                for i in k:
                    SW_global.cursor_data.append(i)
                    i.set_visible(False)
                for cur_count in range(len(SW_global.cursor_data)-1):
                    invisible_item=SW_global.cursor_data[cur_count]
                    invisible_item.set_visible(False)
                fig.canvas.draw()
        # -----------------------------------------------------------------------------------------------------
                final_enrty_pos = len(SW_global.letters_already_written)
                final_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
                features_checking_function()
                #return delete_list,kern_value_array
            else:
                print("I am in space add part ")
                length12 = len(SW_global.recent_input_list)
                print(" This is recent_input list",SW_global.recent_input_list)
                user_input = " "
                event_key = " "
                x_max= 0
                print("check point alpha")
                #print(kern_value_array)
                kern_x = SW_global.kern_list[0]
                c1,c2=[0],[0]
                kern_x = SW_global.kern_list[0] + 300
                SW_global.kern_list.insert(0, kern_x)
                kern_counter = len(kern_value_array)
                kern_value_array.insert(kern_counter, kern_x)
                SW_global.recent_input_list.insert(length12, event_key)
                delete_list.insert(len(delete_list), event_key)
                init_enrty_pos = len(SW_global.letters_already_written)
                print("check point 2")
                inti_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
                guideline_axes[l].plot(c1,c2)
                (guideline_axes[l].lines[len(guideline_axes[l].lines)-1]).set_visible(False)
                item_cursor=kern_x
                print("check point 1")
                cursor_y=list(np.linspace(-900,1500,500))
                cursor_x=list(np.full((500),item_cursor))
                SW_global.cursor_pos.append(item_cursor)
                cursor_x1=list(np.full((500),item_cursor))
                plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                SW_global.single_click_data=plot_data[0]
                SW_global.current_axes=guideline_axes[l]
                SW_global.current_pos=item_cursor
                SW_global.current_pos_in_number=len(delete_list)
                k=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                for i in k:
                    SW_global.cursor_data.append(i)
                    i.set_visible(False)

                for cur_count in range(len(SW_global.cursor_data)-1):
                    invisible_item=SW_global.cursor_data[cur_count]
                    #print("This is invisible_item")
                    #print(invisible_item)
                    invisible_item.set_visible(False)
                fig.canvas.draw()
                #print(guideline_axes[0].lines)
        # -----------------------------------------------------------------------------------------------------
                final_enrty_pos = len(SW_global.letters_already_written)
                final_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
                features_checking_function()
                #return delete_list,kern_value_array
    except Exception as e:
        print(e)
        pass

def main_add_controller(event_key=None):
    print("delete_list:",delete_list)
    print("kern_value_array",kern_value_array)
    print("SW_global.current_pos",SW_global.current_pos)
    print("SW_global.current_axes",SW_global.current_axes)
    if((event_key!=None) and(SW_global.current_axes!=None)):
        print("I am in main add controller")
        print("SW_global.current_axes",SW_global.current_axes)
        print("SW_global.current_pos",SW_global.current_pos)
        print("SW_global.cursor_pos",SW_global.cursor_pos)
        #### Here We have to add a block for SW_global.current_axes==guideline_axes[l] and SW_global.current_pos!=SW_global.cursor_pos[-1]
        if(SW_global.current_axes==guideline_axes[l]):
            if((SW_global.kern_list[0]>SW_global.max_limit) and((SW_global.current_pos==None) or(SW_global.current_pos>=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))):
                ### Take all the data of current line to the dictinary and create new line and reset data
                a=dict()
                a["letters_already_written"]=SW_global.letters_already_written.copy()
                a["delete_list"]=delete_list.copy()
                a["kern_value_array"]=kern_value_array.copy()
                a["gval"]=guideline_axes[l].lines.copy()
                a["lines"]=guideline_axes[l].lines.copy()
                a["kern_list"]=SW_global.kern_list.copy()
                a["cursor_pos"]=SW_global.cursor_pos.copy()
                a["cursor_data"]=SW_global.cursor_data.copy()
                a["recent_input_list"]=SW_global.recent_input_list.copy()
                a["compositedot_already_applied_array"]=compositedot_already_applied_array.copy()
                a["startdot_already_applied_array"]=startdot_already_applied_array.copy()
                a["decisiondot_already_applied_array"]=decisiondot_already_applied_array.copy()
                a["connectdot_already_applied_array"]=connectdot_already_applied_array.copy()
                a["axis_data"]=guideline_axes[l]
                a["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
                a["decision_dot_flag_pos"]=decision_dot_flag_pos
                a["connect_dot_flag_pos"]=connect_dot_flag_pos
                a["startdot_flag_pos"]=startdot_flag_pos
                SW_global.axes_data[str(len(SW_global.axes_data))]=a

                if(event_key==" "):
                    print("Normal add function need to used ")
                    newCreateGuideLine(1,None,None,None,None)
                    SW_global.recent_input_list.clear()
                    SW_global.kern_list.clear()
                    SW_global.kern_list.append(0)
                    kern_value_array.clear()
                    delete_list.clear()
                    kern_value_array.append(0)
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_pos.append(0)
                    SW_global.cursor_data.clear()
                    compositedot_already_applied_array.clear()
                    startdot_already_applied_array.clear()
                    connectdot_already_applied_array.clear()
                    decisiondot_already_applied_array.clear()
                    SW_global.current_axes=guideline_axes[l]
                    SW_global.letters_already_written.clear()
                    SW_global.current_pos=0
                    reset_features_flag()
                    add_any_letter_with_space_from_rear_side(event_key=event_key)
                else:
                    print("Need to use speacial operation for data handaling ")
                    print("delete_list :",delete_list)
                    if(" " in delete_list):
                        #print("Need to check ")
                        key_from_last_word_detection=last_word_detection(axesdata=guideline_axes[l])
                        #print(" key form detection ",key_from_last_word_detection)
                        SW_global.delete_list_divide.clear()
                        temp_delete_list1=[]
                        #print(temp_delete_list1)
                        for k5 in range(0,key_from_last_word_detection+1):
                            temp_delete_list1.append(delete_list[k5])
                        #    print(delete_list[k5])
                        k12=temp_delete_list1.copy()
                        SW_global.delete_list_divide.append(k12)
                        #print(temp_delete_list1)
                        #print(SW_global.delete_list_divide)
                        temp_delete_list1.clear()
                        for j in range(key_from_last_word_detection+1,len(delete_list)):
                            temp_delete_list1.append(delete_list[j])
                        temp_delete_list1.append(event_key)
                         #   print(delete_list[j])
                        k13=temp_delete_list1.copy()
                        SW_global.delete_list_divide.append(k13)
                        #print("This is SW_global.delete_list",SW_global.delete_list_divide)
                        temp_axes_list=[]
                        newCreateGuideLine(1,None,None,None,None)
                        temp_axes_list.append(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"])
                        temp_axes_list.append(guideline_axes[l])
                        clear_digit_from_axes(axesdata=temp_axes_list[0])
                        clear_digit_from_axes(axesdata=temp_axes_list[1])
                        temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=SW_global.delete_list_divide[0],spec_axes=temp_axes_list[0],baselines_objects_array=None)
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"]=temp_kern_value.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"]=temp_kern_list.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"]=temp_delete.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"]=temp_recent.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"]=temp_cursor_pos.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"]=temp_cursor_data.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"]=letters_already_written2.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"]=temp_guideline_axes2.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["gval"]=temp_guideline_axes2.copy()
                        SW_global.axes_data[str(len(SW_global.axes_data)-1)]["recent_input_list"]=temp_recent.copy()
                        temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=SW_global.delete_list_divide[1],spec_axes=temp_axes_list[1],baselines_objects_array=None)
                        kern_value_array.clear()
                        delete_list.clear()
                        SW_global.kern_list=temp_kern_list1.copy()
                        print("temp_delete1",temp_delete1)
                        print("temp_kern_value1",temp_kern_value1)
                        reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)
                        #delete_list=temp_delete1.copy()
                        SW_global.recent_input_list=temp_recent1.copy()
                        SW_global.cursor_pos=temp_cursor_pos1.copy()
                        SW_global.cursor_data=temp_cursor_data1.copy()
                        SW_global.letters_already_written=letters_already_written3.copy()
                        #guideline_axes[l].lines.clear()
                        while(len(guideline_axes[l].lines)>4):
                            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                        for j in temp_guideline_axes1:
                            guideline_axes[l].lines.append(j)
                        print("cursor_pos",SW_global.cursor_pos)
                        print("cursor_data",SW_global.cursor_data)
                        print("delete_list:",delete_list)
                        print("kern_value_array",kern_value_array)
                        SW_global.current_axes=guideline_axes[l]
                        if(len(SW_global.cursor_pos)>0):
                            SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
                        fig.canvas.draw()
                        features_checking_function()
                        ###kern_value_array2,kern_list2,delete_list2,recent_input_list2,cursor_data2,cursor_pos2,letters_already_written2
                    else:
                        print("Don't need to check just use normal operation ")
                        newCreateGuideLine(1,None,None,None,None)
                        SW_global.recent_input_list.clear()
                        SW_global.kern_list.clear()
                        SW_global.kern_list.append(0)
                        SW_global.letters_already_written.clear()
                        kern_value_array.clear()
                        delete_list.clear()
                        kern_value_array.append(0)
                        SW_global.cursor_pos.clear()
                        SW_global.cursor_pos.append(0)
                        SW_global.cursor_data.clear()
                        compositedot_already_applied_array.clear()
                        startdot_already_applied_array.clear()
                        connectdot_already_applied_array.clear()
                        decisiondot_already_applied_array.clear()
                        SW_global.current_axes=guideline_axes[l]
                        SW_global.current_pos=0
                        reset_features_flag()
                        add_any_letter_with_space_from_rear_side(event_key=event_key)
            elif((SW_global.current_pos!=None) and(SW_global.current_pos<SW_global.cursor_pos[len(SW_global.cursor_pos)-1])):
                print("checjk")
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                temp=[]
                for j in range(len(delete_list)):
                    if(SW_global.current_pos_in_number!=None and j==SW_global.current_pos_in_number):
                        temp.append(event_key)
                    temp.append(delete_list[j])
                print("This is temp ",temp)
                count1=0
                count2=-1
                temp22=[]
                temp33=[]
                temp10=[]
                calc2=[]
                sum1=0
                # delete_list.clear()
                # for j in temp:
                #     delete_list.append(j)

                # if(" " in temp):
                #     key_from_last_word_detection=last_word_detection(axesdata=guideline_axes[l])


                for j in range(len(temp)):
                    print("I am in loop")
                    if(temp[j]==" "):
                        print("check 1")
                        print(j)
                        sum1=sum1+300
                    else:
                        print("check2")
                        print(j)
                        sum1=sum1+manuscript.x_max[temp[j]]+300
                print("This is sum1 ",sum1)
                if(sum1<=SW_global.max_limit):
                    print("check point333")
                    temp22.clear()
                    for j in temp:
                        temp22.append(j)
                    temp10.append(temp22) 
                else:
                    print("check point 444")
                    # count1=-1
                    # for j in range(len(temp)):
                    #     if(temp[j]==" "):
                    #         count1=temp[j]
                    # count2=0
                    # for j in range(count2,)
                    if( " " in temp):
                        print()
                        count1=-1
                        for j in range(len(temp)):
                            if(temp[j]==" "):
                                count1=j
                        for j in range(0,count1+1):
                            temp22.append(temp[j])
                        temp10.append(temp22.copy())
                        temp22.clear()
                        for j in range(count1+1,len(temp)):
                            temp22.append(temp[j])
                        temp10.append(temp22.copy())

                    else:
                        count1=-1
                        sum1=0
                        for j in range(len(temp)):
                            sum1=sum1+manuscript.x_max[temp[j]]+300
                            if(sum1>SW_global.max_limit):
                                count1=j
                                for k10 in range(0,count1):
                                    temp22.append(temp[k10])
                                temp10.append(temp22.copy())
                                break
                        temp22.clear()
                        for j in range(count1,len(temp)):
                            temp22.append(temp[j])
                        temp10.append(temp22.copy())
                print("This is temp10",temp10)
                if(len(temp10)>1):
                    print("j")
                    clear_digit_from_axes(axesdata=guideline_axes[l])
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[0],spec_axes=guideline_axes[l],baselines_objects_array=None)
                    save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_data1.copy(),cursor_data1=temp_cursor_data1,kern_list1=temp_kern_list1.copy(),axes_key_index=None,letters_already_written1=letters_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=guideline_axes[l])
                    newCreateGuideLine(1,None,None,None,None)
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[1],spec_axes=guideline_axes[l],baselines_objects_array=None)
                    kern_value_array.clear()
                    delete_list.clear()
                    SW_global.kern_list=temp_kern_list1.copy()
                    print("temp_delete1",temp_delete1)
                    print("temp_kern_value1",temp_kern_value1)
                    reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)                    
                    SW_global.recent_input_list=temp_recent1.copy()
                    SW_global.cursor_pos=temp_cursor_pos1.copy()
                    SW_global.cursor_data=temp_cursor_data1.copy()
                    SW_global.letters_already_written=letters_already_written3.copy()
                    #guideline_axes[l].lines.clear()
                    while(len(guideline_axes[l].lines)>4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    for j in temp_guideline_axes1:
                        guideline_axes[l].lines.append(j)
                    print("cursor_pos",SW_global.cursor_pos)
                    print("cursor_data",SW_global.cursor_data)
                    print("delete_list:",delete_list)
                    print("kern_value_array",kern_value_array)
                    print("This is letter already written",SW_global.letters_already_written)
                    SW_global.current_axes=guideline_axes[l]
                    if(len(SW_global.cursor_pos)>0):
                        SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
                    fig.canvas.draw()
                    features_checking_function()
                    ## Testing print
                    print("This is SW_global.recent_input_list",SW_global.recent_input_list)





                elif(len(temp10)==1):
                    print("j1")
                    clear_digit_from_axes(axesdata=guideline_axes[l])
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[0],spec_axes=guideline_axes[l],baselines_objects_array=None)
                    kern_value_array.clear()
                    delete_list.clear()
                    SW_global.kern_list=temp_kern_list1.copy()
                    print("temp_delete1",temp_delete1)
                    print("temp_kern_value1",temp_kern_value1)
                    reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)                    
                    SW_global.recent_input_list=temp_recent1.copy()
                    SW_global.cursor_pos=temp_cursor_pos1.copy()
                    SW_global.cursor_data=temp_cursor_data1.copy()
                    SW_global.letters_already_written=letters_already_written3.copy()
                    #guideline_axes[l].lines.clear()
                    while(len(guideline_axes[l].lines)>4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    for j in temp_guideline_axes1:
                        guideline_axes[l].lines.append(j)
                    print("cursor_pos",SW_global.cursor_pos)
                    print("cursor_data",SW_global.cursor_data)
                    print("delete_list:",delete_list)
                    print("kern_value_array",kern_value_array)
                    print("This is letter already written",SW_global.letters_already_written)
                    SW_global.current_axes=guideline_axes[l]
                    if(len(SW_global.cursor_pos)>0):
                        SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
                    fig.canvas.draw()
                    features_checking_function()
                    ## Testing print
                    print("This is SW_global.recent_input_list",SW_global.recent_input_list)

                fig.canvas.draw()
                        

                #    temp10=divide_delete_list_with_the_base_of_max_limit(need_array=temp)
                #print("This is temp 10",temp10)

                # if(" " in temp):
                #     for j in range(len(temp)):
                #         count2=j
                #         temp22.clear()
                #         if(temp[j]==" "):
                #             for k10 in range(count1,count2+1):
                #                 temp22.append(temp[k10])
                #                 sum1=sum1+manuscript.x_max(temp[k10])
                #             temp33.append(temp22.copy())
                #             sum1=0
                #             temp22.clear()
                #             count1=count2+1
                #         elif(j==len(temp)-1):
                #             temp22.clear()
                #             for k10 in range(count1,count2+1):
                #                 temp22.append(temp[k10])
                #                 sum1=sum1+manuscript.x_max(temp[k10])
                # else:
                #     temp22.clear()
                #     for j in temp:
                #         sum1=sum1+manuscript.x_max(temp[k10])
                #         temp22.append(j)


                # print("This is temp33",temp33)


                # temp10=divide_delete_list_with_the_base_of_max_limit(need_array=temp)
                #print("This is from middle in any ",temp10)
            else:
                print("I am in else part of main add controller")
                add_any_letter_with_space_from_rear_side(event_key=event_key)
        else:
            print("This is current_pos",SW_global.current_pos)
            print("This is current_axes",SW_global.current_axes)
            print("This is len(SW_global.axes_data)",len(SW_global.axes_data))
            ##### for not mouse cursor in guideline #####
            print("This is SW_global.current_pos_in_number",SW_global.current_pos_in_number)
            if(SW_global.current_axes!=None and guideline_axes[l]==SW_global.current_axes):
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                temp=[]
                # for j in delete_list:
                #     if(SW_global.current_pos_in_number!=None):
                #         temp.append(event_key)
                #     temp.append(j)
                for j in range(len(delete_list)):
                    if(SW_global.current_pos_in_number!=None and j==SW_global.current_pos_in_number):
                        temp.append(event_key)
                    temp.append(delete_list[j])
                print("This is temp ",temp)
                temp10=divide_delete_list_with_the_base_of_max_limit(need_array=temp)
                print("This is temp10",temp10)
                # if(event_key==" "):
                #     print("Hi")
                #     print("SW_global.current_pos_in_number",SW_global.current_pos_in_number)
                #     temp_delete_list=
                # elif(event_key!=" "):
                #     print("Hi2")
            else:
                print("chech ")
                key_axes=None
                if((SW_global.current_axes!=None) and(guideline_axes[l]!=SW_global.current_axes)):
                    for j in range(len(SW_global.axes_data)):
                        print("I am in loop0")
                        print(SW_global.axes_data[str(j)]["axis_data"])
                        if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.current_axes):
                            print("yes1")
                            key_axes=j
                            break
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                print("delete_list for guide line",delete_list)
                for k1 in range(len(SW_global.axes_data)):
                    print("delete_list_for",k1)
                    print(SW_global.axes_data[str(k1)]["delete_list"])

                divide_delete_list_for_add_operation(key_axes=key_axes,event_key=event_key)
                fig.canvas.draw()
            ####### #### change SW_global.current_pos ######
            ############ change SW_global.current_axes #######
            #if(SW_global.current_axes==guideline_axes[l]):
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                if(SW_global.current_axes==guideline_axes[l]):
                    if(SW_global.current_pos_in_number<len(SW_global.cursor_data)-1):
                        SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number+1]
                else:
                    for j in range(len(SW_global.axes_data)):
                        if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.current_axes):
                            if(SW_global.current_pos_in_number<len(SW_global.cursor_data)-1):
                                SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number+1]
                            elif(j+1<=len(SW_global.axes_data)-1):
                                SW_global.current_pos=SW_global.axes_data[str(j+1)]["cursor_pos"][1]
                                SW_global.current_axes=SW_global.axes_data[str(j+1)]["axis_data"]
                            elif(j+1>len(SW_global.axes_data)-1):
                                SW_global.current_pos=SW_global.cursor_pos[0]
                                SW_global.current_axes=guideline_axes[l]
    return 


def divide_delete_list_for_add_operation(key_axes=None,axes_list1=None,event_key=None):
    print("I am in divide delete_list for add operation ")
    if(SW_global.current_axes==guideline_axes[l]):
        print("Hi")
    else:
        count_axes=key_axes
        print("key axes",count_axes)
        if(event_key!=None and key_axes!=None and SW_global.current_pos_in_number!=None):
            print("check point122")
            if(SW_global.current_axes==guideline_axes[l]):
                print("check 112")
            else:
                print("check point11")
                SW_global.delete_list_divide.clear()
                delete_list_temp=[]
                kern_list_temp=[]
                for j in  range(len(SW_global.axes_data)):
                    temp=[]
                    if(j==count_axes):
                        for k1 in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                            if(k1==SW_global.current_pos_in_number):
                                delete_list_temp.append(event_key)
                                delete_list_temp.append(SW_global.axes_data[str(j)]["delete_list"][k1])
                                
                            else:
                                delete_list_temp.append(SW_global.axes_data[str(j)]["delete_list"][k1])
                        #delete_list_temp.append(temp)
                    if(j>count_axes):
                        for k4 in SW_global.axes_data[str(j)]["delete_list"]:
                            delete_list_temp.append(k4)
                print("delete_list_temp",delete_list_temp)
                print("delete_list",delete_list)
                for k1 in delete_list:
                    delete_list_temp.append(k1)
                print("delete_list_temp",delete_list_temp)
                ### divide delete_list_temp with the base of space ###

                if(" " in delete_list_temp):
                    count1=0
                    count2=0
                    k1=[]
                    for j in range(len(delete_list_temp)):
                        if(delete_list_temp[j]==" "):
                            for k2 in range(count1,j+1):
                                count2=count2+1
                                k1.append(delete_list_temp[k2])
                            trt=k1.copy()
                            print("This is trt",trt)
                            SW_global.delete_list_divide.append(trt)
                            k1.clear()
                            count1=j+1
                    if(count2<len(delete_list_temp)):
                        for k2 in range(count2,len(delete_list_temp)):
                            print("check 2")
                            k1.append(delete_list_temp[k2])
                        SW_global.delete_list_divide.append(k1)
                else:
                    print("I am in else part ")
                    SW_global.delete_list_divide.append(delete_list_temp)

                ##### Call add_digit_axes #####
                ##### before add we need to check wheather call an entire subarray will cross the max limit or not #####


                print("SW_global.delete_list_divide",SW_global.delete_list_divide)
                print("End of value")
                #SW_global.delete_list_divide.clear()
                SW_global.delete_list_divide=divide_delete_list_with_the_base_of_max_limit(need_array=SW_global.delete_list_divide)
                print(SW_global.delete_list_divide)
                check_sum_of_digit_advanced(array_value=SW_global.delete_list_divide.copy(),key_axes=key_axes)
                #check_sum_of_digit(array_value=SW_global.delete_list_divide,key_axes=key_axes)
                SW_global.delete_list_divide.clear()

    return 

def main_add_controller_for_text_flow(event_key=None):
    SW_global.delete_list_divide.clear()
    if((SW_global.current_axes!=None) and(SW_global.current_pos!=None)):
        if(SW_global.current_axes==guideline_axes[l]):
            current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
            for j in range(len(delete_list)):
                if(j==SW_global.current_pos_in_number):
                    SW_global.delete_list_divide.append(event_key)
                SW_global.delete_list_divide.append(delete_list[j])
        else:
            key_axes=None
            for j in range(len(SW_global.axes_data)):
                if(SW_global.axes_data[str(j)]["axis_list"]==SW_global.current_axes):
                    key_axes=j
                    break
            if(key_axes!=None):
                SW_global.delete_list_divide.clear()
                for j in range(len(SW_global.axes_data)):
                    if(j>key_axes):
                        SW_global.delete_list_divide.extend(SW_global.axes_data[str(j)]["delete_list"])
                    if(j==key_axes):
                        current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes1)
                        for k in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                            if(k==SW_global.current_pos_in_number):
                                SW_global.delete_list_divide.append(event_key)
                            SW_global.delete_list_divide.append(SW_global.axes_data[str(j)]["delete_list"][k])

                next_axes_list=[]
                h=None
                for j in range(len(SW_global.text_flow_axes)):
                    if(SW_global.current_axes==SW_global.text_flow_axes[j]):
                        h=j
                    if((h!=None) and(j>h)):
                        next_axes_list.append(SW_global.text_flow_axes[j])
                for j in next_axes_list:
                    for k in range(len(SW_global.box_data)):
                        if(j in SW_global.box_data[str(k)]["axis_list"]):
                            aw=SW_global.box_data[str(k)]["axes_data"]
                            for k1 in range(len(aw)):
                                SW_global.delete_list_divide.extend(aw[str(k1)]["delete_list"])
                            SW_global.delete_list_divide.extend(SW_global.box_data[str(k)]["delete_list"])

                print("SW_global.delete_list_divide",SW_global.delete_list_divide)
                temp10=divide_delete_list_with_the_base_of_max_limit(need_array=SW_global.delete_list_divide)
                ##### need to print those data #####
                for j in temp10:
                    print(j)

    return 



def part_onrelease():
    return 
def check_axes_need_to_checked(axes=None,extra_array=None):

    return 

# def main_add_controller_for_text_flow_features3(event_key=None):
#     kw=[]
#     if((event_key!=None) and(SW_global.current_axes!=None)):
#         print("I am in main add controller")
#         print("SW_global.current_axes",SW_global.current_axes)
#         print("SW_global.current_pos",SW_global.current_pos)
#         print("SW_global.cursor_pos",SW_global.cursor_pos)
#         #### Here We have to add a block for SW_global.current_axes==guideline_axes[l] and SW_global.current_pos!=SW_global.cursor_pos[-1]
#         if(SW_global.current_axes==guideline_axes[l]):
#             if((SW_global.kern_list[0]>SW_global.max_limit) and((SW_global.current_pos==None) or(SW_global.current_pos>=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))):
#                 ### Take all the data of current line to the dictinary and create new line and reset data
#                 if(event_key==" "):
#                     print("Normal add function need to used ")
#                     ### here need to add the function for change #####
#                     kw.clear()
                    
#                     kw.append(event_key)
#                     if(len(SW_global.axes_data)>0):

#                         text_flow_main(list1=kw,zero_axes=SW_global.axes_data[str(0)]["axis_data"])
#                     else:
#                         text_flow_main(list1=kw,zero_axes=guideline_axes[l])
#                     #add_any_letter_with_space_from_rear_side(event_key=event_key)
#                 else:
#                     print("Need to use speacial operation for data handaling ")
#                     print("delete_list :",delete_list)
#                     if(" " in delete_list):
#                         #print("Need to check ")
#                         key_from_last_word_detection=last_word_detection(axesdata=guideline_axes[l])
#                         #print(" key form detection ",key_from_last_word_detection)
#                         SW_global.delete_list_divide.clear()
#                         temp_delete_list1=[]
#                         #print(temp_delete_list1)
#                         for k5 in range(0,key_from_last_word_detection+1):
#                             temp_delete_list1.append(delete_list[k5])
#                         #    print(delete_list[k5])
#                         k12=temp_delete_list1.copy()
#                         SW_global.delete_list_divide.append(k12)
#                         #print(temp_delete_list1)
#                         #print(SW_global.delete_list_divide)
#                         temp_delete_list1.clear()
#                         for j in range(key_from_last_word_detection+1,len(delete_list)):
#                             temp_delete_list1.append(delete_list[j])
#                         temp_delete_list1.append(event_key)
#                          #   print(delete_list[j])
#                         k13=temp_delete_list1.copy()
#                         SW_global.delete_list_divide.append(k13)
#                         #print("This is SW_global.delete_list",SW_global.delete_list_divide)
#                         temp_axes_list=[]
#                         #### Here need to add part ####
#                        # newCreateGuideLine(1,None,None,None,None)
#                        # temp_axes_list.append(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"])
#                         temp_axes_list.append(guideline_axes[l])
#                         clear_digit_from_axes(axesdata=temp_axes_list[0])
#                        # clear_digit_from_axes(axesdata=temp_axes_list[1])
#                         temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=SW_global.delete_list_divide[0],spec_axes=temp_axes_list[0],baselines_objects_array=None)
#                         kern_value_array.clear()
#                         delete_list.clear()
#                         SW_global.kern_list=temp_kern_list1.copy()
#                         print("temp_delete1",temp_delete1)
#                         print("temp_kern_value1",temp_kern_value1)
#                         reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)
#                         #delete_list=temp_delete1.copy()
#                         SW_global.recent_input_list=temp_recent1.copy()
#                         SW_global.cursor_pos=temp_cursor_pos1.copy()
#                         SW_global.cursor_data=temp_cursor_data1.copy()
#                         SW_global.letters_already_written=letters_already_written3.copy()
#                         #guideline_axes[l].lines.clear()
#                         while(len(guideline_axes[l].lines)>4):
#                             del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
#                         for j in temp_guideline_axes1:
#                             guideline_axes[l].lines.append(j)
#                         print("cursor_pos",SW_global.cursor_pos)
#                         print("cursor_data",SW_global.cursor_data)
#                         print("delete_list:",delete_list)
#                         print("kern_value_array",kern_value_array)
#                         print("SW_global.delete_list_divide",SW_global.delete_list_divide)
#                         SW_global.current_axes=guideline_axes[l]
#                         if(len(SW_global.cursor_pos)>0):
#                             SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
#                         fig.canvas.draw()
#                         if(len(SW_global.axes_data)>0):
#                             text_flow_main(list1=SW_global.delete_list_divide[1],zero_axes=SW_global.axes_data[str(0)]["axis_data"])
#                         else:
#                             text_flow_main(list1=SW_global.delete_list_divide[1],zero_axes=guideline_axes[l])
#                         features_checking_function()
#                         ###kern_value_array2,kern_list2,delete_list2,recent_input_list2,cursor_data2,cursor_pos2,letters_already_written2
#                     else:
#                         print("Don't need to check just use normal operation ")
#                         #### here need to add function ####
#                         # newCreateGuideLine(1,None,None,None,None)
#                         # SW_global.recent_input_list.clear()
#                         # SW_global.kern_list.clear()
#                         # SW_global.kern_list.append(0)
#                         # SW_global.letters_already_written.clear()
#                         # kern_value_array.clear()
#                         # delete_list.clear()
#                         # kern_value_array.append(0)
#                         # SW_global.cursor_pos.clear()
#                         # SW_global.cursor_data.clear()
#                         # compositedot_already_applied_array.clear()
#                         # startdot_already_applied_array.clear()
#                         # connectdot_already_applied_array.clear()
#                         # decisiondot_already_applied_array.clear()
#                         # SW_global.current_axes=guideline_axes[l]
#                         # SW_global.current_pos=0
#                         # reset_features_flag()
#                         # add_any_letter_with_space_from_rear_side(event_key=event_key)
#                         kw.clear()
#                         kw.append(event_key)
#                         if(len(SW_global.axes_data)>0):
#                             text_flow_main(list1=kw,zero_axes=SW_global.axes_data[str(0)]["axis_data"])
#                         else:
#                             text_flow_main(list1=kw,zero_axes=guideline_axes[l])
#                         features_checking_function()

#     return

def main_back_space_controller_for_text_flow_features2():
    zero_axes=None
    temp_delete_list=[]
    if(len(SW_global.axes_data)>0):
        zero_axes=SW_global.axes_data[str(0)]["axis_data"]
    else:
        zero_axes=guideline_axes[l]

    next_axes,key=find_next_axes1(zero_axes=zero_axes)
    if(len(next_axes)==0):
        main_back_space_controller()
    else:
        #### This is main part of backspace of text flow ####
        if(SW_global.current_axes==guideline_axes[l]):
            current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
            key=len(SW_global.axes_data)
            if(SW_global.current_pos_in_number!=None):
                for j in range(len(delete_list)):
                    if(j!=SW_global.current_pos_in_number):
                        temp_delete_list.append(delete_list[j])
            for j in range(len(next_axes)):
                temp_key=checking_for_which_box_need_to_switch(axesdata=next_axes[j])
                if(temp_key!=None):
                    axes_data1=SW_global.box_data[str(temp_key)]["SW_global_axes_data"]
                    for k1 in range(len(axes_data1)):
                        temp_delete_list.extend(axes_data1[str(k1)]["delete_list"])
                    temp_delete_list.extend(SW_global.box_data[str(temp_key)]["delete_list"])
            
            #temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
        else:
            if(SW_global.current_pos_in_number!=None):
                for j in range(len(SW_global.axes_data)):
                    if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.current_axes):
                        key=j
                        for k1 in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                            if(k1!=SW_global.current_pos_in_number):
                                temp_delete_list.append((SW_global.axes_data[str(j)]["delete_list"])[k1])
                    else:
                        temp_delete_list.extend(SW_global.axes_data[str(j)]["delete_list"])
                
            for j in range(len(next_axes)):
                temp_key=checking_for_which_box_need_to_switch(axesdata=next_axes[j])
                if(temp_key!=None):
                    axes_data1=SW_global.box_data[str(temp_key)]["SW_global_axes_data"]
                    for k1 in range(len(axes_data1)):
                        temp_delete_list.extend(axes_data1[str(k1)]["delete_list"])
                    temp_delete_list.extend(SW_global.box_data[str(temp_key)]["delete_list"])
        temp=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)                    
        ##### This is erase part #####
        if(key==len(SW_global.axes_data)):
            clear_digit_from_axes(axesdata=guideline_axes[l])
        elif(key<len(SW_global.axes_data)):
            for j in range(key,len(SW_global.axes_data)):
                clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
            clear_digit_from_axes(axesdata=guideline_axes[l])
        #for j in range(len(SW_global))
        #### we have to set varibles for current box we will do it later  ####
        axes_list_for_box=[]
        for j in range(len(SW_global.axes_data)):
            axes_list_for_box.append(SW_global.axes_data[str(j)]["axis_data"])
        axes_list_for_box.append(guideline_axes[l])
        if(len(SW_global.box_data)>0):
            data_checking_for_need_to_create_or_update_back_page(axes_list=axes_list_for_box,delete_list1=delete_list,kern_value_array1=kern_value_array)
        else:
            create_new_page_on_box_data(delete_list1=delete_list,kern_value_array1=kern_value_array)

        #for j in range(next_axes):
        for j in range(len(SW_global.axes_data)):
            clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
        clear_digit_from_axes(axesdata=guideline_axes[l])
        for j in range(len(next_axes)):
            temp_key=checking_for_which_box_need_to_switch(axesdata=next_axes[j])
            if(temp_key!=None):
                lines=SW_global.box_data[str(temp_key)]["guideline_axes_lines"]
                for k in range(4,len(lines)):
                    lines[k].set_visible(False)
                axes1=SW_global.box_data[str(temp_count)]["SW_global_axes_data"]
                for k in range(len(axes1)):
                    for k1 in range(4,len(axes1["lines"])):
                        (axes1["lines"][k1]).set_visible(False)
                #### we need to set all the variables of data that's we will do it later 
        fig.canvas.draw()
        #### This is part is for data printing to the axes####
        len1=len(SW_global.axes_data)
        temp_count=key
        if((key!=None) and(temp!=None)):
            for j in range(len(temp)):
                if(temp_count<len1):
                    print("This is need to complete")
                    base_array=[]
                    for k1 in range(4):
                        base_array.append((SW_global.axes_data[str(temp_count)]["lines"])[k1])
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                    save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=temp_count,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(temp_count)]["axis_data"],lines1=temp_guideline_axes2,kern_list1=temp_kern_list)
                elif(temp_count==len1):
                    base_array=[]
                    for k1 in range(4):
                        base_array.append(guideline_axes[l].lines[k1])
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp[j],spec_axes=SW_global.axes_data[str(temp_count)]["axis_data"],baselines_objects_array=base_array)
                    set_guideLine_variables(kern_value_array1=temp_kern_value,delete_list1=temp_delete,kern_list1=temp_kern_list,recent1=temp_recent,lines1=temp_guideline_axes2,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,letters_already_written=letters_already_written2)
                    axes_list_for_box=[]
                    for j in range(len(SW_global.axes_data)):
                        axes_list_for_box.append(SW_global.axes_data[str(j)]["axis_data"])
                    axes_list_for_box.append(guideline_axes[l])
                    if(len(SW_global.box_data)>0):
                        data_checking_for_need_to_create_or_update_back_page(axes_list=axes_list_for_box,delete_list1=delete_list,kern_value_array1=kern_value_array)
                    else:
                        create_new_page_on_box_data(delete_list1=delete_list,kern_value_array1=kern_value_array)
                    print("This is end1")
                    temp_key=checking_for_which_box_need_to_switch(axesdata=next_axes[j])
                    temp=data_Switching2(key=temp_key)
                    if(temp!=None):
                        delete_list.clear()
                        kern_value_array.clear()
                        #print("temp len:",len(temp_data))
                    if(len(temp)==7):
                        for j in temp[1]:
                        #print("I am in kern_ temp_1")
                            kern_value_array.append(j)
                        for j in temp[0]:
                        #print("I am in kern_temp_1")
                            delete_list.append(j)
                    #### There is a chance of getting of reference error ####
                    len1=len(SW_global.axes_data)
                    temp_count=0
                temp_count=temp_count+1
    return





def main_add_controller_for_text_flow_features2(event_key=None):
    print("I am in main add controller")
    kw=[]
    if((event_key!=None) and(SW_global.current_axes!=None)):
        print("I am in main add controller")
        print("SW_global.current_axes",SW_global.current_axes)
        print("SW_global.current_pos",SW_global.current_pos)
        print("SW_global.cursor_pos",SW_global.cursor_pos)
        #### Here We have to add a block for SW_global.current_axes==guideline_axes[l] and SW_global.current_pos!=SW_global.cursor_pos[-1]
        if(SW_global.current_axes==guideline_axes[l]):
            if((SW_global.kern_list[0]>SW_global.max_limit) and((SW_global.current_pos==None) or(SW_global.current_pos>=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))):
                ### Take all the data of current line to the dictinary and create new line and reset data
                if(event_key==" "):
                    print("Normal add function need to used ")
                    ### here need to add the function for change #####
                    kw.clear()
                    
                    kw.append(event_key)
                    if(len(SW_global.axes_data)>0):
                        print("check point x")

                        text_flow_main1(list1=kw,zero_axes=SW_global.axes_data[str(0)]["axis_data"],current_axes=SW_global.current_axes)
                    else:
                        print("check point y")
                        text_flow_main1(list1=kw,zero_axes=guideline_axes[l],current_axes=SW_global.current_axes)
                    #add_any_letter_with_space_from_rear_side(event_key=event_key)
                else:
                    print("Need to use speacial operation for data handaling ")
                    print("delete_list :",delete_list)
                    if(" " in delete_list):
                        #print("Need to check ")
                        key_from_last_word_detection=last_word_detection(axesdata=guideline_axes[l])
                        #print(" key form detection ",key_from_last_word_detection)
                        SW_global.delete_list_divide.clear()
                        temp_delete_list1=[]
                        #print(temp_delete_list1)
                        for k5 in range(0,key_from_last_word_detection+1):
                            temp_delete_list1.append(delete_list[k5])
                        #    print(delete_list[k5])
                        k12=temp_delete_list1.copy()
                        SW_global.delete_list_divide.append(k12)
                        #print(temp_delete_list1)
                        #print(SW_global.delete_list_divide)
                        temp_delete_list1.clear()
                        for j in range(key_from_last_word_detection+1,len(delete_list)):
                            temp_delete_list1.append(delete_list[j])
                        temp_delete_list1.append(event_key)
                         #   print(delete_list[j])
                        k13=temp_delete_list1.copy()
                        SW_global.delete_list_divide.append(k13)
                        #print("This is SW_global.delete_list",SW_global.delete_list_divide)
                        temp_axes_list=[]
                        #### Here need to add part ####
                       # newCreateGuideLine(1,None,None,None,None)
                       # temp_axes_list.append(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"])
                        temp_axes_list.append(guideline_axes[l])
                        clear_digit_from_axes(axesdata=temp_axes_list[0])
                       # clear_digit_from_axes(axesdata=temp_axes_list[1])
                        temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=SW_global.delete_list_divide[0],spec_axes=temp_axes_list[0],baselines_objects_array=None)
                        kern_value_array.clear()
                        delete_list.clear()
                        SW_global.kern_list=temp_kern_list1.copy()
                        print("temp_delete1",temp_delete1)
                        print("temp_kern_value1",temp_kern_value1)
                        reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)
                        #delete_list=temp_delete1.copy()
                        SW_global.recent_input_list=temp_recent1.copy()
                        SW_global.cursor_pos=temp_cursor_pos1.copy()
                        SW_global.cursor_data=temp_cursor_data1.copy()
                        SW_global.letters_already_written=letters_already_written3.copy()
                        #guideline_axes[l].lines.clear()
                        while(len(guideline_axes[l].lines)>4):
                            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                        for j in temp_guideline_axes1:
                            guideline_axes[l].lines.append(j)
                        print("cursor_pos",SW_global.cursor_pos)
                        print("cursor_data",SW_global.cursor_data)
                        print("delete_list:",delete_list)
                        print("kern_value_array",kern_value_array)
                        print("SW_global.delete_list_divide",SW_global.delete_list_divide)
                        SW_global.current_axes=guideline_axes[l]
                        if(len(SW_global.cursor_pos)>0):
                            SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
                        fig.canvas.draw()
                        if(len(SW_global.axes_data)>0):
                            text_flow_main1(list1=SW_global.delete_list_divide[1],zero_axes=SW_global.axes_data[str(0)]["axis_data"],current_axes=SW_global.current_axes)
                        else:
                            text_flow_main1(list1=SW_global.delete_list_divide[1],zero_axes=guideline_axes[l],current_axes=SW_global.current_axes)
                        features_checking_function()
                        ###kern_value_array2,kern_list2,delete_list2,recent_input_list2,cursor_data2,cursor_pos2,letters_already_written2
                    else:
                        print("Don't need to check just use normal operation ")
                        zero_axes=None
                        if(len(SW_global.axes_data)>0):
                            zero_axes=SW_global.axes_data[str(0)]["axis_data"]
                        else:
                            zero_axes=guideline_axes[l]
                        next_axes,key=find_next_axes1(zero_axes=zero_axes)
                        if(len(next_axes)>0):
                            print()
                            ### This part will be embeded ###
                        elif(len(next_axes)==0):
                            newCreateGuideLine(1,None,None,None,None)
                            SW_global.recent_input_list.clear()
                            SW_global.kern_list.clear()
                            SW_global.kern_list.append(0)
                            SW_global.letters_already_written.clear()
                            kern_value_array.clear()
                            delete_list.clear()
                            kern_value_array.append(0)
                            SW_global.cursor_pos.clear()
                            SW_global.cursor_data.clear()
                            compositedot_already_applied_array.clear()
                            startdot_already_applied_array.clear()
                            connectdot_already_applied_array.clear()
                            decisiondot_already_applied_array.clear()
                            SW_global.current_axes=guideline_axes[l]
                            SW_global.current_pos=0
                            reset_features_flag()
                            add_any_letter_with_space_from_rear_side(event_key=event_key)



                        #newCreateGuideLine(1.None,None,None,None)
                        #### here need to add function ####
                        # newCreateGuideLine(1,None,None,None,None)
                        # SW_global.recent_input_list.clear()
                        # SW_global.kern_list.clear()
                        # SW_global.kern_list.append(0)
                        # SW_global.letters_already_written.clear()
                        # kern_value_array.clear()
                        # delete_list.clear()
                        # kern_value_array.append(0)
                        # SW_global.cursor_pos.clear()
                        # SW_global.cursor_data.clear()
                        # compositedot_already_applied_array.clear()
                        # startdot_already_applied_array.clear()
                        # connectdot_already_applied_array.clear()
                        # decisiondot_already_applied_array.clear()
                        # SW_global.current_axes=guideline_axes[l]
                        # SW_global.current_pos=0
                        # reset_features_flag()
                        # add_any_letter_with_space_from_rear_side(event_key=event_key)
                        kw.clear()
                        kw.append(event_key)
                        SW_global.embed_array.append(event_key)
                        print("This is embed array",SW_global.embed_array)
                        # if(len(SW_global.axes_data)>0):
                        #     text_flow_main(list1=kw,zero_axes=SW_global.axes_data[str(0)]["axis_data"])
                        # else:
                        #     text_flow_main(list1=kw,zero_axes=guideline_axes[l])
                        #features_checking_function()

            elif((SW_global.current_pos!=None) and(SW_global.current_pos<SW_global.cursor_pos[len(SW_global.cursor_pos)-1])):
                print("checjk")
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                temp=[]
                for j in range(len(delete_list)):
                    if(SW_global.current_pos_in_number!=None and j==SW_global.current_pos_in_number):
                        temp.append(event_key)
                    temp.append(delete_list[j])
                print("This is temp ",temp)
                count1=0
                count2=-1
                temp22=[]
                temp33=[]
                temp10=[]
                calc2=[]
                sum1=0

                for j in range(len(temp)):
                    print("I am in loop")
                    if(temp[j]==" "):
                        print("check 1")
                        print(j)
                        sum1=sum1+300
                    else:
                        print("check2")
                        print(j)
                        sum1=sum1+manuscript.x_max[temp[j]]+300
                print("This is sum1 ",sum1)
                if(sum1<=SW_global.max_limit):
                    print("check point333")
                    temp22.clear()
                    for j in temp:
                        temp22.append(j)
                    temp10.append(temp22) 
                else:
                    print("check point 444")
                    if( " " in temp):
                        print()
                        count1=-1
                        for j in range(len(temp)):
                            if(temp[j]==" "):
                                count1=j
                        for j in range(0,count1+1):
                            temp22.append(temp[j])
                        temp10.append(temp22.copy())
                        temp22.clear()
                        for j in range(count1+1,len(temp)):
                            temp22.append(temp[j])
                        temp10.append(temp22.copy())

                    else:
                        count1=-1
                        sum1=0
                        for j in range(len(temp)):
                            sum1=sum1+manuscript.x_max[temp[j]]+300
                            if(sum1>SW_global.max_limit):
                                count1=j
                                for k10 in range(0,count1):
                                    temp22.append(temp[k10])
                                temp10.append(temp22.copy())
                                break
                        temp22.clear()
                        for j in range(count1,len(temp)):
                            temp22.append(temp[j])
                        temp10.append(temp22.copy())
                print("This is temp10",temp10)
                if(len(temp10)>1):
                    print("j")
                    clear_digit_from_axes(axesdata=guideline_axes[l])
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[0],spec_axes=guideline_axes[l],baselines_objects_array=None)
                    # save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_data1.copy(),cursor_data1=temp_cursor_data1,kern_list1=temp_kern_list1.copy(),axes_key_index=None,letters_already_written1=letters_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=guideline_axes[l])
                    # ##### need to add function and others checking
                    # newCreateGuideLine(1,None,None,None,None)
                    # temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[1],spec_axes=guideline_axes[l],baselines_objects_array=None)
                    kern_value_array.clear()
                    delete_list.clear()
                    SW_global.kern_list=temp_kern_list1.copy()
                    print("temp_delete1",temp_delete1)
                    print("temp_kern_value1",temp_kern_value1)
                    reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)                    
                    SW_global.recent_input_list=temp_recent1.copy()
                    SW_global.cursor_pos=temp_cursor_pos1.copy()
                    SW_global.cursor_data=temp_cursor_data1.copy()
                    SW_global.letters_already_written=letters_already_written3.copy()
                    #guideline_axes[l].lines.clear()
                    while(len(guideline_axes[l].lines)>4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    for j in temp_guideline_axes1:
                        guideline_axes[l].lines.append(j)
                    print("cursor_pos",SW_global.cursor_pos)
                    print("cursor_data",SW_global.cursor_data)
                    print("delete_list:",delete_list)
                    print("kern_value_array",kern_value_array)
                    print("This is letter already written",SW_global.letters_already_written)
                    fig.canvas.draw()
                    features_checking_function()
                    print("Temp10",temp10)
                    if(len(SW_global.axes_data)>0):
                        text_flow_main1(list1=temp10[1],zero_axes=SW_global.axes_data[str(0)]["axis_data"],current_axes=SW_global.current_axes)
                    else:
                        text_flow_main1(list1=temp10[1],zero_axes=guideline_axes[l],current_axes=SW_global.current_axes)
                    ## Testing print
                    fig.canvas.draw()
                    print("This is SW_global.recent_input_list",SW_global.recent_input_list)





                elif(len(temp10)==1):
                    print("j1")
                    clear_digit_from_axes(axesdata=guideline_axes[l])
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[0],spec_axes=guideline_axes[l],baselines_objects_array=None)
                    kern_value_array.clear()
                    delete_list.clear()
                    SW_global.kern_list=temp_kern_list1.copy()
                    print("temp_delete1",temp_delete1)
                    print("temp_kern_value1",temp_kern_value1)
                    reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)                    
                    SW_global.recent_input_list=temp_recent1.copy()
                    SW_global.cursor_pos=temp_cursor_pos1.copy()
                    SW_global.cursor_data=temp_cursor_data1.copy()
                    SW_global.letters_already_written=letters_already_written3.copy()
                    #guideline_axes[l].lines.clear()
                    while(len(guideline_axes[l].lines)>4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    for j in temp_guideline_axes1:
                        guideline_axes[l].lines.append(j)
                    print("cursor_pos",SW_global.cursor_pos)
                    print("cursor_data",SW_global.cursor_data)
                    print("delete_list:",delete_list)
                    print("kern_value_array",kern_value_array)
                    print("This is letter already written",SW_global.letters_already_written)
                    SW_global.current_axes=guideline_axes[l]
                    if(len(SW_global.cursor_pos)>0):
                        SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
                    fig.canvas.draw()
                    features_checking_function()
                    ## Testing print
                    print("This is SW_global.recent_input_list",SW_global.recent_input_list)
                fig.canvas.draw()
            else:
                print("I am in else part of main add controller")
                print("event_key",event_key,"event_key")
                add_any_letter_with_space_from_rear_side(event_key=event_key)
        else:
            #### Need to check #####
            print("This is current_pos",SW_global.current_pos)
            print("This is current_axes",SW_global.current_axes)
            print("This is len(SW_global.axes_data)",len(SW_global.axes_data))
            ##### for not mouse cursor in guideline #####
            print("This is SW_global.current_pos_in_number",SW_global.current_pos_in_number)
            if(SW_global.current_axes!=None and guideline_axes[l]==SW_global.current_axes):
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                temp=[]
                for j in range(len(delete_list)):
                    if(SW_global.current_pos_in_number!=None and j==SW_global.current_pos_in_number):
                        temp.append(event_key)
                    temp.append(delete_list[j])
                print("This is temp ",temp)
                temp10=divide_delete_list_with_the_base_of_max_limit3(need_array=temp)
                print("This is temp10",temp10)
            else:
                print("check point alpha 2")
                print("chech ")
                key_axes=None
                if((SW_global.current_axes!=None) and(guideline_axes[l]!=SW_global.current_axes)):
                    for j in range(len(SW_global.axes_data)):
                        print("I am in loop0")
                        print(SW_global.axes_data[str(j)]["axis_data"])
                        if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.current_axes):
                            print("yes1")
                            key_axes=j
                            break
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                print("delete_list for guide line",delete_list)
                # for k1 in range(len(SW_global.axes_data)):
                #     print("delete_list_for",k1)
                #     print(SW_global.axes_data[str(k1)]["delete_list"])
                #### need to add function ####
                temp_delete_list1=[]
                temp_delete_list2=[]
                temp_delete_list1.extend(SW_global.axes_data[str(key_axes)]["delete_list"])
                for j in range(len(temp_delete_list1)):
                    if(j==SW_global.current_pos_in_number):
                        temp_delete_list2.append(event_key)
                    temp_delete_list2.append(temp_delete_list1[j])
                sum1=sum_of_digit(list1=temp_delete_list2)
                temp10=[]
                temp11=[]
                if(sum1>SW_global.max_limit):
                    print("ok1")
                    temp12=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list2.copy(),limit1=SW_global.max_limit)
                    clear_digit_from_axes(axesdata=SW_global.axes_data[str(key_axes)]["axis_data"])
                    print("This is temp12",temp12)
                    for j in temp12:
                        temp10.append(j)
                    print("This is temp 10",temp10)
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[0],spec_axes=SW_global.axes_data[str(key_axes)]["axis_data"],baselines_objects_array=None)
                    save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),
                        delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),
                        cursor_pos1=temp_cursor_pos1.copy(),
                        cursor_data1=temp_cursor_data1.copy(),
                        kern_list1=temp_kern_list1.copy(),axes_key_index=key_axes,
                        letters_already_written1=letters_already_written3.copy(),
                        lines1=temp_guideline_axes1,axesdata=SW_global.axes_data[str(key_axes)]["axis_data"])
                    zero_axes=None
                    if(len(SW_global.axes_data)>0):
                        zero_axes=SW_global.axes_data[str(0)]["axis_data"]
                    else:
                        zero_axes=guideline_axes[l]
                    print("check 251")
                    print("This is temp 10",temp10)
                    axes1=None
                    after_manupulation=before_send_to_text_flow_mannupulation(list1=temp10[1],axes_key=key_axes+1)
                    # if(len(SW_global.axes_data)>key_axes+1):
                    #     after_manupulation=before_send_to_text_flow_mannupulation(list1=None,axes_key=None)
                    #     #### need to attached before function####
                    #     print("check point delta 3")
                    #     axes1=guideline_axes[l]
                    # else:
                    #     print("check point delta 4")
                    axes1=guideline_axes[l]
                    if((after_manupulation!=None) and(axes1!=None)):
                        text_flow_main1(list1=after_manupulation,zero_axes=zero_axes,current_axes=axes1)

                    # if(axes1!=None):
                    #     text_flow_main1(list1=temp10[1],zero_axes=zero_axes,current_axes=axes1)

                else:
                    temp12=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list2.copy(),limit1=SW_global.max_limit)
                    temp10.clear()
                    for j in temp12:
                        temp10.append(j)

                    print("check point gurur")
                    print("check 252")
                    print("This is temp10",temp10)
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[0],spec_axes=SW_global.axes_data[str(key_axes)]["axis_data"],baselines_objects_array=None)
                    save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),
                        delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),
                        cursor_pos1=temp_cursor_pos1.copy(),
                        cursor_data1=temp_cursor_data1.copy(),
                        kern_list1=temp_kern_list1.copy(),axes_key_index=key_axes,
                        letters_already_written1=letters_already_written3.copy(),
                        lines1=temp_guideline_axes1,axesdata=SW_global.axes_data[str(key_axes)]["axis_data"])
                #divide_delete_list_for_add_operation(key_axes=key_axes,event_key=event_key)
                fig.canvas.draw()
            ####### #### change SW_global.current_pos ######
            ############ change SW_global.current_axes #######
            #if(SW_global.current_axes==guideline_axes[l]):
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                if(SW_global.current_axes==guideline_axes[l]):
                    if(SW_global.current_pos_in_number<len(SW_global.cursor_data)-1):
                        SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number+1]
                else:
                    for j in range(len(SW_global.axes_data)):
                        if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.current_axes):
                            if(SW_global.current_pos_in_number<len(SW_global.cursor_data)-1):
                                SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number+1]
                            elif(j+1<=len(SW_global.axes_data)-1):
                                SW_global.current_pos=SW_global.axes_data[str(j+1)]["cursor_pos"][1]
                                SW_global.current_axes=SW_global.axes_data[str(j+1)]["axis_data"]
                            elif(j+1>len(SW_global.axes_data)-1):
                                SW_global.current_pos=SW_global.cursor_pos[0]
                                SW_global.current_axes=guideline_axes[l]
    return 





def change_controller(key=None,axesdata=None):
    ###need to check change controller #####
    print("I am in change controller")
    if(guideline_axes[l]==axesdata):
        print("ok")
    else:
        flag=False
        if(len(SW_global.axes_data)>0):
            for j in range(len(SW_global.axes_data)):
                if(axesdata==SW_global.axes_data[str(j)]["axis_data"]):
                    break
                elif(j==len(SW_global.axes_data)-1):
                    axes_list_for_box=[]
                    for k11 in range(len(SW_global.axes_data)):
                        axes_list_for_box.append(SW_global.axes_data[str(k11)]["axis_data"])
                    axes_list_for_box.append(guideline_axes[l])
                    if(len(SW_global.box_data)>0):
                        data_checking_for_need_to_create_or_update_back_page(axes_list=axes_list_for_box,delete_list1=delete_list,kern_value_array1=kern_value_array)
                    else:
                        create_new_page_on_box_data(delete_list1=delete_list,kern_value_array1=kern_value_array)


        else:
            axes_list_for_box=[]
            for j in range(len(SW_global.axes_data)):
                axes_list_for_box.append(SW_global.axes_data[str(j)]["axis_data"])
            axes_list_for_box.append(guideline_axes[l])
            if(len(SW_global.box_data)>0):
                data_checking_for_need_to_create_or_update_back_page(axes_list=axes_list_for_box,delete_list1=delete_list,kern_value_array1=kern_value_array)
            else:
                create_new_page_on_box_data(delete_list1=delete_list,kern_value_array1=kern_value_array)
        temp_key=checking_for_which_box_need_to_switch(axesdata=axesdata)
        temp=data_Switching2(key=temp_key)

        if(temp!=None):
            delete_list.clear()
            kern_value_array.clear()
            #print("temp len:",len(temp_data))
            if(len(temp)==7):
                for j in temp[1]:
                    #print("I am in kern_ temp_1")
                    kern_value_array.append(j)
                for j in temp[0]:
                    #print("I am in kern_temp_1")
                    delete_list.append(j)
    return


def next_axes_for_text_flow(list1=None,zero_axes=None):

    return 
def sum_of_digit(list1=None):
    sum1=0
    if(list1!=None):
        for j in list1:
            if(j==" "):
                sum1=sum1+300
            else:
                sum1=sum1+manuscript.x_max[j]+300
        return sum1
    else:
        return None


def text_flow_main(list1=None,zero_axes=None):
    print("I am in text flow main ")
    key=None
    next_axes=[]
    #temp10=[]
    if((list1!=None) and(zero_axes!=None)):
        print("check point 11")
        for j in range(len(SW_global.text_flow_axes)):
            if(SW_global.text_flow_axes[j]==zero_axes):
                key=j
            elif(key!=None and key<j):
                next_axes.append(SW_global.text_flow_axes[j])

        print("This is next_axes",next_axes)
        print("This is key ", key)

        print("check point 22")
        if((key==None) and(len(next_axes)==0)):
            print("check point 33")
            save_data_to_axes_dict(kern_value1=kern_value_array.copy(),
                delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list.copy(),
                cursor_pos1=SW_global.cursor_pos.copy(),
                cursor_data1=SW_global.cursor_data.copy(),
                kern_list1=SW_global.kern_list.copy(),axes_key_index=None,
                letters_already_written1=SW_global.letters_already_written.copy(),
                lines1=guideline_axes[l].lines.copy(),axesdata=guideline_axes[l])
            newCreateGuideLine(1,None,None,None,None)
            temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=list1.copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
            SW_global.kern_list=temp_kern_list1.copy()
            print("temp_delete1",temp_delete1)
            print("temp_kern_value1",temp_kern_value1)
            reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)
            #delete_list=temp_delete1.copy()
            SW_global.recent_input_list=temp_recent1.copy()
            SW_global.cursor_pos=temp_cursor_pos1.copy()
            SW_global.cursor_data=temp_cursor_data1.copy()
            SW_global.letters_already_written=letters_already_written3.copy()
            #guideline_axes[l].lines.clear()
            while(len(guideline_axes[l].lines)>4):
                del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
            for j in temp_guideline_axes1:
                guideline_axes[l].lines.append(j)
            print("cursor_pos",SW_global.cursor_pos)
            print("cursor_data",SW_global.cursor_data)
            print("delete_list:",delete_list)
            print("kern_value_array",kern_value_array)
            SW_global.current_axes=guideline_axes[l]
            if(len(SW_global.cursor_pos)>0):
                SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
        else:
            ### Main logic start from here 
            print("check point 44 ***************")
            SW_global.delete_list_text_flow.clear()
            #print()
            count1=len(next_axes)-1
            count2=0
            check_axes=None
            change_key=None
            flag_break=False
            key1_for_next_axes=None
            print("next_axes",next_axes)
            SW_global.delete_list_text_flow.extend(list1.copy())
            print("I am in loppp start point ")
            for k in range(count2,count1+1):
                print("check point axes")
                check_axes=next_axes[k]
                key1_for_next_axes=k
                temp20=[]
                print("check point 3454566")
                for j in range(len(SW_global.box_data)):
                    print("I am in loop 11")
                    if(check_axes in SW_global.box_data[str(j)]["axes_list"]):
                        axes_data1=SW_global.box_data[str(j)]["SW_global_axes_data"]
                        change_key=j
                        if(len(axes_data1)>0):
                            SW_global.delete_list_text_flow.extend(axes_data1[str(0)]["delete_list"])
                        else:
                            SW_global.delete_list_text_flow.extend(SW_global.box_data[str(j)]["delete_list"])
                        temp10=divide_delete_list_with_the_base_of_max_limit3(need_array=SW_global.delete_list_text_flow,limit1=SW_global.max_limit)
                        print(temp10)
                        temp20=temp10.copy()
                        change_controller(key=j,axesdata=check_axes)
                        clear_digit_from_axes(axesdata=check_axes)
                        print(temp10)
                        temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp10[0].copy(),spec_axes=check_axes,baselines_objects_array=None)
                        print(temp10)
                        if(len(SW_global.axes_data)>0):
                            print()
                            save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=0,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=check_axes)
                            if(len(temp10)>1):
                                if(len(SW_global.axes_data)==1):
                                    letter_manupulation_after_apply_text_flow(axesdata=guideline_axes[l],need_array=temp10[1],key_for_next_axes=key1_for_next_axes)
                                else:
                                    letter_manupulation_after_apply_text_flow(axesdata=SW_global.axes_data[1],need_array=temp10[1],key_for_next_axes=key1_for_next_axes)

                        else:
                            if(len(temp10)>1):
                                print()
                                save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=None,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=check_axes)
                                newCreateGuideLine(1,None,None,None,None)
                                temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp10[1].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                                kern_value_array.clear()
                                kern_value_array.extend(temp_kern_value11.copy())
                                delete_list.clear()
                                delete_list.extend(temp_delete11.copy())
                                SW_global.kern_list.clear()
                                SW_global.kern_list.extend(temp_kern_list11.copy())
                                SW_global.recent_input_list.clear()
                                SW_global.recent_input_list.extend(temp_recent11.copy())
                                SW_global.cursor_pos.clear()
                                SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                                SW_global.cursor_data.clear()
                                SW_global.cursor_data.extend(temp_cursor_data11.copy())
                                SW_global.letters_already_written.clear()
                                ### need to remove after complete
                                ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                                for k22 in range(len(letters_already_written31)):
                                    letters_already_written3[k22]=letters_already_written3[k22]+3

                                SW_global.letters_already_written.extend(letters_already_written31.copy())
                                while(len(guideline_axes[l].lines)>4):
                                    del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                                guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
                            else:
                                kern_value_array.clear()
                                kern_value_array.extend(temp_kern_value11.copy())
                                delete_list.clear()
                                delete_list.extend(temp_delete11.copy())
                                SW_global.kern_list.clear()
                                SW_global.kern_list.extend(temp_kern_list11.copy())
                                SW_global.recent_input_list.clear()
                                SW_global.recent_input_list.extend(temp_recent11.copy())
                                SW_global.cursor_pos.clear()
                                SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                                SW_global.cursor_data.clear()
                                SW_global.cursor_data.extend(temp_cursor_data11.copy())
                                SW_global.letters_already_written.clear()
                                ### need to remove after complete
                                ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                                for k22 in range(len(letters_already_written31)):
                                    letters_already_written3[k22]=letters_already_written3[k22]+3

                                SW_global.letters_already_written.extend(letters_already_written31.copy())
                                while(len(guideline_axes[l].lines)>4):
                                    del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                                guideline_axes[l].lines.extend(temp_guideline_axes11.copy())


                ### need to write data updating function
                        if(len(temp10)>1):
                            if(len(next_axes)<key1_for_next_axes+1):
                                save_data_to_axes_dict()
                        SW_global.delete_list_text_flow.clear()
                        SW_global.delete_list_text_flow.extend(temp10[1].copy())
                        flag_break=True
                        break
                if(flag_break==True):
                    break
                        # print("check point alpha 11")
                        # print("temp10",temp10)
                        # if(len(SW_global.axes_data)==0):
                        #     SW_global.delete_list_text_flow.extend(delete_list.copy())
                        #     temp11=divide_delete_list_with_the_base_of_max_limit3(need_array=SW_global.delete_list_text_flow,limit1=SW_global.max_limit)
                        #     if(len(next_axes)<key1_for_next_axes+1):
                        #         print()
                        #         save_data_to_axes_dict(kern_value1=kern_value_array.copy(),
                        #             delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list.copy(),
                        #             cursor_pos1=SW_global.cursor_pos.copy(),
                        #             cursor_data1=SW_global.cursor_data.copy(),
                        #             kern_list1=SW_global.kern_list.copy(),axes_key_index=None,
                        #             letters_already_written1=SW_global.letters_already_written.copy(),
                        #             lines1=guideline_axes[l].lines.copy(),axesdata=guideline_axes[l])
                        #         reset_all_recent_guideline_features()
                        #         newCreateGuideLine(1,None,None,None,None)
                        #         temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                        #         kern_value_array.clear()
                        #         kern_value_array.extend(temp_kern_value11.copy())
                        #         SW_global.kern_list.extend(temp_kern_list11.copy())
                        #         delete_list.extend(temp_delete11.copy())
                        #         SW_global.recent_input_list.extend(temp_recent11.copy())
                        #         SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                        #         SW_global.cursor_data.extend(temp_cursor_data11.copy())
                        #         SW_global.letters_already_written.extend(letters_already_written2.copy())
                        #         guideline_axes[l].lines.clear()
                        #         guideline_axes[l].lines.extend(temp_guideline_axes2)
                        #     else:
                        #         print()
                        # #k=k+1





                        #if((len(next_axes)>key1_for_next_axes):
                        # if(len(temp10)>1):
                        #     SW_global.delete_list_text_flow.clear()
                        #     SW_global.delete_list_text_flow.extend(temp10[1])
                        #     k=1
                        #     while(k<len(temp10)):
                        #         if((len(SW_global.axes_data)==0) or(len(SW_global.axes_data)==key1_for_next_axes)):
                        #             SW_global.delete_list_text_flow.extend(delete_list.copy())
                        #             temp11=divide_delete_list_with_the_base_of_max_limit3(need_array=SW_global.delete_list_text_flow,limit1=SW_global.max_limit)
                        #             if(len()):




                        # if(len(temp10)>1):
                        #     print("check point beta 11")
                        #     print("This is ",temp10)
                        #     SW_global.delete_list_text_flow.extend(temp10[1])
                        #     print("I am in loop",len(temp10))
                        #     k=0
                        #     while(len(temp10)>k):
                        #         print("I am in loop")
                        # ### terminate condision will be len(temp10)<=1 due to print of letter
                        #         if((len(SW_global.axes_data)==key1_for_next_axes) or(len(SW_global.axes_data)==0)):
                        #             print("check point beta 22")
                        #             SW_global.delete_list_text_flow.extend(delete_list.copy())
                        #             sum1=sum_of_digit(list1=SW_global.delete_list_text_flow)
                        #             temp11=divide_delete_list_with_the_base_of_max_limit3(need_array=SW_global.delete_list_text_flow,limit1=SW_global.max_limit)
                        #             temp10.clear()
                        #             for j in temp11:
                        #                 temp10.append(j)
                        #             print("This temp11",temp11)
                        #             #break
                        #             print("This is temp11",temp11)
                        #             if(len(next_axes)<key1_for_next_axes):
                        #                 save_data_to_axes_dict(kern_value1=kern_value_array.copy(),
                        #                     delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list.copy(),
                        #                     cursor_pos1=SW_global.cursor_pos.copy(),
                        #                     cursor_data1=SW_global.cursor_data.copy(),
                        #                     kern_list1=SW_global.kern_list.copy(),axes_key_index=None,
                        #                     letters_already_written1=SW_global.letters_already_written.copy(),
                        #                     lines1=guideline_axes[l].lines.copy(),axesdata=guideline_axes[l])
                        #                 reset_all_recent_guideline_features()
                        #                 newCreateGuideLine(1,None,None,None,None)
                        #                 temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp10[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                        #                 ###guideline_axes[l].lines.clear()
                        #                 kern_value_array.clear()
                        #                 kern_value_array.extend(temp_kern_value11.copy())
                        #                 SW_global.kern_list.extend(temp_kern_list11.copy())
                        #                 delete_list.extend(temp_delete11.copy())
                        #                 SW_global.recent_input_list.extend(temp_recent11.copy())
                        #                 SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                        #                 SW_global.cursor_data.extend(temp_cursor_data11.copy())
                        #                 SW_global.letters_already_written.extend(letters_already_written2.copy())
                        #                 guideline_axes[l].lines.clear()
                        #                 guideline_axes[l].lines.extend(temp_guideline_axes2)

                        #             else:
                        #                 print("This")
                        #             #k=k+1


                        #         else:
                        #             print("check point beta 33")
                        #             key1_for_next_axes=key1_for_next_axes+1
                        #             SW_global.text_list_text_flow.extend((SW_global.axes_data[str(key1_for_next_axes)]["delete_list"]).copy())
                        #             sum1=sum_of_digit(list1=SW_global.text_list_text_flow)
                        #             if(sum1>=SW_global.max_limit):
                        #                 temp11=divide_delete_list_with_the_base_of_max_limit3(need_array=SW_global.delete_list_text_flow,limit1=SW_global.max_limit)
                        #                 temp10.clear()
                        #             for j in temp11:
                        #                 temp10.append(j)
                        #         k=k+1
                # if(temp20>1):
                #     SW_global.delete_list_text_flow.clear()
                #     k=0
                #     while(k<len(temp20)):
                #         if((len(SW_global.axes_data)==key1_for_next_axes) or(len(SW_global.axes_data)==0)):
                #             print("check point beta 22")
                #             SW_global.delete_list_text_flow.extend(delete_list.copy())
                #             sum1=sum_of_digit(list1=SW_global.delete_list_text_flow)
                #             temp11=divide_delete_list_with_the_base_of_max_limit3(need_array=SW_global.delete_list_text_flow,limit1=SW_global.max_limit)
                #             temp10=[]
                #             for j in temp11:
                #                 temp10.append(j)
                #             print("This temp11",temp11)
                #             break
                #         print("This is temp11",temp11)
                #         if(len(next_axes)<key1_for_next_axes):
                #             save_data_to_axes_dict(kern_value1=kern_value_array.copy(),
                #                 delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list.copy(),
                #                 cursor_pos1=SW_global.cursor_pos.copy(),
                #                 cursor_data1=SW_global.cursor_data.copy(),
                #                 kern_list1=SW_global.kern_list.copy(),axes_key_index=None,
                #                 letters_already_written1=SW_global.letters_already_written.copy(),
                #                 lines1=guideline_axes[l].lines.copy(),axesdata=guideline_axes[l])
                #             reset_all_recent_guideline_features()
                #             newCreateGuideLine(1,None,None,None,None)
                #             temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=temp10[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                #             ###guideline_axes[l].lines.clear()
                #             kern_value_array.clear()
                #             kern_value_array.extend(temp_kern_value11.copy())
                #             SW_global.kern_list.extend(temp_kern_list11.copy())
                #             delete_list.extend(temp_delete11.copy())
                #             SW_global.recent_input_list.extend(temp_recent11.copy())
                #             SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                #             SW_global.cursor_data.extend(temp_cursor_data11.copy())
                #             SW_global.letters_already_written.extend(letters_already_written2.copy())
                #             guideline_axes[l].lines.clear()
                #             guideline_axes[l].lines.extend(temp_guideline_axes2)

                #         else:
                #             print("This")
                #         k=k+1                            





            print("SW_global.delete_list_for_text_flow",SW_global.delete_list_text_flow)
    return

def text_flow_main1(list1=None,current_axes=None,zero_axes=None):
    print("I am in text flow main1")
    print("This is list1",list1)
    print("This is current_axes",current_axes)
    print("This is zero_axes",zero_axes)
    if((list1!=None) and(current_axes!=None) and(zero_axes!=None)):
        ###
        next_axes,key=find_next_axes1(zero_axes=zero_axes)

        if(current_axes==guideline_axes[l]):
            print("check pint 234")
            print()
            check_axes=None
            if(len(SW_global.axes_data)>0):
                #check_axes=SW_global.axes_data[0]
                if(len(next_axes)>0):
                    print("check point 2")
                    change_controller(key=None,axesdata=next_axes[0])
                    print("check point 3")
                    check_axes=next_axes[0]
                    print("This is list1",list1)
                    print("Next_axes1",next_axes)
                    letter_manupulation_after_apply_text_flow(need_array=list1,next_axes1=next_axes,key_for_axes_no=key,axesdata=check_axes)
                    print("check point 4")

                else:
                    print("check point 5")
                    save_data_to_axes_dict(kern_value1=kern_value_array.copy(),delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list,cursor_pos1=SW_global.cursor_pos.copy(),cursor_data1=SW_global.cursor_data.copy(),kern_list1=SW_global.kern_list,axes_key_index=None,letters_already_written1=SW_global.letters_already_written,lines1=guideline_axes[l].lines,axesdata=guideline_axes[l])
                    newCreateGuideLine(1,None,None,None,None)#createNewGuideLine(1,None,None,None,None)
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=list1.copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                    kern_value_array.clear()
                    kern_value_array.extend(temp_kern_value1.copy())
                    SW_global.kern_list.clear()
                    SW_global.kern_list.extend(temp_kern_list1)
                    delete_list.clear()
                    delete_list.extend(temp_delete1.copy())
                    SW_global.cursor_data.clear()
                    SW_global.cursor_data.extend(temp_cursor_data1.copy())
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_pos.extend(temp_cursor_pos1.copy())
                    SW_global.letters_already_written.clear()
                    ### need to remove after complete
                    ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                    for k22 in range(len(letters_already_written3)):
                        letters_already_written3[k22]=letters_already_written3[k22]+3

                    SW_global.letters_already_written.extend(letters_already_written3.copy())
                    while(len(guideline_axes[l].lines)>4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
        #letter_manupulation_after_apply_text_flow(need_array=None,next_axes1=None,key_for_axes_no=None,axesdata=None)

            else:
                print("check point 6")
                #check_axes=next_axes[0]
                if(len(next_axes)>0):
                    check_axes=next_axes[0]
                    change_controller(key=None,axesdata=check_axes)

                    print("check axes",check_axes)
                    next_axes1,key1=find_next_axes1(zero_axes=zero_axes)
                    if(len(SW_global.axes_data)>0):
                        check_axes=SW_global.axes_data[str(0)]["axis_data"]
                    else:
                        check_axes=guideline_axes[l]
                    if(key1==None):
                        key1=0
                    print("This is check point 6 list1,next_axes1,key1_for_next_axes_no",list1,next_axes1,key1)


                    letter_manupulation_after_apply_text_flow(need_array=list1,next_axes1=next_axes1,key_for_axes_no=0,axesdata=check_axes)
                else:
                    newCreateGuideLine(1,None,None,None,None)
                    temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=list1.copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                    kern_value_array.clear()
                    kern_value_array.extend(temp_kern_value11.copy())
                    delete_list.clear()
                    delete_list.extend(temp_delete11.copy())
                    SW_global.kern_list.clear()
                    SW_global.kern_list.extend(temp_kern_list11.copy())
                    SW_global.recent_input_list.clear()
                    SW_global.recent_input_list.extend(temp_recent11.copy())
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                    SW_global.cursor_data.clear()
                    SW_global.cursor_data.extend(temp_cursor_data11.copy())
                    SW_global.letters_already_written.clear()
                    ### need to remove after complete
                    ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                    for k22 in range(len(letters_already_written31)):
                        letters_already_written31[k22]=letters_already_written31[k22]+3

                    SW_global.letters_already_written.extend(letters_already_written31.copy())
                    while(len(guideline_axes[l].lines)>4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    guideline_axes[l].lines.extend(temp_guideline_axes11.copy())


        else:
            print("I am in else part ")
            check_flag=None
            key_axes=None
            print()
            for j in range(len(SW_global.axes_data)):
                if(SW_global.axes_data[str(j)]["axis_data"]==current_axes):
                    key_axes=j
                    break
            print("This is list1",list1)
            print("This is need axes",next_axes)

            #next_axes1,key1=find_next_axes1(zero_axes=zero_axes)
            letter_manupulation_after_apply_text_flow(need_array=list1,next_axes1=next_axes,key_for_axes_no=key,axesdata=SW_global.axes_data[str(key_axes)]["axis_data"])


    return


def before_send_to_text_flow_mannupulation(list1=None,axes_key=None):
    break_flag=None
    temp_list=[]
    temp_delete_list2=[]
    if((list1!=None) and(axes_key!=None) and(axes_key>=len(SW_global.axes_data))):
        temp_delete_list2.extend(list1.copy())
        temp_delete_list2.extend(delete_list.copy())
        temp12=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list2.copy(),limit1=SW_global.max_limit)
        clear_digit_from_axes(axesdata=guideline_axes[l])
        temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp12[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
        kern_value_array.clear()
        kern_value_array.extend(temp_kern_value11.copy())
        SW_global.kern_list.clear()
        SW_global.kern_list.extend(temp_kern_list11.copy())
        delete_list.clear()
        delete_list.extend(temp_delete11.copy())
        SW_global.recent_input_list.clear()
        SW_global.recent_input_list.extend(temp_recent11.copy())
        SW_global.cursor_data.clear()
        SW_global.cursor_data.extend(temp_cursor_data11.copy())
        SW_global.cursor_pos.clear()
        SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
        SW_global.letters_already_written.clear()
        SW_global.letters_already_written.extend(letters_already_written31.copy())
        while(len(guideline_axes)>=4):
            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]

        if(len(temp12)>1):
            return temp12[1]
        else:
            return None

    
    if((list1!=None) and(axes_key!=None)):
        for j in range(axes_key,len(SW_global.axes_data)):
            temp_delete_list2.clear()
            temp_delete_list2.extend(list1.copy())
            temp_delete_list2.extend((SW_global.axes_data[str(j)]["delete_list"]).copy())
            temp10=[]
            temp11=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list2.copy(),limit1=SW_global.max_limit)
            if((len(temp11)==1) and(j!=len(SW_global.axes_data)-1)):
                clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=SW_global.axes_data[str(j)]["axis_data"],baselines_objects_array=None)
                save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=j,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=SW_global.axes_data)
                return None
                break_flag=True
            elif((len(temp11)>1) and(j!=len(SW_global.axes_data)-1)):
                clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=SW_global.axes_data[str(j)]["axis_data"],baselines_objects_array=None)
                save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=j,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=SW_global.axes_data)
                list1.clear()
                list1.extend(temp11[1].copy())
            elif((len(temp11)==1) and(j==len(SW_global.axes_data)-1)):
                clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=SW_global.axes_data[str(j)]["axis_data"],baselines_objects_array=None)
                save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=j,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=SW_global.axes_data)
                return None
                break_flag=True
            elif((len(temp11)>=1) and(j==len(SW_global.axes_data)-1)):
                clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=SW_global.axes_data[str(j)]["axis_data"],baselines_objects_array=None)
                save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=j,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=SW_global.axes_data)
                temp_delete_list2.clear()
                temp_delete_list2.extend(temp11[1].copy())
                temp_delete_list2.extend(delete_list.copy())
                temp12=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list2.copy(),limit1=SW_global.max_limit)
                clear_digit_from_axes(axesdata=guideline_axes[l])
                temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp12[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                kern_value_array.clear()
                kern_value_array.extend(temp_kern_value11.copy())
                SW_global.kern_list.clear()
                SW_global.kern_list.extend(temp_kern_list11.copy())
                delete_list.clear()
                delete_list.extend(temp_delete11.copy())
                SW_global.recent_input_list.clear()
                SW_global.recent_input_list.extend(temp_recent11.copy())
                SW_global.cursor_data.clear()
                SW_global.cursor_data.extend(temp_cursor_data11.copy())
                SW_global.cursor_pos.clear()
                SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                SW_global.letters_already_written.clear()
                SW_global.letters_already_written.extend(letters_already_written31.copy())
                while(len(guideline_axes)>=4):
                    del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]

                if(len(temp12)>1):
                    return temp12[1]
                else:
                    return None







            if(break_flag==True):
                break








def find_next_axes1(zero_axes=None):
    print("I am in find next axes1")
    next_axes=[]
    key=None
    if(zero_axes!=None):
        for j in range(len(SW_global.text_flow_axes)):
            if(SW_global.text_flow_axes[j]==zero_axes):
                key=j
            elif(key!=None and key<j):
                next_axes.append(SW_global.text_flow_axes[j])


    return next_axes,key

def letter_manupulation_after_apply_text_flow(need_array=None,next_axes1=None,key_for_axes_no=None,axesdata=None):
    print("I am in letter manupulation")
    print("This need array",need_array)
    print("This is next_axes1",next_axes1)
    print("This is key for axes no ",key_for_axes_no)
    print("This is axesdata",axesdata)
    temp_delete_for_calc=[]
    temp11=[]
    flag_break=False
    temp11.extend(need_array.copy())
    if((need_array!=None) and(next_axes1!=None) and (key_for_axes_no!=None) and (axesdata!=None)):
        print("check 45")
        temp_delete_for_calc.extend(need_array.copy())
        print("This is key for axes no",key_for_axes_no)
        if(key_for_axes_no<len(next_axes1)):
            for j in range(key_for_axes_no,len(next_axes1)):
                if(axesdata==guideline_axes[l]):
                    temp_delete_for_calc.extend(delete_list.copy())
                    temp10=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_for_calc.copy(),limit1=SW_global.max_limit)
                    print("This is temp 10",temp10)
                    temp11.clear()
                    for k10 in temp10:
                        ### this can be replaced by extend()
                        temp11.append(k10)
                    print(temp11)
                    if(len(temp11)>1):
                        if(key_for_axes_no+1>len(next_axes1)):
                            print("need not to switch")
                            temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                            #temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp10[1].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                            save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=None,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=guideline_axes[l])#save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=None,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=guideline_axes[l])
                            newCreateGuideLine(1,None,None,None)
                            temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp10[1].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                            kern_value_array.clear()
                            kern_value_array.extend(temp_kern_value11.copy())
                            delete_list.clear()
                            delete_list.extend(temp_delete11.copy())
                            SW_global.kern_list.clear()
                            SW_global.kern_list.extend(temp_kern_list11.copy())
                            SW_global.recent_input_list.clear()
                            SW_global.recent_input_list.extend(temp_recent11.copy())
                            SW_global.cursor_pos.clear()
                            SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                            SW_global.cursor_data.clear()
                            SW_global.cursor_data.extend(temp_cursor_data11.copy())
                            SW_global.letters_already_written.clear()
                            ### need to remove after complete
                            ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                            for k22 in range(len(letters_already_written31)):
                                letters_already_written31[k22]=letters_already_written31[k22]+3

                            SW_global.letters_already_written.extend(letters_already_written31.copy())
                            while(len(guideline_axes[l].lines)>4):
                                del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                            guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
                            #newCreateGuideLine(1,None,None,None,None)
                            #save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=None,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=guideline_axes[l])
                            
                            key_for_axes_no=key_for_axes_no+1
                        else:
                            print("need to SWitch")
                            clear_digit_from_axes(axesdata=guideline_axes[l])
                            temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                            #save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=None,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=guideline_axes[l])
                            kern_value_array.clear()
                            kern_value_array.extend(temp_kern_value11.copy())
                            delete_list.clear()
                            delete_list.extend(temp_delete11.copy())
                            SW_global.kern_list.clear()
                            SW_global.kern_list.extend(temp_kern_list11.copy())
                            SW_global.recent_input_list.clear()
                            SW_global.recent_input_list.extend(temp_recent11.copy())
                            SW_global.cursor_pos.clear()
                            SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                            SW_global.cursor_data.clear()
                            SW_global.cursor_data.extend(temp_cursor_data11.copy())
                            SW_global.letters_already_written.clear()
                            ### need to remove after complete
                            ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                            for k22 in range(len(letters_already_written31)):
                                letters_already_written31[k22]=letters_already_written31[k22]+3

                            SW_global.letters_already_written.extend(letters_already_written31.copy())
                            while(len(guideline_axes[l].lines)>4):
                                del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                            guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
                            #### data saving in box function call
                            #### then switching_data sunction call and switch to next_axes[key_for_axes_no]                            
                            key_for_axes_no=key_for_axes_no+1
                            print("check point beta ")
                            ##check_axes=next_axes1[key_for_axes_no]
                            # if(len(SW_global.axes_data)>0):
                            #     check_axes=SW_global.axes_data[str(0)]["axis_data"]
                            # else:
                            #     check_axes=guideline_axes[l]

                            ##change_controller(key=None,axesdata=check_axes)
                            ##axesdata=check_axes
                            temp11.clear()
                            temp11.append(temp10[1])
                            k=temp10[1]
                            print("This is last temp10",temp10)
                            if(len(temp11)>0):
                                print("I am in last word which does not get place in current_axes need to create another one")
                                save_data_to_axes_dict(kern_value1=kern_value_array.copy(),delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list.copy(),cursor_pos1=SW_global.cursor_pos.copy(),cursor_data1=SW_global.cursor_data.copy(),kern_list1=SW_global.kern_list.copy(),axes_key_index=None,letters_already_written1=SW_global.letters_already_written.copy(),lines1=guideline_axes[l].lines.copy(),axesdata=guideline_axes[l])
                                newCreateGuideLine(1,None,None,None,None)
                                temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                                flag_break=True
                                kern_value_array.clear()
                                kern_value_array.extend(temp_kern_value11.copy())
                                delete_list.clear()
                                delete_list.extend(temp_delete11.copy())
                                SW_global.kern_list.clear()
                                SW_global.kern_list.extend(temp_kern_list11.copy())
                                SW_global.recent_input_list.clear()
                                SW_global.recent_input_list.extend(temp_recent11.copy())
                                SW_global.cursor_pos.clear()
                                SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                                SW_global.cursor_data.clear()
                                SW_global.cursor_data.extend(temp_cursor_data11.copy())
                                SW_global.letters_already_written.clear()
                                while(len(guideline_axes[l].lines)>4):
                                    del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                                guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
                                flag_break=True
                                break








                    else:
                        print("check point 46")
                        clear_digit_from_axes(axesdata=guideline_axes[l])
                        # print("do normal print on axes ")
                        # for i in range(len(SW_global.axes_data)):
                        #     if(SW_global.axes_data[str(i)]["axis_data"]==axesdata):
                        #temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp11[1].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                        temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp11[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                        #save_data_to_axes_dict(kern_value1=temp_kern_value1.copy(),delete_list1=temp_delete1.copy(),recent_input_list1=temp_recent1.copy(),cursor_pos1=temp_cursor_pos1.copy(),cursor_data1=temp_cursor_data1.copy(),kern_list1=temp_kern_list1.copy(),axes_key_index=None,letters_already_written1=letter_already_written3.copy(),lines1=temp_guideline_axes1.copy(),axesdata=guideline_axes[l])
                        kern_value_array.clear()
                        kern_value_array.extend(temp_kern_value11.copy())
                        delete_list.clear()
                        delete_list.extend(temp_delete11.copy())
                        SW_global.kern_list.clear()
                        SW_global.kern_list.extend(temp_kern_list11.copy())
                        SW_global.recent_input_list.clear()
                        SW_global.recent_input_list.extend(temp_recent11.copy())
                        SW_global.cursor_pos.clear()
                        SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                        SW_global.cursor_data.clear()
                        SW_global.cursor_data.extend(temp_cursor_data11.copy())
                        SW_global.letters_already_written.clear()
                        ### need to remove after complete
                        ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                        for k22 in range(len(letters_already_written31)):
                            letters_already_written31[k22]=letters_already_written31[k22]+3

                        SW_global.letters_already_written.extend(letters_already_written31.copy())
                        while(len(guideline_axes[l].lines)>4):
                            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                        guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
                        #### data saving in box function call
                        #### then switching_data sunction call and switch to next_axes[key_for_axes_no]                            
                        key_for_axes_no=key_for_axes_no+1
                        flag_break=True
                        break
                else:
                    print("check point 47")
                    key10=None
                    temp_delete_list=[]
                    temp_delete_list.extend(need_array.copy())
                    print("temp_delete_list",temp_delete_list)
                    print("check point 471")
                    for k1 in range(len(SW_global.axes_data)):
                        if(axesdata==SW_global.axes_data[str(k1)]["axis_data"]):
                            print("check point 472")
                            key10=k1
                            temp11.extend(SW_global.axes_data[str(k1)]["delete_list"])
                            print("check point 4731")
                            temp9=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                            clear_digit_from_axes(axesdata=SW_global.axes_data[str(k1)]["axis_data"])
                            print("check point 4741")
                            temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp9[0].copy(),spec_axes=SW_global.axes_data[str(k1)]["axis_data"],baselines_objects_array=None)
                            save_data_to_axes_dict(kern_value1=temp_kern_value11.copy(),delete_list1=temp_delete11.copy(),recent_input_list1=temp_recent11.copy(),cursor_pos1=temp_cursor_pos11.copy(),cursor_data1=temp_cursor_data11.copy(),kern_list1=temp_kern_list11.copy(),axes_key_index=j,letters_already_written1=letters_already_written31.copy(),lines1=temp_guideline_axes11.copy(),axesdata=SW_global.axes_data[str(j)]["axis_data"])
                            if(len(temp9)==1):
                                break_flag=True
                            elif(len(temp9)>1):
                                temp11.clear()
                                temp11.append(temp9[1])
                        elif(k1==len(SW_global.axes_data)):
                            print("yes")
                            temp11.extend(delete_list)
                            #temp9=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                            temp9=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                            clear_digit_from_axes(axesdata=guideline_axes[l])
                            temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp9[0].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                            #save_data_to_axes_dict(kern_value1=temp_kern_value11.copy(),delete_list1=temp_delete11.copy(),recent_input_list1=temp_recent11.copy(),cursor_pos1=temp_cursor_pos11.copy(),cursor_data1=temp_cursor_data11.copy(),kern_list1=temp_kern_list11.copy(),axes_key_index=j,letters_already_written1=letter_already_written31.copy(),lines1=temp_guideline_axes11.copy(),axesdata=SW_global.axes_data[str(j)]["axis_data"])
                            if(len(temp9)==1):
                                break_flag=True
                            elif(len(temp9)>1):
                                temp11.clear()
                                temp11.append(temp9[1])

                            kern_value_array.clear()
                            kern_value_array.extend(temp_kern_value11.copy())
                            delete_list.clear()
                            delete_list.extend(temp_delete11.copy())
                            SW_global.kern_list.clear()
                            SW_global.kern_list.extend(temp_kern_list11.copy())
                            SW_global.recent_input_list.clear()
                            SW_global.recent_input_list.extend(temp_recent11.copy())
                            SW_global.cursor_pos.clear()
                            SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                            SW_global.cursor_data.clear()
                            SW_global.cursor_data.extend(temp_cursor_data11.copy())
                            SW_global.letters_already_written.clear()
                            ### need to remove after complete
                            ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                            for k22 in range(len(letters_already_written31)):
                                letters_already_written31[k22]=letters_already_written31[k22]+3
                            print("check point 473")

                            SW_global.letters_already_written.extend(letters_already_written31.copy())
                            while(len(guideline_axes[l].lines)>4):
                                del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                            guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
                            print("check point 474")
                            if(len(temp9)>1):
                                key_for_next_axes=key_for_next_axes+1
                                if(len(next_axes1)<key_for_next_axes):
                                    save_data_to_axes_dict(kern_value1=kern_value_array.copy(),delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list.copy(),cursor_pos1=SW_global.cursor_pos.copy(),cursor_data1=SW_global.cursor_data.copy(),kern_list1=SW_global.kern_list.copy(),axes_key_index=None,letters_already_written1=SW_global.letters_already_written.copy(),lines1=guideline_axes[l].lines.copy(),axesdata=guideline_axes[l])
                                    createNewGuideLine(1,None,None,None)
                                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp9[1].copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                                    kern_value_array.clear()
                                    kern_value_array.extend(temp_kern_value11.copy())
                                    delete_list.clear()
                                    delete_list.extend(temp_delete11.copy())
                                    SW_global.kern_list.clear()
                                    SW_global.kern_list.extend(temp_kern_list11.copy())
                                    SW_global.recent_input_list.clear()
                                    SW_global.recent_input_list.extend(temp_recent11.copy())
                                    SW_global.cursor_pos.clear()
                                    SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                                    SW_global.cursor_data.clear()
                                    SW_global.cursor_data.extend(temp_cursor_data11.copy())
                                    SW_global.letters_already_written.clear()
                                    ### need to remove after complete
                                    ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                                    for k22 in range(len(letters_already_written31)):
                                        letters_already_written31[k22]=letters_already_written31[k22]+3

                                    SW_global.letters_already_written.extend(letters_already_written31.copy())
                                    while(len(guideline_axes[l].lines)>4):
                                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                                    guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
                                    print("check point 477")
                                else:
                                    print("check point 478")
                                    check_axes=next_axes1[key_for_axes_no]
                                    change_controller(key=None,axesdata=check_axes)
                                    axesdata=check_axes
                                    temp11.clear()
                                    temp11.append(temp10[1])

                            ### need to switch data in this block if need ## ##condition will be like len(temp10)>1
                        elif((key10!=None) and (key10>j)):
                            print("need to continue ")
                            temp11.extend(SW_global.axes_data[str(k1)]["delete_list"])
                            temp9=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                            temp9=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list.copy(),limit1=SW_global.max_limit)
                            clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["delete_list"])
                            temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=temp9[0].copy(),spec_axes=SW_global.axes_data[str(j)]["axes_data"],baselines_objects_array=None)
                            save_data_to_axes_dict(kern_value1=temp_kern_value11.copy(),delete_list1=temp_delete11.copy(),recent_input_list1=temp_recent11.copy(),cursor_pos1=temp_cursor_pos11.copy(),cursor_data1=temp_cursor_data11.copy(),kern_list1=temp_kern_list11.copy(),axes_key_index=j,letters_already_written1=letter_already_written31.copy(),lines1=temp_guideline_axes11.copy(),axesdata=SW_global.axes_data[str(j)]["axis_data"])
                            if(len(temp9)==1):
                                break_flag=True
                            elif(len(temp9)>1):
                                temp11.clear()
                                temp11.append(temp9[1])

                            ###
                            ### need to update temp11 for next operation
                            #temp11.append()
                if(flag_break==True):
                    print("I am in break 2nd ")
                    break
                        





    print("I am in end part of letter manupulation  ")

    return



def reset_all_recent_guideline_features():
    SW_global.recent_input_list.clear()
    SW_global.kern_list.clear()
    SW_global.kern_list.append(0)
    kern_value_array.clear()
    kern_value_array.append(0)
    delete_list.clear()
    SW_global.letters_already_written.clear()
    SW_global.cursor_pos.clear()
    SW_global.cursor_pos.append(0)
    SW_global.cursor_data.clear()
    return

def divide_delete_list_with_the_base_of_max_limit3(need_array=None,limit1=None):
    print(" I  am in divide")
    print("need array",need_array)

    temp=[]
    sum1=0
    temp1=[]
    count1=0
    count2=-1
    if(need_array!=None and limit1!=None): 
        if(" " in need_array):
            for k0 in need_array:
                count2=count2+1
                if(k0==" "):
                    for k1 in range(count1,count2+1):
                        temp1.append(need_array[k1])
                    temp.append(temp1.copy())
                    temp1.clear()
                    count1=count2+1
                elif(len(need_array)-1==count2):
                    for k1 in range(count1,count2+1):
                        temp1.append(need_array[k1])
                    temp.append(temp1.copy())
                    temp1.clear()
                    count1=count2+1
        else:
            temp.append(need_array.copy())

        sum1=0
        count1=0
        count2=-1
        temp3=[]
        temp10=[]
        calc=[]
        print("temp",temp)
        for j in temp:
            count1=0
            count2=-1
            print(j)
#            if(" " in j):
            for k1 in j:
                count2=count2+1
                if(k1==" "):
                    sum1=sum1+300
                else:
                    sum1=sum1+manuscript.x_max[k1]+300
                if(sum1>=limit1):
                    print("check point 10")
                    for k2 in range(count1,count2+1):
                        temp10.append(j[k2])
                        count1=count2+1
                    print(temp10)
                    temp3.append(temp10.copy())
                    temp10.clear()
                    calc.append(sum1)
                    sum1=0
                if((count2==len(j)-1) and (sum1<=limit1)):
                    print("check point 11")
                    for k2 in range(count1,count2+1):
                        temp10.append(j[k2])
                    temp3.append(temp10.copy())
                    temp10.clear()
                    calc.append(sum1)
                    sum1=0
            # else:
            #     print("2")
            #     print(j)
            #     temp3.append(j.copy())
        print(calc)
        print(temp3)
        sum1=0
        count1=0
        count2=-1
        temp4=[]
        temp5=[]


        count1=0
        count2=0
        temp4=[]
        count1=0
        count2=-1
        sum1=0
        for j in range(len(calc)):
            sum1=sum1+calc[j]
            count2=count2+1
            print(sum1)
            print("count1",count1)
            print("count2",count2)
            print(j)
            print("temp3",temp3)

            if(sum1>=limit1):
                if(count1==count2):
                    print("check point 11111")
                    temp5.append(temp3[count1])
                    sum1=0
                    count1=count2+1
                elif(count1<count2):
                    print("check point112233")
                    temp4.clear()
                    for k2 in range(count1,count2):
                        temp4.extend(temp3[k2])
                    sum1=0
                    temp5.append(temp4.copy())
                    temp4.clear()
                    count1=count2
            if((j==len(calc)-1)):
                print("I am in end point")
                print(count1)
                print(count2)
                if(count1<count2):
                    print("check point 111123455")
                    for k2 in range(count1,count2):
                        temp4.extend(temp3[k2])
                    sum1=0
                    temp5.append(temp4.copy())
                    temp4.clear()
                    count1=count2
                elif(count1==count2):
                    print("check point 11111")
                    temp5.append(temp3[count1])
                    sum1=0
                    count1=count2
                #else:
                elif(count1>count2):
                    temp5.append(temp3[j])

        print("temp5",temp5)

        count1=0
        count2=-1
        temp10=[]
        sum1=0

        for j in range(len(calc)):
            count2=j
            sum1=sum1+calc[j]
            if(calc[j]>limit1):
                if(count1<count2):
                    temp4.clear()
                    for k1 in range(count1,count2):
                        temp4.extend(temp3[k1])
                    temp10.append(temp4.copy())
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
                elif(count1==count2):
                    temp4.clear()
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()

            elif(sum1>SW_global.max_limit):
                temp4.clear()
                if(count1<count2):
                    for k1 in range(count1,count2):
                        temp4.extend(temp3[k1])
                    temp10.append(temp4.copy())
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
                elif(count1==count2):
                    temp4.clear()
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
            elif((j==len(calc)-1) and (sum1<SW_global.max_limit)):
                for k1 in range(count1,count2):
                    temp4.extend(temp3[k1])
                temp10.append(temp4.copy())
                temp10.append(temp3[count2].copy())
                sum1=0
                count1=count2+1
                temp4.clear()
        print("This is temp 10", temp10)
        temp11=[]
        for j in temp10:
            if(len(j)!=0):
                temp11.append(j.copy())





    return temp11.copy()


def divide_delete_list_with_the_base_of_max_limit2(need_array=None,limit1=None):
    print(" I  am in divide")
    print("need array")

    temp=[]
    sum1=0
    temp1=[]
    count1=0
    count2=-1

    if need_array!=None and limit1!=None:
        print("ok")
        for k0 in need_array:
            count2=-1
            count1=0
            print("I am starting ")
#            if(" " in k0):
            for j in k0:
                count2=count2+1
                print("count2",count2)
                print(len(need_array))
                print(j)
                print(need_array)
                print(k0)
                if(j==" "):
                    print("check point 4")
                    print(count1)
                    print(count2+1)
                    for k1 in range(count1,count2+1):
                        temp1.append(k0[k1])
                    temp.append(temp1.copy())
                    temp1.clear()
                    count1=count2+1
                if((count2==len(k0)-1) and(j!=" ")):
                    print("check point2")
                    for k1 in range(count1,count2+1):
                        temp1.append(k0[k1])
                    print("check point3")
                    temp.append(temp1.copy())
                    temp1.clear()
#            else:
#                temp.append(k0)
        #temp.clear()
        sum1=0
        count1=0
        count2=-1
        temp3=[]
        temp10=[]
        calc=[]
        print("temp",temp)
        for j in temp:
            count1=0
            count2=-1
            print(j)
#            if(" " in j):
            for k1 in j:
                count2=count2+1
                if(k1==" "):
                    sum1=sum1+300
                else:
                    sum1=sum1+manuscript.x_max[k1]+300
                if(sum1>=limit1):
                    print("check point 10")
                    for k2 in range(count1,count2+1):
                        temp10.append(j[k2])
                        count1=count2+1
                    print(temp10)
                    temp3.append(temp10.copy())
                    temp10.clear()
                    calc.append(sum1)
                    sum1=0
                if((count2==len(j)-1) and (sum1<=limit1)):
                    print("check point 11")
                    for k2 in range(count1,count2+1):
                        temp10.append(j[k2])
                    temp3.append(temp10.copy())
                    temp10.clear()
                    calc.append(sum1)
                    sum1=0
            # else:
            #     print("2")
            #     print(j)
            #     temp3.append(j.copy())
        print(calc)
        print(temp3)
        sum1=0
        count1=0
        count2=-1
        temp4=[]
        temp5=[]


        count1=0
        count2=0
        temp4=[]
        count1=0
        count2=-1
        sum1=0
        for j in range(len(calc)):
            sum1=sum1+calc[j]
            count2=count2+1
            print(sum1)
            print("count1",count1)
            print("count2",count2)
            print(j)
            print("temp3",temp3)

            if(sum1>=limit1):
                if(count1==count2):
                    print("check point 11111")
                    temp5.append(temp3[count1])
                    sum1=0
                    count1=count2+1
                elif(count1<count2):
                    print("check point112233")
                    temp4.clear()
                    for k2 in range(count1,count2):
                        temp4.extend(temp3[k2])
                    sum1=0
                    temp5.append(temp4.copy())
                    temp4.clear()
                    count1=count2
            if((j==len(calc)-1)):
                print("I am in end point")
                print(count1)
                print(count2)
                if(count1<count2):
                    print("check point 111123455")
                    for k2 in range(count1,count2):
                        temp4.extend(temp3[k2])
                    sum1=0
                    temp5.append(temp4.copy())
                    temp4.clear()
                    count1=count2
                elif(count1==count2):
                    print("check point 11111")
                    temp5.append(temp3[count1])
                    sum1=0
                    count1=count2
                #else:
                elif(count1>count2):
                    temp5.append(temp3[j])

        print("temp5",temp5)

        count1=0
        count2=-1
        temp10=[]
        sum1=0

        for j in range(len(calc)):
            count2=j
            sum1=sum1+calc[j]
            if(calc[j]>limit1):
                if(count1<count2):
                    temp4.clear()
                    for k1 in range(count1,count2):
                        temp4.extend(temp3[k1])
                    temp10.append(temp4.copy())
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
                elif(count1==count2):
                    temp4.clear()
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()

            elif(sum1>SW_global.max_limit):
                temp4.clear()
                if(count1<count2):
                    for k1 in range(count1,count2):
                        temp4.extend(temp3[k1])
                    temp10.append(temp4.copy())
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
                elif(count1==count2):
                    temp4.clear()
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
            elif((j==len(calc)-1) and (sum1<SW_global.max_limit)):
                for k1 in range(count1,count2):
                    temp4.extend(temp3[k1])
                temp10.append(temp4.copy())
                temp10.append(temp3[count2].copy())
                sum1=0
                count1=count2+1
                temp4.clear()
        print("This is temp 10", temp10)
        temp11=[]
        for j in temp10:
            if(len(j)!=0):
                temp11.append(j.copy())
    return temp11.copy() #temp5.copy()




def divide_delete_list_with_the_base_of_max_limit(need_array=None):
    print(" I  am in divide")

    temp=[]
    sum1=0
    temp1=[]
    count1=0
    count2=-1

    if need_array!=None:
        print("ok")
        for k0 in need_array:
            count2=-1
            count1=0
            print("I am starting ")
            for j in k0:
                count2=count2+1
                print("count2",count2)
                print(len(need_array))
                print(j)
                print(need_array)
                print(k0)
                if(j==" "):
                    print("check point 4")
                    print(count1)
                    print(count2+1)
                    for k1 in range(count1,count2+1):
                        temp1.append(k0[k1])
                    temp.append(temp1.copy())
                    temp1.clear()
                    count1=count2+1
                if((count2==len(k0)-1) and(j!=" ")):
                    print("check point2")
                    for k1 in range(count1,count2+1):
                        temp1.append(k0[k1])
                    print("check point3")
                    temp.append(temp1.copy())
                    temp1.clear()
        #temp.clear()
        sum1=0
        count1=0
        count2=-1
        temp3=[]
        temp10=[]
        calc=[]
        print("temp",temp)
        for j in temp:
            count1=0
            count2=-1
            print(j)
            for k1 in j:
                count2=count2+1
                if(k1==" "):
                    sum1=sum1+300
                else:
                    sum1=sum1+manuscript.x_max[k1]+300
                if(sum1>=SW_global.max_limit):
                    print("check point 10")
                    for k2 in range(count1,count2+1):
                        temp10.append(j[k2])
                        count1=count2+1
                    print(temp10)
                    temp3.append(temp10.copy())
                    temp10.clear()
                    calc.append(sum1)
                    sum1=0
                if((count2==len(j)-1) and (sum1<=SW_global.max_limit)):
                    print("check point 11")
                    for k2 in range(count1,count2+1):
                        temp10.append(j[k2])
                    temp3.append(temp10.copy())
                    temp10.clear()
                    calc.append(sum1)
                    sum1=0
        print(calc)
        print(temp3)
        sum1=0
        count1=0
        count2=-1
        temp4=[]
        temp5=[]


        count1=0
        count2=0
        temp4=[]
        # for j in range(len(calc)):
        #     print("I am in check 11122")
        #     sum1=sum1+calc[j]
        #     if(sum1>SW_global.max_limit):
        #         print("I am in check 33333")
        #         if(count1==count2):
        #             temp4.extend(temp3[count1])
        #             temp5.append(temp4.copy())
        #             temp4.clear()
        #             sum1=0
        #         else:
        #             if(count1<count2):
        #                 print("I am in check 44444")
        #                 for k2 in range(count1,count2):
        #                     temp4.extend(temp3[k2])
        #                 temp5.append(temp4.copy())
        #                 count1=count2+1
        #                 sum1=0
        #                 temp4.clear()
        #             if((j==len(calc)-1) and(count2>count1)):
        #                 print("I am in check 5555")
        #                 for k2 in range(count1,count2):
        #                     temp4.extend(temp3[k2])
        #                 temp5.append(temp4)
        #                 sum1=0
        #                 temp4.clear()
        #     if((j==len(calc)-1) and(count2>count1)):
        #         print("I am in check 6666")
        #         for k2 in range(count1,count2):
        #             temp4.extend(temp3[k2])
        #         temp5.append(temp4.copy())
        #         sum1=0
        #         temp4.clear()

        #     count2=count2+1
        count1=0
        count2=-1
        sum1=0
        # for j in range(len(calc)):
        #     if((calc[j]>=SW_global.max_limit) and (count1==None)):
        #         temp5.append(temp3[j])
        #     elif(calc[j]<SW_global.max_limit):
        #         if(sum1==None):
        #             sum1=calc[j]
        #             count1=j
        #             count2=j
        #         elif(sum1!=None):
        #             sum1=sum1+calc[j]
        #         elif((sum1>SW_global.max_limit) and (count1!=None) and (count2!=None)):
        #             for k2 in range(count1,count2)
        for j in range(len(calc)):
            sum1=sum1+calc[j]
            count2=count2+1
            print(sum1)
            print("count1",count1)
            print("count2",count2)
            print(j)
            print("temp3",temp3)

            if(sum1>=SW_global.max_limit):
                if(count1==count2):
                    print("check point 11111")
                    temp5.append(temp3[count1])
                    sum1=0
                    count1=count2+1
                elif(count1<count2):
                    print("check point112233")
                    temp4.clear()
                    for k2 in range(count1,count2):
                        temp4.extend(temp3[k2])
                    sum1=0
                    temp5.append(temp4.copy())
                    temp4.clear()
                    count1=count2
            if((j==len(calc)-1)):
                print("I am in end point")
                print(count1)
                print(count2)
                if(count1<count2):
                    print("check point 111123455")
                    for k2 in range(count1,count2):
                        temp4.extend(temp3[k2])
                    sum1=0
                    temp5.append(temp4.copy())
                    temp4.clear()
                    count1=count2
                elif(count1==count2):
                    print("check point 11111")
                    temp5.append(temp3[count1])
                    sum1=0
                    count1=count2
                #else:
                elif(count1>count2):
                    temp5.append(temp3[j])

        print("temp5",temp5)

        count1=0
        count2=-1
        temp10=[]
        sum1=0

        for j in range(len(calc)):
            count2=j
            sum1=sum1+calc[j]
            if(calc[j]>SW_global.max_limit):
                if(count1<count2):
                    temp4.clear()
                    for k1 in range(count1,count2):
                        temp4.extend(temp3[k1])
                    temp10.append(temp4.copy())
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
                elif(count1==count2):
                    temp4.clear()
#                    for k1 in range(count1,count2):
#                        temp4.extend(temp3[k1])
#                    temp10.append(temp4.copy())
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()

            elif(sum1>SW_global.max_limit):
                temp4.clear()
                if(count1<count2):
                    for k1 in range(count1,count2):
                        temp4.extend(temp3[k1])
                    temp10.append(temp4.copy())
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
                elif(count1==count2):
                    temp4.clear()
#                    for k1 in range(count1,count2):
#                        temp4.extend(temp3[k1])
#                    temp10.append(temp4.copy())
                    temp10.append(temp3[count2].copy())
                    sum1=0
                    count1=count2+1
                    temp4.clear()
            elif((j==len(calc)-1) and (sum1<SW_global.max_limit)):
                for k1 in range(count1,count2):
                    temp4.extend(temp3[k1])
                temp10.append(temp4.copy())
                temp10.append(temp3[count2].copy())
                sum1=0
                count1=count2+1
                temp4.clear()
        print("This is temp 10", temp10)
        temp11=[]
        for j in temp10:
            if(len(j)!=0):
                temp11.append(j.copy())







        #check_sum_of_digit_advanced(array_value=None,key_axes=None)

            
    return temp11.copy() #temp5.copy()


def save_data_to_axes_dict(kern_value1=None,delete_list1=None,recent_input_list1=None,cursor_pos1=None,cursor_data1=None,kern_list1=None,axes_key_index=None,letters_already_written1=None,lines1=None,axesdata=None):
    print("I am in savce data ")
    a=dict()
    print("Check point gamma ")

    if(letters_already_written1!=None):
        print("letter")
        a["letters_already_written"]=letters_already_written1.copy()
    if(delete_list1!=None):
        a["delete_list"]=delete_list1.copy()
    if(kern_value1!=None):
        a["kern_value_array"]=kern_value1.copy()
    if(lines1!=None):
        a["gval"]=lines1.copy()
        a["lines"]=lines1.copy()
    if(kern_list1!=None):
        a["kern_list"]=kern_list1.copy()
    if(cursor_pos1!=None):
        a["cursor_pos"]=cursor_pos1.copy()
    if(cursor_data1!=None):
        a["cursor_data"]=cursor_data1.copy()
    if(recent_input_list1!=None):
        a["recent_input_list"]=recent_input_list1.copy()
    a["compositedot_already_applied_array"]=[]
    a["startdot_already_applied_array"]=[]
    a["decisiondot_already_applied_array"]=[]
    a["connectdot_already_applied_array"]=[]
    if(axesdata!=None):
        a["axis_data"]=axesdata
    a["stoke_arrow_flag_pos"]=0
    a["decision_dot_flag_pos"]=0
    a["connect_dot_flag_pos"]=0
    a["startdot_flag_pos"]=0
    if(axes_key_index!=None):
        SW_global.axes_data[str(axes_key_index)]=a
    else:
        SW_global.axes_data[str(len(SW_global.axes_data))]=a
    print("check point alpha")



    return

#def check_sum_digit_for_guideLine(array_value=None):
#    return
#### need to update add operation 
#### need to update back space normal
#### need to update
def check_sum_of_digit_advanced(array_value=None,key_axes=None):
    if((array_value!=None) and (key_axes!=None)):
        print("This is in array value")
        print(array_value)
        print("This is key_axes",key_axes)
        count1=key_axes
        len1=len(SW_global.axes_data)
        for j in range(len(SW_global.axes_data)):
            if(key_axes<=j):
                while(len(SW_global.axes_data[str(j)]["lines"])>=4):
                    ((SW_global.axes_data[str(j)]["lines"])[len(SW_global.axes_data[str(j)]["lines"])-1]).set_visible(False)
                    del (SW_global.axes_data[str(j)]["lines"])[len(SW_global.axes_data[str(j)]["lines"])-1]

        while(len(guideline_axes[l].lines)>=4):
            (guideline_axes[l].lines[len(guideline_axes[l].lines)-1]).set_visible(False)
            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
        spec_axes=None
        for j in range(len(array_value)):
            if(count1<len1):
                print("check point1")
                spec_axes=SW_global.axes_data[str(count1)]["axis_data"]
                base_array=[]
                for k1 in range(4):
                    print(k1)
                    print("check point 11")
                    print(SW_global.axes_data[str(count1)]["gval"])
                    base_array.append((SW_global.axes_data[str(count1)]["gval"])[k1])
                print("check point 12")
                temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=array_value[j],spec_axes=spec_axes,baselines_objects_array=base_array)
                save_data_to_axes_dict(kern_value1=temp_kern_value1,delete_list1=temp_delete1,recent_input_list1=temp_recent1,cursor_pos1=temp_cursor_pos1,cursor_data1=temp_cursor_data1,axes_key_index=count1,
                    letters_already_written1=letters_already_written3,axesdata=SW_global.axes_data[str(count1)]["axis_data"],lines1=temp_guideline_axes1)
                count1=count1+1
            elif(count1==len1):
                print("check point 2")
                spec_axes=guideline_axes[l]
                base_array=[]
                for k1 in range(4):
                    base_array.append(SW_global.g_val.lines[k1])
                temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=array_value[j],spec_axes=spec_axes,baselines_objects_array=base_array)
                kern_value_array.clear()
                kern_value_array.extend(temp_kern_value1)
                SW_global.kern_list.clear()
                SW_global.kern_list.extend(temp_kern_list1)
                delete_list.clear()
                delete_list.extend(temp_delete1)
                SW_global.recent_input_list.clear()
                SW_global.recent_input_list.extend(temp_recent1)
                SW_global.cursor_pos.clear()
                SW_global.cursor_pos.extend(temp_cursor_pos1)
                SW_global.cursor_data.clear()
                SW_global.cursor_data.extend(temp_cursor_data1)
                SW_global.letters_already_written.clear()
                guideline_axes[l].lines.clear()
                guideline_axes[l].lines.extend(temp_guideline_axes1)
                count1=count1+1
            elif(count1>len1):
                print("check point 3")
                save_data_to_axes_dict(kern_value1=kern_value_array.copy(),delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list,cursor_pos1=SW_global.cursor_pos.copy(),cursor_data1=SW_global.cursor_data.copy(),axes_key_index=None,
                    letters_already_written1=SW_global.letters_already_written.copy(),axesdata=guideline_axes[l],lines1=guideline_axes[l].lines)
                newCreateGuideLine(1,None,None,None,None)
                base_array=[]
                spec_axes=guideline_axes[l]
                for k1 in range(4):
                    base_array.append(SW_global.g_val.lines[k1])
                    spec_axes=guideline_axes[l]
                temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=array_value[j],spec_axes=spec_axes,baselines_objects_array=base_array)
                kern_value_array.clear()
                kern_value_array.extend(temp_kern_value1)
                SW_global.kern_list.clear()
                SW_global.kern_list.extend(temp_kern_list1)
                delete_list.clear()
                delete_list.extend(temp_delete1)
                SW_global.recent_input_list.clear()
                SW_global.recent_input_list.extend(temp_recent1)
                SW_global.cursor_pos.clear()
                SW_global.cursor_pos.extend(temp_cursor_pos1)
                SW_global.cursor_data.clear()
                SW_global.cursor_data.extend(temp_cursor_data1)
                SW_global.letters_already_written.clear()
                guideline_axes[l].lines.clear()
                guideline_axes[l].lines.extend(temp_guideline_axes1)                












        # count1=key_axes
        # spec_axes=None
        # part1=None
        # len1=len(SW_global.axes_data)
        # print("This is len1",len1)
        # #for j in range(len(SW_global.axes_data)):
        # print("key_axes",key_axes)
        # #    print("10"*10,j)
        # #    (SW_global.axes_data[str(j)]["axis_data"]).set_visible(False)
        # for j in array_value:
        #     print("I am in advanced loop"*100)
        #     print(count1)
        #     print(len1)
        #     if(int(len1)<int(count1)):
        #         print("I am in part 3")
        #         save_data_to_axes_dict(kern_value1=kern_value_array.copy(),delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list.copy(),cursor_pos1=SW_global.cursor_pos.copy(),cursor_data1=SW_global.cursor_data.copy(),kern_list1=SW_global.kern_list.copy(),axes_key_index=None,
        #             letters_already_written1=SW_global.letters_already_written.copy(),lines1=guideline_axes[l].lines.copy(),axesdata=guideline_axes[l])
        #         newCreateGuideLine(1,None,None,None,None)
        #         spec_axes=guideline_axes[l]
        #         count1=count1+1
        #         part1=3
        #     elif(count1==len1):
        #         print("I am in part2")
        #         spec_axes=guideline_axes[l]
        #         count1=count1+1
        #         part1=2
        #     elif(int(count1)<int(len1)):
        #         print("I am in part 1")
        #         print("This is count1",count1)
        #         spec_axes=SW_global.axes_data[str(count1)]["axis_data"]
        #        # (SW_global.axes_data[str(count1)]["axis_data"]).set_visible(False)
        #         count1=count1+1
        #         part1=1

        #     temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=j,spec_axes=spec_axes,baselines_objects_array=None)
        #     if(part1==1):
        #         print("I am on part1")
        #         save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=count1,letters_already_written1=letters_already_written2,axesdata=spec_axes,lines1=temp_guideline_axes2,kern_list1=temp_kern_list)
        #     if(part1==2 or part1==3):
        #         print("I am on part2")
        #         kern_value_array.clear()
        #         for k10 in temp_kern_value:
        #             kern_value_array.append(k10)
        #         delete_list.clear()
        #         for k10 in temp_delete:
        #             delete_list.append(k10)
        #         SW_global.letters_already_written.clear()
        #         for k10 in letters_already_written2:
        #             SW_global.letters_already_written.append(k10)
        #         SW_global.cursor_pos.clear()
        #         for k10 in temp_cursor_pos:
        #             SW_global.cursor_pos.append(k10)
        #         SW_global.cursor_data.clear()
        #         for k10 in temp_cursor_data:
        #             SW_global.cursor_data.append(k10)
        #         SW_global.kern_list.clear()
        #         for k10 in temp_kern_list:
        #             SW_global.kern_list.append(k10)
        #         while(len(guideline_axes[l].lines)>=4):
        #             del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
        #         for k10 in temp_guideline_axes2:
        #             guideline_axes[l].lines.append(k10)
        fig.canvas.draw()
    return 


def check_sum_of_digit(array_value=None,key_axes=None):
    if((array_value!=None) and(key_axes!=None)):
        print(array_value)
        sum1=0
        count1=0
        k=[]
        temp=[]
        for j in range(len(array_value)):
            sum1=0
            count1=0
            temp1=[]
            for k1 in range(len(array_value[j])):
                if(array_value[j][k1]!=" "):
                    sum1=sum1+manuscript.x_max[array_value[j][k1]]
                if(array_value[j][k1]==" "):
                    sum1=sum1+300
                if(sum1>=SW_global.max_limit):
                    for k2 in range(count1,k1):
                        temp.append(array_value[j][k2])
                        sum1=sum1+300
                    count1=j+1
                    SW_global.final_array.append(temp)
                    temp.clear()
                    SW_global.calculation_array.append(sum1)
                    sum1=0
            if((sum1<=SW_global.max_limit) and(count1==0)):
                SW_global.final_array.append(array_value[j])
                sum1=sum1+(len(array_value)*300)
                SW_global.calculation_array.append(sum1)
            else:
                temp.clear()
                sum2=0
                for k1 in range(count1,len(array_value[j])-1):
                    temp.append(array_value[j][k1])
                    sum2=sum2+manuscript.x_max[array_value[j][k1]]
                    sum2=sum2+300
                SW_global.calculation_array.append(sum2)
                SW_global.final_array.append(temp)
        #print("This is final array")
        for j in range(len(SW_global.axes_data)):
            if(j>=key_axes):
                clear_digit_from_axes(axesdata=SW_global.axes_data[str(j)]["axis_data"])
                while(len(SW_global.axes_data[str(j)]["lines"])>=4):
                   #del (SW_global.axes_data[str(j)]["lines"])[len(SW_global.axes_data[str(j)]["lines"])-1]
                   ((SW_global.axes_data[str(j)]["lines"])[len(SW_global.axes_data[str(j)]["lines"])-1]).set_visible(False)
                   del (SW_global.axes_data[str(j)]["lines"])[len(SW_global.axes_data[str(j)]["lines"])-1]
                while(len(SW_global.axes_data[str(j)]["gval"])>=4):
                   #del (SW_global.axes_data[str(j)]["gval"])[len(SW_global.axes_data[str(j)]["gval"])-1]
                   ((SW_global.axes_data[str(j)]["lines"])[len(SW_global.axes_data[str(j)]["lines"])-1]).set_visible(False)
                   del (SW_global.axes_data[str(j)]["gval"])[len(SW_global.axes_data[str(j)]["gval"])-1]


                #SW_global.axes_data[str(j)]["kern_valur"]
        clear_digit_from_axes(axesdata=guideline_axes[l])
        delete_list.clear()
        kern_value_array.clear()
        kern_value_array.append(0)
        SW_global.kern_list.clear()
        SW_global.kern_list.append(0)
        SW_global.recent_input_list.clear()
        SW_global.cursor_data.clear()
        SW_global.cursor_pos.clear()
        SW_global.cursor_pos.append(0)
        while(len(guideline_axes[l].lines)>=4):
            #del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
            (guideline_axes[l].lines[len(guideline_axes[l].lines)-1]).set_visible(False)
            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]

        count_axes=key_axes
        count_for_select1=key_axes
        len1=len(SW_global.axes_data)
        #print("This is axes")
        #print(len1)
        part1=None
        prev_count=0


        for j in range(len(SW_global.final_array)):
            if((j+1)<=len(SW_global.final_array)-1):
               # print("check point 111")
                if(SW_global.calculation_array[j]+SW_global.calculation_array[j+1]<=SW_global.max_limit-3000):
                #    print("I am in loop111 if")
                    k=SW_global.final_array[j].copy()
                    for q1 in SW_global.final_array[j+1]:
                        k.append(q1)
                    j=j+1
                 #   print("loop22")
                    if(count_axes<len1):
                        prev_count=count_axes
                        spec_axes=SW_global.axes_data[str(count_axes)]["axis_data"]
                        count_axes=count_axes+1
                        part1=1
                    elif(count_axes==len1):
                        prev_count=count_axes
                        spec_axes=guideline_axes[l]
                        count_axes=count_axes+1
                        part1=2
                    elif(count_axes>len1):
                        prev_count=count_axes
                        count_axes=count_axes+1
                        save_data_to_axes_dict(kern_value1=kern_value_array.copy(),delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list.copy(),cursor_pos1=SW_global.cursor_pos.copy(),cursor_data1=SW_global.cursor_data.copy(),kern_list1=SW_global.kern_list.copy(),axes_key_index=None,letter_already_written1=SW_global.letters_already_written.copy(),lines1=guideline_axes[l].lines.copy(),axesdata=guideline_axes[l])
                        newCreateGuideLine(1,None,None,None,None)
                        spec_axes=guideline_axes[l]
                        part1=3
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=k,spec_axes=spec_axes,baselines_objects_array=None)
                    if(part1==1):
                        save_data_to_axes_dict(kern_list1=temp_kern_list,kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=count_axes,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(prev_count)]["axis_data"],lines1=temp_guideline_axes2)
                    if(part1==2 or part1==3):
                        kern_value_array.clear()
                        for k10 in temp_kern_value:
                            kern_value_array.append(k10)
                        delete_list.clear()
                        for k10 in temp_delete:
                            delete_list.append(k10)
                        SW_global.letters_already_written.clear()
                        for k10 in letters_already_written2:
                            SW_global.letters_already_written.append(k10)
                        SW_global.cursor_pos.clear()
                        for k10 in temp_cursor_pos:
                            SW_global.cursor_pos.append(k10)
                        SW_global.cursor_data.clear()
                        for k10 in temp_cursor_data:
                            SW_global.cursor_data.append(k10)
                        SW_global.kern_list.clear()
                        for k10 in temp_kern_list:
                            SW_global.kern_list.append(k10)
                        while(len(guideline_axes[l].lines)>=4):
                            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                        for k10 in temp_guideline_axes2:
                            guideline_axes[l].lines.append(k10)
                    #if(part1==3):



                else:
                    #print("check point 2")
                    #print("This is len1",len1)
                    if(count_axes<len1):
                        prev_count=count_axes
                        spec_axes=SW_global.axes_data[str(count_axes)]["axis_data"]
                        count_axes=count_axes+1
                        part1=1
                    elif(count_axes==len1):
                        prev_count=count_axes
                        spec_axes=guideline_axes[l]
                        count_axes=count_axes+1
                        part1=2
                    elif(count_axes>len1):
                        prev_count=count_axes
                        count_axes=count_axes+1
                        newCreateGuideLine(1,None,None,None,None)
                        spec_axes=guideline_axes[l]
                        part1=3
                    temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=SW_global.final_array[j],spec_axes=spec_axes,baselines_objects_array=None)
                    print("check point 11")
                    if(part1==1):
                    #    print("check point 111")
                    #    print("check point 000")
                    #    print("This is count_of_axes",count_axes)
                        try:
                            save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=count_axes,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(prev_count)]["axis_data"],lines1=temp_guideline_axes2)
                        except Exception as e:
                            print("This is exception ")
                            print(e)
                    if(part1==2 or part1==3):
                    #    print("check point112")
                        kern_value_array.clear()
                        for k10 in temp_kern_value:
                            kern_value_array.append(k10)
                        delete_list.clear()
                        for k10 in temp_delete:
                            delete_list.append(k10)
                        SW_global.letters_already_written.clear()
                        for k10 in letters_already_written2:
                            SW_global.letters_already_written.append(k10)
                        SW_global.cursor_pos.clear()
                        for k10 in temp_cursor_pos:
                            SW_global.cursor_pos.append(k10)
                        SW_global.cursor_data.clear()
                        for k10 in temp_cursor_data:
                            SW_global.cursor_data.append(k10)
                        SW_global.kern_list.clear()
                        for k10 in temp_kern_list:
                            SW_global.kern_list.append(k10)
                        while(len(guideline_axes[l].lines)>=4):
                            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                        for k10 in temp_guideline_axes2:
                            guideline_axes[l].lines.append(k10) 
                     #   print("check point 10")                   
            else:
               # print("check point3 ")
                if(count_axes<len1):
                    prev_count=count_axes
                    spec_axes=SW_global.axes_data[str(count_axes)]["axis_data"]
                    count_axes=count_axes+1
                    part1=1
                elif(count_axes==len1):
                    prev_count=count_axes
                    spec_axes=guideline_axes[l]
                    count_axes=count_axes+1
                    part1=2
                elif(count_axes>len1):
                    prev_count=count_axes
                    count_axes=count_axes+1
                    newCreateGuideLine(1,None,None,None,None)
                    spec_axes=guideline_axes[l]
                    part1=3
                temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=SW_global.final_array[j],spec_axes=spec_axes,baselines_objects_array=None)
                #print("check point 12")
                if(part1==1):
                    save_data_to_axes_dict(kern_value1=temp_kern_value,delete_list1=temp_delete,recent_input_list1=temp_recent,cursor_pos1=temp_cursor_pos,cursor_data1=temp_cursor_data,axes_key_index=count_axes,letters_already_written1=letters_already_written2,axesdata=SW_global.axes_data[str(prev_count)]["axis_data"],lines1=temp_guideline_axes2)
                if(part1==2 or part1==3):
                    kern_value_array.clear()
                    for k10 in temp_kern_value:
                        kern_value_array.append(k10)
                    delete_list.clear()
                    for k10 in temp_delete:
                        delete_list.append(k10)
                    SW_global.letters_already_written.clear()
                    for k10 in letters_already_written2:
                        SW_global.letters_already_written.append(k10)
                    SW_global.cursor_pos.clear()
                    for k10 in temp_cursor_pos:
                        SW_global.cursor_pos.append(k10)
                    SW_global.cursor_data.clear()
                    for k10 in temp_cursor_data:
                        SW_global.cursor_data.append(k10)
                    SW_global.kern_list.clear()
                    for k10 in temp_kern_list:
                        SW_global.kern_list.append(k10)
                    while(len(guideline_axes[l].lines)>=4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    for k10 in temp_guideline_axes2:
                        guideline_axes[l].lines.append(k10)
                    #SW_global.final_array.clear()
                    #SW_global.calculation_array.clear()
        fig.canvas.draw() 
     #   temp_kern_value,temp_kern_list,temp_delete,temp_recent,temp_cursor_data,temp_cursor_pos,letters_already_written2,temp_guideline_axes2=add_digit_in_axes(list_of_digit=SW_global.delete_list_divide[0],spec_axes=temp_axes_list[0],baselines_objects_array=None)

        print(SW_global.final_array)
        print(SW_global.calculation_array)
        SW_global.final_array.clear()
        SW_global.calculation_array.clear()




    return 

def current_pos_in_number_find(current_pos1=None,current_axes1=None):
    if((current_pos1!=None) and(current_axes1!=None)):
        print("check")
        if(current_axes1==guideline_axes[l]):
            for j in range(len(SW_global.cursor_pos)):
                if((len(SW_global.cursor_pos)-1>=j+1) and (SW_global.cursor_pos[j]<=SW_global.current_pos) and(SW_global.cursor_pos[j+1]>=SW_global.current_pos)):
                    SW_global.current_pos_in_number=j
                    break
                if((j==len(SW_global.cursor_pos)-1) and (SW_global.current_pos>=SW_global.cursor_pos[j])):
                    SW_global.current_pos_in_number=j
                    break
        else:
            for j in range(len(SW_global.axes_data)):
                print("I am in loop2")
                if(SW_global.axes_data[str(j)]["axis_data"]==current_axes1):
                    print("I am in loop3")
                    print(SW_global.axes_data[str(j)]["cursor_pos"])
                    for k in range(len(SW_global.axes_data[str(j)]["cursor_pos"])):
                        print("End of check   333")
                        if((len(SW_global.axes_data[str(j)]["cursor_pos"])-1>=k+1) and ((SW_global.axes_data[str(j)]["cursor_pos"])[k]<=SW_global.current_pos) and((SW_global.axes_data[str(j)]["cursor_pos"])[k+1]>=SW_global.current_pos)):
                            SW_global.current_pos_in_number=k
                            print(k)
                            print("cje")
                            break
                        if((k==len(SW_global.axes_data[str(j)]["cursor_pos"])-1) and(SW_global.current_pos>=(SW_global.axes_data[str(j)]["cursor_pos"])[k])):
                            SW_global.current_pos_in_number=k
                            print("cje1")
                            print(k)
                            break
    return

def reset_features_flag():
    stoke_arrow_flag_pos=0
    decision_dot_flag_pos=0
    connect_dot_flag_pos=0
    startdot_flag_pos=0
    return 

def reset_guide_line_delete_kern_value(delete_list1,temp_kern_value1):
    print("temp_kern_value1",temp_kern_value1)
    print("delete_list1",delete_list1)
    delete_list.clear()
    kern_value_array.clear()
    for j in delete_list1:
        delete_list.append(j)
    for j in temp_kern_value1:
        kern_value_array.append(j)

    #delete_list=delete_list1.copy()
    #kern_value_array=temp_kern_value1.copy()
    return

def clear_digit_from_axes(axesdata=None):
    if(axesdata!=None):
        if(axesdata==guideline_axes[l]):
            count=0
            for j in guideline_axes[l].lines:
                
                if(count>=4):
                    j.set_visible(False)
                count=count+1

        else:
            for j in range(len(SW_global.axes_data)):
                if(SW_global.axes_data[str(j)]["axis_data"]==axesdata):
                    count=0
                    for k1 in SW_global.axes_data[str(j)]["lines"]:
                        if(count>=4):
                            k1.set_visible(False)
                        count=count+1
        fig.canvas.draw()
    return 



def backspace_from_rear_side():
    try:
        print()
        
    except Exception as e:
        print(e)
        pass
    return 

def add_space_from_any_postion():

    return 



def cut_add_letter_from_any_position(delete_list1=None,current_axes=None,key=None):
    print("SW_global:",SW_global.current_pos_in_number)
    temp_count=key
    final_guideline=guideline_axes[l]
    print("This is delete_list send to fnction :",delete_list)
    print("This is current_axes:",current_axes)
    print("This is current key:",key)
    if((delete_list1!=None) and (current_axes!=None)):
        if(key<1000):
            guideline_axes[l]=SW_global.axes_data[str(key)]["axis_data"]
        elif(key==10000):
            guideline_axes[l]=guideline_axes[l]
        try:
            for j in range(len(delete_list1)):
                if(SW_global.kern_list[0]>15000):
                    if((temp_count<1000) and (len(SW_global.axes_data)>temp_count)):
                        SW_global.axes_data[str(temp_count)]["letters_already_written"]=[i for i in  SW_global.letters_already_written]
                        SW_global.axes_data[str(temp_count)]["kern_value_array"]=[i for i in kern_value_array]
                        SW_global.axes_data[str(temp_count)]["delete_list"]=[i for i in delete_list]
                        SW_global.axes_data[str(temp_count)]["kern_list"]=[i for i in SW_global.kern_list]
                        SW_global.axes_data[str(temp_count)]["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
                        SW_global.axes_data[str(temp_count)]["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
                        SW_global.axes_data[str(temp_count)]["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
                        SW_global.axes_data[str(temp_count)]["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
                        SW_global.axes_data[str(temp_count)]["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
                        SW_global.axes_data[str(temp_count)]["startdot_flag_pos"]=startdot_flag_pos
                        SW_global.axes_data[str(temp_count)]["decision_dot_flag_pos"]=decision_dot_flag_pos
                        SW_global.axes_data[str(temp_count)]["connect_dot_flag_pos"]=connect_dot_flag_pos
                        SW_global.axes_data[str(temp_count)]["lines"]=[i for i in guideline_axes[l].lines]
                        SW_global.axes_data[str(temp_count)]["gval"]=[i for i in SW_global.g_val.lines]
                        SW_global.axes_data[str(temp_count)]["cursor_pos"]=[i for i in SW_global.cursor_pos]
                        SW_global.axes_data[str(temp_count)]["cursor_data"]=[i for i in SW_global.cursor_data]

                        if((temp_count)>=len(SW_global.axes_data)):
                            temp_count=10000
                            guideline_axes[l]=final_guideline
                        else:
                            temp_count=temp_count+1
                    elif(temp_count==10000):
                        a=dict()
                        #print("check point altra")
                        a["letters_already_written"]=[i for i in  SW_global.letters_already_written]
                        a["kern_value_array"]=[i for i in kern_value_array]
                        a["delete_list"]=[i for i in delete_list]
                        a["kern_list"]=[i for i in SW_global.kern_list]
                        a["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
                        a["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
                        a["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
                        a["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
                        a["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
                        a["startdot_flag_pos"]=startdot_flag_pos
                        a["decision_dot_flag_pos"]=decision_dot_flag_pos
                        a["connect_dot_flag_pos"]=connect_dot_flag_pos
                        a["axis_data"]=guideline_axes[l]
                        #print("This is guide line axes .lines",len(guideline_axes[l].lines))
                        a["lines"]=[i for i in guideline_axes[l].lines]
                        #print("This is check point 3")
                        a["gval"]=[i for i in SW_global.g_val.lines]
                        a["cursor_pos"]=[i for i in SW_global.cursor_pos]
                        a["cursor_data"]=[i for i in SW_global.cursor_data]
                        SW_global.cursor_pos.clear()
                        SW_global.cursor_data.clear()
                        SW_global.cursor_pos.insert(0,0)
                        SW_global.axes_data[str(len(SW_global.axes_data))]=a
                        newCreateGuideLine(1,None,None,None,None)
                        SW_global.cursor_pos.clear()
                        SW_global.cursor_data.clear()
                        SW_global.cursor_pos.insert(0,0)
                        kern_value_array.clear()
                        SW_global.kern_list.clear()
                        SW_global.letters_already_written.clear()
                        SW_global.letters_already_written.clear()
                        SW_global.kern_list.insert(0,0)
                        SW_global.kern_value_array.clear()
                        SW_global.kern_value_array.insert(0,0)
                        kern_value_array.clear()
                        kern_value_array.insert(0,0)
                        compositedot_already_applied_array.clear()
                        startdot_already_applied_array.clear()
                        decisiondot_already_applied_array.clear()
                        connectdot_already_applied_array.clear()
                        stoke_arrow_flag_pos=0
                        startdot_flag_pos=0
                        delete_list.clear()
                        decision_dot_flag_pos=0
                        connect_dot_flag_pos=0
                length12 = len(SW_global.recent_input_list)
                user_input = delete_list1[j]
                print("This is main user input :",user_input)
                x_max = manuscript.x_max[user_input]
                kern_x = SW_global.kern_list[0]
                if color_letter_features_on_off:
                    if user_input in skip_list:
                        c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    else:
                        x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                        c1,c2=font_check(x,y)
                else:
                    if user_input in skip_list:
                        c1, c2 = manuscript.return_manuscript_fonts(user_input)
                    else:
                        x,y=manuscript.return_manuscript_fonts(user_input)
                        c1,c2=font_check(x,y)

                c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)
                kern_x = SW_global.kern_list[0] + x_max + 300
                SW_global.kern_list.insert(0, kern_x)
                kern_counter = len(kern_value_array)
                kern_value_array.insert(kern_counter, kern_x)
                #print(kern_value_array)
                SW_global.recent_input_list.insert(length12, user_input)
                #print("this is list")
                delete_list.insert(length12,user_input)
                #print(delete_list)
                init_enrty_pos = len(SW_global.letters_already_written)
                inti_letter_pos = len(guideline_axes[l].lines)
                #print("This is guide line axes length ")
                #print(len(guideline_axes[l].lines))
                SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
                #print(SW_global.letters_already_written)
                if draw_type_color_letter == 1:
                    if letter_dot_density_no_dot_on_off == 1:
                        alp = 0
                    else:
                        alp = temp_alp
                    if color_letter_features_on_off:
                        guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    else:
                        guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

                else:
                    n = len(c1)
                    if letter_dot_density_no_dot_on_off == 1:
                        alp = 0
                    else:
                        alp = temp_alp
                    if color_letter_features_on_off:
                        for i in range(n):
                            if i == 0:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i == 1:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i == 2:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            if i == 3:
                                guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    else:
                        for i in range(n):
                            guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                #############################   Cursor part code of inserting ###############################
                import numpy as np
                item_cursor=kern_x-300
                cursor_y=list(np.linspace(-900,1500,500))
                #cursor_y_neg=list(np.lenspace)
                cursor_x=list(np.full((500),item_cursor))
                SW_global.cursor_pos.append(item_cursor)
                cursor_x1=list(np.full((500),item_cursor))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
                plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                SW_global.single_click_data=plot_data[0]
                plot_data[0].set_visible(False)
                ##### Add new two variable for current axes and current pos #####
                k=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))

                #print(k)
                #print(k)
                for i in k:
                    SW_global.cursor_data.append(i)
                    i.set_visible(False)

                #SW_global.cursor_data.append(k)
                #print(SW_global.cursor_data)
                for cur_count in range(len(SW_global.cursor_data)-1):
                    invisible_item=SW_global.cursor_data[cur_count]
                    invisible_item.set_visible(False)
                fig.canvas.draw()
                #print(guideline_axes[0].lines)

        # -----------------------------------------------------------------------------------------------------
                final_enrty_pos = len(SW_global.letters_already_written)
                final_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
                features_checking_function()
        except Exception as e:
            pass

        fig.canvas.draw()
        if(temp_count==10000):
            print("This is SW_global ",SW_global.current_pos_in_number)

            SW_global.single_click_data=SW_global.cursor_data[SW_global.current_pos_in_number-1]
            SW_global.single_click_data.set_visible(True)
            #SW_global.current_pos=SW_global.cursor_pos[]
            SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number]
            print(SW_global.current_pos)
            print("It is ok")
            #SW_global.single_click_cursor_pos.set_visible(True)
            fig.canvas.draw()
            print("Kern_value_array:",kern_value_array)
            print("DElete_list:",delete_list)
            return delete_list1,kern_value_array
        elif(len(SW_global.axes_data)-1<=temp_count):
            print("ok")

            return delete_list1,kern_value_array

    return



# def main_back_space_controller_for_text_flow_features():


#     return






def cut_addletter(user_input):
    try:
        print("This is cut addletter")
        #print(delete_list)
        print(SW_global.kern_list)
        length12 = len(SW_global.recent_input_list)
        x_max = manuscript.x_max[user_input]
        kern_x = SW_global.kern_list[0]
        #delete_list.append(user_input)
        if color_letter_features_on_off:
            if user_input in skip_list:
                c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
            else:
                x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                c1,c2=font_check(x,y)
        else:
            if user_input in skip_list:
                c1, c2 = manuscript.return_manuscript_fonts(user_input)
            else:
                x,y=manuscript.return_manuscript_fonts(user_input)
                c1,c2=font_check(x,y)
        c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)
        kern_x = SW_global.kern_list[0] + x_max + 300
        SW_global.kern_list.insert(0, kern_x)
        kern_counter = len(kern_value_array)
        kern_value_array.insert(kern_counter, kern_x)
        SW_global.recent_input_list.insert(length12, user_input)
        init_enrty_pos = len(SW_global.letters_already_written)
        inti_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
        if draw_type_color_letter == 1:
            if letter_dot_density_no_dot_on_off == 1:
                alp = 0
            else:
                alp = temp_alp
            if color_letter_features_on_off:
                guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
            else:
                guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

        else:
            n = len(c1)
            if letter_dot_density_no_dot_on_off == 1:
                alp = 0
            else:
                alp = temp_alp
            if color_letter_features_on_off:
                for i in range(n):
                    if i == 0:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    if i == 1:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    if i == 2:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    if i == 3:
                        guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
            else:
                for i in range(n):
                    guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

        import numpy as np
        if(len(SW_global.cursor_data)!=0):
            print("It is ok")
        else:
            print("It is empty")
        item_cursor=kern_x-300
        cursor_y=list(np.linspace(-900,1500,500))
        #cursor_y_neg=list(np.lenspace)
        cursor_x=list(np.full((500),item_cursor))
        SW_global.cursor_pos.append(item_cursor)

        k=guideline_axes[l].plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
        for i in k:
            SW_global.cursor_data.append(i)
        for cur_count in range(len(SW_global.cursor_data)-1):
            invisible_item=SW_global.cursor_data[cur_count]
            invisible_item.set_visible(False)
        final_enrty_pos = len(SW_global.letters_already_written)
        final_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
        print(SW_global.kern_list)
        print("This is from add function")
        print(delete_list)

    except Exception as e:
        print(e)


############################## Multiple guide line function newCreateGuideLine() ####################
po=0
def font_change_automation(sl_b1=None,sl_b2=None):
    try:
        SW_global.entire_delete_list_for_one_page.clear()
        if(len(SW_global.axes_data)>0):
            for j in range(len(SW_global.axes_data)):
                for k1 in SW_global.axes_data[str(j)]["delete_list"]:
                    SW_global.entire_delete_list_for_one_page.append(k1)
                (SW_global.axes_data[str(j)]["axis_data"]).set_visible(False)
            for k1 in delete_list:
                SW_global.entire_delete_list_for_one_page.append(k1)
        reset_after()



    except Exception as e:
        pass 
    return 

global back_axes
def reset_main_selector1():

    SW_global.mainselector_value=widgets.RectangleSelector(SW_global.back_axes, onselect,
                                         drawtype='box', interactive=True,
                                         spancoords='pixels', minspany=110, maxdist=50, button=1,
                                         rectprops=dict(facecolor='white', linestyle='--',
                                                        edgecolor='yellow', alpha=0.45, fill=True))
    SW_global.mainselector_value.extents=(1,0,0,1)
    SW_global.mainselector_value.set_visible(True)
    fig.canvas.draw()
    #mainselector.extents=(1, 0, 0, 1)
    return

def new_create_text_box(n,shift_no):
    global gl, gb, sl_t, sl_b, l,key_c, l
    print("This is himalata checking ",sl_b,SW_global.scl)
    height_axes=((0.15*100*SW_global.count_for_height)/100) 
    #### staic for first then we have to use dynamic
    print("This is height axes")
    print(height_axes)
   # if(SW_global.count_for_height==0):
   #     SW_global.count_for_height=1
    SW_global.count_for_height=SW_global.count_for_height+1
    #if(height_axes==0.0):
    #    height_axes=0.15
    s = n / 100
    old_l = (0 + s)
    sl = (gb - s)
    old_b = (l + sl) #for position change of axes change in old_b which value within 1-0 because position for canvas is 1-0 old_b-0.15
    print("This is from newCreateGuideLine")
    print(guideline_axes[l])
    print("This is sw_global.gval")
    try:
        print("This is before update")
        print(SW_global.g_val)
        print(guideline_axes[l])
        print("This is end")
    except Exception as e:
        print(e)
        pass
    SW_global.back_axes=None

    if(SW_global.back_axes==None):
        SW_global.back_axes=plt.axes([old_l, old_b-height_axes, 0.98, 0.156],frameon=True)
        SW_global.back_axes.set_xticks([])
        SW_global.back_axes.set_yticks([])
        SW_global.back_axes.spines["bottom"].set_linestyle('dashed')
        SW_global.back_axes.spines["bottom"].set_capstyle("butt")
        SW_global.back_axes.spines["top"].set_linestyle('dashed')
        SW_global.back_axes.spines["top"].set_capstyle("butt")
        SW_global.back_axes.spines["left"].set_linestyle('dashed')
        SW_global.back_axes.spines["left"].set_capstyle("butt") 
        SW_global.back_axes.spines["right"].set_linestyle('dashed')
        SW_global.back_axes.spines["right"].set_capstyle("butt") 
        #reset_main_selector1(mainselector)

        #SW_global.back_axes.spines["right"].set_edgecolor("red")

        # SW_global.back_axes.get_frame().set_width(10.0)
    else:
        print("*"*200)
        SW_global.back_axes.set_position([old_l, old_b-height_axes, 0.98, 0.156*SW_global.count_for_height])
        print("*"*200)



    

    guideline_axes[l] = plt.axes([old_l-(0.0001*shift_no), old_b-height_axes, 0.98, 0.15])
    guideline_axes[l].set_xticks([])
    guideline_axes[l].set_yticks([])
    SW_global.g_val=guideline_axes[l]

    print("This is from guide")
    print(guideline_axes[l].lines)
    print("This is new sw global ")
    try:
        print(SW_global.g_val)
        print(guideline_axes[l])
        print("This is end")
    except Exception as e:
        print(e)
        pass


    #print(guideline_axes[l])
    print(guideline_axes[l])
    img = plt.imread('icons/guideline.PNG')
    print(old_l)
    print(old_b)
    guideline_axes[l].imshow(img, extent=[0.0004, 0.0005, 0.0006, 0.002])
    guideline_axes[l].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off',
                                      right='off', left='off', labelleft='off')
   # guideline_axes[l].add_patch(patches.Rectangle((776820, 5000),3000,3500,fill=False,zorder=2,closed=True,alpha=alp))
    guideline_axes[l].set_xticks([])
    guideline_axes[l].set_yticks([])
    print("This is cornner points ",dir(mainselector))
    print("This corner",mainselector.edge_centers)
    print(mainselector.center)
    print(mainselector.corners)
    #plt.plot()
    mainselector.rectprops=dict(facecolor='white', linestyle='--',
                                                        edgecolor='yellow', alpha=0.45, fill=True)
    mainselector.update()
    fig.canvas.draw()

    for ln in ['top', 'right', 'left', 'bottom']:
        guideline_axes[l].spines[ln].set_linewidth(0)

    default_guideline(guideline_axes[l])

    print("This is after guide line")
    print(SW_global.g_val.lines)
    print(guideline_axes[l].lines)
    print("This is end")

    SW_global.left = 0.99
    SW_global.right = 0.01
    ### for size changing#####
    SW_global.top = sl_t
    SW_global.bottom = sl_b-height_axes #-0.15 # (x0,yo,width,height) # change in SW_global.buttom for height change in selector sl_b-0.15
    mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
    for j in range(len(SW_global.axes_data)):
        print((SW_global.axes_data[str(j)]["axis_data"]).get_position())
    print("This is data",guideline_axes[l].get_position())
    fig.canvas.draw()
    return

#### have to add an back axes  #######  


#### same need to change #####

def newCreateGuideLine(n,a,b,c,d):
    global gl, gb, sl_t, sl_b, l,key_c, l
    print("This is himalata checking ",sl_b,SW_global.scl)
    height_axes=((0.15*100*SW_global.count_for_height)/100) 

    #### staic for first then we have to use dynamic
    print("This is height axes")
    print(height_axes)
   # if(SW_global.count_for_height==0):
   #     SW_global.count_for_height=1
    SW_global.count_for_height=SW_global.count_for_height+1
    #if(height_axes==0.0):
    #    height_axes=0.15
    s = n / 100
    old_l = (0 + s)
    sl = (gb - s)
    old_b = (l + sl) #for position change of axes change in old_b which value within 1-0 because position for canvas is 1-0 old_b-0.15
    print("This is from newCreateGuideLine")
    print(guideline_axes[l])
    print("This is sw_global.gval")
    try:
        print("This is before update")
        print(SW_global.g_val)
        print(guideline_axes[l])
        print("This is end")
    except Exception as e:
        print(e)
        pass
    if(SW_global.back_axes==None):
        SW_global.back_axes=plt.axes([old_l, old_b-height_axes, 0.98, 0.156],frameon=True)
        SW_global.back_axes.set_xticks([])
        SW_global.back_axes.set_yticks([])
        SW_global.back_axes.spines["bottom"].set_linestyle('dashed')
        SW_global.back_axes.spines["bottom"].set_capstyle("butt")
        SW_global.back_axes.spines["top"].set_linestyle('dashed')
        SW_global.back_axes.spines["top"].set_capstyle("butt")
        SW_global.back_axes.spines["left"].set_linestyle('dashed')
        SW_global.back_axes.spines["left"].set_capstyle("butt") 
        SW_global.back_axes.spines["right"].set_linestyle('dashed')
        SW_global.back_axes.spines["right"].set_capstyle("butt")       
        #SW_global.back_axes.spines["right"].set_edgecolor("red")

        # SW_global.back_axes.get_frame().set_width(10.0)
    else:
        print("*"*200)
        SW_global.back_axes.set_position([old_l, old_b-height_axes, 0.98, 0.156*SW_global.count_for_height])
        print("*"*200)
    pos11=None

    if(guideline_axes[l]!=None):
        pos11=guideline_axes[l].get_position()
    

    import random

    if(pos11!=None):
        guideline_axes[l]=plt.axes([pos11.x0, pos11.y0-0.15-(random.random()/100000), 0.98, 0.15])
    else:
        guideline_axes[l] = plt.axes([old_l, old_b-height_axes, 0.98, 0.15])
    guideline_axes[l].set_xticks([])
    guideline_axes[l].set_yticks([])
    SW_global.g_val=guideline_axes[l]
    print("This is from guide")
    print(guideline_axes[l].lines)
    print("This is new sw global ")
    try:
        print(SW_global.g_val)
        print(guideline_axes[l])
        print("This is end")
    except Exception as e:
        print(e)
        pass


    #print(guideline_axes[l])
    print(guideline_axes[l])
    img = plt.imread('icons/guideline.PNG')
    print(old_l)
    print(old_b)
    guideline_axes[l].imshow(img, extent=[0.0004, 0.0005, 0.0006, 0.002])
    guideline_axes[l].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off',
                                      right='off', left='off', labelleft='off')
   # guideline_axes[l].add_patch(patches.Rectangle((776820, 5000),3000,3500,fill=False,zorder=2,closed=True,alpha=alp))
    guideline_axes[l].set_xticks([])
    guideline_axes[l].set_yticks([])
    print("This is cornner points ",dir(mainselector))
    print("This corner",mainselector.edge_centers)
    print(mainselector.center)
    print(mainselector.corners)
    #plt.plot()
    #mainselector.rectprops=dict(facecolor='white', linestyle='--',
     #                                                   edgecolor='yellow', alpha=0.45, fill=True)
    mainselector.update()
    fig.canvas.draw()

    for ln in ['top', 'right', 'left', 'bottom']:
        guideline_axes[l].spines[ln].set_linewidth(0)

    default_guideline(guideline_axes[l])

    print("This is after guide line")
    print(SW_global.g_val.lines)
    print(guideline_axes[l].lines)
    print("This is end")

    SW_global.left = 0.99
    SW_global.right = 0.01
    ### for size changing#####
    SW_global.top = sl_t
    SW_global.bottom = sl_b-height_axes #-0.15 # (x0,yo,width,height) # change in SW_global.buttom for height change in selector sl_b-0.15
    #mainselector.set_visible(False)
    #reset_main_selector()
    #mainselector.set_visible(False)
    mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
    for j in range(len(SW_global.axes_data)):
        print((SW_global.axes_data[str(j)]["axis_data"]).get_position())
    print("This is data",guideline_axes[l].get_position())
    fig.canvas.draw()
    return

def reset_main_selector():
    # mainselector=widgets.RectangleSelector(fig_axes, onselect,
    #                                      drawtype='box', interactive=True,
    #                                      spancoords='pixels', minspany=110, maxdist=50, button=1,
    #                                      rectprops=dict(facecolor='white', linestyle='--',
    #                                                     edgecolor='yellow', alpha=0.45, fill=True))
    mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
    mainselector.set_visible(True)
    #mainselector.update()
    return


# def newCreateGuideLine(n,a,b,c,d):
#     global gl, gb, sl_t, sl_b, l,key_c, l
#     print("This is himalata checking ",sl_b,SW_global.scl)
#     height_axes=((0.15*100*SW_global.count_for_height)/100) 
#     #### staic for first then we have to use dynamic
#     print("This is height axes")
#     print(height_axes)
#    # if(SW_global.count_for_height==0):
#    #     SW_global.count_for_height=1
#     SW_global.count_for_height=SW_global.count_for_height+1
#     #if(height_axes==0.0):
#     #    height_axes=0.15
#     s = n / 100
#     old_l = (0 + s)
#     sl = (gb - s)
#     old_b = (l + sl) #for position change of axes change in old_b which value within 1-0 because position for canvas is 1-0 old_b-0.15
#     print("This is from newCreateGuideLine")
#     print(guideline_axes[l])
#     print("This is sw_global.gval")
#     try:
#         print("This is before update")
#         print(SW_global.g_val)
#         print(guideline_axes[l])
#         print("This is end")
#     except Exception as e:
#         print(e)
#         pass


#     # k5=plt.axes([old_l, old_b-height_axes, 0.96, 0.17])
#     # k1=list(np.linspace(-900,1500,500))
#     # k2=list(np.linspace(-900,1500,500))
#     # k3=list(np.full((500),0))
#     # k4=list(np.full((500),1500))
#     # k5.plot(k1,k3,linewidth=0.7, dashes=(d1, d2), alpha=alp)
#     # k5.plot(k2,k3)
#     # k5.set_xticks([])
#     # k5.set_yticks([])
#     # SW_global.back_axes=plt.axes([old_l, old_b-height_axes, 0.99, 0.17])
#     # SW_global.back_axes.set_xticks([])
#     # SW_global.back_axes.set_yticks([])
#     # SW_global.back_axes.spines['bottom'].set_color('#dddddd')
#     # SW_global.back_axes.spines['top'].set_color('#dddddd')
#     # SW_global.back_axes.spines['left'].set_color('#dddddd')
#     # SW_global.back_axes.spines['right'].set_color('#dddddd')
#     # k5.grid(color='r', linestyle='-', linewidth=2)
#     # k5.spines['bottom'].set_color('#dddddd')
#     # k5.spines['left'].set_color('#dddddd')
#     # k5.spines['right'].set_color('#dddddd')
#     # k5.spines['top'].set_color('#dddddd')
#     # print(k5.spines)
#     # k5.set_xticks([])
#     # k5.set_yticks([])
#     guideline_axes[l] = plt.axes([old_l, old_b-height_axes, 0.98, 0.15])
#    # border = Rectangle((20, 30), 10000, 2000, fill=False, color='k', linewidth=1, clip_on=False)
#    # guideline_axes[l].add_artist(border)

#     guideline_axes[l].set_xticks([])
#     guideline_axes[l].set_yticks([])
#     SW_global.g_val=guideline_axes[l]
#     print("This is from guide")
#     print(guideline_axes[l].lines)
#     print("This is new sw global ")
#     try:
#         print(SW_global.g_val)
#         print(guideline_axes[l])
#         print("This is end")
#     except Exception as e:
#         print(e)
#         pass


#     #print(guideline_axes[l])
#     print(guideline_axes[l])
#     img = plt.imread('icons/guideline.PNG')
#     print(old_l)
#     print(old_b)
#     guideline_axes[l].imshow(img, extent=[0.0004, 0.0005, 0.0006, 0.002])
#     guideline_axes[l].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off',
#                                       right='off', left='off', labelleft='off')
#    # guideline_axes[l].add_patch(patches.Rectangle((776820, 5000),3000,3500,fill=False,zorder=2,closed=True,alpha=alp))
#     guideline_axes[l].set_xticks([])
#     guideline_axes[l].set_yticks([])
#     print("This is cornner points ",dir(mainselector))
#     print("This corner",mainselector.edge_centers)
#     print(mainselector.center)
#     print(mainselector.corners)
#     #plt.plot()
#     mainselector.rectprops=dict(facecolor='white', linestyle='--',
#                                                         edgecolor='yellow', alpha=0.45, fill=True)
#     mainselector.update()
#     fig.canvas.draw()

#     for ln in ['top', 'right', 'left', 'bottom']:
#         guideline_axes[l].spines[ln].set_linewidth(0)

#     default_guideline(guideline_axes[l])

#     print("This is after guide line")
#     print(SW_global.g_val.lines)
#     print(guideline_axes[l].lines)
#     print("This is end")

#     SW_global.left = 0.99
#     SW_global.right = 0.01
#     ### for size changing#####
#     SW_global.top = sl_t
#     k55=guideline_axes[l].get_position()
#     print(dir(k55))
#     print(k55.x0)
#     print(k55.x1)
#     print(k55.y0)
#     print(k55.y1)
#     print("This is end")
#     starting_point_x=None
#     starting_point_y=None
#     ending_point_x=None
#     starting_point_y=None
#     if(len(SW_global.axes_data)>0):
#         #SW_global.axes_data[str(0)]["axis_data"]
#         starting_point=(SW_global.axes_data[str(0)]["axis_data"]).get_position()
#         starting_point_x=starting_point.x0
#         starting_point_y=starting_point.y0
#         end_point_x=(guideline_axes[l].get_position()).x1
#         end_point_y=(guideline_axes[l].get_position()).y1
#     else:
#         starting_point_x=((guideline_axes[l]).get_position()).x0
#         starting_point_y=((guideline_axes[l]).get_position()).y0
#         ending_point_x=((guideline_axes[l]).get_position()).x1
#         ending_point_y=((guideline_axes[l]).get_position()).y1
#     print(starting_point_x)
#     print(starting_point_y)
#     print(ending_point_x)
#     print(ending_point_y)
#     length13=abs(starting_point_x-ending_point_x)
#     length113=abs(starting_point_y-ending_point_y)


#     SW_global.bottom = sl_b-height_axes  #-0.15 # (x0,yo,width,height) # change in SW_global.buttom for height change in selector sl_b-0.15
#     mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
#     if(SW_global.back_axes!=None):
#         SW_global.back_axes.set_position([starting_point_x,starting_point_y,length13, length113])
#     for j in range(len(SW_global.axes_data)):
#         print((SW_global.axes_data[str(j)]["axis_data"]).get_position())
#     print("This is data",guideline_axes[l].get_position())
#     fig.canvas.draw()
#     return




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Press Function <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def press(event):
    print("I am in")
    print("I am from press"*20)
    print("This is axes_data",SW_global.axes_data)
    print("This is cursor pos",SW_global.cursor_pos)
    print("This is cursor data",SW_global.cursor_data)
    print("This is kern_value_array",kern_value_array)
    print("This is kern_list",SW_global.kern_list)
    print("This is guideline_axes[l].lines",guideline_axes[l].lines)
    print("*"*200)
    try:
        if(SW_global.single_click_data!=None):
            SW_global.single_click_data.set_visible(False)
    except Exception as e:
        pass 

    try:
        print("This is temp_cursor_temp_data")
        item=SW_global.temp_cursor_temp_data[0]
        item.set_visible(False)
        #SW_global.temp_cursor_temp_data.set_visible(False)
    except Exception as e:
        pass
    print("This is from press")
    print(SW_global.letters_already_written)
    print(SW_global.kern_value_array)
    print(kern_value_array)
    print(compositedot_already_applied_array)

    global init_letter_pos, final_letter_pos, startdot_flag_pos
    global stoke_arrow_flag_pos, connect_dot_flag_pos, decision_dot_flag_pos
    global letter_out_line_flag_pos, letter_out_line_on_off
    global tb_height, kern_x, x_pts, y_pts
    global lft_gd, rht_gd, btm_gd, tp_gd
    global letter_shadding_on_off
    global color_letter_features_on_off, color_letter_flag_pos
    global d1, d2, letter_dot_density_no_dot_on_off, alp, temp_alp
    global k12



    if(event.key=='ctrl+c'):
       # k12=sd
        print("I got cut *********************************")
        print(SW_global.copy_string)
        k_copy=SW_global.copy_string
        import pyperclip
        pyperclip.copy(k_copy)
        print(k_copy)
        SW_global.copy_string=""
    if(event.key=='ctrl+v'):
        print(pos2i)
        print(SW_global.click_x)
        print(SW_global.release_x)
        print(pos1i)
        print("i am in ctrl+v")
        pos4=-1
        paste_on_axes()
        # print(delete_list)
        # if(int(SW_global.click_x)==int(SW_global.release_x)):
        #     if(SW_global.click_x==0):
        #         pos4=0
        #     else:
        #         for i in range(len(SW_global.cursor_pos)):
        #             if((SW_global.cursor_pos[i]>SW_global.click_x)):
        #                 pos4=i
        #                 break
        #     print(pos4)

        #     if(pos4==-1):
        #         pos4=len(SW_global.cursor_pos)-1
        #     else:
        #         pos4=pos4-1
        #     print(pos4)
        #     import pyperclip
        #     k1=list(pyperclip.paste())
        #     print(len(k1))
        #     delete_list11=[]
        #     delete_list22=[]
        #     for i in delete_list:
        #         delete_list22.append(i)
        #     if(len(k1)>0):
        #         print("I got paste with greater zero length")
        #         for i in k1:
        #             delete_list22.insert(pos4,i)
        #             pos4=pos4+1
        #         print(delete_list22)
        #         for i in range(len(SW_global.g_val.lines)):
        #             if(i>3):
        #                 item=SW_global.g_val.lines[i]
        #                 item.set_visible(False)
        #         fig.canvas.draw()

        #         print("This is delete list")
        #         print(delete_list22)
        #         SW_global.letters_already_written.clear()
        #         SW_global.kern_list.insert(0,0)
        #         SW_global.kern_list.insert(0,0)
        #         SW_global.cursor_pos=[0]
        #         SW_global.cursor_data=[]
        #         SW_global.kern_value_array.clear()
        #         SW_global.kern_value_array.insert(0,0)
        #         kern_value_array.clear()
        #         kern_value_array.insert(0,0)
        #         compositedot_already_applied_array.clear()
        #         startdot_already_applied_array.clear()
        #         decisiondot_already_applied_array.clear()
        #         connectdot_already_applied_array.clear()
        #         stoke_arrow_flag_pos=0
        #         startdot_flag_pos=0
        #         decision_dot_flag_pos=0
        #         connect_dot_flag_pos=0
        #         while(len(SW_global.letters_already_written)==3):
        #             del SW_global.letters_already_written[len(SW_global.letters_already_written)-1]
        #         print("This is beging delete_list")
        #         print(delete_list22)
        #         for i in delete_list22:
        #             print(i)
        #             cut_addletter(i)
        #         fig.canvas.draw()
        #         print("Delete list")
        #         delete_list.clear()
        #         for i in delete_list22:
        #             delete_list.append(i)
        #         print(delete_list)
        #         print(SW_global.letters_already_written)
        #         composite_dot()
        #         start_dot()
        #         Decision_dot()
        #         connect_dot()

        #         fig.canvas.draw()
        #     else:
        #         print("I got paste length zero")



    if(event.key=='ctrl+x'):
        print("This is ctrl+x")
        # SW_global.pos1_global=pos1
        # SW_global.pos2_global=pos2
        # SW_global.start_axes_global=start_axes
        # SW_global.end_axes_global=end_axes
        # SW_global.start_axes_global_temp=temp_click_axes
        # SW_global.end_axes_global_temp=temp_release_axes
        print("I am before cut ")
        k_copy=SW_global.copy_string
        import pyperclip
        pyperclip.copy(k_copy)
        print(k_copy)
        SW_global.copy_string=""
        cut_for_single_guideor_multiple_guide(pos1=SW_global.pos1_global,pos2=SW_global.pos2_global,end_axes=SW_global.end_axes_global,start_axes=SW_global.start_axes_global)
        fig.canvas.draw()


        # print(delete_list)
        # import pyperclip
        # k_copy=SW_global.copy_string
        # pyperclip.copy(k_copy)
        # SW_global.copy_string=""
        # print("I am cutting")
        # print(pos11_start)
        # print(pos22_end)
        # if(pos11_start>=0):
        #     if(pos22_end>=0):
        #         Starting_loop_point1=SW_global.letters_already_written[pos11_start]
        #         ending_loop_point1=SW_global.letters_already_written[pos22_end]
        #         temp_array=[]
        #         ####  This  is cut operation ########
        #         if(int(SW_global.click_x)!=int(SW_global.release_x)):
        #             for i in range(len(SW_global.g_val.lines)):
        #                 if(i>3):
        #                     k1=SW_global.g_val.lines[i]
        #                     k1.set_visible(False)

        #             delete1=[]
        #             for i in range(len(delete_list)):
        #                 if((i>=pos1i) and (i<=pos2i)):
        #                     bg=1
        #                 else:
        #                     delete1.append(delete_list[i])
        #           #  print("This is delete list")
        #             print(delete1)
        #             delete_list.clear()
        #             for i in delete1:
        #                 delete_list.append(i)

        #             print(pos1i)
        #             print(pos2i)
        #            # print("This is cursor pos")
        #             print(SW_global.cursor_data)
        #             print(SW_global.cursor_pos)
        #             #for i in range(pos)
        #             loop_start11=pos1i+1
        #             loop_end11=pos2i+1
        #             print(loop_start11)
        #             print(loop_end11)
        #             cur_delete1=[]
        #             cur_delete2=[]
        #             for i in range(len(SW_global.cursor_pos)):
        #             #    print("I am in loop")
        #                 if((i>=loop_start11) and (i<=loop_end11)):
        #                    # print(i)
        #                    # print(loop_start11)
        #                    # print(loop_end11)
        #                     bo=1
        #                 else:
        #                     #cur_delete1.append(SW_global.cursor_data[i])
        #                     cur_delete2.append(SW_global.cursor_pos[i])
        #             print("This is after deletion operation")
        #            # print(cur_delete1)
        #            # print(cur_delete2)
        #             for i in range(len(SW_global.cursor_data)):
        #                 if((i>=pos1i) and (i<=pos2i)):
        #                     print(i)
        #                     print(loop_start11)
        #                     bo=2
        #                 else:
        #                     cur_delete1.append(SW_global.cursor_data[i])
        #           #  print(cur_delete1)
        #           #  print(SW_global.letters_already_written)
        #             ### letter already written update #####
        #             letters_already_written1=[]
        #            # print(pos11_start)
        #            # print(pos22_end)
        #             ## need to add
        #             ###if((len(SW_global.letters_already_written)>=pos11_start) and (len(SW_global.letters_already_written)<=pos22_end)):
        #             loop_1=SW_global.letters_already_written[0]
        #             loop_2=SW_global.letters_already_written[len(SW_global.letters_already_written)-1]
        #            # print("This is loop_1")
        #            # print(loop_1)
        #            # print(loop_2)
        #             #### Set cur sor invisible####

        #             k4=SW_global.cursor_data[len(SW_global.cursor_data)-1]
        #            # print("main cursor data")
        #            # print(k4)
        #             k4.set_visible(False)
        #             for i in range(loop_1,loop_2):
        #             #    print("This is invisible part")
        #                 k=SW_global.g_val.lines[i]
        #                 k.set_visible(False)
        #         #    fig.canvas.draw()


        #             if((len(SW_global.letters_already_written)>0) and (pos22_end<=(len(SW_global.letters_already_written)))):
        #               #  print("This is lett")
        #                 for i in range(len(SW_global.letters_already_written)):
        #                     if((i>=pos11_start) and (i<=pos22_end)):
        #                         bw=3
        #                     else:
        #                         letters_already_written1.append(SW_global.letters_already_written[i])
        #            # print("This is letters alereaudy update")
        #            # print(letters_already_written1)
        #             SW_global.kern_list.insert(0,0)
        #             #delete_list=[]

        #             SW_global.cursor_pos=[0]
        #             SW_global.cursor_data=[] # After complication we have to add default to x=0 y=-900 to 1500
        #             while(len(SW_global.letters_already_written)==3):
        #                 del SW_gobal.letters_already_written[len(SW_global.letters_already_written)-1]
        #             SW_global.kern_list.insert(0,0)
        #             SW_global.letters_already_written.clear()
        #             SW_global.cursor_pos=[0]
        #             SW_global.cursor_data=[]
        #             SW_global.kern_value_array.clear()
        #             SW_global.kern_value_array.insert(0,0)
        #             kern_value_array.clear()
        #             kern_value_array.insert(0,0)
        #             compositedot_already_applied_array.clear()
        #             startdot_already_applied_array.clear()
        #             decisiondot_already_applied_array.clear()
        #             connectdot_already_applied_array.clear()
        #             stoke_arrow_flag_pos=0
        #             startdot_flag_pos=0
        #             decision_dot_flag_pos=0
        #             connect_dot_flag_pos=0
        #             for i in delete1:
        #                 print(i)
        #                 cut_addletter(i)
        #             composite_dot()
        #             start_dot()
        #             Decision_dot()
        #             connect_dot()
        #             fig.canvas.draw()












    if event.key == 'backspace':
        # main_back_space_controller()
        try:
            if(len(SW_global.axes_data)>0):
                if SW_global.axes_data[str(0)]["axis_data"] in SW_global.text_flow_axes:
                    print("check point 1")
                    main_back_space_controller_for_text_flow_features2()
                else:
                    print("check point 2")
                    main_back_space_controller()
            else:
                if(guideline_axes[l] in SW_global.text_flow_axes):
                    print("check point 3")
                    main_back_space_controller_for_text_flow_features2()
                else:
                    print("check point 4")
                    main_back_space_controller()
                #main_add_controller(event.key)
                print("delete_list",delete_list)
                print("kern_value_array",kern_value_array)
        except Exeption as e:
            print(e)


        #backspaceOperation2()     #### backspace function has some bug need to check with respected to commented back space check with commented back space which works well ####
    #     if(SW_global.single_click_data!=None):
    #         SW_global.single_click_data.set_visible(False)
    #     len1 = len(SW_global.letters_already_written)
    #     len2 = len1 - 1
    #     #print("this is start loop variables")
    #     srt_loop = SW_global.letters_already_written[len2 - 1]
    #     end_loop = SW_global.letters_already_written[len2]
    #     for de1 in SW_global.cursor_data:
    #         de1.set_visible(False)
    #     #for de1 in SW_global.g


    #     for i in range(srt_loop, end_loop):
    #         SW_global.g_val.lines[i].set_visible(False)
    #         #print(SW_global.g_val.lines[i])
    #     fig.canvas.draw()

    #     #print(" This is erase end ")

    #     ## this is end of erase part #
    #     del SW_global.letters_already_written[len1-1]
    #     del SW_global.letters_already_written[len1-2]



    #     last_input_len = len(delete_list)
    #     print("This is delete list")
    #     print(delete_list)
    #     print(SW_global.kern_list)
    #     last_glyph = delete_list[last_input_len - 1]
    #     del delete_list[last_input_len - 1]
    #     l12 = len(kern_value_array)
    #     del kern_value_array[l12 - 1]
    #     kern_x = SW_global.kern_list[0] - 300 - manuscript.x_max[last_glyph]
    #     #print("This is from back space ")
    #     #print("This is before kern_x")
    #     SW_global.kern_list.insert(0, kern_x)
    #     #print("This is after kern_x")

    #     if SW_global.connectdot_on_off == 1:
    #         len11 = len(connectdot_already_applied_array)
    #         last_value1 = connectdot_already_applied_array[len11 - 1]
    #         starting_value1 = connectdot_already_applied_array[len11 - 2]
    #         del connectdot_already_applied_array[len11 - 1]
    #         del connectdot_already_applied_array[len11 - 2]
    #         for i in range(starting_value1, last_value1):
    #             guideline_axes[l].lines[i].set_visible(False)
    #             #print(guideline_axes[l].lines[i])
    #         fig.canvas.draw()
    #         connect_dot_flag_pos = connect_dot_flag_pos - 1

    #     if SW_global.decisiondot_on_off == 1:
    #         len11 = len(decisiondot_already_applied_array)
    #         last_value1 = decisiondot_already_applied_array[len11 - 1]
    #         starting_value1 = decisiondot_already_applied_array[len11 - 2]
    #         del decisiondot_already_applied_array[len11 - 1]
    #         del decisiondot_already_applied_array[len11 - 2]
    #         for i in range(starting_value1, last_value1):
    #             guideline_axes[l].lines[i].set_visible(False)
    #             #print(guideline_axes[l].lines[i])
    #         fig.canvas.draw()
    #         decision_dot_flag_pos = decision_dot_flag_pos - 1

    #     if SW_global.stokearrow_on_off == 1:
    #         len11 = len(compositedot_already_applied_array)
    #         last_value1 = compositedot_already_applied_array[len11 - 1]
    #         starting_value1 = compositedot_already_applied_array[len11 - 2]
    #         del compositedot_already_applied_array[len11 - 1]
    #         del compositedot_already_applied_array[len11 - 2]
    #         for i in range(starting_value1, last_value1):
    #             guideline_axes[l].lines[i].set_visible(False)
    #             #print(guideline_axes[l].lines[i])
    #         fig.canvas.draw()
    #         stoke_arrow_flag_pos = stoke_arrow_flag_pos - 1

    #     if SW_global.startdot_on_off == 1:
    #         len11 = len(startdot_already_applied_array)
    #         last_value1 = startdot_already_applied_array[len11 - 1]
    #         starting_value1 = startdot_already_applied_array[len11 - 2]
    #         del startdot_already_applied_array[len11 - 1]
    #         del startdot_already_applied_array[len11 - 2]
    #         for i in range(starting_value1, last_value1):
    #             guideline_axes[l].lines[i].set_visible(False)
    #             #print(guideline_axes[l].lines[i])
    #         ###### Back Space for cursor ##########

    #         fig.canvas.draw()
    #         startdot_flag_pos = startdot_flag_pos - 1
    #    # print("This is before cursor delete")
    #    # print(SW_global.cursor_data)
    #    # print(SW_global.cursor_pos)
    #     del SW_global.cursor_data[len(SW_global.cursor_data)-1]
    #     del SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
    #     try:
    #         visible_item=SW_global.cursor_data[len(SW_global.cursor_data)-1]
    #        # visible_item.set_visible(True)
    #     except Exception as e:
    #         pass
    #     import numpy as np

    #     if(len(SW_global.cursor_pos)>1):
    #         cursor_x1=list(np.full((500),SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
    #         cursor_y=list(np.linspace(-900,1500,500))
    #         plot_data=plt.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
    #         SW_global.single_click_data=plot_data[0]







    #     #         cursor_x1=list(np.full((500),item_cursor-manuscript.x_max[delete_list[len(delete_list)-1]]))
    #     # plot_data=plt.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
    #     # SW_global.single_click_data=plot_data[0]
    #     #print("This is after cursor delete")
    #     #print(SW_global.cursor_pos)
    #     #print(SW_global.cursor_data)
    #     fig.canvas.draw()
    #     # print("This is deleting")
    #     # print("check ")
    #     # print(delete_list)
    #     # print(SW_global.recent_input_list)
    #     # print(SW_global.letters_already_written)
    #     # print("End check")



# ++++++++++++++++++++++++++++++++++++++++++++++++++ A-Z Input +++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # A-Z manuscript
    try:
        #print("i am in ",SW_global.)
################ Checking for wheather multiple guide line is needed or not #################
        # try:
        #     if(SW_global.kern_list[0]>15500):
        #         if((SW_global.current_pos!=None) and (SW_global.current_pos>=15500)):
        #             SW_global.current_axes=None
        #             SW_global.current_pos=None
        #             SW_global.current_pos_in_number=None
        #         else:
        #             pass

        #         print("i am in optimising stage")
        #         a=dict()
        #         a["letters_already_written"]=[i for i in  SW_global.letters_already_written]
        #         a["kern_value_array"]=[i for i in kern_value_array]
        #         a["delete_list"]=[i for i in delete_list]
        #         a["kern_list"]=[i for i in SW_global.kern_list]
        #         a["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
        #         a["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
        #         a["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
        #         a["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
        #         a["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
        #         a["startdot_flag_pos"]=startdot_flag_pos
        #         a["decision_dot_flag_pos"]=decision_dot_flag_pos
        #         a["connect_dot_flag_pos"]=connect_dot_flag_pos
        #         a["axis_data"]=guideline_axes[l]
        #         print("This is guide line axes .lines",len(guideline_axes[l].lines))
        #         a["lines"]=[i for i in guideline_axes[l].lines]
        #         print("This is check point 3")
        #         a["gval"]=[i for i in SW_global.g_val.lines]
        #         a["cursor_pos"]=[i for i in SW_global.cursor_pos]
        #         a["cursor_data"]=[i for i in SW_global.cursor_data]
        #         a["recent_input_list"]=[i for i in SW_global.recent_input_list]
        #         print("This is cursor_data")
        #         print(a["cursor_data"])
        #         SW_global.cursor_pos.clear()
        #         SW_global.cursor_data.clear()
        #         SW_global.cursor_pos.insert(0,0)
        #         #print("This is decision dot flag")
        #         #print(decision_dot_flag_pos)
        #         #print("This is axes data")
        #         #print(len(SW_global.axes_data))
        #         SW_global.axes_data[str(len(SW_global.axes_data))]=a
        #         #print(SW_global.axes_data)
        #         #print(guideline_axes[l].lines)
        #         kern_value_array.clear()
        #         SW_global.kern_list.clear()
        #         SW_global.letters_already_written.clear()
        #         SW_global.letters_already_written.clear()
        #         SW_global.kern_list.insert(0,0)
        #         SW_global.kern_value_array.clear()
        #         SW_global.kern_value_array.insert(0,0)
        #         kern_value_array.clear()
        #         kern_value_array.insert(0,0)
        #         #print("This is check point 2")
        #         #print(guideline_axes[l].lines)
        #         compositedot_already_applied_array.clear()
        #         startdot_already_applied_array.clear()
        #         decisiondot_already_applied_array.clear()
        #         connectdot_already_applied_array.clear()
        #         stoke_arrow_flag_pos =0
        #         #print("This is len")
        #         #print(guideline_axes[l].lines)
        #         startdot_flag_pos=0
        #         decision_dot_flag_pos=0
        #         connect_dot_flag_pos=0
        #         delete_list.clear()
        #         # SW_global.current_axes=None
        #         # SW_global.current_pos=None
        #         # #SW_global.current_pos_in_number=-9999
        #         # SW_global.current_pos_in_number=None
        #         #temp=[i for i in guideline_axes[l].lines]
        #         newCreateGuideLine(1,None,None,None,None)
        #         #print("This is after update ")


        #         for i in range(len(SW_global.axes_data)):
        #             print("8888888888888888888888888888888888888888888888888888888888888888888")
        #             print(SW_global.axes_data[str(i)])
        #             print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #             #print(SW_global.axes_data[str(i)])
        #             print("****************************************")
        #         ################################## checking for guideline_axes[l]
        #         print("This is guideLine axes_data","*"*60)
        #         print(guideline_axes)
        #         print("**"*60)

        # except Exception as e:
        #     print(e)
        #     pass
        # print("This is event.key","k1"+event.key+"k")

        # if(event.key==' '):
        #     print("I am in space ")
        #     if((SW_global.current_pos==None) and(SW_global.curent_axes==None)):
        #         print("ok1")
        #     elif((SW_global.current_axes==guideline_axes[l])):
        #         if((len(SW_global.cursor_pos)>0) and(SW_global.current_pos==SW_global.cursor_pos[-1])):
        #             print("ok3")
        #         else:
        #             print("ok4")
        #             if(len(SW_global.cursor_pos)==0):
        #                 print("ok6")

        #     elif((SW_global.current_pos!=None) and(SW_global.current_pos!=None)):
        #         print("ok2")

        # else:
        if(len(str(event.key))==1):
            try:
                # print("kern_value_array",kern_value_array)
                # temp_kern_value_array=[i for i in kern_value_array]
                # temp_delete_list=[i for i in delete_list]
                # print("pos1i",SW_global.p1)
                # print("pos2i",SW_global.p2)
                # fdelete_list=[]
                # fkern_value_array=[]
                # fdelete_list,fkern_value_array=add_letter_with_mouse_and_from_end2(axesdata=SW_global.current_axes,pos=SW_global.current_pos,
                #     event_key=event.key,kern_value_array=temp_kern_value_array,delete_list1=temp_delete_list)
                # print("********"*60,fdelete_list)
                # print("********"*60,fkern_value_array)
                # print("This is fkern_value_array:",fkern_value_array)
                # print("This is fdelete_list:",fdelete_list)
                # ker=[i for i in fkern_value_array]
                # delete_list.clear()
                # print(kern_value_array)
                # kern_value_array.clear()
                # for kq in fdelete_list:
                #     delete_list.append(kq)
                # for kq in ker:
                #     kern_value_array.append(kq)

                # print(kern_value_array)
                # print(delete_list)
                # features_checking_function()
                if(len(SW_global.axes_data)>0):
                    if SW_global.axes_data[str(0)]["axis_data"] in SW_global.text_flow_axes:
                        print("check point 1")
                        main_add_controller_for_text_flow_features2(event_key=event.key)
                    else:
                        print("check point 2")
                        main_add_controller(event.key)
                else:
                    if(guideline_axes[l] in SW_global.text_flow_axes):
                        print("check point 3")
                        main_add_controller_for_text_flow_features2(event_key=event.key)
                    else:
                        print("check point 4")
                        main_add_controller(event.key)
                #main_add_controller(event.key)
                print("delete_list",delete_list)
                print("kern_value_array",kern_value_array)
            except Exception as e:
                print(e)
                pass






############################ End of multiple guide line ###################################



#         length12 = len(SW_global.recent_input_list)
#         user_input = event.key
#         x_max = manuscript.x_max[user_input]
#         kern_x = SW_global.kern_list[0]

#         if color_letter_features_on_off:
#             c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
#         else:
#             c1, c2 = manuscript.return_manuscript_fonts(user_input)


#         c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)

#         kern_x = SW_global.kern_list[0] + x_max + 300
#         #print("After update kern list")
#         print("This is before kern_x update")
#         SW_global.kern_list.insert(0, kern_x)
#         print("This is after ken_x ")
#         #print(SW_global.kern_list)
#         #print("this is kern value array")
#         #print(kern_value_array)
#         kern_counter = len(kern_value_array)
#         kern_value_array.insert(kern_counter, kern_x)
#         #print(kern_value_array)
#         SW_global.recent_input_list.insert(length12, event.key)
#         #print("this is list")
#         delete_list.insert(length12, event.key)
#         #print(delete_list)
#         init_enrty_pos = len(SW_global.letters_already_written)
#         inti_letter_pos = len(guideline_axes[l].lines)
#         #print("This is guide line axes length ")
#         #print(len(guideline_axes[l].lines))
#         SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
#         #print(SW_global.letters_already_written)
#         if draw_type_color_letter == 1:
#             if letter_dot_density_no_dot_on_off == 1:
#                 alp = 0
#             else:
#                 alp = temp_alp
#             if color_letter_features_on_off:
#                 guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#             else:
#                 guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

#         else:
#             n = len(c1)
#             if letter_dot_density_no_dot_on_off == 1:
#                 alp = 0
#             else:
#                 alp = temp_alp
#             if color_letter_features_on_off:
#                 for i in range(n):
#                     if i == 0:
#                         guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                     if i == 1:
#                         guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                     if i == 2:
#                         guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#                     if i == 3:
#                         guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
#             else:
#                 for i in range(n):
#                     guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
#         #############################   Cursor part code of inserting ###############################
#         import numpy as np
#         if(len(SW_global.cursor_data)!=0):
#             print("It is ok")
#             print(delete_list)
#             print(SW_global.letters_already_written)
#            # print(cursor_data)
#             #cursor_pos(cursor_pos)
#         else:
#             print("It is empty")
#         item_cursor=kern_x-300
#         cursor_y=list(np.linspace(-900,1500,500))
#         #cursor_y_neg=list(np.lenspace)
#         cursor_x=list(np.full((500),item_cursor))
#         SW_global.cursor_pos.append(item_cursor)
#         cursor_x1=list(np.full((500),item_cursor))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
#         plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
#         SW_global.single_click_data=plot_data[0]
#         ##### Add new two variable for current axes and current pos #####
#         SW_global.current_axes=guideline_axes[l]
#         SW_global.current_pos=item_cursor


#         k=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
#         #print(k)
#         #print(k)
#         for i in k:
#             SW_global.cursor_data.append(i)
#             i.set_visible(False)

#         #SW_global.cursor_data.append(k)
#         #print(SW_global.cursor_data)
#         for cur_count in range(len(SW_global.cursor_data)-1):
#             invisible_item=SW_global.cursor_data[cur_count]
#             #print("This is invisible_item")
#             #print(invisible_item)
#             invisible_item.set_visible(False)
#         fig.canvas.draw()
#         #print(guideline_axes[0].lines)

# # -----------------------------------------------------------------------------------------------------
#         final_enrty_pos = len(SW_global.letters_already_written)
#         final_letter_pos = len(guideline_axes[l].lines)
#         SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
#         features_checking_function()
#         print("checking for data inserting")
#         print(delete_list)
#         print(SW_global.recent_input_list)
#         print(SW_global.letters_already_written)
#         print(SW_global.kern_list)
#         print("End")

#         print("SW_global.current_pos:",SW_global.current_pos)
#         print("SW_global.current_axes:",SW_global.current_axes)


    except KeyError:
        pass




# -----------------------------------------------PRESS EVENT END-------------------------------------------
def my_draw(c1, c2):
    guideline_axes[l].plot(c1, c2, color='red', linewidth=0.6, dashes=(3, 4))


def my_draw1(c1, c2):
    guideline_axes[l].plot(c1, c2, color='red', linewidth=0.6, dashes=(3, 4), alpha=alp)


def features_checking_function():
    global letter_out_line_on_off
    global color_letter_features_on_off
    if SW_global.startdot_on_off == 1:
        call_start_dot_multiple_guideline()
        start_dot_continueous_write()

    else:
        pass

    if SW_global.decisiondot_on_off == 1:
        call_decision_dot_for_mul()
        decision_dot_continueous_write()
    else:
        pass

    if SW_global.stokearrow_on_off == 1:
        call_composit_dot_multipleGuideline()
        stoke_arrow_continueous_write()
    else:
        pass

    if SW_global.connectdot_on_off == 1:
        call_connect_dot_for_multipleGuideLine()
        connect_dot_continueous_write()
    else:
        pass

    if letter_out_line_on_off == 1:
        print("check both ")
        #Letter_Out_Line_Continuous_writting()
       #call_letter_on_line()
    else:
        pass

    if color_letter_features_on_off ==1:
        color_letter_continues_write()
    else:
        pass



def onscroll(event):
    global img_pos1, img_pos2
    print("%s %s" % (event.button, event.step))
    img_pos1 = event.step
    img_pos2 = event.button


key_c = 0

def kChange(event):
               # b=dict()
               #  b["axes_data"]=guideline_axes[l]
               #  b["lines"]=guideline_axes[l].lines
               #  b["compositedot_already_applied_array"]=compositedot_already_applied_array
               #  b["decisiondot_already_applied_array"]=decisiondot_already_applied_array
               #  b["startdot_already_applied_array"]=startdot_already_applied_array
               #  b["connectdot_already_applied_array"]=connectdot_already_applied_array
               #  b["kern_value_array"]=kern_value_array
               #  b["kern_list"]=kern_list
               #  SW_global.recent_axes_with_respect_rectangle_selector[str("0")]=
#    SW_global.current_axes=SW_global.release_axes
#    SW_global.current_pos=pos1i
#    print("This is from SW_global.current_axes",SW_global.release_axes)
#    print("This is from SW_global.current_pos",SW_global.pos1i)
    b=dict()
    print("This is K change ****************************************************************")
    b["axes_data"]=guideline_axes[l]
    b["lines"]=guideline_axes[l]
    b["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
    b["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
    b["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
    b["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
    b["kern_value_array"]=[i for i in kern_value_array]
    b["kern_list"]=[i for i in SW_global.kern_list]
    b["connect_dot_flag_pos"]=connect_dot_flag_pos
    b["decision_dot_flag_pos"]=decision_dot_flag_pos
    b["startdot_flag_pos"]=startdot_flag_pos
    b["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
    b["decision_dot_flag_pos"]=decision_dot_flag_pos
    b["connect_dot_flag_pos"]=connect_dot_flag_pos
    b["cursor_pos"]=[i for i in SW_global.cursor_pos]
    b["cursor_data"]=[i for i in SW_global.cursor_data]
    b["gval"]=[i for i in SW_global.g_val.lines]
    # SW_global.recent_axes_with_respect_rectangle_selector[str("0")]=b
    # print("I am in kchange")
    # if(len(SW_global.axes_data)>=1):
    #     for i in range(len(SW_global.axes_data)):
    #         if(SW_global.axes_data[str(i)]["axis_data"]==event.inaxes):
    #             print("I got axes *****************ok check 1")
    return

####### This is add letter outliner  ######

# def add_letter_with_outliner(event):
#     try:
#         length12 = len(SW_global.recent_input_list)
#         user_input = event.key
#         x_max = manu_letter_out_line_inner_fonts.x_max[user_input]
#         kern_x = SW_global.kern_list[0]
#         c1, c2 = manu_letter_outline.return_outline_fonts(user_input)
#         c1, c2, draw_type_letter_out_line = Kern_add_help.kern_add_operation(c1, c2, kern_x)

#         c11, c22 = manu_letter_out_line_inner_fonts.return_letter_out_inner_fonts(user_input)
#         c11, c22, draw_type_letter_in_line = Kern_add_help.kern_add_operation(c11, c22, kern_x)
#         kern_x = SW_global.kern_list[0] + x_max + 400
#         SW_global.kern_list.insert(0, kern_x)

#         kern_counter = len(kern_value_array)
#         kern_value_array.insert(kern_counter, kern_x)
#         SW_global.recent_input_list.insert(length12, event.key)
#         delete_list.insert(length12, event.key)

#         init_enrty_pos = len(letter_out_line_inner_fonts_array)
#         inti_letter_pos = len(guideline_axes[l].lines)
#         letter_out_line_inner_fonts_array.insert(init_enrty_pos, inti_letter_pos)

#         if draw_type_letter_in_line == 1:
#             guideline_axes[l].plot(c11, c22, color='black', dashes=(3, 2), linewidth=0.6)
#         else:
#             for il in range(len(c11)):
#                 guideline_axes[l].plot(c11[il], c22[il], color='black', dashes=(3, 2), linewidth=0.6)
#         fig.canvas.draw()

#         final_enrty_pos = len(letter_out_line_inner_fonts_array)
#         final_letter_pos = len(guideline_axes[l].lines)
#         letter_out_line_inner_fonts_array.insert(final_enrty_pos, final_letter_pos)

#         init_enrty_pos = len(SW_global.letters_already_written)
#         inti_letter_pos = len(guideline_axes[l].lines)
#         SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)

#         if draw_type_letter_out_line == 1:
#             my_draw1(c1, c2)
#             fig.canvas.draw()
#         else:
#             n = len(c1)
#             for i in range(n):
#                 my_draw(c1[i], c2[i])
#             fig.canvas.draw()

# # -----------------------------------------------------------------------------------------------------
#         final_enrty_pos = len(SW_global.letters_already_written)
#         final_letter_pos = len(guideline_axes[l].lines)
#         SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
#         features_checking_function()

#     except KeyError:
#         pass









###### This is add letter with outliner #######
def call_for_main_controller_for_text_flow(event_key):
    
    return 


# def main_back_space_controller():
    
#     return


def main_back_space_controller():
    print("I am form main back space controller")
    if(SW_global.current_axes!=None):
        if(SW_global.current_axes==guideline_axes[l]):
            print("check point back space 11")
            if((len(SW_global.cursor_data)==0) and (len(SW_global.axes_data)>0)):
                guideline_axes[l].set_visible(False)
                print("check point back space 12")
                k1=guideline_axes[l]
                del k1
                print("check point back space 12")
                guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                kern_value_array.clear()
                kern_value_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"])
                SW_global.kern_list.clear()
                SW_global.kern_list.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"])
                delete_list.clear()
                delete_list.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"])
                SW_global.letters_already_written.clear()
                SW_global.letters_already_written.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                guideline_axes[l].lines.clear()
                guideline_axes[l].lines.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"])
                SW_global.cursor_pos.clear()
                SW_global.cursor_pos.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"])
                SW_global.cursor_data.clear()
                # for s in SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"]:
                #     s.set_visible(True)
                # fig.canvas.draw()

                SW_global.cursor_data.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"])
                # for s in SW_global.cursor_data:
                #     s.set_visible(True)
                # fig.canvas.draw()
                compositedot_already_applied_array.clear()
                compositedot_already_applied_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["compositedot_already_applied_array"])
                startdot_already_applied_array.clear()
                startdot_already_applied_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["startdot_already_applied_array"])
                decisiondot_already_applied_array.clear()
                decisiondot_already_applied_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["decisiondot_already_applied_array"])
                connectdot_already_applied_array.clear()
                connectdot_already_applied_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["connectdot_already_applied_array"])
                stoke_arrow_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["stoke_arrow_flag_pos"]
                decision_dot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["decision_dot_flag_pos"]
                connect_dot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["connect_dot_flag_pos"]
                startdot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["startdot_flag_pos"]
                SW_global.current_axes=guideline_axes[l]
                SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
                del SW_global.axes_data[str(len(SW_global.axes_data)-1)]

            elif((SW_global.current_pos==None) or((len(SW_global.cursor_pos)>0) and (SW_global.current_pos==SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))):
                print("check point 13")
                # for k1 in SW_global.cursor_data:
                #     k1.set_visible(True)
                # fig.canvas.draw()
                delete_letter_from_end()
                print("This is cursor data",SW_global.cursor_data)
                print("This is cursor_pos",SW_global.cursor_pos)
            else:
                print("check point 14")
                current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=guideline_axes[l])
                temp=[]
                for j in range(len(delete_list)):
                    if(SW_global.current_pos_in_number!=None and j!=SW_global.current_pos_in_number-1):
                        temp.append(delete_list[j])
                clear_digit_from_axes(axesdata=guideline_axes[l])
                base_line_array=[]
                print("This is temp",temp)
                print("this is ",guideline_axes[l].lines)
                if(len(guideline_axes[l].lines)>4):
                    for j in range(4):
                        base_line_array.append(guideline_axes[l].lines[j])
                temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp,spec_axes=guideline_axes[l],baselines_objects_array=base_line_array)
                kern_value_array.clear()
                kern_value_array.extend(temp_kern_value1.copy())
                SW_global.kern_list.clear()
                SW_global.kern_list.extend(temp_kern_list1.copy())
                delete_list.clear()
                delete_list.extend(temp_delete1.copy())
                SW_global.recent_input_list.clear()
                SW_global.recent_input_list.extend(temp_recent1.copy())
                SW_global.cursor_data.clear()
                SW_global.cursor_data.extend(temp_cursor_data1)
                SW_global.cursor_pos.clear()
                SW_global.cursor_pos.extend(temp_cursor_pos1)
                SW_global.letters_already_written.clear()
                SW_global.letters_already_written.extend(letters_already_written3)
                guideline_axes[l].lines.clear()
                guideline_axes[l].lines.extend(temp_guideline_axes1.copy())
                if(SW_global.current_pos_in_number>0):
                    SW_global.current_pos_in_number=SW_global.current_pos_in_number-1
                    SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number]
                    SW_global.current_axes=guideline_axes[l]
                    ### need to add cursor data #####
        else:
            print("check point 15")
            temp_delete_list0=[]

            if(len(SW_global.axes_data)>0):
                key_for_axes=None
                for j in range(len(SW_global.axes_data)):
                    if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.current_axes):
                        key_for_axes=j
                        break

                if(key_for_axes!=None):
                    for j in range(key_for_axes,len(SW_global.axes_data)):
                        if(j==key_for_axes):
                            current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.axes_data[str(j)]["axis_data"])
                            for i in range(len(SW_global.axes_data[str(j)]["delete_list"])):
                                if(SW_global.current_pos_in_number-1!=i):
                                    temp_delete_list0.append(SW_global.axes_data[str(j)]["delete_list"][i])
                        else:
                            temp_delete_list0.extend(SW_global.axes_data[str(j)]["delete_list"])
                temp_delete_list0.extend(delete_list.copy())
                temp_delete_list1=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list0,limit1=SW_global.max_limit)
                count1=key_for_axes
                print("this is temp_delete_list1",temp_delete_list1)
                for j in range(len(temp_delete_list1)):
                    if(count1<len(SW_global.axes_data)):

                        clear_digit_from_axes(axesdata=SW_global.axes_data[str(count1)]["axis_data"])
                    else:
                        clear_digit_from_axes(axesdata=guideline_axes[l])
                    base_array=[]
                    if(count1<len(SW_global.axes_data)):
                        for k1 in range(4):
                            base_array.append(SW_global.axes_data[str(count1)]["lines"][k1])
                        temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp_delete_list1[j],spec_axes=SW_global.axes_data[str(count1)]["axis_data"],baselines_objects_array=base_array)
                        save_data_to_axes_dict(kern_value1=temp_kern_value1,delete_list1=temp_delete1,recent_input_list1=temp_recent1,cursor_pos1=temp_cursor_pos1,cursor_data1=temp_cursor_data1,axes_key_index=count1,
                            letters_already_written1=letters_already_written3,axesdata=SW_global.axes_data[str(count1)]["axis_data"],lines1=temp_guideline_axes1)
                        count1=count1+1
                    elif(count1==len(SW_global.axes_data)):
                        clear_digit_from_axes(axesdata=guideline_axes[l])
                        base_array=[]
                        for k1 in range(4):
                            base_array.append(guideline_axes[l].lines[k1])
                        temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp_delete_list1[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                        kern_value_array.clear()
                        kern_value_array.extend(temp_kern_value1.copy())
                        SW_global.kern_list.clear()
                        SW_global.kern_list.extend(temp_kern_list1.copy())
                        delete_list.clear()
                        delete_list.extend(temp_delete1.copy())
                        SW_global.recent_input_list.clear()
                        SW_global.recent_input_list.extend(temp_recent1.copy())
                        SW_global.cursor_data.clear()
                        SW_global.cursor_data.extend(temp_cursor_data1)
                        SW_global.cursor_pos.clear()
                        SW_global.cursor_pos.extend(temp_cursor_pos1)
                        SW_global.letters_already_written.clear()
                        SW_global.letters_already_written.extend(letters_already_written3)
                        guideline_axes[l].lines.clear()
                        guideline_axes[l].lines.extend(temp_guideline_axes1.copy())
                        count1=count1+1
                if((count1!=None) and(count1<len(SW_global.axes_data))):
                    guideline_axes[l].set_visible(False)
                    guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                    kern_value_array.clear()
                    kern_value_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"])
                    SW_global.kern_list.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"])
                    delete_list.clear()
                    delete_list.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"])
                    SW_global.letters_already_written.clear()
                    SW_global.letters_already_written.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
                    guideline_axes[l].lines.clear()
                    guideline_axes[l].lines.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"])
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_pos.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"])
                    SW_global.cursor_data.clear()
                    SW_global.cursor_data.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"])
                    compositedot_already_applied_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["compositedot_already_applied_array"])
                    startdot_already_applied_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["startdot_already_applied_array"])
                    decisiondot_already_applied_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["decisiondot_already_applied_array"])
                    connectdot_already_applied_array.extend(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["connectdot_already_applied_array"])
                    stoke_arrow_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["stoke_arrow_flag_pos"]
                    decision_dot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["decision_dot_flag_pos"]
                    connect_dot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["connect_dot_flag_pos"]
                    startdot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["startdot_flag_pos"]
                    SW_global.current_axes=guideline_axes[l]
                    SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
                    del SW_global.axes_data[str(len(SW_global.axes_data)-1)]

    return



def delete_letter_from_end():
    try:
        print("I am in from delete letter from end")
        if(SW_global.single_click_data!=None):
            SW_global.single_click_data.set_visible(False)
        len1 = len(SW_global.letters_already_written)
        len2 = len1 - 1
        srt_loop = SW_global.letters_already_written[len2 - 1]
        end_loop = SW_global.letters_already_written[len2]
        for de1 in SW_global.cursor_data:
            de1.set_visible(False)
        for i in range(srt_loop, end_loop):
            guideline_axes[l].lines[i].set_visible(False)
        del SW_global.letters_already_written[len1-1]
        del SW_global.letters_already_written[len1-2]
        last_input_len = len(delete_list)
        last_glyph = delete_list[last_input_len - 1]
        del delete_list[last_input_len - 1]
        l12 = len(kern_value_array)
        del kern_value_array[l12 - 1]
        if(last_glyph!=" "):
            kern_x = SW_global.kern_list[0] - 300 - manuscript.x_max[last_glyph]

        SW_global.kern_list.insert(0, kern_x)
        if SW_global.connectdot_on_off == 1:
            len11 = len(connectdot_already_applied_array)
            last_value1 = connectdot_already_applied_array[len11 - 1]
            starting_value1 = connectdot_already_applied_array[len11 - 2]
            del connectdot_already_applied_array[len11 - 1]
            del connectdot_already_applied_array[len11 - 2]
            for i in range(starting_value1, last_value1):
                guideline_axes[l].lines[i].set_visible(False)
            connect_dot_flag_pos = connect_dot_flag_pos - 1
        if SW_global.decisiondot_on_off == 1:
            len11 = len(decisiondot_already_applied_array)
            last_value1 = decisiondot_already_applied_array[len11 - 1]
            starting_value1 = decisiondot_already_applied_array[len11 - 2]
            del decisiondot_already_applied_array[len11 - 1]
            del decisiondot_already_applied_array[len11 - 2]
            for i in range(starting_value1, last_value1):
                guideline_axes[l].lines[i].set_visible(False)
            decision_dot_flag_pos = decision_dot_flag_pos - 1
        if SW_global.stokearrow_on_off == 1:
            len11 = len(compositedot_already_applied_array)
            last_value1 = compositedot_already_applied_array[len11 - 1]
            starting_value1 = compositedot_already_applied_array[len11 - 2]
            del compositedot_already_applied_array[len11 - 1]
            del compositedot_already_applied_array[len11 - 2]
            for i in range(starting_value1, last_value1):
                guideline_axes[l].lines[i].set_visible(False)
            stoke_arrow_flag_pos = stoke_arrow_flag_pos - 1
        if SW_global.startdot_on_off == 1:
            len11 = len(startdot_already_applied_array)
            last_value1 = startdot_already_applied_array[len11 - 1]
            starting_value1 = startdot_already_applied_array[len11 - 2]
            del startdot_already_applied_array[len11 - 1]
            del startdot_already_applied_array[len11 - 2]
            for i in range(starting_value1, last_value1):
                guideline_axes[l].lines[i].set_visible(False)
            startdot_flag_pos = startdot_flag_pos - 1
        del SW_global.cursor_data[len(SW_global.cursor_data)-1]
        del SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
        try:
            if(len(SW_global.cursor_data)>0):
                visible_item=SW_global.cursor_data[len(SW_global.cursor_data)-1]
                visible_item.set_visible(True)

        except Exception as e:
            print(e)
            pass
        if(len(SW_global.cursor_pos)>1):
            # cursor_x1=list(np.full((500),SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
            # cursor_y=list(np.linspace(-900,1500,500))
            # plot_data=plt.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            # SW_global.single_click_data=plot_data[0]
            ###### Add current_curosr current_axes ##########
            SW_global.current_axes=guideline_axes[l]
            SW_global.current_pos=SW_global.cursor_pos[-1]
            print("It is changed from point 1")
            SW_global.current_pos_in_number=len(SW_global.cursor_pos)-1
        fig.canvas.draw()
    except Exception as e:
        print("Exception occur",e)
        pass
    return





def backspaceOperation2():
    print("I am in backspace check point 1")
    if((SW_global.current_axes==None and SW_global.current_pos==None) or ((SW_global.current_axes==guideline_axes[l]) and (SW_global.current_pos==SW_global.cursor_pos[-1]))):
        try:
            print("I am in none condition")
            if(SW_global.single_click_data!=None):
                SW_global.single_click_data.set_visible(False)
            len1 = len(SW_global.letters_already_written)
            len2 = len1 - 1
            #print("this is start loop variables")
            srt_loop = SW_global.letters_already_written[len2 - 1]
            end_loop = SW_global.letters_already_written[len2]
            for de1 in SW_global.cursor_data:
                de1.set_visible(False)
            #for de1 in SW_global.g


            for i in range(srt_loop, end_loop):
                SW_global.g_val.lines[i].set_visible(False)
                #print(SW_global.g_val.lines[i])
            fig.canvas.draw()

            #print(" This is erase end ")

            ## this is end of erase part #
            del SW_global.letters_already_written[len1-1]
            del SW_global.letters_already_written[len1-2]



            last_input_len = len(delete_list)
            print("This is delete list")
            print(delete_list)
            print(SW_global.kern_list)
            last_glyph = delete_list[last_input_len - 1]
            del delete_list[last_input_len - 1]
            l12 = len(kern_value_array)
            del kern_value_array[l12 - 1]
            kern_x = SW_global.kern_list[0] - 300 - manuscript.x_max[last_glyph]
            #print("This is from back space ")
            #print("This is before kern_x")
            SW_global.kern_list.insert(0, kern_x)
            #print("This is after kern_x")

            if SW_global.connectdot_on_off == 1:
                len11 = len(connectdot_already_applied_array)
                last_value1 = connectdot_already_applied_array[len11 - 1]
                starting_value1 = connectdot_already_applied_array[len11 - 2]
                del connectdot_already_applied_array[len11 - 1]
                del connectdot_already_applied_array[len11 - 2]
                for i in range(starting_value1, last_value1):
                    guideline_axes[l].lines[i].set_visible(False)
                    #print(guideline_axes[l].lines[i])
                fig.canvas.draw()
                connect_dot_flag_pos = connect_dot_flag_pos - 1

            if SW_global.decisiondot_on_off == 1:
                len11 = len(decisiondot_already_applied_array)
                last_value1 = decisiondot_already_applied_array[len11 - 1]
                starting_value1 = decisiondot_already_applied_array[len11 - 2]
                del decisiondot_already_applied_array[len11 - 1]
                del decisiondot_already_applied_array[len11 - 2]
                for i in range(starting_value1, last_value1):
                    guideline_axes[l].lines[i].set_visible(False)
                    #print(guideline_axes[l].lines[i])
                fig.canvas.draw()
                decision_dot_flag_pos = decision_dot_flag_pos - 1

            if SW_global.stokearrow_on_off == 1:
                len11 = len(compositedot_already_applied_array)
                last_value1 = compositedot_already_applied_array[len11 - 1]
                starting_value1 = compositedot_already_applied_array[len11 - 2]
                del compositedot_already_applied_array[len11 - 1]
                del compositedot_already_applied_array[len11 - 2]
                for i in range(starting_value1, last_value1):
                    guideline_axes[l].lines[i].set_visible(False)
                    #print(guideline_axes[l].lines[i])
                fig.canvas.draw()
                stoke_arrow_flag_pos = stoke_arrow_flag_pos - 1

            if SW_global.startdot_on_off == 1:
                len11 = len(startdot_already_applied_array)
                last_value1 = startdot_already_applied_array[len11 - 1]
                starting_value1 = startdot_already_applied_array[len11 - 2]
                del startdot_already_applied_array[len11 - 1]
                del startdot_already_applied_array[len11 - 2]
                for i in range(starting_value1, last_value1):
                    guideline_axes[l].lines[i].set_visible(False)
                    #print(guideline_axes[l].lines[i])
                ###### Back Space for cursor ##########

                fig.canvas.draw()
                startdot_flag_pos = startdot_flag_pos - 1
           # print("This is before cursor delete")
           # print(SW_global.cursor_data)
           # print(SW_global.cursor_pos)
            del SW_global.cursor_data[len(SW_global.cursor_data)-1]
            del SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
            try:
                visible_item=SW_global.cursor_data[len(SW_global.cursor_data)-1]
               # visible_item.set_visible(True)
            except Exception as e:
                pass
            import numpy as np

            if(len(SW_global.cursor_pos)>1):
                cursor_x1=list(np.full((500),SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
                cursor_y=list(np.linspace(-900,1500,500))
                plot_data=plt.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                SW_global.single_click_data=plot_data[0]
                ###### Add current_curosr current_axes ##########
                SW_global.current_axes=guideline_axes[l]
                SW_global.current_pos=SW_global.cursor_pos[-1]
                print("It is changed from point 1")
                SW_global.current_pos_in_number=len(SW_global.cursor_pos)-1
            fig.canvas.draw()


        except Exception as e:
            pass
    elif((SW_global.current_axes==guideline_axes[l])):
        print("check point 33333")
        for i in range(len(SW_global.cursor_pos)):
            if(SW_global.cursor_pos[i]<SW_global.current_pos):
                SW_global.current_pos_in_number=i
        SW_global.entire_delete_list_for_one_page.clear()
        for j in range(len(delete_list)):
            if(SW_global.current_pos_in_number!=j):
                SW_global.entire_delete_list_for_one_page.append(delete_list[j])

        key=10000
        delete_list1=[j for j in delete_list]
        #delete_list,kern_value_array=
        add_letter_after_backspace(key=key,delete_list1=SW_global.entire_delete_list_for_one_page)



        print("delete_list_entire",SW_global.entire_delete_list_for_one_page)
        if(len(SW_global.cursor_pos)==1):
            # if(len(SW_global.axes_data)>0):
            #     SW_global.current_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"][-1]
            #     SW_global.current_axes=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
            # else:
            SW_global.current_pos=None
            SW_global.current_axes=None
    elif(SW_global.current_axes!=guideline_axes[l]):
        print("*"*200)
        for k5 in range(len(SW_global.axes_data)):
            print(SW_global.axes_data[str(k5)])
        print("*"*200)
        key=None
        for j in range(len(SW_global.axes_data)):
            if(SW_global.current_axes==SW_global.axes_data[str(j)]["axis_data"]):
                key=j
        for j in range(len(SW_global.axes_data[str(key)]["cursor_pos"])):
            if(SW_global.axes_data[str(key)]["cursor_pos"][j]<SW_global.current_pos):
                SW_global.current_pos_in_number=j
        SW_global.entire_delete_list_for_one_page.clear()
        print("SW_global.current_pos_in_number",SW_global.current_pos_in_number)
        if(SW_global.current_pos_in_number-1<0):
            SW_global.current_pos_in_number=0
        else:
            SW_global.current_pos_in_number=SW_global.current_pos_in_number-1
        for j in range(len(SW_global.axes_data[str(key)]["delete_list"])):
            if(SW_global.current_pos_in_number!=j):
                SW_global.entire_delete_list_for_one_page.append(SW_global.axes_data[str(key)]["delete_list"][j])

        for j in range(len(SW_global.axes_data)):
            if(j>key):
                for k in SW_global.axes_data[str(j)]["delete_list"]:
                    SW_global.entire_delete_list_for_one_page.append(k)
        for j in delete_list:
            SW_global.entire_delete_list_for_one_page.append(j)
        for j in range(len(SW_global.axes_data)):
            if(j>=key):
                for k1 in range(len(SW_global.axes_data[str(j)]["lines"])):
                    if(k1>3):
                        (SW_global.axes_data[str(j)]["lines"][k1]).set_visible(False)

                    (SW_global.axes_data[str(j)]["letters_already_written"]).clear()
                    (SW_global.axes_data[str(j)]["cursor_pos"]).clear()
                    (SW_global.axes_data[str(j)]["cursor_data"]).clear()
                    (SW_global.axes_data[str(j)]["kern_value_array"]).clear()
                    (SW_global.axes_data[str(j)]["delete_list"]).clear()
                    (SW_global.axes_data[str(j)]["kern_value_array"]).clear()
                    (SW_global.axes_data[str(j)]["kern_list"]).clear()
                    (SW_global.axes_data[str(j)]["compositedot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(j)]["startdot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(j)]["decisiondot_already_applied_array"]).clear()
                    (SW_global.axes_data[str(j)]["connectdot_already_applied_array"]).clear()
                    SW_global.axes_data[str(j)]["stoke_arrow_flag_pos"]=0
                    SW_global.axes_data[str(j)]["startdot_flag_pos"]=0
                    SW_global.axes_data[str(j)]["decision_dot_flag_pos"]=0
                    SW_global.axes_data[str(j)]["connect_dot_flag_pos"]=0
                    SW_global.axes_data[str(j)]["recent_input_list"].clear()



        for j in range(len(guideline_axes[l].lines)):
            if(j>3):
                (guideline_axes[l].lines[j]).set_visible(False)

        SW_global.cursor_pos.clear()
        SW_global.cursor_data.clear()
        kern_value_array.clear()
        SW_global.kern_list.clear()
        compositedot_already_applied_array.clear()
        startdot_already_applied_array.clear()
        decisiondot_already_applied_array.clear()
        connectdot_already_applied_array.clear()
        decision_dot_flag_pos=0
        startdot_flag_pos=0
        connect_dot_flag_pos=0
        stoke_arrow_flag_pos=0


        for j in range(len(SW_global.axes_data)):
            print("*"*40)
            print(SW_global.axes_data[str(j)])
            print("*"*40)


        print("This is before backspace")





        add_letter_after_backspace(key=key,delete_list1=SW_global.entire_delete_list_for_one_page)






        print("Entire delete_list for one page:",SW_global.entire_delete_list_for_one_page)
        print("The tech")


    return #kern_value_array,delete_list

def add_letter_after_backspace(key=None,delete_list1=None):
    if(key==10000):
        print("This is delete_list1",delete_list1)
        SW_global.cursor_data.clear()
        SW_global.cursor_pos.clear()
        SW_global.cursor_pos.insert(0,0)
        SW_global.letters_already_written.clear()
        kern_value_array.clear()
        kern_value_array.insert(0,0)
        SW_global.kern_list.clear()
        SW_global.kern_list.insert(0,0)
        delete_list.clear()
        SW_global.recent_input_list.clear()
        for k1 in range(len(guideline_axes[l].lines)):
            if(k1>3):
                guideline_axes[l].lines[k1].set_visible(False)
        while(len(guideline_axes[l].lines)<=3):
            del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
        for k1 in range(len(delete_list1)):
            user_input=delete_list1[k1]
            event_key=delete_list1[k1]
            length12=len(SW_global.recent_input_list)
            print("SW_global.recent_input_list:",SW_global.recent_input_list)
            #user_input=delete_list1[j]
            #event_key=delete_list1[j]
            x_max=manuscript.x_max[user_input]
            kern_x=SW_global.kern_list[0]
           ###################################################################################
            skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
            if user_input in skip_list:
                if(color_letter_features_on_off):
                    c1,c2=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                else:
                    c1,c2=manuscript.return_manuscript_fonts(user_input)
            else:
                if(color_letter_features_on_off):
                    x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    c1,c2=font_check(x,y)
                else:
                    x,y=manuscript.return_manuscript_fonts(user_input)
                    c1,c2=font_check(x,y)
            ####################################################################################


            c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)
         #   print("This is check point3")

            kern_x=SW_global.kern_list[0]+x_max+300
            SW_global.kern_list.insert(0,kern_x)
            kern_counter=len(kern_value_array)
            kern_value_array.insert(kern_counter,kern_x)
            SW_global.recent_input_list.insert(length12,event_key)
            delete_list.insert(length12,event_key)
            init_enrty_pos=len(SW_global.letters_already_written)
            inti_letter_pos=len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(init_enrty_pos,inti_letter_pos)
          #  print("Check point 4")
            if draw_type_color_letter==1:
                if letter_dot_density_no_dot_on_off==1:
                    alp=0
                else:
                    alp=temp_alp
                if color_letter_features_on_off:
                    guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
            else:
                n=len(c1)
                if letter_dot_density_no_dot_on_off==1:
                    alp=0
                else:
                    alp=temp_alp
                if color_letter_features_on_off:
                    for i in range(n):
                        if i==0:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==1:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==2:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        if i==3:
                            guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                else:
                    for i in range(n):
                        guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

            fig.canvas.draw()
           # print("check point 5")

            import numpy as np
            item_cursor=kern_x-300
            cursor_y=list(np.linspace(-900,1500,500))
            cursor_x=list(np.full((500),item_cursor))
            SW_global.cursor_pos.append(item_cursor)
            cursor_x1=list(np.full((500),item_cursor))
            plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            if(SW_global.single_click_data!=None):
                SW_global.single_click_data.set_visible(False)
            #SW_global.single_click_data=plot_data[0]
            k2=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            for k5 in SW_global.cursor_data:
                k5.set_visible(False)


            try:
                for i in k2:
                    SW_global.cursor_data.append(i)
                    i.set_visible(False)
            except Exception as e:
                print(e)
            #    print("I am check point22")
            fig.canvas.draw()
            final_enrty_pos = len(SW_global.letters_already_written)
            final_letter_pos = len(guideline_axes[l].lines)
            SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
            print("This is kern_value_array:",kern_value_array)
            print("check point 77")
            print("This is current_pos_in_number:",SW_global.current_pos_in_number)
        if(SW_global.current_pos_in_number-1>=0):
            SW_global.current_pos_in_number=SW_global.current_pos_in_number-1
            SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number]
        elif(SW_global.current_pos_in_number-1<0):
            if(len(SW_global.axes_data)>0):
                print("check point beta 02")
                SW_global.current_pos_in_number=len(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"])-1
                SW_global.current_axes=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
                SW_global.current_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"][-1]

        fig.canvas.draw()

    else:
        print("This is checking purpose")
        for j5 in range(len(SW_global.axes_data)):
            print(SW_global.axes_data[str(j5)])
            print("*"*60)
        print(key)
        print(delete_list1)
        print(key)
        print("This is delete_list:",delete_list1)
        print("I am in else part")
        print("check point 8888888888888")
        SW_global.temp_guideline_axes=None
        SW_global.temp_guideline_axes=SW_global.axes_data[str(key)]["axis_data"]
        count_of_axes=key
        kern_value_array2=[0]
        letters_already_written2=[]
        kern_list2=[0]
        recent_input_list2=[]
        g_val2=[i for i in SW_global.axes_data[str(key)]["lines"]]
        cursor_data2=[]
        cursor_pos2=[0]
        delete_list2=[]
        guideline_flag=-9999
        print("This is delete list:",delete_list1)
        temp_flag=0
        for k10 in range(len(delete_list1)):
            print("count_of_axes:",count_of_axes)
            print("axes is :",SW_global.temp_guideline_axes)
          #  print("axis need to be:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
            if(kern_list2[0]>15500):
                print("check point we*********************************************************")
                if(count_of_axes>len(SW_global.axes_data)-1):
                    guideline_axes[l].lines.clear()
                    for j in g_val2:
                        guideline_axes[l].lines.append(j)
                    SW_global.letters_already_written.clear()
                    for j in letters_already_written2:
                        SW_global.letters_already_written.append(j)
                    SW_global.recent_input_list.clear()
                    for j in recent_input_list:
                        SW_global.recent_input_list.append(j)
                    SW_global.cursor_pos.clear()
                    for j in cursor_pos2:
                        SW_global.cursor_pos.append(j)
                    SW_global.cursor_data.clear()
                    for j in cursor_data2:
                        SW_global.cursor_data.append(j)
                    SW_global.kern_list.clear()
                    for j in kern_list2:
                        SW_global.kern_list.append(j)
                    guideline_flag=40
                    #newCreateGuideLine(1,None,None,None)
                    count_of_axes=count_of_axes+1
                    delete_list2.clear()
                    cursor_data2.clear()
                    cursor_pos2.insert(0,0)
                    letters_already_written2.clear()
                    recent_input_list2.clear()
                    kern_value_array2.clear()
                    kern_value_array2.insert(0,0)
                    kern_list2.clear()
                    kern_list2.insert(0,0)
                    SW_global.temp_guide_line_axes=guideline_axes[l]
                else:
                    print("check point 66")
                    print("letters_already_written2",letters_already_written2)
                    print("delete_list",delete_list2)
                    print("count_of_axes",count_of_axes)
                    SW_global.axes_data[str(count_of_axes)]["letters_already_written"]=[k for k in letters_already_written2]
                    SW_global.axes_data[str(count_of_axes)]["cursor_pos"]=[k for k in cursor_pos2]
                    SW_global.axes_data[str(count_of_axes)]["cursor_data"]=[ k for k in cursor_data2]
                    SW_global.axes_data[str(count_of_axes)]["recent_input_list"]=[k for k in recent_input_list2]
                    SW_global.axes_data[str(count_of_axes)]["delete_list"]=[k for k in delete_list2]
                    SW_global.axes_data[str(count_of_axes)]["gval"]=[k for k in g_val2]
                    SW_global.axes_data[str(count_of_axes)]["lines"]=[k for k in g_val2]
                    SW_global.axes_data[str(count_of_axes)]["kern_value_array"]=[k for k in kern_value_array2]
                    SW_global.axes_data[str(count_of_axes)]["kern_list"]=[k for k in kern_list2]
                    print(SW_global.axes_data[str(count_of_axes)]["delete_list"])
                    g_val2.clear()
                    delete_list2.clear()
                    cursor_data2.clear()
                    cursor_pos2.clear()
                    cursor_pos2.insert(0,0)
                    letters_already_written2.clear()
                    recent_input_list2.clear()
                    kern_value_array2.clear()
                    kern_value_array2.insert(0,0)
                    kern_list2.clear()
                    print("check point 41")
                    kern_list2.insert(0,0)
                    print("check point wwwwqqqq")
                    print("count_of_axes:",count_of_axes)
                    print("len(axes_data):",len(SW_global.axes_data))
                    if(count_of_axes>=len(SW_global.axes_data)-1):
                        SW_global.temp_guideline_axes=guideline_axes[l]
                        g_val2.clear()
                        g_val2.append(guideline_axes[l].lines[0])
                        g_val2.append(guideline_axes[l].lines[1])
                        g_val2.append(guideline_axes[l].lines[2])
                        g_val2.append(guideline_axes[l].lines[3])
                        count_of_axes=count_of_axes+1
                    else:
                        count_of_axes=count_of_axes+1
                        SW_global.temp_guideline_axes=SW_global.axes_data[str(count_of_axes)]["axis_data"]
                        g_val2.clear()
                        for h1 in SW_global.axes_data[str(count_of_axes)]["lines"]:
                            g_val2.append(h1)
        #     #### Write code for data inserting on speacific axes ####
            length12=len(recent_input_list2)
            user_input=delete_list1[k10]
           # print("SW_global.axes_data",SW_global.temp_guideline_axes)
           # print("QWE:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
          #  print("user_input:",user_input)
            x_max=manuscript.x_max[user_input]
            kern_x=kern_list2[0]
          #  print("I am in loop check point1 ")

            ###################################################################################
            skip_list=["A","E","Y","F","M","N","X","z","Z","x","K","[","]","w","W","space"]
            if user_input in skip_list:
                if(color_letter_features_on_off):
                    c1,c2=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                else:
                    c1,c2=manuscript.return_manuscript_fonts(user_input)
            else:
                if(color_letter_features_on_off):
                    x,y=manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
                    c1,c2=font_check(x,y)
                else:
                    x,y=manuscript.return_manuscript_fonts(user_input)
                    c1,c2=font_check(x,y)
            ####################################################################################

            c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)


            kern_x=kern_list2[0]+x_max+300
            kern_list2.insert(0,kern_x)
           # print("check point 30")
            # c1,c2,draw_type_color_letter=Kern_add_help.kern_add_operation(c1,c2,kern_x)
            kern_counter=len(kern_value_array2)
            kern_value_array2.insert(kern_counter,kern_x)
            recent_input_list2.insert(length12,user_input)
            delete_list2.insert(length12,user_input)
            init_enrty_pos=len(letters_already_written2)
            inti_letter_pos=len(g_val2)
            #print("check point 31")
            print("SW_global.temp_guideline_axes:",SW_global.temp_guideline_axes)
            letters_already_written2.insert(init_enrty_pos,inti_letter_pos)
         #   print("check point 2")
            temp_o=[]

            if(draw_type_color_letter==1):
             #   print("check point 32")
                if(letter_dot_density_no_dot_on_off==1):
                    alp=0
                else:
                    alp=temp_alp
                if(color_letter_features_on_off):
                    temp_o.clear()
              #      print("check point 33")
                    temp_o=SW_global.temp_guideline_axes.plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    for k2 in temp_o:
                        g_val2.append(k2)
                   # print("count of axes:",SW_global.axes_data[str(count_of_axes)]["axis_data"])
                    print("temp_guideline_axes",SW_global.temp_guideline_axes)
                else:
               #     print("check point 34")
                    temp_o=SW_global.temp_guideline_axes.plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                    for k2 in temp_o:
                        g_val2.append(k2)
                  #  print("count_of_axes",SW_global.axes_data[str(count_of_axes)]["axis_data"])
                    print("SW_global",SW_global.temp_guideline_axes)
            else:
               # print("check point 35")
                n=len(c1)
                if letter_dot_density_no_dot_on_off == 1:
                    alp=0
                else:
                    alp=temp_alp

                #print("check point 36")


                if(color_letter_features_on_off):
                 #   print("check point 37")
                    for i in range(n):
                        if i==0:
                            temp_o.clear()
                            temp_o=SW_gobal.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            for k2 in temp_o:
                                g_val2.append(k2)
                        if i==1:
                            temp_o.clear()
                            temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            for k2 in temp_o:
                                g_val2.append(k2)
                        if i==2:
                            temp_o.clear()
                            temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            for k2 in temp_o:
                                g_val2.append(k2)
                        if i==3:
                            temp_o.clear()
                            temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                            for k2 in temp_o:
                                g_val2.append(k2)
                else:
                  #  print("check point 38")
                    for i in range(n):
                        temp_o.clear()
                        temp_o=SW_global.temp_guideline_axes.plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
                        for k2 in temp_o:
                            g_val2.append(k2)

            fig.canvas.draw()

            import numpy as np
            item_cursor=kern_x-300
            cursor_y=list(np.linspace(-900,1500,500))
            cursor_x=list(np.full(500,item_cursor))
            cursor_pos2.append(item_cursor)
            cursor_x1=list(np.full(500,item_cursor))
            if(SW_global.single_click_data!=None):
               # print("check point 39")
                SW_global.single_click_data.set_visible(False)

            plot_data=SW_global.temp_guideline_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            SW_global.single_click_data=plot_data[0]
            k2=SW_global.temp_guideline_axes.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))

          #  print("check point 40")

            for j10 in k2:
                cursor_data2.append(j10)
                j10.set_visible(False)

          #  print("check point 41")


            final_enrty_pos = len(letters_already_written2)
            final_letter_pos = len(g_val2)
            letters_already_written2.insert(final_enrty_pos, final_letter_pos)


        #### add condition for changing pos and current_axes #####
        # if(count_of_axes>len(SW_global.axes_data)-1):
        #     print("check point gamma")
        #     SW_global.current_axes=guideline_axes[l]
        #     if(SW_global.current_pos_in_number-1>=0):
        #         print("check point beta")
        #         SW_global.current_pos_in_number=SW_global.current_pos_in_number-1
        #         SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number]
        #     elif(SW_global.current_pos_in_number-1<0):
        #         print("check point beta 01")
        #         if(len(SW_global.axes_data)>0):
        #             print("check point beta 02")
        #             SW_global.current_pos_in_number=len(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"])-1
        #             SW_global.current_axes=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
        #             SW_global.current_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"][-1]
        # else:
        #     print("check point alpha 0111")
        #     SW_global.current_axes=SW_global.axes_data[str(key)]["axis_data"]
        #     if(SW_global.current_pos_in_number-1>=0):
        #         print("check point beta 0222")
        #         SW_global.current_pos_in_number=SW_global.current_pos_in_number-1
        #         SW_global.current_pos=SW_global.axes_data[str(key)]["cursor_pos"][SW_global.current_pos_in_number]
        #     elif(SW_global.current_pos_in_number-1<0):
        #         print("check point")
        #         if(key-1>0):
        #             SW_global.current_axes=SW_global.axes_data[str(key-1)]["axis_data"]
        #             SW_global.current_pos_in_number=len(SW_global.axes_data[str(key)-1]["delete_list"])-1
        #             SW_global.current_pos=SW_global.axes_data[str(key)-1]["cursor_pos"][-1]

        if(count_of_axes>len(SW_global.axes_data)-1):
            guideline_axes[l].lines.clear()
            for j in g_val2:
                guideline_axes[l].lines.append(j)
            SW_global.letters_already_written.clear()
            for j in letters_already_written2:
                SW_global.letters_already_written.append(j)
            SW_global.cursor_pos.clear()
            for j in cursor_pos2:
                SW_global.cursor_pos.append(j)
            SW_global.cursor_data.clear()
            for j in cursor_data2:
                SW_global.cursor_data.append(j)
            delete_list.clear()
            for j in delete_list2:
                delete_list.append(j)
            kern_value_array.clear()
            for j in kern_value_array2:
                kern_value_array.append(j)
            SW_global.kern_list.clear()
            for j in kern_list2:
                SW_global.kern_list.append(j)
        else:
            (SW_global.axes_data[str(count_of_axes)]["letters_already_written"]).clear()
            for j in letters_already_written2:
                SW_global.letters_already_written.append(j)
            (SW_global.axes_data[str(count_of_axes)]["delete_list"]).clear()
            for j in delete_list2:
                (SW_global.axes_data[str(count_of_axes)]["delete_list"]).clear()
            (SW_global.axes_data[str(count_of_axes)]["cursor_pos"]).clear()
            for j in cursor_pos2:
                (SW_global.axes_data[str(count_of_axes)]["cursor_pos"]).append(j)
            (SW_global.axes_data[str(count_of_axes)]["lines"]).clear()
            for j in g_val2:
                (SW_global.axes_data[str(count_of_axes)]["lines"]).append(j)
            (SW_global.axes_data[str(count_of_axes)]["cursor_data"]).clear()
            for j in cursor_data2:
                (SW_global.axes_data[str(count_of_axes)]["cursor_data"]).append(j)
            (SW_global.axes_data[str(count_of_axes)]["kern_value_array"]).clear()
            for j in  kern_value_array2:
                (SW_global.axes_data[str(count_of_axes)]["kern_value_array"]).append(j)
            SW_global.kern_list.clear()
            for j in kern_list2:
                SW_global.kern_list.append(j)
        try:

            if(len(SW_global.axes_data)-1>count_of_axes):
                if(SW_global.current_pos_in_number-1<0):
                    if(count_of_axes-1>0):
                        SW_global.current_axes=SW_global.axes_data[str(count_of_axes-1)]["axis_data"]
                        SW_global.current_pos=SW_global.axes_data[str(count_of_axes-1)]["cursor_pos"][-2]
                        SW_global.current_pos_in_number=len(SW_global.axes_data[str(count_of_axes-1)]["delete_list"])-1
                elif(SW_global.current_pos_in_number-1>=0):
                    SW_global.current_axes=SW_global.axes_data[str(key)]["axis_data"]
                    SW_global.current_pos=SW_global.axes_data[str(key)]["cursor_pos"][SW_global.current_pos_in_number-1]
                    SW_global.current_pos_in_number=SW_global.current_pos_in_number-1
            elif(count_of_axes>len(SW_global.axes_data)-1):
                if(SW_global.current_pos_in_number-1<0):
                    if(len(SW_global.axes_data)>0):
                        SW_global.current_axes=SW_global.axes_data[len(SW_global.axes)-1]["axis_data"]
                        SW_global.current_pos=SW_global.axes_data[len(SW_global.axes_data)-1]["cursor_pos"][-2]
                        SW_global.current_pos_in_number=len(SW_global.axes_data[len(SW_global.axes_data)-1]["delete_list"])-1
                else:
                    SW_global.current_pos_in_number=SW_global.current_pos_in_number-1
                    SW_global.current_pos=SW_global.current_pos[-1]
                    SW_global.current_axes=guideline_axes[l]
        except Exception as e:
            print(e)
            pass
        ####### Testing purpose ########

        print("This is after axes_data")
        for j in range(len(SW_global.axes_data)):
            print(SW_global.axes_data[str(j)])
            print("*"*60)
        return
    # # return delete_list1,kern_value_array

def backspaceOperation():
    try:
        if(SW_global.single_click_data!=None):
            SW_global.single_click_data.set_visible(False)
        len1 = len(SW_global.letters_already_written)
        len2 = len1 - 1
        #print("this is start loop variables")
        srt_loop = SW_global.letters_already_written[len2 - 1]
        end_loop = SW_global.letters_already_written[len2]
        for de1 in SW_global.cursor_data:
            de1.set_visible(False)
        #for de1 in SW_global.g


        for i in range(srt_loop, end_loop):
            SW_global.g_val.lines[i].set_visible(False)
            #print(SW_global.g_val.lines[i])
        fig.canvas.draw()

        #print(" This is erase end ")

        ## this is end of erase part #
        del SW_global.letters_already_written[len1-1]
        del SW_global.letters_already_written[len1-2]
        last_input_len = len(delete_list)
        print("This is delete list")
        print(delete_list)
        print(SW_global.kern_list)
        last_glyph = delete_list[last_input_len - 1]
        del delete_list[last_input_len - 1]
        l12 = len(kern_value_array)
        del kern_value_array[l12 - 1]
        kern_x = SW_global.kern_list[0] - 300 - manuscript.x_max[last_glyph]
        #print("This is from back space ")
        #print("This is before kern_x")
        SW_global.kern_list.insert(0, kern_x)
        #print("This is after kern_x")

        if SW_global.connectdot_on_off == 1:
            len11 = len(connectdot_already_applied_array)
            last_value1 = connectdot_already_applied_array[len11 - 1]
            starting_value1 = connectdot_already_applied_array[len11 - 2]
            del connectdot_already_applied_array[len11 - 1]
            del connectdot_already_applied_array[len11 - 2]
            for i in range(starting_value1, last_value1):
                guideline_axes[l].lines[i].set_visible(False)
                #print(guideline_axes[l].lines[i])
            fig.canvas.draw()
            connect_dot_flag_pos = connect_dot_flag_pos - 1

        if SW_global.decisiondot_on_off == 1:
            len11 = len(decisiondot_already_applied_array)
            last_value1 = decisiondot_already_applied_array[len11 - 1]
            starting_value1 = decisiondot_already_applied_array[len11 - 2]
            del decisiondot_already_applied_array[len11 - 1]
            del decisiondot_already_applied_array[len11 - 2]
            for i in range(starting_value1, last_value1):
                guideline_axes[l].lines[i].set_visible(False)
                #print(guideline_axes[l].lines[i])
            fig.canvas.draw()
            decision_dot_flag_pos = decision_dot_flag_pos - 1

        if SW_global.stokearrow_on_off == 1:
            len11 = len(compositedot_already_applied_array)
            last_value1 = compositedot_already_applied_array[len11 - 1]
            starting_value1 = compositedot_already_applied_array[len11 - 2]
            del compositedot_already_applied_array[len11 - 1]
            del compositedot_already_applied_array[len11 - 2]
            for i in range(starting_value1, last_value1):
                guideline_axes[l].lines[i].set_visible(False)
                #print(guideline_axes[l].lines[i])
            fig.canvas.draw()
            stoke_arrow_flag_pos = stoke_arrow_flag_pos - 1

        if SW_global.startdot_on_off == 1:
            len11 = len(startdot_already_applied_array)
            last_value1 = startdot_already_applied_array[len11 - 1]
            starting_value1 = startdot_already_applied_array[len11 - 2]
            del startdot_already_applied_array[len11 - 1]
            del startdot_already_applied_array[len11 - 2]
            for i in range(starting_value1, last_value1):
                guideline_axes[l].lines[i].set_visible(False)
                #print(guideline_axes[l].lines[i])
            ###### Back Space for cursor ##########

            fig.canvas.draw()
            startdot_flag_pos = startdot_flag_pos - 1
       # print("This is before cursor delete")
       # print(SW_global.cursor_data)
       # print(SW_global.cursor_pos)
        del SW_global.cursor_data[len(SW_global.cursor_data)-1]
        del SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
        try:
            visible_item=SW_global.cursor_data[len(SW_global.cursor_data)-1]
           # visible_item.set_visible(True)
        except Exception as e:
            pass
        import numpy as np

        if(len(SW_global.cursor_pos)>1):

            cursor_x1=list(np.full((500),SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
            cursor_y=list(np.linspace(-900,1500,500))
            plot_data=plt.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
            SW_global.single_click_data=plot_data[0]
            ###### Add current_curosr current_axes ##########
            SW_global.current_axes=guideline_axes[l]
            SW_global.current_pos=SW_global.cursor_pos[-1]
            print("It is changed from point 1")
            SW_global.current_pos_in_number=len(SW_global.cursor_pos)-1
        fig.canvas.draw()

    except Exception as e:
        pass
    return



# def set_text_for_text_flow():
#     if(SW_global.text_flow_axes1==None):
#         if(SW_global.text_flow_axes2==None):
#             print("This is current_axes with border ",SW_global.current_axes)
#             SW_global.text_flow_axes1=SW_global.current_axes
#         elif(SW_global.text_flow_axes2==SW_global.current_axes):
#             SW_global.text_flow_axes2=None
#         # elif(SW_global.text_flow_axes2==SW_global.current_axes):
#         #     SW_global.text_flow_axes2=None
#         else:
#             SW_global.text_flow_axes1=SW_global.current_axes
#     else:
#         if(SW_global.text_flow_axes2==None):
#             if(SW_global.text_flow_axes1==SW_global.current_axes):
#                 SW_global.text_flow_axes1=None
#             else:
#                 SW_global.text_flow_axes2=SW_global.current_axes


#     print("This is after operation SW_global.text_flow_axes1 : ",SW_global.text_flow_axes1)
#     print("This is after operation SW_global.text_flow_axes2 : ",SW_global.text_flow_axes2)
#     print("This is SW_global.current_axes :",SW_global.current_axes)

def set_text_for_text_flow():
    # if(((SW_global.text_flow_axes1!=None) and (SW_global.text_flow_axes2!=None)) and ((SW_global.temp_axes==SW_global.text_flow_axes1) or(SW_global.temp_axes==SW_global.text_flow_axes2))):
    #     print("I am in rd part ")
    #     text_flow_features_with_third()



    # else:
    #     if(SW_global.text_flow_axes1==None):
    #         if(SW_global.text_flow_axes2==None):
    #             SW_global.text_flow_axes1=SW_global.current_axes
    #             SW_global.text_flow_box_page1.clear()
    #             checklist=[]
    #             for j in range(len(SW_global.axes_data)):
    #                 checklist.append(SW_global.axes_data[str(j)]["axis_data"])
    #             if((SW_global.current_axes==guideline_axes[l]) or(SW_global.current_axes in checklist)):
    #                 if(len(SW_global.axes_data)>0):
    #                     for j in range(len(SW_global.axes_data)):
    #                         SW_global.text_flow_box_page1.append(SW_global.axes_data[str(j)]["axis_data"])
    #                 SW_global.text_flow_box_page1.append(guideline_axes[l])
    #             else:
    #                 if(len(SW_global.box_data)>0):
    #                     for j in range(len(SW_global.box_data)):
    #                         if(SW_global.text_flow_axes1 in SW_global.box_data[str(j)]["axes_list"]):
    #                             SW_global.text_flow_box_page1=(SW_global.box_data[str(j)]["axes_list"]).copy()
    #                             break

    #         elif(SW_global.text_flow_axes2==SW_global.current_axes):
    #             SW_global.text_flow_axes2=None
    #             SW_global.text_flow_box_page2.clear()
    #         else:
    #             SW_global.text_flow_axes1=SW_global.current_axes
    #             SW_global.text_flow_box_page1.clear()
    #             checklist=[]
    #             for j in range(len(SW_global.axes_data)):
    #                 checklist.append(SW_global.axes_data[str(j)]["axis_data"])
    #             if((SW_global.current_axes==guideline_axes[l]) or(SW_global.current_axes in checklist)):
    #                 if(len(SW_global.axes_data)>0):
    #                     for j in range(len(SW_global.axes_data)):
    #                         SW_global.text_flow_page1.append(SW_global.axes_data[str(j)]["axis_data"])
    #                 SW_global.text_flow_box_page1.append(guideline_axes[l])
    #             else:
    #                 if(len(SW_global.box_data)>0):
    #                     for j in range(len(SW_global.box_data)):
    #                         if(SW_global.text_flow_axes1 in SW_global.box_data[str(j)]["axes_list"]):
    #                             SW_global.text_flow_box_page1=(SW_global.box_data[str(j)]["axes_list"]).copy()
    #                             break
    #     else:
    #         if(SW_global.text_flow_axes2==None):
    #             if(SW_global.text_flow_axes1==SW_global.current_axes):
    #                 SW_global.text_flow_axes1=None
    #                 SW_global.text_flow_box_page1.clear()
    #             else:
    #                 SW_global.text_flow_axes2=SW_global.current_axes
    #                 SW_global.text_flow_box_page2.clear()
    #                 if(SW_global.current_axes==guideline_axes[l]):
    #                     if(len(SW_global.axes_data)>0):
    #                         for j in range(len(SW_global.axes_data)):
    #                             SW_global.text_flow_box_page2.append(SW_global.axes_data[str(j)]["axis_data"])
    #                     SW_global.text_flow_box_page2.append(guideline_axes[l])
    #                 #elif()
    #                 else:
    #                     if(len(SW_global.box_data)>0):
    #                         for j in range(len(SW_global.box_data)):
    #                             if(SW_global.text_flow_axes2 in SW_global.box_data[str(j)]["axes_list"]):
    #                                 SW_global.text_flow_box_page2=(SW_global.box_data[str(j)]["axes_list"]).copy()
    #                                 break

    #     print("This is after operation SW_global.text_flow_axes1 :",SW_global.text_flow_axes1)
    #     print("This is after operation SW_global.text_flow_axes2 :",SW_global.text_flow_axes2)
    #     print("This is after operation SW_global.current_axes :",SW_global.current_axes)
    #     print("This is after operation SW_global.text_flow_box2",SW_global.text_flow_box_page1)
    #     print("This is after operation SW_global.text_flow_box1",SW_global.text_flow_box_page2)
    print("This is box_data")
    print(SW_global.box_data)
#    if(SW_global.max_limit<24):
    print("This is end of box data")
    if(SW_global.max_text<12):
        if(len(SW_global.axes_data)>0):
            if(SW_global.axes_data[str(0)]["axis_data"] in SW_global.text_flow_axes):
                for j in range(len(SW_global.text_flow_axes)): #.axes_data[str(0)]["axis_data"]:
                    if(SW_global.text_flow_axes[j]==SW_global.axes_data[str(0)]["axis_data"]):
                        del SW_global.text_flow_axes[j]
                        SW_global.max_text=SW_global.max_text-1
            else:
                if(guideline_axes[l] in SW_global.text_flow_axes):
                    for j in SW_global.text_flow_axes: 
                        if(j==SW_global.axes_data[str(0)]["axis_data"]):
                            del SW_global.text_flow_axes[j]
                            SW_global.max_text=SW_global.max_text-1
                else:
                    SW_global.max_text=SW_global.max_text-1
                    SW_global.text_flow_axes.append(SW_global.axes_data[str(0)]["axis_data"])
                    SW_global.text_flow_pos.append((SW_global.axes_data[str(0)]["axis_data"]).get_position().bounds)
        else:
            if(guideline_axes[l] in SW_global.text_flow_axes):
                for j in range(len(SW_global.text_flow_axes)): #.axes_data[str(0)]["axis_data"]:

                    if(SW_global.text_flow_axes[j]==guideline_axes[l]):
                        del SW_global.text_flow_axes[j]
                        SW_global.max_text=SW_global.max_text-1
            else:
                SW_global.max_text=SW_global.max_text+1
                SW_global.text_flow_axes.append(guideline_axes[l])
                SW_global.text_flow_pos.append(guideline_axes[l].get_position().bounds)
        print("SW_global.text_flow_axes",SW_global.text_flow_axes)
        print("SW_global.text_flow_pos",SW_global.text_flow_pos)

        if((len(SW_global.axes_data)>0)):
            SW_global.left=((SW_global.back_axes).get_position()).x0
            SW_global.right=((SW_global.back_axes).get_position()).x1
            SW_global.top=((SW_global.back_axes).get_position()).y0
            SW_global.bottom=((SW_global.back_axes).get_position()).y1
            reset_main_selector1()
            #mainselector.extents(SW_global.left,SW_global.right,SW_global.top,SW_global.bottom)
        else:
            SW_global.left=((guideline_axes[l]).get_position()).x0
            SW_global.right=((guideline_axes[l]).get_position()).x1
            SW_global.top=((guideline_axes[l]).get_position()).y0
            SW_global.bottom=((guideline_axes[l]).get_position()).y1
            reset_main_selector1()


    return




def onclick(event):
    global lft_gd, rht_gd, tp_gd, btm_gd, l, key_c
    global tb_height, multiimg_flg, pre_l, pre_b
    global click_left, click_bottom, click_x, click_y

    mainselector.set_visible(True)
    click_left, click_bottom = click_x, click_y

    start_arrow_button.configure(state=NORMAL)
    stoke_arrows_button.configure(state=NORMAL)
    connect_dot_button.configure(state=NORMAL)
    stoke_arrows_button.configure(state=NORMAL)
    decision_dot_button.configure(state=NORMAL)
    guidelines_button.configure(state=NORMAL)
    background_button.configure(state=NORMAL)
    letter_dot_density_button.configure(state=NORMAL)
    letter_shadding_button.configure(state=NORMAL)
    background_menu_button.configure(state=NORMAL)
    connect_dot_menu_button.configure(state=NORMAL)
    decision_dot_menu_button.configure(state=NORMAL)
    start_arrow_menu_button.configure(state=NORMAL)
    stoke_arrows_menu_button.configure(state=NORMAL)
    guidelines_menu_button.configure(state=NORMAL)
    letter_dot_density_menu_button.configure(state=NORMAL)
    letter_shadding_menu_button.configure(state=NORMAL)
    border_art_button.configure(state=NORMAL)
    include_following_text_button.configure(state=NORMAL)
    letter_outline_menu_button.configure(state=NORMAL)
    color_letter_menu_button.configure(state=NORMAL)
    color_letter_button.configure(state=NORMAL)
    background_menu_button.configure(background='skyblue')
    connect_dot_menu_button.configure(background='skyblue')
    decision_dot_menu_button.configure(background='skyblue')
    start_arrow_menu_button.configure(background='skyblue')
    stoke_arrows_menu_button.configure(background='skyblue')
    guidelines_menu_button.configure(background='skyblue')
    letter_dot_density_menu_button.configure(background='skyblue')
    letter_shadding_menu_button.configure(background='skyblue')
    guidelines_button.configure(background='skyblue')
    letter_dot_density_button.configure(background='skyblue')
    letter_shadding_button.configure(background='skyblue')

    if SW_global.firstline_color == True or SW_global.secondline_color == True or SW_global.thirdline_color == True or SW_global.forthline_color == True:
        color_letter_button.configure(background='skyblue')
    else:
        color_letter_button.configure(background='#d9d9d9')

    if SW_global.startdot_on_off == 1:
        start_arrow_button.configure(background='skyblue')

    else:
        start_arrow_button.configure(background='#d9d9d9')

    if SW_global.stokearrow_on_off == 1:
        stoke_arrows_button.configure(background='skyblue')
    else:
        stoke_arrows_button.configure(background='#d9d9d9')

    if SW_global.connectdot_on_off == 1:
        connect_dot_button.configure(background='skyblue')
    else:
        connect_dot_button.configure(background='#d9d9d9')

    if SW_global.decisiondot_on_off == 1:
        decision_dot_button.configure(background='skyblue')
    else:
        decision_dot_button.configure(background='#d9d9d9')

    if SW_global.guidelines_toparea == 1 or SW_global.guidelines_middlearea == 1 or SW_global.guidelines_descenderarea == 1:
        background_button.configure(background='skyblue')
    else:
        background_button.configure(background='#d9d9d9')

    if event.inaxes == fig_axes:
        SW_global.figvalue = True

        SW_global.left = 0.01
        SW_global.right = 0.01
        SW_global.top = 0.01
        SW_global.bottom = 0.01

        start_arrow_button.configure(background='#d9d9d9')
        guidelines_button.configure(background='#d9d9d9')
        stoke_arrows_button.configure(background='#d9d9d9')
        letter_outline_button.configure(background='#d9d9d9')
        decision_dot_button.configure(background='#d9d9d9')
        connect_dot_button.configure(background='#d9d9d9')
        color_letter_button.configure(background='#d9d9d9')
        background_button.configure(background='#d9d9d9')
        border_art_button.configure(background='#d9d9d9')
        background_button.configure(background='#d9d9d9')
        letter_dot_density_button.configure(background='#d9d9d9')
        letter_shadding_button.configure(background='#d9d9d9')

        background_menu_button.configure(background='#d9d9d9')
        color_letter_menu_button.configure(background='#d9d9d9')
        connect_dot_menu_button.configure(background='#d9d9d9')
        decision_dot_menu_button.configure(background='#d9d9d9')
        start_arrow_menu_button.configure(background='#d9d9d9')
        stoke_arrows_menu_button.configure(background='#d9d9d9')
        guidelines_menu_button.configure(background='#d9d9d9')
        letter_dot_density_menu_button.configure(background='#d9d9d9')
        letter_shadding_menu_button.configure(background='#d9d9d9')

        background_menu_button.configure(state=DISABLED)
        color_letter_menu_button.configure(state=DISABLED)
        connect_dot_menu_button.configure(state=DISABLED)
        decision_dot_menu_button.configure(state=DISABLED)
        start_arrow_menu_button.configure(state=DISABLED)
        stoke_arrows_menu_button.configure(state=DISABLED)
        guidelines_menu_button.configure(state=DISABLED)
        letter_dot_density_menu_button.configure(state=DISABLED)
        letter_shadding_menu_button.configure(state=DISABLED)
        include_following_text_button.configure(state=DISABLED)
        letter_dot_density_button.configure(state=DISABLED)
        letter_shadding_button.configure(state=DISABLED)

        start_arrow_button.configure(state=DISABLED)
        guidelines_button.configure(state=DISABLED)
        stoke_arrows_button.configure(state=DISABLED)
        letter_outline_button.configure(state=DISABLED)
        decision_dot_button.configure(state=DISABLED)
        connect_dot_button.configure(state=DISABLED)
        color_letter_button.configure(state=DISABLED)
        background_button.configure(state=DISABLED)
        border_art_button.configure(state=DISABLED)
        start_arrow_button.configure(state=DISABLED)
        letter_outline_menu_button.configure(state=DISABLED)

        mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
        fig.canvas.draw()

   # for key, val in fnl_g.items():
   #     if val == event.inaxes:
   #         SW_global.g_key = key
   #         SW_global.g_val = val
    if event.inaxes == SW_global.g_val:

        multiimg_flg = False
        SW_global.gdaxes = SW_global.g_key

        if guideline_axes[l].get_visible() == False:
            SW_global.gdaxes = 0
            SW_global.imgaxes = 0
        else:

            SW_global.imgaxes = 0
            if SW_global.gd_flag2:
                SW_global.left = SW_global.new_left_axes2
                SW_global.right = SW_global.new_right_axes2
                SW_global.top = SW_global.new_top_axes2
                SW_global.bottom = SW_global.new_bottom_axes2
                selector_dict[key_c] = [SW_global.left, SW_global.right, SW_global.bottom, SW_global.top]
            else:
                SW_global.left = 0.99
                SW_global.right = 0.01
                SW_global.top = sl_t + 0.04
                SW_global.bottom = sl_b + 0.04
                selector_dict[key_c] = [SW_global.left, SW_global.right, SW_global.bottom, SW_global.top]

        key_c = SW_global.g_key
   #     mainselector.extents = (
    #    selector_dict[key_c][0], selector_dict[key_c][1], selector_dict[key_c][2], selector_dict[key_c][3])
        fig.canvas.draw()

    # --------------------------------------------------------------------------------------------------------------

    if event.inaxes == image_axes[y]:
        multiimg_flg = False
        if image_axes[y].get_visible() == False:
            SW_global.imgaxes = 0
            SW_global.gdaxes = 0
        else:
            SW_global.imgaxes = 1
            SW_global.gdaxes = 0
            if SW_global.img_flag1:
                SW_global.left, SW_global.right, SW_global.top, SW_global.bottom = SW_global.img_left_axes1, SW_global.img_right_axes1, SW_global.img_top_axes1, SW_global.img_bottom_axes1

            else:
                SW_global.left = 0.02
                SW_global.right = 0.20
                SW_global.top = 0.79
                SW_global.bottom = 0.65

            mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
            mainselector.update()
            fig.canvas.draw()

    if multiimg_flg:
        SW_global.imgaxes = 2
        SW_global.gdaxes = 0
        if SW_global.img_flag2:
            SW_global.left, SW_global.right, SW_global.top, SW_global.bottom = SW_global.img_left_axes2, SW_global.img_right_axes2, SW_global.img_top_axes2, SW_global.img_bottom_axes2
        else:
            SW_global.left = (pre_l - 0.02)
            SW_global.right = 0.24
            SW_global.top = 0.76
            SW_global.bottom = (pre_b + 0.01)
        print("%%%%%%%%5", event.inaxes)
        mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
        mainselector.update()
        fig.canvas.draw()

    # ---------------------------------------------------------------------------------------------------------

    if event.button == 3:
        if SW_global.figvalue == False and SW_global.gdaxes == key_c and SW_global.gd_flag2 == True:
            rightclick_menu.post(click_left, click_bottom)
            print("working right click")
        elif SW_global.figvalue == True:
            rightclick_menu.unpost()
            rightclick_outermenu.post(click_left, click_bottom)
        elif SW_global.imgaxes == 1 or SW_global.imgaxes == 2 and SW_global.img_flag2 == True:
            rightclick_menu.unpost()
            rightclick_outermenu.post(click_left, click_bottom)


def onselect(eclick, erelease):
    global tb_height, key_c
    global new_left, new_bottom
    new_left = eclick.xdata
    new_right = erelease.xdata
    new_top = erelease.ydata
    new_bottom = eclick.ydata

    print("----------------**Mouse Event**-------------------")
    print("mouse click X : left ", new_left)
    print("mouse click Y : bottom:", new_bottom)
    print("mouse release X : right: ", new_right)
    print("mouse release Y : top ", new_top)
    #pos11=SW_global.back_axes.get_position()
    #pos2=[new_left,new_bottom,pos11.width,pos11.height]
    #SW_global.back_axes.set_position(pos2)
    if(len(SW_global.axes_data)>0):
        print("this is o1 data",(SW_global.axes_data[str(0)]["axis_data"]).get_position())
    else:
        print("this is o1 data",(guideline_axes[l]).get_position())
    counter1=0
    counter2=0
    pos_check=new_bottom-0.001
    #temp_pos=None
    if(len(SW_global.axes_data)>0):
        for j in range(len(SW_global.axes_data)):
            temp_pos=(SW_global.axes_data[str(j)]["axis_data"]).get_position()
            temp_check=[new_left,new_bottom+(counter1*temp_pos.height),temp_pos.width,temp_pos.height]
            print("I am in check point 2345555555"*10)
            (SW_global.axes_data[str(j)]["axis_data"]).set_position(temp_check)
            counter1=counter1+1
    temp_pos=guideline_axes[l].get_position()
    #print("This is check ",temp_check)

    temp_check1=[new_left,new_bottom-(counter1*temp_pos.height),temp_pos.width,temp_pos.height]
    (guideline_axes[l]).set_position(temp_check1)
    o1=None
    if(len(SW_global.axes_data)>0):
        o1=(SW_global.axes_data[str(0)]["axis_data"]).get_position()
    else:
        print("i am for guideline_axes[l]")
        o1=guideline_axes[l].get_position()
    print("This is o1",o1)

    pos21=[o1.x0,o1.y0,((SW_global.back_axes).get_position()).width,((SW_global.back_axes).get_position()).height]
    SW_global.back_axes.set_position(pos21)
    SW_global.left=(SW_global.back_axes.get_position()).x0
    SW_global.right=(SW_global.back_axes.get_position()).x1
    SW_global.top=(SW_global.back_axes.get_position()).y0
    SW_global.bottom=(SW_global.back_axes.get_position()).y1

    #mainselector.extents=((SW_global.back_axes.get_position()).x0,(SW_global.back_axes.get_position()).x1,(SW_global.back_axes.get_position()).y0,(SW_global.back_axes.get_position()).y1)
    fig.canvas.draw()








#     if key_c == SW_global.gdaxes:
#         SW_glaobl.gd_flag2 = True
#         SW_global.new_left_axes2, SW_global.new_right_axes2, SW_global.new_bottom_axes2, SW_global.new_top_axes2 = new_left, new_right, new_bottom, new_top

#         g_width = (new_right - new_left)
#         g_height = (new_top - new_bottom)
#         SW_global.g_val.set_position([new_left, new_bottom, g_width, g_height], which='both')
# #        pos2=[new_left,new_bottom.ydata,pos11.width,pos11.height]
# #        SW_global.back_axes.set_position(pos2)

#         selector_dict.update({key_c: [new_left, new_right, new_bottom, new_top]})
#         for j in range(len(SW_global.axes_data)):
#             #new_left=new_left-0.15
#             new_bottom=new_bottom+0.15
#             (SW_global.axes_data[str(j)]["axis_data"]).set_position([new_left, new_bottom, g_width, g_height], which='both')

#     else:
#         print(" Guideline ERROR.........")

#     # if SW_global.gdaxes == key_c:
#     #     SW_global.gd_flag1 = True
#     #     tb_height = 0.15
#     #     SW_global.new_left_axes1, SW_global.new_right_axes1, SW_global.new_bottom_axes1, SW_global.new_top_axes1 = new_left, new_right, new_bottom, new_top
#     #     guideline_axes[l].set_position([new_left, new_bottom, (new_right - new_left), tb_height], which='both')
#     #
#     #     if SW_global.new_gd == 1:
#     #         guideline_axes[l].set_position([new_left, (new_bottom + 0.15), (new_right - new_left), tb_height],
#     #                                        which='both')
#     #         guideline_axes1_1.set_position([new_left, new_bottom, (new_right - new_left), tb_height], which='both')
#     #
#     #     elif SW_global.gird_flag == True:
#     #         fig_axes.axhline(y=new_top, color='red')
#     #         fig_axes.axvline(x=new_left, color='red')

#     # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#     if SW_global.imgaxes == 1:
#         SW_global.img_flag1 = True
#         SW_global.img_left_axes1, SW_global.img_right_axes1, SW_global.img_top_axes1, SW_global.img_bottom_axes1 = new_left, new_right, new_top, new_bottom
#         image_axes[y].set_position([new_left, new_bottom, (new_right - new_left), (new_top - new_bottom)],
#                                    which='both')
#     elif SW_global.imgaxes == 2:
#         SW_global.img_flag2 = True
#         SW_global.img_left_axes2, SW_global.img_right_axes2, SW_global.img_top_axes2, SW_global.img_bottom_axes2 = new_left, new_right, new_top, new_bottom
#         image_axes2.set_position([new_left, new_bottom, (new_right - new_left), (new_top - new_bottom)],
#                                  which='both')
#     else:
#         print(" Img ERROR.........")
    # check=(mainselector.corners)[1]
    # check1=[round(i,2) for i in (mainselector.corners)[1]]
    # check12=[round(i,2) for i in (mainselector.edge_centers)[1]]
    # check13=[round(i,2) for i in (mainselector.edge_centers)[0]]
    # print("This is edge center",mainselector.edge_centers)
    # print(round(SW_global.click_y,2))
    # if(round(SW_global.click_y,2) in check1):
    #     print("ok")
    # elif((round(SW_global.click_y,2) in check12) and(round(SW_global.click_x,2) in check13)):
    #     print("ok _edge center")
    # else:
    #     mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
    #     mainselector.update()
    fig.canvas.draw()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MenuBar Code <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
mnbr = Menu(SW_Main_UI)
SW_Main_UI.config(menu=mnbr)

file = Menu(mnbr, tearoff=0)
file.add_command(label="New", command=newfile, accelerator="Ctrl+N")
file.add_command(label="Open", command=openfile)
file.add_command(label="Close", command=donothing)
file.add_separator()
file.add_command(label="Open Lesson", command=donothing)
file.add_separator()
file.add_command(label="Save", command=saveasfile, accelerator="Ctrl+S")
file.add_command(label="Save as", command=saveasfile)
file.add_separator()
file.add_command(label="Print...", command=donothing, accelerator="Ctrl+P")
file.add_command(label="Print Preview", command=donothing)
file.add_command(label="Print Setup...", command=donothing)
file.add_separator()
file.add_command(label="Recent File", command=donothing)
file.add_separator()
file.add_command(label="Exit", command= on_exit)

edit = Menu(mnbr, tearoff=0)
edit.add_command(label="undo", command=donothing)
edit.add_command(label="Redo", command=donothing)
edit.add_separator()
edit.add_command(label="Cut", command=donothing, accelerator="Ctrl+X")
edit.add_command(label="Copy", command=donothing, accelerator="Ctrl+C")
edit.add_command(label="Paste", command=donothing, accelerator="Ctrl+V")
edit.add_separator()
edit.add_command(label="Delete Box", command=delguideline, accelerator="Ctrl-Del")
edit.add_command(label="Delete Page", command=donothing)
edit.add_separator()
edit.add_command(label="Go To...", command=donothing)
edit.add_separator()
edit.add_command(label="Select All Text", command=donothing)

view = Menu(mnbr, tearoff=0)
view.add_command(label="Zoom...", command=zoom_wp)
view.add_separator()
vm1 = IntVar()
vm1.set(0)
vm2 = IntVar()
vm2.set(0)
vm3 = IntVar()
vm3.set(0)
view.add_checkbutton(label="Toolbar", onvalue=vm1, command = toolbarhideshow)
view.add_checkbutton(label="Property Bar", onvalue=vm2, command = propertybarhideshow)
view.add_checkbutton(label="Status Bar", onvalue=vm3, command = statusbarhideshow)
view.add_separator()
view.add_command(label="Show Grid", command=gird_on)
view.add_command(label="Snap to Grid", command=donothing)
view.add_separator()
view.add_command(label="Redraw All", command=donothing)

insert = Menu(mnbr, tearoff=0)
insert.add_command(label="Page", command=insert_page_option_mw)
insert.add_command(label="Text", command=add_text_box)
insert.add_command(label="Art", command=add_new_art_box)

frmt = Menu(mnbr, tearoff=0)
frmt.add_command(label="Font...", command=font_wp)
frmt.add_checkbutton(label="Allow Windows Fonts", onvalue=1, offvalue=False)
frmt.add_separator()

artchild = Menu(frmt, tearoff=0)
artchild.add_checkbutton(label="Replace...", state = DISABLED)
artchild.add_checkbutton(label="Maintain Proportions", state = DISABLED)
frmt.add_cascade(label="Art", menu=artchild)

frmt.add_command(label="Delete Box", command=delguideline)

centerBoxChild = Menu(frmt, tearoff=0)
centerBoxChild.add_checkbutton(label="On Page")
centerBoxChild.add_checkbutton(label="Horizontal")
centerBoxChild.add_checkbutton(label="Vertically")
frmt.add_cascade(label="Center Box", menu=centerBoxChild)

BorderChild = Menu(frmt, tearoff=0)
BorderChild.add_command(label="Border Art...", command=borderart_wp)
BorderChild.add_separator()
BorderChild.add_checkbutton(label="None", command=snln0)
BorderChild.add_checkbutton(label="Single line 1pt", command=snln1)
BorderChild.add_checkbutton(label="Single line 2pt", command=snln2)
BorderChild.add_checkbutton(label="Single line 3pt", command=snln3)
BorderChild.add_checkbutton(label="Single line 6pt", command=snln6)
BorderChild.add_checkbutton(label="Double line 1pt")
BorderChild.add_checkbutton(label="Double line 2pt")
BorderChild.add_checkbutton(label="Double line 3pt")
BorderChild.add_checkbutton(label="Double line 6pt")
frmt.add_cascade(label="Borders", menu=BorderChild)

frmt.add_command(label="Including in Flowing Text", command=set_text_for_text_flow)
frmt.add_separator()

GuidelinesChild = Menu(frmt, tearoff=0)
GuidelinesChild.add_checkbutton(label="Top",command=guideline_del_asenderline)
GuidelinesChild.add_checkbutton(label="Middle",command=guideline_del_middleline)
GuidelinesChild.add_checkbutton(label="Baseline",command=guideline_del_baseline)
GuidelinesChild.add_checkbutton(label="Descender",command=guideline_del_descenderline)
frmt.add_cascade(label="Guidelines", menu=GuidelinesChild)

GuideThickChild_1 = Menu(frmt, tearoff=0)
GuideThickChild_2 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_2.add_checkbutton(label="Normal")
GuideThickChild_2.add_checkbutton(label="Thick")
GuideThickChild_2.add_checkbutton(label="Thicker")
GuideThickChild_2.add_checkbutton(label="Thickest")
GuideThickChild_1.add_cascade(label="All", menu=GuideThickChild_2)

GuideThickChild_3 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_3.add_checkbutton(label="Normal", command=on_click_guide_clr_change_help_function_top_0)
GuideThickChild_3.add_checkbutton(label="Thick", command=on_click_guide_clr_change_help_function_top_1)
GuideThickChild_3.add_checkbutton(label="Thicker", command=on_click_guide_clr_change_help_function_top_2)
GuideThickChild_3.add_checkbutton(label="Thickest", command=on_click_guide_clr_change_help_function_top_3)
GuideThickChild_1.add_cascade(label="Top", menu=GuideThickChild_3)

GuideThickChild_4 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_4.add_checkbutton(label="Normal", command=on_click_guide_clr_change_help_function_middle_0)
GuideThickChild_4.add_checkbutton(label="Thick", command=on_click_guide_clr_change_help_function_middle_1)
GuideThickChild_4.add_checkbutton(label="Thicker", command=on_click_guide_clr_change_help_function_middle_2)
GuideThickChild_4.add_checkbutton(label="Thickest", command=on_click_guide_clr_change_help_function_middle_3)
GuideThickChild_1.add_cascade(label="Middle", menu=GuideThickChild_4)

GuideThickChild_5 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_5.add_checkbutton(label="Normal", command=on_click_guide_clr_change_help_function_base_0)
GuideThickChild_5.add_checkbutton(label="Thick", command=on_click_guide_clr_change_help_function_base_1)
GuideThickChild_5.add_checkbutton(label="Thicker", command=on_click_guide_clr_change_help_function_base_2)
GuideThickChild_5.add_checkbutton(label="Thickest", command=on_click_guide_clr_change_help_function_base_3)
GuideThickChild_1.add_cascade(label="Base", menu=GuideThickChild_5)

GuideThickChild_6 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_6.add_checkbutton(label="Normal", command=on_click_guide_clr_change_help_function_descender_0)
GuideThickChild_6.add_checkbutton(label="Thick", command=on_click_guide_clr_change_help_function_descender_1)
GuideThickChild_6.add_checkbutton(label="Thicker", command=on_click_guide_clr_change_help_function_descender_2)
GuideThickChild_6.add_checkbutton(label="Thickest", command=on_click_guide_clr_change_help_function_descender_3)
GuideThickChild_1.add_cascade(label="Bottom", menu=GuideThickChild_6)

frmt.add_cascade(label="Guidelines Thickness", menu=GuideThickChild_1)

AreaHighLightChild = Menu(frmt, tearoff=0)
AreaHighLightChild.add_checkbutton(label="Top", command = guidelines_toparea_submenu)
AreaHighLightChild.add_checkbutton(label="Middle", command = guidelines_middlearea_submenu)
AreaHighLightChild.add_checkbutton(label="Descender", command = guidelines_descenderarea_submenu)
frmt.add_cascade(label="Area Highlight", menu=AreaHighLightChild)

frmt.add_separator()

LetterShadingChild = Menu(frmt, tearoff=0)
LetterShadingChild.add_checkbutton(label="25%")
LetterShadingChild.add_checkbutton(label="50%")
LetterShadingChild.add_checkbutton(label="75%")
LetterShadingChild.add_checkbutton(label="100%")
LetterShadingChild.add_separator()
LetterShadingChild.add_command(label="Options...", command=letter_shading_option_mw)
frmt.add_cascade(label="Letter Shading", menu=LetterShadingChild)

StrokeArrowChild = Menu(frmt, tearoff=0)
StrokeArrowChild.add_checkbutton(label="On", command=main3)
StrokeArrowChild.add_command(label="Options...", command=stoke_arrows_option_mw)
frmt.add_cascade(label="Stroke Arrows", menu=StrokeArrowChild)

DotDensityChild = Menu(frmt, tearoff=0)
DotDensityChild.add_checkbutton(label="25%")
DotDensityChild.add_checkbutton(label="50%")
DotDensityChild.add_checkbutton(label="75%")
DotDensityChild.add_checkbutton(label="100%")
DotDensityChild.add_separator()
DotDensityChild.add_command(label="Options...", command=letter_dot_density_option_mw)
frmt.add_cascade(label="Dot Density", menu=DotDensityChild)

DecisionDotChild = Menu(frmt, tearoff=0)
DecisionDotChild.add_checkbutton(label="On", command=main)
DecisionDotChild.add_checkbutton(label="Connect Dots", command=main4)
frmt.add_cascade(label="Decision Dots", menu=DecisionDotChild)

frmt.add_checkbutton(label="Start Dot", command=main1)
frmt.add_checkbutton(label="Letter Outline", command=donothing)
frmt.add_checkbutton(label="Color Letters", command=donothing)
frmt.add_separator()

WordSpacingChild = Menu(frmt, tearoff=0)
WordSpacingChild.add_checkbutton(label="Regular")
WordSpacingChild.add_checkbutton(label="Wide")
frmt.add_cascade(label="Word Spacing", menu=WordSpacingChild)

tools = Menu(mnbr, tearoff=0)
tools.add_command(label="Spell Check...", command=donothing)
tools.add_separator()
tools.add_command(label="Default Setting...", command=donothing)
tools.add_command(label="Default Space Width...", command=donothing)
tools.add_command(label="Default Fonts...", command=donothing)

window = Menu(mnbr, tearoff=0)
window.add_command(label="New Window", command=donothing)
window.add_command(label="Cascade", command=donothing)
window.add_command(label="Tile", command=donothing)
window.add_separator()
window.add_command(label="show based on new doc open", command=donothing)

hlp = Menu(mnbr, tearoff=0)
hlp.add_command(label="Help Topics", command=ShowManualPdf)

if lin_flag == True:
    hlp.add_command(label="Purchase Online", command=lin_purchase_wp)
    hlp.add_command(label="Activate License", command=valid_key_wp)
    hlp.add_command(label="About Startwrite...", command=aboutstartwrite)
else:
    hlp.add_command(label="About Startwrite...", command=aboutstartwrite)

mnbr.add_cascade(label="File", menu=file)
mnbr.add_cascade(label="Edit", menu=edit)
mnbr.add_cascade(label="View", menu=view)
mnbr.add_cascade(label="Insert", menu=insert)
mnbr.add_cascade(label="Format", menu=frmt)
mnbr.add_cascade(label="Tools", menu=tools)
mnbr.add_cascade(label="Window", menu=window)
mnbr.add_cascade(label="Help", menu=hlp)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Disabled Matplotlib default  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
plt.rcParams['keymap.save'].remove('s')
plt.rcParams['keymap.fullscreen'].remove('f')
plt.rcParams['keymap.back'].remove('left')
plt.rcParams['keymap.forward'].remove('right')
plt.rcParams['keymap.quit'].remove('q')
plt.rcParams['keymap.pan'].remove('p')
plt.rcParams['axes.formatter.useoffset'] = False
plt.rcParams['toolbar'] = 'None'
plt.rcParams['keymap.xscale'].remove('k')
# *************************************************** End ********************************************************

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Creating Fig <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
fig = plt.figure()

fig_axes = fig.add_axes([0, 0, 1, 1])

fig_axes.patch.set_alpha(0.3)

# [left, bottom, width, height]
n = 1
guideline_axes = np.empty([n], dtype=object)

guideline_axes1_1 = fig.add_axes([0.00001, 0.0001, 0, 0])
guideline_axes1_1.set_visible(False)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# IMG axes

image_axes2 = fig.add_axes([0.0002, 0.0002, 0, 0])
image_axes2.set_visible(False)

m = 1
y = 0
image_axes = np.empty([m], dtype=object)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

base_x = [0, (1500 * SW_global.scl)]
base_y = [0, 0]
median_x = [0, (1500 * SW_global.scl)]
median_y = [757, 757]
descender_x = [0, (1500 * SW_global.scl)]
descender_y = [-747, -747]
ascender_x = [0, (1500 * SW_global.scl)]
ascender_y = [1510, 1510]

f_btm = 0.05

if wd < 1200:
    SW_global.u_r = 1
    f_w = 6
    f_h = 8
elif wd > 1200:
    SW_global.w_r = 1
    f_w = 8
    f_h = 9

fig.set_size_inches(f_w, f_h)

fig.text(0.98, 0.009, EtsPyTech.dev_details(),
         fontsize=7, color='black',
         ha='right', va='bottom', alpha=0.090)

if restaurar_wn:
    addScrollingFigure(fig, writingareaframe)
else:
    addScrollingFigure(fig, sub)

# Rectangle Selector is Define Here
print("$%$%$%$%"*20)
mainselector = widgets.RectangleSelector(fig_axes, onselect,
                                         drawtype='box', interactive=True,
                                         spancoords='pixels', minspany=110, maxdist=50, button=1,
                                         rectprops=dict(facecolor='white', linestyle='--',
                                                        edgecolor='black', alpha=0.45, fill=True))

# Initial Selector Position is Setting Here
mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)

selector_dict = {g_c: [SW_global.left, SW_global.right, SW_global.bottom, SW_global.top]}
print("Dipu : ", selector_dict[g_c])
#SW_global.back_axes=plt.axes([0,0,0.1,0.3])

##default_guideline(guideline_axes[l])
call_multigudeline()
##cursor_line = MultiCursor(fig.canvas, (fig_axes, ), color='r',
##                          lw=1, horizOn=True, vertOn=True)

##cursor_line.set_active(False)

##fig.canvas.mpl_connect('button_press_event', onpick)
print("check point13")
fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('scroll_event', onscroll)
fig.canvas.mpl_connect('button_press_event',onclick2)
fig.canvas.mpl_connect('button_release_event',onrelease)
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_press_event', kChange) ############### Adding function for press of mouse ############
canvas.configure(background='grey')
# *************************************************** End ********************************************************

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Right Click Pop Up <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#************************************************ Right-Click Pop-Up Menu ***************************************************#

def show_info(txt):
    infolbl.configure(text = txt)

def hello():
    print("hello!")




#rightclickmenu
# create a pop up menu

rightclick_outermenu = Menu(writingareaframe, tearoff=0)
rightclick_outermenu.add_command(label="Cut", command=hello, state=DISABLED)
rightclick_outermenu.add_command(label="Copy", command=hello, state=DISABLED)
rightclick_outermenu.add_command(label="Paste", command=hello, state=DISABLED)
rightclick_outermenu.add_command(label="Select All Text", command=hello, state=DISABLED)
rightclick_outermenu.add_command(label="Insert Special Characters", command=insert_special_character)
rightclick_outermenu.add_separator()
rightclick_outermenu.add_command(label="Delete Box", state=DISABLED)

centerboxsubmenu2 = Menu(rightclick_outermenu, tearoff=0)
centerboxsubmenu2.add_checkbutton(label="On Page", command=hello)
centerboxsubmenu2.add_checkbutton(label="Horizontial", command=hello)
centerboxsubmenu2.add_checkbutton(label="Vertically", command=hello)

rightclick_outermenu.add_cascade(label="Center Box", menu=centerboxsubmenu2)

rightclick_outermenu.add_separator()
rightclick_outermenu.add_checkbutton(label="Show Grid", command=gird_on)
rightclick_outermenu.add_checkbutton(label="Snap to Grid", command=hello)
rightclick_outermenu.add_separator()

rightclick_outermenu.add_command(label="Insert Page", command=insert_page_option_mw)
rightclick_outermenu.add_command(label="Insert Text", command=add_text_box)
rightclick_outermenu.add_command(label="Insert Art", command=add_new_art_box)
rightclick_outermenu.add_separator()
rightclick_outermenu.add_command(label="Replace Art", command=replace_art_box)
rightclick_outermenu.add_checkbutton(label="Maintain protion", onvalue=1, offvalue= SW_global.viewvalue1, command=hello, state=DISABLED)

bordersubmenu2 = Menu(rightclick_outermenu, tearoff=0)
bordersubmenu2.add_command(label="Border Art...", command=borderart_wp)
bordersubmenu2.add_separator()
bordersubmenu2.add_checkbutton(label="None", command=snln0, state=DISABLED)
bordersubmenu2.add_checkbutton(label="Single Line 1", command=snln1, state=DISABLED)
bordersubmenu2.add_checkbutton(label="Single Line 2", command=snln2, state=DISABLED)
bordersubmenu2.add_checkbutton(label="Single Line 3", command=snln3, state=DISABLED)
bordersubmenu2.add_checkbutton(label="Single Line 6", command=snln6, state=DISABLED)
bordersubmenu2.add_checkbutton(label="Double Line 1", command=hello, state=DISABLED)
bordersubmenu2.add_checkbutton(label="Double Line 2", command=hello, state=DISABLED)
bordersubmenu2.add_checkbutton(label="Double Line 3", command=hello, state=DISABLED)
bordersubmenu2.add_checkbutton(label="Double Line 6", command=hello, state=DISABLED)

rightclick_outermenu.add_cascade(label="Box Frame", menu=bordersubmenu2)
# -----------------------------------------------------------------------------------------------------------

rightclick_menu = Menu(writingareaframe, tearoff=0)
rightclick_menu.add_command(label="Undo", command=hello)
rightclick_menu.add_command(label="Redo", command=hello)
rightclick_menu.add_separator()
rightclick_menu.add_command(label="Cut", command=hello)
rightclick_menu.add_command(label="Copy", command=hello)
rightclick_menu.add_command(label="Paste", command=hello)
rightclick_menu.add_command(label="Select All Text", command=hello)
rightclick_menu.add_command(label="Insert Special Characters", command=insert_special_character)
rightclick_menu.add_separator()
rightclick_menu.add_command(label="Delete Box", command=delguideline)

centerboxsubmenu1 = Menu(rightclick_menu, tearoff=0)
centerboxsubmenu1.add_checkbutton(label="On Page", command=hello)
centerboxsubmenu1.add_checkbutton(label="Horizontial", command=hello)
centerboxsubmenu1.add_checkbutton(label="Vertically", command=hello)

rightclick_menu.add_cascade(label="Center Box", menu=centerboxsubmenu1)

bordersubmenu1 = Menu(rightclick_menu, tearoff=0)
bordersubmenu1.add_command(label="Border Art...", command=borderart_wp)
bordersubmenu1.add_separator()
bordersubmenu1.add_checkbutton(label="None", command=snln0)
bordersubmenu1.add_checkbutton(label="Single Line 1", command=snln1)
bordersubmenu1.add_checkbutton(label="Single Line 2", command=snln2)
bordersubmenu1.add_checkbutton(label="Single Line 3", command=snln3)
bordersubmenu1.add_checkbutton(label="Single Line 6", command=snln6)
bordersubmenu1.add_checkbutton(label="Double Line 1", command=hello)
bordersubmenu1.add_checkbutton(label="Double Line 2", command=hello)
bordersubmenu1.add_checkbutton(label="Double Line 3", command=hello)
bordersubmenu1.add_checkbutton(label="Double Line 6", command=hello)

rightclick_menu.add_cascade(label="Borders", menu=bordersubmenu1)
rightclick_menu.add_command(label="Include in Flowing Text", command=hello)
rightclick_menu.add_separator()

submenu1 = Menu(rightclick_menu, tearoff=0)
submenu1.add_checkbutton(label="Top", command=guideline_del_asenderline)
submenu1.add_checkbutton(label="Middle", command=guideline_del_middleline)
submenu1.add_checkbutton(label="Baseline", command=guideline_del_baseline)
submenu1.add_checkbutton(label="Descender", command=guideline_del_descenderline)
rightclick_menu.add_cascade(label="Guidelines", menu=submenu1)

GuideThickChild_1 = Menu(rightclick_menu, tearoff=0)
GuideThickChild_2 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_2.add_checkbutton(label="Normal")
GuideThickChild_2.add_checkbutton(label="Thick")
GuideThickChild_2.add_checkbutton(label="Thicker")
GuideThickChild_2.add_checkbutton(label="Thickest")
GuideThickChild_1.add_cascade(label="All", menu=GuideThickChild_2)

GuideThickChild_3 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_3.add_checkbutton(label="Normal", command=on_click_guide_clr_change_help_function_top_0)
GuideThickChild_3.add_checkbutton(label="Thick", command=on_click_guide_clr_change_help_function_top_1)
GuideThickChild_3.add_checkbutton(label="Thicker", command=on_click_guide_clr_change_help_function_top_2)
GuideThickChild_3.add_checkbutton(label="Thickest", command=on_click_guide_clr_change_help_function_top_3)
GuideThickChild_1.add_cascade(label="Top", menu=GuideThickChild_3)

GuideThickChild_4 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_4.add_checkbutton(label="Normal", command=on_click_guide_clr_change_help_function_middle_0)
GuideThickChild_4.add_checkbutton(label="Thick", command=on_click_guide_clr_change_help_function_middle_1)
GuideThickChild_4.add_checkbutton(label="Thicker", command=on_click_guide_clr_change_help_function_middle_2)
GuideThickChild_4.add_checkbutton(label="Thickest", command=on_click_guide_clr_change_help_function_middle_3)
GuideThickChild_1.add_cascade(label="Middle", menu=GuideThickChild_4)

GuideThickChild_5 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_5.add_checkbutton(label="Normal", command=on_click_guide_clr_change_help_function_base_0)
GuideThickChild_5.add_checkbutton(label="Thick", command=on_click_guide_clr_change_help_function_base_1)
GuideThickChild_5.add_checkbutton(label="Thicker", command=on_click_guide_clr_change_help_function_base_2)
GuideThickChild_5.add_checkbutton(label="Thickest", command=on_click_guide_clr_change_help_function_base_3)
GuideThickChild_1.add_cascade(label="Base", menu=GuideThickChild_5)

GuideThickChild_6 = Menu(GuideThickChild_1, tearoff=0)
GuideThickChild_6.add_checkbutton(label="Normal", command=on_click_guide_clr_change_help_function_descender_0)
GuideThickChild_6.add_checkbutton(label="Thick", command=on_click_guide_clr_change_help_function_descender_1)
GuideThickChild_6.add_checkbutton(label="Thicker", command=on_click_guide_clr_change_help_function_descender_2)
GuideThickChild_6.add_checkbutton(label="Thickest", command=on_click_guide_clr_change_help_function_descender_3)
GuideThickChild_1.add_cascade(label="Bottom", menu=GuideThickChild_6)

rightclick_menu.add_cascade(label="Guidelines Thickness", menu=GuideThickChild_1)

AreaHighLightChild = Menu(rightclick_menu, tearoff=0)
AreaHighLightChild.add_checkbutton(label="Top", command = guidelines_toparea_submenu)
AreaHighLightChild.add_checkbutton(label="Middle", command = guidelines_middlearea_submenu)
AreaHighLightChild.add_checkbutton(label="Descender", command = guidelines_descenderarea_submenu)
rightclick_menu.add_cascade(label="Area Highlight", menu=AreaHighLightChild)

rightclick_menu.add_separator()

LetterShadingChild = Menu(rightclick_menu, tearoff=0)
LetterShadingChild.add_checkbutton(label="25%")
LetterShadingChild.add_checkbutton(label="50%")
LetterShadingChild.add_checkbutton(label="75%")
LetterShadingChild.add_checkbutton(label="100%")
LetterShadingChild.add_separator()
LetterShadingChild.add_command(label="Options...", command=letter_shading_option_mw)
rightclick_menu.add_cascade(label="Letter Shading", menu=LetterShadingChild)

StrokeArrowChild = Menu(rightclick_menu, tearoff=0)
StrokeArrowChild.add_checkbutton(label="On", command=main3)
StrokeArrowChild.add_command(label="Options...")
rightclick_menu.add_cascade(label="Stroke Arrows", menu=StrokeArrowChild)

DotDensityChild = Menu(rightclick_menu, tearoff=0)
DotDensityChild.add_checkbutton(label="25%")
DotDensityChild.add_checkbutton(label="50%")
DotDensityChild.add_checkbutton(label="75%")
DotDensityChild.add_checkbutton(label="100%")
DotDensityChild.add_separator()
DotDensityChild.add_command(label="Options...", command=letter_dot_density_option_mw)
rightclick_menu.add_cascade(label="Dot Density", menu=DotDensityChild)

DecisionDotChild = Menu(rightclick_menu, tearoff=0)
DecisionDotChild.add_checkbutton(label="On", command=main)
DecisionDotChild.add_checkbutton(label="Connect Dots", command=main4)
rightclick_menu.add_cascade(label="Decision Dots", menu=DecisionDotChild)

rightclick_menu.add_checkbutton(label="Start Dot", onvalue=1, offvalue=False, command=main1)
rightclick_menu.add_checkbutton(label="Letter Outline", command=donothing, onvalue=1, offvalue=False)
rightclick_menu.add_checkbutton(label="Color Letters", onvalue=1, offvalue=False)
rightclick_menu.add_separator()

WordSpacingChild = Menu(rightclick_menu, tearoff=0)
WordSpacingChild.add_checkbutton(label="Regular")
WordSpacingChild.add_checkbutton(label="Wide")
rightclick_menu.add_cascade(label="Word Spacing", menu=WordSpacingChild)

SW_Main_UI.bind("<Button-1>", popupFocusOut)
SW_Main_UI.bind("<Button-3>", popup)
SW_Main_UI.bind('<Motion>', motion)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

new_icon = PhotoImage(file="icons/11.png")
new_button = tk.Button(maintoolbarframe, image=new_icon, command=lambda: NewWindow(SW_Main_UI))
new_button.image = new_icon
wl_ttp = CreateToolTip(new_button, "New")
new_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
open_icon = PhotoImage(file="icons/10.png")
open_button = tk.Button(maintoolbarframe, image=open_icon, command=openfile)
open_button.image = open_icon
wl_ttp = CreateToolTip(open_button, "Open")
open_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
save_icon = PhotoImage(file="icons/9.png")
save_button = tk.Button(maintoolbarframe, image=save_icon, command=saveasfile)
save_button.image = save_icon
wl_ttp = CreateToolTip(save_button, "Save")
save_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
print_icon = PhotoImage(file="icons/8.png")
print_button = tk.Button(maintoolbarframe, image=print_icon)
print_button.image = print_icon
wl_ttp = CreateToolTip(print_button, "Print")
print_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
cut_icon = PhotoImage(file="icons/27.png")
cut_button = tk.Button(maintoolbarframe, image=cut_icon)
cut_button.image = cut_icon
wl_ttp = CreateToolTip(cut_button, "Cut")
cut_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
copy_icon = PhotoImage(file="icons/21.png")
copy_button = tk.Button(maintoolbarframe, image=copy_icon)
copy_button.image = copy_icon
wl_ttp = CreateToolTip(copy_button, "Copy")
copy_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
paste_icon = PhotoImage(file="icons/24.png")
paste_button = tk.Button(maintoolbarframe, image=paste_icon)
paste_button.image = paste_icon
wl_ttp = CreateToolTip(paste_button, "Paste")
paste_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
new_art_box_icon = PhotoImage(file="icons/22.png")
new_art_box_button = tk.Button(maintoolbarframe, image=new_art_box_icon, command=add_new_art_box)
new_art_box_button.image = new_art_box_icon
wl_ttp = CreateToolTip(new_art_box_button, "Add New Artbox")
new_art_box_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
new_text_box_icon = PhotoImage(file="icons/23.png")
new_text_box_button = tk.Button(maintoolbarframe, image=new_text_box_icon, command=add_text_box)
new_text_box_button.image = new_text_box_icon
wl_ttp = CreateToolTip(new_text_box_button, "Add New textbox")
new_text_box_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
spell_check_icon = PhotoImage(file="icons/20.png")
spell_check_button = tk.Button(maintoolbarframe, image=spell_check_icon)
spell_check_button.image = spell_check_icon
wl_ttp = CreateToolTip(spell_check_button, "Spell check")
spell_check_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
zoom_icon = PhotoImage(file="icons/26.png")
zoom_button = tk.Button(maintoolbarframe, image=zoom_icon, command=zoom_wp)
zoom_button.image = zoom_icon
wl_ttp = CreateToolTip(zoom_button, "Zoom")
zoom_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
fonts_icon = PhotoImage(file="icons/25.png")
fonts_button = tk.Button(maintoolbarframe, image=fonts_icon, command=font_wp)
fonts_button.image = fonts_icon
wl_ttp = CreateToolTip(fonts_button, "Font")
fonts_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
portrait_icon = PhotoImage(file="icons/19.png")
portrait_button = tk.Button(maintoolbarframe, image=portrait_icon)
portrait_button.image = portrait_icon
wl_ttp = CreateToolTip(portrait_button, "Portrait")
portrait_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
landscape_icon = PhotoImage(file="icons/18.png")
landscape_button = tk.Button(maintoolbarframe, image=landscape_icon)
landscape_button.image = landscape_icon
wl_ttp = CreateToolTip(landscape_button, "Landscape")
landscape_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
show_hide_grid_icon = PhotoImage(file="icons/17.png")
show_hide_grid_button = tk.Button(maintoolbarframe, image=show_hide_grid_icon, command=gird_on)
show_hide_grid_button.image = show_hide_grid_icon
wl_ttp = CreateToolTip(show_hide_grid_button, "Grid")
show_hide_grid_button.pack(side=LEFT, expand=0, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
show_hide_grid_menu_icon = tk.PhotoImage(file="icons/d11.png")
show_hide_grid_menu_button = tk.Menubutton(maintoolbarframe, width=10, height=35, image=show_hide_grid_menu_icon)
show_hide_grid_menu_button.menu = Menu(show_hide_grid_menu_button, tearoff=0)
show_hide_grid_menu_button["menu"] = show_hide_grid_menu_button.menu
shwgrd = IntVar()
snpgrd = IntVar()
show_hide_grid_menu_button.menu.add_checkbutton(label="Show Gird", variable=shwgrd)
show_hide_grid_menu_button.menu.add_checkbutton(label="Snap to Gird", variable=snpgrd)
show_hide_grid_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
close_icon = PhotoImage(file="icons/closewindow1.png")
close_button = tk.Button(maintoolbarframe, image=close_icon, command=close_wn)
close_button.image = close_icon
wl_ttp = CreateToolTip(close_button, "close")
close_button.pack(side=RIGHT, expand=0)
# ---------------------------------------------------------------------------------------------------------------#
restaurar_icon = PhotoImage(file="icons/restaurar2.png")
restaurar_button = tk.Button(maintoolbarframe, image=restaurar_icon, command=restaurar_wn)
restaurar_button.image = restaurar_icon
wl_ttp = CreateToolTip(restaurar_button, "restaurar")
restaurar_button.pack(side=RIGHT, expand=0)
# ---------------------------------------------------------------------------------------------------------------#
minimize_icon = PhotoImage(file="icons/minimizewindow2.png")
minimize_button = tk.Button(maintoolbarframe, image=minimize_icon, command=minimize_wn)
minimize_button.image = minimize_icon
wl_ttp = CreateToolTip(minimize_button, "minimize")
minimize_button.pack(side=RIGHT, expand=0)


# **************************************************Toolbar-frame End**************************************************************#
# -----------------------------------------------------------------------------------------------------------------------------------#
# ********************************************propertybar-frame**********************************************************************#

# Create a TkInter image to be used in the button
def insert_font_combobox(box):
    box['values'] = ['Manuscript', 'ManuScript-Simple', 'ManScript2',
                     'Cursive', 'Cursive-Simple', 'Modern Manuscript', 'Modern Cursive']


text_font = ('Manuscript', '12')
main_frame = tk.Frame(propertybarframe)
combo_box = ttk.Combobox(main_frame, font=text_font, width=14)
propertybarframe.option_add('*TCombobox*Listbox.font', text_font)
combo_box.set('Manuscript')
combo_box.state(['readonly'])
combo_box.pack(side=LEFT)
main_frame.pack(side=LEFT)
insert_font_combobox(combo_box)


def call_letter_out_liner():
    SW_global.entire_delete_list_for_one_page.clear()
    for i in range(len(SW_global.axes_data)):
        for j in SW_global.axes_data[str(i)]["delete_list"]:
            SW_global.entire_delete_list_for_one_page.append(j)#(SW_global.axes_data[str(i)]["delete_list"])[j])
        (SW_global.axes_data[str(i)]["delete_list"]).clear()
        (SW_global.axes_data[str(i)]["letters_already_written"]).clear()
        (SW_global.axes_data[str(i)]["cursor_data"]).clear()
        (SW_global.axes_data[str(i)]["kern_list"]).clear()
        (SW_global.axes_data[str(i)]["kern_list"]).append(0)
        (SW_global.axes_data[str(i)]["kern_value_array"]).append(0)
        (SW_global.axes_data[str(i)]["delete_list"]).clear()
        (SW_global.axes_data[str(i)]["recent_input_list"]).clear()
        (SW_global.axes_data[str(i)]["cursor_pos"]).clear()
        (SW_global.axes_data[str(i)]["cursor_pos"]).append(0)
        for j in range(len(SW_global.axes_data[str(i)]["lines"])):
            if(j>=3):
                ((SW_global.axes_data[str(i)]["lines"])[j]).set_visible(False)
        for j in range(len(SW_global.axes_data[str(i)]["gval"])):
            if(j>=3):
                ((SW_global.axes_data[str(i)]["lines"])[j]).set_visible(False)

        while(len(SW_global.axes_data[str(i)]["lines"])>=3):
            del (SW_global.axes_data[str(i)]["lines"])[len(SW_global.axes_data[str(i)]["lines"])-1]

        while(len(SW_global.axes_data[str(i)]["gval"])>=3):
            del (SW_global.axes_data[str(i)]["gval"])[len(SW_global.axes_data[str(i)]["gval"])-1]
        #(SW_global.axes_data[str(i)]["lines"]).clear()
        #(SW_global.axes_data[str(i)]["gval"]).clear()
    for i in range(len(delete_list)):
        SW_global.entire_delete_list_for_one_page.append(delete_list[i])
    SW_global.cursor_pos.clear()
    SW_global.cursor_pos.append(0)
    SW_global.cursor_data.clear()
    delete_list.clear()
    kern_value_array.clear()
    SW_global.kern_list.clear()
    kern_value_array.append(0)
    SW_global.kern_list.append(0)

    #delete_list.clear()

    print("This is entire delete_list for:",SW_global.entire_delete_list_for_one_page)
    add_letter_outliner_from_any_position(delete_list1=SW_global.entire_delete_list_for_one_page)



def add_letter_outliner_from_any_position(delete_list1=None,axesdata=None):
    recent_input_list2=[]
    cursor_pos2=[]
    cursor_data2=[]
    kern_value_array2=[0]
    kern_list2=[0]
    letters_already_written2=[]
    letter_out_line_inner_fonts_array2=[]
    delete_list2=[]
    guideline_axes_lines2=[]
    temp_guideline_axes2=None
    recent_input_list2=[]
    temp_guideline_flag=None
    temp_data=[]
    for k1 in range(len(guideline_axes[l].lines)):
        if(k1>=3):
            (guideline_axes[l].lines[k1]).set_visible(False)



    if(len(SW_global.axes_data)>0):
        count_of_axes=0

        temp_guideline_axes2=SW_global.axes_data[str(0)]["axis_data"]
        for j in range(len(delete_list1)):
            print("check point 1")
            c1=[]
            c2=[]
            c11=[]
            c22=[]
            if(kern_list2[0]>15500):
                print("check point 2")
                print("Count of axes",count_of_axes)
                print("len(SW_global.axes_data)",len(SW_global.axes_data)-1)
                if(count_of_axes<len(SW_global.axes_data)-1):
                    print("check point 3")
                    SW_global.axes_data[str(count_of_axes)]["lines"]=[i for i in guideline_axes_lines2]
                    SW_global.axes_data[str(count_of_axes)]["delete_list"]=[i for j in delete_list2]
                    SW_global.axes_data[str(count_of_axes)]["recent_input_list"]=[i for i in recent_input_list2]
                    SW_global.axes_data[str(count_of_axes)]["letters_already_written"]=[i for i in letters_already_written2]
                    SW_global.axes_data[str(count_of_axes)]["kern_list"]=[i for i in kern_list2]
                    SW_global.axes_data[str(count_of_axes)]["kern_value_array"]=[i for i in kern_value_array2]
                    SW_global.axes_data[str(count_of_axes)]["letter_out_line_inner_fonts_array"]=[i for i in letter_out_line_inner_fonts_array2]
                    SW_global.axes_data[str(count_of_axes)]["cursor_pos"]=[i for i in cursor_pos2]
                    SW_global.axes_data[str(count_of_axes)]["cursor_data"]=[i for i in cursor_data2]
                    SW_global.axes_data[str(count_of_axes)]["lines"]=[i for i in guideline_axes_lines2]
                    SW_global.axes_data[str(count_of_axes)]["gval"]=[i for i in guideline_axes_lines2]
                    count_of_axes=count_of_axes+1
                    temp_guideline_axes2=SW_global.axes_data[str(count_of_axes)]["axis_data"]
                elif(count_of_axes>=len(SW_global.axes_data)-1):
                    print("check point 4")
                    if((temp_guideline_flag!=None) and (temp_guideline_flag>0)):
                        print("check point 5")
                        a=dict()
                        a["letters_already_written"]=[j for j in  letters_already_written2]
                        a["kern_value_array"]=[j for j in kern_value_array2]
                        a["delete_list"]=[j for j in delete_list2]
                        a["kern_list"]=[j for j in kern_list2]
                        a["lines"]=[j for j in guideline_axes_lines2]
                        a["gval"]=[j for j in guideline_axes_lines2]
                        a["cursor_pos"]=[j for j in cursor_pos2]
                        a["cursor_data"]=[j for j in cursor_data2]
                        a["axis_data"]=guideline_axes[l]
                        a["compositedot_already_applied_array"]=[]
                        a["decisiondot_already_applied_array"]=[]
                        a["connectdot_already_applied_array"]=[]
                        a["startdot_already_applied_array"]=[]
                        a["recent_input_list"]=[j for j in recent_input_list2]
                        a["connect_dot_flag_pos"]=0
                        a["decision_dot_flag_pos"]=0
                        a["stoke_arrow_flag_pos"]=0
                        a["startdot_flag_pos"]=0
                        SW_global.axes_data[str(len(SW_global.axes_data))]=a
                        newCreateGuideLine(1,None,None,None,None)
                        print("This is check point22")
                        count_of_axes=count_of_axes+1
                        SW_global.current_pos=0
                        SW_global.current_axes=guideline_axes[l]
                        temp_guideline_axes2=guideline_axes[l]
                        count_of_axes=count_of_axes+1
                    else:
                        print("check point 6")
                        for k1 in range(len(guideline_axes[l].lines)):
                            if(k1>=3):
                                (guideline_axes[l].lines[k1]).set_visible(False)

                        #while(len(guideline_axes[l].lines)>=3):
                         #   del (guideline_axes[l].lines)[len(guideline_axes[l].lines)-1]

                        #guideline_axes[l].lines.clear()
                        for j in guideline_axes_lines2:
                            guideline_axes[l].lines.append(j)
                        SW_global.letters_already_written.clear()
                        for j in letters_already_written2:
                            SW_global.letters_already_written.append(j)
                        SW_global.recent_input_list.clear()
                        for j in recent_input_list2:
                            SW_global.recent_input_list.append(j)
                        SW_global.cursor_pos.clear()
                        for j in cursor_pos2:
                            SW_global.cursor_pos.append(j)
                        SW_global.cursor_data.clear()
                        for j in cursor_data2:
                            SW_global.cursor_data.append(j)
                        SW_global.kern_list.clear()
                        for j in kern_list2:
                            SW_global.kern_list.append(j)
                        temp_guideline_flag=40
                        count_of_axes=count_of_axes+1
                        temp_guideline_axes2=guideline_axes[l]
                kern_list2.clear()
                kern_list2.insert(0,0)
                kern_value_array2.clear()
                kern_value_array2.insert(0,0)
                cursor_pos2.clear()
                cursor_pos2.insert(0,0)
                cursor_data2.clear()
                cursor_data2.insert(0,0)
                letters_already_written2.clear()
                letter_out_line_inner_fonts_array2.clear()

            user_input=delete_list1[j]
            length12 = len(recent_input_list2)
            event_key=delete_list1[j]
            print("This check point 8")
            #user_input = event.key
            x_max = manu_letter_out_line_inner_fonts.x_max[user_input]
            kern_x =kern_list2[0] #SW_global.kern_list[0]
            c1, c2 = manu_letter_outline.return_outline_fonts(user_input)
            c1, c2, draw_type_letter_out_line = Kern_add_help.kern_add_operation(c1, c2, kern_x)

            c11, c22 = manu_letter_out_line_inner_fonts.return_letter_out_inner_fonts(user_input)
            c11, c22, draw_type_letter_in_line = Kern_add_help.kern_add_operation(c11, c22, kern_x)
            kern_x = kern_list2[0] + x_max + 400
            kern_list2.insert(0, kern_x)

            kern_counter = len(kern_value_array2)
            kern_value_array2.insert(kern_counter, kern_x)
            recent_input_list2.insert(length12,event_key)#SW_global.recent_input_list.insert(length12, event.key)
            delete_list2.insert(length12, event_key)

            init_enrty_pos = len(letter_out_line_inner_fonts_array2)
            #print(guideline_axes_lines2)
            inti_letter_pos =len(guideline_axes_lines2) #len(guideline_axes[l].lines)
            letter_out_line_inner_fonts_array2.insert(init_enrty_pos, inti_letter_pos)

            if draw_type_letter_in_line == 1:
                temp_data.clear()
                print("check point 9")

                temp_data=temp_guideline_axes2.plot(c11, c22, color='black', dashes=(3, 2), linewidth=0.6)
                for k1 in temp_data:
                    guideline_axes_lines2.append(k1)

            else:
                print("check point 10")

                for il in range(len(c11)):
                    temp_data.clear()
                    temp_data=temp_guideline_axes2.plot(c11[il], c22[il], color='black', dashes=(3, 2), linewidth=0.6)
                    for k1 in temp_data:
                        guideline_axes_lines2.append(k1)
            fig.canvas.draw()

            print("check point 11")

            final_enrty_pos = len(letter_out_line_inner_fonts_array2)
            final_letter_pos = len(guideline_axes_lines2)
            letter_out_line_inner_fonts_array2.insert(final_enrty_pos, final_letter_pos)

            init_enrty_pos = len(letters_already_written2)
            inti_letter_pos = len(guideline_axes_lines2)
            letters_already_written2.insert(init_enrty_pos, inti_letter_pos)
            temp_data=[]

            if draw_type_letter_out_line == 1:
                temp_data.clear()
                temp_data=temp_guideline_axes2.plot(c1, c2, color='black', linewidth=0.6)
                for k1 in temp_data:
                    guideline_axes_lines2.append(k1)
                fig.canvas.draw()
            else:
                n = len(c1)
                for i in range(n):
                    temp_data.clear()
                   # print(c1,c2)
                    temp_data=temp_guideline_axes2.plot(c1[i], c2[i], color='black', linewidth=0.6)
                    for k1 in temp_data:
                        guideline_axes_lines2.append(k1)
                fig.canvas.draw()

    # ----------------------------------------------------------------------------------------------------

        delete_list.clear()
        print("check point 12")
        for k1 in delete_list2:
            delete_list.append(k1)

        SW_global.cursor_pos.clear()
        for k1 in cursor_pos2:
            SW_global.cursor_pos.append(k1)

        SW_global.cursor_data.clear()
        for k1 in cursor_data2:
            SW_global.cursor_data.append(k1)

        SW_global.letters_already_written.clear()

        for k1 in letters_already_written2:
            SW_global.letters_already_written.append(k1)

        letter_out_line_inner_fonts_array.clear()

        for k1 in letter_out_line_inner_fonts_array:
            letter_out_line_inner_fonts_array2.append(k1)
        SW_global.recent_input_list.clear()
        for k1 in recent_input_list2:
            SW_global.recent_input_list.append(k1)

        kern_value_array.clear()
        for k1 in kern_value_array2:
            kern_value_array.append(k1)

        SW_global.kern_list.clear()
        for k1 in kern_list2:
            SW_global.kern_list.append(k1)
    else:
        try:
            for j in range(len(delete_list1)):
                if(SW_global.kern_list[0]>15500):
                    a=dict()
                    a["letters_already_written"]=[j for j in  letters_already_written2]
                    a["kern_value_array"]=[j for j in kern_value_array2]
                    a["delete_list"]=[j for j in delete_list2]
                    a["kern_list"]=[j for j in kern_list2]
                    a["lines"]=[j for j in guideline_axes_lines2]
                    a["gval"]=[j for j in guideline_axes_lines2]
                    a["cursor_pos"]=[j for j in cursor_pos2]
                    a["cursor_data"]=[j for j in cursor_data2]
                    a["axis_data"]=guideline_axes[l]
                    a["compositedot_already_applied_array"]=[]
                    a["decisiondot_already_applied_array"]=[]
                    a["connectdot_already_applied_array"]=[]
                    a["startdot_already_applied_array"]=[]
                    a["recent_input_list"]=[j for j in recent_input_list2]
                    a["connect_dot_flag_pos"]=0
                    a["decision_dot_flag_pos"]=0
                    a["stoke_arrow_flag_pos"]=0
                    a["startdot_flag_pos"]=0
                    SW_global.axes_data[str(len(SW_global.axes_data))]=a
                    newCreateGuideLine(1,None,None,None,None)
                    print("This is check point22")
                    #count_of_axes=count_of_axes+1
                    SW_global.current_pos=0
                    SW_global.current_axes=guideline_axes[l]
                    SW_global.kern_list.clear()
                    SW_global.kern_list.insert(0,0)
                    kern_value_array2.clear()
                    kern_value_array2.insert(0,0)
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_pos.insert(0,0)
                    SW_global.cursor_data.clear()
                    SW_global.cursor_data.insert(0,0)
                    SW_global.letters_already_written.clear()
                    letter_out_line_inner_fonts_array.clear()


                length12 = len(SW_global.recent_input_list)
                user_input = delete_list1[j]
                event_key=delete_list1[j]
                x_max = manu_letter_out_line_inner_fonts.x_max[user_input]
                kern_x = SW_global.kern_list[0]
                c1, c2 = manu_letter_outline.return_outline_fonts(user_input)
                c1, c2, draw_type_letter_out_line = Kern_add_help.kern_add_operation(c1, c2, kern_x)

                c11, c22 = manu_letter_out_line_inner_fonts.return_letter_out_inner_fonts(user_input)
                c11, c22, draw_type_letter_in_line = Kern_add_help.kern_add_operation(c11, c22, kern_x)
                kern_x = SW_global.kern_list[0] + x_max + 400
                SW_global.kern_list.insert(0, kern_x)

                kern_counter = len(kern_value_array)
                kern_value_array.insert(kern_counter, kern_x)
                SW_global.recent_input_list.insert(length12, event_key)
                delete_list.insert(length12, event_key)

                init_enrty_pos = len(letter_out_line_inner_fonts_array)
                inti_letter_pos = len(guideline_axes[l].lines)
                letter_out_line_inner_fonts_array.insert(init_enrty_pos, inti_letter_pos)

                if draw_type_letter_in_line == 1:
                    guideline_axes[l].plot(c11, c22, color='black', dashes=(3, 2), linewidth=0.6)
                else:
                    for il in range(len(c11)):
                        guideline_axes[l].plot(c11[il], c22[il], color='black', dashes=(3, 2), linewidth=0.6)
                fig.canvas.draw()

                final_enrty_pos = len(letter_out_line_inner_fonts_array)
                final_letter_pos = len(guideline_axes[l].lines)
                letter_out_line_inner_fonts_array.insert(final_enrty_pos, final_letter_pos)

                init_enrty_pos = len(SW_global.letters_already_written)
                inti_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)

                if draw_type_letter_out_line == 1:
                    #my_draw1(c1, c2)
                    guideline_axes[l].plot(c1, c2, color='black', linewidth=0.6)
                    fig.canvas.draw()
                else:
                    n = len(c1)
                    for i in range(n):
                     #   my_draw(c1[i], c2[i])
                     guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.6)
                    fig.canvas.draw()

        # -----------------------------------------------------------------------------------------------------
                final_enrty_pos = len(SW_global.letters_already_written)
                final_letter_pos = len(guideline_axes[l].lines)
                SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
                features_checking_function()
            fig.canvas.draw()

        except KeyError:
            pass

    return


def add_letter_with_outliner(event):
    try:
        length12 = len(SW_global.recent_input_list)
        user_input = event.key
        x_max = manu_letter_out_line_inner_fonts.x_max[user_input]
        kern_x = SW_global.kern_list[0]
        c1, c2 = manu_letter_outline.return_outline_fonts(user_input)
        c1, c2, draw_type_letter_out_line = Kern_add_help.kern_add_operation(c1, c2, kern_x)

        c11, c22 = manu_letter_out_line_inner_fonts.return_letter_out_inner_fonts(user_input)
        c11, c22, draw_type_letter_in_line = Kern_add_help.kern_add_operation(c11, c22, kern_x)
        kern_x = SW_global.kern_list[0] + x_max + 400
        SW_global.kern_list.insert(0, kern_x)

        kern_counter = len(kern_value_array)
        kern_value_array.insert(kern_counter, kern_x)
        SW_global.recent_input_list.insert(length12, event.key)
        delete_list.insert(length12, event.key)

        init_enrty_pos = len(letter_out_line_inner_fonts_array)
        inti_letter_pos = len(guideline_axes[l].lines)
        letter_out_line_inner_fonts_array.insert(init_enrty_pos, inti_letter_pos)

        if draw_type_letter_in_line == 1:
            guideline_axes[l].plot(c11, c22, color='black', dashes=(3, 2), linewidth=0.6)
        else:
            for il in range(len(c11)):
                guideline_axes[l].plot(c11[il], c22[il], color='black', dashes=(3, 2), linewidth=0.6)
        fig.canvas.draw()

        final_enrty_pos = len(letter_out_line_inner_fonts_array)
        final_letter_pos = len(guideline_axes[l].lines)
        letter_out_line_inner_fonts_array.insert(final_enrty_pos, final_letter_pos)

        init_enrty_pos = len(SW_global.letters_already_written)
        inti_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)

        if draw_type_letter_out_line == 1:
            #my_draw1(c1, c2)
            guideline_axes[l].plot(c1, c2, color='black', linewidth=0.6)
            fig.canvas.draw()
        else:
            n = len(c1)
            for i in range(n):
             #   my_draw(c1[i], c2[i])
             guideline_axes[l].plot(c1, c2, color='black', linewidth=0.6)
            fig.canvas.draw()

# -----------------------------------------------------------------------------------------------------
        final_enrty_pos = len(SW_global.letters_already_written)
        final_letter_pos = len(guideline_axes[l].lines)
        SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
        features_checking_function()

    except KeyError:
        pass




def backSpace_with_outliner():
    len1 = len(SW_global.letters_already_written)
    len2 = len1 - 1
    srt_loop = SW_global.letters_already_written[len2 - 1]
    end_loop = SW_global.letters_already_written[len2]
    for i in range(srt_loop, end_loop):
        SW_global.g_val.lines[i].set_visible(False)
    fig.canvas.draw()
    del SW_global.letters_already_written[len1-1]
    del SW_global.letters_already_written[len1-2]

    len1 = len(letter_out_line_inner_fonts_array)
    len2 = len1 - 1
    srt_loop = letter_out_line_inner_fonts_array[len2 - 1]
    end_loop = letter_out_line_inner_fonts_array[len2]
    for i in range(srt_loop, end_loop):
        SW_global.g_val.lines[i].set_visible(False)
    fig.canvas.draw()
    del letter_out_line_inner_fonts_array[len1 - 1]
    del letter_out_line_inner_fonts_array[len1 - 2]

    last_input_len = len(delete_list)
    last_glyph = delete_list[last_input_len - 1]
    del delete_list[last_input_len - 1]
    l12 = len(kern_value_array)
    del kern_value_array[l12 - 1]
    kern_x = SW_global.kern_list[0] - 400 - manu_letter_out_line_inner_fonts.x_max[last_glyph]
    SW_global.kern_list.insert(0, kern_x)
    return 



def callbackguidelineFunc(event):
    global guideline_counter
    global value1, base_x, base_y, median_y, descender_y, ascender_y, median_x, descender_x, ascender_x


   # fig.canvas.mpl_connect('key_press_event', press)
   # fig.canvas.draw()
    #if combo_box.get()=='8':

        # SW_global.btm_gd_1 = 0.93
        # SW_global.ht_gd_1 = 0.04
        # SW_global.bottom = 0.93
        # SW_global.top = 0.97
        # #default_guideline(guideline_ax
        # guideline_axes[l].set_position([SW_global.lt_gd_1, SW_global.btm_gd_1, SW_global.wd_gd_1, SW_global.ht_gd_1])
        # fig.canvas.draw()
        # fig.canvas.mpl_connect('key_press_event', press)


    # if combo_box.get() == '8':
    #     guideline_axes[l].cla()
    #     SW_global.scl = 32
    #     SW_global.btm_gd_1 = 0.93
    #     SW_global.ht_gd_1 = 0.04
    #     SW_global.bottom = 0.93
    #     SW_global.top = 0.97
    #     default_guideline(guideline_axes[l])
    #     mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
    #     mainselector.maxdist = 8
    #     SW_global.gd_sc1 = True
    #     fig.canvas.draw()
    #     print("combobox value applied : 8")


    #     print("gdhhd"*200)
    # elif combo_box.get() == '10':
    #     guideline_axes[l].cla()
    #     SW_global.scl = 31
    #     SW_global.btm_gd_1 = 0.93
    #     SW_global.ht_gd_1 = 0.05
    #     SW_global.bottom = 0.93
    #     SW_global.top = 0.98
    #     mainselector.maxdist = 10
    #     SW_global.gd_sc1 = True
    #     guideline_axes[l].set_position([SW_global.lt_gd_1, SW_global.btm_gd_1, SW_global.wd_gd_1, SW_global.ht_gd_1])
    #     default_guideline(guideline_axes[l])
    #     fig.canvas.draw()
    #     print("combobox value applied : 10")
    # SW_global.entire_delete_list_for_one_page.clear()
    #fig.canvas.mpl_connect('key_press_event', press)
    #fig.canvas.mpl_connect('key_press_event',lambda event:canvas._tkcanvas.focus_set())
    #fig.canvas.draw()
#    fig.canvas.setFocusPolicy( Tk.ClickFocus )
#    fig.canvas.setFocus()
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event',onclick2)
    fig.canvas.mpl_connect('button_release_event',onrelease)
    fig.canvas.get_tk_widget.focus_set()
    
    fig.canvas.draw()

    # for j in range(len(SW_global.axes_data)):
    #     for k in SW_global.axes_data[str(j)]["lines"]:
    #         k.set_visible(False)

    # for j in guideline_axes[l].lines:
    #     j.set_visible(False)
#fig.canvas.mpl_connect('key_press_event', press)



#from font_change  import font_value
import font_change
def combo_box_select(event):
    #global sl_b
    print("This is ok")
    print(combo_box.get())
    print("This is font value",font_change.font_value(combo_box.get()))
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event',onclick2)
    fig.canvas.mpl_connect('button_release_event',onrelease)
    fig.canvas.draw()
    print("This is default",SW_global.scl,sl_b)
    SW_global.scl,sl_b1=font_change.font_value(combo_box.get())
    print("After")
    print(SW_global.scl)
    def reqw(sl_b1):
        sl_b=sl_b1
    reqw(sl_b1)
    print(sl_b1)
    font_size_automate()




def font_size_automate():    ##### SW_global.scl,sl_b
    SW_global.entire_delete_list_for_one_page.clear()
    if(len(SW_global.axes_data)>0):
        for j in range(len(SW_global.axes_data)):
            for k1 in SW_global.axes_data[str(j)]["delete_list"]:
                SW_global.entire_delete_list_for_one_page.append(k1)
                (SW_global.axes_data[str(j)]["axis_data"]).set_visible(False)
    for k1 in delete_list:
        SW_global.entire_delete_list_for_one_page.append(k1)
    guideline_axes[l].set_visible(False)
    SW_global.axes_data.clear()
    guideline_axes[l].lines.clear()
    fig.canvas.draw()
    SW_global.cursor_pos.clear()
    SW_global.cursor_data.clear()
    SW_global.cursor_pos.insert(0,0)
    kern_value_array.clear()
    SW_global.kern_list.clear()
    SW_global.letters_already_written.clear()
    SW_global.letters_already_written.clear()
    SW_global.kern_list.insert(0,0)
    SW_global.kern_value_array.clear()
    SW_global.kern_value_array.insert(0,0)
    kern_value_array.clear()
    kern_value_array.insert(0,0)
    #print("This is check point 2")
    #print(guideline_axes[l].lines)
    compositedot_already_applied_array.clear()
    startdot_already_applied_array.clear()
    decisiondot_already_applied_array.clear()
    connectdot_already_applied_array.clear()
    stoke_arrow_flag_pos =0
    #print("This is len")
    #print(guideline_axes[l].lines)
    startdot_flag_pos=0
    decision_dot_flag_pos=0
    connect_dot_flag_pos=0
    delete_list.clear()
    newCreateGuideLine(1,None,None,None,None)
    #create_guideline(1)
    if(len(SW_global.entire_delete_list_for_one_page)>0):
        for j in SW_global.entire_delete_list_for_one_page:
            delete_after_font_change(event_key=j)
    fig.canvas.draw()

    return 



def delete_after_font_change(event_key=None):
    try:
        if(SW_global.kern_list[0]>15500):
            print("i am in optimising stage")
            a=dict()
            a["letters_already_written"]=[i for i in  SW_global.letters_already_written]
            a["kern_value_array"]=[i for i in kern_value_array]
            a["delete_list"]=[i for i in delete_list]
            a["kern_list"]=[i for i in SW_global.kern_list]
            a["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
            a["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
            a["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
            a["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
            a["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
            a["startdot_flag_pos"]=startdot_flag_pos
            a["decision_dot_flag_pos"]=decision_dot_flag_pos
            a["connect_dot_flag_pos"]=connect_dot_flag_pos
            a["axis_data"]=guideline_axes[l]
            print("This is guide line axes .lines",len(guideline_axes[l].lines))
            a["lines"]=[i for i in guideline_axes[l].lines]
            print("This is check point 3")
            a["gval"]=[i for i in SW_global.g_val.lines]
            a["cursor_pos"]=[i for i in SW_global.cursor_pos]
            a["cursor_data"]=[i for i in SW_global.cursor_data]
            print("This is cursor_data")
            print(a["cursor_data"])
            SW_global.cursor_pos.clear()
            SW_global.cursor_data.clear()
            SW_global.cursor_pos.insert(0,0)
            #print("This is decision dot flag")
            #print(decision_dot_flag_pos)
            #print("This is axes data")
            #print(len(SW_global.axes_data))
            SW_global.axes_data[str(len(SW_global.axes_data))]=a
            #print(SW_global.axes_data)
            #print(guideline_axes[l].lines)
            kern_value_array.clear()
            SW_global.kern_list.clear()
            SW_global.letters_already_written.clear()
            SW_global.letters_already_written.clear()
            SW_global.kern_list.insert(0,0)
            SW_global.kern_value_array.clear()
            SW_global.kern_value_array.insert(0,0)
            kern_value_array.clear()
            kern_value_array.insert(0,0)
            compositedot_already_applied_array.clear()
            startdot_already_applied_array.clear()
            decisiondot_already_applied_array.clear()
            connectdot_already_applied_array.clear()
            stoke_arrow_flag_pos =0
            startdot_flag_pos=0
            decision_dot_flag_pos=0
            connect_dot_flag_pos=0
            delete_list.clear()
            #temp=[i for i in guideline_axes[l].lines]
            newCreateGuideLine(1,None,None,None,None)

    except Exception as e:
        print(e)





############################ End of multiple guide line ################################### 



    length12 = len(SW_global.recent_input_list)
    user_input = event_key
    x_max = manuscript.x_max[user_input]
    kern_x = SW_global.kern_list[0]

    if color_letter_features_on_off:
        c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
    else:
        c1, c2 = manuscript.return_manuscript_fonts(user_input)


    c1, c2, draw_type_color_letter = Kern_add_help.kern_add_operation(c1, c2, kern_x)

    kern_x = SW_global.kern_list[0] + x_max + 300
    #print("After update kern list")
    print("This is before kern_x update")
    SW_global.kern_list.insert(0, kern_x)
    print("This is after ken_x ")
    #print(SW_global.kern_list)
    #print("this is kern value array")
    #print(kern_value_array)
    kern_counter = len(kern_value_array)
    kern_value_array.insert(kern_counter, kern_x)
    #print(kern_value_array)
    SW_global.recent_input_list.insert(length12, event_key)
    #print("this is list")
    delete_list.insert(length12, event_key)
    #print(delete_list)
    init_enrty_pos = len(SW_global.letters_already_written)
    inti_letter_pos = len(guideline_axes[l].lines)
    #print("This is guide line axes length ")
    #print(len(guideline_axes[l].lines))
    SW_global.letters_already_written.insert(init_enrty_pos, inti_letter_pos)
    #print(SW_global.letters_already_written)
    if draw_type_color_letter == 1:
        if letter_dot_density_no_dot_on_off == 1:
            alp = 0
        else:
            alp = temp_alp
        if color_letter_features_on_off:
            guideline_axes[l].plot(c1, c2, color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
        else:
            guideline_axes[l].plot(c1, c2, color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)

    else:
        n = len(c1)
        if letter_dot_density_no_dot_on_off == 1:
            alp = 0
        else:
            alp = temp_alp
        if color_letter_features_on_off:
            for i in range(n):
                if i == 0:
                    guideline_axes[l].plot(c1[i], c2[i], color=SW_global.first_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                if i == 1:
                    guideline_axes[l].plot(c1[i], c2[i], color=SW_global.second_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                if i == 2:
                    guideline_axes[l].plot(c1[i], c2[i], color=SW_global.third_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
                if i == 3:
                    guideline_axes[l].plot(c1[i], c2[i], color=SW_global.forth_letter_background_color, linewidth=0.7, dashes=(d1, d2), alpha=alp)
        else:
            for i in range(n):
                guideline_axes[l].plot(c1[i], c2[i], color='black', linewidth=0.7, dashes=(d1, d2), alpha=alp)
    #############################   Cursor part code of inserting ###############################
    import numpy as np 
    if(len(SW_global.cursor_data)!=0):
        print("It is ok")
        print(delete_list)
        print(SW_global.letters_already_written)
       # print(cursor_data)
        #cursor_pos(cursor_pos)
    else:
        print("It is empty")
    item_cursor=kern_x-300
    cursor_y=list(np.linspace(-900,1500,500))
    #cursor_y_neg=list(np.lenspace)
    cursor_x=list(np.full((500),item_cursor))
    SW_global.cursor_pos.append(item_cursor)
    cursor_x1=list(np.full((500),item_cursor))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
    plot_data=guideline_axes[l].plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
    SW_global.single_click_data=plot_data[0]


    k=plt.plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
    #print(k)
    #print(k)
    for i in k:
        SW_global.cursor_data.append(i)
        i.set_visible(False)

    #SW_global.cursor_data.append(k)
    #print(SW_global.cursor_data)
    for cur_count in range(len(SW_global.cursor_data)-1):
        invisible_item=SW_global.cursor_data[cur_count]
        #print("This is invisible_item")
        #print(invisible_item)
        invisible_item.set_visible(False)
    fig.canvas.draw()
    #print(guideline_axes[0].lines)

# -----------------------------------------------------------------------------------------------------
    final_enrty_pos = len(SW_global.letters_already_written)
    final_letter_pos = len(guideline_axes[l].lines)
    SW_global.letters_already_written.insert(final_enrty_pos, final_letter_pos)
    features_checking_function()
    return 

    #for j in range(l())


def insert_fontsize_combobox(box):
    box['values'] = ['8', '10', '12',
                     '14', '16', '18', '20', '24', '30', '36', '42', '48', '54', '60',
                     '66', '72', '96', '128', '144', '160', '192']
    #fig.canvas.mpl_connect('key_press_event', press)


text_font = ('Manuscript', '12')
main_frame = tk.Frame(propertybarframe)
combo_box = ttk.Combobox(main_frame, font=text_font, width=4,takefocus=False,exportselection=0)
propertybarframe.option_add('*TCombobox*Listbox.font', text_font)
combo_box.set('48')
#fig.canvas.mpl_connect('key_press_event', press)
combo_box.pack(side=LEFT)
main_frame.pack(side=LEFT)
insert_fontsize_combobox(combo_box)
#fig.canvas.mpl_connect('key_press_event', press)
#combo_box.bind("<<ComboboxSelected>>", callbackguidelineFunc)
combo_box.bind("<<ComboboxSelected>>", combo_box_select)

# ---------------------------------------------------------------------------------------------------------------#
letter_shadding_icon = PhotoImage(file="icons/2.png")
letter_shadding_button = tk.Button(propertybarframe, image=letter_shadding_icon, width=23, height=32)
letter_shadding_button.image = letter_shadding_icon
wl_ttp = CreateToolTip(letter_shadding_button, "Letter Shadding")
letter_shadding_button.pack(side=LEFT, ipady=4, ipadx=4)

letter_shadding_menu_icon = tk.PhotoImage(file="icons/d11.png")
letter_shadding_menu_button = tk.Menubutton(propertybarframe, width=10, height=35, image=letter_shadding_menu_icon)
letter_shadding_menu_button.menu = Menu(letter_shadding_menu_button, tearoff=0)
letter_shadding_menu_button["menu"] = letter_shadding_menu_button.menu
v1 = IntVar()
v2 = IntVar()
v3 = IntVar()
v4 = IntVar()
v5_option = IntVar()
letter_shadding_menu_button.menu.add_checkbutton(label="25%", variable=v1, command=letter_shadding_25)
letter_shadding_menu_button.menu.add_checkbutton(label="50%", variable=v2, command=letter_shadding_50)
letter_shadding_menu_button.menu.add_checkbutton(label="75%", variable=v3, command=letter_shadding_75)
letter_shadding_menu_button.menu.add_checkbutton(label="100%", variable=v4, command=letter_shadding_100)
letter_shadding_menu_button.menu.add_separator()
letter_shadding_menu_button.menu.add_checkbutton(label="Options...", variable=v5_option,
                                                 command=letter_shading_option_mw)
letter_shadding_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
letter_dot_density_icon = PhotoImage(file="icons/3.png")
letter_dot_density_button = tk.Button(propertybarframe, image=letter_dot_density_icon, width=23, height=32)
letter_dot_density_button.image = letter_dot_density_icon
wl_ttp = CreateToolTip(letter_dot_density_button, "Letter Dot Density")
letter_dot_density_button.pack(side=LEFT, ipady=4, ipadx=4)

letter_dot_density_menu_icon = tk.PhotoImage(file="icons/d11.png")
letter_dot_density_menu_button = tk.Menubutton(propertybarframe, width=10, height=35,
                                               image=letter_dot_density_menu_icon)
letter_dot_density_menu_button.menu = Menu(letter_dot_density_menu_button, tearoff=0)
letter_dot_density_menu_button["menu"] = letter_dot_density_menu_button.menu
x0_no_dot = IntVar()
x1 = IntVar()
x2 = IntVar()
x3 = IntVar()
x4 = IntVar()
x5_option = IntVar()
letter_dot_density_menu_button.menu.add_checkbutton(label="No Dots", variable=x0_no_dot, command=letter_dot_density_no_dot)
letter_dot_density_menu_button.menu.add_checkbutton(label="25%", variable=x1, command=letter_dot_density_25)
letter_dot_density_menu_button.menu.add_checkbutton(label="50%", variable=x2, command=letter_dot_density_50)
letter_dot_density_menu_button.menu.add_checkbutton(label="75%", variable=x3, command=letter_dot_density_75)
letter_dot_density_menu_button.menu.add_checkbutton(label="100%", variable=x4, command=letter_dot_density_100)
letter_dot_density_menu_button.menu.add_separator()
letter_dot_density_menu_button.menu.add_checkbutton(label="Options...", variable=x5_option,
                                                    command=letter_dot_density_option_mw)
letter_dot_density_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
guidelines_icon = PhotoImage(file="icons/4.png")
guidelines_button = tk.Button(propertybarframe, image=guidelines_icon, width=23, height=32, command=main2)
guidelines_button.image = guidelines_icon
wl_ttp = CreateToolTip(guidelines_button, "Guidelines")
guidelines_button.pack(side=LEFT, ipady=4, ipadx=4)

guidelines_menu_icon = tk.PhotoImage(file="icons/d11.png")
guidelines_menu_button = tk.Button(propertybarframe, width=10, height=40, image=guidelines_menu_icon,
                                   command=guidelines_menu_wtp)
guidelines_menu_button.image = guidelines_menu_icon
guidelines_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
stoke_arrows_icon = tk.PhotoImage(file="icons/5.png")
stoke_arrows_button = tk.Button(propertybarframe, image=stoke_arrows_icon, width=23, height=32, command=main3)
stoke_arrows_button.image = stoke_arrows_icon
wl_ttp = CreateToolTip(stoke_arrows_button, "Stoke Arrows")
stoke_arrows_button.pack(side=LEFT, ipady=4, ipadx=4)

stoke_arrows_menu_icon = tk.PhotoImage(file="icons/d11.png")
stoke_arrows_menu_button = tk.Menubutton(propertybarframe, width=10, height=35, image=stoke_arrows_menu_icon)
stoke_arrows_menu_button.menu = Menu(stoke_arrows_menu_button, tearoff=0)
stoke_arrows_menu_button["menu"] = stoke_arrows_menu_button.menu
z1 = IntVar()
z2 = IntVar()
z3 = IntVar()
stoke_arrows_menu_button.menu.add_checkbutton(label="On", variable=z1, command=main3)
stoke_arrows_menu_button.menu.add_checkbutton(label="Options", variable=z2, command=stoke_arrows_option_mw)
stoke_arrows_menu_button.menu.add_checkbutton(label="Arrow Color", variable=z3, command=stroke_arrow_color_mw)
stoke_arrows_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
start_arrow_icon = tk.PhotoImage(file="icons/6.png")
start_arrow_button = tk.Button(propertybarframe, image=start_arrow_icon, width=23, height=32, command=main1)
start_arrow_button.image = start_arrow_icon
wl_ttp = CreateToolTip(start_arrow_button, "Start Arrow")
start_arrow_button.pack(side=LEFT, ipady=4, ipadx=4)

start_arrow_menu_icon = tk.PhotoImage(file="icons/d11.png")
start_arrow_menu_button = tk.Button(propertybarframe, width=10, height=40, image=start_arrow_menu_icon,
                                    command=start_arrow_menu_wtp)
start_arrow_menu_button.image = start_arrow_menu_icon
start_arrow_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
letter_outline_icon = tk.PhotoImage(file="icons/1.png")
letter_outline_button = tk.Button(propertybarframe, width=23, height=32, image=letter_outline_icon, command=main_out)
letter_outline_button.image = letter_outline_icon
wl_ttp = CreateToolTip(letter_outline_button, "Letter Outline")
letter_outline_button.pack(side=LEFT, ipady=4, ipadx=4)

letter_outline_menu_icon = tk.PhotoImage(file="icons/d11.png")
letter_outline_menu_button = tk.Button(propertybarframe, width=10, height=40, image=start_arrow_menu_icon,
                                       command=letter_outline_menu_wtp)
letter_outline_menu_button.image = letter_outline_menu_icon
letter_outline_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
decision_dot_icon = tk.PhotoImage(file="icons/7.png")
decision_dot_button = tk.Button(propertybarframe, width=23, height=32, image=decision_dot_icon, command=main)
decision_dot_button.image = decision_dot_icon
wl_ttp = CreateToolTip(decision_dot_button, "Decision Dot")
decision_dot_button.pack(side=tk.LEFT, ipady=4, ipadx=4)

decision_dot_menu_icon = tk.PhotoImage(file="icons/d11.png")
decision_dot_menu_button = tk.Button(propertybarframe, width=10, height=40, image=decision_dot_menu_icon,
                                     command=decision_dot_menu_wtp)
decision_dot_menu_button.image = decision_dot_menu_icon
decision_dot_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
connect_dot_icon = tk.PhotoImage(file="icons/16.png")
connect_dot_button = tk.Button(propertybarframe, width=23, height=32, image=connect_dot_icon, command=main4)
connect_dot_button.image = connect_dot_icon
wl_ttp = CreateToolTip(connect_dot_button, "Connect Dot")
connect_dot_button.pack(side=LEFT, ipady=4, ipadx=4)

connect_dot_menu_icon = tk.PhotoImage(file="icons/d11.png")
connect_dot_menu_button = tk.Button(propertybarframe, width=10, height=40, image=connect_dot_menu_icon,
                                    command=connect_dot_menu_wtp)
connect_dot_menu_button.image = connect_dot_menu_icon
connect_dot_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
color_letter_icon = tk.PhotoImage(file="icons/15.png")
color_letter_button = tk.Button(propertybarframe, width=23, height=32, image=color_letter_icon, command=main12345)
color_letter_button.image = color_letter_icon
wl_ttp = CreateToolTip(color_letter_button, "Color Letter")
color_letter_button.pack(side=LEFT, ipady=4, ipadx=4)

color_letter_menu_icon = tk.PhotoImage(file="icons/d11.png")
color_letter_menu_button = tk.Button(propertybarframe, width=10, height=40, image=color_letter_menu_icon,
                                     command=color_letter_menu_wtp)
color_letter_menu_button.image = color_letter_menu_icon
color_letter_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
background_icon = tk.PhotoImage(file="icons/14.png")
background_button = tk.Button(propertybarframe, width=23, height=32, image=background_icon)
background_button.image = background_icon
wl_ttp = CreateToolTip(background_button, "background")
background_button.pack(side=LEFT, ipady=4, ipadx=4)

background_menu_icon = tk.PhotoImage(file="icons/d11.png")
background_menu_button = tk.Button(propertybarframe, width=10, height=40, image=background_menu_icon,
                                   command=background_menu_wtp)
background_menu_button.image = background_menu_icon
background_menu_button.pack(side=LEFT)
# ---------------------------------------------------------------------------------------------------------------#
include_following_text_icon = tk.PhotoImage(file="icons/13.png")
include_following_text_button = tk.Button(propertybarframe, width=23, height=32, image=include_following_text_icon,command=set_text_for_text_flow)
include_following_text_button.image = background_icon
wl_ttp = CreateToolTip(include_following_text_button, "Include following text")
include_following_text_button.pack(side=LEFT, ipady=4, ipadx=4)
# ---------------------------------------------------------------------------------------------------------------#
border_art_icon = tk.PhotoImage(file="icons/12.png")
border_art_button = tk.Button(propertybarframe, width=23, height=32, image=border_art_icon, command=borderart_wp)
border_art_button.image = border_art_icon
CreateToolTip(border_art_button, "Border art")
border_art_button.pack(side=LEFT, ipady=4, ipadx=4)
# **************************************** propertybar-frame End *****************************************

# ******************************************** Bottombar-frame***********************************************
infolbl = Label(endgridtoolframe)
infolbl.place(x=5, y=10, anchor="w")

plus_icon = tk.PhotoImage(file="icons/plus.png")
biggerButton = tk.Button(endgridtoolframe, image=plus_icon, command=zoom_plus)
biggerButton.image = plus_icon
biggerButton.pack(side=RIGHT, expand=0)

zoomLabel = Label(endgridtoolframe, text=str(SW_global.change_size_count) + "%")
zoomLabel.pack(side=RIGHT, expand=0)

minus_icon = tk.PhotoImage(file="icons/minus.png")
smallerButton = tk.Button(endgridtoolframe, image=minus_icon, command=zoom_minus)
smallerButton.image = minus_icon
smallerButton.pack(side=RIGHT, expand=0)
smallerButton.config(state=DISABLED)

right_icon = tk.PhotoImage(file="icons/rArrow.png")
rhtpgButton = tk.Button(endgridtoolframe, image=right_icon, command=lambda: raise_frame(writingareaframe1))
rhtpgButton.image = right_icon
rhtpgButton.pack(side=RIGHT, expand=0)

pageLabel = Label(endgridtoolframe, text="page " + str(int(SW_global.page_no)) + "of " + str(int(SW_global.page_no)))
pageLabel.pack(side=RIGHT, expand=0)

left_icon = tk.PhotoImage(file="icons/lArrow.png")
lftpgButton = tk.Button(endgridtoolframe, image=left_icon, command=lambda: raise_frame(writingareaframe1))
lftpgButton.image = left_icon
lftpgButton.pack(side=RIGHT, expand=0)
fig.canvas.mpl_connect('key_press_event', press)
raise_frame(writingareaframe1)

# ******************************************** Bottom-bar-frame End ********************************************
# --------------------------------------------------------------------------------------------------------------
SW_Main_UI.mainloop()
# ******************************************* End Grid <<<<<<<<<<********************************************
