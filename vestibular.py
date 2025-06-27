import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Inicializa a lista no estado da sessão
if 'tabela_revisao' not in st.session_state:
    st.session_state.tabela_revisao = []

def calcular_prioridade(materias):
    prioridade_map = {1: 3, 2: 2, 3: 1, 4: 0.5}
    for materia in materias:
        materia['Percentual Erro'] = (materia['Erros'] / materia['Total Questões']) * 100
        categoria_peso = prioridade_map.get(materia['Categoria'], 1)
        materia['Prioridade'] = materia['Percentual Erro'] * categoria_peso
    return sorted(materias, key=lambda x: x['Prioridade'], reverse=True)

def gerar_plano_revisao(materias):
    hoje = datetime.date.today()
    espacamentos = [1, 3, 7, 90]
    for i, materia in enumerate(materias):
        data_base = hoje + datetime.timedelta(days=i)  # Escalonando matérias
        materia['Revisões'] = [str(data_base + datetime.timedelta(days=delta)) for delta in espacamentos]
    return materias


def adicionar_materia(nome, total, erros, categoria):
    st.session_state.tabela_revisao.append({
        'Matéria': nome,
        'Total Questões': total,
        'Erros': erros,
        'Categoria': categoria
    })

def remover_materia(index):
    if 0 <= index < len(st.session_state.tabela_revisao):
        st.session_state.tabela_revisao.pop(index)

def salvar_csv():
    df = pd.DataFrame(st.session_state.tabela_revisao)
    return df.to_csv(index=False).encode('utf-8')

def importar_csv(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if 'Revisões' not in df.columns:
            materias = df.to_dict(orient='records')
            materias = gerar_plano_revisao(materias)
            df = pd.DataFrame(materias)
        st.session_state.tabela_revisao = df.to_dict(orient='records')

st.title("Plano de Revisão de Matérias")

with st.form("form_add"):
    nome = st.text_input("Matéria")
    total = st.number_input("Total Questões", min_value=1, step=1)
    erros = st.number_input("Erros", min_value=0, step=1)
    categoria = st.selectbox("Categoria",
                             options=[1, 2, 3, 4],
                             format_func=lambda x: {
                                 1: "1 - Muito Importante",
                                 2: "2 - Importante",
                                 3: "3 - Menos Prioritário",
                                 4: "4 - Relativo"
                             }[x])
    submitted = st.form_submit_button("Adicionar Matéria")

if submitted:
    if erros <= total and nome.strip():
        adicionar_materia(nome.strip(), total, erros, categoria)
        st.success(f"Matéria '{nome}' adicionada!")
    else:
        st.error("Erro: Verifique os dados inseridos.")

if st.session_state.tabela_revisao:
    materias = calcular_prioridade(st.session_state.tabela_revisao)
    materias = gerar_plano_revisao(materias)
    df = pd.DataFrame(materias)
    st.dataframe(df)

    for i, row in df.iterrows():
       if st.button(f"Remover {row['Matéria']}", key=f"remover_{i}"):
         remover_materia(i)
        


    fig, ax = plt.subplots()
    ax.barh(df['Matéria'], df['Prioridade'], color='skyblue')
    ax.invert_yaxis()
    ax.set_xlabel("Prioridade")
    ax.set_title("Prioridade das Matérias")
    st.pyplot(fig)

if st.button("Limpar Tudo"):
    st.session_state.tabela_revisao = []
    st.experimental_rerun()

csv = salvar_csv()
st.download_button(
    label="Salvar Plano de Revisão (CSV)",
    data=csv,
    file_name='plano_revisao.csv',
    mime='text/csv',
)

uploaded_file = st.file_uploader("Importar Plano de Revisão (CSV)", type=['csv'])
if uploaded_file is not None:
    importar_csv(uploaded_file)
    st.success("Arquivo importado com sucesso!")
    st.experimental_rerun()
