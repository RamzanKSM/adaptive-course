-- Rebuild translations generated with an ambiguous target or masked Markdown headings on demand.
DELETE FROM content_translations
WHERE (locale = 'fr' AND translated_text GLOB '*[؀-ۿ]*')
   OR (locale IN ('fr', 'ar-SD') AND translated_text GLOB '*# [А-Яа-яЁё]*');

-- Reviewed translation of the affected production explanation. A source edit naturally gets a new key.
INSERT INTO content_translations (source_hash, locale, kind, translated_text)
VALUES ('64b6811b8cdab9ee150d672ac89dc0fa02d9bf60ee9fc0644501fde147dd33e6', 'fr', 'explanation',
'### À quoi ça sert ?

Imagine une fiche sur laquelle tu as écrit un texte. Tu peux enlever les espaces au début et à la fin, mettre toutes les lettres en majuscules ou remplacer un mot par un autre. En Python, tu peux faire ces opérations sur une chaîne de caractères, par exemple `"Привет"`.

C’est pratique pour préparer un texte avant de l’afficher, notamment pour enlever des espaces superflus ou modifier une partie d’un message.

### L’idée principale

Une chaîne possède des **méthodes** : ce sont des opérations que Python sait effectuer sur du texte. Pour appeler une méthode, écris un point entre la chaîne et le nom de la méthode. Les méthodes présentées ici renvoient une nouvelle chaîne. La chaîne d’origine garde sa valeur.

Voici la forme générale :

```python
строка.метод(аргументы)
```

- `строка` représente la chaîne sur laquelle porte l’opération.
- `.` relie la chaîne à sa méthode.
- `метод` représente le nom de la méthode, par exemple `strip` ou `replace`.
- `()` indique à Python qu’il doit appeler la méthode.
- `аргументы` représente les arguments, c’est-à-dire les valeurs que tu fournis à la méthode. Certaines méthodes s’utilisent sans argument.

Par exemple, `text.strip()` enlève les caractères blancs aux extrémités. `text.lower()` met les lettres en minuscules et `text.upper()` en majuscules. Avec `replace`, tu remplaces un fragment par un autre, comme dans `text.replace("кот", "пёс")`.

### Pas à pas

Commençons par une méthode sans argument :

```python
text = "  Привет!  "
clean_text = text.strip()
print(clean_text)
```

1. Python enregistre dans `text` une chaîne avec des espaces au début et à la fin.
2. `text.strip()` renvoie une nouvelle chaîne débarrassée de ces espaces.
3. L’affectation enregistre le résultat dans `clean_text`. La variable `text` garde sa valeur initiale.
4. `print` affiche la valeur de `clean_text`.

```text
Привет!
```

Changeons maintenant la **casse**, c’est-à-dire le fait d’écrire une lettre en minuscule ou en majuscule :

```python
word = "Python"
print(word.lower())
print(word.upper())
```

1. La variable `word` contient la chaîne `"Python"`.
2. `word.lower()` renvoie la chaîne en minuscules.
3. `word.upper()` la renvoie en majuscules.
4. Chaque appel à `print` affiche son résultat. La valeur de `word` reste la même.

```text
python
PYTHON
```

Enfin, remplaçons une partie du texte :

```python
message = "Я люблю чай"
new_message = message.replace("чай", "какао")
print(new_message)
```

1. La variable `message` contient la chaîne d’origine.
2. L’appel `replace("чай", "какао")` cherche le fragment `"чай"` et le remplace par `"какао"`.
3. La nouvelle chaîne est enregistrée dans `new_message`.
4. `print` affiche cette chaîne.

```text
Я люблю какао
```

### Erreurs fréquentes

**Oublier les parenthèses.** Si tu écris `text.strip` sans `()`, tu obtiens une référence à la méthode. Python peut alors afficher une description de la méthode. Pour obtenir la chaîne nettoyée, appelle la méthode :

```python
text = "  да  "
print(text.strip())
```

Les parenthèses après `strip` déclenchent l’appel. Le programme affiche `да`.

**Oublier les arguments de `replace`.** Indique le fragment recherché et son remplacement. L’appel `text.replace()` provoque une erreur `TypeError`. Le message qui commence par « Traceback » indique où elle s’est produite.

```python
text = "чай"
print(text.replace("ч", "д"))
```

Les deux arguments sont présents : le fragment d’origine `"ч"` et son remplacement `"д"`. Le résultat est `дай`.

**Croire que la méthode modifie la variable.** Après `text.upper()`, la variable `text` contient toujours la chaîne d’origine. Pour conserver le résultat, affecte-le à une variable : `text = text.upper()`.

### Dans les exercices

Tu peux enregistrer du texte dans une variable, appeler une méthode et transmettre le résultat à `print`. Pour afficher le résultat une seule fois, tu peux écrire `print(text.strip())`. Si tu veux le réutiliser à la ligne suivante, conserve-le dans une nouvelle variable.

### À toi de vérifier

1. Qu’affiche `print(" привет ".strip())` ?
2. Comment enregistrer dans `shout` le contenu de `word` en majuscules ?

**Réponses**

1. `привет` : `strip()` enlève les espaces aux extrémités.
2. `shout = word.upper()` : la méthode renvoie la chaîne en majuscules et l’affectation enregistre le résultat dans `shout`.

### À retenir

- Le point permet d’accéder à une méthode de la chaîne.
- Les parenthèses `()` permettent de l’appeler.
- `strip()` enlève les espaces aux extrémités. `lower()` et `upper()` changent la casse.
- `replace(старый_фрагмент, новый_фрагмент)` remplace un fragment de texte.
- Pour réutiliser le résultat d’une méthode, enregistre-le dans une variable.')
ON CONFLICT DO NOTHING;
