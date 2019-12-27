import numpy as np
import matplotlib.pyplot as plt
import tkinter
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
from tkinter import filedialog
from skimage.transform import rescale, resize, downscale_local_mean
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import inspect
# from PIL import Image
import numpy as np

def DrawBorderArt(dynamic_axes,fig1=None,image=None,size=30):
    print('\n\n\n\n#######################\n\t\t\t',dynamic_axes.__dir__(),'\n#######################')
    zoom_index = 1*(size)/30
    # image = filedialog.askopenfilename()

    if image:

        arr_img = plt.imread(image)
        arr_img = resize(arr_img,[35,35])
        imagebox = OffsetImage(arr_img,zoom=zoom_index)
        img_width,img_height,*useless = arr_img.shape
        img_width,img_height = img_width*zoom_index, img_height*zoom_index
        imagebox.image.axes = fig1
        print(fig1,dynamic_axes.get_xlim())
        print('image dimensions',img_width,img_height)
        axes_width = dynamic_axes.axes.get_position().x1 - dynamic_axes.axes.get_position().x0
        axes_height = dynamic_axes.axes.get_position().y1 - dynamic_axes.axes.get_position().y0
        print('axes dimensions', axes_height,axes_width)
        print('__dir__()',dynamic_axes.axes.xaxis)
        print('dynamic_axes.axes.get_position().x0',dynamic_axes.axes.get_position().x0)  
        print('dynamic_axes.axes.get_position().x1',dynamic_axes.axes.get_position().x1) 
        print('dynamic_axes.axes.get_position().y0',dynamic_axes.axes.get_position().y0)  
        print('dynamic_axes.axes.get_position().y1',dynamic_axes.axes.get_position().y1) 

        def Map(num_itr):
            return np.linspace(0,1,len(num_itr))

        x_axis_img_intervals = np.arange(-35,dynamic_axes.get_xlim()[-1]/img_width,img_width)
        # LOWER AXIS
        print('x_axis_img_intervals',x_axis_img_intervals, len(x_axis_img_intervals))
        for xi in x_axis_img_intervals:#
            # print(xi)
            ab = AnnotationBbox(imagebox, (xi,0),
                            xycoords=("data", "axes fraction"),
                            boxcoords="offset points",
                            box_alignment=(0, 1),
                            bboxprops={"edgecolor": "none"},
                            pad=0.)
            dynamic_axes.add_artist(ab)    
        #TOP AXIS
        for xi in x_axis_img_intervals:#
            # print(xi)
            ab = AnnotationBbox(imagebox, (xi,1),
                            xycoords=("data", "axes fraction"),
                            boxcoords="offset points",
                            box_alignment=(0, 0),
                            bboxprops={"edgecolor": "none"},
                            pad=0.)
            dynamic_axes.add_artist(ab)   

         
            # res = [1]
            # num_itr.sort()
            # reversed_list = [*reversed(num_itr)]
            # for i,v in enumerate(reversed_list):
            #     if i < len(reversed_list)-2:
            #         ratio = reversed_list[i] / reversed_list[i+1]
            #         res.append(res[i]/ratio) 
            # final = [*reversed(res)]
            # final.insert(0,0) 
            # return final
        # RIGHT AXIS 
        img_intervals = Map(np.arange(0,(dynamic_axes.get_ylim()[-1])/img_height,img_height/2))
        print(img_intervals)
        print("This is check point 1")
        for i,yi in enumerate(img_intervals):
            print("This is i",i)
            if i<= len(img_intervals)-2:
                ab = AnnotationBbox(imagebox, (x_axis_img_intervals[-1],yi),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(0, 0),
                                bboxprops={"edgecolor": "none"},
                                pad=0.)
                dynamic_axes.add_artist(ab)   


        # LEFT AXIS
        left_wall_pos = dynamic_axes.get_xlim()[0]*zoom_index
        for i,yi in enumerate(img_intervals):
            if i<= len(img_intervals)-2:
                ab = AnnotationBbox(imagebox, (0,yi),
                                xycoords=("data", "axes fraction"),
                                boxcoords="offset points",
                                box_alignment=(1, 0),
                                bboxprops={"edgecolor": "none"},
                                pad=0.)
                dynamic_axes.add_artist(ab)  
        fig1.canvas.draw()           

if __name__ == "__main__":
    root = tkinter.Tk()

    root.geometry("480x480+250+100")

    frame1 = tkinter.Frame(root)
    frame1.grid(row=0,column=0)

    frame2 = tkinter.Frame(root)
    frame2.grid(row=1, column=0)




    fig = plt.Figure(dpi=100)

    ax1 = fig.add_axes([0.05, 0.30, 0.9, 0.50])  #rect=>[left, bottom, width , height]
    ax1.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off',
                        labelleft='off')                    
    fig.set_size_inches(4.5*3, 2.2*3)

    x=[[0,15000],[0,15000],[0,15000],[0,15000]]
    y=[[-750,-750],[0,0],[750,750],[1500,1500]]

    for i in range(len(x)):
        ax1.plot(x[i],y[i])
    # fig.add_subplot(111).plot((0,-750),(0,0),(0,750),(0,1500))
    # print(ax1)



    canvas = FigureCanvasTkAgg(fig, master=frame1) # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


    # plt.show()
    # print(fig)
    # image = filedialog.askopenfilename()
    btn = tkinter.Button(frame1,text="add border art",command = lambda : DrawBorderArt(ax1,fig))
    btn.pack()


    root.mainloop()