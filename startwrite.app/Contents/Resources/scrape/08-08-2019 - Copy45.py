#!/usr/local/bin/python3
from SW_lib import *
import key_generation
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

# ****************************************** Global Variable & Statement ********************************************
global f_w, f_h
global tem_cursor_x,temp_cursor_y #,temp_cursor_temp_data
#SW_global.temp_cursor_temp_data=0
print("This is SW_global temp_cursor_temp_data")
print(SW_global.temp_cursor_temp_data)
try:
    o=SW_global.temp_cursor_temp_data[0]
    o.set_visible(False)


except Exception as e:
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
#    flag=None


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
                            copy_string=copy_string+str((SW_global.axes_data[str(j)]["delete_list"]))

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
                                    if(k<=pos2+1):
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

#global click_cursor

def onrelease(event):
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

    try:
        #print("I am on set invisible_item")
        item=SW_global.temp_cursor_temp_data[0]
        item.set_visible(False)
        #print(SW_global.temp_cursor_temp_data)
    except Exception as e:
        pass
    for i in SW_global.cursor_data:
        i.set_visible(False)
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
    starting_x=-999
    ending_x=-999
    pos1=-1
    pos2=-1
    cur_temp_start=-999
    cur_temp_end=-999
    # for i in range(len(SW_global.cursor_pos)):
    #    if(start_point<=SW_global.cursor_pos[i]):
    #        pos1=i-1
    #        cur_temp_start=pos1+1
    #        break
    #print(start_axes)

    #print(start_point)
    #print("This is before pos1")
    #print("This is start axes",start_axes)
    #print("This is start point",start_point)
    pos1,cur_temp_start=findPos1(axesdata=start_axes,start_point=start_point)
    #print("This is after pos1")
    print("this is pos1",pos1)

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

    print("this is pos2",pos2)

    #print("This is cur temp start",cur_temp_start)
    #print("This is cur temp end",cur_temp_end)
    #print(pos1)
    #print(pos2)

    if((pos1==10000)):
        if(cur_temp_start==1000):
            SW_global.single_click_data=SW_global.cursor_data[-1]
            (SW_global.cursor_data[-1]).set_visible(True)
            print("I am in return Statement")
            fig.canvas.draw()
            return
        else:
            SW_global.single_click_data=(SW_global.axes_data[str(cur_temp_start)]["cursor_pos"])[-1]
            ((SW_global.axes_data[str(cur_temp_start)]["cursor_data"])[-1]).set_visible(True)
            print("I am in return Statement1")
            fig.canvas.draw()
            return


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

    global pos1i
    global pos2i
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
            if(SW_global.click_axes==guideline_axes[l]):
     #           print("check point echo1")
                count_for_select=0


                for i in range(SW_global.letters_already_written[pos1*2],SW_global.letters_already_written[(pos2*2)+1]):
                    (guideline_axes[l].lines[i]).set_color("red")
            else:
                for j in range(len(SW_global.axes_data)):
                    if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.click_axes):
                        for k in range((SW_global.axes_data[str(j)]["letters_already_written"])[pos1*2],(SW_global.axes_data[str(j)]["letters_already_written"])[(pos2*2)+1]):
                            ((SW_global.axes_data[str(j)]["lines"])[k]).set_color("red")

        else:
            global start_of_select_temp
            global end_of_select_temp
            start_of_select=-999
            end_of_select=-999
            for k in range(len(SW_global.axes_data)):
        #        print("check point echo (((((((1")
         #       print(end_axes)
          #      print(SW_global.axes_data[str(k)]["axis_data"])
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
                            print("check point echo 8888888*************************************************")
                            for h in range((SW_global.axes_data[str(i)]["letters_already_written"])[0],(SW_global.axes_data[str(i)]["letters_already_written"])[-1]):
                                ((SW_global.axes_data[str(i)]["lines"])[h]).set_color("red")
                else:
                    print("This is ok111111111111111111111111111111")
                    for i in range(len(SW_global.axes_data)):
                        if(SW_global.release_axes==SW_global.axes_data[str(i)]["axis_data"]):
                            end_of_select=i

                    for i in range(len(guideline_axes[l].lines)):
                        if(i>4):
                            if(i<=SW_global.letters_already_written[pos2*2+1]):
                                (guideline_axes[l].lines[i]).set_color("red")


                    for i in range((SW_global.axes_data[str(end_of_select)]["letters_already_written"])[pos1*2],(SW_global.axes_data[str(end_of_select)]["letters_already_written"])[-1]):
                        ((SW_global.axes_data[str(end_of_select)]["lines"])[i]).set_color("red")


                    for i in range(len(SW_global.axes_data)):
                        if(i>end_of_select):
                            for k in range((SW_global.axes_data[str(end_of_select)]["letters_already_written"])[0],(SW_global.axes_data[str(end_of_select)]["letters_already_written"])[-1]):
                                if(k>4):
                                    ((SW_global.axes_data[str(i)]["lines"])[k]).set_color("red")

                        #if(i>=(SW_global.axes_data[end_of_select]["letters_already_written"])[pos1*2]):


                    #for i in range(len(SW_global.axes_data)):
                        #if(i==end_of_select):
                            #for k in range(len(SW_global.axes_data[str(i)]["lines"])):
                             #   if(i>=pos1*2):
                              #      ((SW_global.axes_data[str(i)]["lines"])[i]).set_color("red")

                       # if(i>end_of_select):
                        #    for k in range(len(SW_global.axes_data[str(i)]["lines"])):
                         #       if(k>3):
                          #          ((SW_global.axes_data[str(i)]["lines"])[k]).set_color("red")




            else:
                if(end_of_select==str(1000)):
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
            for i in range(len(guideline_axes[l].lines)):
                if(i>3):
                    item=SW_global.g_val.lines[i]
                    item.set_color('black')


            for i in range(len(SW_global.axes_data)):
                for k in range(len(SW_global.axes_data[str(i)]["lines"])):
                    if(k>=4):
                        ((SW_global.axes_data[str(i)]["lines"])[k]).set_color("black")


        #if(SW_global.click_x>0):
         #   if(pos1!=pos2):
          #      pos1=len(delete_list)-1
           #     pos2=len(delete_list)-1
        for de in SW_global.cursor_data:
            de.set_visible(False)

        ########      SWglobal single cursor      for multiple guide line#####
        if((end_axes==guideline_axes[l]) and (start_axes==guideline_axes[l])):
            invisible_item=SW_global.cursor_data[len(SW_global.cursor_data)-1]
            invisible_item.set_visible(False)
            visible_item=SW_global.cursor_data[pos1]
            single_click_cursor_pos=SW_global.cursor_pos[pos1+1]
            cursor_y=list(np.linspace(-900,1500,500))
            SW_global.single_click_pos=SW_global.cursor_pos[pos1+1]
            cursor_x=list(np.full((500),SW_global.single_click_pos-manuscript.x_max[delete_list[pos1]]))

            if(SW_global.release_x>=SW_global.cursor_pos[-1]):
            #print("yes I got in outer letter line ")
                SW_global.single_click_data=SW_global.cursor_data[-1]
                SW_global.single_click_data.set_visible(True)
            else:
                plot_data=guideline_axes[l].plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                SW_global.single_click_data=plot_data[0]
        else:
           # print("it's ok")

           # print("this is pos1",pos1)

            for i in range(len(SW_global.axes_data)):
                if((SW_global.axes_data[str(i)]["axis_data"])==end_axes):
                   # print("I am in axis data")
                    single_click_cursor_pos=(SW_global.axes_data[str(i)]["cursor_pos"])[pos1+1]
                   # print(single_click_cursor_pos)

                    kq1=(SW_global.axes_data[str(i)]["delete_list"])[pos1]
                    kq3=(single_click_cursor_pos)-manuscript.x_max[kq1]
                    print(SW_global.single_click_pos-manuscript.x_max[kq1])
                    print(manuscript.x_max[kq1])
                    cursor_y=list(np.linspace(-900,1500,500))
                    cursor_x=list(np.full((500),single_click_cursor_pos-manuscript.x_max[kq1]))
                    kq=SW_global.axes_data[str(i)]["axis_data"]
                    print(kq)
                    plot_data=kq.plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                    SW_global.single_click_data=plot_data[0]
            fig.canvas.draw()
            



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
    filewin = Toplevel(SW_Main_UI)
    button = Button(filewin, text="Do nothing button")
    button.pack()


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

    def on_exit(cur_window):
        print('exit', cur_window.winfo_id(), 'window')
        # all_windows.st_remove(cur_window)
        all_windows.pop(str(cur_window.winfo_id()))
        cur_window.destroy()

    def getactivewindow(event,arg):
        global active_window
        print(event.x,event.y)
        print(arg.winfo_id())
        print(active_window)
        active_window=arg
        print(active_window)
        # print(arg)

    childWindow = tk.Toplevel(master=master)
    childWindow.wm_transient(master)
    childWindow.protocol('WM_DELETE_WINDOW', lambda: on_exit(childWindow))
    label1 = tk.Label(childWindow, text=str("PP")).pack()
    all_windows.update({str(childWindow.winfo_id()): childWindow})
    chd = childWindow
    childWindow.bind('<Button-1>', lambda event, arg=chd: getactivewindow(event, arg))
    childWindow.title('child window {}'.format(childWindow.winfo_id()))
    width, height = 500, 500
    centre_x, centre_y = childWindow.winfo_screenwidth() / 2 - width / 2, childWindow.winfo_screenheight() / 2 - height / 2
    childWindow.geometry('{}x{}+{}+{}'.format(width, height, int(centre_x), int(centre_y)))

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
def delguideline():
    if SW_global.gdaxes == key_c:
        SW_global.gd_flag1 = False
        SW_global.g_val.set_position([0.01, 0.01, 0, 0])
        SW_global.g_val.set_visible(False)
        SW_global.g_val.cla()
        fig.canvas.draw()
        SW_global.recent_input_list1.clear()
        SW_global.kern_list1.clear()
        SW_global.kern_list1.insert(0, 0)
        kern_value_array1.clear()
        delete_list1.clear()
        if SW_global.new_gd == 1:
            guideline_axes1_1.set_position([0.00001, 0.0001, 0, 0])
            guideline_axes1_1.set_visible(False)
            guideline_axes1_1.cla()
            mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom+0.15, SW_global.top)
            mainselector.update()
        fig.canvas.draw()

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
    mainselector.extents = (0.99,0.01,0.83,0.98)

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

