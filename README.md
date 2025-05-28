# 💰 SRES - Sistema de Registro de Entradas e Saídas

Projeto full-stack desenvolvido em Django com o objetivo de gerenciar o fluxo financeiro (entradas e saídas) de igrejas e instituições similares.

## 🛠 Tecnologias Utilizadas

- Python 3
- Django
- HTML + Bootstrap
- JavaScript
- SQLite
- Sistema de sessões e autenticação nativa do Django

## 📦 Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/Victor-Drt/sres-full-stack.git
   cd sres-full-stack
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Crie o arquivo `.env` com a seguinte variável:

   ```dotenv
   SECRET_KEY=sua_chave_secreta
   ```

5. Rode as migrações:

   ```bash
   python manage.py migrate
   ```

6. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

## 👤 Autenticação

O sistema utiliza autenticação de usuários via Django nativamente. Para acessar as funcionalidades protegidas, é necessário criar uma conta e fazer login.

## ✍️ Observações

* Totalmente funcional, pronto para modificações e melhorias.
* Criado como projeto final da formação de **Backend com Django** da Alura.
* Banco de dados padrão: SQLite (pode ser alterado para PostgreSQL facilmente).

## 📸 Imagens (opcional)

Se desejar, adicione prints da interface aqui para ilustrar o funcionamento.

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para clonar, modificar e usar como quiser.
