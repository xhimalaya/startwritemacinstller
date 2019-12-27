#!/usr/local/bin/python3
from SW_lib import *
import data_store_in_registry

# to get physical address:
original_mac_address = getnode()
print("MAC Address: " + str(original_mac_address))  # this output is in raw format

#convert raw format into hex format:
hex_mac_address = str(":".join(re.findall('..', '%012x' % original_mac_address)))
print("HEX MAC Address: " + hex_mac_address)

# to get Hostname and IP Address:
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)


def main_SWindow():
    sw_rgchk.destroy()
    sw_rgchk.quit()
    import SW_v03


def new_chn_rgchk():
    def blink():
        sw_rgchk.geometry("650x300+200+150")
        btn1.destroy()
        lbl1.config(text="Welcome to StartWriteIndia", pady=100, font=("Courier", 30))
        sw_rgchk.after(1080, main_SWindow)

    if sys.platform.startswith('darwin'):
        lbl1.after(1500, lambda: lbl1.config(text=platform.platform(), pady=100, font=("Courier", 25)))
        btn1.after(1500, lambda: btn1.config(state=tk.NORMAL))
        btn1.configure(command=blink)

    elif sys.platform.startswith('linux'):
        lbl1.after(1500, lambda: lbl1.config(text=platform.platform(), pady=100, font=("Courier", 15)))
        btn1.after(1500, lambda: btn1.config(state=tk.NORMAL))
        btn1.configure(command=blink)

    elif platform.system() == 'Windows':
        lbl1.after(1500, lambda: lbl1.config(text=platform.platform(), pady=100, font=("Courier", 25)))
        btn1.after(1500, lambda: btn1.config(state=tk.NORMAL))
        btn1.configure(command=blink)

    btn1['state'] = tk.DISABLED
    lbl1.configure(text="Checking OS Please Wait...", pady=100, font=("Courier", 25))


sw_rgchk = tk.Tk()
sw_rgchk.geometry("640x380+200+150")
sw_rgchk.title("Startwrite One Try Trail Version")

if "nt" == os.name:
    sw_rgchk.wm_iconbitmap(bitmap="icons/Startwrite.ico")
else:
    sw_rgchk.iconphoto(True, PhotoImage(file=os.path.join("icons/Startwrite.png")))


with open("startwriteonetrytrailversion.txt", "r") as f:
    lbl1 = Label(sw_rgchk, text=f.read(), font=("Courier", 14))
    lbl1.pack(pady=10)

btn1 = tk.Button(sw_rgchk, text="Ok", width=10, command=new_chn_rgchk)
btn1.pack(pady=10, ipadx=12)

sw_rgchk.mainloop()
