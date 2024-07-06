# Dienruei

### Pipeline

Video -> `split_audio.py` -> `nr_split.py` -> `transcript.py` -> `summary.py`

The above pipeline is implemented in `genai.py`.

### Usage

```bash
python genai.py [-h] [--denoise DENOISE] [-o OUTPUT] video

python split_audio.py [-h] [-o OUTPUT] input

python nr_split.py [-h] audio

python transcript.py [-h] [-o OUTPUT] audio

python summary.py [-h] [-o OUTPUT] text
```
