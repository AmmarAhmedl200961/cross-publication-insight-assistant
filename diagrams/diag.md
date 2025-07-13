```mermaid
graph TD
    A[Publication URLs] --> B[Publication Analyzer Agent]
    B --> C[Web Scraping Tool]
    B --> D[Keyword Extraction Tool]
    C --> E[Raw Content]
    D --> F[Keywords List]
    F --> G[Trend Aggregator Agent]
    G --> H[Data Analysis Tool]
    H --> I[Frequency Analysis]
    I --> J[Insight Generator Agent]
    J --> K[Final Report]
    
    style B fill:#e1f5fe
    style G fill:#f3e5f5  
    style J fill:#e8f5e8
```