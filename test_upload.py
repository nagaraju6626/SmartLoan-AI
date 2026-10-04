from streamlit.testing.v1 import AppTest

at = AppTest.from_file("frontend/pages/02_Data_Upload.py").run()
with open("test2.csv", "rb") as f:
    content = f.read()
at.file_uploader[0].set_value(content)
at.button[0].click().run()

if at.error:
    print("Errors:")
    for e in at.error:
        print(e.value)
if at.success:
    print("Success:")
    for s in at.success:
        print(s.value)
