// =========================
//   CONSTANTE & STARE
// =========================

// Codul hub-ului din viz_data.json (vezi "HUB1" în airport_states)
const HUB_ID = "HUB1";

const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const RADIUS = 260;
const SPOKE_CAPACITY_LIMIT = 200;
const HUB_CAPACITY_LIMIT = 3000;

const COLOR_MAP = {
    RED: "#ef4444",
    YELLOW: "#eab308",
    GREEN: "#22c55e",
    FADED: "#6b7280"
};

// Elemente UI
const canvas = document.getElementById("network-canvas");
const ctx = canvas.getContext("2d");

const dayDisplay = document.getElementById("current-day");
const timeDisplay = document.getElementById("current-hour");
const maxTimeSpan = document.getElementById("max-time");
const activeFlightsCount = document.getElementById("active-flights-count");

const reportsButton = document.getElementById("reports-button");

const airportSelector = document.getElementById("airport-selector");
const airportSearchInput = document.getElementById("airport-search");
const selectAllButton = document.getElementById("select-all-btn");
const selectedCountLabel = document.getElementById("selected-count");
const totalAirportsLabel = document.getElementById("total-airports-count");

const flightEventsList = document.getElementById("flight-events-list");
const eventsCountPill = document.getElementById("events-count-pill");

const nextHourButton = document.getElementById("next-hour");
const prevHourButton = document.getElementById("prev-hour");
const nextDayButton = document.getElementById("next-day");
const prevDayButton = document.getElementById("prev-day");

const darkModeToggle = document.getElementById("dark-mode-toggle");
const autoFilterBtn = document.getElementById("auto-filter-btn");
const manualFilterBtn = document.getElementById("manual-filter-btn");

const tooltip = document.getElementById("tooltip");

// Variabile de stare
let networkData = null;
let nodePositions = {};
let maxTimeStep = 0;
let currentTime = 0;

let allAirportIds = [];
let selectedAirportIds = [];
let autoFilterMode = true;
let hoveredAirportId = null;


// =========================
//   UTILITARE
// =========================

function calculatePositions(ids) {
    const positions = {};
    if (!ids || !ids.length) return positions;

    const spokeIds = ids.filter((id) => id !== HUB_ID);
    const numSpokes = spokeIds.length;

    const centerX = CANVAS_WIDTH / 2;
    const centerY = CANVAS_HEIGHT / 2;

    positions[HUB_ID] = [centerX, centerY];

    if (numSpokes === 0) return positions;

    const adjustedRadius = Math.min(RADIUS, CANVAS_WIDTH * 0.42);
    const angles = Array.from({ length: numSpokes }, (_, i) =>
        i * ((2 * Math.PI) / numSpokes) - Math.PI / 2
    );

    for (let i = 0; i < numSpokes; i++) {
        const angle = angles[i];
        const x = centerX + adjustedRadius * Math.cos(angle);
        const y = centerY + adjustedRadius * Math.sin(angle);
        positions[spokeIds[i]] = [x, y];
    }

    return positions;
}

function getAirportStatus(stock, capacity, airportId) {
    const capLimit = airportId === HUB_ID ? HUB_CAPACITY_LIMIT : SPOKE_CAPACITY_LIMIT;
    capacity = Math.max(capacity || 0, capLimit);

    if (stock < 0 || stock > capacity) {
        return { code: "RED", description: "Criză / supra-capacitate" };
    } else if (stock <= capacity * 0.2) {
        return { code: "YELLOW", description: "Stoc scăzut" };
    } else {
        return { code: "GREEN", description: "Stoc OK" };
    }
}

function clampTime(value) {
    if (!networkData) return 0;
    return Math.max(0, Math.min(value, maxTimeStep));
}

function updateTimeDisplay(time) {
    const day = Math.floor(time / 24);
    const hour = time % 24;
    dayDisplay.textContent = `Ziua ${day}`;
    timeDisplay.textContent = `Ora ${hour}:00`;

    prevHourButton.disabled = time <= 0;
    prevDayButton.disabled = time < 24;
    nextHourButton.disabled = time >= maxTimeStep;
    nextDayButton.disabled = time + 24 > maxTimeStep;
}

