CREATE TABLE Estudantes(
    matricula int PRIMARY KEY,
    is_adm boolean,
    nome varchar(200),
    email varchar(200),
    curso varchar(200),
    senha varchar(200),
    imagem bytea
);

CREATE TABLE Departamentos(
    codigo int PRIMARY KEY,
    nome varchar(200)
);

CREATE TABLE Professores(
    id int PRIMARY KEY,
    nome varchar(200),
    fk_cod_dep int,
    FOREIGN KEY (fk_cod_dep) REFERENCES Departamentos(codigo) ON DELETE CASCADE
);

CREATE TABLE Disciplinas(
    codigo varchar(15) PRIMARY KEY,
    nome varchar(200),
    fk_cod_dep int,
    FOREIGN KEY (fk_cod_dep) REFERENCES Departamentos(codigo) ON DELETE CASCADE
);

CREATE TABLE Turmas(
    id int PRIMARY KEY,
    turma varchar(200),
    periodo varchar(200),
    vagas_ocupadas int,
    total_vagas int,
    local varchar(200),
    horario varchar(350),
    fk_professor int,
    fk_cod_disciplina varchar(15),
    fk_cod_dep int,
    FOREIGN KEY (fk_cod_disciplina) REFERENCES Disciplinas (codigo) ON DELETE CASCADE,
    FOREIGN KEY (fk_cod_dep) REFERENCES Departamentos (codigo) ON DELETE CASCADE,
    FOREIGN KEY (fk_professor) REFERENCES Professores (id) ON DELETE CASCADE
);

CREATE TABLE Avaliacoes(
    id int PRIMARY KEY,
    comentario varchar(200),
    is_turma boolean,
    fk_matricula int,
    fk_turma int,
    fk_professor int,
    nota int,
    data date,
    FOREIGN KEY (fk_matricula) REFERENCES Estudantes (matricula) ON DELETE CASCADE,
    FOREIGN KEY (fk_turma) REFERENCES Turmas (id) ON DELETE CASCADE,
    FOREIGN KEY (fk_professor) REFERENCES Professores (id) ON DELETE CASCADE
);

CREATE TABLE Denuncias(
    id int PRIMARY KEY,
    fk_id_avaliacao int,
    comentario varchar(500),
    FOREIGN KEY (fk_id_avaliacao) REFERENCES Avaliacoes (id) ON DELETE CASCADE
);

CREATE VIEW Notas_professor AS 
    SELECT fk_professor, nota FROM Avaliacoes WHERE is_turma=false;

CREATE VIEW Notas_turmas AS 
    SELECT fk_turma, nota FROM Avaliacoes WHERE is_turma=true;

CREATE PROCEDURE AcaoDenuncia(
    option int,
	id_denuncia int,
    id_avaliacao int,
    matricula_in int
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF (option = 1) THEN
        -- Ignora a denuncia
        DELETE FROM Denuncias WHERE id = id_denuncia;
    ELSIF (option = 2) THEN
        -- Aceita a Denuncia
        DELETE FROM Denuncias WHERE id = id_denuncia;
        DELETE FROM Avaliacoes WHERE id = id_avaliacao;
    ELSIF (option = 3) THEN
        -- Deleta usuario
        DELETE FROM Denuncias WHERE id = id_denuncia;
        DELETE FROM Avaliacoes WHERE id = id_avaliacao;
        DELETE FROM Estudantes WHERE matricula = matricula_in;
    END IF;
END
$$;


CREATE PROCEDURE inserir_avaliacoes(
    next_val int,
    comentario varchar, 
    matricula int, 
    turma int,
    professor int, 
    nota int,
    data date
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO Avaliacoes (id, comentario, is_turma, fk_turma, fk_matricula, nota, data) 
  VALUES (next_val, comentario, true, turma, matricula, nota, data);
  INSERT INTO Avaliacoes (id, comentario, is_turma, fk_matricula, fk_professor, nota, data) 
  VALUES (next_val+1, comentario, false, matricula, professor, nota, data);
END;
$$;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO PUBLIC;