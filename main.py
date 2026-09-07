from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>DSA Sorting Visualizer</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; text-align: center; }
            .controls { margin-bottom: 25px; display: flex; justify-content: center; gap: 15px; align-items: center; }
            button { background: #38bdf8; color: #0f172a; border: none; padding: 10px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; }
            button:disabled { background: #475569; cursor: not-allowed; }
            #array-container { display: flex; align-items: flex-end; justify-content: center; height: 320px; gap: 6px; background: #1e293b; padding: 20px; border-radius: 10px; }
            .bar { width: 28px; background: #38bdf8; border-radius: 4px 4px 0 0; transition: height 0.1s ease, background-color 0.1s ease; }
            .bar.active { background: #f43f5e; } /* Highlight active comparison */
            .bar.sorted { background: #22c55e; } /* Highlight completed elements */
        </style>
    </head>
    <body>
        <h1>📊 Sorting Algorithm Visualizer</h1>
        
        <div class="controls">
            <button id="reset-btn" onclick="generateArray()">Generate New Array</button>
            <button id="sort-btn" onclick="startBubbleSort()">Start Bubble Sort</button>
        </div>

        <div id="array-container"></div>

        <script>
            let array = [];
            const container = document.getElementById("array-container");
            const sortBtn = document.getElementById("sort-btn");
            const resetBtn = document.getElementById("reset-btn");

            function generateArray() {
                array = [];
                container.innerHTML = "";
                for (let i = 0; i < 20; i++) {
                    const value = Math.floor(Math.random() * 80) + 10;
                    array.push(value);
                    const bar = document.createElement("div");
                    bar.classList.add("bar");
                    bar.style.height = `${value * 3.5}px`;
                    bar.id = `bar-${i}`;
                    container.appendChild(bar);
                }
            }

            const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

            async function startBubbleSort() {
                sortBtn.disabled = true;
                resetBtn.disabled = true;
                const bars = document.getElementsByClassName("bar");

                for (let i = 0; i < array.length; i++) {
                    for (let j = 0; j < array.length - i - 1; j++) {
                        // Highlight comparing bars
                        bars[j].classList.add("active");
                        bars[j+1].classList.add("active");

                        await sleep(100);

                        if (array[j] > array[j + 1]) {
                            // Swap values
                            let temp = array[j];
                            array[j] = array[j + 1];
                            array[j + 1] = temp;

                            // Update visual heights
                            bars[j].style.height = `${array[j] * 3.5}px`;
                            bars[j + 1].style.height = `${array[j + 1] * 3.5}px`;
                        }

                        bars[j].classList.remove("active");
                        bars[j+1].classList.remove("active");
                    }
                    bars[array.length - i - 1].classList.add("sorted");
                }

                sortBtn.disabled = false;
                resetBtn.disabled = false;
            }

            // Generate initial array on load
            generateArray();
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)