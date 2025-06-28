# Primantik: Priming-Experiment

## To-Do
- [ ] Parameter Versuchspersonen mit random slopes modellieren
- [ ] Modell inkl Testdaten rechnen
- [ ] Visualisierungsskript modularisieren
- [ ] Standardabweichungen/Konfidenzintervalle zu Grafik hinzufügen

## Skripte

Die Datei `main.py` wird als Einstiegspunkt genutzt, um die Funktionen des Aufbereitungs- (`process.py`) oder Analyseskripts (`analyse.py`) aufzurufen.

### Aufbereitung & Analyse

Das Verzeichnis `evaluation` enthält das Skript zur Erzeugung von Grafiken `visualise.py` sowie jenes zur statistischen Analyse `analyse.py`. Bei der statistischen Analyse werden die Wortpaare bestehend aus Prime und Target der aufgearbeiten Ergebnisse ergänzt um die Information der Beziehung zwischen Prime und Target (assoziativ, semantisch, keine) mittels der Datei `conditions-experiment.csv`.

Das Skript `process.py` bereitet die Daten aus `results-raw.txt` auf und erzeugt `results-processed.txt`. Es besteht die Möglichkeit die Ergebnisse in leicht lesbarer Form auszugeben (Variable `pretty_print`). Für die Analyse sollte allerdings die kompakte Darstellung gewählt werden, da bei dieser in jeder Zeile ein eigener Datensatz steht.

### Python set-up

Um die Analyse in Python durchzuführen, werden ein paar Bibliotheken benötigt. Diese werden am besten in einer virtuellen Umgebung installiert. Dazu kann im Verzeichnis des Repo eine solche angelegt werden und die benötigten Pakete mittels Pip installiert werden:

```
python3 -m venv .
python3 -m pip install scipy==1.15.3
python3 -m pip install statsmodels
python3 -m pip install bambi
python3 -m pip install seaborn
```

> [!IMPORTANT]  
> Statsmodels version 0.14.4 only works with SciPy version <= 1.15.3 since it relies on `_lazywhere` which was removed in newer versions of SciPy.

## Ergebnisse

Im Verzeichnis `results` finden sich die unverarbeiteten Ergebnisse von JATOS in der Datei `results-raw.txt`, wobei jede Zeile die Ergebnisse einer Versuchsperson im JSON-Format hält. Die für die Analyse aufbereiteten Ergebnisse sind in der Datei `results-processed.txt` festgehalten. Für beide Dateien liegt eine JSON-Schema-Datei bei, die für jeweils einen Datensatz das Format spezifiziert.

## Implementierung mit lab.js

Die Projektdatei `primantik.study.json` reicht aus, um das Experiment im lab.js-Builder zu rekonstruieren. Dort kann man sich das Experiment im geeigneten Format exportieren lassen, um es auf JATOS laufen zu lassen.

Die Datei `conditions-experiment.csv` enthält die Stimuli für das Experiments; `conditions-test.csv` jene für die Proberunde. Die Daten basieren auf jenen von `conditions.xlsx` wurden allerdings in mehreren Aspekten angepasst:

* Es gibt nur drei Spalten (`condition`, `prime`, `target`), da nur diese für den Experimentaufbau relevant sind.
* Die Werte des Attributs `condition` wurden gruppiert:
    * Bedingungen, in denen der Zielstimulus ein Wort ist, tragen den Wert `w`.
    * Bedingungen, in denen der Zielstimulus ein Nicht-Wort ist, tragen den Wert `n`.

Aus der Gesamtmenge der Bedingungen wurden die 50 Wortpaare der Bedingung "Associative+Semantic", die ersten 25 Wortpaare der Bedingung "Pronouncable Nonword Target" sowie die ersten 25 Wortpaare der Bedingung "Unpronouncable Nonword Target" entnommen, um den Datensatz für die Proberunde zu bilden. Dieser besteht wie der Datensatz für das Experiment zur Hälfte aus Nicht-Wörtern.

## Website

Begleitend zum Experiment steht eine Website zur Verfügung, auf der Informationen zum Experimentaufbau angeboten werden. In der Durchführungsphase wird dort auf die JATOS-Bereitstellung des Experiments verlinkt. Nach dessen Auswertung wird dort das Ergebnis präsentiert.

Die Website wurde mittels [Hugo](https://github.com/gohugoio/hugo) im minimalistischen [Hugo Book Theme](https://github.com/alex-shpak/hugo-book) erstellt. Hugo ermöglicht die Erstellung statischer Websites mit minimaler Konfiguration und unter Verwendung von Markdown.

Die Website kann rekonstruiert werden indem, nach Anlegen eines neuen Hugo-Projekts und der Installation des Themes, die Konfigurationsdatei des Projekts `hugo.toml` und das Verzeichnis `content` durch jene dieses Repos ausgetauscht werden. Nach dem Aufruf von `hugo build` steht die fertige Website im Verzeichnis `public` zur Verfügung.

## Vorlage

Das Experiment repliziert die Studie 
[A novel co-occurrence-based approach to predict pure associative and semantic priming](https://doi.org/10.3758/s13423-018-1453-6) von Roelke et al.

## Implementierung mit PsychoPy (überholt)

Die Arbeit mit PsychoPy wurde aufgegeben, da sich das Programm als nicht geeignet herausgestellt hat.

### Routinen

Die Proberunde und das eigentliche Experiment nutzen dieselben Routinen. Die Routinen greifen auf dieselben Variablen zu, die allerdings aus zwei unterschiedlichen Stimulus-Dateien gespeist werden – diese Aufgabe übernehmen die Schleifen.

### Stimuli

Die Stimuli sind in zwei Dateien enthalten: `conditions.xlsx` enthält die Stimuli für das eigentliche Experiment und `conditions_test.xlsx` enthält die Stimuli für die Proberunde. Der Aufbau beider Dateien ist ident.

### Texte

Die Schleife mit dem Namen `text` überspannt das gesamte Experiment, um die Einträge der Datei `texts.xlsx` bereitzustellen. Aus diesen beziehen die Textfelder in der Einführung (intro), Überleitung von Versuchsrunde zu eigentlichem Experiment (bridge) und am Ende (end) ihren Inhalt.
