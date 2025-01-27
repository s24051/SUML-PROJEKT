import tkinter as tk
from tkinter import Entry, IntVar, Radiobutton, ttk
from src.Enumy import CityEnum

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
        
        print(price)
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
    ttk.Label(prediction_frame, text="Powierzchnia:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    sqm_var = tk.DoubleVar(value=profile.square_meters)

    sqm_label_var = tk.StringVar(value=str(profile.square_meters))
    sqm_label = ttk.Label(prediction_frame, textvariable=sqm_label_var)

    # Attach a trace to the variable so it calls update_rooms_label on change
    sqm_var.trace_add('write', lambda *args : sqm_label_var.set(str(int(sqm_var.get()))))
    sqm_scale = ttk.Scale(prediction_frame, from_=15, to=100, orient=tk.HORIZONTAL, variable=sqm_var)
    
    sqm_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")
    sqm_scale.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    # --- Odległość od centrum --- #
    ttk.Label(prediction_frame, text="Odległość do centrum [km]:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    center_var = tk.DoubleVar(value=profile.distanceFromCenter)
    slider = tk.StringVar()
    slider.set(profile.distanceFromCenter)
    center_distance_scale = ttk.Scale(prediction_frame, from_=0, to_=20, length=300, command=lambda s:slider.set('%0.2f' % float(s)), variable=center_var)
    center_distance_label = ttk.Label(prediction_frame, textvariable=slider)
    center_distance_scale.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    center_distance_label.grid(row=4, column=2, padx=5, pady=5, sticky="ew")



    ttk.Label(prediction_frame, text="Pomieszczeń:").grid(row=5, column=0, padx=5, pady=5, sticky="w")

    rooms_var = tk.DoubleVar(value=profile.rooms)

    # Create a label that will display the current rooms_var value
    rooms_label_var = tk.StringVar(value=str(profile.rooms))
    rooms_value_label = ttk.Label(prediction_frame, textvariable=rooms_label_var)
    rooms_var.trace_add('write', lambda *args : rooms_label_var.set(str(int(rooms_var.get()))))
    rooms_scale = ttk.Scale(prediction_frame, from_=0, to=20, orient=tk.HORIZONTAL, variable=rooms_var)
    rooms_value_label.grid(row=5, column=2, padx=5, pady=5, sticky="w")
    rooms_scale.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

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


    ttk.Button(prediction_frame, text="Oszacuj cenę", command=predict).grid(row=15, column=0, columnspan=3, padx=5, pady=5)

    price_label = ttk.Label(prediction_frame, text="Szacowana cena:")
    price_label.grid(row=16, column=0, padx=5, pady=5, sticky="w")

    return prediction_frame