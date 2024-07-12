# TMF - Artificial Intelligence

## Descrição

TMF - Artificial Intelligence é um aplicativo web de conversação AI, alimentado por Tauan, utilizando as bibliotecas Streamlit e LangChain. Este aplicativo permite que os usuários se registrem, façam login, conversem com a IA e gerem imagens com base em prompts fornecidos.

## Funcionalidades

1. **Login e Registro**:
   - Os usuários podem registrar-se com um email e senha.
   - Os usuários registrados podem fazer login com suas credenciais.

2. **Histórico de Conversas**:
   - Os usuários podem visualizar o histórico de suas conversas anteriores.
   - Os usuários têm a opção de limpar seu histórico de conversas.

3. **Chat com IA**:
   - Os usuários podem enviar mensagens e receber respostas da IA.
   - As conversas são salvas no perfil do usuário.

4. **Geração de Imagens**:
   - Os usuários podem gerar imagens com base em prompts de texto.
   - As imagens geradas são exibidas e salvas no histórico de conversas do usuário.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas listadas no arquivo `requirements.txt`:

    ```txt
    streamlit
    streamlit-option-menu
    langchain-core
    langchain-groq
    python-dotenv
    openai
    ```

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/Tauan0021/Intelig-ncia-Artificial-Particular.git
    cd Intelig-ncia-Artificial-Particular
    ```

2. Crie um ambiente virtual e ative-o:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Windows: venv\Scripts\activate
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` na raiz do projeto e adicione sua chave API da OpenAI:

    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Uso

Para iniciar o aplicativo Streamlit, execute o seguinte comando no terminal:

```bash

streamlit run app.py
```

## Estrutura do Projeto

```bash
Intelig-ncia-Artificial-Particular/
├── app.py
├── requirements.txt
├── .env
├── users.json
└── README.md
