function sort_by(key, order)
{
    const url = new URL(window.location.href);
    url.searchParams.set("sort", key);
    url.searchParams.set("order", order);
    window.location.href = url.toString();
}

function search_table()
{
    const input = document.getElementById("search-input").value.toLowerCase();
    const rows = document.querySelectorAll("#agencies-table tbody tr");

    for (let i = 0; i < rows.length; i++)
    {
        const row = rows[i];
        if (row.classList.contains("collapse"))
        {
            row.style.display = ""; // leave as is, we handle child visibility through parent
            continue;
        }

        const cells = row.querySelectorAll("td");
        const match = Array.from(cells).some(cell =>
            cell.textContent.toLowerCase().includes(input)
        );

        row.style.display = match ? "" : "none";

        const collapseButton = row.querySelector(".toggle-arrow");
        if (collapseButton)
        {
            const collapseId = collapseButton.getAttribute("data-bs-target");
            const childRow = document.querySelector(collapseId);
            if (childRow)
            {
                childRow.style.display = match ? "" : "none";
            }
        }
    }
}


const combinedData = chart_labels.map((label, idx) => {
    return { label: label, value: chart_data[idx] };
});

// Sort by value descending and take top 20
const top20 = combinedData
    .sort((a, b) => b.value - a.value)
    .slice(0, 20);

// Separate labels and values again
const topLabels = top20.map(item => item.label);
const topValues = top20.map(item => item.value);

// Generate gradient colors from orange (#FFA500) to yellow (#FFFF00)
const gradientColors = topValues.map((_, idx) => {
    const ratio = idx / (topValues.length - 1);
    const r = 255;
    const g = Math.round(165 + (255 - 165) * ratio);
    const b = 0;
    return `rgb(${r}, ${g}, ${b})`;
});

const bar_ctx = document.getElementById('sectionPieChart').getContext('2d');

const sectionBarChart = new Chart(bar_ctx, {
    type: 'bar',
    data: {
        labels: topLabels,
        datasets: [{
            label: 'Word Count per Agency',
            data: topValues,
            backgroundColor: gradientColors,
            borderColor: '#fff',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'x', // vertical bars
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const total = total_words;
                        const value = context.parsed.y ?? context.parsed.x;
                        const percentage = ((value / total) * 100).toFixed(2);
                        return `${context.label}: ${value.toLocaleString()} words (${percentage}%)`;
                    }
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                ticks: {
                    precision: 0
                }
            }
        }
    }
});


amendment_ctx = document.getElementById('amendments-chart').getContext('2d');

const amendments_chart = new Chart(amendment_ctx, {
    type: 'line',
    data: {
        labels: amendmentLabels,
        datasets: [{
            label: "Total Regulatory Amendments",
            data: amendmentData,
            borderColor: '#fdbb24',
            backgroundColor: 'rgba(251, 130, 28, 0.2)',
            tension: 0.3,
            fill: true,
            pointRadius: 3
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false, // control height freely
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date (YYYY-MM)'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Total Regulatory Amendments Passed'
                }
            }
        }
    }
});


covid_ctx = document.getElementById('covid-amendments-chart').getContext('2d');

const covid_amendments_chart = new Chart(covid_ctx, {
    type: 'line',
    data: {
        labels: covidAmendmentLabels,
        datasets: [{
            label: "COVID Related Regulatory Amendments",
            data: covidAmendmentData,
            borderColor: '#fdbb24',
            backgroundColor: 'rgba(251, 130, 28, 0.2)',
            tension: 0.3,
            fill: true,
            pointRadius: 3
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false, // control height freely
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date (YYYY-MM)'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Total COVID Related Regulatory Amendments Passed'
                }
            }
        }
    }
});
