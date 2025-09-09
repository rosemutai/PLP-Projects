from typing import Dict, Any, Optional


crypto_db: Dict[str, Dict[str, Any]] = {
    "Bitcoin": {
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3/10,
    },
    "Ethereum": {
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6/10,
    },
    "Cardano": {
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8/10,
    },
}

AVAILABLE_TONES = ("friendly", "professional", "meme")


def choose_tone_interactive() -> str:
    """Ask the user to choose a tone at startup."""
    print("Choose a tone for the bot (friendly / professional / meme). Press Enter for friendly.")
    choice = input("Tone: ").strip().lower()
    if choice not in AVAILABLE_TONES:
        print("Unknown or empty choice - defaulting to 'friendly'.")
        return "friendly"
    return choice


def tone_prefix(tone: str) -> str:
    """Return a short prefix/voice tailored to the chosen tone."""
    if tone == "professional":
        return "Hello. Here's an objective summary:"
    if tone == "meme":
        return "Yo! LFG 🚀 — memeing aside, here's the tea:"
    # friendly default
    return "Hey there! Let's find you a green and growing crypto 🌱"


MARKET_CAP_WEIGHT = {"high": 1.0, "medium": 0.7, "low": 0.4}
TREND_WEIGHT = {"rising": 0.9, "stable": 0.6, "falling": 0.2, "declining": 0.2}
ENERGY_PREFERENCE = {"low": 1.0, "medium": 0.6, "high": 0.2}


def find_coin_by_name(name: str) -> Optional[str]:
    """Case-insensitive exact match helper (returns canonical key or None)."""
    name = name.strip().lower()
    for k in crypto_db:
        if k.lower() == name:
            return k
    return None

def compute_profitability_score(coin: Dict[str, Any]) -> float:
    """
    Simple heuristic:
      - trend (rising/stable/falling) has 60% weight
      - market cap has 40% weight
    Returns a score between 0 and 1.
    """
    trend = coin.get("price_trend", "stable")
    cap = coin.get("market_cap", "medium")
    t = TREND_WEIGHT.get(trend, 0.5)
    c = MARKET_CAP_WEIGHT.get(cap, 0.7)
    score = 0.6 * t + 0.4 * c
    # clamp
    return max(0.0, min(1.0, score))


def compute_sustainability_score(coin: Dict[str, Any]) -> float:
    """
    Uses the provided sustainability_score (expected 0..1) and energy preference.
    Combines them into a single 0..1 number for ranking.
    """
    base = float(coin.get("sustainability_score", 0.0))
    energy = coin.get("energy_use", "medium")
    e_pref = ENERGY_PREFERENCE.get(energy, 0.6)
    # Weighted combination (base is important, energy preference refines it)
    combined = 0.75 * base + 0.25 * e_pref
    return max(0.0, min(1.0, combined))


def combined_investment_score(coin: Dict[str, Any]) -> float:
    """Higher means better: 60% profitability, 40% sustainability (per instructions)."""
    p = compute_profitability_score(coin)
    s = compute_sustainability_score(coin)
    combined = 0.6 * p + 0.4 * s
    return max(0.0, min(1.0, combined))


def recommendation_label(score: float) -> str:
    """Map a numeric score to a readable recommendation."""
    if score >= 0.8:
        return "Strong Buy"
    if score >= 0.6:
        return "Buy"
    if score >= 0.45:
        return "Hold"
    if score >= 0.25:
        return "Sell"
    return "Strong Sell"


def handle_list() -> str:
    return "Available coins: " + ", ".join(sorted(crypto_db.keys()))


def handle_trending() -> str:
    rising = [k for k, v in crypto_db.items() if v.get("price_trend") == "rising"]
    if not rising:
        return "No coins are currently marked as rising in the dataset."
    # sort rising coins by market cap
    rising_sorted = sorted(rising, key=lambda x: MARKET_CAP_WEIGHT[crypto_db[x].get("market_cap","medium")], reverse=True)
    return "Trending up: " + ", ".join(rising_sorted)


