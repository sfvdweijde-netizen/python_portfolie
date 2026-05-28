import tkinter as tk
from tkinter import messagebox, ttk
import urllib.request
import json
from datetime import datetime


class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Currency Converter with History")
        self.root.geometry("680x340")  # Venster verbreed voor het geschiedenispaneel
        self.root.resizable(False, False)

        # Design Constants
        self.BG_COLOR = "#23272A"
        self.BG_LIGHT = "#2C2F33"
        self.FG_COLOR = "#FFFFFF"
        self.ACCENT_COLOR = "#7289DA"
        self.root.configure(bg=self.BG_COLOR)

        self.rates = {}
        self.fetch_live_rates()
        self.create_widgets()

    def fetch_live_rates(self):
        """Fetches the latest global currency exchange rates live via API."""
        url = "https://er-api.com"
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get("result") == "success":
                    self.rates = data.get("rates", {})
                else:
                    raise Exception("API status error")
        except Exception:
            messagebox.showwarning("Offline Mode", "Could not fetch live rates. Using offline backup rates.")
            self.rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 155.0, "CAD": 1.36}

    def create_widgets(self):
        # Configure drop-down styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.BG_LIGHT, background=self.BG_LIGHT, foreground=self.FG_COLOR,
                        arrowcolor=self.FG_COLOR)

        # Base layout splits into Left (Converter) and Right (History)
        left_frame = tk.Frame(self.root, bg=self.BG_COLOR, padx=20, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(self.root, bg=self.BG_LIGHT, padx=15, pady=15)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, width=260)

        # --- LEFT PANEL: CONVERTER ---
        tk.Label(left_frame, text="Currency Converter", bg=self.BG_COLOR, fg=self.ACCENT_COLOR,
                 font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(left_frame, text="Amount:", bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Arial", 10)).pack(anchor=tk.W,
                                                                                                          pady=(5, 0))
        self.amount_entry = tk.Entry(left_frame, bg=self.BG_LIGHT, fg=self.FG_COLOR, insertbackground=self.FG_COLOR,
                                     bd=0, font=("Arial", 12), width=25)
        self.amount_entry.pack(pady=5, ipady=4)
        self.amount_entry.insert(0, "100")

        drop_frame = tk.Frame(left_frame, bg=self.BG_COLOR)
        drop_frame.pack(fill=tk.X, pady=5)

        currency_list = sorted(list(self.rates.keys()))
        if not currency_list: currency_list = ["USD", "EUR", "GBP", "JPY", "CAD"]

        tk.Label(drop_frame, text="From:", bg=self.BG_COLOR, fg=self.FG_COLOR).grid(row=0, column=0, sticky=tk.W)
        self.from_combo = ttk.Combobox(drop_frame, values=currency_list, width=10, state="readonly")
        self.from_combo.set("EUR" if "EUR" in currency_list else currency_list[0])
        self.from_combo.grid(row=1, column=0, padx=(0, 10))

        tk.Label(drop_frame, text="To:", bg=self.BG_COLOR, fg=self.FG_COLOR).grid(row=0, column=1, sticky=tk.W)
        self.to_combo = ttk.Combobox(drop_frame, values=currency_list, width=10, state="readonly")
        self.to_combo.set("USD" if "USD" in currency_list else currency_list[0])
        self.to_combo.grid(row=1, column=1)

        convert_btn = tk.Button(left_frame, text="Convert", command=self.perform_conversion, bg=self.ACCENT_COLOR,
                                fg=self.FG_COLOR, activebackground="#5b70b3", activeforeground=self.FG_COLOR,
                                relief=tk.FLAT, font=("Arial", 11, "bold"))
        convert_btn.pack(fill=tk.X, pady=15)

        self.result_label = tk.Label(left_frame, text="Result: --", bg=self.BG_COLOR, fg=self.FG_COLOR,
                                     font=("Arial", 12, "bold"))
        self.result_label.pack(pady=5)

        # --- RIGHT PANEL: HISTORY ---
        tk.Label(right_frame, text="Conversion History", bg=self.BG_LIGHT, fg=self.FG_COLOR,
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))

        history_scroll_frame = tk.Frame(right_frame, bg=self.BG_LIGHT)
        history_scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.history_listbox = tk.Listbox(history_scroll_frame, bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Arial", 9),
                                          bd=0, highlightthickness=0)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(history_scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)

        clear_btn = tk.Button(right_frame, text="Clear History", command=self.clear_history, bg="#A80000",
                              fg=self.FG_COLOR, relief=tk.FLAT, font=("Arial", 9))
        clear_btn.pack(fill=tk.X, pady=(5, 0))

    def perform_conversion(self):
        try:
            amount = float(self.amount_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.")
            return

        from_curr = self.from_combo.get()
        to_curr = self.to_combo.get()

        if from_curr in self.rates and to_curr in self.rates:
            amount_in_usd = amount / self.rates[from_curr]
            converted_amount = amount_in_usd * self.rates[to_curr]

            result_text = f"{amount:.2f} {from_curr} = {converted_amount:.2f} {to_curr}"
            self.result_label.config(text=result_text)

            # Log to History listbox with a clean timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {result_text}"
            self.history_listbox.insert(0, log_entry)  # Adds to the top of the list
        else:
            messagebox.showerror("Error", "Selected currency data unavailable.")

    def clear_history(self):
        self.history_listbox.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
