CREATE OR REPLACE FUNCTION maj_habitude() RETURNS TRIGGER AS $maj_habitude$
    
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
 
$maj_habitude$ lANGUAGE plpgsql;
    
CREATE TRIGGER maj_habitude
    AFTER INSERT OR UPDATE ON courses
    FOR EACH ROW EXECUTE PROCEDURE maj_habitude();