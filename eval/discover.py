# /// script
# requires-python = ">=3.10"
# ///
"""Generate the pinned URL lists in eval/manifests/<dataset>.urls.tsv.

Discovery is run ONCE and its output committed; fetch.py never re-discovers.
Each subcommand documents how a dataset's list was derived, so a third party
can audit or regenerate it. Regenerating MAY produce a different list (new
arXiv submissions, PMC additions); the committed list is the pinned one.

Usage:
    uv run eval/discover.py arxiv|pmc|bills|olmocr|datasheets|all

Sources (all probed live 2026-08-03):
  arxiv       export.arxiv.org Atom API, 20 newest per category, version-pinned
  pmc         ftp.ncbi.nlm.nih.gov/pub/pmc/deprecated/oa_pdf/ dir listings
  bills       govinfo.gov public bulkdata JSON, 118th Congress House bills (ih)
  olmocr      HuggingFace tree API for allenai/olmOCR-bench (sha256 from LFS)
  datasheets  curated part list; only vendors that allow automated fetch

  datasheet_holdout  (2026-08-13) eleven vendors, deliberately NOT TI-dominated
"""
import gzip, json, pathlib, random, re, sys, time, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
MANI = HERE / "manifests"
UA = {"User-Agent": "doc-extract-bench/1.0 (mailto:lenards@optonics.eu)"}


def get(url, timeout=60, accept=None):
    req = urllib.request.Request(url, headers=UA | (accept or {}))
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def write_tsv(name, rows):
    """rows: [(filename, url)] or [(filename, url, sha256)]"""
    MANI.mkdir(exist_ok=True)
    p = MANI / f"{name}.urls.tsv"
    p.write_text("".join("\t".join(r) + "\n" for r in rows))
    print(f"{p.name}: {len(rows)} entries")


# --------------------------------------------------------------------- arxiv
ARXIV_CATS = ["cs.LG", "cs.CL", "cs.CV", "cs.RO", "math.AP", "math.PR",
              "astro-ph.GA", "quant-ph", "q-bio.PE", "eess.SP"]

def arxiv():
    """25 most recent submissions in each of 10 categories at discovery time,
    pinned to the exact version (vN) returned by the API. Cross-listed papers
    are de-duplicated, so the final list is a little under 250."""
    rows = []
    for cat in ARXIV_CATS:
        xml = get("https://export.arxiv.org/api/query?search_query=cat:"
                  f"{cat}&start=0&max_results=25&sortBy=submittedDate"
                  "&sortOrder=descending")
        ids = re.findall(r"<id>https?://arxiv\.org/abs/([^<]+)</id>", xml)
        for aid in ids:
            fn = aid.replace("/", "_") + ".pdf"
            rows.append((fn, f"https://export.arxiv.org/pdf/{aid}"))
        print(f"  {cat}: {len(ids)}")
        time.sleep(3)  # arXiv API politeness
    # de-dup (cross-listed papers appear in several categories)
    seen, out = set(), []
    for r in rows:
        if r[0] not in seen:
            seen.add(r[0]); out.append(r)
    write_tsv("arxiv", out)


# ----------------------------------------------------------------------- pmc
PMC_BASE = "https://ftp.ncbi.nlm.nih.gov/pub/pmc/deprecated/oa_pdf"

def pmc(target=220):
    """Walk oa_pdf leaf directories 00/00, 00/01, ... in order, taking every
    PDF listed, until `target` files are pinned. Deterministic given a fixed
    snapshot of the FTP tree."""
    rows = []
    for hi in range(256):
        for lo in range(256):
            d = f"{hi:02x}/{lo:02x}"
            try:
                html = get(f"{PMC_BASE}/{d}/")
            except Exception as e:
                print(f"  skip {d}: {e}"); continue
            for fn in re.findall(r'href="([^"/]+\.pdf)"', html):
                rows.append((fn, f"{PMC_BASE}/{d}/{fn}"))
            print(f"  {d}: total {len(rows)}")
            if len(rows) >= target:
                write_tsv("pmc", rows[:target]); return
    write_tsv("pmc", rows)


