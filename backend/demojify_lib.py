# -*- coding: utf-8 -*-
"""
Emoji Remover Application (production-ready)

- STANDARD path (deterministic): emojis -> (meaning)
- LLM path (controlled): emojis -> plain neutral words (NO parentheses, NO emojis).
  If input has no emojis, LLM is skipped and the text is returned unchanged.
- Validator: LLM-based 0/1 decision; robust parsing; 1 => accept LLM; else fallback.

Usage example (pseudo):
    from your_provider import Client
    client = Client(api_key="...")
    res = demojify("so what's up man 😚", client, model="DeepSeek-V3.1")
    print(res.final_text, res.source, res.reason)
"""

# ------------ Config ------------
MODEL = "DeepSeek-V3.1"
# --------------------------------

import re
import json
from dataclasses import dataclass
from typing import Optional


# ========== Utility: unified way to call chat completions ==========
def _create_chat_completion(client, **kwargs):
    """
    Calls the REAL chat completions endpoint on your SDK.
    Tries `client.chat.completions.create` first, then `client.chat_completions.create`.
    """
    # Prefer OpenAI-style
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        return client.chat.completions.create(**kwargs)
    # Some SDKs expose this alias
    if hasattr(client, "chat_completions"):
        return client.chat_completions.create(**kwargs)
    raise RuntimeError("No supported chat completions method found on the client.")


# ========== Emoji detection ==========
def _has_emoji(text: str) -> bool:
    try:
        import emoji
        if hasattr(emoji, "emoji_list"):
            return bool(emoji.emoji_list(text))
        # fallback for older versions
        return emoji.demojize(text) != text
    except Exception:
        # last-ditch heuristic
        return any("\U0001F300" <= ch <= "\U0001FAFF" for ch in text)


