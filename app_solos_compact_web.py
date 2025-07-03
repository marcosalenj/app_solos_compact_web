import dash
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server  # Necessário para Render

app.layout = html.Div([
    html.H2("Simulador de Ensaio de Solos"),

    html.Label("Peso do cilindro (g):"),
    dcc.Input(id='peso', type='number', placeholder='Digite aqui...', style={'marginBottom': '20px'}),

    html.Label("Volume do cilindro (L):"),
    dcc.Input(id='volume', type='number', placeholder='Digite aqui...', style={'marginBottom': '20px'}),

    html.Br(),
    html.Div(id='resultado')
])

@app.callback(
    Output('resultado', 'children'),
    Input('peso', 'value')
)
def atualizar_saida(peso):
    if peso is None:
        return "Digite o peso do cilindro."
    return f"Peso inserido: {peso} g"

if __name__ == '__main__':
    app.run_server(debug=True)
