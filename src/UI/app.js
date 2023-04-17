const configFileInput = document.getElementById('config-file-input');
async function handleConfigSelect(event) {
    const file = event.target.files[0];
    const config = await read(file);
    const ini = parseINI(config);
    buildForm(ini, 'config-file-form');
}

function buildForm(ini, id) {
    const form = document.getElementById(id);
    while (form.firstChild) {
        form.removeChild(form.firstChild);
    }

    form.classList.add('config-form');
    for (const section in ini) {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'section';
        const sectionHeader = document.createElement('h3');
        sectionHeader.innerText = section;
        sectionDiv.appendChild(sectionHeader);
        for (const key in ini[section]) {
            const kvpDiv = document.createElement('div');
            kvpDiv.className = 'key-value-pair';
            sectionDiv.appendChild(kvpDiv);
            const keyLabel = document.createElement('label');
            keyLabel.innerText = key;
            kvpDiv.appendChild(keyLabel);
            let valueInput;
            if (key === 'Rotation' || key === 'Name') {
                keyLabel.className = 'rotation-label';
            }
            if (key === 'Rotation') {
                valueInput = document.createElement('textarea');
                valueInput.className = 'rotation';
                valueInput.name = `${section}.${key}`;
                let value = ini[section][key];
                // convert string array to array
                value = value.replace('[', '');
                value = value.replace(']', '');
                value = value.split('\',');
                // remove quotes
                value = value.map((v) => v.replace(/'/g, ''));
                valueInput.value = value.join('\n');
                // set height of textarea
                valueInput.rows = value.length;

                keyLabel.style.alignSelf = 'flex-start';
            } else {
                valueInput = document.createElement('input');
                valueInput.className = 'rotation-input';
                valueInput.type = 'text';
                valueInput.name = `${section}.${key}`;
                valueInput.value = ini[section][key];
            }
            kvpDiv.appendChild(valueInput);
        }
        form.appendChild(sectionDiv);
    }

    const submitButton = document.createElement('button');
    submitButton.innerText = 'Save';
    submitButton.type = 'submit';
    form.appendChild(submitButton);
}


function read(file) {
    return new Promise((resolve, reject) => {
        const fileReader = new FileReader();

        fileReader.onload = () => {
            resolve(fileReader.result);
        };

        fileReader.onerror = () => {
            reject(fileReader.error);
        };

        fileReader.readAsText(file);
    });
}

function parseINI(config) {
    const ini = {};
    let section = ini;
    config.split(/\r?\n/).forEach((line, lineNumber) => {
        if (line.match(/^\s*;/)) {
            return;
        }
        const sectionMatch = line.match(/^\[(.*)\]$/);
        if (sectionMatch) {
            section = ini[sectionMatch[1]] = {};
        } else {
            const match = line.match(/^\s*(\w+)\s*=\s*(.*)\s*$/);
            if (match) {
                section[match[1]] = match[2];
            } else if (line.length === 0) {
                return;
            } else {
                console.error(`Line ${lineNumber + 1} '${line}' is invalid.`);
                throw new Error(`Line '${line}' is invalid.`);
            }
        }
    });
    return ini;
}


configFileInput.addEventListener('change', (event) => {
    handleConfigSelect(event);
    const file = event.target.files[0];
    const label = document.querySelector(`label[for="${event.target.id}"]`);
    label.innerText = file.name;
});

const configForm = document.getElementById('config-file-form');
configForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(configForm);
    saveFormData(formData);
});

function generateINI(config) {
    let ini = '';
    for (const section in config) {
        ini += `[${section}]\n`;
        for (const key in config[section]) {
            if (key === 'Rotation') {
                let value = config[section][key];
                value = value.split('\n');
                value = value.map((v) => `'${v}'`);
                config[section][key] = `[${value.join(',')}]`;
            }
            ini += `${key} = ${config[section][key]}\n`;
        }
        ini += '\n';
    }
    return ini;
}

function save(ini) {
    const blob = new Blob([ini], { type: 'text/plain' });
    const a = document.createElement('a');
    a.download = 'config.ini';
    a.href = URL.createObjectURL(blob);
    a.dataset.downloadurl = ['text/plain', a.download, a.href].join(':');
    a.click();
}

