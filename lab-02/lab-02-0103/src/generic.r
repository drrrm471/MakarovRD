get_area <- function(x){
    UseMethod('get_area')
}


get_area.default <- function(x) {
    cat('Невозможно обработать данные.')
    return(NA)
}

create_rectangle <- function(length, width) {
    if (any(is.na(c(length, width))) || length <= 0 || width <= 0) {
        stop("Ошибка: длина и ширина должны быть положительными числами")
  }
  rectangle <- list(
  length = length,
  width = width,
  type = 'Прямоугольник'
  )
  class(rectangle) <- c('rectangle', 'view')
  return (rectangle)
}


create_parallelogram <- function(base, height) {
    if (any(is.na(c(base, height))) || base <= 0 || height <= 0) {
        stop("Ошибка: основание и высота должны быть положительными числами")
  }
  parallelogram <- list(
  base = base,
  height = height,
  type = 'Параллелограмм'
  )
  class(parallelogram) <- c('parallelogram', 'view')
  return (parallelogram)
}


create_circle <- function(radius) {
  if (is.na(radius) || radius <= 0) {
    stop("Ошибка: радиус должен быть положительным числом")
  }
  circle <- list(
  radius = radius,
  type = 'Круг'
  )
  class(circle) <- c('circle', 'view')
  return (circle)
}


get_area.rectangle <- function(x) {
    area <- x$length * x$width
    cat('Площадь прямоугольника: ', area, '\n')
    return(area)
}    
    
get_area.parallelogram <- function(x) {
    area <- x$base * x$height
    cat('Площадь параллелограмма: ', area, '\n')
    return(area)
} 

get_area.circle <- function(x) {
    area <- pi * (x$radius ^ 2)
    cat('Площадь круга: ', area, '\n')
    return(area)
} 


# test

# создание фигур
rec <- create_rectangle(5, 2)
par <- create_parallelogram(2, 5)
cir <- create_circle(5)

# вычисление площадей фигур
area_rec <- get_area(rec)
area_par <- get_area(par)
area_cir <- get_area(cir)

# вызов  метода по умолчанию
cat('\n')
get_area()    

# вывод информации о фигурах (классах фигур)
cat('\n')
print(rec)
cat('\n')
print(par)
cat('\n')
print(cir)
