# DDLC Worlds Apart

Immerse yourself in an unparalleled dialogue experience with the members of the Literature Club. DDLC AI extends beyond pre-scripted responses, introducing fluid, generative, and memory-rich interactions.

![DDLC AI Banner](path-to-your-banner-image-if-you-have-one.png)

## Table of Contents

- [About](#about) 📖
- [Features](#features) 🎮
- [Technology](#technology) 🧠
- [Installation](#installation) 🛠️
- [Credits](#credits) 🙏
- [License](#license) 📜

## About

DDLC AI reimagines the way you engage with the Literature Club members. While the current version places you in the familiar clubroom, future iterations will unveil more environments and opportunities for exploration.

**Character Status:**
- **Monika**: 🟢 Active
- **Sayori**: 🟠 Coming Soon
- **Natsuki**: 🟠 Coming Soon
- **Yuri**: 🟠 Coming Soon
- **MC**: ❓

## Features

- **Generative Conversations**: Speak freely and receive human-like responses.
- **Memory-Rich Interactions**: The AI recalls past discussions, making every conversation nuanced and unique.
- **Expansive Environments**: The clubroom is just the beginning.

## Technology

At the core of DDLC AI is a Generative Agent, inspired by cutting-edge research from Google and Stanford University. Powering these interactions is ChatGPT, specifically the `gpt-3.5-turbo` variant, boasting 175 billion parameters.

📄 [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/pdf/2304.03442.pdf)

Our bespoke implementation introduces optimizations, ensuring faster and seamless dialogues. A cornerstone of our project is the long-term memory system, obviating the conventional token limitations and archiving essential memories in MongoDB. Note: Usage of ChatGPT necessitates charges for the OpenAI API.

## Installation

**Prerequisites**:

1. [Ren'Py](https://www.renpy.org/latest.html) - The heart of DDLC.
2. [Python](https://www.python.org/downloads/) - For backend processes.
3. DDLC AI Repository.

**Setup**:

1. Clone or download this repository.
2. Navigate to the project directory.
3. Initiate a virtual environment:
```bash
python -m venv env
```
4. Activate the virtual environment:
```bash
env\Scripts\activate
```
5. Install dependencies:
```bash
pip install -r requirements.txt
```
6. Configure your .env:
  `OPENAI`: Your OpenAI API Key.
  `MONGO_URI`: Your MongoDB Connection URI.
7. Boot up Ren'Py, select "DDLC Hope", and initiate your experience.

## Credits
A heartfelt appreciation to Google, Stanford University, and OpenAI for their invaluable research and tools. This project stands on the shoulders of their pioneering work.

