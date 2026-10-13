# OS-Synchronization-Assignment
**Name:** DHRITHI P | **USN:** NNM24IS071   

## Implementations (Python 3.8+, standard library only)
| # | Problem | Technique | File |
|---|---------|-----------|------|
| 1 | Readers-Writers | Semaphores (`mutex`, `wrt`), readers preference | `readers_writers/semaphore/rw_semaphore.py` |
| 2 | Readers-Writers | Monitor (lock + condition variables), writer preference | `readers_writers/monitor/rw_monitor.py` |
| 3 | Dining Philosophers (4) | Semaphores (Asymmetric deadlock prevention) | `dining_philosophers/semaphore/dining_philosophers_semaphore.py` |
| 4 | Dining Philosophers (4) | Monitor (`threading.Condition`), all-or-nothing logic | `dining_philosophers/monitor/dining_philosophers_monitor.py` |

Python has no native monitor, so a monitor is built from `threading.Lock` and `threading.Condition` objects; all shared state is touched only inside the lock[cite: 1].

## Build / run
No build step and no external libraries. Run the scripts directly to execute the synchronization and regenerate the HTML files[cite: 1]:
```bash
python readers_writers/semaphore/rw_semaphore.py
python readers_writers/monitor/rw_monitor.py
python dining_philosophers/semaphore/dining_philosophers_semaphore.py
python dining_philosophers/monitor/dining_philosophers_monitor.py
```

## How the HTML is generated
log_event() is called by the threads at every state change, inside the critical/monitor sections so ordering is faithful. It uses a threading.Lock() to safely append the current state (actor ID, state, resource ownership) into an event array. After all threads finish, generate_html() embeds the recorded events as JSON into an HTML template string. The generated page replays that data visually with interactive controls (Start/Pause/Step, speed dropdown, and progress slider).

## Viewing
Open any file in `generated_html/` in a browser (double-click). Output files: `readers_writers_semaphore.html`, `readers_writers_monitor.html`, `dining_philosophers_semaphore.html`, `dining_philosophers_monitor.html`.

## Self-checks built into the programs
* RW: Monitor logic strictly tracks waiting writers to prevent writer starvation.
* DP: The asymmetric algorithm mathematically prevents circular wait in semaphores. The HTML visualizer uses precise array mapping to draw dynamic SVG lines, proving visually that neighbors never hold the same chopstick simultaneously and that no cross-table fetching occurs.

## Known limitations
* Python's GIL means threads interleave rather than run in parallel; `time.sleep` is used to make interleavings visible - delays never replace synchronization.
* Trace timestamps are real, but the HTML replays at a fixed step rate, not real-time.
* Neither RW policy nor the monitor DP solution is fully starvation-free (discussed in source comments).

## AI tools used
See `ai_prompts/prompts.md`. 

## References:
`references/references.md`.

## Screenshots
See `screenshots/`.
