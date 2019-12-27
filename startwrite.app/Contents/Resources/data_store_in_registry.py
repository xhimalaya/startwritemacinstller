import winreg as wreg


def get_data(my_str="StartWriteIndia"):
    try:
        key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, my_str)
        return wreg.QueryValue(key, my_str)
    except:
        return False


def store_data_in_windows_registry(usr_name, user_mail):
    usr_name = usr_name.strip().lower()
    user_mail = user_mail.strip().lower()
    set_data(usr_name, user_mail)


def set_data(usr_name, user_mail):
    my_str = "StartWriteIndia"
    key = wreg.CreateKey(wreg.HKEY_CURRENT_USER, my_str)
    wreg.SetValue(key, my_str, wreg.REG_SZ, user_mail + '-' + usr_name)


def clear_data(my_str="StartWriteIndia"):
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, my_str)
    try:
        wreg.DeleteKey(key, my_str)
    except:
        print("No License is present ")
