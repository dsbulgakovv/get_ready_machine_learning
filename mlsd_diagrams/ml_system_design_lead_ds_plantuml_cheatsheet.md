# ML System Design Interview Cheat Sheet — Lead DS / Analytics Developer

Редактируемый markdown-файл с диаграммами **PlantUML** для подготовки к ML System Design секции с упором на роль Lead DS.

## Как открыть preview в VS Code

Рекомендуемые расширения:

- **PlantUML** by jebbs
- **Markdown Preview Enhanced** или любой markdown preview, который умеет PlantUML
- Для рендера PlantUML локально может понадобиться Java + Graphviz

Обычно блоки в markdown пишутся так:

```plantuml
@startuml
...
@enduml
```

## Цветовая легенда

| Уровень | Цвет | Смысл |
|---|---:|---|
| Business | синий | бизнес-цель, пользователи, деньги, impact |
| Metrics | зелёный | продуктовые, ML, guardrail и системные метрики |
| Data | жёлтый | источники, фичи, качество данных, таргет |
| Model | фиолетовый | baseline, advanced models, ML formulation |
| Validation | оранжевый | offline validation, A/B, rollout |
| Production | серый | архитектура, API, storage, serving, monitoring |
| Team / Lead | красный | ownership, команда, риски, управление |

---

# 1. Главная схема: универсальный процесс ответа на ML/System Design секции

