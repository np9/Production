CREATE FUNCTION suppr_course() RETURNS TRIGGER AS $suppr_course$
   
	BEGIN  
      
        -- Si 12h après l'heure de départ prévue de la course, 
	-- on a pas d'heure d'arrivée, 
	-- alors la course n'est pas effectuée et on supprime la ligne dans course et facturation.
       
	   DELETE FROM factures
	   WHERE course in (select numero from courses
						WHERE DATE_PART('day',CURRENT_TIMESTAMP - debut) * 24 + 
						DATE_PART('hour',CURRENT_TIMESTAMP - debut) >= 12 AND
						fin is NULL);
	   DELETE FROM courses
	   WHERE DATE_PART('day',CURRENT_TIMESTAMP - debut) * 24 + 
			DATE_PART('hour',CURRENT_TIMESTAMP - debut) >= 12 AND
		fin is NULL;
		
		RETURN NULL;
	 END;  
$suppr_course$ lANGUAGE plpgsql;
    
CREATE TRIGGER suppr_course
    AFTER INSERT OR UPDATE ON courses
    FOR EACH ROW EXECUTE PROCEDURE suppr_course();