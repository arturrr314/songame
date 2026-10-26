from pygame import *   
import sounddevice as sd 
import scipy.io.wavfile as wav
# === Настройки ===
fs = 44100     
chunk = 1024   
width, height = 800, 400  
voice_file = "voice_record.wav"
is_recording = False

songs = [
"sounds\\MinusDuHast.mp3"
]

curent_index = 0
minus_track = songs[curent_index]


init()
mixer.init()
mixer.music.set_volume(0.4) 

font.init()
font_big = font.SysFont("Arial", 32, bold=True)

btn_record  = Rect(425, 250, 200, 80)
btn_record_color = "green"
btn_record_text = "ЗАПИС"

btn_stop = Rect (70, 250, 200, 80)
btn_stop_color = "red"
btn_stop_text = "СТОП"


screen = display.set_mode((width, height))
display.set_caption("Live Audio (Mic)")
clock = time.Clock()


data = [0.0] * chunk


def audio_callback(indata, frames, time_info, status):
    global data
    if status:
        print(status)  
    
    data = [sample * (height // 2) for sample in indata[:, 0].tolist()]


stream = sd.InputStream(
    callback=audio_callback,  
    channels=1,              
    samplerate=fs,            
    blocksize=chunk,           
    dtype='float32'           
)
stream.start()

def start_recording():
    global recording
    recording = sd.rec(int(fs*5), samplerate=fs, channels=1, dtype='int16')

def stop_voice_record():
    global recording
    sd.stop()
    if recording is not None:
        wav.write(voice_file, fs, recording)
        recording = None

def play_music():
    mixer.music.load(minus_track)
    mixer.music.play()
    voice_sound = mixer.Sound(voice_file)
    voice_sound.play()




def stop_all_music():
    mixer.music.stop()
    mixer.stop()






running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            if btn_record.collidepoint(e.pos):
                if not is_recording:
                    btn_record_color = "red"
                    btn_record_text =  "СТОП"
                    is_recording = True
                    mixer.music.load(minus_track)
                    mixer.music.play()
                    start_recording()
                else:
                    btn_record_color = "green"
                    btn_record_text = "ЗАПИС"
                    is_recording = False
                    stop_voice_record()
                    play_music()

            if btn_stop.collidepoint(e.pos):
                stop_all_music()
                is_recording = False
                btn_record_color = "green"
                btn_record_text = "ЗАПИС"



    screen.fill((0, 0, 0))

    
    points = []
    for i, sample in enumerate(data):
        x = int(i * width / chunk)         
        y = int(height / 2 + sample)        
        points.append((x, y))               

   
    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)

    draw.rect(screen, btn_record_color, btn_record)
    rec_text = font_big.render(btn_record_text, True, "black" )
    screen.blit(rec_text, (btn_record.x + 20, btn_record.y + 20))
    draw.rect(screen, btn_stop_color, btn_stop)
    rec_text = font_big.render(btn_stop_text, True, "black" )
    screen.blit(rec_text, (btn_stop.x + 20, btn_stop.y + 20))


    display.update()
    clock.tick(60)

stream.stop()
quit()