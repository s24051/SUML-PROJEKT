import tkinter as tk
from tkinter import Entry, IntVar, Radiobutton, ttk
from src.widoki.predykcja import create_prediction_tab
from src.widoki.trening import create_training_tab
from src.widoki.model import create_model_tab
import src.MLEngine as MLEngine
from src.helpers import load_model
from os.path import isfile

class Profile:
    def __init__(self):
        self.city = "warszawa"
        self.type = "Blok"
        self.square_meters = 20
        self.rooms = 1
        self.condition = "Low"
        self.distanceFromCenter = 5
        self.hasParkingSpace = False
        self.hasBalcony = False
        self.hasElevator = False
        self.hasSecurity = False
        self.hasStorageRoom = False

class Model:
    def __init__(self):
        self.cached_path = "./cache/cached_model.model_meta"
        self.model = {}
        self.info = {}
        self.metrics = {}
        self.listeners = []

    def update(self, update):
        print("model update")
        self.model = update["model"]
        self.info = update["info"]
        self.metrics = update["metrics"]
        self.notify()
    
    def updated(self):
        print("updated")
        print(self.info)
        self.notify()

    def notify(self):
        print("notify")
        for callback in self.listeners:
            print(self.info)
            callback(self)

    def add_listener(self, cb):
        self.listeners.append(cb)


def main():
    root = tk.Tk()
    root.title("wycenadomu.pl")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # preset predykcji, oraz wrapper na model
    preset = Profile()
    model = Model()

    prediction_tab = create_prediction_tab(notebook, preset,  MLEngine.predict, model)
    notebook.add(prediction_tab, text="Predykcja")

    training_tab = create_training_tab(notebook, MLEngine.train, model)
    notebook.add(training_tab, text="Trening")

    model_tab = create_model_tab(notebook, model)
    notebook.add(model_tab, text="Model")

    if isfile(model.cached_path):
        load_model(model.cached_path, model)
    root.mainloop()

if __name__ == "__main__":
    main()
