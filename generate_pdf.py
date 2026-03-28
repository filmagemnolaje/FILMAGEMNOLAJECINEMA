"""
generate_pdf.py
Converte portfolio-filmagem-no-laje.html em PDF interativo (links clicáveis preservados).
Dependências: pip install playwright && playwright install chromium
"""

import asyncio
import os
import sys
from pathlib import Path


async def generate():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("[ERRO] Playwright não instalado.")
        print("       Execute: pip install playwright && playwright install chromium")
        sys.exit(1)

    base_dir = Path(__file__).parent.resolve()
    html_file = base_dir / "portfolio-filmagem-no-laje.html"
    pdf_file  = base_dir / "portfolio-filmagem-no-laje.pdf"

    if not html_file.exists():
        print(f"[ERRO] Arquivo HTML não encontrado: {html_file}")
        sys.exit(1)

    print(f"[INFO] Lendo: {html_file}")
    print(f"[INFO] Gerando: {pdf_file}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Carrega o HTML local com suporte a assets relativos
        await page.goto(html_file.as_uri(), wait_until="networkidle")

        # Aguarda fontes do Google Fonts carregarem (ou timeout de 5s)
        try:
            await page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

        await page.pdf(
            path=str(pdf_file),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            # Preserva links clicáveis no PDF
            tagged_pdf=True,
        )

        await browser.close()

    size_kb = pdf_file.stat().st_size // 1024
    print(f"[OK]   PDF gerado com sucesso: {pdf_file}  ({size_kb} KB)")


if __name__ == "__main__":
    asyncio.run(generate())
