# from SW.manuscript_letter_outline import manu_letter_out_line_inner_fonts
#
# while True:
#     large = 0
#     inp = input("Enter : ")
#     x, y = manu_letter_out_line_inner_fonts.return_letter_out_inner_fonts(inp)
#     try:
#         new_x = max([max(i) for i in x])
#     except:
#         new_x = max(x)
#     print(new_x)



from SW.manuscript_letter_outline import manu_letter_start_dot

while True:
    total_x = 0
    total_y = 0
    inp = input("Enter : ")
    x, y = manu_letter_start_dot.return_letter_outline_start_dot(inp)
    for i in range(len(x)):
        total_x = total_x + x[i]
        total_y = total_y + y[i]
    print("X = ", int(total_x / len(x)))
    print("Y = ", int(total_y / len(y)))

