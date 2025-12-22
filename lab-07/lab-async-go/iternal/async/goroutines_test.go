package async

import (
	"fmt"
	"sync"
	"testing"
	"time"
)

func TestCounter(t *testing.T) {
	counter := &Counter{}
	var wg sync.WaitGroup
	
	// Запускаем 100 горутин для инкремента
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
		}()
	}
	
	wg.Wait()
	
	if counter.Value() != 100 {
		t.Errorf("Expected counter value 100, got %d", counter.Value())
	}
}

func TestCounterConcurrency(t *testing.T) {
	counter := &Counter{}
	var wg sync.WaitGroup
	numGoroutines := 1000
	
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
			time.Sleep(time.Microsecond)
			counter.Increment()
		}()
	}
	
	wg.Wait()
	
	expectedValue := numGoroutines * 2
	if counter.Value() != expectedValue {
		t.Errorf("Expected counter value %d, got %d", expectedValue, counter.Value())
	}
}

func TestProcessItems(t *testing.T) {
	items := []int{1, 2, 3, 4, 5}
	var processed []int
	var mu sync.Mutex
	
	processor := func(item int) {
		mu.Lock()
		defer mu.Unlock()
		processed = append(processed, item)
	}
	
	ProcessItems(items, processor)
	
	if len(processed) != len(items) {
		t.Errorf("Expected %d processed items, got %d", len(items), len(processed))
	}
	
	itemMap := make(map[int]bool)
	for _, item := range processed {
		itemMap[item] = true
	}
	
	for _, item := range items {
		if !itemMap[item] {
			t.Errorf("Item %d was not processed", item)
		}
	}
}

func TestProcessItemsLarge(t *testing.T) {
	items := make([]int, 100)
	for i := 0; i < 100; i++ {
		items[i] = i
	}
	
	var counter int
	var mu sync.Mutex
	
	processor := func(item int) {
		mu.Lock()
		defer mu.Unlock()
		counter++
	}
	
	ProcessItems(items, processor)
	
	if counter != 100 {
		t.Errorf("Expected 100 processed items, got %d", counter)
	}
}

func BenchmarkCounter(b *testing.B) {
	counter := &Counter{}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		counter.Increment()
	}
}

func BenchmarkCounterConcurrent(b *testing.B) {
	counter := &Counter{}
	var wg sync.WaitGroup
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
		}()
	}
	wg.Wait()
}

func TestGoroutinesPanic(t *testing.T) {
	// Проверяем, что паника в горутине не влияет на основную программу
	var wg sync.WaitGroup
	recovered := false
	
	wg.Add(1)
	go func() {
		defer wg.Done()
		defer func() {
			if r := recover(); r != nil {
				recovered = true
			}
		}()
		panic("test panic")
	}()
	
	wg.Wait()
	
	if !recovered {
		t.Error("Expected panic to be recovered")
	}
}

func ExampleCounter() {
	counter := &Counter{}
	
	for i := 0; i < 5; i++ {
		counter.Increment()
	}
	
	fmt.Printf("Counter value: %d\n", counter.Value())
	// Output: Counter value: 5
}
