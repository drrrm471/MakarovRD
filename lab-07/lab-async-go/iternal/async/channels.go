package async

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// MergeChannels объединяет несколько каналов в один
func MergeChannels(ctx context.Context, chs ...<-chan int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup

	multiplex := func(c <-chan int) {
		defer wg.Done()
		for {
			select {
			case val, ok := <-c:
				if !ok {
					return
				}
				select {
				case out <- val:
				case <-ctx.Done():
					return
				}
			case <-ctx.Done():
				return
			}
		}
	}

	wg.Add(len(chs))
	for _, c := range chs {
		go multiplex(c)
	}

	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

// BufferedChannelProcessor обрабатывает элементы буферизованного канала
func BufferedChannelProcessor(input <-chan int, bufferSize int) <-chan int {
	output := make(chan int, bufferSize)

	go func() {
		defer close(output)
		for val := range input {
			output <- val * 2
		}
	}()

	return output
}

// DemoUnbufferedChannels демонстрирует небуферизованные каналы
func DemoUnbufferedChannels() {
	ch := make(chan int)

	go func() {
		for i := 1; i <= 3; i++ {
			fmt.Printf("  Отправка: %d\n", i)
			ch <- i
		}
		close(ch)
	}()

	fmt.Println("Получение данных:")
	for val := range ch {
		fmt.Printf("  Получено: %d\n", val)
	}
}

// DemoBufferedChannels демонстрирует буферизованные каналы
func DemoBufferedChannels() {
	ch := make(chan int, 3)

	fmt.Println("Отправка в буферизованный канал:")
	for i := 1; i <= 3; i++ {
		ch <- i
		fmt.Printf("  Отправлено: %d\n", i)
	}
	close(ch)

	fmt.Println("Получение из буферизованного канала:")
	for val := range ch {
		fmt.Printf("  Получено: %d\n", val)
	}
}

// DemoSelectTimeout демонстрирует select с таймаутом
func DemoSelectTimeout() {
	ch := make(chan string)

	go func() {
		time.Sleep(500 * time.Millisecond)
		ch <- "Данные пришли!"
	}()

	fmt.Println("Ожидание данных с таймаутом 1 сек:")
	select {
	case msg := <-ch:
		fmt.Printf("  Получено: %s\n", msg)
	case <-time.After(1 * time.Second):
		fmt.Println("  Таймаут истек")
	}

	fmt.Println("Ожидание данных с таймаутом 100 мс (истечет):")
	ch2 := make(chan string)
	select {
	case msg := <-ch2:
		fmt.Printf("  Получено: %s\n", msg)
	case <-time.After(100 * time.Millisecond):
		fmt.Println("  Таймаут истек")
	}
}