function getActiveAirports(time) {
    const active = new Set();
    const currentState = networkData.airport_states[time] || {};

    // 1) Aeroporturi implicate în zboruri (plecări/sosiri)
    const departuresNow = networkData.flight_events[time] || [];
    departuresNow.forEach((flight) => {
        active.add(flight.origin);
        active.add(flight.dest);
    });

    // 2) Aeroporturi al căror stoc s-a schimbat față de ora precedentă
    const prevTime = Math.max(0, time - 1);
    const prevState = networkData.airport_states[prevTime] || {};

    for (const id in currentState) {
        const currentStock = currentState[id].stock;
        const previousStock = prevState[id] ? prevState[id].stock : Number.NaN;
        if (currentStock !== previousStock) {
            active.add(id);
        }
    }

    // 3) Adaugă HUB dacă există orice activitate
    if (active.size > 0 && allAirportIds.includes(HUB_ID)) {
        active.add(HUB_ID);
    }

    let activeList = Array.from(active).filter((id) =>
        allAirportIds.includes(id)
    );

    // Limitează numărul maxim de noduri pentru claritate vizuală
    if (activeList.length > 28) {
        const withoutHub = activeList.filter((id) => id !== HUB_ID);
        const sliceCount = HUB_ID && allAirportIds.includes(HUB_ID) ? 27 : 28;
        activeList = (activeList.includes(HUB_ID) ? [HUB_ID] : []).concat(
            withoutHub.slice(0, sliceCount)
        );
    }

    return activeList;
}

function getFlightsInAir(time) {
    if (!networkData || !networkData.flight_events) return [];

    const active = [];

    const tMax = Math.min(time, maxTimeStep);
    for (let t = 0; t <= tMax; t++) {
        const departures = networkData.flight_events[t] || [];
        departures.forEach((flight) => {
            const travelTime = flight.travel_time || 1;
            if (time >= t && time < t + travelTime) {
                active.push({
                    ...flight,
                    start_time: t,
                    travel_time: travelTime
                });
            }
        });
    }

    return active;
}

function updateSelectedCount() {
    selectedCountLabel.textContent = selectedAirportIds.length.toString();
    totalAirportsLabel.textContent = allAirportIds.length.toString();
}


// =========================
//   UI – SELECTOR AEROPORT
// =========================

function populateAirportSelector() {
    airportSelector.innerHTML = "";
    const sortedIds = [...allAirportIds].sort();

    sortedIds.forEach((id) => {
        const option = document.createElement("option");
        option.value = id;
        option.textContent = id === HUB_ID ? `${id} (HUB)` : id;
        airportSelector.appendChild(option);
    });

    // Selectează toate implicit (folosit în modul manual)
    selectedAirportIds = [...allAirportIds];
    updateSelectedCount();

    airportSelector.addEventListener("change", () => {
        selectedAirportIds = Array.from(airportSelector.options)
            .filter((opt) => opt.selected)
            .map((opt) => opt.value);
        updateSelectedCount();
        autoFilterMode = false;
        setFilterModeButtons();
        drawNetworkFrame(currentTime);
    });

    selectAllButton.addEventListener("click", () => {
        Array.from(airportSelector.options).forEach((opt) => {
            opt.selected = true;
        });
        selectedAirportIds = [...allAirportIds];
        autoFilterMode = false;
        setFilterModeButtons();
        updateSelectedCount();
        drawNetworkFrame(currentTime);
    });

    airportSearchInput.addEventListener("input", () => {
        const q = airportSearchInput.value.trim().toLowerCase();
        Array.from(airportSelector.options).forEach((opt) => {
            if (!opt.value) return;
            opt.style.display = opt.value.toLowerCase().includes(q) ? "block" : "none";
        });
    });
}

function syncSelectorWithSelected() {
    Array.from(airportSelector.options).forEach((opt) => {
        opt.selected = selectedAirportIds.includes(opt.value);
    });
    updateSelectedCount();
}


// =========================
//   UI – MOD FILTRARE
// =========================

function setFilterModeButtons() {
    if (autoFilterMode) {
        autoFilterBtn.classList.add("chip-btn-active");
        manualFilterBtn.classList.remove("chip-btn-active");
    } else {
        manualFilterBtn.classList.add("chip-btn-active");
        autoFilterBtn.classList.remove("chip-btn-active");
    }
}

