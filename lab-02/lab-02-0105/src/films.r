library(repurrrsive)
library(purrr)
library(dplyr)

# Создаем именованный список на основе sw_films
named_sw_films <- sw_films %>%
  set_names(map_chr(sw_films, "title"))

# Проверяем результат
str(named_sw_films, max.level = 1)
names(named_sw_films)

# Функциональный подход с явным использованием map
named_sw_films_functional <- sw_films %>%
  map(~ .x) %>%  # Проходим по всем элементам списка
  set_names(map_chr(sw_films, ~ .x$title))  # Устанавливаем имена из заголовков

# Проверка эквивалентности
identical(named_sw_films, named_sw_films_functional)

# Демонстрация доступа к элементам по имени и индексу

# По имени фильма
named_sw_films[["A New Hope"]]
named_sw_films$`The Empire Strikes Back`

# По индексу
named_sw_films[[1]]
named_sw_films[[3]]