const { ipcRenderer } = require('electron');
const merge = require('deepmerge');
console.log("renderer.js is loaded");

const assignState = (state, extensionsList) => {
    return Object.assign.apply(null, [{ state }, ...extensionsList.map(fn => fn(state))]);
};

const mergeObjectStructures = (destination, source) => merge(destination, source);

module.exports = {
    assignState,
    mergeObjectStructures
};

function handleFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const code = event.target.result;
            document.getElementById('codeArea').value = code;
            displayActualCode(code, 'actualCode');
            validateCode(code);
            handleJSCodeUpload(code); 
        };
        reader.readAsText(file);
    }
}

function handleCodePaste() {
    const code = document.getElementById('codeArea').value;
    if (code) {
        displayActualCode(code, 'actualCode');
        validateCode(code);
        handleJSCodeUpload(code);
    }
}

function validateCode(code) {
    ipcRenderer.send('upload-code', code);
}

function handleJSCodeUpload(code) {
    displayActualCode(code, 'jsActualCode');
    ipcRenderer.send('upload-js-code', code);
}

ipcRenderer.on('code-validation-result', (event, validationResult) => {
    if (validationResult.isValid) {
        parseCodeStructure(document.getElementById('codeArea').value);
    } else {
        console.error("Code validation failed");
    }
});

ipcRenderer.on('code-parse-result', (event, parseResult) => {
    if (parseResult.success) {
        renderGraph(parseResult.data, 'graph');
    } else {
        console.error("Failed to parse the Python code structure");
    }
});

ipcRenderer.on('js-code-parse-result', (event, parseResult) => {
    if (parseResult.success) {
        renderGraph(parseResult.data, 'jsGraph');
    } else {
        console.error("Failed to parse the JavaScript code structure");
    }
});

function parseCodeStructure(code) {
    ipcRenderer.send('parse-code', code);
}

function displayActualCode(code, elementId) {
    const codeElement = document.getElementById(elementId);
    const lines = code.split('\n');
    codeElement.innerHTML = '';
    lines.forEach((line, index) => {
        const lineElement = document.createElement('span');
        lineElement.id = `${elementId}-line-${index}`;
        lineElement.innerText = line;
        lineElement.appendChild(document.createElement('br'));
        codeElement.appendChild(lineElement);
    });
}

function renderGraph(graphData, svgId) {
    const svg = d3.select(`#${svgId}`);
    const nodes = svg.selectAll("circle")
        .data(graphData.nodes)
        .enter()
        .append("circle")
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .attr("r", 5);
    nodes.on("click", function(event, d) {
        const nodeDetailsDiv = document.getElementById(svgId === 'graph' ? 'nodeDetails' : 'jsNodeDetails');
        nodeDetailsDiv.innerHTML = `Selected Node ID: ${d.id}`;
        highlightCodeLine(d.lineNumber, svgId === 'graph' ? 'actualCode' : 'jsActualCode');
    });
}

function highlightCodeLine(lineNumber, elementId) {
    const allLines = document.querySelectorAll(`#${elementId} span`);
    allLines.forEach(line => line.style.backgroundColor = '');
    const lineElement = document.getElementById(`${elementId}-line-${lineNumber}`);
    if (lineElement) {
        lineElement.style.backgroundColor = 'yellow';
    }
}

document.getElementById('codeArea').addEventListener('input', handleCodePaste);
document.getElementById('jsCodeArea').addEventListener('input', handleCodePaste); // 添加对JavaScript代码的监听

window.handleFileUpload = handleFileUpload;
window.handleCodePaste = handleCodePaste;
