import pandas as pd
import numpy as np
from operator import attrgetter

import pickle
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from tensorflow.keras.metrics import R2Score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

def predict(modelWrapper, data):
    print("predict")
    X_new_raw = pd.DataFrame([{
    "city": data["city"],
    "type": data["type"],
    "squareMeters": data["squareMeters"],
    "rooms": data["rooms"],
    "centreDistance": data["centreDistance"],
    "condition": data["condition"],
    "hasParkingSpace_yes": data["parking"],
    "hasBalcony_yes": data["balcony"],
    "hasElevator_yes": data["elevator"],
    "hasSecurity_yes": data["security"],
    "hasStorageRoom_yes": data["storage"]
    }])
    print(modelWrapper.model.predict(X_new_raw))
    pred = modelWrapper.model.predict(X_new_raw)
    if modelWrapper.info["model"] == "Sequential":
        return pred[0]
    
    return pred

#
# parametry
# data["randomForestRegression"] : { n_estimators, max_depth }
# data["sequential"] : { layers, epochs, learning_rate, earlyStopping, lrlOnPlateau }
# data["missing"] : "drop" | "mean"
# data["test_size"]

ignore_columns=['id', 'latitude', 'longitude', 'floor', 'floorCount', 'ownership', 'buildingMaterial', 
                'schoolDistance', 'clinicDistance','kindergartenDistance','restaurantDistance','collegeDistance',
                'pharmacyDistance','postOfficeDistance', 'poiCount', 'ownership', 'buildYear']

user_city_mapping = {
    "bialystok": 0,
    "bydgoszcz": 1,
    "czestochowa": 2,
    "gdansk": 3,
    "gdynia": 4,
    "katowice": 5,
    "krakow": 6,
    "lodz": 7,
    "lublin": 8,
    "poznan": 9,
    "radom": 10,
    "rzeszow": 11,
    "szczecin": 12,
    "warszawa": 13,
    "wroclaw": 14}
user_type_mapping = {
    "apartmentBuilding": 0,
    "blockOfFlats": 1,
    "tenement": 2
}
user_condition_mapping = {
    "normal": 0,
    "premium": 1
}

def train(data, modelRef):
    print("Train")
    df = data["df"].copy()

    print("Dropping duplicates")
    df.drop_duplicates(inplace=True)

    print("Dropping unused columns")
    df.drop(columns=ignore_columns, inplace=True)

    # encode categorical 
    print("inting categorical values")
    df["city"] = df["city"].map(user_city_mapping)
    df["type"] = df["type"].map(user_type_mapping)
    df["condition"] = df["condition"].map(user_condition_mapping)

    # manage onehotencoded values
    print("OneHotEncoding binary values")
    oneHotColumns = ['hasParkingSpace','hasBalcony','hasElevator','hasSecurity','hasStorageRoom']

    if data["missing"] == 0:
        df.dropna(subset=oneHotColumns, inplace=True)
    else:
        for c in oneHotColumns:
            mode = df[c].mode()[0]
            df[c].fillna(mode, inplace=True)

    oneHotEncoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop='first').set_output(transform='pandas')
    oneHotDf = oneHotEncoder.fit_transform(df[oneHotColumns])
    df.drop(columns=oneHotColumns, inplace=True)
    df = pd.concat([df, oneHotDf], axis=1)
    
    # handle the rest of nan values
    print("handling nan values")
    if data["missing"] == 0:
        print("dropping..")
        print(f"left with ${df.shape}")
        df = df.dropna()
    else:
        print("substituting with mean..")
        print(f"left with ${df.shape}")
        df = df.fillna(df.mean())

    X = df.drop('price', axis=1)
    Y = df['price']

    if "randomForestRegression" in data:
        return trainForest(X, Y, data, modelRef)
    elif "sequential" in data:
        return trainSequential(X, Y, data, modelRef)
    else:
        print("Err - unknown algorithm")

    return;

def trainForest(X, Y, data, modelRef):
    print("Training Forest")
    test_size = data["test_size"]
    forest_data = data["randomForestRegression"]
    n_estimators = int(forest_data["n_estimators"])
    max_depth = int(forest_data["max_depth"])

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=1)
    rf_model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, max_features='sqrt', random_state=2)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'MSE: {mse}')
    print(f'MAE: {mae}')
    print(f'R-squared: {r2}')


    modelRef.model = rf_model
    modelRef.info = {
        "model": "RandomForestRegressor",
        "max_depth": max_depth,
        "test_size": test_size,
        "summary": f"N Estimators: {n_estimators}"
    }
    modelRef.metrics = {
        "mse": mse,
        "mae": mae,
        "r2": r2
    }

    return modelRef

def trainSequential(X, Y, data, modelRef):
    print("Training Sequential")
    print(data)
    test_size = data["test_size"]
    sequential_data = data["sequential"]
    layers = int(sequential_data["layers"])
    epochs = int(sequential_data["epochs"])
    learning_rate = sequential_data["learning_rate"]
    earlyStopping = int(sequential_data["earlyStopping"])
    lrlOnPlateau = int(sequential_data["lrlOnPlateau"])

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=1)
    modelRef.model = Sequential()
    modelRef.model.add(Dense(pow(2, 2+layers), input_dim=X_train.shape[1], activation='relu'))
    for i in range(layers-1, 0, -1):
        modelRef.model.add(Dense(pow(2, 2+i), activation='relu'))

    modelRef.model.add(Dense(1, activation='linear'))
    modelRef.model.summary()
    rlronp= ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, verbose=1)

    modelRef.model.compile(loss='mse', optimizer=Adam(learning_rate=learning_rate), metrics=['mse','mae', R2Score()])

    callbacks = []
    if earlyStopping > 0:
        estop= EarlyStopping( monitor="val_loss", patience=earlyStopping, verbose=1, restore_best_weights=True)
        callbacks.append(estop)
    if lrlOnPlateau > 0:
        rlronp= ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=lrlOnPlateau, verbose=1)
        callbacks.append(rlronp)

    modelRef.model.fit(X_train, y_train, epochs=epochs, batch_size=15,  verbose=1, validation_split = test_size, callbacks=callbacks)
    print( modelRef.model.evaluate(X_test, y_test))
    loss, mse, mae, r2 = modelRef.model.evaluate(X_test, y_test)

    layer_summary = f"Layers: [ {pow(2, 2+layers)}"
    for i in range(layers-1, 0, -1):
        layer_summary += f", {pow(2, 2+i)}"
    layer_summary += ", 1 ]"
    modelRef.info = {
        "model": "Sequential",
        "layers": layers,
        "epochs": epochs,
        "earlyStopping": earlyStopping,
        "lrlOnPlateau": lrlOnPlateau,
        "learning_rate": learning_rate,
        "summary": layer_summary
    }
    modelRef.metrics = {
        "mse": mse,
        "mae": mae,
        "r2": r2
    }
    return 
    