function initFilterModeControls() {
    autoFilterBtn.addEventListener("click", () => {
        autoFilterMode = true;
        setFilterModeButtons();
        updateVisualization(currentTime, true);
    });

    manualFilterBtn.addEventListener("click", () => {
        autoFilterMode = false;
        setFilterModeButtons();
        // nu schimbăm selecția, doar redesenăm
        drawNetworkFrame(currentTime);
    });
}


// =========================
//   UI – EVENIMENTE ZBOR
// =========================

function humanOriginDest(text) {
    // În prezent origin/dest sunt ID-uri lungi (UUID).
    // Le scurtăm ca să nu speriem user-ul :)
    if (!text) return "N/A";
    if (text.length <= 6) return text;
    return `${text.slice(0, 4)}…${text.slice(-3)}`;
}

function updateFlightEventsList(time) {
    const departures = (networkData.flight_events && networkData.flight_events[time]) || [];
    flightEventsList.innerHTML = "";

    if (!departures.length) {
        eventsCountPill.textContent = "0 zboruri";
        const empty = document.createElement("p");
        empty.className = "empty-state";
        empty.textContent = "Nu există evenimente de zbor la ora curentă.";
        flightEventsList.appendChild(empty);
        return;
    }

    eventsCountPill.textContent =
        departures.length === 1 ? "1 zbor" : `${departures.length} zboruri`;

    departures.forEach((flight) => {
        const card = document.createElement("div");
        const statusClass = (flight.status_code || "GREEN").toLowerCase();

        card.className = `flight-card ${statusClass}`;
        card.innerHTML = `
            <div class="flight-card-status-dot"></div>
            <div class="flight-id">${flight.id || "Flight"}</div>
            <div class="flight-badge">${flight.status_code || "GREEN"}</div>
            <div class="flight-route">
                ${humanOriginDest(flight.origin)} &rarr; ${humanOriginDest(flight.dest)}
            </div>
            <div class="flight-meta">
                Durată: ${flight.travel_time || "N/A"}h · Kituri: ${flight.kit_quantity ?? "N/A"}
            </div>
        `;

        card.addEventListener("click", () => {
            // doar highlight vizual în listă (nu avem mapare clară spre coduri aeroport)
            Array.from(flightEventsList.querySelectorAll(".flight-card")).forEach((c) =>
                c.classList.remove("selected")
            );
            card.classList.add("selected");
        });

        flightEventsList.appendChild(card);
    });
}


// =========================
//   DESENARE REȚEA PE CANVAS
// =========================

function updateActiveFlights(time) {
    const active = getFlightsInAir(time);
    activeFlightsCount.textContent = active.length.toString();
    return active;
}