const newBindingsButton = document.getElementById('create-bindings-file');
newBindingsButton.addEventListener('click', () => {
    const bindings = {
        "Bindings": {
            "GAME": "",
            "PLAYER": "",
            "DU": "",
            "DD": "",
            "DL": "",
            "DR": "",
            "START": "",
            "BACK": "",
            "GUIDE": "",
            "LTHUMB": "",
            "RTHUMB": "",
            "LB": "",
            "RB": "",
            "A": "",
            "B": "",
            "X": "",
            "Y": "",
            "LT_DU": "",
            "LT_DD": "",
            "LT_DL": "",
            "LT_DR": "",
            "LT_START": "",
            "LT_BACK": "",
            "LT_GUIDE": "",
            "LT_LTHUMB": "",
            "LT_RTHUMB": "",
            "LT_LB": "",
            "LT_RB": "",
            "LT_A": "",
            "LT_B": "",
            "LT_X": "",
            "LT_Y": "",
            "RT_DU": "",
            "RT_DD": "",
            "RT_DL": "",
            "RT_DR": "",
            "RT_START": "",
            "RT_BACK": "",
            "RT_GUIDE": "",
            "RT_LTHUMB": "",
            "RT_RTHUMB": "",
            "RT_LB": "",
            "RT_RB": "",
            "RT_A": "",
            "RT_B": "",
            "RT_X": "",
            "RT_Y": "",
            "LTRT_DU": "",
            "LTRT_DD": "",
            "LTRT_DL": "",
            "LTRT_DR": "",
            "LTRT_START": "",
            "LTRT_BACK": "",
            "LTRT_GUIDE": "",
            "LTRT_LTHUMB": "",
            "LTRT_RTHUMB": "",
            "LTRT_LB": "",
            "LTRT_RB": "",
            "LTRT_A": "",
            "LTRT_B": "",
            "LTRT_X": "",
            "LTRT_Y": ""
        }
    };
    buildForm(bindings, 'bindings-file-form');
});

const bindingsForm = document.getElementById('bindings-file-form');
bindingsForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(bindingsForm);
    saveFormData(formData);
});

function saveFormData(formData) {
    const config = {};
    for (const [key, value] of formData) {
        const [section, keyName] = key.split('.');
        if (!config[section]) {
            config[section] = {};
        }
        config[section][keyName] = value;
    }
    const ini = generateINI(config);
    save(ini);
}

const bindingsFileInput = document.getElementById('bindings-file-input');
bindingsFileInput.addEventListener('change', (event) => {
    handleBindingsSelect(event);
    const file = event.target.files[0];
    const label = document.querySelector(`label[for="${event.target.id}"]`);
    label.innerText = file.name;
});

async function handleBindingsSelect(event) {
    const file = event.target.files[0];
    const config = await read(file);
    const ini = parseINI(config);
    buildForm(ini, 'bindings-file-form');
}

const rotationsFileInput = document.getElementById('rotations-file-input');
rotationsFileInput.addEventListener('change', (event) => {
    handleRotationsSelect(event);
    const file = event.target.files[0];
    const label = document.querySelector(`label[for="${event.target.id}"]`);
    label.innerText = file.name;
});

async function handleRotationsSelect(event) {
    const file = event.target.files[0];
    const config = await read(file);
    const ini = parseINI(config);
    buildForm(ini, 'rotations-file-form');
}

const rotationsForm = document.getElementById('rotations-file-form');
rotationsForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(rotationsForm);
    saveFormData(formData);
});

const newRotationsButton = document.getElementById('create-rotations-file');
newRotationsButton.addEventListener('click', () => {
    const rotations = {
        "ROT": {
            "Name": "",
            "Rotation": "",
        }
    };
    buildForm(rotations, 'rotations-file-form');
});

if ('serviceWorker' in navigator) {
    navigator.serviceWorker
        .register('service-worker.js')
        .then((registration) => {
            console.log('Service worker registered:', registration);
        })
        .catch((error) => {
            console.log('Service worker registration failed:', error);
        });
}
