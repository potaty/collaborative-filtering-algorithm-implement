import math

# assume the vectors are zero or rating.
def cosine(a, b):
	fz = 0.0
	fm1 = 0.0
	fm2 = 0.0
	if (len(a) != len(b)):
		return 0.0
	a_len = len(a)
	for i in xrange(a_len):
		if (a[i] == 0 or b[i] == 0):
			continue
		fz += a[i] * b[i]
		fm1 += a[i] ** 2
		fm2 += b[i] ** 2
	if (fm1 < 1e-10 or fm2 < 1e-10):
		return 0.0
	return fz / math.sqrt(fm1) / math.sqrt(fm2)

def average(v):
	average_v = 0.0
	if (max(v) != 0):
		average_v = (1.0 * sum(v)) / sum(map(lambda (x): 1 if x > 0 else 0, v))
	return average_v



def exactly_cosine(a, b):
	average_a = average(a)
	average_b = average(b)
	fz = 0.0
	fm1 = 0.0
	fm2 = 0.0
	if (len(a) != len(b)):
		return 0.0
	a_len = len(a)
	for i in xrange(a_len):
		if (a[i] == 0 or b[i] == 0):
			continue
		x = 1.0 * a[i] - average_a
		y = 1.0 * b[i] - average_b
		#print x, y
		fz += x * y
		fm1 += x ** 2
		fm2 += y ** 2
	if (fm1 < 1e-10 or fm2 < 1e-10):
		return 0.0
	#print fm1, fm2, fz
	return fz / math.sqrt(fm1) / math.sqrt(fm2)

