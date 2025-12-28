def parse_percent(value):
    if value is None:
        return None
    return float(value.replace('%', '').replace(',', '.'))


def parse_float(value):
    if value is None:
        return None
    return float(value.replace('.', '').replace(',', '.'))


def avaliar_acao(dados):
    score = 0

    # =========================
    # ETAPA 1 — SOBREVIVÊNCIA
    # =========================
    liquidez = parse_float(dados.get("Liquidez Corr"))
    divida = parse_float(dados.get("Div Br/ Patrim"))
    margem_liq = parse_percent(dados.get("Marg. Líquida"))

    sobrevivencia = 0
    if liquidez and liquidez > 1.5:
        sobrevivencia += 1
    if divida and divida < 1.0:
        sobrevivencia += 1
    if margem_liq and margem_liq > 0:
        sobrevivencia += 1

    if sobrevivencia < 2:
        return "DESCARTAR", score

    score += sobrevivencia

    # =========================
    # ETAPA 2 — VALUATION
    # =========================
    pl = parse_float(dados.get("P/L"))
    pvp = parse_float(dados.get("P/VP"))
    ev_ebit = parse_float(dados.get("EV / EBIT"))

    if pl and pl < 10:
        score += 1
    if pvp and pvp < 1:
        score += 1
    if ev_ebit and ev_ebit < 10:
        score += 1

    # =========================
    # ETAPA 3 — QUALIDADE
    # =========================
    roe = parse_percent(dados.get("ROE"))
    roic = parse_percent(dados.get("ROIC"))
    margem_ebit = parse_percent(dados.get("Marg. EBIT"))

    if roe and roe >= 8:
        score += 1
    if roic and roic >= 6:
        score += 1
    if margem_ebit and margem_ebit >= 8:
        score += 1

    # =========================
    # ETAPA 4 — CONSISTÊNCIA
    # =========================
    anos = ["2020", "2021", "2022", "2023", "2024", "2025"]
    positivos = 0
    negativos = 0
    maior_queda = 0

    for ano in anos:
        retorno = parse_percent(dados.get(ano))
        if retorno is None:
            continue
        if retorno > 0:
            positivos += 1
        else:
            negativos += 1
            maior_queda = min(maior_queda, retorno)

    if positivos >= negativos:
        score += 1

    if maior_queda < -60:
        score -= 1

    # =========================
    # ETAPA 5 — RISCO & CONTEXTO
    # =========================
    setor = dados.get("Setor", "")
    dy = parse_percent(dados.get("Div. Yield"))
    cresc_rec = parse_percent(dados.get("Cres. Rec (5a)"))

    if setor in ["Construção Civil", "Commodities"]:
        score -= 1

    if dy and dy > 12 and negativos > positivos:
        score -= 1

    if cresc_rec and cresc_rec >= 10:
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
