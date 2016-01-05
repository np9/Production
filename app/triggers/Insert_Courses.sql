CREATE FUNCTION Insert_Courses() RETURNS TRIGGER AS $Insert_Courses$
    
	DECLARE
		Comptadress INTEGER;
    
	BEGIN  
        
        -- Vérifie si l'adresse de destination existe dans habitude
		-- et si non, on ajoute une nouvelle habitude
       
		SELECT count(*) INTO Comptadress
		FROM Habitude H
		WHERE H.Adresse = NEW.Adresse AND
		H.Utilisateur = NEW.Arrivee;
        
        IF Comptadress < 1 THEN
            INSERT INTO Habitude VALUES(NEW.Utilisateur, NEW.Arrivee);
		END IF;
    END;
 
$Insert_Courses$ lANGUAGE plpgsql;
    
CREATE TRIGGER Insert_Courses
    AFTER INSERT OR UPDATE ON Courses
    FOR EACH ROW EXECUTE PROCEDURE Insert_Courses();
    
  