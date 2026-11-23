"""Turns the computed facts into a short coach's note."""
import json, os, sys
from pathlib import Path

REF = Path(__file__).parent / "references"
MODEL = os.environ.get("COACH_MODEL", "claude-sonnet-5-5")

SYSTEM = """You are a data-driven marathon running coach blending the Norwegian
double-threshold method with Stryd running-power data. Reference material:

{refs}

Write a coach's text message, 100-180 words, technical, numbers first, no bullet
lists, no fluff. Four parts: (1) what the run was for and whether execution
matched (%CP, zone, pace/HR); (2) form snapshot (CTL/ATL/TSB, ramp, resting HR,
sleep); (3) one concrete recommendation for the next session or two; (4) a
red-flag warning ONLY if the data warrants it. Use only the numbers provided.

If facts.intervals is present, the run was a structured session: judge it rep by rep
(mean %CP vs the intended zone, spread, fade, HR drift, recoveries) and lead with that
rather than the whole-run average, which blends warm-up, reps and cooldown. You may
go to ~220 words in that case. Name any flags explicitly."""


def fallback(facts: dict) -> str:
    r, f = facts["run"], facts["form"]
    iv = facts.get("intervals")
    extra = ""
    if iv:
        reps = ", ".join(f"{x['watts']}W/{x['pct_cp']}%" for x in iv["reps"])
        extra = (f" Reps ({iv['n_reps']}, {iv['kind']}): {reps}; mean {iv['mean_pct_cp']}% CP, "
                 f"fade {iv['fade_pct']}%, flags: {'; '.join(iv['flags']) or 'none'}.")
    base = (f"{r['name']} ({r['date']}): {r['avg_power']} W = {r['pct_cp']}% CP -> {r['zone']} "
            f"({r['landmark']}). Form TSB {f.get('tsb')} ({f.get('tsb_state')}), ramp "
            f"{f.get('ramp')} ({f.get('ramp_state')}). Flags: {'; '.join(r['flags']) or 'none'}.")
    return base + extra


def _refs() -> str:
    return "\n\n".join(p.read_text() for p in sorted(REF.glob("*.md")))


def _via_api(facts: dict) -> str:
    import anthropic
    msg = anthropic.Anthropic().messages.create(
        model=MODEL, max_tokens=600, system=SYSTEM.format(refs=_refs()),
        messages=[{"role": "user", "content": json.dumps(facts, indent=1, default=str)}])
    return msg.content[0].text.strip()


def _via_claude_code(facts: dict) -> str:
    """Use a Claude subscription via the Claude Code CLI (CLAUDE_CODE_OAUTH_TOKEN)."""
    import subprocess
    prompt = SYSTEM.format(refs=_refs()) + "\n\nFACTS:\n" + json.dumps(facts, indent=1, default=str)
    r = subprocess.run(["claude", "-p", "--output-format", "text"], input=prompt,
                       capture_output=True, text=True, timeout=240)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(r.stderr[-300:])
    return r.stdout.strip()


def coach_note(facts: dict) -> str:
    """API key -> subscription token -> plain numeric summary. Never raises."""
    try:
        if os.environ.get("ANTHROPIC_API_KEY"):
            return _via_api(facts)
        if os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
            return _via_claude_code(facts)
    except Exception as e:  # keep the check-in alive even if the model call fails
        print(f"LLM failed ({type(e).__name__}): {e}", file=sys.stderr)
    return fallback(facts)
