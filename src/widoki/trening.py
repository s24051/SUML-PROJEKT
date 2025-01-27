import tkinter as tk
from tkinter import Entry, IntVar, Radiobutton, ttk
from tkinter import messagebox
import pandas as pd
import pickle
import os
from src.helpers import select_file, create_floatslider, create_slider, save_model
model_preset_path = "./cache/model_preset.pkl"

def create_training_tab(notebook, training_function, model):
    df = None
    required_columns = ["city", "type", "squareMeters", "rooms", "centreDistance", "condition", 
                        "hasParkingSpace", "hasBalcony", "hasElevator", "hasSecurity", "hasStorageRoom"]
    def load_dataset():
        dataset_path = select_file("Dataset", "csv")
        print(dataset_path)
        try:
            _df = pd.read_csv(dataset_path)
            if not set(required_columns).issubset(_df.columns):
                raise Exception(f"Niepoprawny dataset - brakuje kolumn {set(required_columns) - set(_df.columns)}")
            messagebox.showinfo("Sukces", "Dataset wydaje się być poprawny!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")
        print(_df.head())
        nonlocal df
        df = _df

    training_frame = ttk.Frame(notebook)
    ttk.Label(training_frame, text="Trenowanie").grid(row=0, column=0, padx=5, pady=5, sticky="w")

    load_dataset_button = ttk.Button(training_frame, text="Wskaż dataset", command=load_dataset)
    load_dataset_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    test_size_var = tk.DoubleVar(value=0.2)
    create_floatslider(training_frame, test_size_var, 0, 0.5, "Stosunek danych walidacyjnych do trenowanych", 2)

    ttk.Label(training_frame, text="Brakujące dane:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    drop_mean_var = IntVar()
    class_radio_frame = tk.Frame(training_frame, bg="lightgray", padx=10, pady=10)
    class_radio_frame.grid(row=3, column=1, padx=10, pady=10)
    Radiobutton(class_radio_frame, text="Usuń", variable=drop_mean_var, value=0).pack(side="left")
    Radiobutton(class_radio_frame, text="Zastąp średnią", variable=drop_mean_var, value=1).pack(side="left")

    #######################
    ### <ALGO NOTEBOOK> ###
    #######################
    ttk.Label(training_frame, text="Algorytm").grid(row=7, column=0, padx=5, pady=5, sticky="w")
    ml_notebook = ttk.Notebook(training_frame)
    ml_notebook.grid(row=8, column=0, padx=5, pady=5, sticky="w")
  
    sequentialFrame = ttk.Frame(ml_notebook)
    ml_notebook.add(sequentialFrame, text="Sieci neuronowe")
    layers_var = tk.DoubleVar(value=3)
    epochs_var = tk.DoubleVar(value=5)
    lr_var = tk.DoubleVar(value=0.02)
    early_stopping_var = tk.DoubleVar(value=5)
    reduceLR_var = tk.DoubleVar(value=2)
    create_slider(sequentialFrame, layers_var, 2, 10, "Ilość warstw:", 0)
    create_slider(sequentialFrame, epochs_var, 1, 20, "Epok:", 1)
    create_floatslider(sequentialFrame, lr_var, 0.001, 0.1, "Współczynnik uczenia:", 2)
    create_slider(sequentialFrame, early_stopping_var, 0, 10, "Zatrzymaj po X krokach spadku dokładności:", 3)
    create_slider(sequentialFrame, reduceLR_var, 0, 10, "Zmniejsz WU po X krokach spadku dokładności:", 4)

    randomForestFrame = ttk.Frame(ml_notebook)
    ml_notebook.add(randomForestFrame, text="RandomForestRegressor")
    estimators_var = tk.DoubleVar(value=100)
    max_depth_var = tk.DoubleVar(value=20)
    create_slider(randomForestFrame, estimators_var, 10, 500, "Ilość drzew (n_estimators):", 0)
    create_slider(randomForestFrame, max_depth_var, 10, 100, "Poziomów drzew(max_depth):", 1)
    ########################
    ### </ALGO NOTEBOOK> ###
    ########################


    def train_model():
        data = get_data()
        data["df"] = df.copy()
        data["missing"] = drop_mean_var.get()
        data["test_size"] = test_size_var.get()

        if ml_notebook.index(ml_notebook.select()) == 0:
            print("Sequential selected!")
            data.pop("randomForestRegression", None)
        else:
            print("RandomForest selected")
            data.pop("sequential", None)
        messagebox.showwarning("Trening", "Trenowanie - może chwilę potrwać.")
        model_data = training_function(data, model)
        print(model_data)
        save_model(model, "./cache/cached_model")
        model.updated()
        messagebox.showinfo("Sukces", "Wytrenowano model - sprawdź w zakładce model.")

    def get_data():
        data = {}
        data["df"] = df
        data["missing"] = drop_mean_var.get()
        data["test_size"] = test_size_var.get()
        sequential = {}
        sequential["layers"] = layers_var.get()
        sequential["epochs"] = epochs_var.get()
        sequential["learning_rate"] = lr_var.get()
        sequential["earlyStopping"] = early_stopping_var.get()
        sequential["lrlOnPlateau"] = reduceLR_var.get()
        data["sequential"] = sequential
        regressor = {}
        regressor["n_estimators"] = estimators_var.get()
        regressor["max_depth"] = max_depth_var.get()
        data["randomForestRegression"] = regressor
        return data;

    def save_preset():
        print("save_preset")
        try:
            data = get_data()
            pickle.dump(data, open(model_preset_path, "wb"))
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")    

    def load_preset():
        print("load_preset")
        try:
            data = pickle.load(open(model_preset_path,'rb'))
            nonlocal df
            df = data["df"]
            drop_mean_var.set(data["missing"])
            test_size_var.set(data["test_size"])
            layers_var.set(data["sequential"]["layers"])
            epochs_var.set(data["sequential"]["epochs"])
            lr_var.set(data["sequential"]["learning_rate"])
            early_stopping_var.set(data["sequential"]["earlyStopping"])
            reduceLR_var.set(data["sequential"]["lrlOnPlateau"])
            estimators_var.set(data["randomForestRegression"]["n_estimators"])
            max_depth_var.set(data["randomForestRegression"]["max_depth"])
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")

    ttk.Button(training_frame, text="Zapisz", command=save_preset).grid(row=14, column=0, padx=5, pady=5, sticky="w")
    ttk.Button(training_frame, text="Wczytaj", command=load_preset).grid(row=14, column=1, padx=5, pady=5, sticky="w")

    train_button = ttk.Button(training_frame, text="Trenuj", command=train_model)
    train_button.grid(row=15, column=0, padx=5, pady=5, sticky="w")

    if os.path.isfile(model_preset_path):
        load_preset()
    return training_frame