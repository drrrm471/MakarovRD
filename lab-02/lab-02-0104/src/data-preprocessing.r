my_vector <- c(21, 18, 21, 19, 25, 20, 17, 17, 18, 22, 17, 18, 18, 19, 19, 27, 21, 20, 
               24, 17, 15, 24, 24, 29, 19, 14, 21, 17, 19, 18, 18, 20, 21, 21, 19, 17, 
               21, 13, 17, 13, 23, 15, 23, 24, 16, 17, 25, 24, 22)

mean_val <- mean(my_vector)
sd_val <- sd(my_vector)
my_vector2 <- my_vector[abs(my_vector - mean_val) < sd_val]