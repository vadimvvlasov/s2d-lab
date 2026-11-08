# S2D Lab — Архитектурный принцип

**Дата утверждения:** 2026-11-08  
**Статус:** Стратегическое решение на весь срок жизни проекта

## Принцип

**S2D Lab — это система задач, артефактов и независимых проверок, а не система агентов, обменивающихся сообщениями.**

## Целевая архитектура

```
Task Backlog
    ↓
Agent (исполнитель одной ограниченной задачи)
    ↓
Artifact (сохранённый результат)
    ↓
Verifier (независимая проверка)
    ↓
Dependency Graph (определяет scope перепроверки)
    ↓
State Manager (гарантирует корректное продолжение)
```

### Компоненты

1. **Task Backlog** — определяет, что необходимо сделать
   - Извлечь вопросы из беседы
   - Исследовать вопрос Q1
   - Проверить Research Packet v1
   - Исправить Finding F-001

2. **Agent** — выполняет одну ограниченную задачу
   - Не постоянный собеседник
   - Не хранит контекст между вызовами
   - Получает явные входы, возвращает проверяемый артефакт
   - Четыре существующих агента остаются неизменными

3. **Artifact** — сохраняет результат
   - Версионированный (v1, v2, v3, v4)
   - С метаданными (source_refs, claim_ids, depends_on)
   - Неизменяемый после создания
   - Проверяемый (машинная валидация схемы)

4. **Verifier** — проверяет результат независимо
   - Read-only (никогда не редактирует артефакты)
   - Работает в отдельном контексте
   - Возвращает structured findings
   - Не принимает на веру чужие выводы

5. **Dependency Graph** — определяет scope перепроверки
   - Claim C1.2 depends_on C1.1
   - Изменение C1.1 → recheck C1.2
   - Differential audit = changed claims + dependencies + local regression
   - Не перепроверяет весь артефакт

6. **State Manager** — гарантирует корректное продолжение
   - Хранит run_id, artifact versions, cycle counts, CR statuses
   - Проверяет transitions (нет cycle > 3, нет PASS при BLOCKER)
   - Поддерживает resume после interruption
   - Детерминированная логика (не только LLM-инструкции)

## Почему эта архитектура оптимальна для RTX 3090

### Контекст-эффективность
- Один активный agent-вызов за раз (последовательное выполнение)
- Артефакты компактны (передаём выводы, не chain-of-thought)
- Source reading по необходимости (chunking, anchors)
- Не держим несколько полных копий беседы в памяти

### KV cache управление
- Последовательное выполнение → один активный KV cache
- Prefix caching для неизменного system prompt
- Selective loading артефактов (metadata vs. full body)
- Резерв 25-30% от 256k бюджета на непредвиденное

### Проверяемость
- Каждый артефакт имеет чёткую схему
- State transitions машинно-валидируемы
- Dependency graph определяет recheck scope
- Resume protocol детерминирован

### Масштабируемость
- Новая задача = новый task в backlog, не новый постоянный агент
- Dependency graph растёт с количеством claims, не с количеством агентов
- Structural tests не зависят от model quality

## Последствия для разработки

### Порядок реализации

**Сейчас (B3/B4):**
- Стабилизировать prompt contracts
- Определить, что agent получает и возвращает
- Проверить поведение на fixtures

**После валидации (C/D):**
- Формализовать artifact schemas
- Реализовать dependency tracking
- Построить state validator
- Реализовать resume protocol

**Не делать:**
- D2/D3 до завершения B3/B4
- Автоматизировать нестабильные контракты
- Строить сложную оркестрацию вокруг непроверенных prompts

### Что НЕ меняется

- Четыре существующих агента сохраняются
- UX команды `/recap` не меняется
- Bounded verifier loop (max 3 cycles)
- Release gate (no unresolved BLOCKER)
- Financial safety policies
- Evidence discipline

### Что меняется

- Agent становится stateless task executor, не conversational partner
- Передаём structured artifacts, не chat history
- Dependency graph определяет recheck scope явно
- State Manager обеспечивает deterministic control

## Примеры задач (Task Backlog)

### Intake Task
**Input:** conversation file  
**Agent:** research-lead  
**Output:** source.md, state.yaml (initial), task backlog  
**Next tasks:** extract-questions

### Extract Questions Task
**Input:** source.md  
**Agent:** conversation-analyst  
**Output:** question-map-v1.md  
**Next tasks:** audit-question-map-v1

### Audit Question Map Task
**Input:** source.md, question-map-v1.md  
**Agent:** independent-auditor  
**Output:** verification-report-qm-v1.md  
**Next tasks:** create-CRs (if CHANGES_REQUESTED) OR research-questions (if PASS)

### Fix Question Map Task (Cycle 1)
**Input:** source.md, question-map-v1.md, CR-001.md  
**Agent:** conversation-analyst  
**Output:** question-map-v2.md  
**Next tasks:** audit-question-map-v2-differential

### Research Question Task
**Input:** source.md, question-map-v2.md, question Q1  
**Agent:** quant-researcher  
**Output:** research-packet-v1.md (portion for Q1)  
**Next tasks:** research-question-Q2, ..., audit-research-packet-v1

## Переход к целевой архитектуре

### Фаза 1: Prompt Contracts (сейчас — B3/B4)
- Определить точные входы/выходы каждого agent
- Стабилизировать artifact structure
- Проверить на fixtures

### Фаза 2: Artifact Infrastructure (C1-C4)
- Schemas + validators
- Source indexing
- Token budget tracking
- Sequential scheduling

### Фаза 3: Dependency + State (D1-D4)
- Claim dependency graph
- State validator
- Resume protocol
- Source-first audit

### Фаза 4: Validation (E1-E3)
- Structural tests
- LLM behavior eval
- Adversarial cases

### Фаза 5: Production (F1-F2)
- Documentation
- Rollout

## Критерий успеха

Modernization успешна, когда:
1. Agent вызывается с explicit inputs, возвращает validatable artifact
2. Verifier работает независимо, без edit permissions
3. Dependency graph определяет recheck scope детерминированно
4. State Manager проверяет transitions программно
5. Resume работает without guessing
6. Всё это помещается в RTX 3090 при sequential execution

---

**Ключевое правило:** Не строить sophisticated orchestration вокруг unstable prompt contracts.

**Порядок работы:** A → B → C → D → E

**Текущий этап:** B (prompt refactoring) → проверка на fixtures → затем C/D