# ========== STANDARD path: rule-based demojifier (parentheses) ==========
def emoji_semantic_clean(text: str, *, keep_case: bool = False) -> str:
    import unicodedata
    import emoji
    from collections import deque

    EMOJI_MAP = {
        "❤️": "love","♥️":"love","💙":"love","💜":"love","🖤":"love",
        "👍":"okay","👎":"no","😂":"laughing","🤣":"laughing hard","😅":"embarrassed",
        "😊":"smiling","😃":"smiling","😁":"smiling","🙂":"smiling","😢":"crying","😭":"crying",
        "😡":"angry","😠":"angry","😮":"surprised","😲":"surprised","😎":"cool","😍":"in love",
        "🤔":"thinking","🙄":"eyeroll","😒":"unamused","🔥":"awesome","✨":"sparkles","🎉":"congrats",
        "👏":"applause","🙏":"please","🤝":"handshake","👍🏻":"okay","🍕":"pizza","🍺":"beer",
        "🍿":"popcorn","🏆":"trophy","🚀":"taking off","💀":"dead (figuratively)","😤":"frustrated",
        "😴":"sleepy","😜":"playful","😉":"wink","🤷":"shrug","🤷‍♂️":"shrug","🤷‍♀️":"shrug",
        "🇺🇸":"USA","🇯🇵":"Japan","🇬🇧":"UK",
    }
    EMOJI_COMBOS = {"🍕🍺":"pizza and beer","😂😂":"hilarious","🔥🔥":"absolutely awesome","💀😂":"dead from laughter","🎉🎉":"congratulations"}
    ALIAS_FALLBACK = {
        "thumbs up":"okay","thumbs down":"no","red heart":"love","smiling face with sunglasses":"cool","fire":"awesome",
        "united states":"USA","united kingdom":"UK","japan":"Japan","woman technologist":"technologist","man technologist":"technologist","technologist":"technologist",
    }

    _SKIN_TONE_RE = re.compile(r"(?: light| medium| medium-light| medium-dark| dark)? skin tone", re.I)
    _VS_ZW_RE     = re.compile(r"[\uFE0F\u200D]")
    MULTISPACE_RE = re.compile(r"\s+")
    ELONG_RE      = re.compile(r"(.)\1{2,}")
    ONLY_EMOJI_OR_PUNCT_RE = re.compile(r"^[\W_]+$")
    WORD_STRIP_RE = re.compile(r"^[^\w]+|[^\w]+$")

    def _wrap(w: str) -> str: return f"({w})"
    def _strip_parens(t: str) -> str: return t[1:-1] if len(t)>=2 and t[0]=="(" and t[-1]==")" else t
    def _normalize(s: str) -> str: return _VS_ZW_RE.sub("", unicodedata.normalize("NFKC", s))
    def _apply_combos(s: str) -> str:
        for combo, phrase in EMOJI_COMBOS.items():
            if combo in s: s = s.replace(combo, " "+_wrap(phrase)+" ")
        return s
    def _alias_words(alias: str) -> str:
        name = alias.strip(":").replace("_"," ")
        name = _SKIN_TONE_RE.sub("", name).strip().lower()
        return ALIAS_FALLBACK.get(name, name)
    def _emoji_to_word(e: str) -> str:
        if e in EMOJI_MAP: return EMOJI_MAP[e]
        alias = emoji.demojize(e, language="en")
        words = _alias_words(alias)
        return ALIAS_FALLBACK.get(words, words)
    def _merge_punct(t: str) -> str:
        t = re.sub(r"[!?.]{3,}", "!!", t)
        t = re.sub(r"\s+([!?,.;:])", r"\1", t)
        t = re.sub(r"([!?,.;:]){2,}", r"\1\1", t)
        return t.strip()
    def _emoji_only_or_lowinfo(raw: str) -> bool:
        raw = raw.strip()
        return bool(ONLY_EMOJI_OR_PUNCT_RE.fullmatch(re.sub(r"\s+","",raw)))
    def _collapse_repeats(s: str):
        if not hasattr(emoji, "emoji_list"): return s, False
        items = emoji.emoji_list(s)
        if not items: return s, False
        out=[]; pos=0; i=0; n=len(items); had=False
        while i<n:
            st=items[i]["match_start"]; e=items[i]["emoji"]
            if pos<st: out.append(s[pos:st])
            j=i+1
            while j<n and items[j]["match_start"]==items[j-1]["match_end"] and items[j]["emoji"]==e: j+=1
            if j-i>=2: had=True
            out.append(e); pos=items[j-1]["match_end"]; i=j
        if pos<len(s): out.append(s[pos:])
        return "".join(out), had

    # pipeline
    s = _normalize(text)
    s, had_repeat = _collapse_repeats(s)

    import emoji as _emoji_lib
    def _replace(s: str) -> str:
        def cb(e, data=None): return " "+f"({_emoji_to_word(e)})"+" "
        s = _apply_combos(s)
        s = _emoji_lib.replace_emoji(s, replace=cb)
        return MULTISPACE_RE.sub(" ", s).strip()

    s = _replace(s)
    s = ELONG_RE.sub(r"\1\1", s)
    s = MULTISPACE_RE.sub(" ", s).strip()
    if not keep_case: s = s.lower()

    if _emoji_only_or_lowinfo(text):
        words = s.split()
        core = [_strip_parens(w) for w in words]
        if len(core)==1 and core[0] in {"awesome","sparkles","applause","congrats","hilarious","love","laughing","laughing hard"}:
            return f"({core[0]})"
        return ""

    # drop emoji tokens if neighbors already express the meaning
    _SYN = {
        "awesome":{"awesome","amazing","great","fantastic","lit","fire"},
        "love":{"love","loved","loving","adore","heart"},
        "laughing":{"lol","lmao","rofl","haha","hahaha","funny"},
        "laughing hard":{"lmao","rofl","hysterical"},
        "hilarious":{"hilarious","hysterical"},
        "crying":{"crying","tears","sad","sobbing"},
        "angry":{"angry","mad","furious"},
        "surprised":{"surprised","shocked","wow"},
        "cool":{"cool","chill"},
        "please":{"please","pls","plz"},
        "okay":{"ok","okay","k","kk","ack"},
        "congrats":{"congrats","congratulations","gg"},
        "applause":{"applause","clap","clapping"},
        "wink":{"wink","winking"},
        "thinking":{"thinking","think"},
        "in love":{"in","love"},
    }
    WORD_STRIP_RE = re.compile(r"^[^\w]+|[^\w]+$")
    def _norm(w: str) -> str: return WORD_STRIP_RE.sub("", w or "").lower()
    def _similar(a: str, meaning: str) -> bool:
        a=_norm(a); b=_norm(meaning)
        if not a or not b: return False
        if a==b or a in b or b in a: return True
        return a in _SYN.get(b, set())

    toks = s.split()
    def _drop(idx) -> bool:
        tok = toks[idx]
        if not (tok.startswith("(") and tok.endswith(")")): return False
        meaning = tok[1:-1]
        prev = toks[idx-1][1:-1] if idx-1>=0 and toks[idx-1].startswith("(") and toks[idx-1].endswith(")") else toks[idx-1] if idx-1>=0 else ""
        next_ = toks[idx+1][1:-1] if idx+1<len(toks) and toks[idx+1].startswith("(") and toks[idx+1].endswith(")") else toks[idx+1] if idx+1<len(toks) else ""
        if (prev and prev.isalpha() and _similar(prev, meaning)) or (next_ and next_.isalpha() and _similar(next_, meaning)):
            return True
        return False
    toks = [t for i,t in enumerate(toks) if not _drop(i)]

    # collapse duplicates
    out=[]
    def _base(x): return x[1:-1] if x.startswith("(") and x.endswith(")") else x
    for i,t in enumerate(toks):
        prev_same = (i>0 and _base(toks[i-1])==_base(t))
        next_same = (i<len(toks)-1 and _base(toks[i+1])==_base(t))
        if prev_same or next_same:
            if not prev_same: out.append(t)
        else:
            out.append(t)
    toks = out

    # mild intensifier handling
    from collections import deque
    buf, out = deque(), []
    def flush():
        if not buf: return
        last = buf[-1]; b=_base(last)
        if len(buf)>1 and b in {"laughing","laughing hard","hilarious","awesome","sparkles","applause","congrats","love"}:
            out.append(last); out.append("!!")
        else:
            out.append(last)
        buf.clear()
    for t in toks:
        if not buf or _base(buf[-1])==_base(t): buf.append(t)
        else: flush(); buf.append(t)
    flush(); toks=out

    # remove decorative sparkles if we already have words
    if any(_base(t).isalpha() and _base(t)!="sparkles" for t in toks):
        toks = [t for t in toks if _base(t)!="sparkles"]

    s = " ".join(toks)
    s = _merge_punct(s)
    if any(_base(t) in {"laughing","laughing hard","hilarious"} for t in toks) and "!" not in s:
        s += "!"
    if had_repeat and "!" not in s:
        s += "!"
    return s


