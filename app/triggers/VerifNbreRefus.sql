#VerifNbreRefus
CREATE FUNCTION VerifNbreRefus() RETURNS TRIGGER AS $VerifNbreRefus$
    
	DECLARE
		Nb_Refus INTEGER;
    
    BEGIN
    
        SELECT COUNT(*) AS Nb_Refus
        FROM Propositions P
        WHERE P.Conducteur = NEW.Conducteur
        AND P.Statut = 'Refus'
        AND Pr.MomentRep > NEW.MomentRep - 3600;
		-- /!\ Définir sur quelle durée est calculé de nombre de refus
        
        IF Nb_Refus > 100 THEN
			-- /!\ Définir à partir de combien de refus par durée on attribue une pénalité 
			-- /!\ Définir jusqu'à quand dure une pénalité
            INSERT INTO Penalites VALUES(
				NEW.Conducteur, NEW.MomentRep, NEW.MomentRep + (3600*24),'Le conducteur a refusé trop de courses.'
			);
			
        END IF;
        
    END;
    
$VerifNbreRefus$ LANGUAGE plpgsql;

CREATE TRIGGER VerifNbreRefus
	AFTER UPDATE ON Propositions
	FOR EACH ROW EXECUTE PROCEDURE VerifNbreRefus();