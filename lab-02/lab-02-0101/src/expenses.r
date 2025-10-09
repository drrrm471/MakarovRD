expenses <- c()
while (TRUE) {
    art <- (readline(prompt = 'Введите статью расходов: '))
    if (art == '') {
        if (length(expenses) >= 3) {
            cat('\n', 'Суммарные расходы: ', sum(expenses), '\n', 'Максимальная статья расходов: ', names(expenses)[which.max(expenses)], max(expenses), '\n')
            break
        } else {
           cat('Необходимо ввести минимум 3 статьи расходов!', '\n')
        }
    } else {
       expenses[art] <- as.numeric(readline(prompt = 'Введите число расходов: '))
    }
}