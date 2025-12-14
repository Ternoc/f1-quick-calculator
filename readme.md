Petit script pour convertir un fichier CSV avec les résultats en place des GP en nombre de points.

## Utilisation

L'unique argument requis est le fichier csv contenant les résultats des pilotes par grand prix : 

```bash
$ python main.py -i fichier.csv
```

## Fichier CSV

Le fichier csv doit être formaté tel qu'un pilote par colonne et un grand prix par ligne.

Chaque cellule (résultat d'un pilote pour le grand prix) peux contenir plusieurs informations séparées par un `+`.

La cellule peut être vide.

La place en GP s'indique directement

La place en sprint s'indique précédé d'un S

Les bonus peuvent êtres ajoutés après.

**Exemple** : `12+S3+FL+PP`

### Exmeple

```csv
GP,Pilote A,Pilote B,Pilote C
Bahrein,1+S3,5+S1,4+S2+FL
Saudi Arabia,1+FL,3,2
Portugal,1+S3+FL,2,5
```

## Paramètres

Un fichier de paramètres au format JSON de la saison peut être adjoint :

```bash
$ python main.py -i fichier.csv -s 
```

Il permet d'indiquer le barème de point en course et en sprint, les points bonus, les constructeurs avec leurs pilotes, ainsi que la possibilité de modifier la barème de points pour certaines courses.

### Barème de point

Paramètre `point_scale` : Liste qui indique le barème pour chaque place, de la 1ère à la dernière qui rapporte des points.

Paramètre `sprint_point_scale` : analogue mais pour les courses sprint.

On peut **désactiver** le barème de points avec une liste vide : `[]`

#### Exemple

```json
"point_scale":[25, 18, 15, 12, 10, 8, 6, 4, 2, 1],
"sprint_point_scale":[3, 2, 1]
```

### Points bonus

Paramètre `bonus` : On peut ajouter des points bonus.

Chaque élément est une clef avec le nom du point bonus (qui doit correspondre dans le fichier csv) et une liste de 2 elements : le premier est le nombre de points, le second est la place minimale pour scorer ce point (ou -1 pour ne pas avoir de place minimum).

#### Exemple

```json
"bonus":{
        "FL":[1, 10],
        "PP":[2, -1]
    }
```

### Modificateur de barème

Paramètre `modified_scales` : On peut multiplier la barème d'une course d'un coefficient.

Chaque element est une clef avec le nom du grand prix *correspondant* dans le fichier csv et le multiplicateur.

#### Exemple

```json
"modified_scales":{
    "Belgique":0.5,
    "Abu Dhabi":2
}
```

### Constructeurs

Paramètre `constructors` : Indique les pilotes d'un constructeur, avec les courses effectuées par chacun.

Chaque élément est une clef avec le nom du constructeur et un dictionnaire contenant les infos des pilotes.

Chaque pilote est une clef avec le nom du pilote (*correspondant* avec le nom de la colonne du fichier CSV) et une liste. Chaque liste est elle même une liste avec le numéro de ligne première courses (incluse) et de la dernière course (incluse).

On peut à la place mettre -1 pour indiquer que le pilote a effectuée l'entièreté de la saison.

#### Exemple

```json
"constructors":{
    "Mercedes":{
        "HAM":-1,
        "BOT":-1
    },
    "Redbull":{
        "VER":-1,
        "GAS":[[1,12]],
        "ALB":[[13,21]]
    },
    "Constructor C":{
        "X":-1,
        "Y":[[1,5], [8,21]],
        "Z":[[6, 7]]
    }
}
```
