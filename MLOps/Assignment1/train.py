from sklearn.tree import DecisionTreeRegressor

from misc import (
    load_data,
    preprocess_data,
    train_model,
    evaluate_model
)

df = load_data()

X_train, X_test, y_train, y_test = preprocess_data(df)

model = DecisionTreeRegressor(
    random_state=42
)

model = train_model(
    model,
    X_train,
    y_train
)

mse = evaluate_model(
    model,
    X_test,
    y_test
)

print(f"Decision Tree MSE: {mse:.4f}")