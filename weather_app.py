import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
from datetime import datetime


class UltimateWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Weather Dashboard")
        self.root.geometry("550x550")
        self.root.resizable(False, False)

        # Modern Material Dark Theme
        self.BG_DARK = "#1A1C23"
        self.BG_CARD = "#232631"
        self.FG_WHITE = "#FFFFFF"
        self.FG_GRAY = "#A0A5B5"
        self.ACCENT_BLUE = "#4A90E2"
        self.ACCENT_CYAN = "#50E3C2"

        self.root.configure(bg=self.BG_DARK)
        self.create_widgets()
        self.fetch_weather()  # Laad direct het lokale weer op basis van IP-locatie

    def create_widgets(self):
        # --- TOP SECTION: SEARCH BAR ---
        search_frame = tk.Frame(self.root, bg=self.BG_DARK, pady=15)
        search_frame.pack(fill=tk.X, padx=25)

        tk.Label(search_frame, text="Search City:", bg=self.BG_DARK, fg=self.FG_GRAY, font=("Arial", 10, "bold")).pack(
            anchor=tk.W)

        input_frame = tk.Frame(search_frame, bg=self.BG_DARK)
        input_frame.pack(fill=tk.X, pady=5)

        self.city_entry = tk.Entry(input_frame, bg=self.BG_CARD, fg=self.FG_WHITE, insertbackground=self.FG_WHITE, bd=0,
                                   font=("Arial", 12), width=35)
        self.city_entry.pack(side=tk.LEFT, ipady=6, padx=(0, 10))

        search_btn = tk.Button(input_frame, text="Get Weather", command=self.fetch_weather, bg=self.ACCENT_BLUE,
                               fg=self.FG_WHITE, activebackground="#357ABD", activeforeground=self.FG_WHITE,
                               font=("Arial", 10, "bold"), relief=tk.FLAT, padx=15)
        search_btn.pack(side=tk.RIGHT, ipady=4)

        # --- MIDDLE SECTION: CURRENT WEATHER CARD ---
        self.current_frame = tk.Frame(self.root, bg=self.BG_CARD, padx=20, pady=15)
        self.current_frame.pack(fill=tk.X, padx=25, pady=(0, 15))

        self.location_label = tk.Label(self.current_frame, text="Detecting location...", bg=self.BG_CARD,
                                       fg=self.ACCENT_CYAN, font=("Arial", 16, "bold"))
        self.location_label.pack(anchor=tk.W)

        # Temp en Beschrijving naast elkaar via grid
        info_frame = tk.Frame(self.current_frame, bg=self.BG_CARD)
        info_frame.pack(fill=tk.X, pady=10)

        self.temp_label = tk.Label(info_frame, text="--°C", bg=self.BG_CARD, fg=self.FG_WHITE,
                                   font=("Arial", 36, "bold"))
        self.temp_label.grid(row=0, column=0, sticky=tk.W)

        self.desc_label = tk.Label(info_frame, text="Fetching data...", bg=self.BG_CARD, fg=self.FG_GRAY,
                                   font=("Arial", 12, "italic"))
        self.desc_label.grid(row=0, column=1, padx=20, sticky=tk.W)

        # Grid voor alle extra weer-details (Alles wat erin kan)
        self.details_frame = tk.Frame(self.current_frame, bg=self.BG_CARD)
        self.details_frame.pack(fill=tk.X, pady=5)

        self.detail_labels = {}
        details_list = [
            ("Feels Like:", "--°C", 0, 0), ("Wind Speed:", "-- km/h", 0, 1),
            ("Humidity:", "--%", 1, 0), ("Wind Direction:", "--", 1, 1),
            ("UV Index:", "--", 2, 0), ("Precipitation:", "-- mm", 2, 1),
            ("Visibility:", "-- km", 3, 0), ("Cloud Cover:", "--%", 3, 1)
        ]

        for name, default, r, c in details_list:
            lbl = tk.Label(self.details_frame, text=f"{name} {default}", bg=self.BG_CARD, fg=self.FG_GRAY,
                           font=("Arial", 9))
            lbl.grid(row=r, column=c, sticky=tk.W, pady=3, padx=(0, 40))
            self.detail_labels[name] = lbl

        # --- BOTTOM SECTION: 3-DAY FORECAST ---
        forecast_title = tk.Label(self.root, text="3-Day Weather Forecast", bg=self.BG_DARK, fg=self.FG_WHITE,
                                  font=("Arial", 12, "bold"))
        forecast_title.pack(anchor=tk.W, padx=25, pady=(5, 5))

        self.forecast_frame = tk.Frame(self.root, bg=self.BG_DARK)
        self.forecast_frame.pack(fill=tk.X, padx=25)

        self.day_cards = []
        for i in range(3):
            card = tk.Frame(self.forecast_frame, bg=self.BG_CARD, padx=10, pady=10, width=150)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0 if i == 0 else 10, 0))

            day_lbl = tk.Label(card, text=f"Day {i + 1}", bg=self.BG_CARD, fg=self.ACCENT_BLUE,
                               font=("Arial", 10, "bold"))
            day_lbl.pack()

            temp_lbl = tk.Label(card, text="-- / --°C", bg=self.BG_CARD, fg=self.FG_WHITE, font=("Arial", 11, "bold"))
            temp_lbl.pack(pady=4)

            desc_lbl = tk.Label(card, text="--", bg=self.BG_CARD, fg=self.FG_GRAY, font=("Arial", 8, "italic"),
                                wraplength=130)
            desc_lbl.pack()

            rain_lbl = tk.Label(card, text="☔ --%", bg=self.BG_CARD, fg=self.ACCENT_CYAN, font=("Arial", 8))
            rain_lbl.pack(pady=2)

            self.day_cards.append({"day": day_lbl, "temp": temp_lbl, "desc": desc_lbl, "rain": rain_lbl})

    def fetch_weather(self):
        """Fetches advanced real-time and forecast weather telemetry from wttr.in."""
        city = self.city_entry.get().strip().replace(" ", "+")
        url = f"https://wttr.in{city}?format=j1"

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))

                # 1. PARSE CURRENT WEATHER
                current = data['current_condition'][0]
                area = data['nearest_area'][0]

                area_name = area['areaName'][0]['value']
                country = area['country'][0]['value']
                self.location_label.config(text=f"{area_name}, {country}")

                self.temp_label.config(text=f"{current['temp_C']}°C")
                self.desc_label.config(text=current['weatherDesc'][0]['value'].capitalize())

                # Update alle detailvelden dynamisch [1]
                self.detail_labels["Feels Like:"].config(text=f"Feels Like: {current['FeelsLikeC']}°C")
                self.detail_labels["Wind Speed:"].config(text=f"Wind Speed: {current['windspeedKmph']} km/h")
                self.detail_labels["Humidity:"].config(text=f"Humidity: {current['humidity']}%")
                self.detail_labels["Wind Direction:"].config(text=f"Wind Dir: {current['winddir16Point']}")
                self.detail_labels["UV Index:"].config(text=f"UV Index: {current['uvIndex']}")
                self.detail_labels["Precipitation:"].config(text=f"Precipitation: {current['precipMM']} mm")
                self.detail_labels["Visibility:"].config(text=f"Visibility: {current['visibility']} km")
                self.detail_labels["Cloud Cover:"].config(text=f"Cloud Cover: {current['cloudcover']}%")

                # 2. PARSE 3-DAY FORECAST
                forecast_days = data['weather']
                for idx, day_data in enumerate(forecast_days[:3]):
                    # Formateer datum naar leesbare dag (bijv. Monday, Tuesday)
                    date_obj = datetime.strptime(day_data['date'], "%Y-%m-%d")
                    day_name = date_obj.strftime("%A") if idx > 0 else "Today"

                    max_temp = day_data['maxtempC']
                    min_temp = day_data['mintempC']

                    # Pak de omschrijving en de regen kans uit het midden van de dag (index 4 = ~12:00 uur)
                    mid_day_condition = day_data['hourly'][4]
                    day_desc = mid_day_condition['weatherDesc'][0]['value']
                    rain_chance = mid_day_condition['chanceofrain']

                    # Update de kaarten onderaan het scherm [1]
                    card = self.day_cards[idx]
                    card["day"].config(text=day_name)
                    card["temp"].config(text=f"{min_temp}°C / {max_temp}°C")
                    card["desc"].config(text=day_desc.capitalize())
                    card["rain"].config(text=f"☔ {rain_chance}% Rain")

        except Exception as e:
            messagebox.showerror("Network Error", "Could not fetch advanced weather telemetry. Check your connection.")


if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateWeatherApp(root)
    root.mainloop()
