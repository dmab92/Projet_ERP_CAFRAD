# -*- coding: utf-8 -*-
{
    'name': "CAFRAD",

    'summary': """
        Projet de digitalisation des activites du CAFRAD 
        pour assurer la gestion efficace des processus du CAFRAD afin de faciliter et assurer sa bonne gouvernance.""",

    'description': """
        Ce projet contient les fonctionalités suivantes: 
        Education de base 
-	Recueil et archivage des données des élèves/apprenants;
-	Planification du programme des cours;
-	Gestion des fichiers des enseignants;
-	Gestion du programme de renforcement des capacités;
-	Gestion financière du groupe scolaire;
-	Statistiques globales (nombre d’élève par classe, nombre d’admis en classe supérieure/admis au CEP/admis au concours d’entrée en 6è, nombre de non admis, Effectif annuel des élèves);
Département Communication et information 
●	Magazine
-	Gestion et suivi des activités de rédaction du Magazine;
-	Statistiques de vente du magazine.
●	médiathèque      
-	Recueil et archivage des visiteurs et abonnés de la médiathèque;
-	Statistiques et Rapports des lecteurs de la médiathèque.
●	Programmes radio
-	Recueil et archivage des données et  intervenants (bénévoles, stagiaires, invités, auditeurs, partenaires) de la radio;
-	Gestion et suivi des programmes de la radio;
-	Gestion des recettes financières de la radio;
-	Statistiques et rapports des activités de la radio.

Département Formations Suivie et Placements 
Gestion du Service accueil écoute et orientation
-	Faire passer un prospect en client ou en apprenant;
-	Statistique et rapport des prospects et apprenants.
●	Gestion suivi et insertion des apprenants
-	Gestion et suivi des formés
-	Impression de la fiche de suivi de l’apprenant
-	Gestion de l’insertion des formés;
●	Gestion du Secrétariat Programme et Projet
-	Planification des programmes et projets;
-	Gestion et suivi des programmes et projets;
-	Planification des formations;
-	Gestion et suivi des formations professionnelles;
●	Service actions diaconales
-	Planification et suivi des activités diaconales;
-	Recueil et archivage des données des handicapés;
-	Gestion et Suivi des handicapés;
-	Statistiques et rapports des actions diaconales.

●	Garage Casmando
-	Recueil et archivage des données des prospects et apprenants du garage;
-	Statistique et rapport des prospects et apprenants;
-	Gestion financière des recettes du garage;

RH et Animations 
-	Gestion de la présence du personnel 
-	Planification des animations
-	 Suivi des animations
Service accueil et Hébergement /salle de fêtes/espace vert et boukarou
-	Gestion des réservations;
-	Gestion des commandes
-	Statistiques et rapports d’activités ;
Gestion de la caisse
Tableau bord du manager 
Impression de tous les états statistiques (Rapport d’activité, fiche de suivi, Fiche d’écoute, emploi de temps, Chronogramme, rapport, planning d’activité, etc…) 



    """,

    'author': "Boris MENI",
    'Email': 'borismeni2@gmail.com',
    'Phone':'+237 697005649/ 678128120',
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/cafrad_security.xml',
        'views/apprenant_cafrad.xml',
        'views/timetable_views.xml',
        'views/teacher_cafrad.xml',
        'views/ane_academiq_cafrad.xml',
        'views/config_class.xml',
        'menu_cafrad.xml',
        #'report_cafrad.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False
}
