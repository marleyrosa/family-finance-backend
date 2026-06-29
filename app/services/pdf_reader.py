import io
import pdfplumber
import re


def detect_card(text: str) -> str:
    text = text.lower()

    if "master" in text or "mastercard" in text:
        return "Mastercard"
    elif "visa" in text:
        return "Visa"
    elif "elo" in text:
        return "Elo"
    elif "amex" in text:
        return "American Express"
    else:
        return "Desconhecido"


def extract_items_from_pdf(file_bytes: bytes):
    text = ""

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception:
        return []

    text = text.replace("\n", " ")

    cartao = detect_card(text)

    pattern = re.findall(
        r'(\d{2}/\d{2})\s+([A-Z0-9\s\.\-/]+?)\s+(\d{1,3}(?:\.\d{3})*(?:,\d{2}))',
        text
    )

    itens = []

    for data, descricao, valor in pattern:
        try:
            valor_float = float(
                valor.replace(".", "").replace(",", ".")
            )
        except:
            continue

        itens.append({
            "data": data,
            "descricao": descricao.strip(),
            "valor": valor_float,
            "cartao": cartao
        })  # ✅ AQUI FECHA A CHAVE CORRETAMENTE

    return itens