import streamlit as st
from PIL import Image
import numpy as np
from backend import FuelDocumentProcessor

st.title("🚗 Hệ thống Quản lý & Đối chiếu Đa chứng từ Xăng dầu")

# Khởi tạo processor backend
processor = FuelDocumentProcessor()

uploaded_files = st.file_uploader("Tải lên hình ảnh chứng từ...", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files and st.button("🚀 Xử lý & Đối chiếu chéo"):
    for file in uploaded_files:
        image = Image.open(file)
        img_array = np.array(image)
        
        # 1. Gọi Backend chạy OCR
        ocr_text = processor.run_ocr(img_array)
        
        # 2. Gọi Backend bóc tách 8 trường chuẩn
        extracted_data = processor.extract_invoice_fields(ocr_text)
        
        # 3. Hiển thị kết quả lên giao diện
        st.success(f"Đã xử lý xong file: {file.name}")
        st.json(extracted_data)
        
        # 4. Tạo nút tải Excel từ Backend
        excel_bytes = processor.generate_excel_report(extracted_data)
        st.download_button(
            label="📥 Tải xuống Báo cáo Excel",
            data=excel_bytes,
            file_name="Bao_Cao_Doi_Soat_Xang_Dau.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )