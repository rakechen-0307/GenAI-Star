# Hybrid highlight generator

### Workflow

Input Video,
-> `split_audio.py`
-> (optional) `nr_split.py`
-> `transcript.py`
-> (timeline, prompt ->) `summary.py`

The above pipeline is implemented in `genai.py`.

`split_audio.py`: First separate audio wave from the original mp4, then split the wave into small segments with each clip 15 seconds.

`nr_split.py`: Perform denoise on the audio wave.

`transcript.py`: Use speech-to-text method, extract the transcript from the audio wave using `whisper` module (implemented via OpenAI API).

`summary.py`: Given the transcript above, paired with preprocessed timeline (optional) and user prompt(optional), GPT-4o will response appropriate summary in table format and give some interesting highlights. Also, a JSON file for highlight is also generated to perform postprocessing.

``

### Usage

Load API Key in `.env`

```bash
python genai.py [-h] [-t TIMELINE] [--denoise DENOISE] [-o OUTPUT] video

python split_audio.py [-h] [-o OUTPUT] input

python nr_split.py [-h] audio

python transcript.py [-h] [-o OUTPUT] audio

python summary.py [-h] [-o OUTPUT] [--outputjson OUTPUTJSON] [-t TIMELINE] text
```
