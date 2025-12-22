package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"sync/atomic"
	"time"
)

// HTTPServer представляет многопоточный HTTP сервер
type HTTPServer struct {
	server       *http.Server
	requestCount int64
	mu           sync.RWMutex
	activeConns  int64
}

// NewHTTPServer создает новый HTTP сервер
func NewHTTPServer(addr string) *HTTPServer {
	hs := &HTTPServer{}

	mux := http.NewServeMux()
	mux.HandleFunc("/", hs.handleRoot)
	mux.HandleFunc("/health", hs.handleHealth)
	mux.HandleFunc("/slow", hs.handleSlow)
	mux.HandleFunc("/stats", hs.handleStats)

	hs.server = &http.Server{
		Addr:    addr,
		Handler: mux,
	}

	return hs
}

// handleRoot основной обработчик
func (hs *HTTPServer) handleRoot(w http.ResponseWriter, r *http.Request) {
	count := atomic.AddInt64(&hs.requestCount, 1)
	atomic.AddInt64(&hs.activeConns, 1)
	defer atomic.AddInt64(&hs.activeConns, -1)

	time.Sleep(10 * time.Millisecond) // Имитация обработки

	w.Header().Set("Content-Type", "text/plain")
	fmt.Fprintf(w, "Hello! Request #%d\n", count)
	log.Printf("Handled request #%d from %s", count, r.RemoteAddr)
}

// handleHealth проверка здоровья сервера
func (hs *HTTPServer) handleHealth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprint(w, `{"status":"ok"}`)
}

// handleSlow медленный обработчик для тестирования
func (hs *HTTPServer) handleSlow(w http.ResponseWriter, r *http.Request) {
	atomic.AddInt64(&hs.activeConns, 1)
	defer atomic.AddInt64(&hs.activeConns, -1)

	time.Sleep(500 * time.Millisecond)
	w.Header().Set("Content-Type", "text/plain")
	fmt.Fprint(w, "Slow response\n")
}

// handleStats статистика сервера
func (hs *HTTPServer) handleStats(w http.ResponseWriter, r *http.Request) {
	count := atomic.LoadInt64(&hs.requestCount)
	active := atomic.LoadInt64(&hs.activeConns)

	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, `{"total_requests":%d,"active_connections":%d}`+"\n", count, active)
}

// Start запускает сервер
func (hs *HTTPServer) Start() error {
	log.Printf("Server starting on %s", hs.server.Addr)
	return hs.server.ListenAndServe()
}

// StartAsync запускает сервер асинхронно
func (hs *HTTPServer) StartAsync() {
	go func() {
		if err := hs.Start(); err != nil && err != http.ErrServerClosed {
			log.Printf("Server error: %v", err)
		}
	}()
}

// Shutdown корректно завершает работу сервера
func (hs *HTTPServer) Shutdown(ctx context.Context) error {
	log.Println("Server shutting down...")
	return hs.server.Shutdown(ctx)
}

// GetRequestCount возвращает количество обработанных запросов
func (hs *HTTPServer) GetRequestCount() int64 {
	return atomic.LoadInt64(&hs.requestCount)
}

// GetActiveConnections возвращает количество активных подключений
func (hs *HTTPServer) GetActiveConnections() int64 {
	return atomic.LoadInt64(&hs.activeConns)
}

// DemoHTTPServer демонстрирует работу HTTP сервера
func DemoHTTPServer() {
	server := NewHTTPServer(":8080")

	// Запускаем сервер асинхронно
	server.StartAsync()
	time.Sleep(500 * time.Millisecond)

	fmt.Println("HTTP сервер запущен на :8080")
	fmt.Println("Отправка пробных запросов...")

	// Отправляем несколько тестовых запросов
	client := &http.Client{Timeout: 5 * time.Second}
	var wg sync.WaitGroup

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			resp, err := client.Get("http://localhost:8080/")
			if err != nil {
				fmt.Printf("  Ошибка запроса %d: %v\n", id, err)
				return
			}
			defer resp.Body.Close()
			fmt.Printf("  Запрос %d выполнен (статус: %d)\n", id, resp.StatusCode)
		}(i)
	}

	wg.Wait()

	fmt.Printf("Статистика: %d запросов обработано\n", server.GetRequestCount())

	// Graceful shutdown
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		fmt.Printf("Ошибка при завершении: %v\n", err)
	} else {
		fmt.Println("Сервер корректно завершил работу")
	}
}

// RunWithGracefulShutdown запускает сервер с обработкой сигналов
func RunWithGracefulShutdown(addr string) {
	server := NewHTTPServer(addr)

	// Канал для сигналов
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt)

	// Запускаем сервер асинхронно
	server.StartAsync()

	fmt.Printf("Server running on %s\n", addr)
	fmt.Println("Press Ctrl+C to shutdown")

	// Ожидаем сигнала завершения
	<-sigChan

	fmt.Println("\nShutting down server...")
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Printf("Shutdown error: %v", err)
	} else {
		fmt.Println("Server shutdown gracefully")
	}
}
