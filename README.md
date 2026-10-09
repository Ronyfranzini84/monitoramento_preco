# 📚 Monitoramento de Preço — Estudo de Web Scraping com BeautifulSoup

Projeto de estudo com foco em **web scraping** usando a biblioteca **BeautifulSoup**, complementado com **tratamento e análise de dados em pandas** e **formatação de planilhas Excel via openpyxl**.

O site utilizado como alvo da raspagem é o [books.toscrape.com](https://books.toscrape.com/), um site público criado justamente para praticar técnicas de scraping (catálogo fictício de livros, sem necessidade de login ou autorização especial).

## 🎯 Objetivo

Praticar o fluxo completo de um projeto de coleta e análise de dados:

1. Fazer requisições HTTP a um site (`requests`).
2. Extrair informações do HTML com `BeautifulSoup`.
3. Paginar automaticamente por todas as páginas do catálogo até o fim.
4. Estruturar os dados coletados em um `DataFrame` (`pandas`).
5. Exportar os dados para uma planilha Excel (`.xlsx`).
6. Analisar os dados (preços, avaliações, filtros, agrupamentos etc.).
7. Formatar a planilha Excel final (cabeçalho em destaque) com `openpyxl`.

## 🗂️ Estrutura do projeto

| Arquivo | Descrição |
|---|---|
| [main.ipynb](./main.ipynb) | Notebook principal: faz o scraping de todas as páginas do site, extrai nome, preço, disponibilidade e avaliação de cada livro, consolida tudo em um `DataFrame`, salva em `books_catalog.xlsx` e realiza diversas análises exploratórias com pandas. |
| [format_catolog_2.ipynb](./format_catolog_2.ipynb) | Notebook que abre o `books_catalog.xlsx` gerado e formata a linha de cabeçalho (negrito, fundo azul) usando `openpyxl`. |
| [tratamento_dados_pandas.ipynb](./tratamento_dados_pandas.ipynb) | Notebook inicial/experimental para tratamento de dados com pandas (ainda em esboço). |
| [books_catalog.xlsx](./books_catalog.xlsx) | Planilha gerada automaticamente pelo `main.ipynb` com os dados de todos os livros coletados. |
| [requirements.txt](./requirements.txt) | Dependências Python do projeto. |

## 🔎 Como funciona o scraping (main.ipynb)

- A partir da URL inicial `https://books.toscrape.com/`, o código:
  - Faz o `GET` da página com `requests` e interpreta o HTML com `BeautifulSoup`.
  - Localiza todos os elementos `<article class="product_pod">` (cada livro do catálogo).
  - Para cada livro extrai:
    - **name** — nome/título do livro (atributo `title` do link).
    - **price** — preço (convertido de string para `float`, removendo o símbolo de moeda).
    - **availability** — texto de disponibilidade em estoque.
    - **rating** — nota de avaliação (de 1 a 5), convertida a partir da classe CSS textual (`One`, `Two`, `Three`...) para número.
  - Segue automaticamente o link **"next"** de paginação (`urljoin`) até não haver mais próxima página, percorrendo as 50 páginas do catálogo (1000 livros no total).
  - Consolida tudo em um `DataFrame` do pandas e exporta para `books_catalog.xlsx`.

### Análises realizadas com pandas

Depois da coleta, o notebook explora os dados com:

- Verificação de duplicados e valores ausentes/vazios.
- Estatísticas descritivas de preço (`describe`).
- Top 10 livros mais caros e mais baratos (`sort_values`, `nlargest`, `nsmallest`).
- Filtros por faixa de preço (`between`) e por avaliação (`isin`, `query`).
- Contagem de livros por avaliação (`value_counts`).
- Preço médio por avaliação (`groupby` + `agg`).
- Exemplos adicionais de `merge` e `concat` entre DataFrames (simulando tabelas de cargas/transportadoras) para praticar junções e combinações de dados.

## 🖌️ Formatação da planilha (format_catolog_2.ipynb)

Abre o arquivo `books_catalog.xlsx` com `openpyxl` e aplica formatação visual na primeira linha (cabeçalho): texto em negrito e branco sobre um fundo azul, salvando a planilha já formatada.

## 🛠️ Tecnologias utilizadas

- **Python 3**
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — parsing de HTML
- [requests](https://docs.python-requests.org/) — requisições HTTP
- [pandas](https://pandas.pydata.org/) — manipulação e análise de dados
- [openpyxl](https://openpyxl.readthedocs.io/) — leitura/escrita/formatação de arquivos Excel
- [Jupyter Notebook](https://jupyter.org/) — ambiente interativo de desenvolvimento

## ▶️ Como executar

1. Crie e ative um ambiente virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
3. Abra os notebooks no VS Code ou Jupyter e execute as células em ordem:
   - `main.ipynb` → coleta os dados e gera `books_catalog.xlsx`.
   - `format_catolog_2.ipynb` → formata o cabeçalho do Excel gerado.

## 📌 Observações

- Este é um **projeto de estudo**, criado para praticar scraping e análise de dados — não tem fins comerciais.
- O site `books.toscrape.com` é um ambiente público destinado exatamente a esse tipo de prática, não havendo preocupações éticas/legais quanto ao scraping nesse caso.
- Os arquivos `.xlsx` estão listados no `.gitignore`, então `books_catalog.xlsx` só existe localmente após a execução do `main.ipynb` (a cópia atual no repositório é um artefato de exemplo gerado durante o estudo).
