from programs.programs.tanf.tanf import calculate_tanf


def calculate_andcs(screen, data):
    andcs = Andcs(screen)
    eligibility = andcs.eligibility
    value = andcs.value

    calculation = {
        'eligibility': eligibility,
        'value': value
    }

    return calculation


class Andcs():
    grant_standard = 841
    earned_standard_deduction = 65
    unearned_standard_deduction = 20
    min_age = 0
    max_age = 59

    def __init__(self, screen):
        self.screen = screen

        self.eligibility = {
            "eligible": True,
            "passed": [],
            "failed": []
        }

        self.calc_eligibility()

        self.calc_value()

    def calc_eligibility(self):

        # Has SSI
        self._condition(self.screen.has_ssi,
                        "Must be receiving SSI",
                        "Is receive SSI")

        # No TANIF
        tanf_eligible = calculate_tanf(self.screen, None)[
            "eligibility"]["eligible"]
        self._condition(not (self.screen.has_tanf or tanf_eligible),
                        "Must not be eligible for TANF",
                        "Is not eligible for TANF")

        # Has disability/blindness
        self.posible_eligble_members = []

        for member in self.screen.household_members.all():
            if member.disabled is True or member.visually_impaired is True:
                self.posible_eligble_members.append(member)
                
        self._condition(len(self.posible_eligble_members) >= 1,
                        "No one in the household has a disability or blindness",
                        "Someone in the household has a disability or blindness")

        # Right age
        for member in self.posible_eligble_members:
            is_in_age_range = self._between(member.age, Andcs.min_age, Andcs.max_age)
            if not is_in_age_range:
                self.posible_eligble_members.remove(member)
        self._condition(len(self.posible_eligble_members) >= 1,
                        "No member of the household with a disability is between the ages of 0-59",
                        "A member of the house hold is with a disability is between the ages of 0-59")

        # Income
        def calc_total_countable_income(member):
            earned = member.calc_gross_income("monthly", ["earned"])
            countable_earned = max(0, (earned - Andcs.earned_standard_deduction) / 2)

            unearned = member.calc_gross_income("monthly", ["unearned"])
            countable_unearned = max(0, unearned - Andcs.unearned_standard_deduction)

            total_countable = countable_earned + countable_unearned

            return {"member": member, "countable_income": total_countable}

        self.posible_eligble_members = map(
            calc_total_countable_income, self.posible_eligble_members)

        self.posible_eligble_members = list(filter(
            lambda m: m["countable_income"] < Andcs.grant_standard, self.posible_eligble_members))

        self._condition(len(self.posible_eligble_members) >= 1,
                        "No member of the household with a disability makes less than $248 a month",
                        "A member of the house hold is with a disability makes less than $248 a month")

    def calc_value(self):
        self.value = 0
        for member in self.posible_eligble_members:
            member_value = max(0, Andcs.grant_standard - member["countable_income"])
            self.value += member_value
        self.value *= 12

    def _failed(self, msg):
        self.eligibility["eligible"] = False
        self.eligibility["failed"].append(msg)

    def _passed(self, msg):
        self.eligibility["passed"].append(msg)

    def _condition(self, condition, failed_msg, pass_msg):
        if condition is True:
            self._passed(pass_msg)
        else:
            self._failed(failed_msg)

    def _between(self, value, min_val, max_val):
        return min_val <= value <= max_val
