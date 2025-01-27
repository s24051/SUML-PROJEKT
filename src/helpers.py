import tkinter as tk
from tkinter import filedialog, ttk
import os
import pickle

def select_file(type, extension):
    file_path = filedialog.askopenfilename(title="Wybierz plik", filetypes=[(f"{type}", f".{extension}")])
    if file_path:
        print(f"Wybrano plik: {file_path}")
        return file_path
    else:
        print("Nie wybrano pliku.")
        return ""
    
def select_save(type, extension):
    file_path = filedialog.asksaveasfilename(title="Zapisz jako", filetypes=[(f"{type}", f".{extension}")])
    if file_path:
        print(f"Wybrano plik: {file_path}")
        return file_path
    else:
        print("Nie wybrano pliku.")
        return ""

def create_slider(frame, variable, min, max, label, row):
    ttk.Label(frame, text=label).grid(row=row, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(frame, textvariable=variable).grid(row=row, column=2, padx=5, pady=5, sticky="ew")
    variable.trace_add('write', lambda *args : variable.set(str(int(variable.get()))))
    ttk.Scale(frame, from_=min, to=max, orient=tk.HORIZONTAL, variable=variable).grid(row=row, column=1, padx=5, pady=5, sticky="w")

def create_floatslider(frame, variable, min, max, label, row):
    ttk.Label(frame, text=label).grid(row=row, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(frame, textvariable=variable).grid(row=row, column=2, padx=5, pady=5, sticky="ew")
    variable.trace_add('write', lambda *args : variable.set(str(round(float(variable.get()), 3))))
    ttk.Scale(frame, from_=min, to=max, orient=tk.HORIZONTAL, variable=variable).grid(row=row, column=1, padx=5, pady=5, sticky="w")

def save_model(modelWrapper, path):
    print(path)
    directory, filename_with_ext = os.path.split(path)
    filename = os.path.splitext(filename_with_ext)[0]

    print(directory)
    print(filename_with_ext)
    print(filename)
    meta = {
        "info": modelWrapper.info,
        "metrics": modelWrapper.metrics
    }
    pickle.dump(meta, open(f"{directory}/{filename}.model_meta", "wb"))
    pickle.dump(modelWrapper.model, open(f"{directory}/{filename}.pickle", "wb"))


def load_model(path, modelWrapper):
    directory, filename_with_ext = os.path.split(path)

    meta = pickle.load(open(f"{path}",'rb'))
    filename = os.path.splitext(filename_with_ext)[0]
    modelWrapper.model = pickle.load(open(f"{directory}/{filename}.pickle",'rb'))
    modelWrapper.info = meta["info"]
    modelWrapper.metrics = meta["metrics"]
    modelWrapper.updated()

