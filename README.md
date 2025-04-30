# Gerenciador de Tarefas

Este é um gerenciador de tarefas simples desenvolvido em Flask. Ele permite que os usuários adicionem, editem, excluam e visualizem tarefas, além de enviar lembretes por e-mail para tarefas com vencimento próximo.

## Pré-requisitos

Antes de começar, você precisará ter o seguinte instalado em sua máquina:

- Python 3.x
- pip (gerenciador de pacotes do Python)

## Passo a Passo para Instalação e Execução

### 1. Clonar o Repositório

Primeiro, clone o repositório do gerenciador de tarefas para sua máquina local. Abra o terminal e execute:

```bash
git clone https://github.com/Trincademes/gerenciador_tarefas.git
cd gerenciador_tarefas
```
##
### 2. Criar um Ambiente Virtual

É uma boa prática usar um ambiente virtual para gerenciar as dependências do seu projeto. Para criar um ambiente virtual, execute:

```bash
python -m venv venv
```
##
#### No Windows:

```bash
venv\Scripts\activate
```
##
#### No macOS/Linux:

```bash
source venv/bin/activate
```
##
### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências necessárias. Execute o seguinte comando:

```bash
pip install Flask Flask-SQLAlchemy Flask-Mail APScheduler
```
##
### 4. Configurar o E-mail

Para que o envio de e-mails funcione, você precisará configurar suas credenciais de e-mail no arquivo enviar_email.py. Abra o arquivo e substitua as seguintes linhas com suas informações:

```python
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'  # Substitua pelo seu e-mail
app.config['MAIL_PASSWORD'] = 'sua_senha_de_app'  # Senha de app gerada
app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@gmail.com'  # Substitua pelo seu e-mail
```
Observação: Para usar o Gmail, você precisará gerar uma senha de aplicativo. Siga as instruções aqui para gerar uma senha de aplicativo:  [Gerar Senha de App - Google.](https://support.google.com/accounts/answer/185833?hl=pt-BR)
##
### 5. Criar o Banco de Dados

Antes de executar o aplicativo, você precisa criar o banco de dados. No terminal, execute o seguinte comando no Python shell:

```bash
python
```
##
Em seguida, execute os seguintes comandos para criar as tabelas no banco de dados:

```python
from app import db
db.create_all()
exit()
```
##
### 6. Executar o Aplicativo

Agora você está pronto para executar o aplicativo. No terminal, execute:

```bash
python app.py
```

O aplicativo será iniciado e você verá uma mensagem indicando que ele está rodando. Por padrão, ele estará disponível em http://127.0.0.1:5000/.

##
### 7. Acessar o Gerenciador de Tarefas

Abra seu navegador e acesse http://127.0.0.1:5000/. Você verá a interface do gerenciador de tarefas, onde poderá adicionar, editar e excluir tarefas.

##
### 8. Enviar E-mails
Para enviar e-mails com as tarefas, você pode acessar a rota /enviar_email no seu navegador. Isso enviará um e-mail com a lista de tarefas.# lusitana
