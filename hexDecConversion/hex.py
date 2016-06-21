import random
ln = 0
gn = 0
while True:
	while gn == ln:
		gn = random.randrange(1, 16)
	
	print(hex(gn))
	o = 0
	while o != gn:
		s = input()
		o = 0
		for c in s:
			o = (o << 1) | (ord(c) - ord('0'))
	ln = gn

	print()
	nn = random.randrange(10, 16)
	print(bin(nn)[2:])
	a = 0
	while a != nn:
		a = int(ord(input()) - ord('a') + 10)
	
	print()
	