```plantuml
@startuml
title Universal ML System Design Answer Flow — Lead DS

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam roundcorner 20
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam ArrowColor #475569
skinparam ArrowThickness 1.4

skinparam activity {
  BackgroundColor #F8FAFC
  BorderColor #334155
  FontColor #0F172A
}

skinparam activityDiamond {
  BackgroundColor #FEF3C7
  BorderColor #F59E0B
}

start

partition "1. Business context" #DBEAFE {
  :Получил задачу / сервис / продуктовый кейс;
  :Уточнить бизнес-контекст;
  note right
    Кто пользователь?
    Какую бизнес-метрику улучшаем?
    Какая цена FP/FN?
    Batch или real-time?
    Ограничения: latency, privacy, cost, explainability
  end note

  :Сформулировать цель и success criteria;
  note right
    North Star:
    GMV, revenue, margin,
    retention, cost reduction,
    SLA, NPS
  end note
}

partition "2. Metric tree" #DCFCE7 {
  :Построить дерево метрик;
  note right
    Business:
    revenue, GMV, margin, retention

    Product:
    CTR, CVR, churn, activation, frequency

    Guardrails:
    latency, complaints, errors,
    fairness, infra cost, retention degradation
  end note
}

partition "3. ML formulation" #F3E8FF {
  :Перевести в ML / аналитическую задачу;

  if ("Тип задачи?") then ("classification")
    :Churn / fraud / propensity / moderation;
    note right
      Metrics:
      PR-AUC, ROC-AUC,
      Precision@K, Recall@K,
      calibration, expected profit
    end note
  elseif ("regression")
    :ETA / LTV / demand / price;
    note right
      Metrics:
      MAE, RMSE, WAPE,
      bias, quantile loss
    end note
  elseif ("ranking")
    :Search / recommendations / next-best-action;
    note right
      Metrics:
      NDCG@K, MAP@K,
      MRR, Recall@K, CTR/CVR
    end note
  elseif ("NLP / LLM / RAG")
    :QA / summarization / extraction / assistant;
    note right
      Metrics:
      retrieval Recall@K,
      groundedness,
      hallucination rate,
      human eval, cost
    end note
  elseif ("CV")
    :OCR / detection / moderation / quality control;
    note right
      Metrics:
      F1, mAP, IoU,
      CER/WER,
      manual review reduction
    end note
  else ("pricing / optimization")
    :Dynamic pricing / promo / bids / allocation;
    note right
      Metrics:
      margin, revenue,
      elasticity, conversion,
      long-term retention
    end note
  endif
}

partition "4. Data and features" #FEF9C3 {
  :Разобрать данные и фичи;
  note right
    Sources:
    logs, transactions, profiles,
    texts, images, CRM, support, external data

    Data quality:
    missing, duplicates, freshness,
    target leakage, label delay,
    train-serving skew

    Feature engineering:
    RFM, history, aggregates,
    embeddings, graph features,
    temporal and segment features
  end note
}

partition "5. Baseline and model approach" #F3E8FF {
  :Выбрать baseline;
  note right
    rules, SQL, popularity,
    logistic regression, CatBoost,
    BM25, moving average
  end note

  :Предложить advanced model;
  note right
    GBDT, ranking, two-tower,
    transformer, LLM, uplift,
    bandits, optimization
  end note

  :Обсудить trade-offs;
  note right
    quality vs latency
    quality vs cost
    explainability vs complexity
    offline quality vs online impact
  end note
}

partition "6. Offline validation" #FFEDD5 {
  :Провалидировать offline;
  note right
    Correct split:
    time-based, user-based,
    group-based, no leakage

    Offline metrics:
    AUC, PR-AUC, F1,
    NDCG, MAE, WAPE,
    calibration

    Business proxy:
    profit curve, expected value,
    saved cost, incremental LTV

    Segment analysis:
    regions, devices, cohorts,
    categories, high-value users
  end note
}

partition "7. Production design" #E2E8F0 {
  :Спроектировать production-систему;

  if ("Serving mode?") then ("Batch")
    :Batch scoring;
    note right
      Airflow / Spark / SQL
      → scores table
      → product consumes scores
    end note
  elseif ("Online")
    :Online inference;
    note right
      API → feature service
      → model serving
      → decision engine
    end note
  else ("Hybrid")
    :Hybrid serving;
    note right
      batch candidates/features
      + online reranking/scoring
    end note
  endif
}

partition "8. Online validation and A/B" #FFEDD5 {
  :Спланировать online validation / A-B test;
  note right
    Experiment:
    hypothesis, primary metric,
    guardrails, unit of randomization

    Quality checks:
    SRM, logging, overlap,
    pre-period balance

    Decision:
    effect size, CI,
    practical significance,
    segment stability

    Rollout:
    shadow → 1% → 5%
    → 25% → 50% → 100%
  end note
}

partition "9. Monitoring and operations" #E2E8F0 {
  :Настроить monitoring and operations;
  note right
    Data monitoring:
    freshness, missing rate,
    drift, schema changes

    Model monitoring:
    score distribution, calibration,
    quality by segment, retraining triggers

    Business monitoring:
    North Star, funnel, revenue,
    retention, complaints

    System monitoring:
    p50/p95/p99 latency,
    errors, throughput, queue lag, cost
  end note
}

partition "10. Team and lead ownership" #FEE2E2 {
  :Разложить команду и ownership;
  note right
    Lead role:
    goal, scope, trade-offs,
    design review, risk management,
    stakeholder sync

    Streams:
    Product / Analytics / Data /
    ML / Backend / MLOps / QA

    Lean team:
    MVP first, reuse platform,
    shared services,
    automate repeatable work
  end note

  :Final summary;
  note right
    business value
    + ML approach
    + architecture
    + experiment
    + team plan
  end note
}

stop
@enduml
```

---

# 2. Дерево метрик для любого кейса

