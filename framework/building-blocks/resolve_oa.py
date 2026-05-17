#!/usr/bin/env python3
"""resolve_oa.py — sources-fetch Method B (free open-access API resolver).

Resolve a paper/guideline (PMID, DOI, or title) to a *legal* open-access PDF
URL with no browser and no VPN. Called by framework/building-blocks/
sources-fetch.md on rung B of the fetch ladder; sources-fetch downloads the
returned URL into Sources/.

Legality guardrail: only PDF URLs that the open-access services themselves
report as openly licensed or author/repository-deposited are emitted —
Europe PMC (isOpenAccess) / NCBI PMC OA / Unpaywall best_oa_location. A
paywalled publisher URL is never emitted. No paywall bypass.

Stdlib only (urllib/json) — no third-party deps, consistent with
audit_references.py.

Usage:
    python resolve_oa.py (--pmid ID | --doi DOI | --title "T") [--email ADDR]
                         [--api-key KEY] [--timeout SECS]

Contact email: required by Unpaywall and requested by NCBI. Pass --email or
set MPF_CONTACT_EMAIL. Optional NCBI key via --api-key or env NCBI_API_KEY
(env only — never commit a key).

Output (stdout, single JSON line):
    success -> {"resolved": true, "pdf_url": ..., "source": ...,
                "license": ..., "doi": ..., "pmid": ..., "title": ...}
                exit 0
    no legal free copy / error -> {"resolved": false, "reason": ...}
                exit 1   (signal: fall through to Method C/D)
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

TOOL = "medical-presentation-framework"


def _get_json(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": TOOL})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def _ncbi_params(email, api_key):
    p = {"tool": TOOL}
    if email:
        p["email"] = email
    if api_key:
        p["api_key"] = api_key
    return p


def title_to_pmid(title, email, api_key, timeout):
    q = _ncbi_params(email, api_key)
    q.update({"db": "pubmed", "term": title, "retmode": "json", "retmax": "1"})
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(q)
    try:
        data = _get_json(url, timeout)
        ids = data.get("esearchresult", {}).get("idlist", [])
        return ids[0] if ids else None
    except Exception:
        return None


def title_to_doi(title, timeout):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": title, "rows": "1"}
    )
    try:
        data = _get_json(url, timeout)
        items = data.get("message", {}).get("items", [])
        return items[0].get("DOI") if items else None
    except Exception:
        return None


def pmid_ids(pmid, email, api_key, timeout):
    """Return (doi, pmcid) from NCBI esummary articleids."""
    q = _ncbi_params(email, api_key)
    q.update({"db": "pubmed", "id": pmid, "retmode": "json"})
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" + urllib.parse.urlencode(q)
    doi = pmcid = None
    try:
        data = _get_json(url, timeout)
        rec = data.get("result", {}).get(str(pmid), {})
        for aid in rec.get("articleids", []):
            t, v = aid.get("idtype"), (aid.get("value") or "").strip()
            if t == "doi" and not doi:
                doi = v
            elif t in ("pmc", "pmcid") and not pmcid:
                pmcid = v.replace("PMC", "").strip()
    except Exception:
        pass
    return doi, pmcid


def europepmc(pmid, timeout):
    """Europe PMC core record -> (pdf_url, license, doi, pmcid, title) if OA."""
    q = urllib.parse.urlencode(
        {"query": f"EXT_ID:{pmid} AND SRC:MED", "resultType": "core",
         "format": "json", "pageSize": "1"}
    )
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + q
    try:
        data = _get_json(url, timeout)
        res = data.get("resultList", {}).get("result", [])
        if not res:
            return None
        r = res[0]
        if str(r.get("isOpenAccess", "")).upper() != "Y":
            return None
        lic = r.get("license")
        doi = r.get("doi")
        pmcid = (r.get("pmcid") or "").replace("PMC", "").strip() or None
        title = r.get("title")
        for u in r.get("fullTextUrlList", {}).get("fullTextUrl", []):
            if (u.get("documentStyle") == "pdf"
                    and str(u.get("availabilityCode", "")).upper() == "OA"
                    and u.get("url")):
                return (u["url"], lic, doi, pmcid, title)
        if pmcid:
            return (f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/pdf/",
                    lic, doi, pmcid, title)
    except Exception:
        return None
    return None


def unpaywall(doi, email, timeout):
    if not doi or not email:
        return None
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={urllib.parse.quote(email)}"
    try:
        data = _get_json(url, timeout)
        if not data.get("is_oa"):
            return None
        loc = data.get("best_oa_location") or {}
        pdf = loc.get("url_for_pdf") or loc.get("url")
        if not pdf:
            return None
        return (pdf, loc.get("license"), data.get("doi"), data.get("title"))
    except Exception:
        return None


def emit(obj, code):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(description="Resolve a paper to a legal OA PDF URL.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pmid")
    g.add_argument("--doi")
    g.add_argument("--title")
    ap.add_argument("--email", default=os.environ.get("MPF_CONTACT_EMAIL"))
    ap.add_argument("--api-key", default=os.environ.get("NCBI_API_KEY"))
    ap.add_argument("--timeout", type=int, default=20)
    a = ap.parse_args()

    pmid, doi, title = a.pmid, a.doi, a.title

    if title and not pmid and not doi:
        pmid = title_to_pmid(title, a.email, a.api_key, a.timeout)
        if not pmid:
            doi = title_to_doi(title, a.timeout)

    if pmid and not doi:
        doi, pmcid = pmid_ids(pmid, a.email, a.api_key, a.timeout)
    else:
        pmcid = None

    # 1) Europe PMC (definitive OA flag + license), PMID-keyed.
    if pmid:
        ep = europepmc(pmid, a.timeout)
        if ep:
            pdf, lic, d, pc, t = ep
            emit({"resolved": True, "pdf_url": pdf, "source": "EuropePMC",
                  "license": lic, "doi": d or doi, "pmid": pmid,
                  "title": t or title}, 0)

    # 2) NCBI PMC OA direct PDF when a PMC id exists.
    if pmcid:
        emit({"resolved": True,
              "pdf_url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/pdf/",
              "source": "PMC", "license": None, "doi": doi, "pmid": pmid,
              "title": title}, 0)

    # 3) Unpaywall (legal OA: gold/green/author manuscript/repository) by DOI.
    up = unpaywall(doi, a.email, a.timeout)
    if up:
        pdf, lic, d, t = up
        emit({"resolved": True, "pdf_url": pdf,
              "source": f"Unpaywall:{urllib.parse.urlparse(pdf).netloc}",
              "license": lic, "doi": d or doi, "pmid": pmid,
              "title": t or title}, 0)

    reason = "no legal open-access copy found"
    if not a.email:
        reason += " (no contact email: Unpaywall skipped — set --email/MPF_CONTACT_EMAIL)"
    emit({"resolved": False, "reason": reason,
          "doi": doi, "pmid": pmid, "title": title}, 1)


if __name__ == "__main__":
    main()
