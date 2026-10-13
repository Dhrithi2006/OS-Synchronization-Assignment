import threading
import time
import random
import json
from datetime import datetime

NUM_PHILOSOPHERS = 4

# --- MONITOR STATE VARIABLES ---
# The single Monitor construct[cite: 1]
monitor = threading.Condition()
states = ["THINKING"] * NUM_PHILOSOPHERS

# For the HTML UI
chopstick_owners = ["free", "free", "free", "free"]
event_log = []
log_lock = threading.Lock()

def log_event(philosopher_id, state):
    """Captures state transitions for the HTML simulation[cite: 2]."""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    with log_lock:
        current_chopsticks = list(chopstick_owners)
        event_log.append({
            "time": timestamp,
            "actorId": philosopher_id,
            "state": state,
            "chopsticks": current_chopsticks
        })
    print(f"[{timestamp}] P{philosopher_id} - {state}. Chopsticks: {current_chopsticks}")

def pick_up_chopsticks(i):
    # Mapping exactly matches the HTML circular layout[cite: 8]
    left = (i - 1) % NUM_PHILOSOPHERS
    right = i
    
    # --- MONITOR ENTRY ---
    with monitor:
        states[i] = "HUNGRY"
        log_event(i, "HUNGRY")
        
        left_neighbor = (i - 1) % NUM_PHILOSOPHERS
        right_neighbor = (i + 1) % NUM_PHILOSOPHERS
        
        # Wait while either neighbor is eating (Monitor Condition)[cite: 1]
        while states[left_neighbor] == "EATING" or states[right_neighbor] == "EATING":
            monitor.wait()
            
        # Condition met: grab both chopsticks simultaneously
        states[i] = "EATING"
        chopstick_owners[left] = f"P{i}"
        chopstick_owners[right] = f"P{i}"
        log_event(i, "EATING")

def put_down_chopsticks(i):
    left = (i - 1) % NUM_PHILOSOPHERS
    right = i
    
    # --- MONITOR ENTRY ---
    with monitor:
        states[i] = "THINKING"
        chopstick_owners[left] = "free"
        chopstick_owners[right] = "free"
        log_event(i, "THINKING")
        
        # Wake up all waiting philosophers to check if their neighbors have finished
        monitor.notify_all()

def philosopher(i):
    log_event(i, "THINKING")
    for _ in range(2):
        time.sleep(random.uniform(0.1, 0.2))
        
        # 1. Becomes HUNGRY and attempts to acquire both chopsticks via Monitor
        pick_up_chopsticks(i)
        
        # 2. EATING
        time.sleep(random.uniform(0.2, 0.4))
        
        # 3. Finished eating, revert to THINKING and notify others
        put_down_chopsticks(i)

