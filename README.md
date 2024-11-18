# Yara: AI Beauty Agent 🌟

**Yara** is an intelligent AI-powered beauty assistant that provides personalized beauty recommendations, product suggestions, and style guidance in real-time. Using advanced AI and real-time data analysis, Yara serves as your personal beauty expert, understanding your unique features and preferences to deliver tailored recommendations.

~ _Developed by Perfect3sixty_

```mermaid
flowchart TD
    User[User Request] --> Assistant[AI Beauty Assistant]
    
    subgraph CoreSystem[Core System]
        Assistant --> UserProfile[User Profile Processing]
        UserProfile --> Preferences[Basic Preferences DB]
        Assistant --> RealtimeAI[Realtime AI Analysis]
    end
    
    subgraph DynamicData[Dynamic Data Layer]
        RealtimeAI --> WebScraper[AI Web Scraper]
        WebScraper --> ProductSearch[Product Search]
        WebScraper --> ReviewAnalysis[Review Analysis]
        WebScraper --> TrendAnalysis[Trend Analysis]
    end
    
    subgraph Processing[AI Processing]
        RealtimeAI --> ImageAnalysis[Image Analysis]
        RealtimeAI --> StyleMatching[Style Matching]
        RealtimeAI --> RecommendationEngine[Recommendation Engine]
    end
    
    DynamicData --> Processing
    Processing --> Response[Response to User]
```

## Development

```bash
python -m venv .venv

source .venv/Scripts/activate 
# or
source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload --port 7600
```


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Perfect3sixty - [@perfect3sixty](https://twitter.com/perfect3sixty)

Project Link: [https://github.com/perfect3sixty/yara](https://github.com/perfect3sixty/yara)

## Acknowledgments

- OpenAI for AI capabilities
