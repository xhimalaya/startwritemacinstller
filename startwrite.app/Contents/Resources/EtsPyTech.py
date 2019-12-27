def dev_details():
    devinfo = 472054174768796337289255662761302807153682040363081911193182652280889708
    return devinfo.to_bytes((devinfo.bit_length() + 7) // 8, 'big').decode()
