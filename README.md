# 🧠 Breast Cancer Detection App (Ultrasound Based)

A deep learning-powered diagnostic web application for **Breast Cancer Detection** using **ultrasound images**. This Streamlit-based tool performs **tumor segmentation** and **classification** into **Benign**, **Malignant**, or **Normal** categories using pre-trained **PyTorch models**. It supports uploading custom images, selecting trained model (e.g., best), and generates a professional **PDF diagnostic report** with patient details and prediction results.


---

## 📦 Features

- Tumor segmentation using U-Net++
- Classification: **Benign**, **Malignant**, or **Normal**
- Web-based interface via Streamlit
- Generates downloadable PDF report
- Real-time predictions from uploaded images
- Built-in model options: best

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

### On Windows:
.venv\Scripts\activate

### On Linux/macOS:
source .venv/bin/activate


### ✅ Step 3: Install dependencies

If you have requirements.txt, run:

pip install -r requirements.txt

Or manually install:

pip install streamlit torch torchvision torchaudio
pip install opencv-python pillow albumentations segmentation-models-pytorch
pip install matplotlib seaborn fpdf scikit-learn tqdm

streamlit run app.py

![image](https://github.com/user-attachments/assets/172bff82-66b4-4c64-9686-d5bf15182d41)
![image](https://github.com/user-attachments/assets/de4a12be-f275-4df0-a7bf-8b68ae9415c1)
![image](https://github.com/user-attachments/assets/8dd758a6-4475-4022-8172-5089b5f4f16b)


🚀 Run the Application

streamlit run app.py

* Opens in browser: http://localhost:8501

* Upload an ultrasound image

* Fill in patient details

* View segmentation, classification, and download the report

📄 PDF Report Includes

* Patient Name, Age, Mobile, and Address

* Segmentation Output

* Timestamp

🔍 Notes
* Models: .pth files (BestModel) are loaded for prediction
* .venv/ and __pycache__/ should be excluded from Git commits
* App is fast, private, and self-contained

🛡️ Disclaimer

This tool is intended for educational and experimental use only. It is not a replacement for professional medical diagnosis. Always consult a dermatologist for accurate evaluation.


📧 Contact
Author: Vikas Sanchaniya
🔗 LinkedIn:https://www.linkedin.com/in/vikas-sanchaniya-31151a214/
📧 sanchaniyavikas@gmail.com


