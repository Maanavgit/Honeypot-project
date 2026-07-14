// ======================================================
// HONEYPOT DASHBOARD
// ======================================================

// Graph data from Flask

const labels = window.graphLabels || [];

const graphData = window.graphValues || [];


// ======================================================
// BAR CHART
// ======================================================

const canvas = document.getElementById("timelineChart");

if (canvas) {

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Commands per Minute",

                    data: graphData,

                    backgroundColor: "#38bdf8",

                    borderColor: "#0ea5e9",

                    borderWidth: 1,

                    borderRadius: 5,

                    barPercentage: 0.75,

                    categoryPercentage: 0.8

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            animation: false,

            plugins: {

                legend: {

                    display: true,

                    labels: {

                        color: "#ffffff",

                        font: {

                            size: 13

                        }

                    }

                },

                tooltip: {

                    backgroundColor: "#1e293b",

                    titleColor: "#ffffff",

                    bodyColor: "#ffffff",

                    borderColor: "#38bdf8",

                    borderWidth: 1

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

                        stepSize: 1,

                        color: "#cbd5e1"

                    },

                    title: {

                        display: true,

                        text: "Commands Captured",

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
// LIVE STATUS BLINK
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