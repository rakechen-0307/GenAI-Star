import librosa
import numpy as np

librosa.ex('trumpet')

y, sr = librosa.load(librosa.ex('trumpet'))
onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                         hop_length=512,
                                         aggregate=np.median)
peaks = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=10)
print(peaks)

import matplotlib.pyplot as plt
times = librosa.times_like(onset_env, sr=sr, hop_length=512)
fig, ax = plt.subplots(nrows=2, sharex=True)
D = np.abs(librosa.stft(y))
librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                         y_axis='log', x_axis='time', ax=ax[1])
ax[0].plot(times, onset_env, alpha=0.8, label='Onset strength')
ax[0].vlines(times[peaks], 0,
             onset_env.max(), color='r', alpha=0.8,
             label='Selected peaks')
ax[0].legend(frameon=True, framealpha=0.8)
ax[0].label_outer()
