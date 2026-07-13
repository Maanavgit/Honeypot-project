// ======================================================
// HONEYPOT DASHBOARD
// ======================================================

// Timeline data passed from Flask
const timelineData = window.graphValues || [];

// Generate labels
const labels = window.graphLabels || [];

// ======================================================
// ATTACK PULSE GRAPH
// ======================================================

const canvas = document.getElementById("timelineChart");

if (canvas) {

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Attacks Per Minute",

                    data: timelineData,

                    borderColor: "#38bdf8",

                    backgroundColor: "rgba(56,189,248,0.18)",

                    fill: true,

                    borderWidth: 3,

                    pointRadius: 5,

                    pointHoverRadius: 7,

                    pointBackgroundColor: "#38bdf8",

                    tension: 0.35

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            animation: false,

            interaction: {

                intersect: false,

                mode: "index"

            },

            plugins: {

                legend: {

                    labels: {

                        color: "#ffffff",

                        font: {

                            size: 13

                        }

                    }

                }

            },

            scales: {

                x: {

                    title: {

                        display: true,

                        text: "Time (Minute)",

                        color: "#ffffff",

                        font: {

                            size: 14,

                            weight: "bold"

                        }

                    },

                    ticks: {

                        color: "#cbd5e1"

                    },

                    grid: {

                        color: "#334155"

                    }

                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        precision: 0,

                        color: "#cbd5e1"

                    },

                    title: {

                        display: true,

                        text: "Attack Count",

                        color: "#ffffff",

                        font: {

                            size: 14,

                            weight: "bold"

                        }

                    },

                    grid: {

                        color: "#334155"

                    }

                }

            }

        }

    });

}


// ======================================================
// AUTO REFRESH
// ======================================================

setInterval(function () {

    location.reload();

}, 3000);


// ======================================================
// LIVE STATUS ANIMATION
// ======================================================

const liveDot = document.querySelector(".live-dot");

if (liveDot) {

    setInterval(function () {

        liveDot.style.visibility =
            liveDot.style.visibility === "hidden"
            ? "visible"
            : "hidden";

    }, 700);

}