```plantuml
@startmindmap
title Metric Tree — Business → Product → ML → Guardrails → Decision

skinparam backgroundColor #FFFFFF
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam shadowing false

<style>
mindmapDiagram {
  node {
    BackgroundColor #F8FAFC
    LineColor #334155
    FontColor #0F172A
  }
  :depth(1) {
    BackgroundColor #DBEAFE
    LineColor #2563EB
  }
  :depth(2) {
    BackgroundColor #DCFCE7
    LineColor #16A34A
  }
  :depth(3) {
    BackgroundColor #FEF9C3
    LineColor #CA8A04
  }
}
</style>

* Metric Tree
** Business / North Star
*** Revenue / GMV
*** Margin / profit
*** Retention / churn
*** Cost reduction
*** SLA / quality of service
*** NPS / CSAT
** Product metrics
*** CTR
*** CVR
*** Activation
*** Frequency
*** Time to value
*** Funnel conversion
*** Complaint / refund / cancellation rate
** ML metrics
*** Classification
**** ROC-AUC
**** PR-AUC
**** Precision@K
**** Recall@K
**** F1
**** LogLoss
**** Calibration
*** Regression
**** MAE
**** RMSE
**** WAPE
**** MAPE
**** Bias
**** Quantile loss
*** Ranking
**** NDCG@K
**** MAP@K
**** MRR
**** Recall@K
**** Coverage
**** Diversity
*** Forecasting
**** WAPE
**** sMAPE
**** Bias
**** Backtest error
**** Stockout / overstock
*** NLP / LLM / RAG
**** Retrieval Recall@K
**** Groundedness
**** Hallucination rate
**** Human eval
**** Cost
*** CV
**** F1
**** mAP
**** IoU
**** OCR CER/WER
**** Manual review reduction
** Guardrails
*** Latency
*** Error rate
*** Infra cost
*** Fairness / segment degradation
*** Privacy / safety
*** Long-term retention
*** User complaints
** Operational / system metrics
*** p50 / p95 / p99 latency
*** Throughput / RPS
*** CPU / GPU utilization
*** Queue lag
*** Availability
*** Cost per prediction
** Diagnostic metrics
*** Data freshness
*** Missing rate
*** Feature drift
*** Score distribution drift
*** Train-serving skew
*** Label delay
*** Quality by segment
** Decision logic
*** Ship if business metric improves
*** Guardrails are stable
*** Effect is practically significant
*** Segments do not degrade
*** Cost is acceptable

@endmindmap
```

---

# 3. Как не потеряться в доменах и выбрать подход

```plantuml
@startuml
title Domain Decision Map — How to Pick ML Approach

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam roundcorner 18
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam ArrowColor #475569

skinparam rectangle {
  BorderColor #334155
  FontColor #0F172A
}

rectangle "Получили домен / задачу" as A #DBEAFE
diamond "Что нужно сделать?" as B #FEF3C7

rectangle "Classification\n\nExamples:\nchurn, fraud, propensity, moderation\n\nModels:\nLogReg, CatBoost, LightGBM, NN\n\nMetrics:\nPR-AUC, Precision@K, Recall@K,\ncalibration, expected profit" as C #F3E8FF

rectangle "Regression\n\nExamples:\nETA, LTV, demand, revenue\n\nModels:\nlinear, CatBoost, LightGBM,\nquantile regression\n\nMetrics:\nMAE, RMSE, WAPE, bias,\nquantile loss" as D #F3E8FF

rectangle "Ranking\n\nExamples:\nsearch, ads, candidates,\nnext-best-action\n\nModels:\nBM25, LambdaMART, CatBoostRanker,\nneural reranker\n\nMetrics:\nNDCG@K, MRR, MAP@K,\nCTR, CVR" as E #F3E8FF

rectangle "Recommendation System\n\nArchitecture:\ncandidate generation → ranker\n→ reranker → business rules\n\nModels:\npopular baseline, collaborative filtering,\ntwo-tower, ranker\n\nMetrics:\nCTR, CVR, GMV, retention,\ndiversity, coverage" as F #F3E8FF

rectangle "Forecasting\n\nExamples:\ndemand, load, supply, revenue\n\nModels:\nnaive, moving average, ARIMA,\nCatBoost with lags, deep forecasting\n\nMetrics:\nWAPE, sMAPE, bias,\nservice level" as G #F3E8FF

rectangle "NLP / LLM\n\nExamples:\nclassification, NER, RAG,\nassistant, summarization\n\nModels:\nTF-IDF baseline, BERT,\nembeddings, LLM, RAG\n\nMetrics:\nF1, retrieval Recall@K,\ngroundedness, hallucination rate,\nhuman eval" as H #F3E8FF

rectangle "CV\n\nExamples:\nOCR, detection, moderation, defects\n\nModels:\nCNN, YOLO, ViT, OCR pipeline\n\nMetrics:\nF1, mAP, IoU,\nCER/WER, manual review reduction" as I #F3E8FF

rectangle "Optimization / Pricing\n\nExamples:\ndynamic pricing, promo,\nrouting, allocation\n\nApproach:\nelasticity, causal inference,\nuplift, bandits, constrained optimization\n\nMetrics:\nmargin, revenue, conversion,\nretention, fairness" as J #F3E8FF

rectangle "Fraud / Anomaly Detection\n\nExamples:\npayments, abuse, fake accounts, spam\n\nApproach:\nrules + ML + graph features\n+ human review\n\nMetrics:\nprevented loss,\nPrecision@review_capacity,\nFPR, user friction" as K #F3E8FF

rectangle "Always connect to business value" as L #DCFCE7
rectangle "Then design:\ndata → model → validation → production → A/B → monitoring → team plan" as M #E2E8F0

A --> B
B --> C : вероятность события
B --> D : число
B --> E : порядок объектов
B --> F : рекомендации
B --> G : будущее по времени
B --> H : смысл из текста
B --> I : изображения
B --> J : цена / действие / ресурс
B --> K : аномалии / злоупотребления

C --> L
D --> L
E --> L
F --> L
G --> L
H --> L
I --> L
J --> L
K --> L
L --> M

@enduml
```

