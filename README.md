# Корпус финансовых новостей

## О корпусе

Корпус представляет собой новости, связанные с рынком акций за период с 1 июня по 7 октября. 
Его можно скачать [здесь](https://drive.google.com/open?id=1oGc5aEZPXmEAiS6iCx1vwI59yWioc50S).

В корпусе содержатся файлы с именами вида `источник-дата-id`. Каждому названию соответствует отдельная новость и 4 файла с разными расширениями. Например,
```
investing-2018-10-07-1634826.txt
investing-2018-10-07-1634826.csv
investing-2018-10-07-1634826.tokens
investing-2018-10-07-1634826.segments
```
В файле `.txt` хранится текст новости, в файле `.csv` хранится метаинформация, в `.tokens` -- разбиение на токены (слова), в `.segments` -- на сегменты (предложения).

### Метаинформация
Файл `.csv` содержит следующие поля:

| Поле      | Значение                                                    |
|-----------|-------------------------------------------------------------|
| language  | язык: ru или en                                             |
| url       | оригинальный URL новости                                    |
| title     | заголовок                                                   |
| timestamp | дата и время публикации в формате YY-MM-DD HH:MM            |
| agency    | агенство, например Reuters                                  |
| author    | автор новости, если известен, иначе unknown                 |
| category  | категория                                                   |
| image_url | URL главного изображения, опубликованного вместе с новостью |
| image_alt | подпись к изображению                                       |

### Разметка
Каждый слой разметки хранится в отдельном файле, в первой строке которого записан формат столбцов, а далее перечислено содержимое. 

В качестве токенизатора используется [spaCy](https://spacy.io/) -- NLP-фреймворк с открытым исходным кодом на языке Python. Spacy использует смешанные алгоритмы, основанные на правилах и предобученных статистических языковых моделях. 
Токенизатор принимает на вход исходный текст, записанный в строке Unicode и возвращает объект "Spacy.Doc" ("документ"), содержащий необходимые разборы. 
Алгоритм токенизации на слова разбивает текст по пробелам, полученные части обрабатываются поочередно слева направо: 
* просматривается список исключений, которые обрабатываются особым образом (например, don't считается двумя токенами)
* отрезаются префиксы ( $, (, “, ¿ ), остаток проверяется в новой итерации цикла
* отрезаются суффиксы (km, ), ”, !), остаток проверяется в новой итерации цикла
* разбивается по -, --, /, ….
Получившееся в итоге разбиение становится окончательным. Знаки препинания считаются отдельными токенами.

Сегментация на предложения осуществляется с помощью предобученной модели и синтаксического анализатора "spaCy Dependency Parcer", но алгоритм способен учитывать начальную разметку. Английская модель обучена на корпусе OntoNotes (новости, блоги).


### Статистика по корпусу

| Элемент                 | Значение                                                           |
|-------------------------|--------------------------------------------------------------------|
| количество статей       | 10 165                                                             |
| количество токенов      | 3 860 635                                                          |
| количество предложений  | 154 565                                                            |
| количество символов     | 18 437 652                                                         |
| top-5 новостных агенств | Investing.com, Reuters, Seeking Alpha, Bloomberg, Business Insider |
| top-5 авторов           | J. Stempel, D. Shepardson, H. Reid, N. Raymond, S. Herbst-Bayliss  |
| количество авторов      | 937                                                                |
| количество агенств      | 5                                                                  |

### Источник
[Investing.com](http://investing.com)

## Инструменты для сбора корпуса
Новости собираются с помощью [Scrapy](https://scrapy.org/) в директорию `data`. 
Запустить краулинг новостей можно командой:

`cd crawler && scrapy crawl investing`

Также можно задать желаемые даты новостей в формате YY-MM-DD. Команда

`scrapy crawl investing -a start=2018-09-30 -a end=2018-10-07`

скачает новости с 00:00 30 сентября 2018 года по 23:59 7 октября 2018 года.

Если параметр `end` не задан, новости скачиваются по текущий день включительно.


## Поиск
Реализован с помощью библиотеки whoosh и веб-сервера flask. Сервер запускается export (set) FLASK_APP=web/backend/core.py && flask run. Для запуска фронтенда требуется Node.js (npm install && npm run serve из web/frontend). Построение индекса см. в "tools/prepare_index.ipynb".

Индексируются следущие поля: название новости, дата публикации, агенство, автор, текст новости, имя файла. Индекс учитывает разбиение текста на токены и морфологию (поддерживается поиск по всем формам слова), капитализация букв сбрасывается, стоп-слова (предлоги) игнорируются. В результатах поиска выводится заголовок и небольшой отрывок новости, доступен переход к полному тексту.
 

