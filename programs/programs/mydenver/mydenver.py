from django.utils.translation import gettext as _
from decimal import Decimal
import math
from programs.co_county_zips import counties_from_zip

def calculate_mydenver(screen, data):
    eligibility = eligibility_mydenver(screen)
    value = value_mydenver(screen)

    calculation = {
        'eligibility': eligibility,
        'value': value
    }

    return calculation

def eligibility_mydenver(screen):
    eligible = True

    eligibility = {
        "eligible": True,
        "passed": [],
        "failed": []
    }

    eligible_counties = ['Denver County']
    child_age_min = 5
    child_age_max = 18
    child_relationship = ['child', 'fosterChild', 'stepChild', 'grandChild']
    frequency = "yearly"

    # geography test
    county_eligible = False
    counties = counties_from_zip(screen.zipcode)
    for county in counties:
        if county in eligible_counties:
            county_eligible = True

    if not county_eligible:
        eligibility["eligible"] = False
        eligibility["failed"].append(_("To qualify for the My Denver card must live in Denver County or have a child who attends a DPS school."))
    else:
        eligibility["passed"].append(_("The zipcode ")\
                +screen.zipcode\
                +_(" is within Denver County."))


    children = screen.num_children(age_max=child_age_max, age_min=child_age_min, child_relationship=child_relationship)
    if children < 1:
        eligibility['eligible'] = False
        eligibility['failed'].append(_("The My Denver card is limited to youth aged 5-18."))
    else:
        eligibility['passed'].append(_("The My Denver card is limited to youth aged 5-18."))
    return eligibility

def value_mydenver(screen):
    child_age_min = 5
    child_age_max = 18
    child_relationship = ['child', 'fosterChild', 'stepChild', 'grandChild']
    children = screen.num_children(age_max=child_age_max, age_min=child_age_min, child_relationship=child_relationship)
    value = children * 150

    return value