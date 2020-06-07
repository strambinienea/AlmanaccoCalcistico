-- STRAMBINI ENEA CL. 5AI A.S. 2019/2020 --
-- SVOLGIMENTO ELABORATO INDIVIDUALE DI INFORMATICA  --

CREATE TYPE fase AS ENUM ('Quarti di Finale', 'Semifinale', 'Finale');

CREATE TABLE public.Calciatore (
    "CF" CHAR(16) NOT NULL,
    "Nome" VARCHAR(40) NOT NULL,
    "Cognome" VARCHAR(40) NOT NULL,
    "Numero" CHAR(2) NOT NULL,

    PRIMARY KEY ("CF")
);

CREATE TABLE public.Squadra (
    "ID" SERIAL NOT NULL,
    "Nome" VARCHAR(50) NOT NULL,
    "Stagione" VARCHAR(9) NOT NULL,
    "Punti" INT NOT NULL,

    PRIMARY KEY ("ID")
);

CREATE TABLE public.CalciatoreSquadra (
    "CF" CHAR(16) NOT NULL,
    "IDSquadra" INT NOT NULL,
    
    PRIMARY KEY ("CF", "IDSquadra"),

    FOREIGN KEY ("CF") REFERENCES public.Calciatore ("CF") 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("IDSquadra") REFERENCES public.Squadra ("ID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE public.Campionato (
    "ID" SERIAL NOT NULL,
    "Stagione" VARCHAR (9) NOT NULL,

    PRIMARY KEY ("ID")
);

CREATE TABLE public.Partita (
    "IDSquadra1" INT NOT NULL,
    "IDSquadra2" INT NOT NULL,
    "Data" DATE NOT NULL,
    "Stadio" VARCHAR(50) NOT NULL,
    "Vincitore" INT NOT NULL,
    "Campionato" INT NOT NULL,
    "Fase" fase NOT NULL,

    PRIMARY KEY ("IDSquadra1", "IDSquadra2", "Data"),

    FOREIGN KEY ("IDSquadra1") REFERENCES public.Squadra ("ID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("IDSquadra2") REFERENCES public.Squadra ("ID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("Vincitore") REFERENCES public.Squadra ("ID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("Campionato") REFERENCES public.Campionato ("ID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);