use std::rc::Rc;
use std::fmt;

#[derive(Debug, Clone)]
enum List<T> {
    Empty,
    Cons(T, Rc<List<T>>),
}

impl<T: Clone + fmt::Debug> List<T> {
    fn new() -> Self {
        List::Empty
    }
    
    fn prepend(&self, elem: T) -> Self {
        List::Cons(elem, Rc::new(self.clone()))
    }
    
    fn head(&self) -> Option<&T> {
        match self {
            List::Cons(head, _) => Some(head),
            List::Empty => None,
        }
    }
    
    fn tail(&self) -> Option<&List<T>> {
        match self {
            List::Cons(_, tail) => Some(tail),
            List::Empty => None,
        }
    }
    
    fn iter(&self) -> ListIter<T> {
        ListIter { current: self }
    }
}

// Итератор для функционального списка
struct ListIter<'a, T> {
    current: &'a List<T>,
}

impl<'a, T> Iterator for ListIter<'a, T> {
    type Item = &'a T;
    
    fn next(&mut self) -> Option<Self::Item> {
        match self.current {
            List::Cons(head, tail) => {
                self.current = tail;
                Some(head)
            }
            List::Empty => None,
        }
    }
}

#[derive(Clone, Copy, Debug)]
pub struct Fibonacci {
    pub current: u64,
    pub next: u64,
}

impl Fibonacci {
    pub fn new() -> Self {
        Fibonacci { current: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u64;
    
    fn next(&mut self) -> Option<Self::Item> {
        let next = self.current + self.next;
        
        if next > u64::MAX - self.current {
            None
        } else {
            self.current = self.next;
            self.next = next;
            Some(self.current)
        }
    }
}

fn demonstrate_functional_structures() {
    println!("\n=== Функциональные структуры данных ===");
    
    // Создание списка в функциональном стиле
    let list = List::new()
        .prepend(3)
        .prepend(2)
        .prepend(1);
    
    println!("Функциональный список: {:?}", list);
    
    // Итерация по списку
    println!("Элементы списка:");
    for elem in list.iter() {
        println!("- {}", elem);
    }
    
    // Голова и хвост
    if let Some(head) = list.head() {
        println!("Голова списка: {}", head);
    }
    
    if let Some(tail) = list.tail() {
        println!("Хвост списка: {:?}", tail);
    }
}

pub fn demonstrate_functional_structures() {
    demonstrate_functional_structures();
    
    // Демонстрация неизменяемой точки
    let point1 = ImmutablePoint::new(0.0, 0.0);
    let point2 = point1.translate(3.0, 4.0);
    
    println!("Расстояние между {:?} и {:?} = {:.2}", 
             point1, point2, point1.distance(&point2));
}

// Неизменяемая структура данных
#[derive(Debug, Clone, Copy)]
struct ImmutablePoint {
    x: f64,
    y: f64,
}

impl ImmutablePoint {
    fn new(x: f64, y: f64) -> Self {
        ImmutablePoint { x, y }
    }
    
    // Вместо мутации возвращаем новую структуру
    fn translate(&self, dx: f64, dy: f64) -> Self {
        ImmutablePoint {
            x: self.x + dx,
            y: self.y + dy,
        }
    }
    
    fn distance(&self, other: &ImmutablePoint) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - 0.0).powi(2)).sqrt()
    }
}
