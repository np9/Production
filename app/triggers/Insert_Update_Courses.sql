CREATE FUNCTION Insert_Update_Courses() RETURNS TRIGGER AS $Insert_Update_Courses$
    
	DECLARE
		ComptBan INTEGER;
    
	BEGIN
    
        -- Vérifie qu'un utilisateur n'est pas bannit
        
        SELECT count(*) INTO ComptBan 
        FROM Bannissements B
        WHERE B.Telephone = NEW.Telephone 
		AND B.fin >= CURRENT_DATE;
        
		IF ComptBan > 0 THEN
            RAISE EXCEPTION 'l''utilisateur est actuellement bannit';
        END IF;
        
    END;
    
$Insert_Update_Courses$ lANGUAGE plpgsql;     
    
CREATE TRIGGER Insert_Update_Courses
    AFTER INSERT OR UPDATE ON Courses
    FOR EACH ROW EXECUTE PROCEDURE Insert_Update_Courses();
    
-- Test Insert_update_courses
-- Insert into banissements values('+33628251338','05/01/2016','06/01/2016','Impolitesse')
-- Insert into Courses values(')
