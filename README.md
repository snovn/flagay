<h1 align="center">Flagify :3</h1>

<p align="center">
  <img src="example/input_preset.jpg" alt="Image 1" style="margin-right: 10px; width: 300px; height: auto;" />
  <img src="example/output_preset.png" alt="Image 2" style="margin-left: 10px; width: 300px; height: auto;" />
</p>

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/snovn/flagay?label=Release&style=flat-square)](https://github.com/snovn/flagay/releases/tag/v1.0)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/snovn/flagay?label=Version&style=flat-square)](https://github.com/snovn/flagay/tree/v1.0)

A Python script that removes backgrounds from images using the [remove.bg](http://remove.bg) API. Afterward, you can add different flags onto the cleaned-up images. It's made for easily creating images with transparent backgrounds and adding flags that represent different identities -w-



## Installation
**Clone the repository:**
```bash
git clone https://github.com/snovn/flagay.git
```
**Import necessary packages:**
- Python 3.x
```bash
pip install -r requirements.txt
```

**Run the program.**
```bash
py main.py
```



## Usage
0. **Edit .env file:** Add your desired API Key for background removal.

1. **Select an Image:** Run the script and choose an image file (.png, .jpg, .jpeg) when prompted.

2. **Remove Background:** Confirm if you want to remove the background from the selected image.

3. **Choose a Flag:** Select a flag from the options provided (Gay, Bisexual, Transgender, Lesbian, Asexual, Pansexual) or upload a custom flag image.

4. **Save the Image:** Save the final image with the overlayed flag in PNG format.

## Contributing

If you'd like to contribute to this project, please follow the guidelines. >w<

## License

This project is licensed under the [MIT LICENSE](LICENSE) - see the LICENSE file for details.

<div style="display: flex; justify-content: center; align-items: center; margin: 20px;">
  <img src="example/input_preset_1.jpg" alt="Image 1" style="margin-right: 10px; width: 300px; height: auto;" />
  <img src="example/output_preset_1.png" alt="Image 2" style="margin-left: 10px; width: 300px; height: auto;" />
</div>
<div style="display: flex; justify-content: center; align-items: center; margin: 20px;">
  <img src="example/input_custom.jpg" alt="Image 1" style="margin-right: 10px; width: 300px; height: auto;" />
  <img src="example/output_custom.png" alt="Image 2" style="margin-left: 10px; width: 300px; height: auto;" />
</div>