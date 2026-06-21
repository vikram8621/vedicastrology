EXALTATION = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra"
}


def get_strength(planet, sign):

    if planet in EXALTATION:

        if EXALTATION[planet] == sign:
            return "Strong"

    return "Moderate"