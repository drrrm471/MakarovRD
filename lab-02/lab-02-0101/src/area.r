side_square <- as.numeric(readline(prompt = 'Введите сторону квадрата: '))
side_rectangle_1 <- as.numeric(readline(prompt = 'Введите 1 сторону прямоугольника: '))
side_rectangle_2 <- as.numeric(readline(prompt = 'Введите 2 сторону прямоугольника: '))
radius <- as.numeric(readline(prompt = 'Введите радиус круга: '))

s_square <- side_square^2
s_rectangle <- side_rectangle_1 * side_rectangle_2
s_circle <- pi * radius^2

s_total <- s_square + s_rectangle + s_circle

cat('\n', 'Площадь квадрата: ', s_square, '\n', 'Площадь прямоугольника: ', s_rectangle, '\n', 'Площадь круга: ', s_circle, '\n', 'Общая площадь: ', s_total, '\n')