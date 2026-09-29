import os

pages_dir = r"d:\project\Loanproject\frontend\pages"

for filename in os.listdir(pages_dir):
    if filename.endswith(".py") and filename != "01_Home.py":
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace the old navigation import and call
        if "from frontend.components.navigation import render_sidebar" in content:
            content = content.replace(
                "from frontend.components.navigation import render_sidebar",
                "from frontend.components.layout import render_layout"
            )
            content = content.replace("render_sidebar()", "render_layout()")
        else:
            # If it's missing entirely (like some pages), just add it after set_page_config or st.title
            pass
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print("Done updating existing imports.")