def handle_most_sustainable() -> str:
    best = max(crypto_db.keys(), key=lambda x: compute_sustainability_score(crypto_db[x]))
    score = compute_sustainability_score(crypto_db[best])
    return f"Most sustainable: {best} — sustainability index {score:.2f} (higher is greener)."


def handle_analyze(name: str) -> str:
    key = find_coin_by_name(name)
    if not key:
        return f"I don't have data for '{name}'. Try 'list' to see supported coins."
    coin = crypto_db[key]
    p = compute_profitability_score(coin)
    s = compute_sustainability_score(coin)
    combined = combined_investment_score(coin)
    label = recommendation_label(combined)

    lines = [
        f"Analysis for {key}:",
        f" - Price trend: {coin.get('price_trend')}",
        f" - Market cap: {coin.get('market_cap')}",
        f" - Energy use: {coin.get('energy_use')}",
        f" - Raw sustainability_score: {float(coin.get('sustainability_score')):.2f} (0..1)",
        f" - Profitability index: {p:.2f}",
        f" - Sustainability index: {s:.2f}",
        f" -> Combined score: {combined:.2f} => Recommendation: {label}",
    ]

    if coin.get('market_cap') == 'low' and combined >= 0.6:
        lines.append("Note: strong signal but small market cap increases risk; consider a smaller position size.")
    return "".join(lines)


def handle_recommendation() -> str:
    scored = [(k, combined_investment_score(v)) for k, v in crypto_db.items()]
    scored_sorted = sorted(scored, key=lambda x: x[1], reverse=True)
    top_name, top_score = scored_sorted[0]
    label = recommendation_label(top_score)
    explanation = (
        f"Top pick: {top_name} — score {top_score:.2f}. {label}."
        "(Scoring uses 60% profitability and 40% sustainability by default.)"
    )
    if len(scored_sorted) > 1 and scored_sorted[1][1] >= top_score - 0.05:
        explanation += f"Close contender: {scored_sorted[1][0]} (score {scored_sorted[1][1]:.2f})."
    return explanation


def print_help(tone: str) -> None:
    base = (
        "Commands:"
        " - list : show supported coins"
        " - trending : which coins are trending up"
        " - sustainable : show the most sustainable coin"
        " - analyze <coin> : analyze a named coin (e.g. analyze Cardano)"
        " - recommend : give a top pick based on profitability + sustainability"
        " - tone : change the bot tone (friendly / professional / meme)"
        " - help : show this help text"
        " - exit : quit"
    )
    if tone == 'meme':
        print(base + "Pro tip: only invest what you can meme-loss 😂")
    else:
        print(base)


def run_chatbot():
    tone = choose_tone_interactive()
    print(tone_prefix(tone))
    print("Type 'help' to see commands.")

    while True:
        try:
            user = input('You: ').strip()
        except (KeyboardInterrupt, EOFError):
            print('Goodbye!')
            break

        if not user:
            continue

        u = user.lower()
        if u in ('exit', 'quit'):
            print('Goodbye!')
            break
        if u in ('help', '?'):
            print_help(tone)
            continue
        if u == 'list' or u == 'show':
            print(handle_list())
            continue
        if 'trend' in u or 'trending' in u or 'rising' in u:
            print(handle_trending())
            continue
        if 'sustain' in u or 'sustainable' in u or 'green' in u:
            print(handle_most_sustainable())
            continue
        if u.startswith('analyze '):
            name = user[len('analyze '):].strip()
            print(handle_analyze(name))
            continue
        if 'recommend' in u or 'what should i buy' in u or 'advice' in u:
            print(handle_recommendation())
            continue
        if u.startswith('tone'):
            # allow commands like: tone meme
            parts = u.split()
            if len(parts) >= 2 and parts[1] in AVAILABLE_TONES:
                tone = parts[1]
                print(f"Tone set to {tone}.")
            else:
                print(f"Current tone: {tone}. Available: {', '.join(AVAILABLE_TONES)}")
            continue

        print("Sorry, I didn't understand. Type 'help' for commands.")


if __name__ == '__main__':
    run_chatbot()
