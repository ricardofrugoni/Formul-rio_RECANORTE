import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIGURAÇÕES ===
EMAIL_DESTINO = "ricardo.gsse@gmail.com"

st.set_page_config(page_title="Questionário Recanorte", layout="centered")
st.image("a292de41-0aae-4c0d-943f-4d78c5d5c5fd.png", width=120)
st.title("Questionário - RECANORTE")
st.markdown("""
### Este questionário tem como finalidade pesquisa para o curso de Administração da PUC Minas.  
Os dados serão tratados dentro das legalidades exigidas pela **Lei Geral de Proteção de Dados (LGPD)**.
""")

# === IDENTIFICAÇÃO ===
tipo_pessoa = st.radio("Você é Pessoa Física ou Jurídica?", ["Pessoa Física", "Pessoa Jurídica"], horizontal=True)

respostas = {}

# === PERGUNTAS EM COMUM ===
respostas["Conheceu como"] = st.selectbox("Como você conheceu a empresa RECANORTE?", ["Propaganda", "Internet", "Recomendação", "Sinalização e localização da loja", "Outros"])
respostas["Por que frequenta"] = st.multiselect("Por que você utiliza os serviços da RECANORTE?", ["Localização", "Qualidade e variedade", "Serviços de qualidade", "Prazo menor de entrega", "Preços competitivos", "Outros"])
respostas["Tempo como cliente"] = st.radio("Há quanto tempo você é cliente da RECANORTE?", ["Menos de 1 ano", "1 a 3 anos", "3 a 5 anos", "Mais que 5 anos"])

# === PESSOA FÍSICA ===
if tipo_pessoa == "Pessoa Física":
    respostas["Serviços contratados"] = st.multiselect("Que tipo de serviços costuma contratar?", ["Reforma de Pneus", "Conserto de Pneus", "Reconstrução de Pneus", "Outros"])
    respostas["Segmento"] = st.selectbox("Qual o segmento do seu negócio?", ["Transporte", "Mineração", "Construção", "Agrícola", "Industrial"])
    respostas["Gasto anual"] = st.radio("Quanto costuma gastar anualmente com recapagem?", ["R$ 100 a 1.000", "R$ 1.000 a 10.000", "Acima de 10.000"])
    respostas["Concorrentes"] = st.text_area("Cite as principais empresas do mesmo segmento que você utiliza")
    respostas["Motivos uso concorrentes"] = st.multiselect("Por que você utiliza essas empresas?", ["Localização", "Qualidade", "Prazo", "Preços competitivos", "Outros"])
    respostas["NPS"] = st.slider("De 0 a 10, quanto você indicaria a RECANORTE para um amigo?", 0, 10)
    respostas["Sugestões"] = st.text_area("Sugestões de melhorias")
    respostas["Faixa etária"] = st.radio("Qual sua faixa etária?", ["Até 25", "25 a 35", "36 a 45", "46 a 65", "Acima de 65"])
    respostas["Gênero"] = st.radio("Gênero", ["Feminino", "Masculino"])
    respostas["Bairro"] = st.text_input("Bairro/Cidade")
    respostas["Estado civil"] = st.selectbox("Estado civil", ["Solteiro", "Casado", "Separado", "Viúvo"])
    respostas["Renda"] = st.radio("Rendimento familiar", ["Menos de R$ 3.000", "R$ 3.000 a 5.000", "R$ 5.000 a 10.000", "R$ 10.000 a 20.000", "Acima de R$ 20.000"])

# === PESSOA JURÍDICA ===
elif tipo_pessoa == "Pessoa Jurídica":
    respostas["Serviços contratados"] = st.multiselect("Que tipo de produtos/serviços consome?", ["Conserto", "Reconstrução", "Reforma", "Outros"])
    respostas["Segmento"] = st.selectbox("Em qual segmento você utiliza nossos produtos?", ["Transporte", "Mineração", "Construção", "Agrícola", "Industrial"])
    respostas["Frequência de compra"] = st.radio("Com que frequência realiza pedidos?", ["1x por semana", "2-3x por semana", "1x ao mês", "Mais de 2x por mês", "De vez em quando"])
    respostas["Gasto médio"] = st.radio("Quanto costuma gastar com empresas como a RECANORTE?", ["R$ 1.000 a 3.000", "R$ 3.000 a 5.000", "Acima de R$ 5.000"])
    respostas["Concorrentes"] = st.text_area("Cite concorrentes que você utiliza")
    respostas["Motivos uso concorrentes"] = st.multiselect("Por que utiliza essas empresas?", ["Localização", "Qualidade", "Preços", "Outros"])
    respostas["NPS"] = st.slider("De 0 a 10, quanto você indicaria a RECANORTE a outro empreendedor?", 0, 10)
    respostas["Sugestões"] = st.text_area("Sugestões de melhoria")
    respostas["Funcionários"] = st.radio("Quantidade de funcionários da sua empresa", ["Até 5", "6 a 10", "11 a 50", "51 a 100", "Acima de 100"])
    respostas["Ramo da empresa"] = st.text_input("Ramo de atividade da empresa")
    st.markdown("**Avalie os itens abaixo de 1 (Péssimo) a 5 (Excelente):**")
    for item in ["Qualidade", "Preço", "Condições de pagamento", "Prazo de entrega", "Variedade", "Atendimento vendas", "Pós-venda"]:
        respostas[f"Avaliação: {item}"] = st.slider(item, 1, 5, 3)

# === ENVIO ===
if st.button("Enviar respostas"):
    corpo_email = f"Tipo de Pessoa: {tipo_pessoa}\n\n"
    for k, v in respostas.items():
        corpo_email += f"{k}: {v}\n"

    msg = MIMEMultipart()
    msg['From'] = "seu_email@gmail.com"
    msg['To'] = EMAIL_DESTINO
    msg['Subject'] = "Nova resposta - Questionário RECANORTE"
    msg.attach(MIMEText(corpo_email, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("ricardo.gsse@gmail.com", "faivmhifbzmunplw")
        server.send_message(msg)
        server.quit()
        st.success("Respostas enviadas com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar: {e}")
