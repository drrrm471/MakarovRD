get_negative_values <- function(df) {
  negative_list <- lapply(df, function(x) x[!is.na(x) & x < 0])
  
  negative_list <- negative_list[sapply(negative_list, length) > 0]
  
  if (length(negative_list) > 0) {
    lengths <- sapply(negative_list, length)
    if (length(unique(lengths)) == 1) {
      result_matrix <- matrix(unlist(negative_list), 
                             nrow = lengths[1], 
                             ncol = length(negative_list),
                             dimnames = list(NULL, names(negative_list)))
      return(result_matrix)
    } else {
      return(negative_list)
    }
  } else {
    return(NULL)
  }
}


# Проверка работы функции на предоставленных примерах:

# Пример 1
test_data1 <- as.data.frame(list(
  V1 = c(-9.7, -10, -10.5, -7.8, -8.9), 
  V2 = c(NA, -10.2, -10.1, -9.3, -12.2), 
  V3 = c(NA, NA, -9.3, -10.9, -9.8)
))
get_negative_values(test_data1)

# Пример 2  
test_data2 <- as.data.frame(list(
  V1 = c(NA, 0.5, 0.7, 8), 
  V2 = c(-0.3, NA, 2, 1.2), 
  V3 = c(2, -1, -5, -1.2)
))
get_negative_values(test_data2)

# Пример 3
test_data3 <- as.data.frame(list(
  V1 = c(NA, -0.5, -0.7, -8), 
  V2 = c(-0.3, NA, -2, -1.2), 
  V3 = c(1, 2, 3, NA)
))
get_negative_values(test_data3)