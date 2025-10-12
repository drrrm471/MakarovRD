library(janeaustenr)
library(stringr)
library(parallel)

extract_words <- function(book_name) {
  text <- subset(austen_books(), book == book_name)$text
  str_extract_all(text, boundary("word")) %>% unlist %>% tolower
}

janeausten_words <- function() {
  books <- austen_books()$book %>% unique %>% as.character
  words <- sapply(books, extract_words) %>% unlist
  words
}

max_frequency <- function(letter, words, min_length = 1) {
  w <- select_words(letter, words = words, min_length = min_length)
  frequency <- table(w)     
  frequency[which.max(frequency)]
}

select_words <- function(letter, words, min_length = 1) {
  min_length_words <- words[nchar(words) >= min_length]
  grep(paste0("^", letter), min_length_words, value = TRUE)
}

words_vector <- janeausten_words()

# Параллельная обработка с использованием parallel
ncores <- detectCores(logical = FALSE)
cl <- makeCluster(ncores)

# ЭКСПОРТ ВСЕХ НЕОБХОДИМЫХ ФУНКЦИЙ В КЛАСТЕР
clusterExport(cl, c("words_vector", "select_words", "max_frequency"))
clusterEvalQ(cl, {
  library(stringr)
})

# Параллельное вычисление максимальных частот для каждой буквы
max_freq_list <- clusterApply(cl, letters, function(letter) {
  max_frequency(letter, words = words_vector, min_length = 5)
})

# Остановка кластера
stopCluster(cl)

# Преобразование результатов в именованный вектор
max_freq_vector <- unlist(max_freq_list)
names(max_freq_vector) <- letters

# Визуализация результатов
barplot(max_freq_vector, 
        main = "Наиболее частые слова по буквам алфавита\n(длина ≥ 5 букв)",
        xlab = "Буквы алфавита", 
        ylab = "Частота",
        las = 2,
        col = "lightblue",
        cex.names = 0.8)