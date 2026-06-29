def categorize_expense(text: str) -> str:
    text = text.lower()

    # 💳 CARTÃO (SEU CASO PRINCIPAL)
    if "santander" in text or "fatura" in text or "cartão" in text:
        return "Cartão de Crédito"

    # ⚡ ENERGIA
    elif "energia" in text or "enel" in text:
        return "Energia"

    # 🛒 MERCADO
    elif "mercado" in text or "supermercado" in text:
        return "Alimentação"

    # 🌐 INTERNET
    elif "internet" in text or "vivo" in text:
        return "Internet"

    # 💧 ÁGUA
    elif "água" in text or "copasa" in text:
        return "Água"

    else:
        return "Outros"
