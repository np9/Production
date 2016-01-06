CREATE OR REPLACE FUNCTION insert_courses() RETURNS TRIGGER AS $insert_courses$
    
	DECLARE
		comptadress INTEGER;
    
	BEGIN  
        
        -- Vérifie si l'adresse de destination existe dans habitude
		-- et si non, on ajoute une nouvelle habitude
       
		SELECT count(*) INTO comptadress
		FROM habitudes h
		WHERE h.adresse = NEW.arrivee AND
		h.utilisateur = NEW.utilisateur;
        
        IF comptadress < 1 THEN
            INSERT INTO habitudes VALUES(NEW.utilisateur, NEW.arrivee);
		END IF;
	return null;
    END;
 
$insert_courses$ lANGUAGE plpgsql;
    
CREATE TRIGGER insert_courses
    AFTER INSERT OR UPDATE ON courses
    FOR EACH ROW EXECUTE PROCEDURE insert_courses();