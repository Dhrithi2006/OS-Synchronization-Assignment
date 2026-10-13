import threading
import time
import random
import json
from datetime import datetime

#SHARED RESOURCES & SEMAPHORES
shared_data = 0
read_count = 0

mutex = threading.Semaphore(1)
write_block = threading.Semaphore(1)

#EXECUTION LOGGING
event_log = []
log_lock = threading.Lock()

def log_event(actor, action, data_val, readers):
    """Captures state transitions for the HTML simulation."""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    with log_lock:
        event_log.append({
            "time": timestamp,
            "actor": actor,
            "action": action,
            "data": data_val,
            "readers": readers
        })
    print(f"[{timestamp}] {actor} - {action} (Data: {data_val}, Readers: {readers})")

def reader(reader_id):
    global read_count
    actor = f"Reader {reader_id}"
    
    log_event(actor, "Waiting to read", shared_data, read_count)
    
    #ENTRY SECTION
    mutex.acquire()
    read_count += 1
    if read_count == 1:
        write_block.acquire()
    mutex.release()
    
    #CRITICAL SECTION
    log_event(actor, "Reading (Entered Critical Section)", shared_data, read_count)
    time.sleep(random.uniform(0.1, 0.5)) 
    
    #EXIT SECTION
    mutex.acquire()
    read_count -= 1
    if read_count == 0:
        write_block.release()
    mutex.release()
    
    log_event(actor, "Finished and Left", shared_data, read_count)

def writer(writer_id):
    global shared_data
    actor = f"Writer {writer_id}"
    
    log_event(actor, "Waiting to write", shared_data, read_count)
    
    #ENTRY SECTION
    write_block.acquire()
    
    #CRITICAL SECTION
    shared_data += 10
    log_event(actor, "Writing (Entered Critical Section)", shared_data, read_count)
    time.sleep(random.uniform(0.2, 0.7)) 
    
    #EXIT SECTION
    write_block.release()
    log_event(actor, "Finished and Left", shared_data, read_count)

def generate_html():
    """Generates an animated HTML visual simulation using JavaScript."""
    
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Readers-Writers Animated Simulation</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px; text-align: center; }
            .container { display: flex; justify-content: space-around; margin-top: 20px; }
            .zone { width: 30%; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); min-height: 200px; }
            h3 { border-bottom: 2px solid #333; padding-bottom: 5px; }
            .actor { padding: 10px; margin: 5px; border-radius: 5px; font-weight: bold; color: white; display: inline-block; transition: all 0.5s ease; }
            .reader { background-color: #0056b3; }
            .writer { background-color: #d9534f; }
            #controls { margin-bottom: 20px; }
            button { padding: 10px 20px; font-size: 16px; cursor: pointer; background: #28a745; color: white; border: none; border-radius: 5px; }
            button:disabled { background: #ccc; }
            .stats { font-size: 1.2em; margin: 10px; font-weight: bold; }
            #log { margin-top: 20px; text-align: left; background: #fff; padding: 10px; height: 150px; overflow-y: auto; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h2>Readers-Writers Synchronization (Semaphore)</h2>
        
        <div id="controls">
            <button id="startBtn" onclick="startSimulation()">Start Simulation</button>
            <button onclick="location.reload()">Reset</button>
        </div>
        
        <div class="stats">Shared Data: <span id="sharedData">0</span> | Active Readers: <span id="activeReaders">0</span></div>

        <div class="container">
            <div class="zone" id="waitingZone">
                <h3>Waiting Room</h3>
            </div>
            <div class="zone" id="criticalZone" style="border: 3px solid #ffc107;">
                <h3>Critical Section</h3>
            </div>
            <div class="zone" id="finishedZone">
                <h3>Finished</h3>
            </div>
        </div>

        <div id="log"><strong>Event Log:</strong><br></div>

        <script>
            const events = EVENT_DATA_PLACEHOLDER;
            let currentIndex = 0;
            let timer;

            function updateUI(event) {
                // Create or find the actor element
                let actorId = event.actor.replace(/\s+/g, '_');
                let actorEl = document.getElementById(actorId);
                
                if (!actorEl) {
                    actorEl = document.createElement('div');
                    actorEl.id = actorId;
                    actorEl.className = 'actor ' + (event.actor.includes('Reader') ? 'reader' : 'writer');
                    actorEl.innerText = event.actor;
                }

                // Move the actor based on action
                if (event.action.includes('Waiting')) {
                    document.getElementById('waitingZone').appendChild(actorEl);
                } else if (event.action.includes('Entered')) {
                    document.getElementById('criticalZone').appendChild(actorEl);
                } else if (event.action.includes('Finished')) {
                    document.getElementById('finishedZone').appendChild(actorEl);
                }

                // Update Stats
                document.getElementById('sharedData').innerText = event.data;
                document.getElementById('activeReaders').innerText = event.readers;

                // Update text log
                let logDiv = document.getElementById('log');
                logDiv.innerHTML += `[${event.time}] ${event.actor} - ${event.action}<br>`;
                logDiv.scrollTop = logDiv.scrollHeight;
            }

            function startSimulation() {
                document.getElementById('startBtn').disabled = true;
                timer = setInterval(() => {
                    if (currentIndex < events.length) {
                        updateUI(events[currentIndex]);
                        currentIndex++;
                    } else {
                        clearInterval(timer);
                        let logDiv = document.getElementById('log');
                        logDiv.innerHTML += "<strong>--- Execution Complete ---</strong><br>";
                    }
                }, 800); 
            }
        </script>
    </body>
    </html>
    """
    
    # Inject the JSON string directly into the JavaScript
    html_content = html_template.replace("EVENT_DATA_PLACEHOLDER", json.dumps(event_log))
    
    with open("readers_writers_semaphore.html", "w") as file:
        file.write(html_content)
    print("\n[SUCCESS] Animated HTML simulation generated: readers_writers_semaphore.html")

if __name__ == "__main__":
    threads = []
    
    for i in range(1, 6):
        threads.append(threading.Thread(target=reader, args=(i,)))
    for i in range(1, 3):
        threads.append(threading.Thread(target=writer, args=(i,)))
        
    random.shuffle(threads)
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        
    generate_html()