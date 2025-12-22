package main

import (
	"fmt"
	
	"lab-async-go/internal/async"
	"lab-async-go/internal/server"
)

func main() {
	fmt.Println("=== Демонстрация асинхронного программирования в Go ===\n")

	// Часть 1: Базовые горутины
	fmt.Println("--- 1. Базовые горутины и WaitGroup ---")
	async.DemoBasicGoroutines()
	fmt.Println()

	// Часть 2: Небуферизованные каналы
	fmt.Println("--- 2. Небуферизованные каналы ---")
	async.DemoUnbufferedChannels()
	fmt.Println()

	// Часть 3: Буферизованные каналы
	fmt.Println("--- 3. Буферизованные каналы ---")
	async.DemoBufferedChannels()
	fmt.Println()

	// Часть 4: Select с таймаутом
	fmt.Println("--- 4. Select с таймаутом ---")
	async.DemoSelectTimeout()
	fmt.Println()

	// Часть 5: Worker Pool
	fmt.Println("--- 5. Паттерн Worker Pool ---")
	async.DemoWorkerPool()
	fmt.Println()

	// Часть 6: HTTP сервер
	fmt.Println("--- 6. Многопоточный HTTP сервер ---")
	server.DemoHTTPServer()
}
