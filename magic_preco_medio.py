import re

import numpy as np
import pandas as pd
from playwright.sync_api import sync_playwright


def acessar_site(nome_portugues: str, nome_ingles: str):
    """
    Acessa a página do card no Liga Magic, aceita os cookies e
    inicia a extração de dados.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = f"https://www.ligamagic.com/?view=cards/card&card={nome_ingles}&aux={nome_portugues}"
        print(f"Acessando: {nome_portugues} ({nome_ingles})...")

        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        # Tratamento do banner de Cookies
        botao_cookie = page.locator("#lgpd-cookie button").first
        if botao_cookie.count() > 0:
            print("Banner de cookies encontrado. Aceitando...")
            botao_cookie.click()
            page.wait_for_timeout(500)

        try:
            # CORREÇÃO AQUI: Passando os nomes como argumentos para o fallback
            dados = pegar_dados_cartas(page, nome_portugues, nome_ingles)
            return dados
        except Exception as e:
            print(f"❌ Erro crítico ao processar {nome_portugues}: {e}")
            return []
        finally:
            browser.close()


def pegar_dados_cartas(page, nome_pt_fallback, nome_en_fallback):
    """
    Extrai os dados de todas as edições de uma carta.
    Lida tanto com cartas de múltiplas edições (com slider)
    quanto com cartas de edição única (sem slider).
    """
    page.wait_for_timeout(1500)  # Aguarda renderização do JS

    botoes_edicao = page.locator("#slider-editions-icons > a").all()
    dados_coletados = []

    # Função interna para evitar repetição de código (DRY)
    def extrair_dados_da_tela_atual():
        # 1. Edição (se não achar, assume "Edição Única")
        try:
            edicao = (
                page.locator("div.name-edition").inner_text().replace("\n", " ").strip()
            )
        except Exception:
            edicao = "Edição Única"

        # 2. Artista
        try:
            artista = page.locator('//*[@id="details-screen-artist"]/a').inner_text()
        except Exception:
            artista = "N/A"

        # 3. Raridade
        try:
            raridade = page.locator(
                '//*[@id="details-screen-rarity"]/a[1]'
            ).inner_text()
        except Exception:
            raridade = "N/A"

        # 4. Preço
        try:
            preco_medio = page.locator(
                'xpath=//*[@id="container-price-mkp-card"]/div[2]/div[2]/div[2]/div'
            ).inner_text()
        except Exception:
            preco_medio = "N/A"

        # 5. Nomes (Tenta extrair, usa fallback se falhar)
        try:
            nome_por = page.locator(
                "xpath=/html/body/main/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[1]"
            ).inner_text(timeout=3000)
            nome_ing = page.locator(
                "xpath=/html/body/main/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[2]"
            ).inner_text(timeout=3000)
        except Exception:
            nome_por = nome_pt_fallback
            nome_ing = nome_en_fallback

        return {
            "nome_pt": nome_por,
            "nome_en": nome_ing,
            "edicao": edicao,
            "raridade": raridade,
            "artista": artista,
            "preco": preco_medio,
        }

    # --- LÓGICA PRINCIPAL ---
    if len(botoes_edicao) == 0:
        print(
            f"   [Info] Apenas 1 edição encontrada (sem slider). Extraindo dados da tela principal."
        )
        dados = extrair_dados_da_tela_atual()
        dados_coletados.append(dados)
        print(f'✅ {dados["nome_pt"]} | {dados["edicao"]} | {dados["preco"]}')

    else:
        print(f"🔍 Encontrados {len(botoes_edicao)} botões de edição no slider.")
        for indice, botao in enumerate(botoes_edicao, start=1):
            try:
                botao.click()
                page.wait_for_timeout(800)
                page.wait_for_selector(
                    "div.name-edition", state="visible", timeout=5000
                )

                dados = extrair_dados_da_tela_atual()
                dados_coletados.append(dados)
                print(f'✅ {dados["nome_pt"]} | {dados["edicao"]} | {dados["preco"]}')

            except Exception as e:
                print(f"⚠️ Erro na edição {indice}: {e}")
                continue

    return dados_coletados


def limpar_e_converter_preco(df):
    """
    Limpa a coluna 'preco' (ex: 'R$ 1.023,00' ou 'N/A')
    e cria uma nova coluna 'preco_float' com valores numéricos.
    """
    # Cria uma cópia da coluna para não estragar a original (boa prática)
    preco_limpo = df["preco"].astype(str).str.replace("R$", "", regex=False).str.strip()

    # Remove os pontos de milhar e troca a vírgula decimal por ponto
    preco_limpo = preco_limpo.str.replace(".", "", regex=False).str.replace(",", ".")

    # Converte para número. O 'errors="coerce"' transforma 'N/A' ou textos inválidos em NaN (Not a Number)
    df["preco_float"] = pd.to_numeric(preco_limpo, errors="coerce")

    return df


# calculando a comissão do mercado livre
def comissao_ml(valor_medio) -> int:
    """
    calculo de porcentagem (ml) e valor final do produto:
    - valores maiores ou iguais a R$ 79,00 a comissão do ML é de 11,5%
    - valores menores que R$ 79,00 a comissão do ML é de 11,5% + R$ 5,00
    """
    # Tratamento de valores nulos ou inválidos
    if pd.isna(valor_medio) or valor_medio == 0:
        return 0.0

    # Cálculo da comissão
    comissao = 0.115 * valor_medio
    if valor_medio < 79:
        comissao += 5.0

    valor_final = valor_medio + comissao
    return round(valor_final, 2)


def separar_edicao_ano(edicao_completa):
    """
    Separa 'Sexta Edição Classica (1999)' em ('Sexta Edição Classica', 1999).
    Se não tiver ano, retorna (edicao, None).
    """
    if pd.isna(edicao_completa):
        return (edicao_completa, None)

    # Regex para encontrar (ANO) no final da string
    match = re.search(r"\((\d{4})\)\s*$", str(edicao_completa))

    if match:
        ano = int(match.group(1))
        # Remove o (ANO) do final e limpa espaços
        nome_edicao = re.sub(r"\s*\(\d{4}\)\s*$", "", str(edicao_completa)).strip()
        return (nome_edicao, ano)
    else:
        return (str(edicao_completa).strip(), None)


# ==============================================================================
# PROCESSAMENTO DOS DADOS
# ==============================================================================

todos_os_dados = []

cartas_df = pd.read_excel("excel/lista_cartas_magic_com_edicao.xlsx")
cartas_df = cartas_df.drop_duplicates(
    subset="nome_portugues", keep="first"
).reset_index(drop=True)

for portugues, ingles in zip(cartas_df["nome_portugues"], cartas_df["nome_ingles"]):

    print(f"\n{'='*60}")
    print(f"Processando: {portugues} ({ingles})")
    print(f"{'='*60}")

    dados_carta = acessar_site(portugues, ingles)

    # Se a função retornou dados, adicione à lista principal
    if dados_carta:
        todos_os_dados.extend(dados_carta)
        print(f"✅ {len(dados_carta)} edições capturadas para {portugues}")
    else:
        print(f"⚠️ Nenhuma edição capturada para {portugues}")

# 3. Converta a lista acumulada para DataFrame
if todos_os_dados:
    cartas_web_df = pd.DataFrame(todos_os_dados)
    print(f"\n{'='*60}")
    print(f"Total de registros capturados: {len(cartas_web_df)}")
    print(cartas_web_df.head())

    # APLIQUE A LIMPEZA DO PREÇO AQUI
    cartas_web_df = limpar_e_converter_preco(cartas_web_df)

    cartas_web_df["valor_ml"] = cartas_web_df["preco_float"].apply(comissao_ml)

    # Renomeia as colunas do DataFrame raspado para bater com o original
    cartas_web_df = cartas_web_df.rename(
        columns={
            "nome_pt": "nome_portugues",
            "nome_en": "nome_ingles",
            "edicao": "edicao_completa",
        }
    )

    # Separa edição e ano
    cartas_web_df[["edicao", "ano"]] = cartas_web_df["edicao_completa"].apply(
        lambda x: pd.Series(separar_edicao_ano(x))
    )

    # Limpeza de segurança nas chaves de merge (remove espaços extras)
    cartas_df["nome_portugues"] = cartas_df["nome_portugues"].str.strip()
    cartas_df["nome_ingles"] = cartas_df["nome_ingles"].str.strip()
    cartas_df["edicao"] = cartas_df["edicao"].str.strip()

    # Corrige a pequena diferença de digitação no arquivo original
    cartas_df["edicao"] = cartas_df["edicao"].replace(
        "Máscara de Mercádia", "Máscaras de Mercádia"
    )

    # Garante que o DataFrame raspado também esteja limpo
    cartas_web_df["nome_portugues"] = cartas_web_df["nome_portugues"].str.strip()
    cartas_web_df["nome_ingles"] = cartas_web_df["nome_ingles"].str.strip()
    cartas_web_df["edicao"] = cartas_web_df["edicao"].str.strip()

    # Merge usando 'edicao' (sem ano) como chave
    cartas_final_df = pd.merge(
        cartas_df,
        cartas_web_df,
        how="left",
        on=["nome_portugues", "nome_ingles", "edicao"],
    )

    # Opcional: mostrar Top 5 no terminal
    print("\n--- Top 5 Cartas/Edições mais caras ---")
    print(
        cartas_web_df.sort_values("preco_float", ascending=False)[
            ["nome_portugues", "edicao_completa", "preco", "preco_float"]
        ].head()
    )

    # Salvar dados brutos
    cartas_web_df.to_excel("excel/precos_capturados.xlsx", index=False)
    print("Dados brutos salvos em excel/precos_capturados.xlsx")

    # Salvar arquivo final com merge
    cartas_final_df.to_excel("excel/cartas_com_precos_atualizados.xlsx", index=False)
    print(f"Arquivo final salvo em excel/cartas_com_precos_atualizados.xlsx")
    print(f"Total de registros: {len(cartas_final_df)}")