# ========== Helper: replace leftover emojis with words (NO parentheses) ==========
def _to_words_no_parens(text: str) -> str:
    """
    If the LLM accidentally returns emojis, convert them to neutral words (no parentheses),
    preserving other text and spacing as much as possible.
    """
    try:
        import emoji
    except Exception:
        return text

    EMOJI_NAME_FALLBACKS = {
        "thumbs up":"okay","thumbs down":"no","red heart":"love","smiling face with sunglasses":"cool","fire":"awesome",
        "united states":"USA","united kingdom":"UK","japan":"Japan",
    }

    def alias_to_word(alias: str) -> str:
        name = alias.strip(":").replace("_"," ").lower()
        # strip skin tone words
        name = re.sub(r"(?: light| medium| medium-light| medium-dark| dark)? skin tone", "", name).strip()
        return EMOJI_NAME_FALLBACKS.get(name, name)

    def cb(e, data=None):
        # return just the neutral words, no parens
        alias = emoji.demojize(e, language="en")
        return " " + alias_to_word(alias) + " "

    out = emoji.replace_emoji(text, replace=cb)
    return re.sub(r"\s+", " ", out).strip()


# ========== LLM path: JSON-only, no emojis in output ==========
JSON_ONLY_SYSTEM = (
    "Convert emoji-filled text into clear, plain English for someone who doesn’t understand emojis. Interpret emojis by context and rephrase naturally so the same meaning is conveyed. Keep important details like names and facts, use a neutral tone, and skip decorative or repeated emojis."
    "Output MUST be a single-line JSON object with exactly one key: response. "
    "Never include code fences or any extra text."
)

