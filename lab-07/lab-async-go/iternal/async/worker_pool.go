package async

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// Task представляет задачу для обработки
type Task struct {
	ID   int
	Data interface{}
}

// Result представляет результат обработки задачи
type Result struct {
	TaskID int
	Output interface{}
	Error  error
}

// WorkerPool управляет пулом рабочих горутин
type WorkerPool struct {
	workersCount int
	tasks        chan Task
	results      chan Result
	wg           sync.WaitGroup
	ctx          context.Context
	cancel       context.CancelFunc
}

// NewWorkerPool создает новый пул рабочих
func NewWorkerPool(workers int) *WorkerPool {
	ctx, cancel := context.WithCancel(context.Background())
	return &WorkerPool{
		workersCount: workers,
		tasks:        make(chan Task, workers*2),
		results:      make(chan Result, workers*2),
		ctx:          ctx,
		cancel:       cancel,
	}
}

// Start запускает пул рабочих с функцией обработки
func (wp *WorkerPool) Start(processor func(Task) Result) {
	for i := 0; i < wp.workersCount; i++ {
		wp.wg.Add(1)
		go func(workerID int) {
			defer wp.wg.Done()
			for {
				select {
				case task, ok := <-wp.tasks:
					if !ok {
						return
					}
					result := processor(task)
					wp.results <- result
				case <-wp.ctx.Done():
					return
				}
			}
		}(i)
	}
}

// Submit отправляет задачу в пул
func (wp *WorkerPool) Submit(task Task) error {
	select {
	case wp.tasks <- task:
		return nil
	case <-wp.ctx.Done():
		return fmt.Errorf("worker pool is closed")
	}
}

// GetResults возвращает канал результатов
func (wp *WorkerPool) GetResults() <-chan Result {
	return wp.results
}

// Stop останавливает пул и закрывает каналы
func (wp *WorkerPool) Stop() {
	close(wp.tasks)
	wp.wg.Wait()
	close(wp.results)
}

// Close закрывает контекст пула
func (wp *WorkerPool) Close() {
	wp.cancel()
}

// DemoWorkerPool демонстрирует работу пула рабочих
func DemoWorkerPool() {
	numWorkers := 3
	numTasks := 10

	pool := NewWorkerPool(numWorkers)

	// Функция обработки задачи
	processor := func(task Task) Result {
		fmt.Printf("  Worker обрабатывает задачу %d\n", task.ID)
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
		return Result{
			TaskID: task.ID,
			Output: fmt.Sprintf("Результат задачи %d", task.ID),
			Error:  nil,
		}
	}

	pool.Start(processor)

	// Отправляем задачи
	fmt.Printf("Отправка %d задач в пул из %d рабочих:\n", numTasks, numWorkers)
	go func() {
		for i := 1; i <= numTasks; i++ {
			pool.Submit(Task{ID: i, Data: nil})
		}
		pool.Stop()
	}()

	// Обработка результатов
	fmt.Println("Результаты:")
	for result := range pool.GetResults() {
		fmt.Printf("  Задача %d: %v\n", result.TaskID, result.Output)
	}

	fmt.Println("Все задачи завершены")
}
