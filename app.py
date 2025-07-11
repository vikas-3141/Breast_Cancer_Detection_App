import streamlit as st
import torch
import cv2
import numpy as np
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
import segmentation_models_pytorch as smp
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import datetime

# Model Definition
class MultiTaskModel(torch.nn.Module):
    def __init__(self, backbone='resnet34', num_classes=3):
        super().__init__()
        self.backbone = smp.UnetPlusPlus(
            encoder_name=backbone, encoder_weights=None, in_channels=1, classes=1, activation='sigmoid'
        )
        self.pool = torch.nn.AdaptiveAvgPool2d(1)
        self.fc = torch.nn.Linear(512, num_classes)

    def forward(self, x):
        seg_output = self.backbone(x)
        enc_feat = self.backbone.encoder(x)[-1]
        cls_output = self.pool(enc_feat).view(enc_feat.size(0), -1)
        cls_output = self.fc(cls_output)
        normal_mask = (torch.argmax(cls_output, dim=1) == 0).float().unsqueeze(1).unsqueeze(2).unsqueeze(3)
        seg_output = seg_output * (1 - normal_mask)
        return seg_output, cls_output

# Refine Predictions
def refine_predictions(seg_pred, cls_pred):
    normal_probs = torch.softmax(cls_pred, dim=1)[:, 0].unsqueeze(1).unsqueeze(2).unsqueeze(3)
    return seg_pred * (1 - normal_probs)

# Image Transformation
val_transform = A.Compose([
    A.Resize(256, 256),
    A.Normalize(mean=0.5, std=0.5),
    ToTensorV2()
])

# Load Model
@st.cache_resource
def load_model():
    model = MultiTaskModel().cpu()
    model.load_state_dict(torch.load('D:/Projects Machine Learning/Breast Cancer/BestModel.pth', map_location=torch.device('cpu')))
    model.eval()
    return model

# PDF Generation Function
def generate_pdf(name, age, mobile, address, prediction, confidence):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Breast Cancer Diagnostic Report", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Generated by AI Diagnostic System", ln=True, align='C')
    pdf.ln(10)

    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.cell(0, 10, f"Date: {datetime.date.today().strftime('%B %d, %Y')}", ln=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Patient Information:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"Age: {age}", ln=True)
    pdf.cell(0, 10, f"Mobile No: {mobile}", ln=True)
    pdf.multi_cell(0, 10, f"Address: {address}")

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Diagnosis Result:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f" Prediction: {prediction} (Confidence: {confidence:.2f}%)", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, "This report is generated based on AI analysis and is not a substitute for professional medical advice.")

    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Doctor Signature: ____________________", ln=True)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# Streamlit App
st.title("Breast Ultrasound Tumor Segmentation and Classification")
st.write("Upload an ultrasound image to get segmentation and classification results.")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Image processing
    image = Image.open(uploaded_file).convert('L')
    image_np = np.array(image)
    augmented = val_transform(image=image_np)
    image_tensor = augmented['image'].unsqueeze(0)

    # Model prediction
    model = load_model()
    with torch.no_grad():
        seg_pred, cls_pred = model(image_tensor.cpu())
        seg_pred = refine_predictions(seg_pred, cls_pred)
        seg_pred = (seg_pred.squeeze().cpu().numpy() > 0.5).astype(np.uint8) * 255
        cls_pred = torch.softmax(cls_pred, dim=1).cpu().numpy()[0]
        predicted_class = np.argmax(cls_pred)
        class_names = ['Normal', 'Benign', 'Malignant']
        predicted_label = class_names[predicted_class]
        confidence = cls_pred[predicted_class] * 100

    # Show results
    st.subheader("Results")
    col1, col2 = st.columns(2)

    with col1:
        st.image(image_np, caption="Input Image", use_container_width=True, clamp=True)

    with col2:
        st.image(seg_pred, caption="Predicted Segmentation Mask", use_container_width=True, clamp=True)

    st.write(f" **✅ Predicted Class**: {predicted_label} ({confidence:.2f}% confidence)")

    # Show bar chart
    fig, ax = plt.subplots()
    ax.bar(class_names, cls_pred * 100)
    ax.set_ylabel("Probability (%)")
    ax.set_title("Classification Probabilities")
    st.pyplot(fig)

    # PDF Export Section
    with st.expander("📄 Generate PDF Diagnostic Report"):
        name = st.text_input("Patient Name")
        age = st.number_input("Patient Age", min_value=1, max_value=120, step=1)
        mobile = st.text_input("Mobile Number")
        address = st.text_area("Patient Address")

        if st.button("Generate Report PDF"):
            # Validation checks
            if not name.strip():
                st.error("Patient name is required.")
            elif not mobile.isdigit() or len(mobile) != 10:
                st.error("Please enter a valid 10-digit mobile number.")
            elif not address.strip():
                st.error("Patient address is required.")
            else:
                pdf_path = generate_pdf(name, age, mobile, address, predicted_label, confidence)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download PDF",
                        data=f,
                        file_name=f"{name.replace(' ', '_')}_diagnostic_report.pdf",
                        mime="application/pdf"
                    )


# Instructions
st.write("""
### Instructions
1. Upload a grayscale ultrasound image (PNG, JPG, or JPEG format).
2. The model will predict the tumor type (Normal, Benign, or Malignant) and display the segmentation mask.
3. The segmentation mask highlights the tumor region (if any) in the image.
4. You can generate a diagnostic PDF report with patient details.
""")
