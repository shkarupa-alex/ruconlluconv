# ruconlluconv

Общеизвестные корпуса с морфологической разметкой для русского языка:
- Национальный корпус (НКРЯ, RNC) [www.ruscorpora.ru](http://www.ruscorpora.ru/)
- Глубоко аннотированный синтаксический корпус (ГАК, SynTagRus) [www.ruscorpora.ru](http://www.ruscorpora.ru/corpora-structure.html)
- Генеральный интернет-корпус (ГИКРЯ, GICR) [www.webcorpora.ru](http://www.webcorpora.ru/)
- Открытый корпус (OpenCorpora) [opencorpora.org](http://opencorpora.org/)
- Тестовая часть (MorphoRuEval2017) [https://github.com/dialogue-evaluation/morphoRuEval-2017/blob/master/test_set.rar]
- Корпус из (Solarix) [https://kelijah.livejournal.com/202487.html]

Проект [UniversalDependencies](http://universaldependencies.org/) предоставляет корпуса:
- GSD
- SynTagRus
- Taiga // содержит некоторое подмножество данных из MorphoRuEval-2017
- Parallel Universal Dependencies (PUD)


## SynTagRus
- Версия UD на ~5К предложений больше чем MRE17 и содержит синтаксические связи, но где-то потеряла ~5К предложений.
- Версия UD использует _ для объединения токенов (до_того,_как).

HowTo:
- использовать версию UD без изменений (TODO _)
- добавить отсутствующие предложения из MRE17

```bash
ruconlluconv-str data/ud/UD_Russian-SynTagRus/ data/mre17/SynTagRus.ud data/processed/notext/ru_str-ud-add.conllu
```


## RNC
- Версия MRE17 на ~1К предложений меньше чем оригинальная (100К), зато разбирается намного проще.

HowTo:
- использовать версию MRE17 с приведением формата

```bash
ruconlluconv-rnc data/mre17/RNC.conll data/processed/notext/ru_rnc-mre17-train.conllu
```


## GICR
- Официальная версия свежее и ~в 2.5 раза больше чем MRE17
- Собрать композиты в одно слово
- Леммы иногда содержат посторонние данные (70 -> #Number)

HowTo:
- сконвертировать официальную версию в CoNNL-U

```bash
ruconlluconv-gicr data/manual/GICR_GOLD_1.2_release data/processed/notext/ru_gicr-orig-train.conllu
```


## OC
- Официальная версия меньше ~в 2.5 раза чем MRE17, есть ощущение что на MRE отдали датасет с омонимией
```bash
ruconlluconv-oc data/manual/annot.opcorpora.no_ambig.xml data/processed/ru_oc-orig-train.conllu
```

HowTo:
- сконвертировать официальную версию в CoNNL-U

## MRE17 test
```bash
ruconlluconv-mrg data/mre17/MRE_Gold/ data/processed/notext/ru_mre17-orig-test.conllu
```

## Solarix
```bash
ruconlluconv-slr data/manual/morpheval_corpus_solarix.full.dat data/processed/notext/ru_slr-orig-train.conllu
```

HowTo:
- сконвертировать предоставленную версию в CoNNL-U


## GSD, PUD
HowTo:
- использовать как есть все кроме Taiga (для обучения пробельной модели и его тоже)
- подкорпус Taiga проверить на пересечение со всеми остальными корпусами (особенно MRE17)


## Для всех "доработанных" датасетов:
- спрогнозировать признак SpaceAfter
- сформировать полный текст

```bash
ruconlluconv-space-dataset data/ready/ data/space/
ruconlluconv-space-vocab data/space/ data/space/vocab.pkl
ruconlluconv-space-train data/space/ data/space/vocab.pkl space_model/
ruconlluconv-space-predict data/space/vocab.pkl space_model/ data/processed/notext/ data/processed/
```

TODO
_ в слове
_ в POS
сокращения т. \n д \n.
&#39; and ``
http://www.dialog-21.ru/media/3951/sorokinaetal.pdf


Один из источников проблем - неконсистентность в обучающем корпусе GIKRYA_texts.txt, например встречается такое:
14   более   более    ADV    Degree=Cmp
и такое:
22   более   много    ADV    Degree=Cmp

неё -> он, она

https://kelijah.livejournal.com/206721.html
https://github.com/Koziev/MorphoRuEval2017/blob/master/CORPORA/merge_contest_corpora.py
