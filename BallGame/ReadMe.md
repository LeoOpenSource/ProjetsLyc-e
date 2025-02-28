-- Description du Projet --
Le jeu BallGame est une reproduction du jeu Idle Breakout en Python à l'aide de la bibliothèque Pyxel Studio. 
Ce projet vise à travailler la maîtrise de la Programmation Orientée Objet.
Il s'agit d'un projet de type "Simulateur" où vous devez simplement terminer une infinité de niveaux de difficulté croissante en détruisant toutes les briques.

-- Comment jouer --
Tout d'abord assurez-vous d'avoir installé la bibliothèque Pyxel sur votre ordinateur.
Lorsque vous lancerez le jeu, une pop up devrait s'ouvrir affichant des blocs de couleur violette ainsi qu'un menu sur la partie supérieure de l'écran.
Pour jouer, il vous suffit de commencer à détruire des briques avec votre clic gauche, afin de faire augmenter votre score.
A mesure que votre score augmente, vous aurez la possibilité d'accéder à la boutique en cliquant sur le bouton composé de trois barres horizontales, puis en cliquant sur "SHOP".
Vous pourrez acheter vos premières balles, qui vous permettrons d'automatiser la destruction de Briques et donc le gain de score.
Tous les dix niveaux, un Boss apparait: une grande brique avec beaucoup de vie.
Compléter un niveau vous apporte une quantité de points proportionnées à sa difficultée.
Vous aurez plus tard la possibilité d'améliorer les dégats infligés par les balles.
Chaque balle dispose de capacités propres listées ci-dessous.

-- Liste des Balles --
Prix: 100 --> Balle Basique 
  Une simple balle qui rebondit de part et d'autres et qui inflige au départ 1 point de dégat.
Prix: 200 --> Balle Plasma 
  Une balle qui rebondit de part et d'autres et qui inflige au départ 2 points de dégat.
  Cette balle a la particularité d'infliger des points de dégats à toutes les briques comprises à une certaine distance de la brique touchée.
Prix: 300 --> Balle Sniper 
  Une balle qui rebondit de part et d'autres et qui inflige au départ 3 points de dégat.
  Cette balle a la particularité d'être téléguidée vers la cible qu'elle aura choisie et de ne pas la lâcher avant de l'avoir détruite.
Prix: 400 --> Balle Canon 
  Une balle qui rebondit de part et d'autres et qui inflige au départ 5 points de dégat.
  Cette balle a la particularité d'être plus grosse que les autres, ce qui lui permet de rebondir plus facilement et d'infliger énormément de dégats.
Prix: 500 --> Balle Angélique 
  Une balle qui rebondit de part et d'autres et qui inflige au départ 0 points de dégat.
  Cette balle a la particularité de renforcer la valeur des briques qu'elle touche. Au départ, chaque brique touchée augmente de 5 points sa valeur.
Prix: 600 --> Balle Divisive 
  Une balle qui rebondit de part et d'autres et qui inflige au départ 2 points de dégat.
  Cette balle a la particularité de former une Balle Basique à chaque fois qu'elle rebondit sur une brique.
  Chaque Balle Divisive ne peut engendrer que 8 balles enfants à la fois qui cessent d'exister au bout de 10 secondes.

