# Guia do Sistema de apostas

## Descrição
Esse seria um sistema de apostas que nao possui acesso a dinheiro real, mas utilizamos pontos para poder usar como saldo.
Ele possui uma segurança de nivel aceitavel tendo criptografia avançada e verificaçao de nomes (lista proibida).

## Requisitos

* Python 3.12+
* PostgresSQL (pondendo ser em modo online de sites)
* Necessita de uma chave (token) para poder acessar e conectar se com banco online.

## Instalação

(Os comandos indicados abaixo no tuturial de instalação precisara que sejam colocados no Prompt de comando ou CMD, se não sabe como acessar click win + R e digite cmd e click em enter)

1. Faça um clone do repositorio apartir do comando abaixo:
   git clone https://github.com/williamRamosM/SistemaDeApostaDeJogos.git

2. Instale as dependencias para o projeto funcionar corretamente, logo abaixo o comando:
    pip install -r requirement.txt

3. configure o banco de dados para poder rodar adequadamente,para ter a estrutura certa mais abaixo terá uma sessao chamada (Estrutura SQL).


## Como executar?

    Para executar o codigo rode a main com o seguinte comando. (Isso seria no terminal dentro do projeto)
    Comando: python main.py


## Tecnologias utilizadas para o sistema:

* Python (linguagem de programação)
* SQLModel
* certifi
* charset-normalizer
* idna
* psycopg2
* python-dotenv
* requests
* urllib3
* pydantic
* argon2-cffi
* validate-docbr

## Estrutura SQL

    CREATE TABLE IF NOT EXISTS usuarios(
        ID     SERIAL PRIMARY KEY,
        incremental_id INT DEFAULT 2 NOT NULL,
        name   VARCHAR(150) NOT NULL,
        email  VARCHAR(320) NOT NULL,
        cpf    CHAR(14) NOT NULL UNIQUE,
        date_birth DATE NOT NULL,
        login VARCHAR(30) NOT NULL UNIQUE,
        password TEXT NOT NULL,
        points DECIMAL(10,2) DEFAULT 100 NOT NULL,
        status boolean default TRUE NOT NULL,
        CONSTRAINT chk_email_format
        CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    );
    
    CREATE TABLE IF NOT EXISTS bets(
        ID SERIAL PRIMARY KEY,
        points DECIMAL(10,2),
        user_id INT,
        game_id INT,
        time_escolhido_id INT,
        odds DECIMAL(5,2),
        status VARCHAR(20) NOT NULL DEFAULT 'pendente',
        FOREIGN KEY (user_id) REFERENCES Usuarios(ID),
        FOREIGN KEY (game_id) REFERENCES Jogos(ID)
    );

    CREATE TABLE IF NOT EXISTS jogos(
        ID     SERIAL PRIMARY KEY,
        incremental_id INT NOT NULL,
        team_one INT NOT NULL,
        team_two INT NOT NULL,
        placar_one INT,
        placar_two INT,
        date_game TIMESTAMP NOT NULL,
        status BOOLEAN DEFAULT FALSE NOT NULL,
        jogo_iniciado BOOLEAN DEFAULT FALSE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS times(
        ID     SERIAL PRIMARY KEY,
        incremental_id INT NOT NULL,
        name VARCHAR(150) NOT NULL
    );

## O que devo ter no .env?

DATABASE_URL= "Aqui vai o link do banco"
PEPPER_SECRET = "Aqui voce vai colocar um codigo gerado"
TOKEN = 'Aqui vai colocar o token do seu banco online'
API_URL = "https://api.football-data.org/v4/competitions/WC/"

* Use esse cogigo no terminal para obter o codigo gerado (ele seá mais seguro)
    python -c "import secrets; print(secrets.token_hex(32))"