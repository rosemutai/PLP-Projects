def calculate_discount(price, discount_percent):
    if  discount_percent > 20:
        discounted_price = price * (1 - (discount_percent / 100))
        return discounted_price
    return price


user_input = input("Enter price and discount percentage separated by a comma: ")
price, discount_percentage = user_input.split(',')

print(calculate_discount(float(price), float(discount_percentage)))
