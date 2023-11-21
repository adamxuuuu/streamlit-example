import streamlit as st
import os
from typing import List

# Streamlit config
st.set_page_config(layout='wide')

class InvalidCVError(BaseException):
    pass

class InvalidJDError(BaseException):
    pass

class CV:
    def __init__(self, name: str):
        segments = name.split(".")[0].split("-")
        if len(segments) != 6:
            raise InvalidCVError
        self.meta = segments[:2]
        self.jid = segments[3]
        self.jname = segments[4]
        self.cid = segments[5]
        self.source = os.path.join("./app/static", name)

    def __str__(self) -> str:
        return f"""
        😊 CV: {self.cid}
        Applyed Job: {self.jname}
        Metadata: {self.meta}"""

class JD:
    def __init__(self, name: str):
        segments = name.split(".")[0].split("_")
        if len(segments) != 3:
            raise InvalidJDError
        self.idx = segments[0]
        self.jname = segments[1]
        self.jid = segments[2]
        self.matched = []

    def __str__(self) -> str:
        return self.jname

def read_pdf(file_path):
    st.write(file_path)
    with open(file_path, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        num_pages = pdf.getNumPages()
        text = ""
        for page_num in range(num_pages):
            page = pdf.getPage(page_num)
            text += page.extractText()
        return text

def _init():
    cvs = [CV(cv) for cv in os.listdir("CV")]
    jds = [JD(jd) for jd in os.listdir("JD")]
    for jd in jds:
        for cv in cvs:
            if cv.jid == jd.jid:
                jd.matched.append(cv)
    return jds

def show_jd_overview(containers, jd):
    for idx, cv in enumerate(jd.matched):
        containers[idx % len(containers)].button(
            label=str(cv), 
            key=cv.cid,
            on_click=show_cv_detail,
            args=[cv.source],
            use_container_width=True)

def show_cv_detail(file):
    # Need to store files on obs and give access to application
    # st.title('PDF Viewer')
    # st.write(read_pdf(file))
    pass

def main():
    jds = _init()
    # UI part
    cols = st.columns(spec=2, gap="large")
    with st.sidebar:
        st.title("Job Descriptions")
        # add_jd = st.file_uploader(label="Upload a Job Description")
        for jd in jds:
            st.button(label=jd.jname,
                    on_click=show_jd_overview,
                    args=[cols, jd],
                    use_container_width=True)


if __name__ == "__main__":
    main()
    