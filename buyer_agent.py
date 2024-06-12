from strategies import Strategy

class BuyerAgent:
    def __init__(self, strategies, assets):
        self.strategies = strategies
        self.assets = assets

    def choose_strategy(self, time_preference):
        if time_preference == "3":
            return self.strategies[0]
        elif time_preference == "7":
            return self.strategies[1]
        elif time_preference == "14":
            return self.strategies[2]
        else:
            return self.strategies[0]

    def negotiate(self, amount, time_preference):
        chosen_strategy = self.choose_strategy(time_preference)
        dollar_value = amount * chosen_strategy.dollar_percentage
        euro_value = amount * chosen_strategy.euro_percentage * self.assets.exchange_rate
        shares_value = (amount * chosen_strategy.shares_percentage * 
                        (self.assets.goldman_sachs_price + self.assets.american_express_price + self.assets.chevron_price) / 3)
        total_value = dollar_value + euro_value + shares_value
        return total_value, chosen_strategy
