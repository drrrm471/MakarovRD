module Main where

import Basics
import Recursion
import Patterns
import HigherOrder
import Types
import Tasks  -- Практические задания

main :: IO ()
main = do
    putStrLn "=== Демонстрация работы функций ==="
    
    -- Базовые функции
    putStrLn "1. Базовые функции:"
    print $ square 5
    print $ grade 85
    putStrLn ""
    
    -- Рекурсия
    putStrLn "2. Рекурсия:"
    print $ factorial 5
    print $ sumList [1, 2, 3, 4, 5]
    putStrLn ""
    
    -- Pattern matching
    putStrLn "3. Pattern matching:"
    print $ addVectors (1, 2) (3, 4)
    putStrLn ""
    
    -- Функции высшего порядка
    putStrLn "4. Функции высшего порядка:"
    print $ map' square [1, 2, 3, 4]
    print $ filter' even [1, 2, 3, 4, 5, 6]
    putStrLn ""
    
    -- Алгебраические типы
    putStrLn "5. Алгебраические типы:"
    print $ distance (Point 0 0) (Point 3 4)
    print $ isWeekend Saturday
    putStrLn ""
    
    -- ПРАКТИЧЕСКИЕ ЗАДАНИЯ
    putStrLn "=== Практические задания ==="
    
    putStrLn "6. Задание 1 - Количество четных чисел:"
    print $ countEven [1, 2, 3, 4, 5, 6, 7, 8]
    print $ countEven [1, 3, 5, 7]
    putStrLn ""
    
    putStrLn "7. Задание 2 - Квадраты положительных чисел:"
    print $ positiveSquares [-1, 2, -3, 4, 0, 5, -7]
    print $ positiveSquares [1, 2, 3]
    putStrLn ""
    
    putStrLn "8. Задание 3 - Пузырьковая сортировка:"
    print $ bubbleSort [5, 2, 8, 1, 9, 3]
    print $ bubbleSort [1, 2, 3, 4]
    print $ bubbleSort []
    putStrLn ""
    
    putStrLn "=== Демонстрация завершена ==="
