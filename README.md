# FocusFlow

**FocusFlow** é um chatbot desenvolvido para os alunos da disciplina de Multimeios Didáticos do IFSP São João da Boa Vista. Utilizando técnicas avançadas de Inteligência Artificial e modelos da OpenAI, o chatbot fornece respostas automáticas sobre o conteúdo da disciplina e informações sobre datas importantes, como provas, tarefas e projetos.

## 📚 **Objetivo do Projeto**

O FocusFlow tem como objetivo auxiliar os alunos na interação com o conteúdo da disciplina de forma intuitiva e eficiente. O chatbot oferece suporte para consultas sobre tópicos de aula, avisos, lembretes e outras informações úteis para o sucesso acadêmico.

## 🚀 **Funcionalidades Principais**

- **Respostas automáticas** sobre conteúdos de Cálculo e Multimeios Didáticos.
- **Notificações e lembretes** sobre datas de provas, entregas de tarefas e projetos.
- **Consulta sobre tópicos específicos da disciplina**, incluindo exercícios resolvidos e conceitos teóricos.
- **Integração com modelos da OpenAI** (embedding-small-3 e gpt4o-mini) para processamento e geração de respostas.

## 🛠️ **Tecnologias Utilizadas**

- **Python 3.10+**
- **FastAPI**: Framework para criação de APIs rápidas e escaláveis.
- **OpenAI GPT Models**: Utilizados para geração de respostas e embeddings.
- **Supabase**: Armazenamento de dados.
- **Pydantic Settings**: Para configuração de variáveis de ambiente.
- **Streamlit**: Interface para o painel administrativo.
- **PyTorch**: Framework para cálculos numéricos e aprendizado de máquina.

## 📦 **Estrutura do Projeto**

```plaintext
FocusFlow/
│
├── src/
│   ├── agents/                 # Agentes que lidam com diferentes funcionalidades do chatbot
│   ├── services/               # Serviços utilizados pelo chatbot (ex: integração com IA)
│   ├── configs/                # Configurações do projeto
│   ├── pages/                  # Páginas da interface do usuário
│   ├── pages/fragments/        # Fragmentos reutilizáveis de UI
│   └── utils/                  # Utilitários gerais do projeto
│
├── requirements.txt            # Lista de dependências do projeto
│
└── README.md                   # Documentação do projeto
```

## 📥 **Instalação e Configuração**

### **Pré-requisitos**

- Python 3.10+
- pip (Python package installer)

### **Passo a Passo de Instalação**

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/focusflow.git
   cd focusflow
   ```

2. **Crie e ative um ambiente virtual (recomendado):**

   ```bash
   python -m venv env
   source env/bin/activate  # Para Linux/Mac
   env\Scripts\activate     # Para Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   - Defina suas chaves de API no arquivo `.streamlit/secrets.toml` ou diretamente no código:
     ```bash
      # [general]
      openai_key = "sk-" 
      database_url = "postgresql://postgres.<PROJECT_ID>:<YOUR_PASSWORD>@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
      supabase_url = "https://<PROJECT_ID>.supabase.co"
      supabase_key = ""
     ```

## 🏃 **Executando o Servidor**

Para iniciar o servidor FastAPI e testar o chatbot:

```bash
streamlit run ./main.py
```