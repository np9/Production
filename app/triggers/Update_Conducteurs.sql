--Attention à changer le temps de rafraichissement
CREATE FUNCTION Update_Proposition() RETURNS TRIGGER AS $Update_Proposition$
    
	DECLARE
    
    BEGIN
    
		-- Lorsqu'une proposition est acceptée, on supprime les suivantes
        
        IF Proposition.Statut = 'OUI' THEN
            DELETE Proposition
            WHERE Proposition.Ordre >  
            
            

CREATE FUNCTION Update_Conducteurs() RETURNS TRIGGER AS $Update_Conducteurs$
    
	DECLARE
    
	BEGIN
	
        -- Lors de la mise à jour d'un conducteur, mettre sa position dans position pour garder un historique
        
		INSERT INTO Positions VALUES(OLD.Conducteur,CURRENT_DATE-600,OLD.Position);
        
    END;
    
$Update_Conducteurs$ LANGUAGE plpgsql;
    
CREATE TRIGGER update_Conducteurs
    AFTER UPDATE ON Conducteurs
    FOR EACH ROW EXECUTE PROCEDURE Update_Conducteurs()
    
    
    