"""The registered fallback linguistic-distance scale, built from open inputs.

The campaign's mandatory country-level control (v1.1 §3.5) has two registered
implementations: the published measure (S-44) and a **pre-registered fallback**,
an "ordinal distance-from-English scale built from the official-language status
published by the UN/ISO 639, with English-official jurisdictions at 0". Decision
**D-023** selected the fallback, because the published measure cannot be
reproduced exactly panel-wide: its jurisdiction-level official-language lists come
from **Ethnologue**, a licensed and versioned database whose vintage the paper does
not archive, and the paper's Ethnologue-to-WALS merge was done by hand.

This module implements the fallback from **open, dated, hashed inputs**:

* **WALS 2020.6** (Dryer & Haspelmath; Zenodo record 23010827) — the 192 linguistic
  characteristics, per language;
* **Unicode CLDR 49** (territory information) — each territory's **official**
  languages, as ISO 639-3 codes;
* **S-44 Table 1** (Guan, Shafron, Ye and Zhuang 2025, *Review of Accounting
  Studies* 30(3): 2963–3020, open access) — the published values used only as an
  **external validation** of the fallback's ordering, never as this campaign's own
  measure.

**The rule, stated once.**

1. The English reference is the WALS language record ``eng``.
2. A WALS **parameter** is *compared* between two languages when both carry at
   least one value for it. A compared parameter is **shared** when the two
   languages' value sets intersect, and **not shared** otherwise.
3. A language's **friction score** is the share of its compared parameters that
   are not shared with English.
4. Where several WALS records carry the same ISO 639-3 code, the ISO-level score
   is the **median** of their friction scores, over the records that reach
   ``MIN_COMMON_FEATURES`` compared parameters.
5. A jurisdiction's score is the **simple mean** of the scores of its official
   languages, which is the aggregation rule the published measure uses. A
   jurisdiction whose official-language set is exactly {English} scores **0**.
6. An official language with no WALS record is **never dropped silently**: the
   jurisdiction is marked ``partial`` and the missing language count is recorded.
7. The ordinal category is read off the fixed boundaries in :data:`LD_BANDS`.

The boundaries are the published measure's own **quartiles** over its 84-country
sample (S-44 Table 2, Panel A: Q1 0.255, median 0.342, Q3 0.482), fixed here so
that the ordinal scale is comparable with the measure it stands in for. They are
calibrated to the *published distribution*, not to this campaign's panel, which is
not assembled yet, and not to any outcome.

The module performs no network access. Retrieval and hashing belong to
``scripts/data_manifest.py`` and to the acquisition script that drives it.
"""

from __future__ import annotations

import csv
import io
import statistics
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

PARSER_VERSION = "linguistic_distance@1.0.0"

ENGLISH_WALS_ID = "eng"
ENGLISH_ISO = "eng"

#: Minimum number of parameters a WALS record must share with English to enter
#: the ISO-level aggregation.
MIN_COMMON_FEATURES = 30

#: The ordinal categories of the registered fallback scale. The boundaries are the
#: published measure's quartiles over its 84-country sample (S-44, Table 2 Panel A).
LD_BANDS: tuple[tuple[str, float, float], ...] = (
    ("LD-0", 0.0, 0.0),
    ("LD-1", 0.0, 0.255),
    ("LD-2", 0.255, 0.342),
    ("LD-3", 0.342, 0.482),
    ("LD-4", 0.482, 1.0),
)

#: Official-language statuses treated as official for the jurisdiction's score.
OFFICIAL_STATUSES = ("official", "official_regional")

#: The strict status filter, used when the jurisdictions' official-language sets
#: must match the published measure's own lists.
OFFICIAL_STATUS_STRICT = ("official",)

