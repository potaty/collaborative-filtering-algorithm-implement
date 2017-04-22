


file = open('ratings.txt', 'r')
count = 0
data = []
USER_COUNT = 6041
MOVIE_COUNT = 3953
for line in file:
    data.append(line.split('::')[:3])
random.shuffle(data)
real_data = data[:int(len(data) * 0.8)]
future_data = data[int(len(data) * 0.8):]
rating = {}
for i in xrange(1, MOVIE_COUNT):
    rating[i] = {}
user_total_rating = [0.0] * USER_COUNT
user_count = [0] * USER_COUNT
for data in real_data:
    # UserID::MovieID::Rating
    rating[int(data[1])][int(data[0])] = int(data[2])
    user_total_rating[int(data[0])] = user_total_rating[int(data[0])] + int(data[2])
    user_count[int(data[0])] = user_count[int(data[0])] + 1
### USE USER-BASED
sim = [[0.0] * 6041] * 6041
count = 0

for i in xrange(1, 6041):
    count = count + 1
    print count
    for j in xrange(i + 1, 6041):
        fz = 0.0
        fm1 = 0.0
        fm2 = 0.0
        for k in xrange(1, 3953):
            if (rating[k][i] != None and rating[k][j] != None):
                fz = fz + (1.0 * rating[k][i] - user_total_rating[i] / user_count[i]) * (1.0 * rating[k][j] - user_total_rating[j] / user_count[j])
                fm1 = fm1 + (1.0 * rating[k][i] - user_total_rating[i] / user_count[i]) ** 2
                fm2 = fm2 + (1.0 * rating[k][j] - user_total_rating[j] / user_count[j]) ** 2
        if (fm1 < 1e-10 or fm2 < 1e-10):
            sim[i][j] = 0.0
        else:
            sim[i][j] = sim[j][i] = fz / (fm1 ** 0.5) / (fm2 ** 0.5)
total = 0.0

for data in future_data:
    user = int(data[0])
    future = user_total_rating[user] / user_count[user]
    fz = 0.0
    fm = 0.0
    movie = int(data[1])
    for u in xrange(1, USER_COUNT):
        if (rating[movie][u] != 0):
            fm = fm + sim[user][u] * rating[movie]
            fz = fz + sim[user][u]
    future = future + fm / fz
    total = total + (1.0 * rating - future) ** 2

print (total / len(future_data)) ** 0.5
