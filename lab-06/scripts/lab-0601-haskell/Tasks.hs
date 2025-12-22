module Tasks where

-- Задание 1: Количество четных чисел
countEven :: [Int] -> Int
countEven [] = 0
countEven (x:xs)
    | even x    = 1 + countEven xs
    | otherwise = countEven xs

-- Задание 2: Квадраты положительных чисел
positiveSquares :: [Int] -> [Int]
positiveSquares [] = []
positiveSquares (x:xs)
    | x > 0     = x*x : positiveSquares xs
    | otherwise = positiveSquares xs

-- Задание 3: Пузырьковая сортировка
bubbleSort :: [Int] -> [Int]
bubbleSort [] = []
bubbleSort [x] = [x]
bubbleSort xs = bubbleSort (swapPass xs)

swapPass :: [Int] -> [Int]
swapPass [] = []
swapPass [x] = [x]
swapPass (x:y:xs)
    | x > y     = y : swapPass (x:xs)
    | otherwise = x : swapPass (y:xs)
