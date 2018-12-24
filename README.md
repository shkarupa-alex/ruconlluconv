# ruconlluconv

Общеизвестные корпуса с морфологической разметкой для русского языка:
- Национальный корпус (НКРЯ, RNC) [www.ruscorpora.ru](http://www.ruscorpora.ru/)
- Глубоко аннотированный синтаксический корпус (ГАК, SynTagRus) [www.ruscorpora.ru](http://www.ruscorpora.ru/corpora-structure.html)
- Генеральный интернет-корпус (ГИКРЯ, GICR) [www.webcorpora.ru](http://www.webcorpora.ru/)
- Открытый корпус (OpenCorpora) [opencorpora.org](http://opencorpora.org/)

Проект [UniversalDependencies](http://universaldependencies.org/) предоставляет корпуса:
- GSD
- SynTagRus // contains syntactic dependencies
- Taiga // uses some data from MorphoRuEval-2017
- Parallel Universal Dependencies (PUD)


## SynTagRus
- Версия UD на ~5К предложений больше чем MRE17 и содержит синтаксические связи, но где-то потеряла ~5К предложений.
- Версия UD использует _ для объединения токенов.

HowTo:
- использовать версию UD без изменений (TODO _)
- добавить отсутствующие предложения из MRE17

```bash
ruconlluconv-str data/ud/UD_Russian-SynTagRus/ data/mre17/SynTagRus.ud data/processed/ru_syntagrus-ud-add.conllu
```


## RNC
- Версия MRE17 на ~1К предложений меньше чем оригинальная (100К), зато разбирается намного проще.

HowTo:
- использовать версию MRE17 с приведением формата

```bash
ruconlluconv-rnc data/mre17/RNC.conll data/processed/ru_rnc-mre17-train.conllu
```


## GICR
- Официальная версия свежее и ~в 2.5 раза больше чем MRE17
- Восстановить признак SpaceAfter возможно лишь частично (для композитов)
- Леммы иногда содержат посторонние данные (70 -> #Number)

HowTo:
- сконвертировать официальную версию в CoNNL-U

```bash
ruconlluconv-gicr data/manual/GICR_GOLD_1.2_release data/processed/ru_gicr-orig-train.conllu
```


## OC
- Официальная версия меньше ~в 2.5 раза чем MRE17, есть ощущение что на MRE отдали датасет с омонимией

HowTo:
- сконвертировать официальную версию в CoNNL-U


## GSD, PUD
HowTo:
- использовать как есть все кроме Taiga
- подкорпус Taiga проверить на пересечение со всеми остальными корпусами (особенно MRE17)


## Для всех "доработанных" датасетов:
- спрогнозировать признак SpaceAfter
- сформировать полный текст

```bash
ruconlluconv-space-dataset data/processed/ data/text/
ruconlluconv-space-vocab data/text/ data/text/vocab.pkl
ruconlluconv-space-train data/text/ data/text/vocab.pkl model/
ruconlluconv-space-predict data/text/vocab.pkl model/ data/processed/ data/ready/
```

TODO
http://www.dialog-21.ru/media/3951/sorokinaetal.pdf