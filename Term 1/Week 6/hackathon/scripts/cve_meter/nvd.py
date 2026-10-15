"""The NVD: the official record of one CVE, and the CVSS score we take from it."""
import requests

from . import config

NVD_SOURCE = "nvd@nist.gov"
NOT_FOUND = {"nvd_status": "Not found"}  # the id is reserved, mistyped or too new for the NVD


def fetch(cve_id):
    """The NVD's record of one CVE, or None when the NVD does not know the id."""
    headers = {"User-Agent": config.USER_AGENT}
    if config.NVD_API_KEY:
        headers["apiKey"] = config.NVD_API_KEY
    r = requests.get(config.NVD_URL, params={"cveId": cve_id}, headers=headers, timeout=60)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    found = r.json()["vulnerabilities"]
    return found[0]["cve"] if found else None


def best_score(cve):
    """The score to show: the NVD's own if there is one, otherwise a CNA's, newest CVSS version first."""
    # Only the source says who gave a score. "type" does not: a CNA can be Primary too.
    scores = [m for entries in cve.get("metrics", {}).values() for m in entries
              if "cvssData" in m]  # an SSVC entry sits in the same list and is not a CVSS score
    if not scores:
        return {"cvss_source": "none"}
    m = max(scores, key=lambda m: (m["source"] == NVD_SOURCE, float(m["cvssData"]["version"])))
    data = m["cvssData"]
    by_nvd = m["source"] == NVD_SOURCE
    return {
        "cvss_score": data["baseScore"],
        "cvss_version": data["version"],
        "cvss_severity": data.get("baseSeverity") or m.get("baseSeverity"),  # CVSS 2 keeps it one level up
        "cvss_source": "nvd" if by_nvd else "cna",
        "cvss_cna": None if by_nvd else m["source"],
    }


def products(cve):
    """Vendor and product names: those the CNA supplied and those the NVD added (CPE)."""
    names = [f"{a.get('vendor', '')} {a.get('product', '')}".strip()
             for entry in cve.get("affected", []) for a in entry.get("affectedData", [])]
    for config_ in cve.get("configurations", []):
        for node in config_.get("nodes", []):
            for match in node.get("cpeMatch", []):
                vendor, product = match["criteria"].split(":")[3:5]  # cpe:2.3:a:vendor:product:...
                names.append(f"{vendor} {product}".replace("_", " "))
    return sorted({n for n in names if n}, key=str.lower)


def parse(cve):
    """The columns of the cves table that come from the NVD."""
    description = next((d["value"] for d in cve.get("descriptions", []) if d["lang"] == "en"), None)
    return {
        "nvd_status": cve.get("vulnStatus"),
        "description": description,
        "products": "\n".join(products(cve)) or None,
        **best_score(cve),
    }