---

# 4. Production ML architecture с ветвлением batch / online / hybrid

```plantuml
@startuml
title Production ML Architecture — Batch / Online / Hybrid

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam roundcorner 18
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam ArrowColor #475569
skinparam ArrowThickness 1.3

skinparam component {
  BorderColor #334155
  FontColor #0F172A
}

left to right direction

package "Data ingestion" #DBEAFE {
  [Product / business event] as Event
  [Event logging] as Logging
  [Kafka / streaming\nclicks, transactions, feedback] as Kafka #FEF9C3
  database "Data Lake / DWH\nraw logs, transactions, profiles" as DWH #FEF9C3
}

package "Feature engineering" #FEF9C3 {
  [ETL / ELT\nSpark / SQL / Airflow] as ETL
  [Stream processing\nFlink / Spark Streaming / consumers] as Stream
  database "Offline Feature Store" as OFS
  database "Online Feature Store\nRedis / low-latency storage" as OnFS
}

package "Training and registry" #F3E8FF {
  [Training dataset builder] as Builder
  [Model training pipeline] as Train
  [Offline evaluation] as Eval
  diamond "Pass quality gate?" as Gate #FEF3C7
  [Model Registry\nversioning, metadata,\nmetrics, approval] as Registry
  [Iterate\ndata fixes, features,\nmodel, target] as Iterate #FFEDD5
}

package "Serving" #E2E8F0 {
  diamond "Serving mode?" as Mode #FEF3C7

  [Batch inference job\ndaily/hourly scoring] as Batch
  database "Scores table /\nrecommendations table" as Scores
  [Product backend reads\nprecomputed scores] as BatchProduct

  [Online model serving\nREST/gRPC service] as Online
  [Decision engine\nbusiness rules, thresholds, fallback] as Decision
  [Product API response] as Response

  [Batch candidates /\nheavy features] as HybridBatch
  [Online lightweight reranker] as Reranker
  [Final decision / response] as HybridResponse
}

package "Experiment and rollout" #FFEDD5 {
  [Experiment / rollout layer] as Experiment
  [Shadow mode] as Shadow
  [A/B test] as AB
  [Gradual rollout] as Rollout
  [Rollback if guardrails fail] as Rollback
}

package "Monitoring and feedback" #DCFCE7 {
  [Data monitoring\nfreshness, missing, drift, schema] as DataMon
  [Model monitoring\nscore drift, calibration,\nquality by segment] as ModelMon
  [Business monitoring\nrevenue, conversion,\nretention, complaints] as BizMon
  [System monitoring\nlatency, errors, RPS,\nqueue lag, cost] as SysMon
  [Feedback loop] as Feedback
}

Event --> Logging
Logging --> Kafka
Logging --> DWH

DWH --> ETL
Kafka --> Stream
ETL --> OFS
Stream --> OnFS

OFS --> Builder
Builder --> Train
Train --> Eval
Eval --> Gate

Gate --> Iterate : no
Iterate --> Builder

Gate --> Registry : yes
Registry --> Mode

Mode --> Batch : batch scoring
Batch --> Scores
Scores --> BatchProduct

Mode --> Online : online inference
OnFS --> Online
Online --> Decision
Decision --> Response

Mode --> HybridBatch : hybrid
HybridBatch --> Reranker
OnFS --> Reranker
Reranker --> HybridResponse

BatchProduct --> Experiment
Response --> Experiment
HybridResponse --> Experiment

Experiment --> Shadow
Experiment --> AB
Experiment --> Rollout
Experiment --> Rollback

Shadow --> DataMon
AB --> ModelMon
Rollout --> BizMon
Rollback --> SysMon

DataMon --> Feedback
ModelMon --> Feedback
BizMon --> Feedback
SysMon --> Feedback

Feedback --> DWH
Feedback --> Kafka

@enduml
```