def add_text_box():
    global  gl, gb
##    if guideline_axes[l].get_visible() == False:
##        guideline_axes[l].set_visible(True)
##        guideline_axes[l].set_position([0.01, 0.83, 0.98, 0.15])
##        default_guideline(guideline_axes[l])
##        guideline_axes[l].tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
##    else:
    call_multigudeline()

    fig.canvas.draw()

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
        c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
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
        c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
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

        arr_img = plt.imread(filename)
        imagebox = OffsetImage(arr_img, zoom=0.08)
        imagebox.image.axes = dynamic_axes

        for xi in range(25, 400, 25):
            ab = AnnotationBbox(imagebox, (xi, 1.1),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 0),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()

        ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        for yi in range(25, 400, 25):
            ab = AnnotationBbox(imagebox, (yi, -0.09),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 1),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()
            ###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # Left_BorderArt
            ##for xx in np.arange(0,1,0.4):

            ab = AnnotationBbox(imagebox, (-0.8, -0.1),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 1),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()

            ab = AnnotationBbox(imagebox, (-0.8, 0.3),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, .5),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()

            ab = AnnotationBbox(imagebox, (-0.8, 0.8),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, .5),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()

            ab = AnnotationBbox(imagebox, (-0.8, 1.1),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 0),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()
            # =======================================================================================
            # Rightside_BorderArt

            ab = AnnotationBbox(imagebox, (402, 1.1),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 0),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()

            ab = AnnotationBbox(imagebox, (402, 0.8),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, .5),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()

            ab = AnnotationBbox(imagebox, (402, 0.3),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, .5),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()

            ab = AnnotationBbox(imagebox, (402, -0.09),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 1),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab).draggable()
        # =======================================================================================

        fig.canvas.draw()

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
        Letter_Out_Line_Apply()
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
                c1, c2 = manuscript_connect_dot.return_manuscript_fonts(glyph)
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

                c1, c2 = manuscript_connect_dot.return_manuscript_fonts(glyph)
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
    global connect_dot_flag_pos
    if SW_global.connectdot_on_off == 1:
        delete_list_counter = len(delete_list)

        if connect_dot_flag_pos == 0:
            for i in range(delete_list_counter):
                glyph = delete_list[i]
                krn = kern_value_array[i]
                connect_dot_flag_pos = connect_dot_flag_pos + 1
                initial_connect_dot_pos = len(guideline_axes[l].lines)

                c1, c2 = manuscript_connect_dot.return_manuscript_fonts(glyph)
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

                c1, c2 = manuscript_connect_dot.return_manuscript_fonts(glyph)
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
            c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
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
            c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
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
                c1, c2 = manuscript.return_manuscript_fonts(user_input)
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
        if SW_global.ba_flag == True or SW_global.ba_size == 1:
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

            arr_img = plt.imread(filename)
            imagebox = OffsetImage(arr_img, zoom=zz)

            imagebox.image.axes = dynamic_axes

            for xi in range(25, xt, 25):
                ab = AnnotationBbox(imagebox, (xi, 1),
                                    xycoords=("data", "axes fraction"),
                                    boxcoords="offset points",
                                    box_alignment=(1, 0),
                                    bboxprops={"edgecolor": "none"})

                dynamic_axes.add_artist(ab)

            ###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            for yi in range(25, xt, 25):
                ab = AnnotationBbox(imagebox, (yi, 0),
                                    xycoords=("data", "axes fraction"),
                                    boxcoords="offset points",
                                    box_alignment=(1, 1),
                                    bboxprops={"edgecolor": "none"})

                dynamic_axes.add_artist(ab)

            ###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            # Rightside_BorderArt
            ##for xx in np.arange(0,1,0.4):

            ab = AnnotationBbox(imagebox, (0, 0),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 1),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab)

            ab = AnnotationBbox(imagebox, (0, 0.3),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, .5),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab)

            ab = AnnotationBbox(imagebox, (0, 0.8),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, .5),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab)

            ab = AnnotationBbox(imagebox, (0, 1),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 0),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab)

            # =======================================================================================
            # Left_BorderArt

            ab = AnnotationBbox(imagebox, (300, 1),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(.5, 0),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab)

            ab = AnnotationBbox(imagebox, (300, 0.8),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, .5),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab)

            ab = AnnotationBbox(imagebox, (300, 0.5),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, .5),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab)

            ab = AnnotationBbox(imagebox, (300, 0.3),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 1),
                                bboxprops={"edgecolor": "none"})

            dynamic_axes.add_artist(ab)
            fig.canvas.draw()

        else:

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
        value1 = widget.get(selection[0])
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
        if color_letter_features_on_off:
            c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
        else:
            c1, c2 = manuscript.return_manuscript_fonts(user_input)

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



