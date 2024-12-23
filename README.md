Aqui está um esboço para o arquivo README do seu projeto de análise de partidas de futebol, destacando as principais funcionalidades e etapas para configuração do ambiente:

```markdown
# Análise de Partidas de Futebol

Este repositório contém o código para uma aplicação de análise de partidas de futebol, desenvolvida com duas abordagens distintas: uma API usando FastAPI e LLM e uma interface interativa usando Streamlit e LangChain.

## Funcionalidades

- **Perfil de Jogador**: Gera estatísticas detalhadas e análises sobre jogadores de uma partida.
- **Sumarização de Eventos**: Transforma os eventos da partida em um resumo textual descritivo.
- **Narração Personalizada**: Cria textos de narração baseados nos eventos da partida, com estilo adaptável conforme a preferência do usuário.

## Configuração do Ambiente

### Pré-requisitos

- Python 3.8+
- pip

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/danimoreira90/Data_Driven_Apps_AT.git
   cd Data_Driven_Apps_AT
   ```


   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Uso

- **API FastAPI + LLM**:
  Execute o servidor FastAPI:
  ```bash
  uvicorn main:app --reload
  ```
  Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

- **Streamlit + LangChain**:
  Inicie a interface Streamlit:
  ```bash
  streamlit run app.py
  ```

## Contribuição

Contribuições são bem-vindas! Para contribuir, por favor abra um pull request para discussão das mudanças propostas.


