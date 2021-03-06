CREATE OR REPLACE FUNCTION suppr_propositions() RETURNS TRIGGER AS $suppr_propositions$
	
	DECLARE
		nb_prop_oui INTEGER;
		
	-- On vérifie que le conducteur a bien été ajouté à la course
	-- On vérifie qu'il y a bien au moins une des propositions de la course qui a été acceptée
	
	BEGIN
		IF OLD.conducteur IS NULL THEN
			IF NEW.conducteur IS NOT NULL THEN
				SELECT COUNT(*) INTO nb_prop_oui FROM propositions p
				WHERE OLD.numero = p.course
				AND p.statut =  'Oui';
				IF nb_prop_oui > 0 THEN
					-- On supprime les propositions de la course affectée
					DELETE FROM propositions 
					WHERE OLD.numero = propositions.course ;
					-- On supprime les propositions du conducteur affecté
					DELETE FROM propositions
					WHERE NEW.conducteur = propositions.conducteur;
				ELSE RAISE EXCEPTION 'Les propositions de la course attribuée au conducteur n''ont jamais été acceptées'; 
				END IF;	
			END IF;	
		END IF;
		
	RETURN NULL ;
	END;
	
			
$suppr_propositions$ LANGUAGE plpgsql;
			
CREATE TRIGGER suppr_propositions 
	AFTER UPDATE ON courses
	FOR EACH ROW EXECUTE PROCEDURE suppr_propositions();