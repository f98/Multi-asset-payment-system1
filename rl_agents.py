import numpy as np
from strategies import Strategy
from assets import Assets

class BuyerAgent:
    def __init__(self, strategies, assets):
        self.strategies = strategies
        self.assets = assets
        self.q_table = np.zeros((3, 3))  # Placeholder for Q-learning table

    def choose_strategy(self, state):
        # Placeholder for choosing a strategy using Q-learning
        return self.strategies[np.argmax(self.q_table[state])]

    def negotiate(self, amount, time_preference):
        state = int(time_preference) // 7  # Simplistic state representation
        chosen_strategy = self.choose_strategy(state)
        dollar_value = amount * chosen_strategy.dollar_percentage
        euro_value = amount * chosen_strategy.euro_percentage * self.assets.exchange_rate
        shares_value = (amount * chosen_strategy.shares_percentage * 
                        (self.assets.goldman_sachs_price + self.assets.american_express_price + self.assets.chevron_price) / 3)
        total_value = dollar_value + euro_value + shares_value
        return total_value, chosen_strategy

class SellerAgent:
    def __init__(self, time_preference):
        self.time_preference = time_preference


