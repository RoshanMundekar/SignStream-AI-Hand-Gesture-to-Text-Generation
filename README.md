# SignStream AI: Hand Gesture to Text Generation

SignStream AI is a modern, real-time hand gesture recognition platform that translates sign language into digital text. Using deep learning (CNN) and advanced computer vision, it provides an intuitive interface for both live detection and custom gesture dataset creation.

![SignStream AI Banner](https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/hand.svg)


---

## Demo Video
Watch here:https://drive.google.com/file/d/1LsUM8MMosxA44UfzbZ94ona_819YZ4wM/view?usp=drive_link

---


## 🌟 Key Features

- **Embedded Live Detection**: Real-time camera feed integrated directly into the browser (no more separate OpenCV popups).
- **Interactive AI Console**: Live prediction feedback with confidence indicators and performance metrics.
- **Dataset Trainer**: Easily record and label thousands of new hand gesture samples to expand the model's vocabulary.
- **Professional Dashboard**: A glassmorphic, responsive UI built with Tailwind CSS and Lucide Icons.
- **Privacy Focused**: All processing happens locally on your machine via Flask and TensorFlow.

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Deep Learning**: TensorFlow, TFLearn (CNN Architecture)
- **Computer Vision**: OpenCV (CV2)
- **Frontend**: Tailwind CSS, Vanilla JavaScript, Lucide Icons
- **Database**: MySQL

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MySQL Server
- Webcam

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/hand-to-text-ai.git
   cd UI
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install flask flask-mysql opencv-python tensorflow==2.12.0 tflearn numpy pillow
   ```

4. **Initialize Database**:
   - Import the provided `final_db.sql` into your MySQL server.
   - Update the database credentials in `app.py`.

### Running the Application

```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your web browser.

## 📁 Project Structure

```text
UI/
├── app.py              # Main Flask application & AI Logic
├── final_db.sql        # Database schema
├── static/             # CSS, Images, and uploaded assets
├── templates/          # Jinja2 HTML templates (Modern UI)
│   ├── base.html       # Global layout & design system
│   ├── userDetails.html # Main AI Command Center
│   └── ...
└── Major Project/      # Trained models and dataset storage
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support
For support or inquiries, please reach out to `hello@signstream.ai`.

---
*Developed with  to empower digital accessibility.*
