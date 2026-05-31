from sklearn.kernel_ridge import KernelRidge

from misc import (
    load_data,
    preprocess_data,
    train_model,
    evaluate_model
)

df = load_data()

X_train, X_test, y_train, y_test = preprocess_data(df)

model = KernelRidge(
    kernel="linear"
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

print(f"Kernel Ridge MSE: {mse:.4f}")