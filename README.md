# 🌍 AI Trip Planner

> An intelligent travel companion that creates personalized itineraries using AI technology.
![Trip Planner - Your AI Travel Companion]([git.png](https://github.com/patelvandan11/Ai-Trip-Planner/blob/main/Frontend/public/git.png))
*AI Trip Planner helps you create personalized travel itineraries with intelligent recommendations and real-time weather updates.(Ongoing)*
[![Made with React](https://img.shields.io/badge/Made%20with-React-61DAFB?style=flat-square&logo=react)](https://reactjs.org/)
[![API](https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![AI](https://img.shields.io/badge/AI-OpenAI%20GPT-412991?style=flat-square&logo=openai)](https://openai.com/)

## ✨ Features

- 🌤️ Real-time weather forecasts for destinations
- 🤖 AI-powered intelligent trip planning
- 💬 Interactive chat interface
- ⚙️ Customizable travel preferences

## 🛠️ Tech Stack

- **Frontend:** React.js
- **Backend:** FastAPI (Python)
- **AI Engine:** OpenAI GPT
- **External APIs:** Weather Integration

## 🚀 Getting Started

### Backend Setup

1. Clone and navigate:
   ```bash
   cd Ai-Trip-Planner/Backend
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```env
   WEATHER_API_KEY=your_weather_api_key
   OPENAI_API_KEY=your_openai_api_key
   MODEL_ID=your_model_id
   ```

5. Launch server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to frontend:
   ```bash
   cd Ai-Trip-Planner/Frontend
   ```

2. Install packages:
   ```bash
   npm install
   ```

3. Start development:
   ```bash
   npm run dev
   ```

## 🔑 Environment Variables

Required environment variables:
- `WEATHER_API_KEY`: OpenWeatherMap API key
- `OPENAI_API_KEY`: OpenAI API key
- `MODEL_ID`: OpenAI model identifier

## 🤝 Contributing

Your contributions are welcome! Feel free to submit issues and enhancement requests.

## 📝 License

[MIT License](LICENSE)
