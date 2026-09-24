class Validation:
    def __init__(self,y_test,y_pred):
        self.y_test = y_test
        self.y_pred = y_pred

    def mean_absolute_error(self):
        actual_price = self.y_test
        predicted_price = self.y_pred
        absolute_errors = abs(actual_price - predicted_price)
        mae = absolute_errors.sum() / len(actual_price)
        return float(mae)
    def r2_score(self):
        actual_price = self.y_test
        predicted_price = self.y_pred
        Pool_A = ((actual_price-predicted_price)**2).sum()
        baseline_avg = self.y_test.mean()
        Pool_B = ((actual_price-baseline_avg)**2).sum()
        r2 = 1-(Pool_A/Pool_B)
        return r2
