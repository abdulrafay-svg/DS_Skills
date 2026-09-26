class Validation:
    def __init__(self):
        pass

    def mean_absolute_error(self, y_test, y_pred):
        actual_price = y_test
        predicted_price = y_pred
        absolute_errors = abs(actual_price - predicted_price)
        mae = absolute_errors.sum() / len(actual_price)
        return float(mae)

    def r2_score(self, y_test, y_pred):
        actual_price = y_test
        predicted_price = y_pred
        Pool_A = ((actual_price - predicted_price)**2).sum()
        baseline_avg = y_test.mean()  # Fixed: use the passed y_test here instead of self.y_test
        Pool_B = ((actual_price - baseline_avg)**2).sum()
        r2 = 1 - (Pool_A / Pool_B)
        return float(r2)

