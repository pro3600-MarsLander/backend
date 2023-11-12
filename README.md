# Mars Lander

## Utilisation

Le fichier launcher lance la simulation.
Dedans vous pouvez modifier les maps employés. 
```bash
python3 launcher.py
```


## Environement 





## Fonction de score
Pour employer des méthodes analytiques tel que l'algorithme génétique, il faudra déterminer une fonction de score. Cette fonction permettra de donner une note pour une trajectoire donnée et ses paramètres.

### Critères
Il existe plusieurs critères plus ou moins important allant de la distance entre la zone de crash et la zone d'atterissage, à la vitesse à l'atterissage ,...

#### Distance
Le plus important des critères est la distance qui sépare le point d'atterissage à la zone d'atterissage prescrite par l'énoncé.
Mais comment définire un bonne distance dans notre cas. Selon l'[article](https://www.codingame.com/blog/genetic-algorithm-mars-lander/) proposé comme source d'inspiration pour ce projet, la meilleur distance semble être la distance à la marche donc pas la distance absolue mais plutot la distance nécessaire pour aller de la zone de crash à la zone d'atterissage en suivant la surface de l'environnement.

#### Vitesse

Il existe des contraintes de vitesses à l'atterissage qu'il faut respecter et donc des nouveaux paramètres pour une fonction de score, cependant il est important de préciser que ce sont les vitesses à l'atterissage, ce paramètre pourra donc être par exemple pris en compte si et seulement si le vaisseau a atterit au bonne endroit.

#### Angle

Pareil que la vitesse

#### Autres

Lorsque j'écris ceci, je me demande si il ne serait pas interressant de créer un score en fonction de l'amélioration d'une trajectoire qui a pour source deux autres trajectoires. Cela me fait penser notamenent au régulateur PID, ce sera peut être le sujet d'une amélioration.
