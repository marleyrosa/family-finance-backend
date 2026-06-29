import pytesseract
from pdf2image import convert_from_path
import re
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def parse_pdf_data(file_path: str):
    itens = []

    try:
        imagens = convert_from_path(file_path)

        for img in imagens:
            texto = pytesseract.image_to_string(img, lang="por")

            print("📄 TEXTO OCR:")
            print(texto)

            # ✅ datas simples
            datas = re.findall(r"\d{2}/\d{2}", texto)

            # ✅ valores FLEXÍVEL (igual antes + melhorias)
            valores = re.findall(r"\d+[.,]\d{2}|\d{3,5}", texto)

            print("📅 DATAS:", datas)
            print("💰 VALORES:", valores)

            for i in range(min(len(datas), len(valores))):
                try:
                    data_str = datas[i]
                    valor_str = valores[i]

                    # ✅ normalização do valor (funciona com tudo)
                    if "," in valor_str or "." in valor_str:
                        valor_str = valor_str.replace(".", "").replace(",", ".")
                    else:
                        if len(valor_str) > 2:
                            valor_str = valor_str[:-2] + "." + valor_str[-2:]
                        else:
                            continue

                    valor = float(valor_str)

                    data = datetime.strptime(data_str + "/2026", "%d/%m/%Y")

                    itens.append({
                        "descricao": "Compra OCR",
                        "valor": valor,
                        "data": data,
                        "categoria": "OUTROS"
                    })

                except Exception as e:
                    print("Erro item:", e)

        print(f"🔥 TOTAL EXTRAÍDO: {len(itens)}")
        return itens

    except Exception as e:
        print("❌ ERRO OCR:", e)
        return []