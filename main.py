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
            .controls { margin-bottom: 25px; display: flex; justify-content: center; gap: 15px; align-items: center; flex-wrap: wrap; }
            button, select, input { background: #38bdf8; color: #0f172a; border: none; padding: 10px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; }
            select { background: #1e293b; color: #38bdf8; border: 1px solid #38bdf8; }
            button:disabled { background: #475569; cursor: not-allowed; }
            label { font-weight: bold; color: #94a3b8; }
            #array-container { display: flex; align-items: flex-end; justify-content: center; height: 320px; gap: 6px; background: #1e293b; padding: 20px; border-radius: 10px; }
            .bar { width: 28px; background: #38bdf8; border-radius: 4px 4px 0 0; transition: height 0.05s ease; }
            .bar.active { background: #f43f5e; }
            .bar.min { background: #a855f7; }
            .bar.sorted { background: #22c55e; }
        </style>
    </head>
    <body>
        <h1>📊 Sorting Algorithm Visualizer</h1>
        
        <div class="controls">
            <button id="reset-btn" onclick="generateArray()">Generate New Array</button>
            
            <select id="algo-select">
                <option value="bubble">Bubble Sort</option>
                <option value="selection">Selection Sort</option>
                <option value="insertion">Insertion Sort</option>
            </select>

            <label for="speed">Speed:</label>
            <input type="range" id="speed" min="10" max="300" value="100" style="direction: rtl;">

            <button id="sort-btn" onclick="runSelectedSort()">Start Sorting</button>
        </div>

        <div id="array-container"></div>

        <script>
            let array = [];
            const container = document.getElementById("array-container");
            const sortBtn = document.getElementById("sort-btn");
            const resetBtn = document.getElementById("reset-btn");
            const algoSelect = document.getElementById("algo-select");
            const speedInput = document.getElementById("speed");

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

            const sleep = () => new Promise(resolve => setTimeout(resolve, speedInput.value));

            function toggleControls(disabled) {
                sortBtn.disabled = disabled;
                resetBtn.disabled = disabled;
                algoSelect.disabled = disabled;
            }

            async function runSelectedSort() {
                toggleControls(true);
                const algo = algoSelect.value;
                if (algo === "bubble") await bubbleSort();
                else if (algo === "selection") await selectionSort();
                else if (algo === "insertion") await insertionSort();
                toggleControls(false);
            }

            async function bubbleSort() {
                const bars = document.getElementsByClassName("bar");
                for (let i = 0; i < array.length; i++) {
                    for (let j = 0; j < array.length - i - 1; j++) {
                        bars[j].classList.add("active");
                        bars[j+1].classList.add("active");
                        await sleep();

                        if (array[j] > array[j + 1]) {
                            [array[j], array[j + 1]] = [array[j + 1], array[j]];
                            bars[j].style.height = `${array[j] * 3.5}px`;
                            bars[j + 1].style.height = `${array[j + 1] * 3.5}px`;
                        }
                        bars[j].classList.remove("active");
                        bars[j+1].classList.remove("active");
                    }
                    bars[array.length - i - 1].classList.add("sorted");
                }
            }

            async function selectionSort() {
                const bars = document.getElementsByClassName("bar");
                for (let i = 0; i < array.length; i++) {
                    let minIdx = i;
                    bars[minIdx].classList.add("min");

                    for (let j = i + 1; j < array.length; j++) {
                        bars[j].classList.add("active");
                        await sleep();

                        if (array[j] < array[minIdx]) {
                            bars[minIdx].classList.remove("min");
                            minIdx = j;
                            bars[minIdx].classList.add("min");
                        } else {
                            bars[j].classList.remove("active");
                        }
                    }

                    if (minIdx !== i) {
                        [array[i], array[minIdx]] = [array[minIdx], array[i]];
                        bars[i].style.height = `${array[i] * 3.5}px`;
                        bars[minIdx].style.height = `${array[minIdx] * 3.5}px`;
                    }
                    
                    bars[minIdx].classList.remove("min");
                    bars[i].classList.add("sorted");
                }
            }

            async function insertionSort() {
                const bars = document.getElementsByClassName("bar");
                bars[0].classList.add("sorted");

                for (let i = 1; i < array.length; i++) {
                    let key = array[i];
                    let j = i - 1;
                    bars[i].classList.add("active");
                    await sleep();

                    while (j >= 0 && array[j] > key) {
                        array[j + 1] = array[j];
                        bars[j + 1].style.height = `${array[j + 1] * 3.5}px`;
                        bars[j].classList.add("active");
                        await sleep();
                        bars[j].classList.remove("active");
                        j--;
                    }
                    array[j + 1] = key;
                    bars[j + 1].style.height = `${key * 3.5}px`;
                    bars[i].classList.remove("active");

                    for (let k = 0; k <= i; k++) {
                        bars[k].classList.add("sorted");
                    }
                }
            }

            generateArray();
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)