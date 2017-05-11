from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.evaluation.prediction import RMSE, MAE


USER_ID_COL = 0
MOVIE_ID_COL = 1
RATINGS_COL = 2

data = Data()
data.load('data/ml-latest/ratings.dat', sep=',', format={'col': USER_ID_COL, 'row': MOVIE_ID_COL, 'value': RATINGS_COL, 'ids': int})

train, test = data.split_train_test(percent=70)

K = 2
svd = SVD()
svd.set_data(train)
svd.compute(k=K, min_values=5, pre_normalize=None, mean_center=True, post_normalize=True)

rmse = RMSE()
mae = MAE()
for rating, movie_id, user_id in test.get():
    try:
        pred_rating = svd.predict(movie_id, user_id)
        rmse.add(rating, pred_rating)
        mae.add(rating, pred_rating)
    except KeyError:
        continue

print 'RMSE = {}'.format(rmse.compute())
print 'MAE = {}'.format(mae.compute())

print svd.recommend(259137, is_row=False)  # User id 259137
