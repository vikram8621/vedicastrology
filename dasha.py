from datetime import datetime

DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}

DASHA_SEQUENCE = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury"
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury",

    "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury",

    "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury"
]


def get_current_mahadasha(
        birth_date,
        moon_degree
):

    # each nakshatra = 13°20'
    nak_size = 13.3333333333

    nak_index = int(moon_degree / nak_size)

    starting_lord = NAKSHATRA_LORDS[nak_index]

    start_index = DASHA_SEQUENCE.index(
        starting_lord
    )

    # beginning of current nakshatra
    nak_start = nak_index * nak_size

    completed = (
        moon_degree - nak_start
    ) / nak_size

    remaining_fraction = 1 - completed

    first_dasha_balance = (
        DASHA_YEARS[starting_lord]
        * remaining_fraction
    )

    age_years = (
        datetime.now() - birth_date
    ).days / 365.25

    if age_years <= first_dasha_balance:
        return starting_lord

    age_years -= first_dasha_balance

    current_index = start_index + 1

    while True:

        planet = DASHA_SEQUENCE[
            current_index % 9
        ]

        years = DASHA_YEARS[planet]

        if age_years <= years:
            return planet

        age_years -= years

        current_index += 1