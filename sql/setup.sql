CREATE SCHEMA ski;

CREATE TYPE ski.grade_type AS ENUM ('kyu','dan');
CREATE TYPE ski.sides AS ENUM ('sx','frontal','dx');
CREATE TYPE ski.movements AS ENUM('Fwd','Still','Bkw');
CREATE TYPE ski.kata_series AS ENUM ('Heian','Tekki','Sentei');
CREATE TYPE ski.target AS ENUM('Jodan','Chudan','Gedan');
CREATE TYPE ski.waza_type AS ENUM('Uke','Uchi','Geri');
CREATE TYPE ski.embusen_points AS (
    x SMALLINT,
    y SMALLINT
);

CREATE TABLE ski.technics(
    id_technic SMALLSERIAL PRIMARY KEY,
    waza ski.waza_type,
    name VARCHAR(255) NOT NULL,
    -- aka VARCHAR(255) ,
    description TEXT,
    notes TEXT,
    resource_url TEXT,
    CONSTRAINT unique_technicname UNIQUE(name)
);

-- tabella spostamenti

CREATE TABLE ski.stands(
    id_stand SMALLSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    -- aka VARCHAR(255) ,
    description TEXT,
    illustration_url TEXT,
    notes TEXT
);

CREATE TABLE ski.grades(
    id_grade SMALLSERIAL PRIMARY KEY,
    gtype ski.grade_type NOT NULL,
    grade SMALLINT CHECK (grade BETWEEN 1 AND 10) NOT NULL ,
    CONSTRAINT unique_grade UNIQUE (gtype, grade)
);

CREATE TABLE ski.kihon_inventory(
    id_inventory SMALLSERIAL PRIMARY KEY,
    grade_id SMALLINT NOT NULL REFERENCES ski.grades(id_grade),
    number SMALLINT NOT NULL,
    CONSTRAINT unique_kihoninventory UNIQUE (grade_id, number)
);

CREATE TABLE ski.kihon_sequences(
    id_sequence SMALLSERIAL PRIMARY KEY,
    inventory_id SMALLSERIAL NOT NULL REFERENCES ski.kihon_inventory(id_inventory),
    seq_num SMALLINT NOT NULL,
    stand SMALLSERIAL NOT NULL REFERENCES ski.stands(id_stand),
    techinc SMALLSERIAL NOT NULL REFERENCES ski.technics(id_technic),
    gyaku bool,
    target_hgt VARCHAR(255) ,
    note TEXT ,
    resource_url TEXT,
    CONSTRAINT unique_kihonsequence UNIQUE (inventory_id, seq_num)
);

CREATE TABLE ski.kihon_tx(
    id_tx SMALLSERIAL PRIMARY KEY,
    from_seq SMALLINT NOT NULL REFERENCES ski.kihon_sequences(id_sequence),
    to_seq SMALLINT NOT NULL REFERENCES ski.kihon_sequences(id_sequence),
    --direction ski.sides ,
    --rotation SMALLINT ,
    movement ski.movements ,
    note TEXT,
    resource_url TEXT,
    CONSTRAINT unique_kihontx UNIQUE (from_seq, to_seq)
);

CREATE TABLE ski.Kata_inventory(
    id_kata SMALLSERIAL PRIMARY KEY,
    kata VARCHAR(255) NOT NULL,
    serie ski.kata_series,
    starting_leg ski.sides NOT NULL,
    Note TEXT,
    resource_url TEXT,
    CONSTRAINT unique_kata UNIQUE (kata)
);

CREATE TABLE ski.kata_sequence(
    id_sequence SMALLSERIAL PRIMARY KEY,
    kata_id SMALLSERIAL NOT NULL,
    seq_num SMALLSERIAL NOT NULL,
    stand SMALLSERIAL NOT NULL REFERENCES ski.stands(id_stand),
    technic SMALLSERIAL NOT NULL REFERENCES ski.technics(id_technic),
    technic_target SMALLSERIAL NOT NULL,
    --embusen
    notes SMALLSERIAL NOT NULL,
    resource_url TEXT NULL , 
    CONSTRAINT unique_kata_seq UNIQUE (kata_id, seq_num)
);

