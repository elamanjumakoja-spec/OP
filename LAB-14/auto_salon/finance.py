def calculate_total_price(base_price, tax_rate):
    return base_price * (1 + tax_rate)

def monthly_payment(principal, annual_rate, months):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return principal / months
    return (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -months)

def apply_discount(price, discount_percent):
    return price * (1 - discount_percent / 100)