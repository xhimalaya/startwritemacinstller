import binascii

# email = input("Enter Your Mail Id : ")
# name = input("Enter Your User Name : ")

# updated_key = []
# np = ''


def key_generation(emil, nme):
    join = emil.strip().lower() + nme.lower().strip()
    a = binascii.crc32(join.encode('utf8'))
    return "%08x" % a


# key = key_generation(email, name)


# for i in range(len(key)):
#     if i == 4:
#         updated_key.append('-')
#
#     if key[i].isdigit():
#         updated_key.append(key[i])
#         continue
#     elif key[i].isalpha():
#         updated_key.append(key[i].upper())
#         continue
#     else:
#         pass
#
#
# for i in range(len(updated_key)):
#     np += updated_key[i]
#
# print(np)


'''
data set
mail = [4u.mithun@gmail.com,
 tanusree.sinha@theetsindia.com1, 
 tanusree.sinha@theetsindia.com2,
  sandip.banerjee@theetsindia.com,
   4u.mithun@gmail.com3]
id = [mit,
 tanusree, 
 tanusree,
  sandip,
   mithun]
'''