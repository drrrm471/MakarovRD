mod ownership;
mod iterators_closures;
mod pattern_matching;
mod error_handling;
mod functional_data_structures;

use iterators_closures::Product;
use error_handling::{Order as ErrorOrder, User, UserDatabase, OrderError};

fn analyze_products(products: &[Product]) -> (f64, usize, Vec<&Product>) {
    let total_price: f64 = products.iter().map(|p| p.price).sum();
    let avg_price = if products.is_empty() {
        0.0
    } else {
        total_price / products.len() as f64
    };
    
    let available_count = products.iter().filter(|p| p.in_stock).count();
    
    let expensive_products = products.iter()
        .filter(|p| p.price > 100.0)
        .collect();
    
    (avg_price, available_count, expensive_products)
}

fn main() {
    println!("=== Rust Функциональное Программирование ===\n");
    
    ownership::main();
    iterators_closures::demonstrate_iterators();
    pattern_matching::demonstrate_pattern_matching();
    error_handling::demonstrate_error_handling();
    functional_data_structures::demonstrate_functional_structures();
    
    println!("\n=== Практические задания ===");
    
    // Задание 1
    let products = vec![
        Product::new(1, "iPhone", 999.99, "electronics", true),
        Product::new(2, "T-shirt", 29.99, "clothing", true),
        Product::new(3, "MacBook", 1999.99, "electronics", false),
    ];
    let (avg, available, expensive) = analyze_products(&products);
    println!("Задание 1 - Средняя цена: {:.2}, Доступно: {}, Дорогие: {} шт.", 
             avg, available, expensive.len());
    
    // Задание 2
    println!("\nЗадание 2 - Валидация заказов:");
    let mut user_db = UserDatabase::new();
    user_db.insert(1, User::new(1, "John", "john@example.com"));
    user_db.insert(2, User::new(2, "Jane", "jane@example.com"));

    let orders = vec![
        ErrorOrder { user_id: 1, amount: 99.99, status: "pending".to_string() },
        ErrorOrder { user_id: 2, amount: 1500.0, status: "pending".to_string() },
        ErrorOrder { user_id: 3, amount: 50.0, status: "pending".to_string() },
    ];

    match error_handling::validate_orders(&orders, &user_db) {
        Ok(valid) => println!("✅ Валидных заказов: {}", valid.len()),
        Err(e) => println!("❌ Первая ошибка: {}", e),
    }
    
    // Задание 3
    println!("\nЗадание 3 - Фибоначчи:");
    let mut fib = functional_data_structures::Fibonacci::new();
    for _ in 0..10 {
        print!("{} ", fib.next().unwrap());
    }
    println!();
}
