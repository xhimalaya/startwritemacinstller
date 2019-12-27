
def kern_add_operation(x, y, kern_x):
    cont = kern_x
    draw_type = 0
    for i in range(len(x)):
        try:
            ln = len(x[i])
            for j in range(ln):
                x[i][j] = x[i][j] + cont
                draw_type = 2
        except TypeError:
            x[i] = x[i] + cont
            draw_type = 1

    return x, y, draw_type