function drawNetworkFrame(time) {
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    const states = networkData.airport_states[time] ||
        networkData.airport_states[Math.max(0, time - 1)] ||
        {};

    // Dacă nu avem nimic selectat (în mod manual), fă fallback la toate
    if (!selectedAirportIds.length) {
        selectedAirportIds = [...allAirportIds];
        syncSelectorWithSelected();
    }

    // Linii hub–spoke
    ctx.save();
    ctx.shadowBlur = 0;

    if (selectedAirportIds.includes(HUB_ID)) {
        const hubPos = nodePositions[HUB_ID];
        for (const id of selectedAirportIds) {
            if (id === HUB_ID) continue;
            const pos = nodePositions[id];
            if (!pos || !hubPos) continue;

            ctx.beginPath();
            ctx.moveTo(hubPos[0], hubPos[1]);
            ctx.lineTo(pos[0], pos[1]);
            ctx.strokeStyle = "rgba(148,163,184,0.7)";
            ctx.lineWidth = 1.2;
            ctx.stroke();
        }
    }
    ctx.restore();

    // Noduri aeroporturi
    for (const id of selectedAirportIds) {
        const pos = nodePositions[id];
        if (!pos) continue;

        const state = states[id];
        const stock = state ? state.stock : 0;
        const capacity = state ? state.capacity : undefined;
        const status = getAirportStatus(stock, capacity, id);

        const isHub = id === HUB_ID;
        const size = isHub ? 24 : 14;

        const nodeColor = COLOR_MAP[status.code] || "#6b7280";

        ctx.save();
        ctx.shadowBlur = 12;
        ctx.shadowColor = "rgba(15, 23, 42, 0.5)";

        if (isHub) {
            // HUB – pătrat rotunjit
            const x = pos[0] - size;
            const y = pos[1] - size;
            const w = size * 2;
            const h = size * 2;
            const r = 8;

            ctx.fillStyle = nodeColor;
            ctx.strokeStyle = "#0f172a";
            ctx.lineWidth = 4;

            ctx.beginPath();
            ctx.moveTo(x + r, y);
            ctx.lineTo(x + w - r, y);
            ctx.quadraticCurveTo(x + w, y, x + w, y + r);
            ctx.lineTo(x + w, y + h - r);
            ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
            ctx.lineTo(x + r, y + h);
            ctx.quadraticCurveTo(x, y + h, x, y + h - r);
            ctx.lineTo(x, y + r);
            ctx.quadraticCurveTo(x, y, x + r, y);
            ctx.closePath();

            ctx.fill();
            ctx.stroke();
        } else {
            // SPOKE – cerc
            ctx.beginPath();
            ctx.arc(pos[0], pos[1], size, 0, Math.PI * 2);
            ctx.fillStyle = nodeColor;
            ctx.fill();
            ctx.strokeStyle = "#020617";
            ctx.lineWidth = 2;
            ctx.stroke();
        }

        // Highlight pe hover
        if (id === hoveredAirportId) {
            ctx.beginPath();
            ctx.arc(pos[0], pos[1], size + 6, 0, Math.PI * 2);
            ctx.strokeStyle = "rgba(59,130,246,0.9)";
            ctx.lineWidth = 2;
            ctx.setLineDash([4, 3]);
            ctx.stroke();
            ctx.setLineDash([]);
        }

        ctx.restore();

        // Text deasupra nodului (cod aeroport)
        ctx.save();
        ctx.font = "11px system-ui";
        ctx.fillStyle = "rgba(209,213,219,0.96)";
        ctx.textAlign = "center";
        ctx.fillText(id, pos[0], pos[1] - size - 6);
        ctx.restore();
    }

    // Zboruri active – doar efect cosmetic (număr în header, fără trasee precise)
    updateActiveFlights(time);
}


// =========================
//   TOOLTIP NODURI
// =========================

function showNodeTooltip(id, x, y) {
    const states = networkData.airport_states[currentTime] ||
        networkData.airport_states[Math.max(0, currentTime - 1)] ||
        {};
    const state = states[id];

    const stock = state ? state.stock : 0;
    const capacity = state ? state.capacity : (id === HUB_ID ? HUB_CAPACITY_LIMIT : SPOKE_CAPACITY_LIMIT);
    const status = getAirportStatus(stock, capacity, id);

    tooltip.innerHTML = `
        <strong>${id === HUB_ID ? id + " – HUB central" : id}</strong><br />
        Stoc: ${stock}<br />
        Capacitate: ${capacity}<br />
        Status: ${status.description}
    `;
    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
    tooltip.style.display = "block";
}

function hideNodeTooltip() {
    tooltip.style.display = "none";
}

function initCanvasInteractions() {
    canvas.addEventListener("mousemove", (ev) => {
        if (!selectedAirportIds.length) return;

        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const x = (ev.clientX - rect.left) * scaleX;
        const y = (ev.clientY - rect.top) * scaleY;

        let foundId = null;
        for (const id of selectedAirportIds) {
            const pos = nodePositions[id];
            if (!pos) continue;
            const isHub = id === HUB_ID;
            const size = isHub ? 24 : 14;

            const dx = x - pos[0];
            const dy = y - pos[1];
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist <= size + 4) {
                foundId = id;
                break;
            }
        }

        if (foundId !== hoveredAirportId) {
            hoveredAirportId = foundId;
            drawNetworkFrame(currentTime);
        }

        if (foundId) {
            const tooltipX = ev.clientX - rect.left;
            const tooltipY = ev.clientY - rect.top - 10;
            showNodeTooltip(foundId, tooltipX, tooltipY);
        } else {
            hideNodeTooltip();
        }
    });

    canvas.addEventListener("mouseleave", () => {
        hoveredAirportId = null;
        hideNodeTooltip();
        drawNetworkFrame(currentTime);
    });
}


