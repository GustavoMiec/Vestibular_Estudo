import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Inicializa estados
if 'tabela_revisao' not in st.session_state:
    st.session_state.tabela_revisao = []
if 'mensagem_alerta' not in st.session_state:
    st.session_state.mensagem_alerta = None
if 'tipo_alerta' not in st.session_state:
    st.session_state.tipo_alerta = None
if 'remover_idx' not in st.session_state:
    st.session_state.remover_idx = None
if 'limpar' not in st.session_state:
    st.session_state.limpar = False
if 'importado' not in st.session_state:
    st.session_state.importado = False

def calcular_prioridade(materias):
    prioridade_map = {1: 3, 2: 2, 3: 1, 4: 0.5}
    for materia in materias:
        materia['Percentual Erro'] = (materia['Erros'] / materia['Total Questões']) * 100
        peso = prioridade_map.get(materia['Categoria'], 1)
        materia['Prioridade'] = materia['Percentual Erro'] * peso
    return sorted(materias, key=lambda x: x['Prioridade'], reverse=True)

def gerar_plano_revisao(materias):
    hoje = datetime.date.today()
    espacamentos = [1, 3, 7, 90]
    for i, materia in enumerate(materias):
        data_base = hoje + datetime.timedelta(days=i)
        materia['Revisões'] = [str(data_base + datetime.timedelta(days=d)) for d in espacamentos]
    return materias

def salvar_csv():
    df = pd.DataFrame(st.session_state.tabela_revisao)
    return df.to_csv(index=False).encode('utf-8')

def importar_csv(uploaded_file):
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Revisões' not in df.columns:
            materias = df.to_dict(orient='records')
            materias = gerar_plano_revisao(materias)
            df = pd.DataFrame(materias)
        st.session_state.tabela_revisao = df.to_dict(orient='records')
        st.session_state.mensagem_alerta = "Arquivo CSV importado com sucesso!"
        st.session_state.tipo_alerta = "success"
        st.session_state.importado = True

# Título
st.title("📘 Plano de Revisão de Matérias")

# Formulário para adicionar matéria
with st.form("form_add"):
    nome = st.text_input("Matéria")
    total = st.number_input("Total Questões", min_value=1, step=1)
    erros = st.number_input("Erros", min_value=0, step=1)
    categoria = st.selectbox("Categoria", options=[1, 2, 3, 4], format_func=lambda x: {
        1: "1 - Muito Importante",
        2: "2 - Importante",
        3: "3 - Menos Prioritário",
        4: "4 - Relativo"
    }[x])
    submitted = st.form_submit_button("Adicionar Matéria")

if submitted:
    if erros <= total and nome.strip():
        st.session_state.tabela_revisao.append({
            'Matéria': nome.strip(),
            'Total Questões': total,
            'Erros': erros,
            'Categoria': categoria
        })
        st.session_state.mensagem_alerta = f"Matéria '{nome}' adicionada com sucesso!"
        st.session_state.tipo_alerta = "success"
    else:
        st.session_state.mensagem_alerta = "Erro: Verifique os dados inseridos."
        st.session_state.tipo_alerta = "error"

# Mensagem depois da ação — mostra aqui, no lugar certo, só se tiver mensagem
if st.session_state.mensagem_alerta:
    if st.session_state.tipo_alerta == "success":
        st.success(st.session_state.mensagem_alerta)
    elif st.session_state.tipo_alerta == "error":
        st.error(st.session_state.mensagem_alerta)

# Remoção de matéria
if st.session_state.remover_idx is not None:
    idx = st.session_state.remover_idx
    if 0 <= idx < len(st.session_state.tabela_revisao):
        removida = st.session_state.tabela_revisao.pop(idx)
        st.session_state.mensagem_alerta = f"Matéria '{removida['Matéria']}' removida com sucesso!"
        st.session_state.tipo_alerta = "success"
    st.session_state.remover_idx = None

# Limpar tudo
if st.session_state.limpar:
    st.session_state.tabela_revisao = []
    st.session_state.mensagem_alerta = "Tabela limpa com sucesso!"
    st.session_state.tipo_alerta = "success"
    st.session_state.limpar = False

# Mostrar tabela e botões só se tiver dados
if st.session_state.tabela_revisao:
    materias = calcular_prioridade(st.session_state.tabela_revisao)
    materias = gerar_plano_revisao(materias)
    df = pd.DataFrame(materias)
    st.dataframe(df, use_container_width=True)

    st.markdown("### Remover Matéria")
    for i, row in df.iterrows():
        if st.button(f"Remover {row['Matéria']}", key=f"remover_{i}"):
            st.session_state.remover_idx = i

    st.markdown("### Prioridade das Matérias")
    fig, ax = plt.subplots()
    ax.barh(df['Matéria'], df['Prioridade'], color='skyblue')
    ax.invert_yaxis()
    ax.set_xlabel("Prioridade")
    ax.set_title("Gráfico de Priorização")
    st.pyplot(fig)

    if st.button("🧹 Limpar Tudo"):
        st.session_state.limpar = True

# Download CSV
csv = salvar_csv()
st.download_button(
    label="💾 Baixar CSV",
    data=csv,
    file_name='plano_revisao.csv',
    mime='text/csv',
)

# Upload CSV
uploaded_file = st.file_uploader("📤 Importar CSV", type=['csv'])
if uploaded_file:
    importar_csv(uploaded_file)
