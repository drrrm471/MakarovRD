package async

import (
	"context"
	"testing"
	"time"
)

func TestMergeChannels(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	ch1 := make(chan int)
	ch2 := make(chan int)

	go func() {
		defer close(ch1)
		for i := 0; i < 3; i++ {
			ch1 <- i
		}
	}()

	go func() {
		defer close(ch2)
		for i := 3; i < 6; i++ {
			ch2 <- i
		}
	}()

	merged := MergeChannels(ctx, ch1, ch2)

	var results []int
	for val := range merged {
		results = append(results, val)
	}

	if len(results) != 6 {
		t.Errorf("Expected 6 values, got %d", len(results))
	}
}

func TestMergeChannelsContext(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())

	ch1 := make(chan int)
	go func() {
		for i := 0; i < 100; i++ {
			ch1 <- i
		}
	}()

	merged := MergeChannels(ctx, ch1)

	count := 0
	for val := range merged {
		count++
		if count >= 5 {
			cancel()
		}
		_ = val
	}

	if count < 5 {
		t.Errorf("Expected at least 5 values, got %d", count)
	}
}

func TestBufferedChannelProcessor(t *testing.T) {
	input := make(chan int, 5)

	for i := 1; i <= 5; i++ {
		input <- i
	}
	close(input)

	output := BufferedChannelProcessor(input, 3)

	expected := []int{2, 4, 6, 8, 10}
	var results []int

	for val := range output {
		results = append(results, val)
	}

	if len(results) != len(expected) {
		t.Errorf("Expected %d results, got %d", len(expected), len(results))
	}

	for i, val := range results {
		if val != expected[i] {
			t.Errorf("Expected %d at position %d, got %d", expected[i], i, val)
		}
	}
}

func TestBufferedChannelProcessorLarge(t *testing.T) {
	input := make(chan int, 100)

	for i := 1; i <= 100; i++ {
		input <- i
	}
	close(input)

	output := BufferedChannelProcessor(input, 10)

	count := 0
	for val := range output {
		count++
		if val%2 != 0 {
			t.Errorf("Expected even number, got %d", val)
		}
	}

	if count != 100 {
		t.Errorf("Expected 100 results, got %d", count)
	}
}

func TestChannelTimeout(t *testing.T) {
	ch := make(chan int)

	select {
	case <-ch:
		t.Error("Should not receive from channel")
	case <-time.After(50 * time.Millisecond):
		// Ожидаемое поведение
	}
}

func TestChannelClose(t *testing.T) {
	ch := make(chan int, 2)
	ch <- 1
	ch <- 2
	close(ch)

	count := 0
	for range ch {
		count++
	}

	if count != 2 {
		t.Errorf("Expected 2 values before close, got %d", count)
	}
}

func TestMultipleChannels(t *testing.T) {
	ctx := context.Background()
	chs := make([]<-chan int, 3)

	for i := 0; i < 3; i++ {
		ch := make(chan int)
		chs[i] = ch

		go func(c chan<- int, id int) {
			for j := 0; j < 3; j++ {
				c <- id*10 + j
			}
			close(c)
		}(ch, i)
	}

	merged := MergeChannels(ctx, chs...)

	var results []int
	for val := range merged {
		results = append(results, val)
	}

	if len(results) != 9 {
		t.Errorf("Expected 9 values, got %d", len(results))
	}
}

func BenchmarkBufferedChannelProcessor(b *testing.B) {
	input := make(chan int, b.N)
	for i := 0; i < b.N; i++ {
		input <- i
	}
	close(input)

	b.ResetTimer()
	output := BufferedChannelProcessor(input, 10)
	for range output {
	}
}

func TestChannelSend(t *testing.T) {
	ch := make(chan int)

	go func() {
		ch <- 42
	}()

	val := <-ch
	if val != 42 {
		t.Errorf("Expected 42, got %d", val)
	}
}
