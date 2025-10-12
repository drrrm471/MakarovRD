library(R6)

PiggyBank <- R6Class(
  "PiggyBank",
  private = list(
    balance = 0,           # текущий баланс
    currency = "рубли",    # валюта
    capacity = 1000        # максимальная вместимость
  ),
  
  public = list(
    initialize = function(balance = 0, currency = "рубли", capacity = 1000) {
      # Проверка корректности входных данных
      if (balance < 0) {
        stop("Баланс не может быть отрицательным")
      }
      if (capacity <= 0) {
        stop("Вместимость должна быть положительной")
      }
      if (balance > capacity) {
        stop("Начальный баланс не может превышать вместимость")
      }
      
      private$balance <- balance
      private$currency <- currency
      private$capacity <- capacity
      
      cat("Создана копилка:\n")
      cat("  Баланс:", private$balance, private$currency, "\n")
      cat("  Валюта:", private$currency, "\n")
      cat("  Вместимость:", private$capacity, private$currency, "\n\n")
    },
    
    # Метод для добавления денег в копилку
    add_money = function(amount) {
      if (amount <= 0) {
        cat("ОШИБКА: Сумма должна быть положительной!\n")
        return(FALSE)
      }
      
      if ((private$balance + amount) > private$capacity) {
        cat("ОШИБКА: Превышена вместимость копилки!\n")
        cat("         Можно добавить максимум:", private$capacity - private$balance, private$currency, "\n")
        return(FALSE)
      }
      
      private$balance <- private$balance + amount
      cat("Успешно добавлено:", amount, private$currency, "\n")
      cat("Новый баланс:", private$balance, "/", private$capacity, private$currency, "\n\n")
      return(TRUE)
    },
    
    # Метод для извлечения денег из копилки
    withdraw_money = function(amount) {
      if (amount <= 0) {
        cat("ОШИБКА: Сумма должна быть положительной!\n")
        return(0)
      }
      
      if (amount > private$balance) {
        cat("ОШИБКА: Недостаточно средств в копилке!\n")
        cat("         Доступно:", private$balance, private$currency, "\n")
        return(0)
      }
      
      private$balance <- private$balance - amount
      cat("Успешно извлечено:", amount, private$currency, "\n")
      cat("Остаток в копилке:", private$balance, "/", private$capacity, private$currency, "\n\n")
      return(amount)
    },
    
    # Метод для проверки баланса
    check_balance = function() {
      cat("Текущий баланс:", private$balance, private$currency, "\n")
      cat("Вместимость:", private$capacity, private$currency, "\n")
      cat("Свободное место:", private$capacity - private$balance, private$currency, "\n")
      cat("Заполнено:", round((private$balance / private$capacity) * 100, 1), "%\n\n")
      return(private$balance)
    },
    
    # Метод для получения текущего баланса
    get_balance = function() {
      return(private$balance)
    },
    
    # Метод для получения валюты
    get_currency = function() {
      return(private$currency)
    },
    
    # Метод для получения вместимости
    get_capacity = function() {
      return(private$capacity)
    },
    
    # Метод для установки новой вместимости
    set_capacity = function(new_capacity) {
      if (new_capacity <= 0) {
        cat("ОШИБКА: Вместимость должна быть положительной!\n")
        return(FALSE)
      }
      
      if (private$balance > new_capacity) {
        cat("ОШИБКА: Новая вместимость меньше текущего баланса!\n")
        cat("         Текущий баланс:", private$balance, private$currency, "\n")
        return(FALSE)
      }
      
      private$capacity <- new_capacity
      cat("Вместимость изменена на:", private$capacity, private$currency, "\n")
      cat("Свободное место:", private$capacity - private$balance, private$currency, "\n\n")
      return(TRUE)
    },
    
    # Метод для отображения полной информации
    get_info = function() {
      info <- list(
        balance = private$balance,
        currency = private$currency,
        capacity = private$capacity,
        free_space = private$capacity - private$balance,
        fill_percentage = round((private$balance / private$capacity) * 100, 1)
      )
      
      cat("Информация о копилке:\n")
      cat("  Баланс:", info$balance, info$currency, "\n")
      cat("  Валюта:", info$currency, "\n")
      cat("  Вместимость:", info$capacity, info$currency, "\n")
      cat("  Свободное место:", info$free_space, info$currency, "\n")
      cat("  Заполнено:", info$fill_percentage, "%\n\n")
      
      return(info)
    }
  )
)


# Демонстрация работы программы
cat("=========================================\n")
cat("ДЕМОНСТРАЦИЯ РАБОТЫ КОПИЛКИ\n")
cat("=========================================\n\n")

# Создание первого объекта со значениями по умолчанию
cat("1. СОЗДАНИЕ ПЕРВОЙ КОПИЛКИ (со значениями по умолчанию):\n")
bank1 <- PiggyBank$new()
bank1$get_info()

# Создание второго объекта с передаваемыми значениями
cat("2. СОЗДАНИЕ ВТОРОЙ КОПИЛКИ (с передаваемыми значениями):\n")
bank2 <- PiggyBank$new(balance = 200, currency = "доллары", capacity = 5000)
bank2$get_info()

# Демонстрация работы с первой копилкой
cat("3. РАБОТА С ПЕРВОЙ КОПИЛКОЙ:\n")

cat("3.1. Добавляем 300 рублей:\n")
bank1$add_money(300)

cat("3.2. Добавляем 500 рублей:\n")
bank1$add_money(500)

cat("3.3. Пытаемся добавить 300 рублей (превышение лимита):\n")
bank1$add_money(300)

cat("3.4. Извлекаем 200 рублей:\n")
bank1$withdraw_money(200)

cat("3.5. Проверяем баланс:\n")
bank1$check_balance()

# Демонстрация работы со второй копилкой
cat("\n4. РАБОТА СО ВТОРОЙ КОПИЛКОЙ:\n")

cat("4.1. Добавляем 1000 долларов:\n")
bank2$add_money(1000)

cat("4.2. Добавляем 2000 долларов:\n")
bank2$add_money(2000)

cat("4.3. Извлекаем 500 долларов:\n")
bank2$withdraw_money(500)

cat("4.4. Пытаемся извлечь 5000 долларов (недостаточно средств):\n")
bank2$withdraw_money(5000)

cat("4.5. Изменяем вместимость на 10000 долларов:\n")
bank2$set_capacity(10000)

cat("4.6. Пытаемся установить вместимость 1000 долларов (меньше текущего баланса):\n")
bank2$set_capacity(1000)

# Работа с геттерами
cat("\n5. РАБОТА С ГЕТТЕРАМИ:\n")
cat("Баланс bank1:", bank1$get_balance(), bank1$get_currency(), "\n")
cat("Баланс bank2:", bank2$get_balance(), bank2$get_currency(), "\n")
cat("Вместимость bank2:", bank2$get_capacity(), bank2$get_currency(), "\n")

# Создание копилки с начальным балансом
cat("\n6. СОЗДАНИЕ КОПИЛКИ С НАЧАЛЬНЫМ БАЛАНСОМ:\n")
bank3 <- PiggyBank$new(balance = 150, currency = "евро", capacity = 1000)
bank3$get_info()

cat("6.1. Добавляем 100 евро:\n")
bank3$add_money(100)

cat("6.2. Извлекаем 50 евро:\n")
bank3$withdraw_money(50)

cat("6.3. Финальная информация о bank3:\n")
bank3$get_info()

cat("\n=========================================\n")
cat("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА\n")
cat("=========================================\n")