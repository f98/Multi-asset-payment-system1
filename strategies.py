class Strategy:
    def __init__(self, dollar_percentage, euro_percentage, shares_percentage):
        self.dollar_percentage = dollar_percentage
        self.euro_percentage = euro_percentage
        self.shares_percentage = shares_percentage

# Define strategies
first_strategy = Strategy(0.70, 0.2, 0.099)
second_strategy = Strategy(0.75, 0.24999, 0)
third_strategy = Strategy(0.7, 0.099, 0.2)

# Print the strategies to verify
print(f"First Strategy: Dollar - {first_strategy.dollar_percentage}, Euro - {first_strategy.euro_percentage}, Shares - {first_strategy.shares_percentage}")
print(f"Second Strategy: Dollar - {second_strategy.dollar_percentage}, Euro - {second_strategy.euro_percentage}, Shares - {second_strategy.shares_percentage}")
print(f"Third Strategy: Dollar - {third_strategy.dollar_percentage}, Euro - {third_strategy.euro_percentage}, Shares - {third_strategy.shares_percentage}")




