Test du trigger verif_banni

On bannit d''abord un utilisateur. Puis on essaye de lui ajouter une course !
INSERT INTO banissements values('33628251338','05/01/2016','06/01/2016','Impolitesse')
INSERT INTO courses(utilisateur, conducteur, places, priorite, debut, fin, retour, commentaire, depart, arrivee) VALUES ('33628251338','33699428430', 4, 'high', '2016-01-05 02:03:04.3256', '2016-01-05 04:03:04.3256', FALSE, 'Haha', 1,2)

ERREUR:  l''utilisateur est actuellement bannit
********** Erreur **********

ERREUR: l''utilisateur est actuellement bannit
État SQL :P0001








Test du trigger maj_habitude
-- On ajoute un utilisateur
INSERT INTO utilisateurs(telephone) VALUES ('33221144556'); 
-- On ajoute une course à cet utilisateur qui elle n'existe pas dans habitude ajoute le point d'arrivée comme une habitude.
-- Ajout d'une ligne dans "habitudes"
INSERT INTO courses(utilisateur, conducteur, places, priorite, debut, fin, retour, commentaire, depart, arrivee) VALUES ('33221144556','33699428430', 4, 'high', '2016-01-07 02:03:04.3256', '2016-01-07 04:03:04.3256', FALSE, 'Haha', 1,2);
-- Si cet utilisateur refait une course avec la même arrivée la course est prise en compte et pas de modifications de la table "habitudes"
INSERT INTO courses(utilisateur, conducteur, places, priorite, debut, fin, retour, commentaire, depart, arrivee) VALUES ('33221144556','33699428430', 4, 'high', '2016-01-06 02:03:04.3256', '2016-01-06 04:03:04.3256', FALSE, 'Yeah', 10,2);








Test Trigger suppr_courses

-- Suppression de la date de fin de la première course

UPDATE courses
SET fin = NULL
WHERE numero = 1;

	-- Résultat : La première course est supprimée et la facture correspondante est supprimée aussi
Suppression de la date de fin de la seconde course
UPDATE courses
SET fin = NULL
WHERE numero = 30;
	-- Résultat : La seconde course n'est pas supprimée et la facture correspondante n'est pas supprimée
	
--Test ok (réalisé le 2016-01-06 à 11:25)







--Test trigger verifheuredepart

Insertion d''une course avec l''heure de début infèrieur à l''heure de l''insertion

INSERT INTO courses(utilisateur, conducteur, places, priorite, debut, fin, retour, commentaire, depart, arrivee) VALUES ('33221144556','33699428430', 4, 'high', '2016-01-04 02:03:04.3256', '2016-01-04 04:03:04.3256', FALSE, 'Haha', 1,10)
	
ERREUR:  L''heure de depart de la course doit être postérieure à l''heure de la commande
********** Erreur **********

ERREUR: L''heure de depart de la course doit être postérieure à l''heure de la commande
État SQL :P0001

Insertion d''une course avec l''heure de début postérieur à l''heure de l''insertion

INSERT INTO courses(finie, utilisateur, conducteur, places, priorite, debut, fin, retour, commentaire, depart, arrivee) VALUES (FALSE,'33221144556','33699428430', 4, 'high', '2016-01-07 02:03:04.3256', '2016-01-07 04:03:04.3256', FALSE, 'Haha', 1,10)
	
	-- Résultat : La requête a été exécutée avec succès : une ligne modifiée. La requête a été exécutée en 122 ms.
	
-- Test ok (réalisé le 06/01/2016 à 14h00)








Test trigger update_conducteur

--Modification de la position du conducteur 
UPDATE conducteurs
SET  position = '01010000005551BCCADACC4540C7A01342071DF73F'
WHERE telephone = '33782191096';

	--Résultat : Ajout de la ligne suivante dans la table positions 
	"33782191096";"2016-01-07 09:22:34.743";"01010000008E60884105CF4540008406AC6687F63F";
	
--Test Ok. Réalisé le 07/01/2016 à 09h32









-- Test du trigger supprimer_propositions
-- On insère tout d'abord 4 propositions avec une qui est acceptée puis on met d'autres lignes pour vérifier que ce seront les bonnes lignes supprimées par la suite.
INSERT INTO propositions (course, conducteur, proposition, reponse, statut) VALUES (10,'33614535685', '2016-01-14 06:43:20.3944', '2016-01-16 06:43:20.3944', 'Oui')
INSERT INTO propositions (course, conducteur, proposition, reponse) VALUES (10,'33608871046', '2016-01-14 06:43:20.3944', '2016-01-16 06:43:20.3944');
INSERT INTO propositions (course, conducteur, proposition, reponse) VALUES (20,'33614535685', '2016-01-14 06:43:20.3944', '2016-01-16 06:43:20.3944');
INSERT INTO propositions (course, conducteur, proposition, reponse) VALUES (12,'33608871046', '2016-01-14 06:43:20.3944', '2016-01-16 06:43:20.3944');
-- On met à jour la table courses en mettant un conducteur pour une certaine course
UPDATE courses
SET conducteur = '33614535685'
WHERE numero = 10;
-- On observe alors que toutes les lignes correspondants au conducteur choisi et de cette course sont donc supprimées.