CREATE TABLE ski.kata_tx(
    id_tx SMALLSERIAL PRIMARY KEY ,
    from_seq SMALLINT NOT NULL ,
    to_seq SMALLINT NOT NULL ,
    direction ski.sides ,
    rotation SMALLINT ,
    movement ski.movements ,
    intermediate_stand SMALLSERIAL REFERENCES ski.stands(id_stand),
    note TEXT,
    resource_url TEXT 
);




CREATE OR REPLACE FUNCTION ski.get_gradeid(
_grade NUMERIC,
_type VARCHAR
)
returns NUMERIC
language sql
as $$
SELECT id_grade 
FROM ski.grades 
WHERE grade = _grade
AND gtype = _type::ski.grade_type
;
$$;
--SELECT ski.get_gradeid(1,'dan');

CREATE OR REPLACE FUNCTION ski.get_kihons(
_grade NUMERIC,
_type VARCHAR
)
RETURNS TABLE(
    id_inventory NUMERIC ,
    grade_id NUMERIC ,
    number NUMERIC
)
LANGUAGE SQL
AS $$
SELECT id_inventory,grade_id, number FROM ski.kihon_inventory WHERE grade_id = ski.get_gradeid(_grade,_type);
$$;

--SELECT * FROM ski.get_kihon(1,'dan');

CREATE OR REPLACE FUNCTION ski.get_kihonid(
_gradeid NUMERIC,
_num NUMERIC
)
returns NUMERIC
LANGUAGE SQL
AS $$
SELECT id_inventory FROM ski.kihon_inventory WHERE grade_id = _gradeid AND number =_num;
$$;
--SELECT ski.get_kihonid(1,'dan',1);

CREATE OR REPLACE FUNCTION ski.get_technic_name(
_technic_id NUMERIC
)
returns VARCHAR
LANGUAGE SQL
AS $$
SELECT name FROM ski.technics WHERE id_technic = _technic_id;
$$;
--Per mettere il nome della tecnica nell' output;

CREATE OR REPLACE FUNCTION ski.get_stand_name(
_stand_id NUMERIC
)
returns VARCHAR
LANGUAGE SQL
AS $$
SELECT name FROM ski.stands WHERE id_stand = _stand_id;
$$;
--Per mettere il nome della posizione nell' output;

INSERT INTO ski.grades (id_grade,gtype,grade) VALUES 
    (1,'kyu',9),
    (2,'kyu',8),
    (3,'kyu',7),
    (4,'kyu',6),
    (5,'kyu',5),
    (6,'kyu',4),
    (7,'kyu',3),
    (8,'kyu',2),
    (9,'kyu',1),
    (10,'dan',1),
    (11,'dan',2),
    (12,'dan',3),
    (13,'dan',4),
    (14,'dan',5),
    (15,'dan',6),
    (16,'dan',7);


