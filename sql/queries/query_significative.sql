-- STRAMBINI ENEA CL. 5AI A.S. 2019/2020 --
-- SVOLGIMENTO ELABORATO INDIVIDUALE DI INFORMATICA  --

-- QUERY N. 1 --
-- MOSTRA LA CLASSIFICA DI UN DETERMINATO CAMPIONATO

PREPARE getClassifica (int) AS
	SELECT S."Nome", S."Stagione", S."Punti" FROM public.Squadra AS S, public.Campionato AS C
	WHERE C."Stagione" = S."Stagione" AND C."ID" = $1
	ORDER BY S."Punti" DESC;

EXECUTE getClassifica (1);

-- QUERY N. 2 --
-- MOSTRA TUTTI I GIOCATORI DI UNA DETERMINATA SQUADRA --

PREPARE getCalciatori (int) AS
	SELECT C."Nome", C."Cognome", C."Numero", S."Nome" AS "Squadra" FROM public.Calciatore AS C, CalciatoreSquadra AS CS, public.Squadra AS S
	WHERE CS."CF" = C."CF" AND CS."IDSquadra" = S."ID" AND CS."IDSquadra" = $1
	ORDER BY C."Nome", C."Cognome" DESC;

EXECUTE getCalciatori (1);