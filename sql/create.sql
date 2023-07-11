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
    FOREIGN KEY (fk_cod_dep) REFERENCES Departamentos(codigo)
);

CREATE TABLE Disciplinas(
    codigo varchar(15) PRIMARY KEY,
    nome varchar(200),
    fk_cod_dep int,
    FOREIGN KEY (fk_cod_dep) REFERENCES Departamentos(codigo)
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
    FOREIGN KEY (fk_cod_disciplina) REFERENCES Disciplinas (codigo),
    FOREIGN KEY (fk_cod_dep) REFERENCES Departamentos (codigo),
    FOREIGN KEY (fk_professor) REFERENCES Professores (id)
);

CREATE TABLE Avaliacoes(
    id int PRIMARY KEY,
    comentario varchar(200),
    is_turma boolean,
    fk_matricula int,
    fk_turma int,
    fk_professor varchar(200),
    nota int
);

CREATE TABLE Denuncias(
    id int PRIMARY KEY,
    fk_id_avaliacao int,
    comentario varchar(500)
);

GRANT ALL ON TABLE estudantes TO usuario;
GRANT ALL ON TABLE departamentos TO usuario;
GRANT ALL ON TABLE professores TO usuario;
GRANT ALL ON TABLE disciplinas TO usuario;
GRANT ALL ON TABLE turmas TO usuario;
GRANT ALL ON TABLE avaliacoes TO usuario;
GRANT ALL ON TABLE denuncias TO usuario;