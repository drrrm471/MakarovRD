package async

import (
	"context"
	"fmt"
	"testing"
	"time"
)

func TestWorkerPool(t *testing.T) {
	pool := NewWorkerPool(3)

	processor := func(task Task) Result {
		return Result{
			TaskID: task.ID,
			Output: task.ID * 2,
			Error:  nil,
		}
	}

	pool.Start(processor)

	// Отправляем 10 задач
	go func() {
		for i := 1; i <= 10; i++ {
			pool.Submit(Task{ID: i})
		}
		pool.Stop()
	}()

	// Проверяем результаты
	count := 0
	for result := range pool.GetResults() {
		count++
		if result.Output != result.TaskID*2 {
			t.Errorf("Expected %d, got %v", result.TaskID*2, result.Output)
		}
	}

	if count != 10 {
		t.Errorf("Expected 10 results, got %d", count)
	}
}

func TestWorkerPoolConcurrentSubmit(t *testing.T) {
	pool := NewWorkerPool(5)

	processor := func(task Task) Result {
		time.Sleep(time.Millisecond)
		return Result{
			TaskID: task.ID,
			Output: "done",
			Error:  nil,
		}
	}

	pool.Start(processor)

	// Конкурентная отправка задач
	go func() {
		for i := 1; i <= 50; i++ {
			pool.Submit(Task{ID: i})
		}
		time.Sleep(500 * time.Millisecond)
		pool.Stop()
	}()

	count := 0
	for range pool.GetResults() {
		count++
	}

	if count != 50 {
		t.Errorf("Expected 50 results, got %d", count)
	}
}

func TestWorkerPoolContext(t *testing.T) {
	pool := NewWorkerPool(2)

	processor := func(task Task) Result {
		return Result{
			TaskID: task.ID,
			Output: "done",
			Error:  nil,
		}
	}

	pool.Start(processor)

	// Отправляем несколько задач
	for i := 1; i <= 3; i++ {
		pool.Submit(Task{ID: i})
	}

	// Закрываем контекст
	pool.Close()
	pool.Stop()

	// Проверяем, что дальнейшие отправки невозможны
	err := pool.Submit(Task{ID: 100})
	if err == nil {
		t.Error("Expected error when submitting to closed pool")
	}
}

func TestWorkerPoolLarge(t *testing.T) {
	pool := NewWorkerPool(10)

	processor := func(task Task) Result {
		return Result{
			TaskID: task.ID,
			Output: task.ID * task.ID,
			Error:  nil,
		}
	}

	pool.Start(processor)

	numTasks := 1000
	go func() {
		for i := 1; i <= numTasks; i++ {
			pool.Submit(Task{ID: i})
		}
		pool.Stop()
	}()

	count := 0
	for result := range pool.GetResults() {
		count++
		expected := result.TaskID * result.TaskID
		if result.Output != expected {
			t.Errorf("Task %d: expected %d, got %v", result.TaskID, expected, result.Output)
		}
	}

	if count != numTasks {
		t.Errorf("Expected %d results, got %d", numTasks, count)
	}
}

func TestWorkerPoolWithTimeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	pool := NewWorkerPool(2)

	processor := func(task Task) Result {
		time.Sleep(50 * time.Millisecond)
		return Result{
			TaskID: task.ID,
			Output: "done",
			Error:  nil,
		}
	}

	pool.Start(processor)

	count := 0
	done := make(chan bool)

	go func() {
		for i := 1; i <= 100; i++ {
			select {
			case <-ctx.Done():
				return
			default:
				pool.Submit(Task{ID: i})
			}
		}
	}()

	go func() {
		for result := range pool.GetResults() {
			select {
			case <-ctx.Done():
				return
			default:
				count++
				_ = result
			}
		}
		done <- true
	}()

	<-ctx.Done()
	pool.Close()
	pool.Stop()

	if count == 0 {
		t.Error("Expected at least some results before timeout")
	}
}

func BenchmarkWorkerPool(b *testing.B) {
	pool := NewWorkerPool(4)

	processor := func(task Task) Result {
		return Result{
			TaskID: task.ID,
			Output: "done",
			Error:  nil,
		}
	}

	pool.Start(processor)

	go func() {
		for i := 0; i < b.N; i++ {
			pool.Submit(Task{ID: i})
		}
		pool.Stop()
	}()

	b.ResetTimer()
	for range pool.GetResults() {
	}
}

func TestWorkerPoolEmpty(t *testing.T) {
	pool := NewWorkerPool(3)

	processor := func(task Task) Result {
		return Result{
			TaskID: task.ID,
			Output: "done",
			Error:  nil,
		}
	}

	pool.Start(processor)
	close(pool.tasks)
	pool.wg.Wait()
	close(pool.results)

	count := 0
	for range pool.GetResults() {
		count++
	}

	if count != 0 {
		t.Errorf("Expected 0 results, got %d", count)
	}
}

func ExampleWorkerPool() {
	pool := NewWorkerPool(2)

	processor := func(task Task) Result {
		return Result{
			TaskID: task.ID,
			Output: fmt.Sprintf("Processed: %d", task.ID),
			Error:  nil,
		}
	}

	pool.Start(processor)

	go func() {
		for i := 1; i <= 3; i++ {
			pool.Submit(Task{ID: i})
		}
		pool.Stop()
	}()

	for result := range pool.GetResults() {
		fmt.Println(result.Output)
	}
	// Output:
	// Processed: 1
	// Processed: 2
	// Processed: 3
}