#: ISO 639-1 to ISO 639-3. CLDR records most common languages with their
#: two-letter code; WALS records ISO 639-3.
ISO639_1_TO_3: dict[str, str] = {
    "aa": "aar", "ab": "abk", "ae": "ave", "af": "afr", "ak": "aka", "am": "amh",
    "an": "arg", "ar": "ara", "as": "asm", "av": "ava", "ay": "aym", "az": "aze",
    "ba": "bak", "be": "bel", "bg": "bul", "bh": "bih", "bi": "bis", "bm": "bam",
    "bn": "ben", "bo": "bod", "br": "bre", "bs": "bos", "ca": "cat", "ce": "che",
    "ch": "cha", "co": "cos", "cr": "cre", "cs": "ces", "cu": "chu", "cv": "chv",
    "cy": "cym", "da": "dan", "de": "deu", "dv": "div", "dz": "dzo", "ee": "ewe",
    "el": "ell", "en": "eng", "eo": "epo", "es": "spa", "et": "est", "eu": "eus",
    "fa": "fas", "ff": "ful", "fi": "fin", "fj": "fij", "fo": "fao", "fr": "fra",
    "fy": "fry", "ga": "gle", "gd": "gla", "gl": "glg", "gn": "grn", "gu": "guj",
    "gv": "glv", "ha": "hau", "he": "heb", "hi": "hin", "ho": "hmo", "hr": "hrv",
    "ht": "hat", "hu": "hun", "hy": "hye", "hz": "her", "ia": "ina", "id": "ind",
    "ie": "ile", "ig": "ibo", "ii": "iii", "ik": "ipk", "io": "ido", "is": "isl",
    "it": "ita", "iu": "iku", "ja": "jpn", "jv": "jav", "ka": "kat", "kg": "kon",
    "ki": "kik", "kj": "kua", "kk": "kaz", "kl": "kal", "km": "khm", "kn": "kan",
    "ko": "kor", "kr": "kau", "ks": "kas", "ku": "kur", "kv": "kom", "kw": "cor",
    "ky": "kir", "la": "lat", "lb": "ltz", "lg": "lug", "li": "lim", "ln": "lin",
    "lo": "lao", "lt": "lit", "lu": "lub", "lv": "lav", "mg": "mlg", "mh": "mah",
    "mi": "mri", "mk": "mkd", "ml": "mal", "mn": "mon", "mr": "mar", "ms": "msa",
    "mt": "mlt", "my": "mya", "na": "nau", "nb": "nob", "nd": "nde", "ne": "nep",
    "ng": "ndo", "nl": "nld", "nn": "nno", "no": "nor", "nr": "nbl", "nv": "nav",
    "ny": "nya", "oc": "oci", "oj": "oji", "om": "orm", "or": "ori", "os": "oss",
    "pa": "pan", "pi": "pli", "pl": "pol", "ps": "pus", "pt": "por", "qu": "que",
    "rm": "roh", "rn": "run", "ro": "ron", "ru": "rus", "rw": "kin", "sa": "san",
    "sc": "srd", "sd": "snd", "se": "sme", "sg": "sag", "si": "sin", "sk": "slk",
    "sl": "slv", "sm": "smo", "sn": "sna", "so": "som", "sq": "sqi", "sr": "srp",
    "ss": "ssw", "st": "sot", "su": "sun", "sv": "swe", "sw": "swa", "ta": "tam",
    "te": "tel", "tg": "tgk", "th": "tha", "ti": "tir", "tk": "tuk", "tl": "tgl",
    "tn": "tsn", "to": "ton", "tr": "tur", "ts": "tso", "tt": "tat", "tw": "twi",
    "ty": "tah", "ug": "uig", "uk": "ukr", "ur": "urd", "uz": "uzb", "ve": "ven",
    "vi": "vie", "vo": "vol", "wa": "wln", "wo": "wol", "xh": "xho", "yi": "yid",
    "yo": "yor", "za": "zha", "zh": "zho", "zu": "zul",
}


#: IFRS Foundation jurisdiction names that do not match a CLDR territory name.
JURISDICTION_ALIASES: dict[str, str] = {
    "Bosnia And Herzegovina": "BA",
    "Chinese Taipei": "TW",
    "Czechia": "CZ",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "Eswatini": "SZ",
    "European Union": "EU",
    "Guinea Bissau": "GW",
    "Hong Kong Sar": "HK",
    "Macedonia": "MK",
    "Moldova": "MD",
    "Myanmar": "MM",
    "Palestine": "PS",
    "Republic Of The Congo": "CG",
    "Democratic Republic Of Congo": "CD",
    "St Kitts And Nevis": "KN",
    "St Lucia": "LC",
    "St Vincent And The Grenadines": "VC",
    "Turkiye": "TR",
}

#: Declared equivalences between an official-language code and the WALS variety
#: that carries it, where ISO 639-3 does not express the relation. Filipino is
#: a standardised variety of Tagalog, and WALS describes the Tagalog record.
WALS_EQUIVALENT_CODES: dict[str, tuple[str, ...]] = {
    "fil": ("tgl",),
}