def pmc_holdout(target=250):
    """A journal corpus DISJOINT from `pmc`, for validating a routing rule
    out-of-sample.

    `pmc` above walks the oa_pdf tree from 00/00 and stops at 220 files, which
    means it never leaves the 00/xx prefix. This walks the 01/xx prefix
    instead and additionally excludes, by filename, everything the `pmc` list
    already pins - so the two sets cannot overlap even if the FTP tree is
    re-shuffled between runs. Filenames embed the PMC id, so filename
    disjointness is identity disjointness; fetch.py's sha256 pinning makes it
    checkable afterwards too.

    Needed because the `curves` and `whole_document` false positives measured
    in eval/nofigure.md are half journal boilerplate, and corpus/arxiv_holdout
    contains none of that - the same mismatch that made arxiv_holdout the
    wrong holdout for the signature-ubiquity rule (eval/rejected-signals.md).
    """
    have = {l.split("\t")[0] for l in
            (MANI / "pmc.urls.tsv").read_text().splitlines() if l.strip()}
    rows = []
    for lo in range(256):
        d = f"01/{lo:02x}"
        try:
            html = get(f"{PMC_BASE}/{d}/")
        except Exception as e:
            print(f"  skip {d}: {e}"); continue
        for fn in re.findall(r'href="([^"/]+\.pdf)"', html):
            if fn not in have:
                rows.append((fn, f"{PMC_BASE}/{d}/{fn}"))
        print(f"  {d}: total {len(rows)}")
        if len(rows) >= target:
            write_tsv("pmc_holdout", rows[:target]); return
    write_tsv("pmc_holdout", rows)


# --------------------------------------------------------------------- bills
def bills(target=230):
    """House bills of the 118th Congress, 1st session, 'ih' (introduced)
    version, enumerated from the public bulkdata JSON listing and taken in
    ascending bill-number order."""
    data = json.loads(get("https://www.govinfo.gov/bulkdata/json/BILLS/118/1/hr",
                          accept={"Accept": "application/json"}))
    names = sorted(
        (f["justFileName"] for f in data["files"]
         if f["justFileName"].endswith("ih.xml")),
        key=lambda n: int(re.search(r"hr(\d+)ih", n).group(1)))
    rows = []
    for n in names[:target]:
        pkg = n[:-4]                       # BILLS-118hr21ih
        rows.append((pkg + ".pdf",
                     f"https://www.govinfo.gov/content/pkg/{pkg}/pdf/{pkg}.pdf"))
    write_tsv("bills", rows)


# -------------------------------------------------------------------- olmocr
OLMO_SETS = {                     # dataset name -> HF categories merged into it
    "olmocr_multi_column":   ["multi_column"],
    "olmocr_headers_footers": ["headers_footers"],
    "olmocr_arxiv_math":     ["arxiv_math"],
    "olmocr_tables":         ["tables"],
    "olmocr_long_tiny_text": ["long_tiny_text"],
    "olmocr_scans":          ["old_scans", "old_scans_math"],
}

def olmocr():
    """All PDFs of the chosen olmOCR-bench categories (ODC-BY 1.0). sha256 is
    pinned up-front from HuggingFace LFS metadata, before any download."""
    for name, cats in OLMO_SETS.items():
        rows = []
        for cat in cats:
            tree = json.loads(get(
                "https://huggingface.co/api/datasets/allenai/olmOCR-bench/"
                f"tree/main/bench_data/pdfs/{cat}?limit=1000"))
            for f in tree:
                if not f["path"].endswith(".pdf"):
                    continue
                fn = pathlib.Path(f["path"]).name
                url = ("https://huggingface.co/datasets/allenai/olmOCR-bench/"
                       f"resolve/main/{f['path']}")
                rows.append((f"{cat}__{fn}", url, f["lfs"]["oid"]))
        write_tsv(name, rows)


