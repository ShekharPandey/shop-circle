# Original Code

# def calculate_discount(prices, discount):
#     result = []
#     for price in prices:
#         result.append(price - (price*discount))
#     return result
    
# prices = [100, 200, 300]
# discounts = 0.2
# final_prices = calculate_discount(prices, discounts)
# print(final_prices)


# Fixed Code
def calculate_discount(prices, discount):
    result = []
    for price in prices:
        discounted_price = price - (price * discount)  # Fixed syntax error, added discounted_price 
        result.append(discounted_price)
    return result
    
prices = [100, 200, 300]
discount = 0.2  # Changed variable name to 'discount'
final_prices = calculate_discount(prices, discount)  # Set variable name to 'discount'
print(final_prices)