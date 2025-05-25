# Primantik: Priming-Experiment

## Implementierung mit lab.js

Die Projektdatei `primantik.study.json` reicht aus, um das Experiment im lab.js-Builder zu rekonstruieren. Dort kann man sich das Experiment im geeigneten Format exportieren lassen, um es auf JATOS laufen zu lassen.

Die Datei `conditions.csv` enthält die Stimuli des Experiments. Die Daten basieren auf jenen von `conditions.xlsx` wurden allerdings in mehreren Aspekten angepasst:

* Es gibt nur drei Spalten (`condition`, `prime`, `target`), da nur diese für den Experimentaufbau relevant sind.
* Die Werte des Attributs `condition` wurden gruppiert:
    * Bedingungen, in denen der Zielstimulus ein Wort ist, tragen den Wert `w`.
    * Bedingungen, in denen der Zielstimulus ein Nicht-Wort ist, tragen den Wert `n`.

## Website

Begleitend zum Experiment steht eine Website zur Verfügung, auf der Informationen zum Experimentaufbau angeboten werden. In der Durchführungsphase wird dort auf die JATOS-Bereitstellung des Experiments verlinkt. Nach dessen Auswertung wird dort das Ergebnis präsentiert.

Die Website wurde mittels [Hugo](https://github.com/gohugoio/hugo) im minimalistischen [Hugo Book Theme](https://github.com/alex-shpak/hugo-book) erstellt. Hugo ermöglicht die Erstellung statischer Websites mit minimaler Konfiguration und unter Verwendung von Markdown.

Die Website kann rekonstruiert werden indem, nach Anlegen eines neuen Hugo-Projekts und der Installation des Themes, die Konfigurationsdatei des Projekts `hugo.toml` und das Verzeichnis `content` durch jene dieses Repos ausgetauscht werden. Nach dem Aufruf von `hugo build` steht die fertige Website im Verzeichnis `public` zur Verfügung.

## Implementierung mit PsychoPy (überholt)

Die Arbeit mit PsychoPy wurde aufgegeben, da sich das Programm als nicht geeignet herausgestellt hat.

### Routinen

Die Proberunde und das eigentliche Experiment nutzen dieselben Routinen. Die Routinen greifen auf dieselben Variablen zu, die allerdings aus zwei unterschiedlichen Stimulus-Dateien gespeist werden – diese Aufgabe übernehmen die Schleifen.

### Stimuli

Die Stimuli sind in zwei Dateien enthalten: `conditions.xlsx` enthält die Stimuli für das eigentliche Experiment und `conditions_test.xlsx` enthält die Stimuli für die Proberunde. Der Aufbau beider Dateien ist ident.

### Texte

Die Schleife mit dem Namen `text` überspannt das gesamte Experiment, um die Einträge der Datei `texts.xlsx` bereitzustellen. Aus diesen beziehen die Textfelder in der Einführung (intro), Überleitung von Versuchsrunde zu eigentlichem Experiment (bridge) und am Ende (end) ihren Inhalt.

## Vorlage

Das Experiment repliziert die Studie 
[A novel co-occurrence-based approach to predict pure associative and semantic priming](https://doi.org/10.3758/s13423-018-1453-6) von Roelke et al.
