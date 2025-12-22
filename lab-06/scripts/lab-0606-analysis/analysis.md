# analysis.md - Сравнительный анализ функционального программирования

## Сравнительная таблица языков

| Критерий | Haskell | Python | JavaScript | Scala | Rust |
|----------|---------|---------|-------------|-------|------|
| **Выразительность** | Очень высокая<br/>Point-free, comprehensions | Высокая<br/>List comprehensions | Высокая<br/>Arrow functions | Очень высокая<br/>For/yield | Средняя<br/>Iterator traits |
| **Безопасность типов** | Максимальная<br/>Полная статическая | Динамическая<br/>(mypy опционально) | Динамическая<br/>(TypeScript опционально) | Высокая<br/>Гибридная | Максимальная<br/>Ownership + traits |
| **Производительность** | Высокая<br/>Ленивые вычисления | Средняя<br/>Интерпретатор | Средняя<br/>V8 JIT | Высокая<br/>JVM оптимизации | Максимальная<br/>Zero-cost abstractions |
| **Иммутабельность** | По умолчанию<br/>Полная | По желанию<br/>frozen_dataclass | По желанию<br/>Spread syntax | По умолчанию<br/>case class | По умолчанию<br/>Строгая ownership |
| **Обработка ошибок** | Monadic (Maybe/Either)<br/>Композиционная | Исключения<br/>try/except | Исключения<br/>try/catch | Try/Either<br/>Функциональная | Result/Option<br/>Безопасная |
| **Кривая обучения** | Высокая<br/>Монды, ленивость | Низкая<br/>Интуитивный синтаксис | Низкая<br/>Веб-разработчики | Средняя<br/>JVM опыт | Высокая<br/>Borrow checker |
| **Экосистема** | Академическая<br/>lens, pipes, aeson | Огромная<br/>pandas, numpy, flask | Огромная<br/>lodash, React, Next.js | Промышленная<br/>Spark, Akka, Cats | Растущая<br/>tokio, serde, rayon |
