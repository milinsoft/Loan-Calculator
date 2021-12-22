# final credit calculator with annuity and differentiated payments
# python3 --type=annuity --principal=30000 --periods=-14 --interest=10

import argparse
import math


class LoanCalculator:
    def __init__(self, payment_type, monthly_payment, principal, periods, interest):
        self.payment_type = payment_type
        self.monthly_payment = monthly_payment
        self.principal = principal
        self.periods = periods
        self.interest = interest  # interest must be always provided
        self.i = float(self.interest / (
                12 * 100))  # Nominal interest rate. This is usually 1/12 of the annual interest rate, and it’s usually a float value, not a percentage.

    def diff_payment_calculation(self, m) -> float:
        return self.principal / self.periods + self.i * (
                self.principal - (self.principal * (m - 1) / self.periods))

    def periods_calculation(self) -> int:
        return math.ceil(
            math.log((self.monthly_payment / (self.monthly_payment - self.i * self.principal)),
                     1 + self.i))

    def annuity_calculation(self) -> float:
        return self.principal * (self.i * pow((self.i + 1), self.periods)) / (
                pow((self.i + 1), self.periods) - 1)

    def principal_calculation(self) -> float:
        return self.monthly_payment / (
                (self.i * pow((1 + self.i), self.periods)) /
                (pow((1 + self.i), self.periods) - 1))

    def annuity_overpayment_value(self, n: int) -> int:
        return int(n * self.monthly_payment - self.principal)

    def get_annuity_payments(self):
        if not self.periods:  # periods parameter missing, calculating it here
            self.periods = self.periods_calculation()
            if self.periods < 12:
                print('It will take {} months to repay this loan!'.format(self.periods))
            elif self.periods % 12 == 0:
                print('It will take 1 year to repay this loan!' if self.periods == 12 else 'It will take {} years to repay this loan!\nOverpayment = {}'.format(math.ceil(self.periods / 12),                                                                                                                              self.annuity_overpayment_value(self.periods)))
            elif int(self.periods) > 12:
                y, m = int(self.periods / 12), round(int(self.periods % 12))
                print('It will take {} years and {}'' months' if m != 1 else ' month',
                      'to repay this loan!'.format(y, m))
        elif not self.monthly_payment:  # annuity parameter missing, calculating it here
            self.monthly_payment = self.annuity_calculation()
            print("Your monthly payment = {}!".format(
                math.ceil(self.monthly_payment)))  # here we can add code if the last payment is not equal to the regular
        elif not self.principal:  # # principal parameter missing, calculating it here
            p = self.principal_calculation()
            print(f'Your loan principal = {p}!')

    def get_diff_payments(self):
        # for type=diff we can't calculate periods of loan principal as each payment is different
        total = 0  # Very important to declare this variable outside the loop
        if not self.monthly_payment:  # annuity parameter missing, calculating it here
            for m in range(1, self.periods + 1):
                a = self.diff_payment_calculation(m)
                total += math.ceil(a)
                print(f'Month {m}: payment is {(math.ceil(a))}!')
            print(f'\n Overpayment = {int(total - self.principal)}')


def main():
    parser = argparse.ArgumentParser(usage='',
                                     description='This god damn calculator will calculate whatever option you need.')

    parser.add_argument("--type", type=str,
                        help="Payment payment_type can be either 'annuity' or 'diff'. if no payment_type choosen the program will not work",
                        choices=["annuity", "diff"])
    parser.add_argument("--payment", type=int, help="If --type=diff, their combination is invalid")
    parser.add_argument("--principal", type=int, help="Valid with every combination")
    parser.add_argument("--periods", type=int,
                        help="Denotes the number of months and/or years  needed to repay the credit")
    parser.add_argument("--interest", type=float,
                        help="Must always be specified.")  # the first short name or an argument (must be a single dash (-)) , the second one is full

    args = parser.parse_args()

    if any([not args.interest,
            args.type not in {'annuity', 'diff'},
            args.type == 'diff' and args.payment,
            args.principal and int(args.principal) < 0,
            args.periods and int(args.periods) < 0,
            args.interest and int(args.interest) < 0,
            args.payment and int(args.payment) < 0]
           ):
        print("Incorrect parameters")
        exit()

    loan_calculator = LoanCalculator(payment_type=args.type, monthly_payment=args.payment,
                                     principal=args.principal,
                                     periods=args.periods, interest=args.interest)
    return loan_calculator.get_annuity_payments() if loan_calculator.payment_type == 'annuity' else loan_calculator.get_diff_payments()


if __name__ == '__main__':
    main()
