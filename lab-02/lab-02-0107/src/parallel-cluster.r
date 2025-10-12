library(parallel)

mean_of_rnorm <- function(n) {
  random_numbers <- rnorm(n)
  mean(random_numbers)
}

ncores <- detectCores(logical = FALSE)
cl <- makeCluster(ncores)

result <- parLapply(cl, rep(10000, 50), mean_of_rnorm)
result <- unlist(result)

stopCluster(cl)

print(head(result))
print(paste("Среднее значение результатов:", mean(result)))