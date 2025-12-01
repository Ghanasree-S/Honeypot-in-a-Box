# core/utils/geoip.py
import os
try:
    import geoip2.database
except Exception:
    geoip2 = None

GEO_DB_PATH = os.environ.get("GEOIP_DB_PATH", "GeoLite2-City.mmdb")

def lookup_ip(ip):
    """
    Returns dict { country, city, lat, lon } or None
    """
    if geoip2 is None:
        return None
    if not os.path.exists(GEO_DB_PATH):
        return None
    try:
        reader = geoip2.database.Reader(GEO_DB_PATH)
        rec = reader.city(ip)
        res = {
            "country": rec.country.name,
            "country_iso": rec.country.iso_code,
            "city": rec.city.name,
            "latitude": rec.location.latitude,
            "longitude": rec.location.longitude
        }
        reader.close()
        return res
    except Exception:
        return None
