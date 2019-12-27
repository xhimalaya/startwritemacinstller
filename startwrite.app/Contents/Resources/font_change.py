from SW_global import *
def font_value(value):
    try:
        print("value from font change",value)
        font_size_list = {
                        '8':[ 55,0.95 ], 
                        '10':[ 52.57,0.94 ], 
                        '12':[ 50.14,0.93 ],
                        '14':[ 47.71,0.92 ], 
                        '16':[ 45.28,0.91], 
                        '18':[ 42.85,0.90], 
                        '20':[ 40.42,0.89 ], 
                        '24':[ 37.99,0.88 ], 
                        '30':[ 35.56,0.87 ], 
                        '36':[ 33.13,0.86 ], 
                        '42':[ 30.7,0.85 ], 
                        '48':[ 28,0.83 ], ### SW_global.scl,sl_b
                        '54':[ 25.84,0.82 ], 
                        '60':[ 23.41,0.80 ],
                        '66':[ 20.98,0.78 ], 
                        '72':[ 18.55,0.76 ], 
                        '96':[ 16.12,0.74], 
                        '128':[ 13.69,0.72 ], 
                        '144':[ 11.26,0.70 ], 
                        '160':[ 7.83,0.68 ], 
                        '192':[ 4,0.65 ],
                    }
        print("print from font change",value)
        x=font_size_list[str(value)][0]
        y=font_size_list[str(value)][1]
        return x,y
    except:
        return 11,0.83