# ---------------------------------------------------------------- datasheets
TI = """tl071 tl072 tl074 tl081 tl082 tl084 tlv9061 tlv9062 tlv2372 tlv271
opa333 opa2333 opa192 opa196 opa350 opa365 opa340 opa2340 opa134 opa2134
opa1612 opa1678 lm324 lm358 lm741 lm833 ne5532 lm393 lm339 lm311 lmv321
lmv324 lmv358 lm2903 lm2901 tlv1701 ne555 ne556 tlc555 lmc555 sn74hc00
sn74hc02 sn74hc04 sn74hc08 sn74hc14 sn74hc32 sn74hc74 sn74hc86 sn74hc123
sn74hc125 sn74hc126 sn74hc132 sn74hc138 sn74hc139 sn74hc151 sn74hc153
sn74hc157 sn74hc161 sn74hc164 sn74hc165 sn74hc174 sn74hc175 sn74hc240
sn74hc244 sn74hc245 sn74hc273 sn74hc373 sn74hc374 sn74hc540 sn74hc541
sn74hc573 sn74hc574 sn74hc595 sn74hc4040 sn74hc4051 sn74hc4052 sn74hc4053
sn74hc4060 sn74hc4066 sn74lvc1g04 sn74lvc1g07 sn74lvc1g08 sn74lvc1g14
sn74lvc1g17 sn74lvc1g125 sn74lvc1g126 sn74ahct125 sn74hct245 lm317 lm337
lm1117 tlv1117 lm2596 lm2576 tps54331 tps5430 tps54560 tps61023 tps62840
tps7a02 tps7a47 tlv757p lp2985 lp5907 tl431 lm4040 ref5025 ads1115 ads1015
ads1256 ads7830 dac8562 adc128s102 tmp117 tmp102 lm35 hdc1080 hdc2080
opt3001 lmt84 ina219 ina226 ina3221 ina180 sn65hvd230 iso1050 max232
max3232 sn75176b sn6501 drv8833 drv8825 drv8871 ucc27517 ucc27524 bq24074
bq25895 bq21040 tps2553 tps22918 lm5069 tca9548a pca9306 cd4017b cd4051b
cd4060b cd4093b cd40106b tlc5940 lm386 tpa3116d2 msp430g2553 tlv9002
opa2277 opa277 lf356 tl066a lm301a lm308? lm4562 sn74ls00 sn74ls138""".split()

DIODES = """AP2114 AP2112 DMN2075U DMG2305UX PAM8403 MMBT3904 MMBT3906
MMBT2222A BSS138 2N7002 BAV99 BAT54 S1M SS34 1N5819HW AZ1117C BC846A
BSS84 DMP2035U ZXCT1009""".split()

NEXPERIA = """BC817_SER PMEG3020EP PBSS4350X 74LVC1G14 PESD5V0X1BL
74HC_HCT595 1N4148_1N4448 BC847_SER BC857_SER PMBT3904 PMBT3906 PMBT2222A
BAT54_SER BAV99_SER 2N7002 BSS138 PESD5V0S1BA 74HC_HCT00 74HC_HCT04
74HC_HCT08 74HC_HCT14 74HC_HCT32 74HC_HCT74 74HC_HCT125 74HC_HCT138
74HC_HCT164 74HC_HCT245 74LVC1G04 74LVC1G08 74LVC1G17 74LVC1G125""".split()

EXTRA = [
    ("irlz44n_infineon.pdf", "https://www.infineon.com/dgdl/Infineon-IRLZ44N-DataSheet-v01_01-EN.pdf?fileId=5546d462533600a4015355d5f0a91480"),
    ("bme280_bosch.pdf", "https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf"),
    ("bmp280_bosch.pdf", "https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf"),
    ("bme680_bosch.pdf", "https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme680-ds001.pdf"),
    ("bmi160_bosch.pdf", "https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi160-ds000.pdf"),
    ("4n25_vishay.pdf", "https://www.vishay.com/docs/83725/4n25.pdf"),
    ("1n4001_vishay.pdf", "https://www.vishay.com/docs/88503/1n4001.pdf"),
    ("led_wurth.pdf", "https://www.we-online.com/components/products/datasheet/150080BS75000.pdf"),
    ("wurth_7447709100.pdf", "https://www.we-online.com/components/products/datasheet/7447709100.pdf"),
]

