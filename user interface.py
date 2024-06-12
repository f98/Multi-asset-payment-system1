import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
from assets import Assets
from strategies import first_strategy, second_strategy, third_strategy
from rl_agents import BuyerAgent, SellerAgent

class MAPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to MAPS")

        # Title
        title = tk.Label(root, text="Welcome to MAPS", font=("Helvetica", 16))
        title.pack(pady=10)

        # Date picker
        self.date_label = tk.Label(root, text="Pick today's date:")
        self.date_label.pack(pady=5)

        self.date_options = self.generate_dates()
        self.date_var = tk.StringVar()
        self.date_var.set(self.date_options[0])
        self.date_menu = ttk.Combobox(root, textvariable=self.date_var, values=self.date_options)
        self.date_menu.pack(pady=5)

        # Time preference
        self.time_label = tk.Label(root, text="Enter time preference (days):")
        self.time_label.pack(pady=5)

        self.time_preference = ttk.Combobox(root, values=["3", "7", "14"])
        self.time_preference.pack(pady=5)

        # Amount to be paid
        self.amount_label = tk.Label(root, text="Enter amount to be paid:")
        self.amount_label.pack(pady=5)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(pady=5)

        # Pay button
        self.pay_button = tk.Button(root, text="Pay", command=self.process_payment)
        self.pay_button.pack(pady=20)

    def generate_dates(self):
        start_date = date(2024, 6, 11)
        return [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    def process_payment(self):
        selected_date = self.date_var.get()
        time_preference = self.time_preference.get()
        amount = self.amount_entry.get()
        print(f"Selected Date: {selected_date}, Time Preference: {time_preference} days, Amount: {amount}")
        
        # Simulate the negotiation logic
        self.simulate_negotiation(float(amount), time_preference, selected_date)

    def simulate_negotiation(self, amount, time_preference, date):
        assets = Assets()
        strategies = [first_strategy, second_strategy, third_strategy]
        buyer_agent = BuyerAgent(strategies, assets)
        seller_agent = SellerAgent(time_preference)
        
        total_value, chosen_strategy = buyer_agent.negotiate(amount, seller_agent.time_preference)
        
        print(f"Negotiated total value: {total_value}")
        print(f"Chosen strategy: Dollar - {chosen_strategy.dollar_percentage}, Euro - {chosen_strategy.euro_percentage}, Shares - {chosen_strategy.shares_percentage}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MAPSApp(root)
    root.mainloop()
