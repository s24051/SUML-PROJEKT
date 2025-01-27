import tkinter as tk
from tkinter import Entry, IntVar, Radiobutton, ttk
from tkinter.font import Font
from src.helpers import select_file, select_save, save_model, load_model

def stringifyFloat(num, d):
    return str(round(float(num), d))

def create_model_tab(notebook, model):
    modelWrapper = model
    model_frame = ttk.Frame(notebook)
    model_info_var = tk.StringVar()
    model_details_var = tk.StringVar()
    model_summary_var = tk.StringVar()

    mse_info_var = tk.StringVar()
    mae_info_var = tk.StringVar()
    r2_info_var = tk.StringVar()

    def update_gui(model_wrapper):
        info = model_wrapper.info
        print(info)
        model_info_var.set(f"Model: {info['model']}")
        if info["model"] == "Sequential":
            model_info =  f"Epochs: {info['epochs']}, Learning Rate: {info['learning_rate']}"
            if info["lrlOnPlateau"] > 0:
                model_info += f", ReduceLROnPlateau (patience {info['lrlOnPlateau']})"
            if info["earlyStopping"] > 0:
                model_info += f", EarlyStopping (patience {info['earlyStopping']})"
        else:
            model_info = f"Max Depth: {info['max_depth']}, Test size: {info['test_size']}"
        model_details_var.set(model_info)
        model_summary_var.set(info['summary'])
            
        validation = model.metrics
        mse_info_var.set(f"MSE: {stringifyFloat(validation['mse'], 2)}")
        mae_info_var.set(f"MAE: {stringifyFloat(validation['mae'], 2)}")
        r2_info_var.set( f"R2:  {stringifyFloat(validation['r2'], 2)}")


    model.add_listener(update_gui)
    boldFont = Font(family="Arial", size=12, weight="bold")
    ttk.Label(model_frame, text="Model Basic Information", font=boldFont).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(model_frame, textvariable=model_info_var).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(model_frame, textvariable=model_details_var).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(model_frame, textvariable=model_summary_var).grid(row=3, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(model_frame, text="Model Metrics", font=boldFont).grid(row=4, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(model_frame, textvariable=mse_info_var).grid(row=5, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(model_frame, textvariable=mae_info_var).grid(row=6, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(model_frame, textvariable=r2_info_var).grid(row=7, column=0, padx=5, pady=5, sticky="w")
    
    def save():
        dataset_path = select_save("Model", "model_meta")
        save_model(model, dataset_path)

    def load():
        dataset_path = select_file("Model", "model_meta")
        load_model(dataset_path, model)
        model.updated()

    ttk.Button(model_frame, text="Zapisz", command=save).grid(row=14, column=0, padx=5, pady=5, sticky="w")
    ttk.Button(model_frame, text="Wczytaj", command=load).grid(row=14, column=1, padx=5, pady=5, sticky="w")
    return model_frame

    