"""M1: Whisper without VAD on the disputed passages (stems and mix), and vocal levels around the cut-off. Usage: NLTK_DATA=$PWD/.venv/nltk_data .venv/bin/python -I scripts/m1_spot_checks.py"""
import sys, numpy as np, soundfile as sf, librosa
import torch, whisperx
from faster_whisper import WhisperModel
base='audio/stems/Effective Immediately (%s).wav'
def load(names):
    y=None
    for n in names:
        a,sr=sf.read(base%n,always_2d=True); a=a.mean(1); y=a if y is None else y+a
    return y,sr
lead,sr=load(['Vocals']); back,_=load(['Backing Vocals']); both=lead+back
mix,_=sf.read('audio/track/effective-immediately.wav',always_2d=True); mix=mix.mean(1)
m=WhisperModel('large-v3',device='cuda',compute_type='float16')
wins=[('took-jacket',24,33),('asides+postchorus',98,116),('postchorus-2nd',108,122),('final-spoken+cutoff',209,232)]
for name,a,b in wins:
    for lab,y in (('lead',lead),('backing',back),('lead+back',both),('mix',mix)):
        seg=librosa.resample(y[int(a*sr):int(b*sr)].astype(np.float32),orig_sr=sr,target_sr=16000)
        s,_=m.transcribe(seg,language='en',beam_size=5,vad_filter=False,word_timestamps=True,condition_on_previous_text=False,no_speech_threshold=None)
        words=[f"{a+w.start:.2f}:{w.word.strip()}" for x in s for w in x.words]
        print(f'[{name} | {lab}]',' '.join(words) or '(none)')
print('--- vocal RMS dBFS per 0.5 s, 214-232 s (lead / backing / mix)')
for t in np.arange(214,232,0.5):
    i,j=int(t*sr),int((t+.5)*sr)
    f=lambda y:20*np.log10(np.sqrt(np.mean(y[i:j]**2))+1e-9)
    print(f'{t:6.1f} {f(lead):7.1f} {f(back):7.1f} {f(mix):7.1f}')
s=sum(load([n])[0] for n in ['Bass','Drums','Synth','Vocals','Guitar','Backing Vocals','Strings','Percussion','Keyboard','Brass','FX'])
n=min(len(s),len(mix)); c=np.corrcoef(s[:n],mix[:n])[0,1]; print('stems-sum vs master correlation',round(float(c),5),'residual dB',round(float(20*np.log10(np.std(s[:n]-mix[:n])/np.std(mix[:n]))),1))
