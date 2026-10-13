# AI Prompt Log

**AI Tool Used:** Google Gemini[cite: 3]

## Initial Prompts[cite: 3]
* "Generate a Python implementation of the Readers-Writers problem using semaphores, and include a mechanism to export the execution trace to a dynamic HTML visualization."
* "Create a Monitor-based solution for the Readers-Writers problem using Python's `threading.Condition` with writer preference, alongside the HTML generation logic."
* "Implement the Dining Philosophers problem for exactly 4 philosophers using semaphores, generating a circular HTML/SVG simulation to visualize state transitions."

## Important Follow-up Prompts[cite: 3]
* "Revise the semaphore-based Dining Philosophers solution to use the asymmetric deadlock prevention strategy (where one philosopher picks up the right chopstick first) rather than the all-or-nothing approach."
* "Improve the visual clarity of the HTML simulation by adding dynamic SVG connection lines between a philosopher and the specific chopsticks they are currently holding."
* "Fix a visual bug in the SVG rendering where only one connection line appears. Correct the array index mapping for the chopsticks to ensure both connection lines draw perfectly according to the physical circular layout of the UI."

## Manual Changes Made[cite: 3]
* Corrected the mathematical mapping of the chopsticks (`left = (i - 1) % 4` and `right = i`) to perfectly match the physical DOM layout of the circular table in the HTML.
* Organized the generated single-file scripts into the strict directory structure required by the assignment (`readers_writers/semaphore/`, etc.).
* Adjusted the time delays to ensure the interleaving of threads was slow enough to clearly demonstrate the synchronization principles visually.

## Reflection on AI Errors and Limitations[cite: 3]
* **Error Identified:** The AI initially generated logical array indices for the chopsticks that did not match the physical SVG layout of the UI. This caused the script to instruct a philosopher to grab a chopstick from across the table. Consequently, the UI highlighted the chopstick as acquired, but the physical connecting line failed to draw.
* **Resolution and Takeaway:** I had to intervene and conceptually align the backend mathematical logic of the array with the frontend physical layout of the HTML table. This highlighted that while AI is highly proficient at generating syntax and boilerplate algorithms, it lacks spatial awareness of the physical UIs it generates. It requires human oversight to ensure the programmatic logic correctly maps to the visual representation.
