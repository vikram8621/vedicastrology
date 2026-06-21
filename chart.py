import swisseph as swe
import pytz

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika",
    "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati"
]


def get_sign(degree):
    return SIGNS[int(degree / 30)]


def get_nakshatra(degree):
    nak_num = int(degree / (360 / 27))
    return NAKSHATRAS[nak_num]


def get_house(planet_degree, asc_degree):
    """
    Whole Sign Houses
    """

    asc_sign = int(asc_degree / 30)
    planet_sign = int(planet_degree / 30)

    return ((planet_sign - asc_sign) % 12) + 1


def calculate_chart(dt, lat, lon, timezone_name):

    tz = pytz.timezone(timezone_name)

    local_dt = tz.localize(dt)

    utc_dt = local_dt.astimezone(pytz.utc)

    jd = swe.julday(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        utc_dt.hour + utc_dt.minute / 60
    )

    # Lahiri Ayanamsha
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Tropical Ascendant
    cusps, ascmc = swe.houses_ex(
        jd,
        lat,
        lon,
        b'P'
    )

    tropical_asc = ascmc[0]

    # Convert to Sidereal Ascendant
    ayanamsa = swe.get_ayanamsa_ut(jd)

    asc_degree = (tropical_asc - ayanamsa) % 360

    result = {
        "Ascendant": {
            "degree": round(asc_degree, 2),
            "sign": get_sign(asc_degree)
        }
    }

    for name, planet in PLANETS.items():

        position = swe.calc_ut(
            jd,
            planet,
            swe.FLG_SIDEREAL
        )[0][0]

        result[name] = {
            "degree": round(position, 2),
            "sign": get_sign(position),
            "house": get_house(position, asc_degree),
            "nakshatra": get_nakshatra(position)
        }

    # Ketu
    rahu_degree = result["Rahu"]["degree"]

    ketu_degree = (rahu_degree + 180) % 360

    result["Ketu"] = {
        "degree": round(ketu_degree, 2),
        "sign": get_sign(ketu_degree),
        "house": get_house(ketu_degree, asc_degree),
        "nakshatra": get_nakshatra(ketu_degree)
    }

    return result