calculate_polygon_area <- function(x, y) {
  n <- length(x)
  polygon_matrix <- cbind(x, y)
  
  area <- 0
  for (i in 1:n) {
    j <- ifelse(i == n, 1, i + 1)
    area <- area + (x[i] * y[j] - x[j] * y[i])
  }
  return(abs(area) / 2)
}


main <- function() {
  N <- as.integer(readline(prompt = 'Введите количество вершин многоугольника: '))
  x_coords <- numeric(N)
  y_coords <- numeric(N)

  cat("\tВведите координаты вершин:\n")
  for (i in 1:N) {
    x_coords[i] <- as.numeric(readline(prompt = paste("Вершина ", i, ": x = ", sep = ''))) 
    y_coords[i] <- as.numeric(readline(prompt = paste("Вершина ", i, ": y = ", sep = '')))
  }

  area <- calculate_polygon_area(x_coords, y_coords)
  cat("Площадь многоугольника:", area, "\n")
}
  
main()