####### function for  add letter for multiple guideline ################

def cut_addletter_for_multiple_guideline(rectangle_wigets_no=None):
    #     b["axes_data"]=guideline_axes[l]
    # b["lines"]=guideline_axes[l]
    # b["compositedot_already_applied_array"]=[i for i in compositedot_already_applied_array]
    # b["decisiondot_already_applied_array"]=[i for i in decisiondot_already_applied_array]
    # b["startdot_already_applied_array"]=[i for i in startdot_already_applied_array]
    # b["connectdot_already_applied_array"]=[i for i in connectdot_already_applied_array]
    # b["kern_value_array"]=[i for i in kern_value_array]
    # b["kern_list"]=[i for i in SW_global.kern_list]
    # b["connect_dot_flag_pos"]=connect_dot_flag_pos
    # b["decision_dot_flag_pos"]=decision_dot_flag_pos
    # b["startdot_flag_pos"]=startdot_flag_pos
    # b["stoke_arrow_flag_pos"]=stoke_arrow_flag_pos
    # b["decision_dot_flag_pos"]=decision_dot_flag_pos
    # b["connect_dot_flag_pos"]=connect_dot_flag_pos
    # b["cursor_pos"]=[i for i in SW_global.cursor_pos]
    # b["cursor_data"]=[i for i in SW_global.cursor_data]
    # b["gval"]=[i for i in SW_global.g_val.lines]
    #print()


    return 




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
            c1, c2 = manuscript_Color_Letters.return_manuscript_color_fonts(user_input)
        else:
            c1, c2 = manuscript.return_manuscript_fonts(user_input)
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

        k=plt.plot(cursor_x, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
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

def newCreateGuideLine(n,a,b,c,d):
    global gl, gb, sl_t, sl_b, l,key_c, l
    height_axes=((0.15*100*SW_global.count_for_height)/100) #### staic for first then we have to use dynamic
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

    #temp=[i for i in guideline_axes[l].lines]
    guideline_axes[l] = plt.axes([old_l, old_b-height_axes, 0.98, 0.15])
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
    # for i in range(len(SW_global.axes_data)):
    #     print("This is axes data")
    #     print("This is for ",str(i))
    #     print(SW_global.axes_data[str(i)])
    #     print("This is axes data end")
    fig.canvas.draw()
    return




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Press Function <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def press(event):
    if(SW_global.single_click_data!=None):
        SW_global.single_click_data.set_visible(False)

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
        SW_global.copy_string=""
    if(event.key=='ctrl+v'):
        print(pos2i)
        print(SW_global.click_x)
        print(SW_global.release_x)
        print(pos1i)
        print("i am in ctrl+v")
        pos4=-1
        print(delete_list)
        if(int(SW_global.click_x)==int(SW_global.release_x)):
            if(SW_global.click_x==0):
                pos4=0
            else:
                for i in range(len(SW_global.cursor_pos)):
                    if((SW_global.cursor_pos[i]>SW_global.click_x)):
                        pos4=i
                        break
            print(pos4)

            if(pos4==-1):
                pos4=len(SW_global.cursor_pos)-1
            else:
                pos4=pos4-1
            print(pos4)
            import pyperclip
            k1=list(pyperclip.paste())
            print(len(k1))
            delete_list11=[]
            delete_list22=[]
            for i in delete_list:
                delete_list22.append(i)
            if(len(k1)>0):
                print("I got paste with greater zero length")
                for i in k1:
                    delete_list22.insert(pos4,i)
                    pos4=pos4+1
                print(delete_list22)
                for i in range(len(SW_global.g_val.lines)):
                    if(i>3):
                        item=SW_global.g_val.lines[i]
                        item.set_visible(False)
                fig.canvas.draw()
                
                print("This is delete list")
                print(delete_list22)
                SW_global.letters_already_written.clear()
                SW_global.kern_list.insert(0,0)
                SW_global.kern_list.insert(0,0)
                SW_global.cursor_pos=[0]
                SW_global.cursor_data=[]
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
                decision_dot_flag_pos=0
                connect_dot_flag_pos=0
                while(len(SW_global.letters_already_written)==3):
                    del SW_global.letters_already_written[len(SW_global.letters_already_written)-1]
                print("This is beging delete_list")
                print(delete_list22)
                for i in delete_list22:
                    print(i)
                    cut_addletter(i)
                fig.canvas.draw()
                print("Delete list")
                delete_list.clear()
                for i in delete_list22:
                    delete_list.append(i)
                print(delete_list)
                print(SW_global.letters_already_written)
                composite_dot()
                start_dot()
                Decision_dot()
                connect_dot()

                fig.canvas.draw()
            else:
                print("I got paste length zero")



    if(event.key=='ctrl+x'):
        print("This is ctrl+x")
        print(delete_list)
        import pyperclip
        k_copy=SW_global.copy_string

        pyperclip.copy(k_copy)
        SW_global.copy_string=""
        print("I am cutting")
        print(pos11_start)
        print(pos22_end)
        if(pos11_start>=0):
            if(pos22_end>=0):
                Starting_loop_point1=SW_global.letters_already_written[pos11_start]
                ending_loop_point1=SW_global.letters_already_written[pos22_end]
                temp_array=[]
                ####  This  is cut operation ########
                if(int(SW_global.click_x)!=int(SW_global.release_x)):
                    for i in range(len(SW_global.g_val.lines)):
                        if(i>3):
                            k1=SW_global.g_val.lines[i]
                            k1.set_visible(False)

                    delete1=[]
                    for i in range(len(delete_list)):
                        if((i>=pos1i) and (i<=pos2i)):
                            bg=1
                        else:
                            delete1.append(delete_list[i])
                  #  print("This is delete list")
                    print(delete1)
                    delete_list.clear()
                    for i in delete1:
                        delete_list.append(i)

                    print(pos1i)
                    print(pos2i)
                   # print("This is cursor pos")
                    print(SW_global.cursor_data)
                    print(SW_global.cursor_pos)
                    #for i in range(pos)
                    loop_start11=pos1i+1
                    loop_end11=pos2i+1
                    print(loop_start11)
                    print(loop_end11)
                    cur_delete1=[]
                    cur_delete2=[]
                    for i in range(len(SW_global.cursor_pos)):
                    #    print("I am in loop")
                        if((i>=loop_start11) and (i<=loop_end11)):
                           # print(i)
                           # print(loop_start11)
                           # print(loop_end11)
                            bo=1
                        else:
                            #cur_delete1.append(SW_global.cursor_data[i])
                            cur_delete2.append(SW_global.cursor_pos[i])
                    print("This is after deletion operation")
                   # print(cur_delete1)
                   # print(cur_delete2)
                    for i in range(len(SW_global.cursor_data)):
                        if((i>=pos1i) and (i<=pos2i)):
                            print(i)
                            print(loop_start11)
                            bo=2
                        else:
                            cur_delete1.append(SW_global.cursor_data[i])
                  #  print(cur_delete1)
                  #  print(SW_global.letters_already_written)
                    ### letter already written update #####
                    letters_already_written1=[]
                   # print(pos11_start)
                   # print(pos22_end)
                    ## need to add 
                    ###if((len(SW_global.letters_already_written)>=pos11_start) and (len(SW_global.letters_already_written)<=pos22_end)):
                    loop_1=SW_global.letters_already_written[0]
                    loop_2=SW_global.letters_already_written[len(SW_global.letters_already_written)-1]
                   # print("This is loop_1")
                   # print(loop_1)
                   # print(loop_2)
                    #### Set cur sor invisible####

                    k4=SW_global.cursor_data[len(SW_global.cursor_data)-1]
                   # print("main cursor data")
                   # print(k4)
                    k4.set_visible(False)
                    for i in range(loop_1,loop_2):
                    #    print("This is invisible part")
                        k=SW_global.g_val.lines[i]
                        k.set_visible(False)
                #    fig.canvas.draw()


                    if((len(SW_global.letters_already_written)>0) and (pos22_end<=(len(SW_global.letters_already_written)))):
                      #  print("This is lett")
                        for i in range(len(SW_global.letters_already_written)):
                            if((i>=pos11_start) and (i<=pos22_end)):
                                bw=3
                            else:
                                letters_already_written1.append(SW_global.letters_already_written[i])
                   # print("This is letters alereaudy update")
                   # print(letters_already_written1)
                    SW_global.kern_list.insert(0,0)
                    #delete_list=[]

                    SW_global.cursor_pos=[0]
                    SW_global.cursor_data=[] # After complication we have to add default to x=0 y=-900 to 1500
                    while(len(SW_global.letters_already_written)==3):
                        del SW_gobal.letters_already_written[len(SW_global.letters_already_written)-1]
                    SW_global.kern_list.insert(0,0)
                    SW_global.letters_already_written.clear()
                    SW_global.cursor_pos=[0]
                    SW_global.cursor_data=[]
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
                    decision_dot_flag_pos=0
                    connect_dot_flag_pos=0
                    for i in delete1:
                        print(i)
                        cut_addletter(i)
                    composite_dot()
                    start_dot()
                    Decision_dot()
                    connect_dot()
                    fig.canvas.draw()     








        



    if event.key == 'backspace':
        backspaceOperation()
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
        try:
            if(SW_global.kern_list[0]>15500):

                print("i am in optimising stage")
                #print("This is swgloba gval",SW_global.g_val.lines)
                #print(kern_value_array)
                #print(SW_global.kern_list)
                #print(guideline_axes[0])
                #print(SW_global.letters_already_written)
                #print(delete_list)
                #print("full")
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
                #temp=[i for i in guideline_axes[l].lines]
                newCreateGuideLine(1,None,None,None,None)
                #print("This is after update ")


                for i in range(len(SW_global.axes_data)):
                    print("8888888888888888888888888888888888888888888888888888888888888888888")
                    print(SW_global.axes_data[str(i)])
                    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    #print(SW_global.axes_data[str(i)])
                    print("****************************************")
                # b=dict()
                # b["axes_data"]=guideline_axes[l]
                # b["lines"]=guideline_axes[l].lines
                # b["compositedot_already_applied_array"]=compositedot_already_applied_array
                # b["decisiondot_already_applied_array"]=decisiondot_already_applied_array
                # b["startdot_already_applied_array"]=startdot_already_applied_array
                # b["connectdot_already_applied_array"]=connectdot_already_applied_array
                # b["kern_value_array"]=kern_value_array
                # b["kern_list"]=kern_list
                # SW_global.recent_axes_with_respect_rectangle_selector[str("0")]=b
                ################################## checking for guideline_axes[l]
                print("This is guideLine axes_data","*"*60)
                print(guideline_axes)
                print("**"*60)
 
        except Exception as e:
            print(e)





############################ End of multiple guide line ################################### 



        length12 = len(SW_global.recent_input_list)
        user_input = event.key
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
        SW_global.recent_input_list.insert(length12, event.key)
        #print("this is list")
        delete_list.insert(length12, event.key)
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
        #print("checking for data inserting")
        # print(delete_list)
        # print(SW_global.recent_input_list)
        # print(SW_global.letters_already_written)
        # print(SW_global.kern_list)
        # print("End")


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
        start_dot_continueous_write()
    else:
        pass

    if SW_global.decisiondot_on_off == 1:
        decision_dot_continueous_write()
    else:
        pass

    if SW_global.stokearrow_on_off == 1:
        stoke_arrow_continueous_write()
    else:
        pass

    if SW_global.connectdot_on_off == 1:
        connect_dot_continueous_write()
    else:
        pass

    if letter_out_line_on_off == 1:
        Letter_Out_Line_Continuous_writting()
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
               #  SW_global.recent_axes_with_respect_rectangle_selector[str("0")]=b
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
    SW_global.recent_axes_with_respect_rectangle_selector[str("0")]=b
    print("I am in kchange")
    if(len(SW_global.axes_data)>=1):
        for i in range(len(SW_global.axes_data)):
            if(SW_global.axes_data[str(i)]["axis_data"]==event.inaxes):
                print("I got axes *****************ok check 1")
    return


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
        fig.canvas.draw()
        
    except Exception as e:
        pass
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

    if key_c == SW_global.gdaxes:
        SW_global.gd_flag2 = True
        SW_global.new_left_axes2, SW_global.new_right_axes2, SW_global.new_bottom_axes2, SW_global.new_top_axes2 = new_left, new_right, new_bottom, new_top

        g_width = (new_right - new_left)
        g_height = (new_top - new_bottom)
        SW_global.g_val.set_position([new_left, new_bottom, g_width, g_height], which='both')

        selector_dict.update({key_c: [new_left, new_right, new_bottom, new_top]})
    ##        print("selector key_c : ", key_c)
    ##        print("selector SW_global.gdaxes :",SW_global.gdaxes)
    else:
        print(" Guideline ERROR.........")

    # if SW_global.gdaxes == key_c:
    #     SW_global.gd_flag1 = True
    #     tb_height = 0.15
    #     SW_global.new_left_axes1, SW_global.new_right_axes1, SW_global.new_bottom_axes1, SW_global.new_top_axes1 = new_left, new_right, new_bottom, new_top
    #     guideline_axes[l].set_position([new_left, new_bottom, (new_right - new_left), tb_height], which='both')
    #
    #     if SW_global.new_gd == 1:
    #         guideline_axes[l].set_position([new_left, (new_bottom + 0.15), (new_right - new_left), tb_height],
    #                                        which='both')
    #         guideline_axes1_1.set_position([new_left, new_bottom, (new_right - new_left), tb_height], which='both')
    #
    #     elif SW_global.gird_flag == True:
    #         fig_axes.axhline(y=new_top, color='red')
    #         fig_axes.axvline(x=new_left, color='red')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

    if SW_global.imgaxes == 1:
        SW_global.img_flag1 = True
        SW_global.img_left_axes1, SW_global.img_right_axes1, SW_global.img_top_axes1, SW_global.img_bottom_axes1 = new_left, new_right, new_top, new_bottom
        image_axes[y].set_position([new_left, new_bottom, (new_right - new_left), (new_top - new_bottom)],
                                   which='both')
    elif SW_global.imgaxes == 2:
        SW_global.img_flag2 = True
        SW_global.img_left_axes2, SW_global.img_right_axes2, SW_global.img_top_axes2, SW_global.img_bottom_axes2 = new_left, new_right, new_top, new_bottom
        image_axes2.set_position([new_left, new_bottom, (new_right - new_left), (new_top - new_bottom)],
                                 which='both')
    else:
        print(" Img ERROR.........")


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

frmt.add_command(label="Including in Flowing Text", command=donothing)
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


def callbackguidelineFunc(event):
    global guideline_counter
    global value1, base_x, base_y, median_y, descender_y, ascender_y, median_x, descender_x, ascender_x
    if combo_box.get() == '8':
        guideline_axes[l].cla()
        SW_global.scl = 32
        SW_global.btm_gd_1 = 0.93
        SW_global.ht_gd_1 = 0.04
        SW_global.bottom = 0.93
        SW_global.top = 0.97
        default_guideline(guideline_axes[l])
        mainselector.extents = (SW_global.left, SW_global.right, SW_global.bottom, SW_global.top)
        mainselector.maxdist = 8
        SW_global.gd_sc1 = True
        fig.canvas.draw()
        print("combobox value applied : 8")
    elif combo_box.get() == '10':
        guideline_axes[l].cla()
        SW_global.scl = 31
        SW_global.btm_gd_1 = 0.93
        SW_global.ht_gd_1 = 0.05
        SW_global.bottom = 0.93
        SW_global.top = 0.98
        mainselector.maxdist = 10
        SW_global.gd_sc1 = True
        default_guideline(guideline_axes[l])
        fig.canvas.draw()
        print("combobox value applied : 10")


def insert_fontsize_combobox(box):
    box['values'] = ['8', '10', '12',
                     '14', '16', '18', '20', '24', '30', '36', '42', '48', '54', '60',
                     '66', '72', '96', '128', '144', '160', '192']


text_font = ('Manuscript', '12')
main_frame = tk.Frame(propertybarframe)
combo_box = ttk.Combobox(main_frame, font=text_font, width=4)
propertybarframe.option_add('*TCombobox*Listbox.font', text_font)
combo_box.set('48')
combo_box.pack(side=LEFT)
main_frame.pack(side=LEFT)
insert_fontsize_combobox(combo_box)
combo_box.bind("<<ComboboxSelected>>", callbackguidelineFunc)
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
include_following_text_button = tk.Button(propertybarframe, width=23, height=32, image=include_following_text_icon)
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

raise_frame(writingareaframe1)

# ******************************************** Bottom-bar-frame End ********************************************
# --------------------------------------------------------------------------------------------------------------
SW_Main_UI.mainloop()
# ******************************************* End Grid <<<<<<<<<<********************************************
