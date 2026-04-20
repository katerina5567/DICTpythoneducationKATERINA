import sys
import math


args = sys.argv[1:]
params = {}

for arg in args:
    if "=" in arg:
        key, value = arg.split("=")
        params[key] = value


def incorrect():
    print("Incorrect parameters")
    sys.exit()


# Перевірка наявності type
if "--type" not in params or params["--type"] not in ["annuity", "diff"]:
    incorrect()

loan_type = params["--type"]

# Interest обов'язковий завжди
if "--interest" not in params:
    incorrect()

try:
    interest = float(params["--interest"])
    if interest <= 0:
        incorrect()
except:
    incorrect()

i = interest / (12 * 100)

# Перевірка негативних значень
for key in ["--principal", "--payment", "--periods"]:
    if key in params:
        try:
            if float(params[key]) < 0:
                incorrect()
        except:
            incorrect()

principal = float(params["--principal"]) if "--principal" in params else None
payment = float(params["--payment"]) if "--payment" in params else None
periods = int(params["--periods"]) if "--periods" in params else None


# ===== DIFF =====
if loan_type == "diff":
    if payment is not None or principal is None or periods is None:
        incorrect()

    total_paid = 0

    for m in range(1, periods + 1):
        diff_payment = math.ceil(
            principal / periods + i * (principal - (principal * (m - 1) / periods))
        )
        total_paid += diff_payment
        print(f"Month {m}: payment is {diff_payment}")

    print()
    print(f"Overpayment = {int(total_paid - principal)}")


# ===== ANNUITY =====
elif loan_type == "annuity":

    # Розрахунок платежу
    if payment is None:
        if principal is None or periods is None:
            incorrect()

        annuity = math.ceil(
            principal * (i * math.pow(1 + i, periods)) /
            (math.pow(1 + i, periods) - 1)
        )
        print(f"Your annuity payment = {annuity}!")
        print(f"Overpayment = {int(annuity * periods - principal)}")

    # Розрахунок основної суми
    elif principal is None:
        if payment is None or periods is None:
            incorrect()

        principal_calc = payment / (
            (i * math.pow(1 + i, periods)) /
            (math.pow(1 + i, periods) - 1)
        )

        principal_calc = math.floor(principal_calc)
        print(f"Your loan principal = {principal_calc}!")
        print(f"Overpayment = {int(payment * periods - principal_calc)}")

    # Розрахунок кількості місяців
    elif periods is None:
        if principal is None or payment is None:
            incorrect()

        n = math.ceil(
            math.log(payment / (payment - i * principal), 1 + i)
        )

        years = n // 12
        months = n % 12

        if years > 0 and months > 0:
            print(f"It will take {years} years and {months} months to repay this loan!")
        elif years > 0:
            print(f"It will take {years} years to repay this loan!")
        else:
            print(f"It will take {months} months to repay this loan!")

        print(f"Overpayment = {int(payment * n - principal)}")

    else:
        incorrect()