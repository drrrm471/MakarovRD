// Main.scala
object Main {
  // Импорт необходимых case classes и функций
  import Collections.Product
  import ErrorHandling.{User, Order, findUser, validateUser}
  import SparkExample.SalesRecord
  
  def main(args: Array[String]): Unit = {
    println("=== Scala Функциональное Программирование ===")
    
    // Базовые операции
    BasicScala.main(Array())
    
    // Коллекции
    Collections.demonstrateCollections()
    
    // Обработка ошибок
    ErrorHandling.demonstrateErrorHandling()
    
    // Pattern matching
    PatternMatching.demonstratePatternMatching()
    
    println("\n" + "="*60)
    println("=== ПРАКТИЧЕСКИЕ ЗАДАНИЯ ===")
    println("="*60)
    
    // Задание 1: Анализ продаж
    println("\n1. Анализ продаж по категориям:")
    val salesData = List(
      SalesRecord("iPhone", "electronics", 999.99, "2024-01-15"),
      SalesRecord("MacBook", "electronics", 1999.99, "2024-01-15"),
      SalesRecord("T-shirt", "clothing", 29.99, "2024-01-16"),
      SalesRecord("Jeans", "clothing", 79.99, "2024-01-16"),
      SalesRecord("iPhone", "electronics", 999.99, "2024-01-17"),
      SalesRecord("Book", "education", 15.99, "2024-01-17")
    )
    
    def analyzeSales(sales: List[SalesRecord]): Map[String, (Double, Int)] = {
      sales
        .groupBy(_.category)
        .mapValues { categorySales =>
          val totalAmount = categorySales.map(_.amount).sum
          val count = categorySales.length
          (totalAmount, count)
        }
    }
    
    val salesAnalysis = analyzeSales(salesData)
    salesAnalysis.foreach { case (category, (total, count)) =>
      println(s"  $category: $${total} (${count} продаж)")
    }
    
    // Задание 2: Цепочка обработки заказа
    println("\n2. Обработка заказов с Either:")
    
    def processOrderPipeline(order: Order): Either[String, Double] = {
      for {
        user <- findUser(order.userId).toRight(s"User ${order.userId} not found")
        validatedUser <- validateUser(user)
        discount = if (order.amount > 100) 0.1 else 0.05
        finalAmount = order.amount * (1 - discount)
      } yield finalAmount
    }
    
    val testOrders = List(
      Order(1, 150.0, "completed"),
      Order(2, 80.0, "pending"),
      Order(3, 200.0, "shipped") // Пользователь не существует
    )
    
    testOrders.foreach { order =>
      processOrderPipeline(order) match {
        case Right(finalAmount) => 
          println(s"  Заказ userId=${order.userId}: $${order.amount} -> $${finalAmount} (OK)")
        case Left(error) => 
          println(s"  Заказ userId=${order.userId}: ОШИБКА - $error")
      }
    }
    
    // Задание 3: Spark отчет (требует Spark)
    println("\n3. Spark отчет (раскомментируйте для выполнения):")
    println("   // SparkExample.main(Array())")
    
    println("\n" + "="*60)
    println("=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")
    println("="*60)
  }
}
