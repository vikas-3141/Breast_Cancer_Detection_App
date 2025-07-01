# 🧠 Breast Cancer Detection App (Ultrasound Based)
A deep learning-based Streamlit application for breast cancer diagnosis using ultrasound images. It supports tumor segmentation and classification (Benign vs. Malignant) using trained PyTorch models. Includes multiple trained models for performance comparison and a PDF diagnostic report generator.

This is a web-based diagnostic application for **Breast Cancer Detection** using **Ultrasound Images**. The app performs **tumor segmentation** and **classification** (Benign / Malignant / Normal) using deep learning (PyTorch), and it is built with **Streamlit** for an interactive UI.

---

## 📦 Features

- Tumor segmentation using U-Net++
- Classification: **Benign**, **Malignant**, or **Normal**
- Web-based interface via Streamlit
- Generates downloadable PDF report
- Real-time predictions from uploaded images
- Built-in model options: best, medium, and low accuracy

---

## 📁 Project Structure
📦 Breast_Cancer_Detection_App
├── .venv/ # Virtual environment (ignore during commit)
├── pycache/ # Python cache files (can ignore)
├── typings/ # Type hints or utility modules (ignore during commit)
├── app.py # Main Streamlit application 
├── BestModel.pth # performing model(ignore during commit)
├── Breast_Cancer.ipynb # Jupyter notebook for model development

---

## 🛠️ Installation & Setup

### ✅ Step 1: Clone the repository

git clone https://github.com/vikas-3141/Breast_Cancer_Detection_App.git
cd Breast_Cancer_Detection_App

### ✅ Step 2: Create and activate virtual environment

python -m .venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate


### ✅ Step 3: Install dependencies

If you have requirements.txt, run:

pip install -r requirements.txt

Or manually install:
pip install streamlit torch torchvision torchaudio
pip install opencv-python pillow albumentations segmentation-models-pytorch
pip install matplotlib seaborn fpdf scikit-learn tqdm


🚀 Run the Application

streamlit run app.py

* Opens in browser: http://localhost:8501

* Upload an ultrasound image

* Fill in patient details

* View segmentation, classification, and download the report

📄 PDF Report Includes

* Patient Name, Age, Mobile, and Address

* Uploaded Image

* Segmentation Output

* Classification Result

* Timestamp

🔍 Notes
* Models: .pth files (BestModel) are loaded for prediction
* .venv/ and __pycache__/ should be excluded from Git commits
* App is fast, private, and self-contained


📧 Contact
Author: Vikas Sanchaniya
🔗 LinkedIn:https://www.linkedin.com/in/vikas-sanchaniya-31151a214/
📧 sanchaniyavikas@gmail.com


