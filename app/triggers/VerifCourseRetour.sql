#Verif CourseRetour
CREATE FUNCTION trigger() RETURNS trigger AS $VerifCourseRetour$
	
	DECLARE
		pb	INTEGER;
		utilisateur Courses.utilisateur%TYPE;
		debut Courses.debut%TYPE;
		fin Courses.fin%TYPE;
		depart Courses.depart%TYPE;
		arrivee Courses.arrivee%TYPE;
		numero INTEGER;
		
	BEGIN
	
		-- comptage du nombre de ligne ou le client choisit un allé ET un retour
		SELECT count(*) AS pb,numero+1 AS numero, utilisateur AS utilisateur, debut AS debut, fin AS fin, depart AS depart, arrivee AS arrivee FROM Courses
		WHERE retour='TRUE';
		
			-- quand le client choisit un allé/retour, on insère son retour dans la table source avec pour adresse de départ du retour, l'adresse d'arrivée de l'allé
			IF (TG_OP = 'INSERT') THEN
				
				IF(pb>=0)
					THEN INSERT INTO Courses VALUES (numero,NULL,utilisateur,NULL,NULL,NULL,debut,fin,'FALSE',NULL,depart,arrivee);
				END IF;
			
			END IF;
			
			-- quand on fait un update sur la table Courses, on renvoit un erreur si l'adresse de départ du retour est différente de l'adresse d'arrivée de l'allé
			IF (TG_OP ='UPDATE') THEN
				
				IF(pb>0)
					THEN RAISE EXCEPTION 'L''adresse de départ du retour doit être égale à l''adresse d''arrivée de l''allé';
				END IF;
			
			END IF;
		
	END;
	
$VerifCourseRetour$ LANGUAGE plpgsql;
	
CREATE TRIGGER VerifCourseRetour BEFORE INSERT OR UPDATE ON Courses
	EXECUTE PROCEDURE trigger();