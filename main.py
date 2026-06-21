from datetime import datetime

from astrology.geocode import get_location
from astrology.chart import calculate_chart
from astrology.strength import get_strength
from astrology.dasha import get_current_mahadasha


def main():

    dob = input("Enter date of birth (YYYY-MM-DD): ")
    tob = input("Enter time of birth (HH:MM): ")
    place = input("Enter place of birth: ")

    dt = datetime.strptime(
        f"{dob} {tob}",
        "%Y-%m-%d %H:%M"
    )

    lat, lon, timezone = get_location(place)

    chart = calculate_chart(
        dt,
        lat,
        lon,
        timezone
    )

    print("\n===== VEDIC BIRTH CHART =====\n")

    asc = chart["Ascendant"]

    print(
        f"Ascendant (Lagna): "
        f"{asc['sign']} "
        f"({asc['degree']}°)\n"
    )

    for planet, data in chart.items():

        if planet == "Ascendant":
            continue

        strength = get_strength(
            planet,
            data["sign"]
        )

        print(
            f"{planet}\n"
            f"  Degree     : {data['degree']}°\n"
            f"  Sign       : {data['sign']}\n"
            f"  House      : {data['house']}\n"
            f"  Nakshatra  : {data['nakshatra']}\n"
            f"  Strength   : {strength}\n"
        )

    # =========================
    # DASHA SECTION
    # =========================

    moon_degree = chart["Moon"]["degree"]

    current_dasha = get_current_mahadasha(
        dt,
        moon_degree
    )

    print("\n===== DASHA =====\n")

    print(
        f"Current Mahadasha: {current_dasha}"
    )


if __name__ == "__main__":
    main()