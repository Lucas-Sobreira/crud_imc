import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.image("logo.png", width=200)

st.title("Avaliações de IMC (Índice de Massa Corporal)")

# Função auxiliar para exibir mensagens de erro detalhadas
def show_response_message(response):
    if response.status_code == 200:
        st.success("Operação realizada com sucesso!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                # Se o erro for uma lista, extraia as mensagens de cada erro
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Erro: {errors}")
                else:
                    # Caso contrário, mostre a mensagem de erro diretamente
                    st.error(f"Erro: {data['detail']}")
        except ValueError:
            st.error("Erro desconhecido. Não foi possível decodificar a resposta.")

# Adicionar avaliação
with st.expander("Adicionar nova avaliação"):
    with st.form("nova_avaliação"):
        name = st.text_input("Nome do paciente")
        wheight = st.number_input("Peso em kg (apenas números)", min_value=40.00, format="%f")
        height = st.number_input("Altura em metros (apenas números)", min_value=1.00, format="%f")
        client_email = st.text_input("Email do paciente")
        submit_button = st.form_submit_button("Adicionar Avaliação")

        if submit_button:
            response = requests.post(
                "http://backend:8000/avaliacoes/",
                json={
                    "name": name,
                    "wheight": wheight,
                    "height": height,
                    "imc": None, 
                    "result": None,
                    "client_email": client_email
                },
            )
            show_response_message(response)

# Visualizar Avaliações
with st.expander("Visualizar Avaliações"):
    if st.button("Exibir Todos os Avaliações"):
        response = requests.get("http://backend:8000/avaliacoes/")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame(product)

            df = df[
                [
                    "id",
                    "name",
                    "wheight",
                    "height",
                    "imc",
                    "result",
                    "client_email",
                    "refdate"
                ]
            ]

            # Exibe o DataFrame sem o índice
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Obter Detalhes de uma Avaliação
with st.expander("Obter Detalhes de uma Avaliação"):
    get_id = st.number_input("ID da Avaliação", min_value=1, format="%d")
    if st.button("Buscar Avaliação"):
        response = requests.get(f"http://backend:8000/avaliacoes/{get_id}")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame([product])

            df = df[
                [
                    "id",
                    "name",
                    "wheight",
                    "height",
                    "imc",
                    "result",
                    "client_email",
                    "refdate"
                ]
            ]

            # Exibe o DataFrame sem o índice
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Deletar avaliação
with st.expander("Deletar avaliação"):
    delete_id = st.number_input("ID da avaliação para Deletar", min_value=1, format="%d")
    if st.button("Deletar avaliação"):
        response = requests.delete(f"http://backend:8000/avaliacoes/{delete_id}")
        show_response_message(response)

# Atualizar avalição
with st.expander("Atualizar avaliação"):
    with st.form("update_avaliacao"):
        update_id = st.number_input("ID do avalição", min_value=1, format="%d")
        
        new_name = st.text_input("Novo Nome do Produto")
        new_wheight = st.number_input("Peso atualizado em kg", min_value=0.00, format="%f")
        new_height = st.number_input("Altura atualizada em metros", min_value=0.00, format="%f")
        new_email = st.text_input("Novo email do paciente")

        update_button = st.form_submit_button("Atualizar avaliação")

        if update_button:
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_wheight > 40.00:
                update_data["wheight"] = new_wheight
            if new_height > 1.00:
                update_data["height"] = new_height
            if new_email:
                update_data["client_email"] = new_email

            if update_data:
                response = requests.put(
                    f"http://backend:8000/avaliacoes/{update_id}", json=update_data
                )
                show_response_message(response)
            else:
                st.error("Nenhuma informação fornecida para atualização")