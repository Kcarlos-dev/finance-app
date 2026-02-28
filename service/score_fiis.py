def parse_percent(value):
    if value is None:
        return None
    return float(value.replace('%', '').replace(',', '.'))


def parse_float(value):
    if value is None:
        return None
    return float(value.replace('.', '').replace(',', '.'))

def normalizar_valor_bruto(valor):
    if valor is None:
        return None
    if valor == "-":
        return "0"
    return valor


def avaliar_fii_fiagro(dados):
    score = 0

    # =========================
    # ETAPA 1 — SOBREVIVÊNCIA / LIQUIDEZ
    # =========================
    vol_med = parse_float(normalizar_valor_bruto(dados.get("Vol $ méd (2m)")))
    patrimonio = parse_float(normalizar_valor_bruto(dados.get("Patrim Líquido")))
    nro_cotas = parse_float(normalizar_valor_bruto(dados.get("Nro. Cotas")))

    sobrevivencia = 0
    if vol_med and vol_med > 1000000:  # Liquidez mínima, ex: >1M volume médio diário nos últimos 2 meses
        sobrevivencia += 1
    if patrimonio and patrimonio > 500000000:  # Patrimônio líquido >500M (fundo robusto)
        sobrevivencia += 1
    if nro_cotas and nro_cotas > 50000000:  # Mais de 50M cotas (boa dispersão)
        sobrevivencia += 1


    score += sobrevivencia

    # =========================
    # ETAPA 2 — VALUATION
    # =========================
    pvp = parse_float(normalizar_valor_bruto(dados.get("P/VP")))
    dy = parse_percent(normalizar_valor_bruto(dados.get("Div. Yield")))
    ffo_yield = parse_percent(normalizar_valor_bruto(dados.get("FFO Yield")))

    if pvp and pvp < 1.0:
        score += 1
    elif pvp and pvp < 1.1:  # Leve prêmio ainda aceitável se yields altos
        score += 0.5
    if dy and dy > 8:
        score += 1
    if ffo_yield and ffo_yield > 8:
        score += 1

    # =========================
    # ETAPA 3 — QUALIDADE
    # =========================
    gestao = dados.get("Gestão", "").lower()
    segmento = dados.get("Segmento", "").lower()

    if gestao == "ativa":  # Gestão ativa pode ser melhor para FIAGROs
        score += 1
    if segmento in ["logística", "shopping", "escritórios", "outros", "agro"]:  # Segmentos considerados estáveis; adapte conforme necessidade
        score += 1

    # =========================
    # ETAPA 4 — CONSISTÊNCIA
    # =========================
    anos = ["2020", "2021", "2022", "2023", "2024", "2025"]
    positivos = 0
    negativos = 0
    maior_queda = 0

    for ano in anos:
        retorno = parse_percent(normalizar_valor_bruto(dados.get(ano)))
        if retorno is None:
            continue
        if retorno > 0:
            positivos += 1
        else:
            negativos += 1
            maior_queda = min(maior_queda, retorno)

    if positivos >= negativos:
        score += 1

    if maior_queda > -20:  # FIIs/FIAGROs toleram menos quedas drásticas, mas são mais estáveis que ações
        score += 1

    # =========================
    # ETAPA 5 — RISCO & CONTEXTO
    # =========================
    mes = parse_percent(normalizar_valor_bruto(dados.get("Mês")))
    dia = parse_percent(normalizar_valor_bruto(dados.get("Dia")))
    cresc_12m = parse_percent(normalizar_valor_bruto(dados.get("12 meses")))

    if mes and mes > 0:
        score += 0.5
    if dia and dia > 0:
        score += 0.5
    if cresc_12m and cresc_12m > 10:  # Crescimento nos últimos 12 meses
        score += 1

    # =========================
    # DECISÃO FINAL
    # =========================
    if score >= 8:
        decisao = "O ALGORITMO RECOMENDA COMPRAR, PORÉM SEMPRE CONSULTAR UM PROFISSIONAL DE INVESTIMENTOS"
    elif score >= 6:
        decisao = "O ALGORITMO RECOMENDA UMA COMPRA COM CAUTELA, LEMBRE-SE SEMPRE CONSULTAR UM PROFISSIONAL DE INVESTIMENTOS"
    elif score >= 4:
        decisao = "O ALGORITMO RECOMENDA OBSERVAR, LEMBRE-SE SEMPRE CONSULTAR UM PROFISSIONAL DE INVESTIMENTOS"
    else:
        decisao = "O ALGORITMO RECOMENDA DESCARTAR A COMPRA, LEMBRE-SE SEMPRE CONSULTAR UM PROFISSIONAL DE INVESTIMENTOS"

    return {
        "decisao": decisao,
        "score": score
    }