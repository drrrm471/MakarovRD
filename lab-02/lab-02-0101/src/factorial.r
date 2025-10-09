foo <- function(n) {
  if (n > 0) {
    return(n * foo(n - 1))
  } else {
    return(1)
  }
}

# передаем функции значение 7 для проверки
result <- foo(7)
print(result)