#: The official-language names published in S-44 Table 1, mapped to ISO 639-3.
PUBLISHED_LANGUAGE_CODES: dict[str, str] = {
    "English": "eng",
    "Spanish": "spa",
    "Arabic": "ara",
    "French": "fra",
    "Russian": "rus",
    "Chinese": "zho",
    "Croatian": "hrv",
    "Portuguese": "por",
    "Swahili": "swa",
    "Malay": "msa",
    "Tamil": "tam",
    "Bengali": "ben",
    "Bosnian": "bos",
    "Serbian": "srp",
    "Haitian Creole": "hat",
    "Hindi": "hin",
    "Indonesian": "ind",
    "Hebrew": "heb",
    "Japanese": "jpn",
    "Kazakh": "kaz",
    "Kyrgyz": "kir",
    "Lao": "lao",
    "Romanian": "ron",
    "Tamazight": "tzm",
    "Nepali": "nep",
    "Urdu": "urd",
    "Tok-Pisin": "tpi",
    "Paraguayan Guaraní": "grn",
    "Filipino": "fil",
    "Afrikaans": "afr",
    "Ndebele": "nde",
    "Northern Sotho": "nso",
    "Setswana": "tsn",
    "Southern Sotho": "sot",
    "Swati": "ssw",
    "Tsonga": "ts",
    "Venda": "ve",
    "Xhosa": "xho",
    "Zulu": "zul",
    "Korean": "kor",
    "Sinhala": "sin",
    "German": "deu",
    "Italian": "ita",
    "Thai": "tha",
    "Turkish": "tur",
}

#: Jurisdictions that are not a single territory and therefore have no
#: jurisdiction-level official-language set.
SUPRANATIONAL_JURISDICTIONS = ("European Union",)


@dataclass(frozen=True)
class LanguageScore:
    """One language's friction score against English."""

    iso639_3: str
    score: float
    compared_features: int
    wals_records: int


@dataclass(frozen=True)
class JurisdictionScore:
    """One jurisdiction's fallback distance from English."""

    jurisdiction: str
    territory: str
    official_languages: tuple[str, ...]
    score: float | None
    category: str
    missing_languages: tuple[str, ...]
    note: str


def _read_csv(archive: zipfile.ZipFile, suffix: str) -> list[dict[str, str]]:
    """Read one CSV member of a zip archive into dictionaries."""
    with archive.open(_member(archive, suffix)) as handle:
        text = io.TextIOWrapper(handle, encoding="utf-8")
        return list(csv.DictReader(text))


def _member(archive: zipfile.ZipFile, suffix: str) -> str:
    """Return the first member whose name ends with ``suffix``."""
    for name in archive.namelist():
        if name.endswith(suffix):
            return name
    raise KeyError(f"no member ending in {suffix!r} in the archive")


def load_wals_values(archive: zipfile.ZipFile) -> dict[str, dict[str, set[str]]]:
    """Load the WALS values as ``language id -> parameter -> {values}``."""
    values: dict[str, dict[str, set[str]]] = {}
    for row in _read_csv(archive, "cldf/values.csv"):
        values.setdefault(row["Language_ID"], {}).setdefault(row["Parameter_ID"], set()).add(row["Value"])
    return values


def load_wals_iso_codes(archive: zipfile.ZipFile) -> dict[str, list[str]]:
    """Map each ISO 639-3 code to the WALS language records that carry it.

    WALS records a language's ISO 639-3 code in ``ISO639P3code`` and, for the
    records whose code is a macrolanguage or a variety, an additional list in
    ``ISO_codes``. Both are used, so a record is reachable under every code it
    declares.
    """
    mapping: dict[str, list[str]] = {}
    for row in _read_csv(archive, "cldf/languages.csv"):
        codes: list[str] = []
        primary = (row.get("ISO639P3code") or "").strip()
        if primary:
            codes.append(primary)
        for token in (row.get("ISO_codes") or "").split():
            if token not in codes:
                codes.append(token)
        for code in codes:
            mapping.setdefault(code, []).append(row["ID"])
    return mapping


def language_friction(
    values: dict[str, dict[str, set[str]]],
    language_id: str,
    english_id: str = ENGLISH_WALS_ID,
) -> tuple[float | None, int]:
    """Friction of one WALS language against English.

    Returns ``(score, compared_features)``; the score is ``None`` when the record
    shares too few parameters with English to be informative.
    """
    english = values.get(english_id, {})
    own = values.get(language_id, {})
    compared = 0
    not_shared = 0
    for parameter, own_values in own.items():
        english_values = english.get(parameter)
        if not english_values:
            continue
        compared += 1
        if not (own_values & english_values):
            not_shared += 1
    if compared == 0:
        return None, 0
    return not_shared / compared, compared


