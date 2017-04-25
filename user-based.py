import random
import math
file = open('ratings.txt', 'r')
count = 0
data = []
USER_COUNT = 6040
MOVIE_COUNT = 3952
for line in file:
    data.append(line.split('::')[:3])
random.shuffle(data)
real_data = data[:int(len(data) * 0.8)]
future_data = data[int(len(data) * 0.8):]
rating = {}
for i in xrange(1, MOVIE_COUNT + 1):
    rating[i] = {}
user_total_rating = [0.0] * (USER_COUNT + 1)
user_count = [0] * (USER_COUNT + 1)
for data in real_data:
    # UserID::MovieID::Rating
    rating[int(data[1])][int(data[0])] = int(data[2])
    user_total_rating[int(data[0])] = user_total_rating[int(data[0])] + int(data[2])
    user_count[int(data[0])] = user_count[int(data[0])] + 1
### USE USER-BASED
sim = {}
for i in xrange(1, USER_COUNT + 1):
    sim[i] = {}
    user_total_rating[i] = user_total_rating[i] / user_count[i]
count = 0

for i in xrange(1, USER_COUNT + 1):
    print count
    count = count + 1
    for j in xrange(i + 1, USER_COUNT + 1):
        fz = 0.0
        fm1 = 0.0
        fm2 = 0.0
        for k in xrange(1, MOVIE_COUNT + 1):
            if (rating[k].get(i) != None and rating[k].get(j) != None):
                fz = fz + (1.0 * rating[k][i] - user_total_rating[i]) * (1.0 * rating[k][j] - user_total_rating[j])
                fm1 = fm1 + (1.0 * rating[k][i] - user_total_rating[i]) ** 2
                fm2 = fm2 + (1.0 * rating[k][j] - user_total_rating[j]) ** 2
        if (fm1 < 1e-10 or fm2 < 1e-10):
			sim[i][j] = 0.0
        else:
			sim[i][j] = fz / math.sqrt(fm1) / math.sqrt(fm2)
			sim[j][i] = sim[i][j]
total = 0.0
for data in future_data:
    user = int(data[0])
    future = user_total_rating[user]
    fz = 0.0
    fm = 0.0
    movie = int(data[1])
    x = 0
    for u in xrange(1, USER_COUNT + 1):
    	
    	if (u == user):
    		continue
        if (rating[movie].get(u) != None and sim[user].get(u) != None):
            s = (sim[user].get(u) + 1) / 2.0
            fz = fz + s * (rating[movie].get(u) - user_total_rating[u])
            fm = fm + s
    if (fm < 1e-10):
    	if (len(rating[movie].values()) != 0):
            future = 1.0 * sum(rating[movie].values()) / len(rating[movie].values())
            x = 1
        else:
            future = user_total_rating[user]
            x = 2
    else:
    	future = future + fz / fm
    	x = 3
    total = total + ((future - float(data[2])) ** 2)
    if (future < -2):
    	print future, data[2], fz, fm, 'future, data[2], fz, fm'
        print x
print math.sqrt(total / len(future_data))
