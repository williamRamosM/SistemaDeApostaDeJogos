CREATE TABLE IF NOT EXISTS Usuarios(
    ID     SERIAL PRIMARY KEY,
    name   VARCHAR(150) NOT NULL,
    email  VARCHAR(320) NOT NULL,
    cpf    CHAR(11) NOT NULL UNIQUE,
    date_birth DATE NOT NULL,
    login VARCHAR(30) NOT NULL UNIQUE,
    passworld  CHAR(8) NOT NULL,
    points INT DECIMAL(10,2) DEFAULT 100 NOT NULL,
    CONSTRAINT chk_email_format
      CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')
  )

  CREATE TABLE IF NO EXISTS Bets(
    ID SERIAL PRIMARY KEY,
    points DECIMAL(10,2),
    user_id INT,
    game_id INT,
    odds DECIMAL(5,2),
    FOREIGN KEY (user_id) REFERENCES Usuarios(ID),
    FOREIGN KEY (game_id) REFERENCES Jogos(ID)
  )

  CREATE TABLE IF NOT EXISTS Jogos(
    ID     SERIAL PRIMARY KEY,
    team_one INT NOT NULL,
    team_two INT NOT NULL,
    date_game TIMESTAMP NOT NULL,
    status BOOLEAN DEFAULT FALSE NOT NULL
  )

  -- OBS:
  -- Isso esta colocado em um banco de dados em nuvem chamado de Supabase
  -- coloquei aqui o que foi adicionado nele, pois acho que nao tem como liberar o acesso dele.


  -- LEMBRETE (para -> WILL)
  -- DELETAR ISSO POIS NAO PRECISO DESSAS INFORMAÇOES AQUI.