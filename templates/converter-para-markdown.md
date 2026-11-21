# Dica: envie o currículo em Markdown (.md)

Mostre este texto quando pedir o currículo, a carta antiga ou o perfil do LinkedIn da pessoa.

---

**Antes de me enviar o seu currículo:** se puder, converta o PDF ou o DOCX para Markdown (`.md`).

- **Por que:** o `.md` é texto puro. Ler um PDF ou um DOCX gasta bem mais tokens do seu plano, por causa do layout e da formatação. Com o `.md` o uso fica menor e a leitura mais fiel.
- **Depois de converter:** abra o `.md` e confira se os cargos, as datas e a ordem das seções estão certos. PDFs em duas colunas às vezes saem embaralhados.
- **Privacidade:** prefira as ferramentas que rodam no seu computador. Evite conversores online desconhecidos, porque o currículo tem seus dados pessoais.

Se preferir, pode mandar o PDF ou o DOCX assim mesmo: eu leio do mesmo jeito.

| Ferramenta | Sistemas | Converte | Como usar |
|---|---|---|---|
| **MarkItDown** (Microsoft, grátis, código aberto) | Mac, Windows, Linux | PDF, DOCX, PPTX, XLSX | `pipx install 'markitdown[all]'` e depois `markitdown curriculo.pdf -o curriculo.md` |
| **Pandoc** (grátis, código aberto) | Mac, Windows, Linux | DOCX (não lê PDF) | `pandoc curriculo.docx -t gfm -o curriculo.md` |
| **Docling** (IBM, grátis, código aberto) | Mac, Windows, Linux | PDF (inclusive com colunas e tabelas), DOCX | `pipx install docling` e depois `docling curriculo.pdf --to md` |
| **Typora** (pago, com interface gráfica) | Mac, Windows, Linux | DOCX | Arquivo > Importar e depois salvar como `.md` (precisa do Pandoc instalado) |
| **Google Docs** (no navegador, sem instalar nada) | Qualquer um | DOCX e PDF | Abra o arquivo no Google Docs e use Arquivo > Fazer download > Markdown (.md). O arquivo fica na sua conta Google. |

## Como instalar

**Pandoc**
- Mac: `brew install pandoc`
- Windows: `winget install --id JohnMacFarlane.Pandoc`
- Linux (Debian/Ubuntu): `sudo apt install pandoc`

**pipx** (para o MarkItDown e o Docling, que precisam do Python 3.10 ou mais novo)
- Mac: `brew install pipx`
- Windows: `py -m pip install --user pipx`
- Linux (Debian/Ubuntu): `sudo apt install pipx`

Depois de instalar o pipx, rode `pipx ensurepath` e abra um terminal novo.
