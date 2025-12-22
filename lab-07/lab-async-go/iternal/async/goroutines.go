package async

import (
	"fmt"
	"sync"
	"time"
)

// Counter - потокобезопасный счетчик с мьютексом
type Counter struct {
	mu    sync.Mutex
	value int
}

// Increment увеличивает счетчик на 1
func (c *Counter) Increment() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
}

// Value возвращает текущее значение счетчика
func (c *Counter) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

// ProcessItems запускает горутины для обработки элементов
func ProcessItems(items []int, processor func(int)) {
	var wg sync.WaitGroup
	for _, item := range items {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			processor(i)
			time.Sleep(10 * time.Millisecond)
		}(item)
	}
	wg.Wait()
}

// DemoBasicGoroutines демонстрирует базовые горутины и WaitGroup
func DemoBasicGoroutines() {
	fmt.Println("Запуск 5 горутин с WaitGroup:")
	
	var wg sync.WaitGroup
	
	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			fmt.Printf("  Worker %d started\n", id)
			time.Sleep(100 * time.Millisecond)
			fmt.Printf("  Worker %d completed\n", id)
		}(i)
	}
	
	wg.Wait()
	fmt.Println("Все горутины завершены")
}

// DemoCounterConcurrency демонстрирует конкурентный доступ
func DemoCounterConcurrency() {
	counter := &Counter{}
	var wg sync.WaitGroup
	
	fmt.Println("Конкурентный доступ к счетчику (100 горутин):")
	
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
		}()
	}
	
	wg.Wait()
	fmt.Printf("  Финальное значение: %d\n", counter.Value())
}
