rectangle_area <- function() {
  cat("\tРасчет площади прямоугольника\n")
  length <- as.numeric(readline("Введите длину: "))
  width <- as.numeric(readline("Введите ширину: "))
  
  if (any(is.na(c(length, width))) || length <= 0 || width <= 0) {
    stop("Ошибка: длина и ширина должны быть положительными числами")
  }
  area <- length * width
  cat("Площадь прямоугольника:", area, "\n")
}


parallelogram_area <- function() {
  cat("\tРасчет площади параллелограмма\n")
  base <- as.numeric(readline("Введите основание: "))
  height <- as.numeric(readline("Введите высоту: "))
  
  if (any(is.na(c(base, height))) || base <= 0 || height <= 0) {
    stop("Ошибка: основание и высота должны быть положительными числами")
  }
  
  area <- base * height
  cat("Площадь параллелограмма:", area, "\n")
}


circle_area <- function() {
  cat("\tРасчет площади круга\n")
  radius <- as.numeric(readline("Введите радиус: "))

  if (is.na(radius) || radius <= 0) {
    stop("Ошибка: радиус должен быть положительным числом")
  }
  area <- round(pi * radius^2, 2)
  cat("Площадь круга:", area, "\n")
}


figures <- list('прямоугольник', 'параллелограм', 'круг')
count <- 0
while (TRUE) {
    input_figure <- tolower(readline(prompt = 'Введите название фигуры (прямоугольник, параллелограм, круг): '))
    if (input_figure %in% figures) {
        count <- 0
        if (input_figure == figures[1]) {
            rectangle_area()
        }
        if (input_figure == figures[2]) {
            parallelogram_area()
        }
        if (input_figure == figures[3]) {
            circle_area()
        }
        break
    } else {
        count <- count + 1
        if (count > 3) {
            cat('Вы совершили слишком много попыток! Программа завершена.\n')
            break
        } else {
            cat('Вы ввели неверное название фигуры. Попробуйте еще раз!\n')
        }
    }
}