INSERT INTO ski.stands(id_stand ,name ,description ,illustration_url ,notes ) VALUES
( 1 ,'Heiko dachi' ,$$Posizione naturale a gambe divaricate e piedi paralleli (YOI)$$ ,NULL ,NULL ),
( 2 ,'Musubi dachi' ,$$Posizione naturale con talloni uniti e punte divaricate a 90° (nel saluto)$$ ,NULL ,NULL ),
( 3 ,'Heisoku dachi' ,$$Posizione naturale con piedi e talloni uniti$$ ,NULL ,NULL ),
( 4 ,'Zenkutsu dachi' ,$$Posizione frontale$$ ,NULL ,NULL ),
( 5 ,'Kokutsu dachi' ,$$Posizione basata sulla gamba posteriore$$ ,NULL ,NULL ),
( 6 ,'Kiba dachi' ,$$Posizione del cavaliere$$ ,NULL ,NULL ),
( 7 ,'Shiko dachi' ,$$Posizione quadrata$$ ,NULL ,NULL ),
( 8 ,'Hangetsu dachi' ,$$Posizione a Mezza luna$$ ,NULL ,NULL ),
( 9 ,'Sochin dachi' ,$$Posizione consolidata$$ ,NULL ,'Detta anche Fudo dachi' ),
( 10 ,'Neko ashi dachi' ,$$Posizione a gatto$$ ,NULL ,NULL ),
( 11 ,'Sanchin dachi' ,$$Posizione a clessidra$$ ,NULL ,NULL ),
( 12 ,'Hachinoji dachi' ,$$Posizione naturale a gambe divaricate e punte divaricate a 90°$$ ,NULL ,NULL ),
( 13 ,'Hachiji dachi' ,$$Posizione naturale a gambe divaricate$$ ,NULL ,NULL ),
( 14 ,'UchiHachiji dachi' ,$$Posizione a gambe divaricate e punte dei piedi all'interno$$ ,NULL ,NULL ),
( 15 ,'Teiji dachi' ,$$Posizione naturale con i piedi a forma di T$$ ,NULL ,NULL ),
( 16 ,'Renoji dachi' ,$$Posizione naturale con i piedi a forma di L$$ ,NULL ,NULL )
;


INSERT INTO ski.technics(id_technic,waza ,name ,description ,notes ,resource_url ) VALUES
    ( 0 , NULL ,'Neutra',$$$$ ,NULL ,NULL ),
    ( 1 , NULL ,'Guardia',$$$$ ,NULL ,NULL ),
    ( 10 , 'Uchi' ,'Age tsuki',$$Pugno diritto che sale dal basso verso l'alto$$ ,NULL ,NULL ),
    ( 11 , 'Uke' ,'Age uke',$$Parata crescente verso l'alto$$ ,NULL ,NULL ),
    ( 12 , 'Geri' ,'Ashi barai',$$Spazzata$$ ,NULL ,NULL ),
    ( 13 , 'Uchi' ,'Awase tsuki',$$Pugni a U piccola (eseguiti colpendo contemporaneamente il bersaglio alto con Choku tsuki e quello medio con Ura tsuki)$$ ,NULL ,NULL ),
    ( 14 , 'Uchi' ,'Chodan tsuki',$$Pugno sferrato verso la parte media del corpo dell'avversario$$ ,NULL ,NULL ),
    ( 15 , 'Uchi' ,'Choku tsuki',$$Pugno frontale sul posto$$ ,NULL ,NULL ),
    ( 16 , 'Uchi' ,'Enpi Uchi',$$Colpo di gomito$$ ,NULL ,NULL ),
    ( 17 , 'Geri' ,'Fumikiri',$$Calcio tagliente (eseguito come uno YOKO GERI KEKOMI portato molto in basso: tibia, piede dell'avversario)$$ ,NULL ,NULL ),
    ( 18 , 'Geri' ,'Fumikomi',$$Calcio pressante (eseguito con una traiettoria dall'alto verso il basso, trasferendo tutto il peso del corpo sul piede che colpisce)$$ ,NULL ,NULL ),
    ( 19 , 'Uke' ,'Gedan barai',$$Parata verso il basso$$ ,NULL ,NULL ),
    ( 20 , 'Uke' ,'Gedan Kake uke',$$Parata bassa uncinante (eseguita facendo compiere all'avambraccio un ampio movimento dall'esterno verso l'interno; normalmente è usata per parare un MAEGERI)$$ ,NULL ,NULL ),
    ( 21 , 'Uchi' ,'Gedan tsuki',$$Pugno sferrato verso la parte bassa dell'avversario$$ ,NULL ,NULL ),
    ( 22 , 'Geri' ,'Gyaku mawashi geri',$$Calcio circolare contrario (è una variante del Mawashi geri, eseguito con traiettoria dall'interno verso l'esterno)$$ ,NULL ,NULL ),
    ( 23 , 'Uchi' ,'Gyaku tsuki',$$Pugno contrario (rispetto alla gamba avanzata)$$ ,NULL ,NULL ),
    ( 24 , 'Uke' ,'Haishu jkji uke',$$Parata con le mani a X (eseguita con le mani aperte ed i polsi uniti)$$ ,NULL ,NULL ),
    ( 25 , 'Uke' ,'Haishu uke',$$Parata con il dorso della mano$$ ,NULL ,NULL ),
    ( 26 , 'Uchi' ,'Haito Uchi',$$Colpo con la mano a coltello (eseguita colpendo con la parte interna del dorso della mano)$$ ,NULL ,NULL ),
    ( 27 , 'Uke' ,'Haiwan nagashi uke',$$Parata deviante con la parte esterna dell'avambraccio (eseguita spostando il braccio in avanti per intercettare l'attacco e deviandone la traiettoria)$$ ,NULL ,NULL ),
    ( 28 , 'Uchi' ,'Hasami tsuki',$$Pugni a forbice (eseguiti con un movimento degli arti in modo ampio e circolare, dall'esterno verso l'interno)$$ ,NULL ,NULL ),
    ( 29 , 'Geri' ,'Hiza geri',$$Ginocchiata$$ ,NULL ,NULL ),
    ( 30 , 'Uchi' ,'Jodan tsuki',$$Pugno sferrato verso il volto dell'avversario (zona tra naso e occhi)$$ ,NULL ,NULL ),
    ( 31 , 'Uke' ,'Juji uke',$$Parata a due mani ad X (effettuata con pugni chiusi e polsi uniti)$$ ,NULL ,NULL ),
    ( 32 , 'Uchi' ,'Kagi tsuki',$$Pugno a uncino (eseguito formando con il braccio un angolo di 90°)$$ ,NULL ,NULL ),
    ( 33 , 'Geri' ,'Kakato geri',$$Calcio con il tallone (eseguita facendo scendere il tallone dall'alto, dopo avere caricato il calcio lanciando la gamba verso l'alto)$$ ,NULL ,NULL ),
    ( 34 , 'Uke' ,'Kakiwake uke',$$Parata a due mani a cuneo rovesciato$$ ,NULL ,NULL ),
    ( 35 , 'Uke' ,'Kakuto uke',$$Parata con il polso a testa di gru$$ ,NULL ,NULL ),
    ( 36 , 'Uke' ,'Keito uke',$$Parata con la mano a testa di gallina$$ ,NULL ,NULL ),
    ( 37 , 'Geri' ,'Kizami Geri',$$$$ ,NULL ,NULL ),
    ( 38 , 'Uchi' ,'Kizami tsuki',$$Pugno anteriore (eseguito lanciando il pugno, corrispondente alla gamba avanzata, verso il bersaglio; il piede potrà rimanere fermo o essere spostato in avanti)$$ ,NULL ,NULL ),
    ( 39 , 'Uchi' ,'Mae Empi ',$$$$ ,NULL ,NULL ),
    ( 40 , 'Uchi' ,'Mae Enpi Uchi',$$Colpo di gomito frontale (eseguita sul piano orizzontale)$$ ,NULL ,NULL ),
    ( 41 , 'Geri' ,'Mae geri',$$Calcio frontale$$ ,NULL ,NULL ),
    ( 42 , 'Geri' ,'Mae tobi geri',$$Calcio volante frontale$$ ,NULL ,NULL ),
    ( 43 , 'Uchi' ,'Mawashi Enpi Uchi',$$Colpo di gomito circolare$$ ,NULL ,NULL ),
    ( 44 , 'Geri' ,'Mawashi geri',$$Calcio circolare$$ ,NULL ,NULL ),
    ( 45 , 'Uchi' ,'Mawashi tsuki',$$Pugno circolare$$ ,NULL ,NULL ),
    ( 46 , 'Geri' ,'Mikatsuki geri',$$Calcio a luna crescente (eseguito con una traiettoria circolare crescente dal suolo sino al bersaglio)$$ ,NULL ,NULL ),
    ( 47 , 'Uchi' ,'Morote tsuki',$$Colpo portato simultaneamente con due pugni$$ ,NULL ,NULL ),
    ( 48 , 'Uke' ,'Morote uke',$$Parata a due mani rinforzata$$ ,NULL ,NULL ),
    ( 49 , 'Geri' ,'Nidan geri',$$Calcio volante doppio (eseguito lanciando due MAE GERI in successione alternata mentre si è in elevazione; il primo colpisce al livello Chudan, il secondo, con l'altra gamba, a livello Jodan)$$ ,NULL ,NULL ),
    ( 50 , 'Uchi' ,'Nihon Nukite',$$$$ ,NULL ,NULL ),
    ( 51 , 'Uchi' ,'Oi tsuki',$$Pugno lungo$$ ,NULL ,NULL ),
    ( 52 , 'Uchi' ,'Otoshi Enpi Uchi',$$Colpo di gomito dall'alto verso il basso$$ ,NULL ,NULL ),
    ( 53 , 'Uke' ,'Otoshi uke',$$Parata discendente (eseguita facendo scendere l'avambraccio perpendicolarmente sull'avambraccio dell'avversario)$$ ,NULL ,NULL ),
    ( 54 , 'Geri' ,'Ren geri',$$Calcio alternato (eseguito lanciando due MAE GERI in successione alternata)$$ ,NULL ,NULL ),
    ( 55 , 'Uchi' ,'Sanbon tsuki',$$Combinazione di tre pugni (generalmente il primo è Jodan, gli altri due Chudan)$$ ,NULL ,NULL ),
    ( 56 , 'Uke' ,'Seirykto uke',$$Parata con la mano a spada cinese$$ ,NULL ,NULL ),
    ( 57 , 'Uchi' ,'Shuto Uchi',$$Colpo con la mano a coltello (eseguita colpendo con la parte esterna del dorso della mano)$$ ,NULL ,NULL ),
    ( 58 , 'Uke' ,'Shuto uke',$$Parata con il taglio della mano$$ ,NULL ,NULL ),
    ( 59 , 'Uke' ,'Sokumen awase uke',$$Parata laterale a due mani (eseguita utilizzando il palmo della mano che è rafforzata dal dorso dell'altra)$$ ,NULL ,NULL ),
    ( 60 , 'Uke' ,'Sokumen Haito Uke',$$$$ ,NULL ,NULL ),
    ( 61 , 'Uke' ,'Sokutei mawashi uke',$$Parata circolare con la pianta del piede$$ ,NULL ,NULL ),
    ( 62 , 'Uke' ,'Sokutei osae uke',$$Parata pressante con la pianta del piede (eseguita per fermare con molto anticipo un calcio che è ancora nella fase di caricamento)$$ ,NULL ,NULL ),
    ( 63 , 'Uke' ,'Sokuto osae uke',$$Parata pressante con il taglio del piede$$ ,NULL ,NULL ),
    ( 64 , 'Uke' ,'Soto Ude uke',$$Parata media eseguita con la parte esterna dell'avambraccio$$ ,NULL ,NULL ),
    ( 65 , 'Uchi' ,'Tate Enpi Uchi',$$Colpo di gomito frontale portato dal basso verso l'alto$$ ,NULL ,NULL ),
    ( 66 , 'Uke' ,'Tate Shuto uke',$$Parata con il taglio della mano verticale$$ ,NULL ,NULL ),
    ( 67 , 'Uke' ,'Te Nagashi uke',$$Parata deviante con la mano (eseguita intercettando il braccio dell'attaccante e deviandone la traiettoria con il palmo della propria mano).$$ ,NULL ,NULL ),
    ( 68 , 'Uke' ,'Te osae uke',$$Parata con la mano pressante (eseguita portando la propria mano ad intercettare l'avambraccio dell'attaccante, abbassandolo e tirandolo all'indietro, provocando lo sbilanciamento in avanti dell'avversario).$$ ,NULL ,NULL ),
    ( 69 , 'Uke' ,'Teisho awase uke',$$Parata con le basi dei palmi delle due mani (eseguita tenendo a contatto i polsi)$$ ,NULL ,NULL ),
    ( 70 , 'Uchi' ,'Teisho Uchi',$$Colpo con la base del palmo della mano$$ ,NULL ,NULL ),
    ( 71 , 'Uke' ,'Teisho uke',$$Parata con la base del palmo della mano$$ ,NULL ,NULL ),
    ( 72 , 'Uchi' ,'Tettsui Uchi',$$Colpo col pugno a martello$$ ,NULL ,NULL ),
    ( 73 , 'Uke' ,'Uchi Ude uke',$$Parata media eseguita con la parte interna dell'avambraccio$$ ,NULL ,NULL ),
    ( 74 , 'Geri' ,'Ura mawashi geri',$$Calcio circolare rovesciato$$ ,NULL ,NULL ),
    ( 75 , 'Uchi' ,'Ura tsuki',$$Pugno rovesciato (eseguito colpendo dal basso verso l'alto e arrivando al bersaglio con il palmo verso l'alto)$$ ,NULL ,NULL ),
    ( 76 , 'Uchi' ,'Uraken Uchi',$$Colpo col dorso del pugno$$ ,NULL ,NULL ),
    ( 77 , 'Uchi' ,'Ushiro Enpi Uchi',$$Colpo di gomito all'indietro$$ ,NULL ,NULL ),
    ( 78 , 'Geri' ,'Ushiro geri',$$Calcio all'indietro$$ ,NULL ,NULL ),
    ( 79 , 'Geri' ,'Ushiro mawashi geri',$$Calcio all'indietro circolare$$ ,NULL ,NULL ),
    ( 80 , 'Uchi' ,'Yama tsuki',$$Pugni a U larga$$ ,NULL ,NULL ),
    ( 81 , 'Uchi' ,'Yoko Enpi Uchi',$$Colpo di gomito laterale$$ ,NULL ,NULL ),
    ( 82 , 'Geri' ,'Yoko geri Keage',$$Calcio laterale frustato$$ ,NULL ,NULL ),
    ( 83 , 'Geri' ,'Yoko geri Kekomi',$$Calcio laterale spinto$$ ,NULL ,NULL ),
    ( 84 , 'Geri' ,'Yoko Tobi geri',$$Calcio volante laterale$$ ,NULL ,NULL ),
    ( 2 , NULL ,'Kiri Kaeshi',$$Cambio guardia$$ ,NULL ,NULL ),
    ( 200 , NULL ,'Shi Ho Soto Uke Gyakuzuki',$$Quattro direzioni$$ ,NULL ,NULL ),
    ( 250 , NULL ,'Kime Waza',$$Controllo$$ ,NULL ,NULL )
;


INSERT INTO ski.kihon_inventory(id_inventory ,grade_id ,number ) VALUES
    ( 1 ,'1' ,'1' ),
    ( 2 ,'1' ,'2' ),
    ( 3 ,'1' ,'3' ),
    ( 4 ,'1' ,'4' ),
    ( 5 ,'1' ,'5' ),
    ( 6 ,'1' ,'6' ),
    ( 7 ,'1' ,'7' ),
    ( 8 ,'1' ,'8' ),
    ( 9 ,'1' ,'9' ),
    ( 10 ,'1' ,'10' ),
    ( 11 ,'2' ,'1' ),
    ( 12 ,'2' ,'2' ),
    ( 13 ,'2' ,'3' ),
    ( 14 ,'2' ,'4' ),
    ( 15 ,'2' ,'5' ),
    ( 16 ,'2' ,'6' ),
    ( 17 ,'2' ,'7' ),
    ( 18 ,'2' ,'8' ),
    ( 19 ,'2' ,'9' ),
    ( 20 ,'2' ,'10' ),
    ( 21 ,'3' ,'1' ),
    ( 22 ,'3' ,'2' ),
    ( 23 ,'3' ,'3' ),
    ( 24 ,'3' ,'4' ),
    ( 25 ,'3' ,'5' ),
    ( 26 ,'3' ,'6' ),
    ( 27 ,'3' ,'7' ),
    ( 28 ,'3' ,'8' ),
    ( 29 ,'3' ,'9' ),
    ( 30 ,'3' ,'10' ),
    ( 31 ,'4' ,'1' ),
    ( 32 ,'4' ,'2' ),
    ( 33 ,'4' ,'3' ),
    ( 34 ,'4' ,'4' ),
    ( 35 ,'4' ,'5' ),
    ( 36 ,'4' ,'6' ),
    ( 37 ,'4' ,'7' ),
    ( 38 ,'4' ,'8' ),
    ( 39 ,'4' ,'9' ),
    ( 40 ,'4' ,'10' ),
    ( 41 ,'5' ,'1' ),
    ( 42 ,'5' ,'2' ),
    ( 43 ,'5' ,'3' ),
    ( 44 ,'5' ,'4' ),
    ( 45 ,'5' ,'5' ),
    ( 46 ,'5' ,'6' ),
    ( 47 ,'5' ,'7' ),
    ( 48 ,'5' ,'8' ),
    ( 49 ,'5' ,'9' ),
    ( 50 ,'5' ,'10' ),
    ( 51 ,'6' ,'1' ),
    ( 52 ,'6' ,'2' ),
    ( 53 ,'6' ,'3' ),
    ( 54 ,'6' ,'4' ),
    ( 55 ,'6' ,'5' ),
    ( 56 ,'6' ,'6' ),
    ( 57 ,'6' ,'7' ),
    ( 58 ,'6' ,'8' ),
    ( 59 ,'6' ,'9' ),
    ( 60 ,'6' ,'10' ),
    ( 61 ,'7' ,'1' ),
    ( 62 ,'7' ,'2' ),
    ( 63 ,'7' ,'3' ),
    ( 64 ,'7' ,'4' ),
    ( 65 ,'7' ,'5' ),
    ( 66 ,'7' ,'6' ),
    ( 67 ,'7' ,'7' ),
    ( 68 ,'7' ,'8' ),
    ( 69 ,'7' ,'9' ),
    ( 70 ,'7' ,'10' ),
    ( 71 ,'8' ,'1' ),
    ( 72 ,'8' ,'2' ),
    ( 73 ,'8' ,'3' ),
    ( 74 ,'8' ,'4' ),
    ( 75 ,'8' ,'5' ),
    ( 76 ,'8' ,'6' ),
    ( 77 ,'8' ,'7' ),
    ( 78 ,'8' ,'8' ),
    ( 79 ,'8' ,'9' ),
    ( 80 ,'8' ,'10' ),
    ( 81 ,'9' ,'1' ),
    ( 82 ,'9' ,'2' ),
    ( 83 ,'9' ,'3' ),
    ( 84 ,'9' ,'4' ),
    ( 85 ,'9' ,'5' ),
    ( 86 ,'9' ,'6' ),
    ( 87 ,'9' ,'7' ),
    ( 88 ,'9' ,'8' ),
    ( 89 ,'9' ,'9' ),
    ( 90 ,'9' ,'10' ),
    ( 91 ,'10' ,'1' ),
    ( 92 ,'10' ,'2' ),
    ( 93 ,'10' ,'3' ),
    ( 94 ,'10' ,'4' ),
    ( 95 ,'10' ,'5' ),
    ( 96 ,'10' ,'6' ),
    ( 97 ,'10' ,'7' ),
    ( 98 ,'10' ,'8' ),
    ( 99 ,'10' ,'9' ),
    ( 100 ,'10' ,'10' ),
    ( 101 ,'11' ,'1' ),
    ( 102 ,'11' ,'2' ),
    ( 103 ,'11' ,'3' ),
    ( 104 ,'11' ,'4' ),
    ( 105 ,'11' ,'5' ),
    ( 106 ,'11' ,'6' ),
    ( 107 ,'11' ,'7' ),
    ( 108 ,'11' ,'8' ),
    ( 109 ,'11' ,'9' ),
    ( 110 ,'11' ,'10' ),
    ( 111 ,'12' ,'1' ),
    ( 112 ,'12' ,'2' ),
    ( 113 ,'12' ,'3' ),
    ( 114 ,'12' ,'4' ),
    ( 115 ,'12' ,'5' ),
    ( 116 ,'12' ,'6' ),
    ( 117 ,'12' ,'7' ),
    ( 118 ,'12' ,'8' ),
    ( 119 ,'12' ,'9' ),
    ( 120 ,'12' ,'10' )
;


INSERT INTO ski.kihon_sequences(id_sequence, inventory_id , seq_num,stand,techinc,gyaku,target_hgt,note,resource_url) VALUES 
    ( 456 ,91 ,0,4 , 1 ,'false' ,NULL , NULL , NULL ),
    ( 457 ,91 ,1,4 , 70 ,'false' ,NULL , NULL , NULL ),
    ( 458 ,91 ,2,4 , 11 ,'true' ,NULL , NULL , NULL ),
    ( 459 ,91 ,3,4 , 26 ,'false' ,NULL , NULL , NULL ),
    ( 460 ,91 ,4,4 , 40 ,'false' ,NULL , NULL , NULL ),
    ( 466 ,92 ,0,4 , 1 ,'false' ,NULL , NULL , NULL ),
    ( 467 ,92 ,1,4 , 36 ,'false' ,NULL , NULL , NULL ),
    ( 468 ,92 ,2,9 , 52 ,'false' ,NULL , NULL , NULL ),
    ( 469 ,92 ,3,4 , 64 ,'false' ,NULL , NULL , NULL ),
    ( 470 ,92 ,4,4 , 76 ,'true' ,'Jodan' , NULL , NULL ),
    ( 476 ,93 ,0,4 , 1 ,'false' ,NULL , NULL , NULL ),
    ( 477 ,93 ,1,4 , 34 ,'false' ,NULL , NULL , NULL ),
    ( 478 ,93 ,2,4 , 80 ,'false' ,NULL , NULL , NULL ),
    ( 479 ,93 ,3,4 , 29 ,'false' ,NULL , NULL , NULL ),
    ( 480 ,93 ,4,4 , 65 ,'false' ,NULL , NULL , NULL ),
    ( 486 ,94 ,0,4 , 1 ,'false' ,NULL , NULL , NULL ),
    ( 487 ,94 ,1,4 , 2 ,'false' ,NULL , NULL , NULL ),
    ( 488 ,94 ,2,9 , 15 ,'false' ,NULL , NULL , NULL ),
    ( 496 ,95 ,0,4 , 1 ,'false' ,NULL , NULL , NULL ),
    ( 497 ,95 ,1,4 , 35 ,'false' ,NULL , NULL , NULL ),
    ( 498 ,95 ,2,4 , 14 ,'false' ,NULL , NULL , NULL ),
    ( 499 ,95 ,3,4 , 18 ,'false' ,NULL , NULL , NULL ),
    ( 500 ,95 ,4,4 , 50 ,'false' ,'Jodan' , NULL , NULL ),
    ( 506 ,96 ,0,4 , 1 ,'false' ,NULL , NULL , NULL ),
    ( 507 ,96 ,1,4 , 73 ,'false' ,NULL , NULL , NULL ),
    ( 508 ,96 ,2,4 , 78 ,'false' ,NULL , NULL , NULL ),
    ( 509 ,96 ,3,6 , 50 ,'false' ,NULL , NULL , NULL ),
    ( 510 ,96 ,4,4 , 32 ,'false' ,NULL , NULL , NULL ),
    ( 516 ,97 ,0,4 , 1 ,'false' ,NULL , NULL , NULL ),
    ( 517 ,97 ,1,4 , 83 ,'false' ,NULL , NULL , NULL ),
    ( 518 ,97 ,2,4 , 41 ,'false' ,NULL , NULL , NULL ),
    ( 526 ,98 ,0,4 , 1 ,'false' ,NULL , NULL , NULL ),
    ( 527 ,98 ,1,4 , 37 ,'false' ,NULL , NULL , NULL ),
    ( 528 ,98 ,2,4 , 38 ,'false' ,NULL , NULL , NULL ),
    ( 529 ,98 ,3,4 , 41 ,'false' ,NULL , NULL , NULL ),
    ( 530 ,98 ,4,4 , 23 ,'false' ,NULL , NULL , NULL ),
    ( 537 ,99 ,1,4 , 200 ,'false' ,NULL , NULL , NULL ),
    ( 541 ,100 ,1,4 , 250 ,'false' ,NULL , NULL , NULL )
;


INSERT INTO ski.kihon_tx(id_tx ,from_seq ,to_seq ,movement ,note ,resource_url ) VALUES
    ( 455 , 456 , 457, 'Fwd' , NULL , NULL ),
    ( 456 , 457 , 458, 'Bkw' , NULL , NULL ),
    ( 457 , 458 , 459, 'Still' , NULL , NULL ),
    ( 458 , 459 , 460, 'Still' , NULL , NULL ),
    ( 465 , 466 , 467, 'Fwd' , NULL , NULL ),
    ( 466 , 467 , 468, 'Still' , NULL , NULL ),
    ( 467 , 468 , 469, 'Fwd' , NULL , NULL ),
    ( 468 , 469 , 470, 'Still' , NULL , NULL ),
    ( 475 , 476 , 477, 'Bkw' , NULL , NULL ),
    ( 476 , 477 , 478, 'Fwd' , NULL , NULL ),
    ( 477 , 478 , 479, 'Fwd' , NULL , NULL ),
    ( 478 , 479 , 480, 'Still' , NULL , NULL ),
    ( 485 , 486 , 487, 'Still' , NULL , NULL ),
    ( 486 , 487 , 488, 'Still' , NULL , NULL ),
    ( 495 , 496 , 497, 'Bkw' , NULL , NULL ),
    ( 496 , 497 , 498, 'Still' , NULL , NULL ),
    ( 497 , 498 , 499, 'Fwd' , NULL , NULL ),
    ( 498 , 499 , 500, 'Still' , NULL , NULL ),
    ( 505 , 506 , 507, 'Bkw' , NULL , NULL ),
    ( 506 , 507 , 508, 'Fwd' , NULL , NULL ),
    ( 507 , 508 , 509, 'Still' , NULL , NULL ),
    ( 508 , 509 , 510, 'Still' , NULL , NULL ),
    ( 515 , 516 , 517, 'Fwd' , NULL , NULL ),
    ( 516 , 517 , 518, 'Still' , NULL , NULL ),
    ( 525 , 526 , 527, 'Still' , NULL , NULL ),
    ( 526 , 527 , 528, 'Still' , NULL , NULL ),
    ( 527 , 528 , 529, 'Still' , NULL , NULL ),
    ( 528 , 529 , 530, 'Still' , NULL , NULL )
;