---

# 5. Команда и роль лида без раздувания штата

```plantuml
@startuml
title Team and Lead Ownership — Lean Delivery Model

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam roundcorner 18
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam ArrowColor #475569

center header
Lead DS should own framing, trade-offs, interfaces, quality bar and business impact,
not become a bottleneck for every implementation detail.
endheader

rectangle "Lead / owner of initiative" as Lead #FEE2E2

package "1. Align business goal" #DBEAFE {
  rectangle "Stakeholders\nbusiness owner, product, operations" as B1
  rectangle "Definition of success\nbusiness metric + product metric + guardrails" as B2
  rectangle "Scope and non-goals\nwhat is MVP, what is later" as B3
}

package "2. Decompose workstreams" #FEF9C3 {
  rectangle "Product / Analytics stream\n\nmetric tree, dashboard,\nA/B design, interpretation" as S1
  rectangle "Data Engineering stream\n\ndata sources, ETL,\nfeature pipelines, data quality" as S2
  rectangle "ML / DS stream\n\nbaseline, features, model,\noffline validation" as S3
  rectangle "Backend / Integration stream\n\nAPI, product integration,\ndecision engine, fallback" as S4
  rectangle "MLOps / Platform stream\n\nserving, registry, CI/CD,\nmonitoring, retraining" as S5
  rectangle "QA / Risk / Legal stream\n\ntest scenarios, privacy,\nsafety, edge cases" as S6
}

package "3. Decision framework" #DCFCE7 {
  rectangle "Design doc" as D1
  rectangle "Architecture review" as D2
  rectangle "Experiment review" as D3
  rectangle "Launch checklist" as D4
  rectangle "Rollback criteria" as D5
}

package "4. Risk management" #FFEDD5 {
  rectangle "Business risks\nwrong metric, cannibalization, no ROI" as R1
  rectangle "Data risks\nleakage, bias, label delay, bad logging" as R2
  rectangle "Model risks\ndrift, poor calibration, segment degradation" as R3
  rectangle "System risks\nlatency, downtime, cost, scaling" as R4
  rectangle "Org risks\nunclear ownership, dependencies, overengineering" as R5
}

package "5. Keep team lean" #F3E8FF {
  rectangle "Use MVP first" as L1
  rectangle "Reuse existing platform and shared services" as L2
  rectangle "One owner per stream,\nnot one person per task" as L3
  rectangle "Automate repeatable work" as L4
  rectangle "Human-in-the-loop only\nwhere risk is high" as L5
  rectangle "Scale team only after\nbusiness value is proven" as L6
}

package "Expected lead behavior" #FEE2E2 {
  rectangle "Lead does not do everything personally" as E1
  rectangle "Lead owns problem framing,\ntrade-offs, interfaces and quality bar" as E2
  rectangle "Lead keeps the project moving\nunder uncertainty" as E3
  rectangle "Lead communicates impact to business\nand details to engineers" as E4
}

Lead --> B1
Lead --> B2
Lead --> B3

Lead --> S1
Lead --> S2
Lead --> S3
Lead --> S4
Lead --> S5
Lead --> S6

Lead --> D1
D1 --> D2
D2 --> D3
D3 --> D4
D4 --> D5

Lead --> R1
Lead --> R2
Lead --> R3
Lead --> R4
Lead --> R5

Lead --> L1
Lead --> L2
Lead --> L3
Lead --> L4
Lead --> L5
Lead --> L6

B2 --> E2
D1 --> E2
R1 --> E3
L1 --> E1
L2 --> E3
E1 --> E4
E2 --> E4
E3 --> E4

@enduml
```

