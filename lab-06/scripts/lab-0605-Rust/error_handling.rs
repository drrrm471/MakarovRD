use std::collections::HashMap;
use std::fmt;

#[derive(Debug, Clone)]
pub struct User {
    pub id: u32,
    pub name: String,
    pub email: String,
}

#[derive(Debug, Clone)]
pub struct Order {
    pub user_id: u32,
    pub amount: f64,
    pub status: String,
}

pub type UserDatabase = HashMap<u32, User>;

impl User {
    pub fn new(id: u32, name: &str, email: &str) -> Self {
        User {
            id,
            name: name.to_string(),
            email: email.to_string(),
        }
    }
}

fn find_user(db: &UserDatabase, id: u32) -> Option<&User> {
    db.get(&id)
}

fn validate_user(user: &User) -> Result<&User, String> {
    if user.email.contains('@') {
        Ok(user)
    } else {
        Err(format!("Invalid email for user {}", user.name))
    }
}

fn process_order(db: &UserDatabase, order: &Order) -> Result<(&User, &Order), String> {
    let user = find_user(db, order.user_id)
        .ok_or_else(|| format!("User {} not found", order.user_id))?;
    
    let validated_user = validate_user(user)?;
    
    Ok((validated_user, order))
}

#[derive(Debug)]
pub enum OrderError {
    UserNotFound(u32),
    InvalidUser(String),
    PaymentFailed(String),
}

impl fmt::Display for OrderError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            OrderError::UserNotFound(id) => write!(f, "User {} not found", id),
            OrderError::InvalidUser(msg) => write!(f, "Invalid user: {}", msg),
            OrderError::PaymentFailed(msg) => write!(f, "Payment failed: {}", msg),
        }
    }
}

pub fn process_order_advanced(db: &UserDatabase, order: &Order) -> Result<String, OrderError> {
    let user = find_user(db, order.user_id)
        .ok_or(OrderError::UserNotFound(order.user_id))?;
    
    validate_user(user)
        .map_err(|e| OrderError::InvalidUser(e))?;
    
    // Симуляция проверки платежа
    if order.amount > 1000.0 {
        return Err(OrderError::PaymentFailed("Amount too large".to_string()));
    }
    
    Ok(format!("Order processed for {}", user.name))
}

// Задание 2
pub fn validate_orders(orders: &[Order], user_db: &UserDatabase) -> Result<Vec<&Order>, OrderError> {
    let mut valid_orders = Vec::new();
    
    for order in orders {
        // Проверяем существование пользователя
        let user = find_user(user_db, order.user_id)
            .ok_or(OrderError::UserNotFound(order.user_id))?;
        
        // Проверяем валидность email
        validate_user(user)
            .map_err(|e| OrderError::InvalidUser(e))?;
        
        // Проверяем сумму заказа
        if order.amount > 1000.0 {
            return Err(OrderError::PaymentFailed(format!("Amount {} too large", order.amount)));
        }
        
        valid_orders.push(order);
    }
    
    Ok(valid_orders)
}

pub fn demonstrate_error_handling() {
    println!("\n=== Обработка ошибок ===");
    
    let mut user_db = UserDatabase::new();
    user_db.insert(1, User::new(1, "John Doe", "john@example.com"));
    user_db.insert(2, User::new(2, "Jane Smith", "jane@example.com"));
    user_db.insert(3, User::new(3, "Invalid User", "invalid-email"));
    
    let orders = vec![
        Order { user_id: 1, amount: 99.99, status: "completed".to_string() },
        Order { user_id: 2, amount: 149.99, status: "pending".to_string() },
        Order { user_id: 4, amount: 199.99, status: "shipped".to_string() },
        Order { user_id: 3, amount: 79.99, status: "processing".to_string() },
    ];
    
    // Обработка заказов с обработкой ошибок
    for order in &orders {
        match process_order(&user_db, order) {
            Ok((user, order)) => {
                println!("✅ Успешно обработан заказ для {}: ${}", user.name, order.amount);
            }
            Err(error) => {
                println!("❌ Ошибка обработки заказа: {}", error);
            }
        }
    }
    
    // Комбинаторы Option и Result
    let user_1_email = find_user(&user_db, 1)
        .map(|user| &user.email)
        .unwrap_or(&"Unknown".to_string());
    println!("Email пользователя 1: {}", user_1_email);
    
    // and_then для цепочки операций
    let result = find_user(&user_db, 1)
        .and_then(|user| validate_user(user).ok())
        .map(|user| user.name.clone());
    println!("Результат цепочки: {:?}", result);
}
