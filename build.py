import subprocess, json, os, wave, pathlib, imageio_ffmpeg
D = pathlib.Path(__file__).parent.resolve(); B = D/'build'; B.mkdir(exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
import sys
RATE = int(sys.argv[1]) if len(sys.argv) > 1 else 1
S = json.load(open(D/'slides.json', encoding='utf-8'))
CSS = """*{box-sizing:border-box;margin:0}body{width:1920px;height:1080px;font-family:'Malgun Gothic',sans-serif;background:#f6f3ff;color:#1e1b2e;padding:70px 120px;position:relative;overflow:hidden}
.k{font-size:30px;letter-spacing:6px;color:#6d3fd6;font-weight:700}h1{font-size:84px;margin:18px 0 30px;line-height:1.2}h1 b{color:#6d3fd6}
ul{list-style:none;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:28px}li{background:#fff;border-radius:28px;padding:26px 36px;font-size:34px;line-height:1.45;box-shadow:0 6px 0 #e3dbfb}li strong{display:block;color:#6d3fd6;font-size:30px;margin-bottom:6px}
.cap{position:absolute;left:0;right:0;bottom:0;background:rgba(20,16,36,.88);color:#fff;font-size:40px;line-height:1.4;padding:28px 140px;text-align:center;min-height:150px;display:flex;align-items:center;justify-content:center}.n{position:absolute;right:40px;top:40px;font-size:28px;color:#8f86a8}.bar{position:absolute;left:0;top:0;height:14px;background:#6d3fd6}"""
clips=[]
for i, s in enumerate(S):
    lis = ''.join(f"<li><strong>{a}</strong>{b}</li>" for a, b in s['items'])
    for j, line in enumerate(s['say']):
        k=f'{i}_{j}'
        html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='bar' style='width:{(i+1)/len(S)*100}%'></div><div class='k'>{s['kicker']}</div><h1>{s['title']}</h1><ul>{lis}</ul><div class='cap'>{line}</div><div class='n'>{i+1}/{len(S)}</div></body></html>"
        (B/f's{k}.html').write_text(html, encoding='utf-8')
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1920,1080', f'--screenshot={B/f"s{k}.png"}', (B/f's{k}.html').as_uri()], check=True, capture_output=True)
        (B/f'n{k}.txt').write_text(line, encoding='utf-8')
        ps = f"Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.SelectVoice('Microsoft Heami Desktop'); $s.Rate={RATE}; $s.SetOutputToWaveFile('{B/f'n{k}.wav'}'); $s.Speak([IO.File]::ReadAllText('{B/f'n{k}.txt'}',[Text.Encoding]::UTF8)); $s.Dispose()"
        subprocess.run(['powershell', '-NoProfile', '-Command', ps], check=True)
        pad = 0.7 if j == len(s['say'])-1 else 0.25
        subprocess.run([FF, '-y', '-loglevel', 'error', '-loop', '1', '-i', str(B/f's{k}.png'), '-i', str(B/f'n{k}.wav'), '-af', f'apad=pad_dur={pad}', '-c:v', 'libx264', '-tune', 'stillimage', '-pix_fmt', 'yuv420p', '-r', '30', '-vf', 'scale=1280:720', '-c:a', 'aac', '-ar', '44100', '-shortest', str(B/f'c{k}.mp4')], check=True)
        clips.append(f'c{k}.mp4')
(B/'list.txt').write_text(''.join(f"file '{c}'\n" for c in clips))
subprocess.run([FF, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(B/'list.txt'), '-c', 'copy', str(D/'pitch.mp4')], check=True)
print(subprocess.run([FF, '-i', str(D/'pitch.mp4')], capture_output=True, encoding='utf-8', errors='ignore').stderr.split('Duration:')[1][:12])
