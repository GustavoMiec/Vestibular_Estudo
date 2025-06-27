# 🧠 Plano de Revisão de Matérias

Aplicativo web para organizar e priorizar revisões de estudos baseado em desempenho e importância de cada matéria. Ideal para quem está se preparando para vestibulares ou provas importantes.

🔗 **Acesse o aplicativo online**:  
[https://vestibularestudo-4jo7wnohextbdmxmtyax2y.streamlit.app/](https://vestibularestudo-4jo7wnohextbdmxmtyax2y.streamlit.app/)

---

## ✨ Funcionalidades

- ✅ Adicionar matérias com total de questões, erros e importância.
- 📊 Cálculo automático da prioridade com base em percentual de erro e categoria.
- 📆 Geração de datas de revisão distribuídas no tempo.
- 📉 Visualização gráfica da prioridade das matérias.
- 🗑 Remoção individual ou geral de matérias.
- 💾 Exportação e importação de planos em CSV.

---

## 📐 Como funciona

A prioridade de cada matéria é calculada com base na fórmula:

```
Prioridade = (Erros / Total de Questões) * 100 * Peso da Categoria
```

Onde o **peso da categoria** é:
- 1️⃣ Muito Importante → 3.0  
- 2️⃣ Importante → 2.0  
- 3️⃣ Menos Prioritário → 1.0  
- 4️⃣ Relativo → 0.5

Após o cálculo, são geradas automaticamente **3 datas de revisão** espaçadas no tempo para cada matéria.

---

## 🖼 Exemplo de uso

1. Preencha os campos com as informações da matéria.
2. Clique em **Adicionar Matéria**.
3. Veja sua matéria aparecer na tabela com datas de revisão e prioridade.
4. Visualize o gráfico com as prioridades.
5. Baixe seu plano de revisão ou importe um existente.

---

## 🛠 Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

---

## 📁 Execução local (opcional)

Se quiser rodar localmente:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
pip install -r requirements.txt
streamlit run vestibular.py
```

Crie um arquivo `requirements.txt` com:

```
streamlit
pandas
matplotlib
```

---

## 🙌 Contribuições

Sinta-se à vontade para abrir issues ou pull requests com melhorias, correções ou sugestões!

---

## 📬 Contato

Desenvolvido por **Gustavo Costa**  
📧 gustavocostamiec@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/gustavo-costa-mieczkowsky-56b210255/)
