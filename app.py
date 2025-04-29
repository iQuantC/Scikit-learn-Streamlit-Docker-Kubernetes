import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
from io import BytesIO
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

# Load data
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target
labels = iris.target_names

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Evaluation
report = classification_report(y_test, y_pred, target_names=labels)
conf_matrix = confusion_matrix(y_test, y_pred)
accuracy = clf.score(X_test, y_test)

# Streamlit App
st.set_page_config(page_title="Iris Classifier", layout="wide")
st.title("🌸 Iris Flower Classification - Streamlit ML App")

# Show raw data
if st.checkbox("📊 Show Raw Data"):
    st.write(X)

# Model Summary
model_summary = f"""
Model: RandomForestClassifier
Training set size: {len(X_train)}
Test set size: {len(X_test)}
Model accuracy: {accuracy:.2f}
"""
st.subheader("🧠 Model Summary")
st.text(model_summary)

# Classification Report
st.subheader("📄 Classification Report")
st.text(report)

# Confusion Matrix Plot
st.subheader("🔍 Confusion Matrix")
fig_conf, ax_conf = plt.subplots()
sns.heatmap(conf_matrix, annot=True, fmt='d',
            xticklabels=labels, yticklabels=labels, cmap="YlGnBu", ax=ax_conf)
st.pyplot(fig_conf)

# Feature Importance Plot
st.subheader("📌 Feature Importance")
fig_feat, ax_feat = plt.subplots()
pd.Series(clf.feature_importances_, index=X.columns).sort_values().plot(kind='barh', color='teal', ax=ax_feat)
st.pyplot(fig_feat)

# Sidebar Input
st.sidebar.header("🔍 Predict New Sample")
sepal_length = st.sidebar.slider("Sepal length (cm)", float(X.min()[0]), float(X.max()[0]), float(X.mean()[0]))
sepal_width = st.sidebar.slider("Sepal width (cm)", float(X.min()[1]), float(X.max()[1]), float(X.mean()[1]))
petal_length = st.sidebar.slider("Petal length (cm)", float(X.min()[2]), float(X.max()[2]), float(X.mean()[2]))
petal_width = st.sidebar.slider("Petal width (cm)", float(X.min()[3]), float(X.max()[3]), float(X.mean()[3]))

sample = [[sepal_length, sepal_width, petal_length, petal_width]]
prediction = clf.predict(sample)
st.sidebar.success(f"🌸 Prediction: {labels[prediction[0]]}")

# Video
st.subheader("🎥 Learn About iQuant YouTube Channel")
st.video("https://youtu.be/MwmuwhwzGTk?si=Rv6qUAsX8vTarvYN")

# Generate PDF with plots
def generate_pdf_with_plots(report_text, model_summary_text, fig_conf, fig_feat):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    #---- Page 1 ----
    # Add model summary
    text = c.beginText(40, height - 40)
    text.setFont("Helvetica-Bold", 12)
    text.textLine("Model Summary")
    text.setFont("Helvetica", 10)
    for line in model_summary_text.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Add classification report
    #y_position -= 120
    #text = c.beginText(40, y_position)
    text = c.beginText(40, height - 180)
    text.setFont("Helvetica-Bold", 12)
    text.textLine("Classification Report")
    text.setFont("Helvetica", 10)
    for line in report_text.split('\n'):
        text.textLine(line)
    c.drawText(text)

    c.showPage()
    
    # ---- Page 2 ----
    # Save confusion matrix image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_conf:
        fig_conf.savefig(tmp_conf.name, bbox_inches='tight')
        c.drawImage(ImageReader(tmp_conf.name), 40, height - 470, width=250, preserveAspectRatio=True)

    # Save feature importance image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_feat:
        fig_feat.savefig(tmp_feat.name, bbox_inches='tight')
        c.drawImage(ImageReader(tmp_feat.name), 320, height - 470, width=250, preserveAspectRatio=True)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# PDF Export Button
if st.button("📝 Download Full PDF Report"):
    pdf = generate_pdf_with_plots(report, model_summary, fig_conf, fig_feat)
    st.download_button("📥 Download PDF", pdf, file_name="iris_detailed_report.pdf", mime="application/pdf")
