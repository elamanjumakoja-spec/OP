def print_receipt_header(company_name):
    border = "=" * 30
    return f"{border}\nWelcome to {company_name}\n{border}"

def format_currency(amount):
    return f"${amount:,.2f}"