def _llm_user_prompt_plain(text: str) -> str:
  return f"""
Rewrite the text so it means the same thing for someone who doesn’t understand emojis.
Interpret emojis by context and express the full message naturally in plain English.
- Don’t describe or name emojis.
- Keep the tone and intent, but make it sound natural.
- Skip redundant or decorative emojis.

Return strictly:
{{"response":"<plain-language version with no emojis>"}}

Example:
"LOL soooo funny 😂😂🔥🔥" → "That’s hilarious!"

Input:
{text}
""".strip()

def emoji_to_meaning(client, text, model=MODEL) -> str:
    """
    Calls the LLM to produce JSON: {"response": "<no-emoji text>"}.
    If there are no emojis, returns that JSON with the original text (LLM not called).
    Guards against validator contamination (single '0'/'1' output).
    Also post-sanitizes any accidental emojis the LLM might return.
    """
    # No-emoji short-circuit: skip the model entirely.
    if not _has_emoji(text):
        return json.dumps({"response": text})

    resp = _create_chat_completion(
        client,
        model=model,
        messages=[
            {"role": "system", "content": JSON_ONLY_SYSTEM},
            {"role": "user", "content": _llm_user_prompt_plain(text)},
        ],
        temperature=0.0, top_p=1.0,
        presence_penalty=0.0, frequency_penalty=0.0,
        # If your SDK supports JSON mode, uncomment:
        # response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content.strip()

    # Guard: if we somehow got a single '0'/'1' (wrong endpoint contamination), fallback to STANDARD-rendered words.
    if raw in {"0", "1"}:
        fallback_words = _to_words_no_parens(text)  # deterministic conversion without ()
        return json.dumps({"response": fallback_words})

    # Try to parse JSON; if it contains emojis, clean them.
    try:
        data = json.loads(raw)
        cand = str(data.get("response", ""))
    except Exception:
        # very defensive: if not JSON, just render ourselves
        cand = _to_words_no_parens(raw if raw else text)

    # Ensure no emojis remain
    if _has_emoji(cand):
        cand = _to_words_no_parens(cand)

    return json.dumps({"response": cand})


# ========== Parse LLM JSON safely ==========
_RESPONSE_FIELD_RE = re.compile(r"^response:\s*(.*)$", re.IGNORECASE | re.MULTILINE)

def parse_llm_demojify_output(content: str) -> str:
    if not content:
        return ""
    # 1) strict JSON
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "response" in data:
            out = str(data["response"])
        else:
            out = ""
    except Exception:
        # 2) Fallbacks if needed
        m = _RESPONSE_FIELD_RE.search(content)
        if m:
            out = m.group(1).strip()
        else:
            lines = [ln.strip() for ln in content.strip().splitlines() if ln.strip()]
            out = lines[-1] if lines else ""

    # final safety: remove any emojis that slipped through
    if _has_emoji(out):
        out = _to_words_no_parens(out)
    return out.strip()


# ========== Validator (robust 0/1 extractor; synonym tolerant) ==========
def _build_validator_messages(standard_text: str, llm_text: str):
    system = (
        "You are an evaluator that outputs EXACTLY one character: '1' or '0'. "
        "Return '1' if the two texts below convey the same intended meaning; "
        "return '0' if they do not or if you are uncertain. Do NOT add any other text."
    )
    user = f"""
Compare two demojified texts describing the same original message.

Decision rule:
- Output "1" if the LLM text and the standard text are semantically consistent.
  Treat minor rewordings and near-synonyms as the SAME meaning
  (e.g., "(kissing face with closed eyes)" ≈ "blowing a kiss").
- Output "0" only if they differ in meaning, omit key intent, or you are unsure.

Return ONLY 1 or 0. No quotes, no spaces, no punctuation.

[STANDARD TEXT]
{standard_text}

[LLM TEXT]
{llm_text}
"""
    return system, user

def _extract_verdict_char(s: str) -> Optional[int]:
    if s is None:
        return None
    s = s.strip()
    if s in ("0", "1"):
        return int(s)
    s = s.strip("`'\" \n\t\r")
    if s in ("0", "1"):
        return int(s)
    m = re.search(r"(?:^|\D)([01])(?:\D|$)", s)
    if m:
        return int(m.group(1))
    return None

def evaluate_consistency_zero_one(client, standard_text: str, llm_text: str, model: str = MODEL) -> Optional[int]:
    system, user = _build_validator_messages(standard_text, llm_text)
    resp = _create_chat_completion(
        client,
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=0.0, top_p=1.0,
        presence_penalty=0.0, frequency_penalty=0.0,
        # max_tokens=2,  # uncomment if supported
    )
    raw = resp.choices[0].message.content if resp and resp.choices else ""
    return _extract_verdict_char(raw)


# ========== Result dataclass ==========
@dataclass
class DemojifyResult:
    final_text: str
    source: str                 # "llm" or "standard"
    standard_text: str
    llm_text: Optional[str]
    reason: str                 # e.g., "llm_valid", "validator_rejected", "validator_error", etc.


# ========== Orchestrator ==========
def demojify(text: str, client, *, model: str = MODEL) -> DemojifyResult:
    print(f"\n=== DEMOJIFY START ===\nInput text: {text}\n")

    # STANDARD (parentheses)
    standard_out = emoji_semantic_clean(text)
    print(f"[STANDARD OUTPUT]\n{standard_out}\n")

    # LLM (plain words or unchanged if no emojis)
    try:
        llm_raw = emoji_to_meaning(client, text, model=model)
        print("[LLM RAW OUTPUT]")
        print(llm_raw, "\n")
        llm_out = parse_llm_demojify_output(llm_raw)
        print(f"[LLM PARSED OUTPUT]\n{llm_out}\n")
        if not llm_out.strip():
            print("[ERROR] LLM output is empty or could not be parsed.")
            return DemojifyResult(
                final_text=standard_out, source="standard",
                standard_text=standard_out, llm_text=None,
                reason="llm_empty_output",
            )
    except Exception as e:
        print("[ERROR] LLM call failed:", repr(e))
        return DemojifyResult(
            final_text=standard_out, source="standard",
            standard_text=standard_out, llm_text=None,
            reason=f"llm_error: {e}",
        )

    # Validator (1 = same meaning, accept LLM)
    try:
        verdict = evaluate_consistency_zero_one(client, standard_out, llm_out, model=model)
        print(f"[VALIDATOR VERDICT] -> {verdict}\n")
    except Exception as e:
        print("[ERROR] Validator call failed:", repr(e))
        verdict = None

    print("[STANDARD]", standard_out)
    print("[LLM RAW]", llm_raw)
    print("[LLM PARSED]", llm_out)
    print("[EVAL VERDICT]", verdict)

    if verdict is None:
        print("[INFO] Validator failed or returned invalid response. Using STANDARD output.")
        return DemojifyResult(
            final_text=standard_out, source="standard",
            standard_text=standard_out, llm_text=llm_out,
            reason="validator_error",
        )

    if verdict == 1:
        print("[SUCCESS] LLM output validated successfully.")
        print(f"→ Final Output: {llm_out}\n")
        return DemojifyResult(
            final_text=llm_out, source="llm",
            standard_text=standard_out, llm_text=llm_out,
            reason="llm_valid",
        )

    print("[INFO] Validator rejected LLM output as semantically inconsistent.")
    print("[DIAGNOSTIC] Standard vs LLM difference:")
    print("→ Standard:", standard_out)
    print("→ LLM:", llm_out)
    return DemojifyResult(
        final_text=standard_out, source="standard",
        standard_text=standard_out, llm_text=llm_out,
        reason="validator_rejected",
    )