// =========================
//   NAVIGARE ÎN TIMP
// =========================

function handleTimeControl(incrementHours) {
    const newTime = clampTime(currentTime + incrementHours);
    updateVisualization(newTime, true);
}

function initTimeControls() {
    nextHourButton.addEventListener("click", () => handleTimeControl(1));
    prevHourButton.addEventListener("click", () => handleTimeControl(-1));
    nextDayButton.addEventListener("click", () => handleTimeControl(24));
    prevDayButton.addEventListener("click", () => handleTimeControl(-24));
}


// =========================
//   DARK MODE
// =========================

function applySavedTheme() {
    const saved = window.localStorage.getItem("dashboard-theme");
    if (saved === "dark") {
        document.body.classList.remove("light-theme");
        darkModeToggle.textContent = "☀️";
    } else {
        document.body.classList.add("light-theme");
        darkModeToggle.textContent = "🌙";
    }
}

function initDarkModeToggle() {
    applySavedTheme();
    darkModeToggle.addEventListener("click", () => {
        const isLight = document.body.classList.contains("light-theme");
        if (isLight) {
            document.body.classList.remove("light-theme");
            window.localStorage.setItem("dashboard-theme", "dark");
            darkModeToggle.textContent = "☀️";
        } else {
            document.body.classList.add("light-theme");
            window.localStorage.setItem("dashboard-theme", "light");
            darkModeToggle.textContent = "🌙";
        }
    });
}


// =========================
/*   VIZUALIZARE + INIT   */
// =========================

function updateVisualization(newTime, recalcFilter) {
    currentTime = clampTime(newTime);
    updateTimeDisplay(currentTime);

    if (autoFilterMode && recalcFilter) {
        selectedAirportIds = getActiveAirports(currentTime);
        syncSelectorWithSelected();
    }

    drawNetworkFrame(currentTime);
    updateFlightEventsList(currentTime);
}

function addGeneralListeners() {
    reportsButton.addEventListener("click", () => {
        window.open("rapoarte.html", "_blank");
    });
}

async function loadDataAndInit() {
    try {
        const response = await fetch("viz_data.json");
        if (!response.ok) {
            throw new Error(`Eroare la rețea: ${response.status} ${response.statusText}`);
        }

        networkData = await response.json();

        if (
            !networkData ||
            !networkData.airport_states ||
            !Object.keys(networkData.airport_states).length
        ) {
            throw new Error("Date JSON invalide sau lipsesc statele aeroporturilor.");
        }

        const timeSteps = Object.keys(networkData.airport_states).map(Number);
        maxTimeStep =
            typeof networkData.max_time_step === "number"
                ? networkData.max_time_step
                : Math.max(...timeSteps);

        const totalDays = networkData.max_days_arg ?? Math.ceil((maxTimeStep + 1) / 24);
        const totalHours = networkData.max_hours_arg ?? (maxTimeStep + 1);

        maxTimeSpan.textContent = `/ Simulat: ${totalDays} Zile (${totalHours} Ore)`;

        // aeroporturile sunt cheile primului timeslot
        const firstTimeKey = String(timeSteps.sort((a, b) => a - b)[0]);
        allAirportIds = Object.keys(networkData.airport_states[firstTimeKey]);
        nodePositions = calculatePositions(allAirportIds);

        populateAirportSelector();
        initFilterModeControls();
        initTimeControls();
        initCanvasInteractions();
        initDarkModeToggle();
        addGeneralListeners();

        setFilterModeButtons();
        updateVisualization(0, true);

        console.log("Vizualizarea web a fost încărcată cu succes.");
    } catch (error) {
        console.error("Eroare la încărcarea datelor:", error);
        const container = document.getElementById("network-visualizer");
        if (container) {
            container.innerHTML = `
                <p style="color: #f97373; padding: 18px; font-size: 0.95rem;">
                    Eroare: Nu s-au putut încărca datele din <strong>viz_data.json</strong>.<br />
                    Asigură-te că <code>app.py</code> a rulat și a generat fișierul înainte de a deschide dashboard-ul.<br />
                    Mesaj: ${error.message}
                </p>
            `;
        }
    }
}

loadDataAndInit();
