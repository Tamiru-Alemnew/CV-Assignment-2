# Digital Image Processing Assignment

This project implements seven elementary digital image processing methods using Python, OpenCV, and Streamlit.  
It supports both RGB and Grayscale workflows with side-by-side visualization and histogram comparison.  
It also includes an automation script to generate Notebook LLM-ready assets and markdown.

## Project Structure

```text
.
├── app.py
├── dip_app/
│   ├── constants.py
│   ├── transforms.py
│   ├── ui.py
│   └── utils.py
├── docs/
│   └── notebook_llm_prompt.md
├── scripts/
│   └── prepare_notebook_llm_assets.py
├── requirements.txt
└── .gitignore
```

## Run the Streamlit App

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Generate Notebook LLM Assets

```bash
python scripts/prepare_notebook_llm_assets.py \
  --image-a /path/to/image1.jpg \
  --image-b /path/to/image2.jpg
```

Generated output goes to:

- `artifacts/notebook_llm_assets/`
  - processed images for all methods
  - input/output histograms
  - `notebook_llm_package.md`

Use this together with:

- `docs/notebook_llm_prompt.md`