def load_sil_macrolanguages(path: Path) -> dict[str, tuple[str, ...]]:
    """Macrolanguage code -> the individual language codes that belong to it."""
    members: dict[str, list[str]] = {}
    with Path(path).open("r", encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2 or not parts[0] or not parts[1]:
                continue
            members.setdefault(parts[0], []).append(parts[1])
    return {macro: tuple(sorted(set(individual))) for macro, individual in members.items()}


def load_sil_code_scopes(path: Path) -> dict[str, str]:
    """ISO 639-3 code -> its scope (``M`` macrolanguage, ``I`` individual)."""
    scopes: dict[str, str] = {}
    with Path(path).open("r", encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            scopes[parts[0]] = parts[4]
    return scopes


def language_candidates(
    iso: str,
    macrolanguages: dict[str, tuple[str, ...]],
    scopes: dict[str, str],
) -> tuple[str, ...]:
    """The ISO 639-3 codes that may carry a jurisdiction's official language.

    A jurisdiction's official-language code is usually a **macrolanguage**
    (``zho`` for Chinese, ``ara`` for Arabic, ``swa`` for Swahili), while WALS
    records individual varieties (``cmn``, ``arb``, ``swh``). The candidates are
    the code itself, the individuals of its macrolanguage, and the collective
    codes that contain it.
    """
    codes: list[str] = [iso]
    codes.extend(macrolanguages.get(iso, ()))
    codes.extend(WALS_EQUIVALENT_CODES.get(iso, ()))
    for macro, individuals in macrolanguages.items():
        if iso in individuals:
            codes.append(macro)
    return tuple(sorted(set(codes)))


def iso_language_scores(
    archive: zipfile.ZipFile,
    codes: Iterable[str] | None = None,
    min_common_features: int = MIN_COMMON_FEATURES,
    macrolanguages: dict[str, tuple[str, ...]] | None = None,
    scopes: dict[str, str] | None = None,
) -> dict[str, LanguageScore]:
    """Friction score per requested ISO 639-3 code, aggregated over WALS records.

    ``codes`` defaults to every code WALS itself carries. Each requested code is
    resolved through :func:`language_candidates`, so a macrolanguage such as
    ``ara`` is scored from the WALS records of the individual languages that
    belong to it.
    """
    values = load_wals_values(archive)
    wals_by_iso = load_wals_iso_codes(archive)
    macrolanguages = macrolanguages or {}
    scopes = scopes or {}
    requested = sorted(set(codes)) if codes is not None else sorted(wals_by_iso)
    scores: dict[str, LanguageScore] = {}
    for iso in requested:
        pool: list[str] = []
        for candidate in language_candidates(iso, macrolanguages, scopes):
            pool.extend(wals_by_iso.get(candidate, ()))
        scored: list[tuple[float, int]] = []
        for language_id in pool:
            score, compared = language_friction(values, language_id)
            if score is None or compared < min_common_features:
                continue
            scored.append((score, compared))
        if not scored:
            continue
        median = statistics.median(score for score, _ in scored)
        best = max(scored, key=lambda item: (item[1], item[0]))
        scores[iso] = LanguageScore(
            iso639_3=iso,
            score=float(median),
            compared_features=best[1],
            wals_records=len(scored),
        )
    return scores


def normalise_language_code(code: str) -> str | None:
    """Map a CLDR language tag to an ISO 639-3 code.

    Script subtags are dropped (``zh_Hant`` -> ``zho``), two-letter ISO 639-1
    codes are expanded, and a three-letter code is passed through.
    """
    tag = (code or "").strip().replace("-", "_")
    if not tag:
        return None
    base = tag.split("_")[0]
    if len(base) == 3:
        return base.lower()
    return ISO639_1_TO_3.get(base.lower())


def load_cldr_official_languages(
    path: Path,
    statuses: Sequence[str] = OFFICIAL_STATUSES,
) -> dict[str, tuple[str, ...]]:
    """Territory -> official languages, as ISO 639-3 codes, from CLDR JSON."""
    import json

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    territories = payload["supplemental"]["territoryInfo"]
    official: dict[str, tuple[str, ...]] = {}
    for territory, record in territories.items():
        languages: list[str] = []
        for tag, info in (record.get("languagePopulation") or {}).items():
            if (info.get("_officialStatus") or "") not in statuses:
                continue
            iso = normalise_language_code(tag)
            if iso and iso not in languages:
                languages.append(iso)
        if languages:
            official[territory] = tuple(sorted(languages))
    return official


def load_cldr_territory_names(archive: zipfile.ZipFile) -> dict[str, str]:
    """Territory code -> English territory name, from CLDR's English bundle."""
    import xml.etree.ElementTree as ET

    names: dict[str, str] = {}
    for member in archive.namelist():
        if not member.endswith("/main/en.xml") and not member.endswith("main/en.xml"):
            continue
        with archive.open(member) as handle:
            tree = ET.parse(handle)
        for territory in tree.iter("territory"):
            code = territory.get("type")
            if code and code not in names:
                names[code] = (territory.text or "").strip()
        if names:
            break
    return names


def _normalise(name: str) -> str:
    text = name.replace("-", " ").replace("(", " ").replace(")", " ")
    text = text.replace("&", " and ")
    return " ".join(text.split()).lower()


def resolve_territory(jurisdiction: str, territory_names: dict[str, str]) -> str | None:
    """Map an IFRS Foundation jurisdiction name to a CLDR territory code."""
    alias = JURISDICTION_ALIASES.get(jurisdiction)
    if alias:
        return alias
    target = _normalise(jurisdiction)
    for code, name in territory_names.items():
        if _normalise(name) == target:
            return code
    return None


def band(score: float, english_only: bool = False) -> str:
    """Ordinal category of a fallback score under the fixed band boundaries."""
    if english_only:
        return "LD-0"
    for name, low, high in LD_BANDS:
        if name == "LD-0":
            continue
        if low < score <= high:
            return name
    return LD_BANDS[-1][0]


def jurisdiction_score(
    jurisdiction: str,
    territory: str,
    official_languages: Sequence[str],
    scores: dict[str, LanguageScore],
) -> JurisdictionScore:
    """Score one jurisdiction from its official-language set."""
    if jurisdiction in SUPRANATIONAL_JURISDICTIONS:
        return JurisdictionScore(
            jurisdiction=jurisdiction,
            territory=territory,
            official_languages=(),
            score=None,
            category="LD-NA",
            missing_languages=(),
            note=(
                "Supranational bloc with no single official-language set. The linguistic-distance "
                "control is absorbed within the bloc and the jurisdiction carries no jurisdiction-level "
                "value; it is recorded as not applicable rather than assigned a number."
            ),
        )
    usable: list[float] = []
    missing: list[str] = []
    for language in official_languages:
        if language == ENGLISH_ISO:
            usable.append(0.0)
            continue
        record = scores.get(language)
        if record is None:
            missing.append(language)
            continue
        usable.append(record.score)
    english_only = tuple(official_languages) == (ENGLISH_ISO,)
    if not usable:
        return JurisdictionScore(
            jurisdiction=jurisdiction,
            territory=territory,
            official_languages=tuple(official_languages),
            score=None,
            category="LD-NA",
            missing_languages=tuple(missing),
            note="No official language could be scored against the WALS feature set.",
        )
    if missing:
        return JurisdictionScore(
            jurisdiction=jurisdiction,
            territory=territory,
            official_languages=tuple(official_languages),
            score=None,
            category="LD-NA",
            missing_languages=tuple(missing),
            note=(
                f"NOT SCORED: {len(missing)} of {len(official_languages)} official language(s) have "
                f"no WALS record with at least {MIN_COMMON_FEATURES} compared features, so the "
                "jurisdiction mean would not be comparable with the other jurisdictions. The "
                "jurisdiction is excluded from the stratification and the exclusion is recorded; "
                "no value is imputed."
            ),
        )
    score = sum(usable) / len(usable)
    return JurisdictionScore(
        jurisdiction=jurisdiction,
        territory=territory,
        official_languages=tuple(official_languages),
        score=score,
        category=band(score, english_only=english_only),
        missing_languages=(),
        note="Complete.",
    )


def score_jurisdictions(
    jurisdictions: Iterable[str],
    official_languages: dict[str, tuple[str, ...]],
    territory_names: dict[str, str],
    scores: dict[str, LanguageScore],
) -> list[JurisdictionScore]:
    """Score every jurisdiction, in the order given."""
    out: list[JurisdictionScore] = []
    for jurisdiction in jurisdictions:
        territory = resolve_territory(jurisdiction, territory_names)
        if territory is None:
            out.append(
                JurisdictionScore(
                    jurisdiction=jurisdiction,
                    territory="",
                    official_languages=(),
                    score=None,
                    category="LD-NA",
                    missing_languages=(),
                    note="No CLDR territory could be matched to this jurisdiction name.",
                )
            )
            continue
        out.append(
            jurisdiction_score(
                jurisdiction,
                territory,
                official_languages.get(territory, ()),
                scores,
            )
        )
    return out


def ranks(values: Sequence[float]) -> list[float]:
    """Average ranks, with ties sharing the mean of the ranks they span."""
    order = sorted(range(len(values)), key=lambda index: values[index])
    out = [0.0] * len(values)
    position = 0
    while position < len(order):
        end = position
        while end + 1 < len(order) and values[order[end + 1]] == values[order[position]]:
            end += 1
        average = (position + end) / 2 + 1
        for index in range(position, end + 1):
            out[order[index]] = average
        position = end + 1
    return out


def spearman(left: Sequence[float], right: Sequence[float]) -> float:
    """Spearman rank correlation, computed without third-party dependencies."""
    if len(left) != len(right) or len(left) < 2:
        raise ValueError("Spearman correlation needs two equal-length series of length >= 2")
    left_ranks = ranks(list(left))
    right_ranks = ranks(list(right))
    left_mean = sum(left_ranks) / len(left_ranks)
    right_mean = sum(right_ranks) / len(right_ranks)
    numerator = sum(
        (a - left_mean) * (b - right_mean) for a, b in zip(left_ranks, right_ranks)
    )
    left_ss = sum((a - left_mean) ** 2 for a in left_ranks)
    right_ss = sum((b - right_mean) ** 2 for b in right_ranks)
    if left_ss == 0 or right_ss == 0:
        raise ValueError("Spearman correlation is undefined for a constant series")
    return numerator / (left_ss * right_ss) ** 0.5


def pearson(left: Sequence[float], right: Sequence[float]) -> float:
    """Pearson correlation, computed without third-party dependencies."""
    if len(left) != len(right) or len(left) < 2:
        raise ValueError("Pearson correlation needs two equal-length series of length >= 2")
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right))
    left_ss = sum((a - left_mean) ** 2 for a in left)
    right_ss = sum((b - right_mean) ** 2 for b in right)
    if left_ss == 0 or right_ss == 0:
        raise ValueError("Pearson correlation is undefined for a constant series")
    return numerator / (left_ss * right_ss) ** 0.5


