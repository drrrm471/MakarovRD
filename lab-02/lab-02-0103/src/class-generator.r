library(R6)

MicrowaveOven <- R6Class(
  "MicrowaveOven",
  private = list(
    power = NULL,      # мощность в Вт
    door_open = NULL   # состояние дверцы (TRUE - открыта, FALSE - закрыта)
  ),
  
  public = list(
    initialize = function(power = 800, door_open = FALSE) {
      private$power <- power
      private$door_open <- door_open
      cat("Создана микроволновая печь. Мощность:", private$power, "Вт, Дверца:", 
          ifelse(private$door_open, "открыта", "закрыта"), "\n")
    },
    
    # Метод для открытия дверцы
    open_door = function() {
      if (!private$door_open) {
        private$door_open <- TRUE
        cat("Дверца микроволновки открыта\n")
      } else {
        cat("Дверца уже открыта\n")
      }
      invisible(self)
    },
    
    # Метод для закрытия дверцы
    close_door = function() {
      if (private$door_open) {
        private$door_open <- FALSE
        cat("Дверца микроволновки закрыта\n")
      } else {
        cat("Дверца уже закрыта\n")
      }
      invisible(self)
    },
    
    # Метод для получения мощности
    get_power = function() {
      return(private$power)
    },
    
    # Метод для установки мощности
    set_power = function(new_power) {
      if (new_power > 0) {
        private$power <- new_power
        cat("Мощность изменена на:", private$power, "Вт\n")
      } else {
        cat("Ошибка: Мощность должна быть положительным числом\n")
      }
      invisible(self)
    },
    
    # Метод для получения состояния дверцы
    is_door_open = function() {
      return(private$door_open)
    },
    
    # Метод для приготовления пищи
    cook_food = function(food_name = "еда") {
      # Проверка состояния дверцы
      if (private$door_open) {
        cat("ОШИБКА: Нельзя готовить с открытой дверцей! Закройте дверцу сначала.\n")
        return(FALSE)
      }
      
      # Расчет времени приготовления в зависимости от мощности
      # Формула: время обратно пропорционально мощности
      # Для мощности 800 Вт - стандартное время 60 секунд
      base_time <- 60    # базовое время в секундах
      base_power <- 800  # базовая мощность в Вт
      
      cooking_time <- base_time * (base_power / private$power)
      
      cat("\n=== Начинаем приготовление ===\n")
      cat("Блюдо:", food_name, "\n")
      cat("Мощность печи:", private$power, "Вт\n")
      cat("Расчетное время приготовления:", round(cooking_time, 1), "секунд\n")
      
      # Имитация процесса приготовления (с ограничением для демонстрации)
      demo_time <- min(cooking_time, 5)  # ограничиваем 5 сек для демонстрации
      cat("Приготовление... (ожидание", demo_time, "секунд)\n")
      
      # Прогресс-бар
      for(i in 1:10) {
        Sys.sleep(demo_time / 10)
        cat(".")
      }
      cat("\n")
      
      cat("=== Приготовление завершено ===\n")
      cat("Ваше блюдо '", food_name, "' готово! Приятного аппетита!\n\n")
      return(TRUE)
    },
    
    # Метод для отображения статуса
    show_status = function() {
      status <- ifelse(private$door_open, "ОТКРЫТА", "ЗАКРЫТА")
      cat("Статус микроволновки:\n")
      cat("  Мощность:", private$power, "Вт\n")
      cat("  Дверца:", status, "\n")
    },
    
    # Метод для получения полной информации о состоянии
    get_info = function() {
      return(list(
        power = private$power,
        door_open = private$door_open
      ))
    }
  )
)

# Демонстрация работы программы
cat("=========================================\n")
cat("ДЕМОНСТРАЦИЯ РАБОТЫ МИКРОВОЛНОВЫХ ПЕЧЕЙ\n")
cat("=========================================\n\n")

# Создание первого объекта со значениями по умолчанию
cat("1. СОЗДАНИЕ ПЕРВОЙ МИКРОВОЛНОВКИ (со значениями по умолчанию):\n")
microwave1 <- MicrowaveOven$new()  # мощность 800 Вт, дверца закрыта
cat("\n")

# Создание второго объекта с передаваемыми значениями
cat("2. СОЗДАНИЕ ВТОРОЙ МИКРОВОЛНОВКИ (с передаваемыми значениями):\n")
microwave2 <- MicrowaveOven$new(power = 1200, door_open = TRUE)
cat("\n")

# Демонстрация работы первой микроволновки
cat("3. РАБОТА С ПЕРВОЙ МИКРОВОЛНОВКОЙ (800 Вт):\n")
microwave1$show_status()

cat("\n3.1. Приготовление супа:\n")
microwave1$cook_food("суп")

cat("\n3.2. Открываем дверцу:\n")
microwave1$open_door()

cat("\n3.3. Попытка приготовить с открытой дверцей:\n")
microwave1$cook_food("суп")

cat("\n3.4. Закрываем дверцу и готовим картофель:\n")
microwave1$close_door()
microwave1$cook_food("картофель")

# Демонстрация работы второй микроволновки
cat("\n4. РАБОТА СО ВТОРОЙ МИКРОВОЛНОВКОЙ (1200 Вт):\n")
microwave2$show_status()

cat("\n4.1. Закрываем дверцу (изначально была открыта):\n")
microwave2$close_door()

cat("\n4.2. Готовим пиццу:\n")
microwave2$cook_food("пицца")

# Демонстрация геттеров и сеттеров
cat("\n5. РАБОТА С ГЕТТЕРАМИ И СЕТТЕРАМИ:\n")
cat("Текущая мощность microwave1:", microwave1$get_power(), "Вт\n")
cat("Дверца microwave1 открыта:", microwave1$is_door_open(), "\n")

cat("\nИзменяем мощность microwave1 на 1500 Вт:\n")
microwave1$set_power(1500)
microwave1$show_status()

cat("\n5.1. Готовим курицу с новой мощностью:\n")
microwave1$cook_food("курица")

# Сравнение времени приготовления для разных мощностей
cat("\n6. СРАВНЕНИЕ ВРЕМЕНИ ПРИГОТОВЛЕНИЯ:\n")

cat("\n6.1. Microwave1 (1500 Вт) - готовим рыбу:\n")
microwave1$cook_food("рыба")

cat("\n6.2. Microwave2 (1200 Вт) - готовим рыбу:\n")
microwave2$cook_food("рыба")

# Попытка установить некорректную мощность
cat("\n7. ПРОВЕРКА ВАЛИДАЦИИ ДАННЫХ:\n")
cat("Попытка установить мощность -100 Вт:\n")
microwave1$set_power(-100)

# Финальный статус всех микроволновок
cat("\n8. ФИНАЛЬНЫЙ СТАТУС ВСЕХ МИКРОВОЛНОВОК:\n")
cat("Микроволновка 1:\n")
microwave1$show_status()
cat("\nИнформация через get_info():")
print(microwave1$get_info())

cat("\nМикроволновка 2:\n")
microwave2$show_status()
cat("\nИнформация через get_info():")
print(microwave2$get_info())

cat("\n=========================================\n")
cat("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА\n")
cat("=========================================\n")