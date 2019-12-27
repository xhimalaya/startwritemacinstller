import webbrowser
from pathlib import Path
import os

# k='C:\Users\ets_asp 2\Desktop\test.pdf'.replace('\\','\\\\')
# data_folder = Path("C:/Users/ets_asp 2/Desktop/test.pdf")
# webbrowser.open_new(k)
print(os.getcwd())
print(str(Path(os.getcwd())))
k=str(os.getcwd())+"\ a.txt"
print(k)
#print(os.listdir(os.getcwd()))
def Print_file(file_path=None):
    if file_path!=None:
        import webbrowser
        webbrowser.open_new(file_path)
    return 

def save_file():
    # default_path=str("G:\StartWrite03-12-2019\SW\StartWrite-Desktop\StartWrite-Desktop")+""
    # SW_global.global_figure.savefig('test.')
    os.chdir('../')

    try:
        default_path=os.path.join(os.getcwd(),"test.pdf")
        SW_global.global_figure.savefig(default_path)

    except Exception as e:
        print(e)

    return 