def generate_html():
    """Generates the circular HTML visual simulation with flawless SVG connection lines[cite: 2, 8]."""
    
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Dining Philosophers (Monitor - Dual Lines)</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1e26; color: white; margin: 0; padding: 20px; }
            .top-bar { display: flex; align-items: center; gap: 15px; background: #232833; padding: 10px 20px; border-radius: 8px; margin-bottom: 20px; }
            button { background: #2c323f; color: white; border: 1px solid #454d5e; padding: 8px 15px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; gap: 5px; }
            button:hover { background: #3a4252; }
            select { background: #2c323f; color: white; border: 1px solid #454d5e; padding: 8px; border-radius: 4px; }
            .slider-container { display: flex; align-items: center; gap: 10px; flex-grow: 1; }
            input[type=range] { flex-grow: 1; }
            
            .simulation-area { position: relative; width: 600px; height: 600px; margin: 0 auto; background: #232833; border-radius: 12px; }
            
            .node { position: absolute; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: bold; transition: all 0.3s ease; z-index: 10; }
            
            .philosopher { width: 120px; height: 120px; transform: translate(-50%, -50%); background-color: #707a8a; }
            .philosopher .id { font-size: 24px; }
            .philosopher .state { font-size: 12px; text-transform: uppercase; margin-top: 5px; }
            
            .chopstick { 
                width: 32px; 
                height: 100px; 
                border-radius: 16px;
                background-color: #d4a373;
                border: 2px solid white; 
                color: #1a1e26; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            .chopstick .id { font-size: 14px; font-weight: 800; }
            .chopstick .status { font-size: 11px; font-weight: bold; margin-top: 2px; }
            
            .dashed-ring { position: absolute; top: 50%; left: 50%; width: 250px; height: 250px; transform: translate(-50%, -50%); border: 2px dashed #454d5e; border-radius: 50%; pointer-events: none; z-index: 1; }

            .legend { display: flex; justify-content: center; gap: 20px; margin-top: 20px; font-size: 14px; }
            .legend-item { display: flex; align-items: center; gap: 8px; }
            .legend-color { width: 12px; height: 12px; border-radius: 2px; }

            .bg-hungry { background-color: #b58900 !important; }
            .bg-eating { background-color: #2aa198 !important; }
            .bg-thinking { background-color: #707a8a !important; }
            
            /* SVG Lines */
            .glow-line { transition: opacity 0.3s ease; filter: drop-shadow(0 0 5px #2aa198); }
        </style>
    </head>
    <body>
        <div class="top-bar">
            <button id="btnStart" onclick="togglePlay()">Start</button>
            <button onclick="stepForward()">Step &#9658;</button>
            <button onclick="location.reload()">Reset</button>
            <span>Speed</span>
            <select id="speedSelect" onchange="updateSpeed()">
                <option value="1500">0.5x</option>
                <option value="800" selected>1x</option>
                <option value="300">2x</option>
            </select>
            <div class="slider-container">
                <input type="range" id="timeline" min="0" value="0" step="1" onchange="seekTo()">
                <span id="stepCounter">0 / 0</span>
            </div>
        </div>

        <div class="simulation-area">
            <div class="dashed-ring"></div>
            
            <!-- SVG Layer for Connection Lines -->
            <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5;">
                <!-- P0 Lines -->
                <line id="line-p0-c3" x1="50%" y1="15%" x2="29%" y2="29%" stroke="#2aa198" stroke-width="4" opacity="0" class="glow-line" />
                <line id="line-p0-c0" x1="50%" y1="15%" x2="71%" y2="29%" stroke="#2aa198" stroke-width="4" opacity="0" class="glow-line" />
                <!-- P1 Lines -->
                <line id="line-p1-c0" x1="85%" y1="50%" x2="71%" y2="29%" stroke="#2aa198" stroke-width="4" opacity="0" class="glow-line" />
                <line id="line-p1-c1" x1="85%" y1="50%" x2="71%" y2="71%" stroke="#2aa198" stroke-width="4" opacity="0" class="glow-line" />
                <!-- P2 Lines -->
                <line id="line-p2-c1" x1="50%" y1="85%" x2="71%" y2="71%" stroke="#2aa198" stroke-width="4" opacity="0" class="glow-line" />
                <line id="line-p2-c2" x1="50%" y1="85%" x2="29%" y2="71%" stroke="#2aa198" stroke-width="4" opacity="0" class="glow-line" />
                <!-- P3 Lines -->
                <line id="line-p3-c2" x1="15%" y1="50%" x2="29%" y2="71%" stroke="#2aa198" stroke-width="4" opacity="0" class="glow-line" />
                <line id="line-p3-c3" x1="15%" y1="50%" x2="29%" y2="29%" stroke="#2aa198" stroke-width="4" opacity="0" class="glow-line" />
            </svg>
            
            <div id="p0" class="node philosopher" style="top: 15%; left: 50%;">
                <div class="id">P0</div><div class="state">THINKING</div>
            </div>
            <div id="p1" class="node philosopher" style="top: 50%; left: 85%;">
                <div class="id">P1</div><div class="state">THINKING</div>
            </div>
            <div id="p2" class="node philosopher" style="top: 85%; left: 50%;">
                <div class="id">P2</div><div class="state">THINKING</div>
            </div>
            <div id="p3" class="node philosopher" style="top: 50%; left: 15%;">
                <div class="id">P3</div><div class="state">THINKING</div>
            </div>

            <div id="c0" class="node chopstick" style="top: 29%; left: 71%; transform: translate(-50%, -50%) rotate(45deg);">
                <div style="transform: rotate(-45deg); text-align: center;">
                    <div class="id">C0</div><div class="status">free</div>
                </div>
            </div>
            <div id="c1" class="node chopstick" style="top: 71%; left: 71%; transform: translate(-50%, -50%) rotate(-45deg);">
                <div style="transform: rotate(45deg); text-align: center;">
                    <div class="id">C1</div><div class="status">free</div>
                </div>
            </div>
            <div id="c2" class="node chopstick" style="top: 71%; left: 29%; transform: translate(-50%, -50%) rotate(45deg);">
                <div style="transform: rotate(-45deg); text-align: center;">
                    <div class="id">C2</div><div class="status">free</div>
                </div>
            </div>
            <div id="c3" class="node chopstick" style="top: 29%; left: 29%; transform: translate(-50%, -50%) rotate(-45deg);">
                <div style="transform: rotate(45deg); text-align: center;">
                    <div class="id">C3</div><div class="status">free</div>
                </div>
            </div>
        </div>

        <div class="legend">
            <div class="legend-item"><div class="legend-color bg-hungry"></div>HUNGRY</div>
            <div class="legend-item"><div class="legend-color bg-eating"></div>EATING</div>
            <div class="legend-item"><div class="legend-color bg-thinking"></div>THINKING</div>
        </div>

        <script>
            const events = EVENT_DATA_PLACEHOLDER;
            let currentStep = 0;
            let timer = null;
            let speed = 800;
            let isPlaying = false;

            document.getElementById('timeline').max = events.length;
            updateCounter();

            function updateCounter() {
                document.getElementById('stepCounter').innerText = `${currentStep} / ${events.length}`;
                document.getElementById('timeline').value = currentStep;
            }

            function applyState(stepIndex) {
                if (stepIndex === 0) return; 
                
                let pStates = {0: 'THINKING', 1: 'THINKING', 2: 'THINKING', 3: 'THINKING'};
                let cStates = ['free', 'free', 'free', 'free'];

                for(let i=0; i<stepIndex; i++) {
                    let ev = events[i];
                    pStates[ev.actorId] = ev.state;
                    cStates = ev.chopsticks;
                }
                
                // Hide all lines first
                document.querySelectorAll('.glow-line').forEach(line => line.style.opacity = '0');

                for(let i=0; i<4; i++) {
                    let pNode = document.getElementById(`p${i}`);
                    pNode.querySelector('.state').innerText = pStates[i];
                    pNode.classList.remove('bg-hungry', 'bg-eating', 'bg-thinking');
                    pNode.classList.add(`bg-${pStates[i].toLowerCase()}`);

                    let cNode = document.getElementById(`c${i}`);
                    cNode.querySelector('.status').innerText = cStates[i];
                    
                    if(cStates[i] === 'free') {
                        cNode.style.backgroundColor = '#d4a373'; 
                        cNode.style.color = '#1a1e26'; 
                        cNode.style.boxShadow = '0 4px 6px rgba(0,0,0,0.3)';
                    } else {
                        cNode.style.backgroundColor = '#2aa198'; 
                        cNode.style.color = '#ffffff'; 
                        cNode.style.boxShadow = '0 0 15px #2aa198';
                        
                        // Draw the connection line bridging the philosopher to the chopstick
                        let ownerStr = cStates[i].toLowerCase(); 
                        let lineId = `line-${ownerStr}-c${i}`;
                        let lineEl = document.getElementById(lineId);
                        if (lineEl) {
                            lineEl.style.opacity = '1';
                        }
                    }
                }
            }

            function stepForward() {
                if (currentStep < events.length) {
                    currentStep++;
                    applyState(currentStep);
                    updateCounter();
                } else {
                    pausePlay();
                }
            }

            function togglePlay() {
                let btn = document.getElementById('btnStart');
                if (isPlaying) {
                    pausePlay();
                } else {
                    if(currentStep >= events.length) currentStep = 0;
                    isPlaying = true;
                    btn.innerText = "Pause";
                    timer = setInterval(stepForward, speed);
                }
            }

            function pausePlay() {
                isPlaying = false;
                document.getElementById('btnStart').innerText = "Start";
                clearInterval(timer);
            }

            function updateSpeed() {
                speed = parseInt(document.getElementById('speedSelect').value);
                if (isPlaying) {
                    pausePlay();
                    togglePlay();
                }
            }

            function seekTo() {
                let val = parseInt(document.getElementById('timeline').value);
                currentStep = val;
                applyState(currentStep);
                updateCounter();
            }
        </script>
    </body>
    </html>
    """
    
    html_content = html_template.replace("EVENT_DATA_PLACEHOLDER", json.dumps(event_log))
    
    with open("dining_philosophers_monitor.html", "w") as file:
        file.write(html_content)
    print("\n[SUCCESS] HTML dual-line simulation generated: dining_philosophers_monitor.html")

if __name__ == "__main__":
    threads = []
    for i in range(NUM_PHILOSOPHERS):
        threads.append(threading.Thread(target=philosopher, args=(i,)))
    random.shuffle(threads)
    for t in threads: t.start()
    for t in threads: t.join()
    generate_html()