"""CISA's Known Exploited Vulnerabilities catalog: one file with every CVE on the list."""
import requests

from . import config


def fetch():
    """The whole catalog as {cve id: (date added, ransomware use, vendor and product)}."""
    r = requests.get(config.KEV_URL, headers={"User-Agent": config.USER_AGENT}, timeout=60)
    r.raise_for_status()
    return parse(r.json())


def parse(catalog):
    """Turns the downloaded catalog into {cve id: (date added, ransomware use, vendor and product)}."""
    return {
        v["cveID"].upper(): (v.get("dateAdded"), v.get("knownRansomwareCampaignUse"),
                             f"{v.get('vendorProject', '')} {v.get('product', '')}".strip())
        for v in catalog["vulnerabilities"]
    }