---

# 6. Как отвечать на секции именно в течение 1 часа

```plantuml
@startuml
title 60-Minute Interview Answer Timeline

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam roundcorner 18
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam ArrowColor #475569

left to right direction

rectangle "0–5 min\nClarify" as T1 #DBEAFE
rectangle "5–10 min\nBusiness goal\nand metrics" as T2 #DCFCE7
rectangle "10–20 min\nData and ML\nformulation" as T3 #FEF9C3
rectangle "20–30 min\nBaseline and\nadvanced model" as T4 #F3E8FF
rectangle "30–40 min\nProduction\narchitecture" as T5 #E2E8F0
rectangle "40–48 min\nValidation\nand A/B" as T6 #FFEDD5
rectangle "48–55 min\nTeam plan\nand risks" as T7 #FEE2E2
rectangle "55–60 min\nSummary and\ntrade-offs" as T8 #DBEAFE

note bottom of T1
Ask about:
users, goal, constraints,
latency, error cost
end note

note bottom of T2
North Star,
product metrics,
ML metrics,
guardrails
end note

note bottom of T3
Sources, target,
features, leakage,
label delay
end note

note bottom of T4
Simple baseline first,
then better model
if ROI exists
end note

note bottom of T5
Batch vs online vs hybrid,
storage, API, cache,
queue, monitoring
end note

note bottom of T6
Offline validation,
shadow mode, A/B,
rollout, rollback
end note

note bottom of T7
Streams, owners,
MVP, dependencies,
lean team
end note

note bottom of T8
Tie everything back
to business result
end note

T1 --> T2
T2 --> T3
T3 --> T4
T4 --> T5
T5 --> T6
T6 --> T7
T7 --> T8

@enduml
```

---

# 7. A/B и валидация модели

```plantuml
@startuml
title Model Validation and A/B Test Flow

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam roundcorner 18
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam ArrowColor #475569

start

partition "Offline validation" #FFEDD5 {
  :Model candidate is ready;
  :Correct split;
  note right
    time / user / group split
    no leakage
  end note

  :ML metrics;
  note right
    AUC, PR-AUC, F1,
    NDCG, MAE, WAPE,
    calibration
  end note

  :Business proxy;
  note right
    expected profit,
    saved cost,
    predicted uplift
  end note

  :Segment analysis;
  note right
    regions, devices,
    user cohorts,
    high-value users
  end note
}

if ("Offline quality good enough?") then ("No")
  :Iterate data, features,\ntarget, model, threshold;
else ("Yes")
endif

partition "Pre-production validation" #E2E8F0 {
  :Backtest if historical data;
  :Shadow mode if online decision;
  :Manual review if high-risk;
  :A/A test or logging validation;
}

if ("Ready for A/B?") then ("No")
  :Fix validation blockers;
else ("Yes")
endif

partition "A/B test design" #DCFCE7 {
  :Hypothesis;
  :Primary metric;
  :Guardrails;
  :Unit of randomization;
  note right
    user, session, geo,
    seller, courier,
    time bucket
  end note
  :MDE / power / sample size;
  :Duration and stopping rules;
}

partition "Run experiment" #DBEAFE {
  :Check SRM;
  :Check logging;
  :Check overlap / contamination;
  :Monitor guardrails;
}

partition "Analyze results" #FEF9C3 {
  :Statistical significance;
  :Practical significance;
  :Confidence intervals;
  :Segment stability;
  :Business impact and cost;
}

if ("Decision") then ("Ship")
  :Gradual rollout\n5% → 25% → 50% → 100%;
elseif ("Iterate")
  :Iterate;
else ("Rollback")
  :Rollback and postmortem;
endif

stop
@enduml
```

---

# 8. Компактная схема для запоминания: Senior answer loop

