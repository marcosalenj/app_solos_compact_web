import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# ==== Funções auxiliares ====

def frange(start, stop, step):
    while start <= stop:
        yield round(start, 2)
        start += step

def gerar_umidades(umidade_hot, quantidade):
    inicio = round(umidade_hot - 1.0, 1)
    fim = round(umidade_hot - 0.1, 1)
    valores = [round(i, 1) for i in frange(inicio, fim, 0.1)]
    return random.choices(valores, k=quantidade)

def gerar_grau_compactacao(tipo):
    if tipo == "1º Aterro / Ligação":
        return round(random.uniform(94.5, 96.4), 1)
    return round(random.uniform(100.0, 102.0), 1)

# ==== Layout ====

app.layout = dbc.Container([
    html.H2("Simulador de Ensaios de Solo", className="text-center my-4"),

    dbc.Row([
        dbc.Col([
            dbc.Label("Tipo de ensaio:"),
            dcc.Dropdown(
                id='tipo-ensaio',
                options=[
                    {"label": "1º Aterro / Ligação", "value": "1º Aterro / Ligação"},
                    {"label": "2º Aterro / Sub-base", "value": "2º Aterro / Sub-base"}
                ],
                value="1º Aterro / Ligação",
                className="mb-3"
            ),

            dbc.Label("Quantidade de ensaios:"),
            dbc.Input(id="qtd", type="number", min=1, placeholder="Ex: 5", className="mb-3"),

            dbc.Label("Peso do cilindro (g):"),
            dbc.Input(id="peso", type="number", placeholder="Ex: 964", className="mb-3"),

            dbc.Label("Volume do cilindro (L):"),
            dbc.Input(id="volume", type="number", placeholder="Ex: 1.5", step=0.1, className="mb-3"),

            dbc.Label("Densidade máxima (ex: 1883):"),
            dbc.Input(id="densidade", type="number", placeholder="Ex: 1883", className="mb-3"),

            dbc.Label("Umidade ótima (%) (ex: 7,4):"),
            dbc.Input(id="umidade", type="text", placeholder="Ex: 7,4", className="mb-3"),

            dbc.Button("Gerar Ensaios", id="gerar", className="mt-3 w-100", color="primary"),
        ], md=6),
    ]),

    html.Hr(),
    html.Div(id="output")
], fluid=True)

# ==== Callback ====

@app.callback(
    Output("output", "children"),
    Input("gerar", "n_clicks"),
    State("tipo-ensaio", "value"),
    State("qtd", "value"),
    State("peso", "value"),
    State("volume", "value"),
    State("densidade", "value"),
    State("umidade", "value")
)
def gerar_ensaios(n, tipo, qtd, peso_cilindro, volume_cilindro, densidade_raw, umidade_raw):
    if not all([n, tipo, qtd, peso_cilindro, volume_cilindro, densidade_raw, umidade_raw]):
        return dbc.Alert("⚠️ Preencha todos os campos corretamente.", color="danger")

    try:
        densidade_maxima = float(densidade_raw) / 1000
        umidade_hot = float(str(umidade_raw).replace(",", "."))
    except ValueError:
        return dbc.Alert("⚠️ Valores inválidos. Verifique a densidade e a umidade.", color="danger")

    umidades = gerar_umidades(umidade_hot, qtd)
    ensaios = []

    for i in range(qtd):
        umidade = umidades[i]
        grau = gerar_grau_compactacao(tipo)

        dens_sec = (grau * densidade_maxima) / 100
        dens_umid = ((100 + umidade) * dens_sec) / 100
        volume_cm3 = volume_cilindro * 1000
        peso_solo = dens_umid * volume_cm3
        peso_total = peso_solo + peso_cilindro
        delta_umid = round(umidade - umidade_hot, 2)

        bloco = dbc.Card([
            dbc.CardBody([
                html.H5(f"🔹 Ensaio {i+1:02}", className="mb-3"),
                html.P(f"- **Peso do Cilindro + Solo:** {int(round(peso_total))} g"),
                html.P(f"- **Peso do Solo:** {int(round(peso_solo))} g"),
                html.P(f"- **Densidade Úmida:** {dens_umid:.3f} g/cm³"),
                html.P(f"- **Umidade:** {umidade:.1f} %"),
                html.P(f"- **Densidade Seca:** {dens_sec:.3f} g/cm³"),
                html.P(f"- **Grau de Compactação:** {grau:.1f} %"),
                html.P(f"- **Δ Umidade:** {delta_umid:.1f}"),
            ])
        ], className="mb-3 shadow-sm")

        ensaios.append(bloco)

    return [dbc.Alert("✅ Ensaios gerados com sucesso!", color="success")] + ensaios

# ==== Execução ====

if __name__ == "__main__":
    app.run_server(debug=True)
