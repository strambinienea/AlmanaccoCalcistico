-- STRAMBINI ENEA CL. 5AI A.S. 2019/2020 --
-- SVOLGIMENTO ELABORATO INDIVIDUALE DI INFORMATICA  --
-- QUERY N. 1 --
-- MOSTRA LA CLASSIFICA DI UN DETERMINATO CAMPIONATO
PREPARE getClassifica (int) AS
SELECT
	S."Nome",
	S."Stagione",
	S."Punti"
FROM
	public.Squadra AS S,
	public.Campionato AS C
WHERE
	C."Stagione" = S."Stagione"
	AND C."ID" = $ 1
ORDER BY
	S."Punti" DESC;

EXECUTE getClassifica (1);

-- QUERY N. 2 --
-- MOSTRA TUTTE LE PARTITE DI UN DETERMINATO CAMPIONATO --
PREPARE getPartite (int) AS
SELECT
	S1."Nome" AS Squadra1,
	S2."Nome" AS Squadra2,
	P."Stadio",
	P."Fase",
	S3."Nome" AS SquadraVincente,
	P."Data"
FROM
	Squadra AS S1,
	Squadra AS S2,
	Squadra AS S3,
	Partita AS P
WHERE
	P."IDSquadra1" = S1."ID"
	AND P."IDSquadra2" = S2."ID"
	AND P."Vincitore" = S3."ID"
	AND P."Campionato" = $ 1
ORDER BY
	P."Data" ASC;

EXECUTE getPartite (1);