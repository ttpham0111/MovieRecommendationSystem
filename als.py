from pyspark.mllib.recommendation import ALS
from numpy import array


data = sc.textFile("data/mllib/als/test.data")
ratings = data.map(lambda line: array([float(x) for x in line.split(',')]))

rank = 10
numIterations = 20
model = ALS.train(ratings, rank, numIterations)


testdata = ratings.map(lambda p: (int(p[0]), int(p[1])))
predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).reduce(lambda x, y: x + y)/ratesAndPreds.count()
print("Mean Squared Error = " + str(MSE))