```plantuml
@startuml
title Senior Answer Loop — One-Line Mental Model

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam roundcorner 20
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam ArrowColor #475569
skinparam ArrowThickness 1.5

left to right direction

rectangle "Business\n\nWhat value?" as A #DBEAFE
rectangle "Metrics\n\nHow measure?" as B #DCFCE7
rectangle "Data\n\nCan we trust data?" as C #FEF9C3
rectangle "Model\n\nBaseline first" as D #F3E8FF
rectangle "Validation\n\nOffline + segments" as E #FFEDD5
rectangle "Production\n\nBatch / online / hybrid" as F #E2E8F0
rectangle "Experiment\n\nA/B + guardrails" as G #FFEDD5
rectangle "Monitoring\n\nDrift + latency + business" as H #E2E8F0
rectangle "Team\n\nOwners + lean team" as I #FEE2E2
rectangle "Business impact\n\nROI + rollout" as J #DBEAFE

A --> B
B --> C
C --> D
D --> E
E --> F
F --> G
G --> H
H --> I
I --> J
J --> A

@enduml
```

---

# 9. Версия, которую можно держать перед глазами на собесе

```plantuml
@startuml
title Interview Quick Reference — From Task to Business Impact

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam roundcorner 18
skinparam defaultFontName Inter
skinparam defaultFontSize 13
skinparam ArrowColor #475569

top to bottom direction

rectangle "Задача" as A #DBEAFE
rectangle "Уточняю бизнес" as B #DBEAFE
rectangle "Фиксирую цель" as C #DBEAFE
rectangle "Строю дерево метрик" as D #DCFCE7
rectangle "Формулирую ML-задачу" as E #F3E8FF
rectangle "Проверяю данные" as F #FEF9C3
rectangle "Делаю baseline" as G #F3E8FF
rectangle "Предлагаю advanced approach" as H #F3E8FF
rectangle "Валидирую offline" as I #FFEDD5
rectangle "Проектирую production" as J #E2E8F0
rectangle "Планирую A/B" as K #FFEDD5
rectangle "Мониторинг и rollout" as L #E2E8F0
rectangle "Команда и ownership" as M #FEE2E2
rectangle "Итог: business impact" as N #DBEAFE

A --> B
B --> C
C --> D
D --> E
E --> F
F --> G
G --> H
H --> I
I --> J
J --> K
K --> L
L --> M
M --> N

note right of B
Пользователь,
бизнес-цель,
ограничения,
цена ошибки
end note

note right of D
Business:
revenue, margin,
retention, cost, SLA

Product:
CTR, CVR, churn,
activation, frequency

ML:
AUC, PR-AUC,
NDCG, MAE, calibration

Guardrails:
latency, complaints,
errors, fairness, cost
end note

note right of F
Sources, target,
leakage, freshness,
label delay
end note

note right of G
Rules / SQL /
simple ML
end note

note right of H
GBDT / ranking /
NLP / CV / LLM /
uplift / optimization
end note

note right of I
Split, offline metrics,
segments, business proxy
end note

note right of J
Batch vs online vs hybrid,
API, DB, cache,
Kafka, feature store
end note

note right of K
Hypothesis,
primary metric,
guardrails,
randomization,
MDE, SRM
end note

note right of L
Shadow, staged rollout,
rollback criteria,
monitoring
end note

note right of M
Lead:
goal, trade-offs,
design review,
owners, lean team
end note

@enduml
```

---

# 10. Финальный фрейм, который стоит выучить

```text
Business → Metrics → Data → Model → Validation → Production → A/B → Monitoring → Team → Business Impact
```

## Как это звучит на интервью

> Я бы начал не с выбора модели, а с формализации бизнес-цели и цены ошибки. Затем построил бы дерево метрик: business, product, ML и guardrails. После этого проверил бы данные, leakage, задержку таргета и доступность фичей в момент принятия решения.
>
> Для MVP сделал бы простой baseline, чтобы быстро проверить гипотезу и получить нижнюю планку. Дальше выбрал бы модельный подход по типу задачи: classification, regression, ranking, NLP/CV, pricing или optimization.
>
> После offline validation я бы спроектировал production-контур: batch, online или hybrid serving, feature store, API, мониторинг, fallback и rollback. Решение о релизе принимал бы через A/B с primary metric, guardrails и проверкой практической значимости.
>
> Как lead я бы разложил работу на потоки, назначил owners, держал design review, управление рисками и связь с бизнес-метриками, не раздувая команду до доказанного business value.
