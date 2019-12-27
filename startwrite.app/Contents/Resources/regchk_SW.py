from SW_lib import *
import key_generation
import data_store_in_registry


def lin_purchase_wp():
    webbrowser.open_new_tab(r"https://www.startwriteindia.com/buy-the-software-license")


def valid_key_wp():
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
            abt_sw.destroy()
            print("Key Matched")
            SWdb.update_data_into_license_table_with_key(name, email, validate_key_f)
            data_store_in_registry.store_data_in_windows_registry(name, email)

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


abt_sw = Tk()
abt_sw.geometry("750x510+150+80")
abt_sw.title("Trail Version About")
abt_sw.resizable(width=False, height=False)

if "nt" == os.name:
    abt_sw.wm_iconbitmap(bitmap="icons/Startwrite.ico")
else:
    abt_sw.iconphoto(True, PhotoImage(file=os.path.join("icons/Startwrite.png")))

lbl_frm = Frame(abt_sw)
lbl_frm.pack(side=LEFT, padx=10)
img = PhotoImage(file="icons/sw60trial.png")
img = img.zoom(4)
img = img.subsample(14)
lbl1 = Label(lbl_frm, image=img)
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
