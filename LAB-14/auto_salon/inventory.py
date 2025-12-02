def format_car_name(make, model, year):
    return f"{year} {make.upper()} {model.title()}"

def generate_slug(make, model):
    return f"{make.lower()}-{model.lower()}"

def check_vin_validity(vin):
    return len(vin) == 17 and vin.isalnum()