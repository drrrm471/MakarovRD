days_week <- vector('numeric', length = 7)
names(days_week) <- c('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')

cat('\tКоличество занятий в день недели.\n')
for (i in 1:7) {
    days_week[i] <- as.numeric(readline(prompt = paste(names(days_week)[i], ': ', sep = '')))
}

average_value <- round(sum(days_week) / 7)
cat('\n', 'Среднее количество занятий в неделю:', average_value, '\n')