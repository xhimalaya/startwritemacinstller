def check():
	a=[1,2,3,4]
	return a

def check2():
	b=[5,6,7,8]
	yield b
	check()
	return 

def check3():
	for i in check2():
		print(i)
	check2()