def published_official_languages(path: Path) -> dict[str, tuple[str, ...]]:
    """Published official-language sets, from the S-44 Table 1 fixture."""
    published: dict[str, tuple[str, ...]] = {}
    for row in read_published_table(path):
        names = [name.strip() for name in row["official_language"].split(",") if name.strip()]
        codes: list[str] = []
        for name in names:
            code = PUBLISHED_LANGUAGE_CODES.get(name)
            if code is None:
                continue
            if code not in codes:
                codes.append(code)
        if codes:
            published[row["country"].strip()] = tuple(codes)
    return published


def read_published_table(path: Path) -> list[dict[str, str]]:
    """Read the published S-44 Table 1 fixture used for the concordance check."""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def concordance(
    published: Sequence[dict[str, str]],
    fallback: dict[str, JurisdictionScore],
) -> dict[str, object]:
    """Rank concordance between the published measure and the fallback.

    ``published`` rows carry ``country`` and ``ld``; ``fallback`` maps a country
    name to its scored jurisdiction. Countries that cannot be matched, or whose
    official-language set cannot be reproduced, are **reported as unmatched**, not
    dropped silently.
    """
    matched: list[tuple[str, float, float]] = []
    unmatched: list[str] = []
    for row in published:
        country = row["country"].strip()
        record = fallback.get(country)
        if record is None or record.score is None:
            unmatched.append(country)
            continue
        matched.append((country, float(row["published_ld"]), record.score))
    if len(matched) < 2:
        raise ValueError("not enough matched countries for a concordance statistic")
    published_values = [item[1] for item in matched]
    fallback_values = [item[2] for item in matched]
    return {
        "matched_count": len(matched),
        "unmatched": unmatched,
        "spearman": spearman(published_values, fallback_values),
        "pearson": pearson(published_values, fallback_values),
        "max_absolute_difference": max(
            abs(published - fallback) for _, published, fallback in matched
        ),
        "matched": matched,
    }
