"""M1: Whisper on the cut-off zone, per-stem levels through the outro, and stem-to-master lag. Usage: NLTK_DATA=$PWD/.venv/nltk_data .venv/bin/python -I scripts/m1_outro_checks.py"""
import torch, whisperx, numpy as np, soundfile as sf, librosa
from faster_whisper import WhisperModel
names=['Vocals','Backing Vocals','Drums','Bass','Guitar','Keyboard','Synth','Percussion','Brass','Strings','FX']
st={n:sf.read(f'audio/stems/Effective Immediately ({n}).wav',always_2d=True)[0].mean(1) for n in names}
sr=48000; mix=sf.read('audio/track/effective-immediately.wav',always_2d=True)[0].mean(1)
m=WhisperModel('large-v3',device='cuda',compute_type='float16')
for a,b in ((218.5,230.2),(219.5,225),(224.5,230.2)):
    for lab,y in (('lead',st['Vocals']),('mix',mix)):
        seg=librosa.resample(y[int(a*sr):int(b*sr)].astype(np.float32),orig_sr=sr,target_sr=16000)
        for temp in (0.0,0.4):
            s,_=m.transcribe(seg,language='en',beam_size=5,vad_filter=False,word_timestamps=True,condition_on_previous_text=False,no_speech_threshold=None,temperature=temp,compression_ratio_threshold=None,log_prob_threshold=None)
            print(f'[{a}-{b} {lab} t={temp}]',' '.join(f"{a+w.start:.2f}:{w.word.strip()}" for x in s for w in x.words) or '(none)')
print('\nRMS dBFS by stem'); edges=[(205,211),(211,219),(219,224),(224,230),(230,236),(236,242),(242,247),(247,250),(250,252)]
print(f"{'stem':16}"+''.join(f'{a}-{b}'.rjust(9) for a,b in edges))
for n,y in list(st.items())+[('MASTER',mix)]:
    print(f'{n:16}'+''.join(f"{20*np.log10(np.sqrt(np.mean(y[a*sr:b*sr]**2))+1e-9):9.1f}" for a,b in edges))
h=480; e=lambda y: librosa.onset.onset_strength(y=y.astype(np.float32),sr=sr,hop_length=h)
A=e(mix); B=e(st['Vocals']+st['Drums']+st['Bass']); n=min(len(A),len(B)); A=A[:n]-A[:n].mean(); B=B[:n]-B[:n].mean()
c=np.fft.irfft(np.fft.rfft(A,2*n)*np.conj(np.fft.rfft(B,2*n))); l=int(np.argmax(c)); l=l-2*n if l>n else l
print('\nstem-to-master lag ms',l*h/sr*1000)
