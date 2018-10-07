# Корпус финансовых новостей

## О корпусе

Корпус представляет собой новости, связанные с рынком акций за период с 1 июня по 7 октября. 
Его можно скачать [здесь](https://drive.google.com/open?id=1swD7syy-CqPva56z6ztiQwX_VB5D9mN1).

В корпусе содержатся файлы форматов `.txt` и `.csv` с именами вида `источник-дата-id`. 
Каждому файлу соответствует отдельная новость. Например,
```
investing-2018-10-07-1634826.txt
investing-2018-10-07-1634826.csv
```
В файле `.txt` хранится текст новости, в файле `.csv` хранится метаинформация, описанная далее.

### Метаинформация
Файл `.csv` содерижит следующие поля:

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

### Статистика по корпусу

| Элемент                 | Значение                                                           |
|-------------------------|--------------------------------------------------------------------|
| количество статей       | 10 217                                                             |
| количество слов         | 30 29 209                                                          |
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

`scrapy crawl investing -a start=2018-09-30 end=2018-10-07`

скачает новости с 00:00 30 сентября 2018 года по 23:59 7 октября 2018 года.

Если параметр `end` не задан, новости скачиваются по текущий день включительно.
