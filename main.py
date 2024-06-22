import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

worksheet_name = "Sheet3"
data = conn.read(worksheet=worksheet_name)

st.title("فرم نظرسنجی")
st.write("لطفاً بازخورد خود را در مورد محصول یا خدمات ما وارد کنید.")

name = st.text_input("نام:")
email = st.text_input("ایمیل:")
rating = st.slider("امتیاز شما از 1 تا 5:", 1, 5, 3)
feedback = st.text_area("بازخورد شما:")

if st.button("ارسال بازخورد"):
    new_feedback = pd.DataFrame([[name, email, rating, feedback]], columns=["Name", "Email", "Rating", "Feedback"])
    data = pd.concat([data, new_feedback], ignore_index=True)
    conn.update(data=data, worksheet=worksheet_name)
    st.success("بازخورد شما با موفقیت ثبت شد!")

st.subheader("تحلیل بازخوردها")
st.write(data)

mean_rating = data["Rating"].mean()
st.metric("میانگین امتیاز", round(mean_rating, 2))

st.bar_chart(data["Rating"].value_counts().sort_index())
