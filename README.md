# magdiploma
Диплом магистра Мисра Никита 628 группа ВМК МГУ.

Два файла: preproc.py и texstats.py

Requirements:
  python3
  Libs:
  1.ast
  2.nltk
  3.pylatexenc
  4.pymorphy2


1. preproc.py Запуск py preproc.py path-to-tex-lib. Параметр-путь до папки с корпусом tex-текстов. Гененирует папку output_preproc и файл index.txt.
2. texstats.py Запуск py texstats.py path-to-tex-lib iternum. Параметры:Параметр-путь до папки с корпусом tex-текстов(как и в первом скрипте)iternum-количество итераций алгоритма. Перед запуском данного модуля нужно обязательно запустить preproc.py, чтобы тот сгенерировал и output_preproc и index.txt. На выходе файл output.txt с выделенными парами
