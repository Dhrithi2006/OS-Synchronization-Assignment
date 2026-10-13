# References and Acknowledgements

## Academic Textbooks & Foundational Papers
1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley. 
   *(Used as the theoretical foundation for process synchronization, the Readers-Writers problem, the Dining Philosophers problem, mutual exclusion, and deadlock prevention strategies).*
2. Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems* (4th ed.). Pearson. 
   *(Referenced for comparative analysis of Interprocess Communication (IPC) techniques and the nuances of classical synchronization problems).*
3. Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. (2018). *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books. 
   *(Referenced for modern explanations of building monitor-like structures using locks and condition variables).*
4. Dijkstra, E. W. (1965). *Co-operating sequential processes*. Technological University Eindhoven. 
   *(The original foundational paper credited with inventing Semaphores and conceptualizing the Dining Philosophers problem).*
5. Hoare, C. A. R. (1974). *Monitors: an operating system structuring concept*. Communications of the ACM, 17(10), 549-557. 
   *(The original academic framework defining the Monitor synchronization construct).*

## Technical Documentation
6. Python Software Foundation. (n.d.). *threading — Thread-based parallelism*. Python Documentation. Retrieved from https://docs.python.org/3/library/threading.html
   *(Used as the primary reference for implementing `threading.Semaphore`, `threading.Lock`, `threading.Condition`, and overall thread lifecycle management).*
7. Python Software Foundation. (n.d.). *json — JSON encoder and decoder*. Python Documentation. Retrieved from https://docs.python.org/3/library/json.html
   *(Used to serialize the execution traces and thread state data from the backend into a format readable by the frontend HTML).*
8. Python Software Foundation. (n.d.). *time — Time access and conversions*. Python Documentation. Retrieved from https://docs.python.org/3/library/time.html
   *(Referenced for utilizing `time.sleep()` to safely force thread interleavings, making concurrent behavior visible without breaking actual synchronization).*
9. MDN Web Docs. (n.d.). *SVG: Scalable Vector Graphics*. Mozilla. Retrieved from https://developer.mozilla.org/en-US/docs/Web/SVG
   *(Referenced for creating the dynamically glowing connection lines in the generated HTML simulation to visually map chopstick ownership).*
10. MDN Web Docs. (n.d.). *Document Object Model (DOM)*. Mozilla. Retrieved from https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model
    *(Used for the JavaScript logic that parses the JSON event log and dynamically manipulates CSS classes and text nodes during the simulation playback).*

## Artificial Intelligence Tools
11. Google Gemini. 
    *(Used as a programming assistant for generating the boilerplate Python threading code, structuring the HTML/SVG visualization dashboard, and refining the markdown documentation. See `ai_prompts/prompts.md` for the complete usage log).*
