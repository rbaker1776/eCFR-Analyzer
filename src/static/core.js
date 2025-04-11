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



// group entries < .9% into other
const total = chart_data.reduce((sum, val) => sum + val, 0);

const groupedLabels = [];
const groupedData = [];
let otherTotal = 0;

chart_labels.forEach((label, index) => {
    const value = chart_data[index];
    const percent = value / total;

    if (percent < 0.009) {
        otherTotal += value;
    } else {
        groupedLabels.push(label);
        groupedData.push(value);
    }
});

if (otherTotal > 0) {
    groupedLabels.push("Other");
    groupedData.push(otherTotal);
}

const pie_ctx = document.getElementById('sectionPieChart').getContext('2d');

const sectionPieChart = new Chart(pie_ctx, {
    type: 'pie',
    data: {
        labels: groupedLabels,
        datasets: [{
            label: 'Sections per Agency',
            data: groupedData,
            backgroundColor: [
                "#FFD700", "#FFC300", "#FFB000", "#FFA500", "#FF8C00",
                "#DAA520", "#B8860B", "#E1C16E", "#F0E68C", "#FFFACD",
                "#FFD700", "#FFC300", "#FFB000", "#FFA500", "#FF8C00"
            ].slice(0, groupedLabels.length),

            borderColor: '#fff',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false, // control height freely
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    font: {
                        size: 16
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const total = context.chart._metasets[0].total;
                        const value = context.parsed;
                        const percentage = ((value / total) * 100).toFixed(2);
                        return `${context.label}: ${value.toLocaleString()} words (${percentage}%)`;
                    }
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
            label: "Total Regulatory Amendments",
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
                    text: 'Total Regulatory Amendments Passed'
                }
            }
        }
    }
});