def datasheets():
    """Curated candidate list. Vendors that block automation (ST, Microchip,
    onsemi — verified 403) are absent. 404s cost nothing: fetch.py validates
    the %PDF magic and drops non-PDFs, and the manifest records only what
    actually landed."""
    rows = [(f"ti_{p}.pdf", f"https://www.ti.com/lit/ds/symlink/{p}.pdf")
            for p in TI if "?" not in p]
    rows += [(f"diodes_{p.lower()}.pdf",
              f"https://www.diodes.com/assets/Datasheets/{p}.pdf") for p in DIODES]
    rows += [(f"nexperia_{p}.pdf",
              f"https://assets.nexperia.com/documents/data-sheet/{p}.pdf")
             for p in NEXPERIA]
    rows += EXTRA
    write_tsv("datasheets", rows)


# ------------------------------------------------------ datasheet_holdout
# Vendors verified 2026-08-13 to serve their PDFs to this script's plain
# User-Agent, with robots.txt read first and obeyed. Nothing here spoofs a
# browser or works around a refusal; a host that says no is simply absent.
#
#   refused, and therefore ABSENT (status with the bench UA):
#     onsemi 403 · Rohm 403 · Toshiba 403 · Bourns 403 · Littelfuse 403 ·
#     TDK 403 · TE 403 · ST, Microchip, TME, LCSC (already recorded in
#     eval/tds-corpus.md)
#   robots.txt says no, so ABSENT even though the file is served:
#     ww1.microchip.com  ("User-agent: * / Disallow: /", serves 200 anyway)
#     www.winbond.com    ("Disallow: /resource-files", where the PDFs live)
#   no response at all from this network (not a refusal, just unreachable):
#     www.analog.com (robots.txt and every datasheet time out)
V_SEED = 20260813          # sampling seed for the three enumerable vendors

TI_HOLD = """ads1220 ads131m04 ina228 ina238 opa189 opa2188 tps63020 tps61093
tps54360 lm5164 ucc21520 drv8323 lmr33630 tps7a4700 ref3025 dac80501 tmp235
lmt01 hdc3020 opt4001 sn74lvc2g14 sn74axc8t245 tca9534 cd4066b cd4013b
ina181 lm5117 tps25200 sn74lv1t34""".split()
# tlv9004 was pinned and then removed: TI serves ONE document for the tlv9002
# and tlv9004 part numbers, so the file came back byte-identical to
# corpus/datasheets/ti_tlv9002.pdf. Filename disjointness did not catch it;
# the sha256 check did. Any future addition to this list needs the same check.

NXP_HOLD = """PMEG2010AEH BUK9K6R2-40E BAS316 PMEG3010ER PMEG6010CEH
PDTC114ET PDTA114ET PBSS5350X PMV30UN PMV45EN BUK7Y12-40E BUK9Y40-100E
PSMN022-30PL PSMN4R0-30YL 74LVC2G14 74LVC1G32 74LVC1G86 74HC_HCT02
74HC_HCT86 74HC_HCT373 74HC_HCT574 1PS76SB40 PESD3V3L1BA NX3008NBKV
BAS40_SER""".split()

MELEXIS = """mlx90614 mlx90393 mlx90632 mlx90640 mlx90641 mlx90372 mlx91220
mlx91221 mlx90395 mlx90397 mlx90333 mlx90316 mlx90363 mlx90365 mlx90371
mlx90373 mlx90421 mlx90422 mlx92232 mlx92242 mlx75026 mlx75027 mlx81325
mlx90109""".split()

SILABS = """cp2102-9 cp2104 cp2105 cp2108 cp2110 cp2112 cp2114 cp2130
efr32bg22-datasheet efr32mg21-datasheet efr32fg23-datasheet
efm32pg22-datasheet efm32gg11-datasheet efm8bb1-datasheet efm8bb3-datasheet
efm8ub1-datasheet efr32mg24-datasheet efr32bg24-datasheet si4468 si4438
si8621 si8641 si5341-40-d-datasheet si1145-46-47""".split()

ESPRESSIF = """esp32_datasheet_en esp32-s3_datasheet_en esp32-c6_datasheet_en
esp32-c3_datasheet_en esp32-s2_datasheet_en esp32-h2_datasheet_en
esp32-c2_datasheet_en esp8684_datasheet_en esp32-wroom-32_datasheet_en
esp32-wroom-32e_esp32-wroom-32ue_datasheet_en
esp32-s3-wroom-1_wroom-1u_datasheet_en esp32-c3-mini-1_datasheet_en
esp32-c6-wroom-1_wroom-1u_datasheet_en esp32-h2-mini-1_mini-1u_datasheet_en
esp32-pico-d4_datasheet_en esp32-wrover-e_esp32-wrover-ie_datasheet_en""".split()

