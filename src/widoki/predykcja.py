import pickle
import tkinter as tk
from tkinter import messagebox
from tkinter import Entry, IntVar, Radiobutton, ttk
from src.Enumy import CityEnum
from src.helpers import create_floatslider, create_slider
profile_cache_path = "./cache/profile_preset.pkl"

def create_prediction_tab(notebook, profile, prediction_function, model):
    prediction_frame = ttk.Frame(notebook)
    def predict():
        print("** ON PREDICT **")
        print(f'city: {city_combo.get()}')
        print(f'type: {type_var.get()}')
        print(f'sqm: {sqm_var.get()}')
        print(f'rooms: {rooms_var.get()}')
        print(f'center distance: {center_var.get()}')
        print(f'conditions: {conditions_var.get()}')
        print(f'balcony: {hasBalcony_var.get()}')
        print(f'parking: {hasParking_var.get()}')
        print(f'elevator: {hasElevator_var.get()}')
        print(f'security: {hasSecurity_var.get()}')
        print(f'storage: {hasStorage_var.get()}')
        print("** DATA FRAME **")
        data = {}
        data["city"] = CityEnum[city_combo.get()].value
        data["type"] = type_var.get()
        data["squareMeters"] = sqm_var.get()
        data["centreDistance"] = center_var.get()
        data["rooms"] = rooms_var.get()
        data["condition"] = conditions_var.get()
        data["balcony"] = float(hasBalcony_var.get())
        data["parking"] = float(hasParking_var.get())
        data["elevator"] = float(hasElevator_var.get())
        data["security"] = float(hasSecurity_var.get())
        data["storage"] = float(hasStorage_var.get())
        print(data)
        
        price = prediction_function(model, data)
        print(price)
        formatted_price = f"{price[0]:,.2f}".replace(",", " ").replace(".", ",")
        price_label.config(text = f"Szacowana cena: {formatted_price} PLN")

    # --- Miasto --- #
    miasta = [ 'szczecin', 'gdynia', 'krakow', 'poznan', 'bialystok', 'gdansk', 'wroclaw', 'radom',
                'rzeszow', 'lodz', 'katowice', 'lublin', 'czestochowa', 'warszawa', 'bydgoszcz']  
    ttk.Label(prediction_frame, text="Miasto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    city_combo = ttk.Combobox(prediction_frame, values=miasta, state="readonly")
    city_combo.set(profile.city) if profile.city in miasta else city_combo.current(0)
    city_combo.grid(row=0, column=1, padx=5, pady=5)

    # --- Typ --- #
    ttk.Label(prediction_frame, text="Rodzaj:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    type_var = IntVar()
    radio_frame = tk.Frame(prediction_frame, bg="lightgray", padx=10, pady=10)
    radio_frame.grid(row=1, column=1, padx=10, pady=10)
    Radiobutton(radio_frame, text="Dom", variable=type_var, value=0).pack(side="left")
    Radiobutton(radio_frame, text="Mieszkanie", variable=type_var, value=1).pack(side="left")
    Radiobutton(radio_frame, text="Kamienica", variable=type_var, value=2).pack(side="left")

    # --- Powierzchnia --- #
    sqm_var = tk.DoubleVar(value=profile.square_meters)
    create_slider(prediction_frame, sqm_var, 10, 100, "Powierzchnia [sqm]:", 3)
    

    # --- Odległość od centrum --- #
    center_var = tk.DoubleVar(value=profile.distanceFromCenter)
    create_floatslider(prediction_frame, center_var, 0, 20, "Odległość do centrum [km]:", 4)


    # --- Ilość pomieszczeń --- #
    rooms_var = tk.DoubleVar(value=profile.rooms)
    create_slider(prediction_frame, rooms_var, 0, 20, "Pomieszczeń:", 5)


    # klasa
    ttk.Label(prediction_frame, text="Klasa:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
    conditions_var = IntVar()
    class_radio_frame = tk.Frame(prediction_frame, bg="lightgray", padx=10, pady=10)
    class_radio_frame.grid(row=6, column=1, padx=10, pady=10)
    Radiobutton(class_radio_frame, text="Zwykłe", variable=conditions_var, value=0).pack(side="left")
    Radiobutton(class_radio_frame, text="Premium", variable=conditions_var, value=1).pack(side="left")


    # --- dodatkowe checkboxy --- #
    ttk.Label(prediction_frame, text="Dodatkowe:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
    hasBalcony_var = tk.BooleanVar(value=profile.hasBalcony)
    ttk.Checkbutton(prediction_frame, text="Balkon", variable=hasBalcony_var).grid(row=10, column=0, padx=5, pady=5, sticky="w")
    hasParking_var = tk.BooleanVar(value=profile.hasParkingSpace)
    ttk.Checkbutton(prediction_frame, text="Parking", variable=hasParking_var).grid(row=10, column=1, padx=5, pady=5, sticky="w")
    hasElevator_var = tk.BooleanVar(value=profile.hasElevator)
    ttk.Checkbutton(prediction_frame, text="Winda", variable=hasElevator_var).grid(row=11, column=0, padx=5, pady=5, sticky="w")
    hasSecurity_var = tk.BooleanVar(value=profile.hasSecurity)
    ttk.Checkbutton(prediction_frame, text="Ochrona", variable=hasSecurity_var).grid(row=11, column=1, padx=5, pady=5, sticky="w")
    hasStorage_var = tk.BooleanVar(value=profile.hasStorageRoom)
    ttk.Checkbutton(prediction_frame, text="Piwnica", variable=hasStorage_var).grid(row=12, column=0, padx=5, pady=5, sticky="w")


    def get_data():
        data = {}
        data["city"] = city_combo.get()
        data["type"] = type_var.get()
        data["squareMeters"] = sqm_var.get()
        data["centreDistance"] = center_var.get()
        data["rooms"] = rooms_var.get()
        data["condition"] = conditions_var.get()
        data["balcony"] = hasBalcony_var.get()
        data["parking"] = hasParking_var.get()
        data["elevator"] = hasElevator_var.get()
        data["security"] = hasSecurity_var.get()
        data["storage"] = hasStorage_var.get()
        return data;

    def save_preset():
        print("save_preset")
        try:
            data = get_data()
            pickle.dump(data, open(profile_cache_path, "wb"))
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")    

    def load_preset():
        print("load_preset")
        try:
            data = pickle.load(open(profile_cache_path,'rb'))
            print(data)
            city_combo.set(data["city"])
            type_var.set(data["type"])
            sqm_var.set(data["squareMeters"])
            center_var.set(data["centreDistance"] )
            rooms_var.set(data["rooms"] )
            conditions_var.set(data["condition"] )
            hasBalcony_var.set(data["balcony"] )
            hasParking_var.set(data["parking"] )
            hasElevator_var.set(data["elevator"] )
            hasSecurity_var.set(data["security"] )
            hasStorage_var.set(data["storage"] )
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")

    ttk.Button(prediction_frame, text="Zapisz", command=save_preset).grid(row=14, column=0, padx=5, pady=5, sticky="w")
    ttk.Button(prediction_frame, text="Wczytaj", command=load_preset).grid(row=14, column=1, padx=5, pady=5, sticky="w")
    ttk.Button(prediction_frame, text="Oszacuj cenę", command=predict).grid(row=15, column=0, columnspan=3, padx=5, pady=5)

    price_label = ttk.Label(prediction_frame, text="Szacowana cena:")
    price_label.grid(row=16, column=0, padx=5, pady=5, sticky="w")

    return prediction_frame