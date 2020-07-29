Как это работает:
- На вход подается sbv
- На выход лбой файл в любом формате

Методы
1) remove timelines - удаляет таймлаыйны и сохраняет  output file

    input file - файл, который имеет исходные данные по переводу
    
    output file - итоовый файл с переводом и таймлайнами

2) concat translate with timelines 
    
    input file - файл, который имеет исходные данные по переводу
    
    output file - итоовый файл с переводом и таймлайнами
   
    subs_file - перевденный файл, без таймлайнов из гугл транслейт.
3) prepare timelines string length

---

vim -NO +'set nu' +'windo set scrollbind' /home/kirill/PycharmProjects/captions-handler/files/captions_without_timelines.sbv /home/kirill/PycharmProjects/captions-handler/files/captions_without_timelines_improved.sbv


# Разбиваем один таймлайн на несколько

0:00:00.110,0:00:06.450
1) Берем первое поле, включая новую строку.
Разбиваем ее в класс TimeLine:
время от, 
время до,
Текст
Определяем время от и до. Переводим время в миллисекунды.
2) Берем следующий по очереди в массиве промежуток времени
Определяем объект TimeLine

3) Определяем Разницу между timelines
4) Делим ее, если в строке больше 35 символов по пробелам
Если поделить не получается нормально, то делим в меньшую сторону (меньше 35символов)




files/captions_rus_test.sbv
files/captions_rus_test_res.sbv


# Алгоритм по транскрибации на английский
1) Преобразование без пунктуации




Улучшенный алгоритм по переводу на русский

1) Формируем captions.sbv
2) Копируем в files.
3) Вызываем команду 1 (remove timelines).
4) Копируем без таймлайнов в MousePad
5) Заменяем new line на пробел
6) Заменяем точкапробел на точка2newline
7) Заменяем ! на !2newline
8) Заменяем ? на ?2newline




