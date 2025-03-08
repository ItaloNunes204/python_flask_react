create schema TEFT;
commit;

create table TEFT.membro(
	email varchar(150) NOT NULL,
	senha varchar(32) NOT NULL,
	nome varchar(150),
	subgrupo varchar(150),
	primary key(email)
);
commit;

create table TEFT.piloto(
id_piloto int auto_increment NOT NULL,
temporada varchar(9) NOT NULL, 
n_testes int, 
email varchar(150) NOT NULL, 
kms float,
primary key(id_piloto),
foreign key(email) references TEFT.membro(email)
);
commit;

create table TEFT.circuito(
id_circuito int auto_increment NOT NULL,
nome varchar(150) NOT NULL,
tempo_descolcamento float,
KM float,
curvas int,
cones int,
local varchar(150),
primary key(id_circuito)
);
commit;

create table TEFT.prototipo(
id_prototipo int auto_increment NOT NULL,
nome varchar(150) NOT NULL,
ano_fabricacao varchar(4) NOT NULL,
status varchar(100) NOT NULL,
peso float,
temporada varchar(50) NOT NULL,
primary key(id_prototipo) 
);
commit;

create table TEFT.metodologia(
id_metodologia int auto_increment NOT NULL,
objetivo text  NOT NULL,
N_pessoas int,
subgrupo varchar(150),
procedimento text  NOT NULL,
N_voltas float  NOT NULL,
primary key(id_metodologia)
);
commit;

create table TEFT.testes(
N_teste int auto_increment NOT NULL,
pilotos varchar(100) NOT NULL,
id_objetivos varchar(100) NOT NULL,
N_voltas float,
inicio time NOT NULL,
fim time NOT NULL,
almoco boolean,
data date NOT NULL,
id_prototipo int NOT NULL,
id_circuito int NOT NULL,
primary key(N_teste),
foreign key(id_prototipo) references TEFT.prototipo(id_prototipo),
foreign key(id_circuito) references TEFT.circuito(id_circuito)
);
commit;

create table TEFT.logs(
vazao_de_bancada_a text,
wps text,
temperatura_oleo text,
pressao_embreagem text,
id_teste int NOT NULL,
tps text,
tempo text,
velo_rte text,
amortecedor_te text,
forca_g_long text,
amortecedor_de text,
tensao_bateria text,
velo_rtd text,
pressao_oleo text,
temperatura_ar text,
temperatura_motor text,
pressao_diferencial_combustivel text,
sonda_geral text,
pressao_freio text,
rpm text,
marcha text,
velo_rfe text,
id_logs int auto_increment NOT NULL,
link text,
descricao text,
forca_g_lateral text,
id_piloto int NOT NULL,
primary key(id_logs),
foreign key(id_piloto) references TEFT.piloto(id_piloto),
foreign key(id_teste) references TEFT.testes(N_teste)
);
commit;

create table TEFT.fator_externo(
id_fator_externo int auto_increment NOT NULL,
temp_pista float,
id_teste int NOT NULL,
hora time,
clima varchar(100),
temperatura float,
primary key(id_fator_externo),
id_log int,
foreign key(id_log) references TEFT.logs(id_logs),
foreign key(id_teste) references TEFT.testes(N_teste)
);
commit;

create table TEFT.grafico(
id_grafico int auto_increment NOT NULL,
id_log int NOT NULL,
tipo_grafico varchar(150) NOT NULL,
descricao text,
primary key(id_grafico),
foreign key(id_log) references TEFT.logs(id_logs)
);
commit;

create table TEFT.marcacao(
id_marcacao int auto_increment NOT NULL,
x float,
y float,
cor varchar(100),
raio float,
id_grafico int,
primary key(id_marcacao),
foreign key(id_grafico) references TEFT.grafico(id_grafico)
);
commit;

create table TEFT.comentario(
id_comentario int auto_increment NOT NULL,
id_grafico int NOT NULL,
id_marcacao int NOT NULL,
comentario text,
id_teste int NOT NULL,
primary key(id_comentario),
foreign key(id_grafico) references TEFT.grafico(id_grafico),
foreign key(id_marcacao) references TEFT.marcacao(id_marcacao),
foreign key(id_teste) references TEFT.testes(N_teste)
);
commit;

create table TEFT.sensores(
id_sensor int auto_increment NOT NULL,
id_prototipo int NOT NULL,
nome varchar(100),
funcionamento boolean,
id_teste int NOT NULL,
informacao text,
primary key(id_sensor),
foreign key(id_prototipo) references TEFT.prototipo(id_prototipo),
foreign key(id_teste) references TEFT.testes(N_teste)
);
commit;

create table TEFT.presenca(
id_presenca int auto_increment NOT NULL,
id_membro varchar(150) NOT NULL,
funcao text,
fim datetime,
inicio datetime,
id_teste int NOT NULL,
primary key(id_presenca),
foreign key(id_membro) references TEFT.membro(email),
foreign key(id_teste) references TEFT.testes(N_teste)
);
commit;

create table TEFT.transmissao(
id_configuracao int auto_increment NOT NULL,
id_teste int NOT NULL,
id_prototipo int NOT NULL,
primary key(id_configuracao),
foreign key(id_teste) references TEFT.testes(N_teste),
foreign key(id_prototipo) references TEFT.prototipo(id_prototipo)
);
commit;

create table TEFT.freio(
id_configuracao int auto_increment NOT NULL,
id_teste int NOT NULL,
id_prototipo int NOT NULL,
primary key(id_configuracao),
foreign key(id_teste) references TEFT.testes(N_teste),
foreign key(id_prototipo) references TEFT.prototipo(id_prototipo)
);
commit;

create table TEFT.chassi(
id_configuracao int auto_increment NOT NULL,
id_teste int NOT NULL,
id_prototipo int NOT NULL,
primary key(id_configuracao),
foreign key(id_teste) references TEFT.testes(N_teste),
foreign key(id_prototipo) references TEFT.prototipo(id_prototipo)
);
commit;

create table TEFT.aerodinamica(
id_configuracao int auto_increment NOT NULL,
id_teste int NOT NULL,
id_prototipo int NOT NULL,
primary key(id_configuracao),
foreign key(id_teste) references TEFT.testes(N_teste),
foreign key(id_prototipo) references TEFT.prototipo(id_prototipo)
);
commit;

create table TEFT.dinamica(
id_configuracao int auto_increment NOT NULL,
id_teste int NOT NULL,
id_prototipo int NOT NULL,
primary key(id_configuracao),
foreign key(id_teste) references TEFT.testes(N_teste),
foreign key(id_prototipo) references TEFT.prototipo(id_prototipo)
);
commit;

create table TEFT.motor(
id_configuracao int auto_increment NOT NULL,
id_teste int NOT NULL,
id_prototipo int NOT NULL,
primary key(id_configuracao),
foreign key(id_teste) references TEFT.testes(N_teste),
foreign key(id_prototipo) references TEFT.prototipo(id_prototipo)
);
commit;
