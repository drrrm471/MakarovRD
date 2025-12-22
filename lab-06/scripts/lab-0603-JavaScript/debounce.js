// ЗАДАНИЕ 3: Функция дебаунсинга
const debounce = (func, delay) => {
    let timeoutId;
    
    return (...args) => {
        // Отменяем предыдущий таймер
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        
        // Устанавливаем новый таймер
        timeoutId = setTimeout(() => {
            func.apply(null, args);
        }, delay);
    };
};

// Пример использования
const searchProducts = debounce((query) => {
    console.log('Поиск по запросу:', query);
    // API запрос поиска
}, 300);

// Тестирование (раскомментируйте для проверки)
// searchProducts('iphone');
// setTimeout(() => searchProducts('macbook'), 100);
// setTimeout(() => searchProducts('laptop'), 200);
