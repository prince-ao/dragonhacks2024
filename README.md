
# Hear2Learn

Hear2Learn is an innovative accessible auditory  platform designed to increase your studying efficiency. It transcribes your lectures in real time so if you get distracted and miss something or mishear something you can catch up easily. After a lecture is recorded we summarize the lecture's core ideas and points. After that is done we create flash cards on the topic for more easily digestable information that can be repeated. We try to use the presenter's own words whenever possible to not generalize an idea since methodology can be taught differently.

This project was developed for Drexel University's 2024 DragonHacks and is hosted at [Hear2Learn.Tech](http://hear2learn.tech).

## Features

- **Real-time Audio Transcription**: Captures every word of your lecture as it happens.
- **Lecture Database**: Access past recordings anytime to review previous lectures.
- **Flashcards**: Quickly review key points from lectures using generated flashcards.
- **Lecture Summarization**: Summaries that highlight the main ideas of each lecture.

## Technologies Used

- **Jinja2**: Templating engine for Python, enhancing HTML integration.
- **Taipy**: Creates dynamic dashboards, useful for professor-side views.
- **Natural Language Processing**: Parses conversational presentations to identify core points.
- **Large Language Models (Mixtral and OpenAI)**: Summarizes texts effectively.
- **RAG (Retrieval Augmented Generation)**: Intended for quiz question generation, to be fully integrated later.
- **PyDub**: Handles audio transcription in real-time.
- **JavaScript**: Manages interactions and links between the platform's components.
- **SQLite**: A lightweight database for storing lecture data and supporting future dashboard implementations.

## Getting Started

### Prerequisites

- Python installed on your machine
- Pipenv for handling Python packages

### Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [project-directory]
   ```

2. Install dependencies using Pipenv:
   ```bash
   pipenv install
   ```

3. Start the application:
   ```bash
   pipenv run python run.py
   ```

4. Configure your `.env` file based on the provided `.env.example` template.

## Anticipated Features

- **Professor Integration**: Allows professors to track student engagement and review chatbot logs.
- **Enterprise/Academic Level Dashboards**: Provides detailed feedback on student performance and lesson engagement.
- **Advanced Audio Analysis**: Enhances the text conversion process for greater accuracy.
- **Machine Learning and RAG**: Generates quiz questions of varying difficulties.
- **Mobile Application**: Facilitates on-the-go access to platform resources.

## Contributing

Contributions are welcome! If you're interested in adding features, fixing bugs, or enhancing documentation, fork the repository and submit a pull request.

## Acknowledgments

Thank you to everyone who has contributed to making Hear2Learn a valuable resource for students and educators worldwide. Special thanks to Drexel University for hosting the 2024 DragonHacks.

---

For more information, visit [Hear2Learn.Tech](http://hear2learn.tech).