RPI = """rp2040/rp2040-datasheet.pdf rp2350/rp2350-datasheet.pdf
pico/pico-datasheet.pdf picow/pico-w-datasheet.pdf pico/pico-2-datasheet.pdf
rp2040/hardware-design-with-rp2040.pdf rp2350/hardware-design-with-rp2350.pdf
cm4/cm4-datasheet.pdf cm5/cm5-datasheet.pdf rpi4/raspberry-pi-4-datasheet.pdf
picow/pico-2-w-datasheet.pdf camera/camera-module-3-product-brief.pdf
cm4io/cm4io-datasheet.pdf rpi5/raspberry-pi-5-product-brief.pdf""".split()

WURTH = """7447779002 7447709220 860010672004 150141M173100 744314650
885012207072 744231091 61300311121 691214110002 7427927 750313638
74404054100 7447708100 860020672008 885012206095 744373240022""".split()

OMRON = "en-g6k en-g5le en-g5q en-g2rl en-g5nb en-g3vm en-b3f en-g6s".split()


def datasheet_holdout(target_big=(55, 55, 50)):
    """A component-datasheet corpus DISJOINT from `datasheets`, for validating
    a routing rule that targets VENDOR boilerplate out-of-sample.

    `corpus/datasheets` is 153 TI + 27 Nexperia + 16 Diodes + 9 assorted, i.e.
    75% one vendor, and the rule under test (`eval/nofigure.md`: small stroke
    cluster + no figure caption) was designed on the TI header logo. A holdout
    that is also TI-dominated would prove almost nothing, so the three vendors
    that can be ENUMERATED rather than guessed - Vishay, Renesas and Alpha &
    Omega - carry the bulk, TI is held to about a tenth, and eight further
    vendors fill in. Every filename is `<vendor>_<part>.pdf`, so the vendor mix
    and the disjointness from `datasheets` are both checkable from the manifest
    alone.

    Three enumerable sources, all from the vendor's own sitemap:
      vishay   sitemap1.xml.gz -> /en/product/<id>/ ids; https://www.vishay.com
               /doc?<id> 302s to the datasheet PDF. The redirect is resolved
               HERE, once, so the manifest pins the real /docs/<id>/<part>.pdf
               URL and the filename carries the part number.
      renesas  sitemap.xml pages, walked in order until 3,000 /en/document/dst/
               (datasheet) URLs are seen, then sampled.
      aos      sitemap.xml -> /products/<family>/<part> pages; the datasheet is
               /res/data_sheets/<PART>.pdf.
    Sampling is `random.Random(V_SEED).sample` over the sorted candidate list,
    so re-running reproduces the same draw against the same site snapshot.

    The rest are curated part lists in the style of `datasheets()` above; 404s
    cost nothing because fetch.py validates the %PDF magic and drops anything
    else, and the manifest records only what was pinned.
    """
    nv, nr, na = target_big
    rows = []

    # -- vishay ---------------------------------------------------------------
    raw = urllib.request.urlopen(
        urllib.request.Request("https://www.vishay.com/sitemap1.xml.gz",
                               headers=UA), timeout=120).read()
    ids = sorted({m for m in re.findall(
        r"/en/product/(\d+)/", gzip.decompress(raw).decode("utf-8", "replace"))})
    print(f"  vishay: {len(ids)} product ids in sitemap")
    got = 0
    for pid in random.Random(V_SEED).sample(ids, min(len(ids), nv * 2)):
        if got >= nv:
            break
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(f"https://www.vishay.com/doc?{pid}",
                                           headers=UA), timeout=45) as r:
                url, head = r.geturl(), r.read(4)
        except Exception as e:
            print(f"    vishay {pid}: {type(e).__name__}"); time.sleep(0.4); continue
        time.sleep(0.4)
        part = url.rsplit("/", 1)[-1]
        if head != b"%PDF" or not part.lower().endswith(".pdf"):
            continue
        rows.append((f"vishay_{part}", url)); got += 1
    print(f"  vishay: {got} datasheets")

    # -- renesas --------------------------------------------------------------
    idx = get("https://www.renesas.com/sitemap.xml", timeout=90)
    pages = re.findall(r"<loc>(https://www\.renesas\.com/sitemap\.xml\?page=\d+)</loc>", idx)
    dst = []
    for p in pages:
        try:
            dst += [l for l in re.findall(r"<loc>([^<]+)</loc>", get(p, timeout=90))
                    if "/en/document/dst/" in l]
        except Exception as e:
            print(f"    renesas {p}: {type(e).__name__}")
        time.sleep(1.0)                       # sitemap pages are 2,000 URLs each
        if len(dst) >= 3000:
            break
    print(f"  renesas: {len(dst)} datasheet documents seen")
    for u in random.Random(V_SEED).sample(sorted(set(dst)), min(len(set(dst)), nr)):
        rows.append((f"renesas_{u.rsplit('/', 1)[-1]}.pdf", u))

    # -- alpha & omega --------------------------------------------------------
    aos = []
    for p in re.findall(r"<loc>([^<]+)</loc>", get("https://www.aosmd.com/sitemap.xml")):
        aos += [l.rsplit("/", 1)[-1] for l in
                re.findall(r"<loc>([^<]+)</loc>", get(p, timeout=90))
                if "/products/" in l and "/zh/" not in l]
        time.sleep(1.0)
    aos = sorted({a for a in aos if re.fullmatch(r"ao[a-z0-9-]+", a)})
    print(f"  aos: {len(aos)} product pages")
    for part in random.Random(V_SEED).sample(aos, min(len(aos), na)):
        rows.append((f"aos_{part.upper()}.pdf",
                     f"https://www.aosmd.com/res/data_sheets/{part.upper()}.pdf"))

    # -- curated lists --------------------------------------------------------
    rows += [(f"ti_{p}.pdf", f"https://www.ti.com/lit/ds/symlink/{p}.pdf")
             for p in TI_HOLD]
    rows += [(f"nexperia_{p}.pdf",
              f"https://assets.nexperia.com/documents/data-sheet/{p}.pdf")
             for p in NXP_HOLD]
    rows += [(f"melexis_{p}.pdf", "https://www.melexis.com/-/media/files/"
              f"documents/datasheets/{p}-datasheet-melexis.pdf") for p in MELEXIS]
    rows += [(f"silabs_{p}.pdf",
              f"https://www.silabs.com/documents/public/data-sheets/{p}.pdf")
             for p in SILABS]
    rows += [(f"espressif_{p}.pdf", "https://www.espressif.com/sites/default/"
              f"files/documentation/{p}.pdf") for p in ESPRESSIF]
    rows += [(f"rpi_{p.split('/')[-1]}", f"https://datasheets.raspberrypi.com/{p}")
             for p in RPI]
    rows += [(f"wurth_{p}.pdf",
              f"https://www.we-online.com/components/products/datasheet/{p}.pdf")
             for p in WURTH]
    rows += [(f"omron_{p}.pdf",
              f"https://omronfs.omron.com/en_US/ecb/products/pdf/{p}.pdf")
             for p in OMRON]

    # A holdout must not re-pin a document the design corpus already holds.
    have = {l.split("\t")[0] for l in
            (MANI / "datasheets.urls.tsv").read_text().splitlines() if l.strip()}
    urls = {l.split("\t")[1] for l in
            (MANI / "datasheets.urls.tsv").read_text().splitlines() if l.strip()}
    rows = [r for r in rows if r[0] not in have and r[1] not in urls]
    write_tsv("datasheet_holdout", rows)


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    fns = {"arxiv": arxiv, "pmc": pmc, "pmc_holdout": pmc_holdout,
           "bills": bills, "olmocr": olmocr, "datasheets": datasheets,
           "datasheet_holdout": datasheet_holdout}
    # "all" regenerates the pinned design corpora only; a holdout is fetched
    # deliberately, once, when a rule needs validating.
    holdouts = {"pmc_holdout", "datasheet_holdout"}
    for w in ([k for k in fns if k not in holdouts] if "all" in which else which):
        print(f"== {w}")
        fns[w]()
