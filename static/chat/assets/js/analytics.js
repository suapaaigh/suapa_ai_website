// Active Users count update
let activeUsers = 1342;
let viewsPerMinute = 320;
function updateCounters() {
    // Random fluctuation (simulate real-time data)
    activeUsers += Math.floor(Math.random() * 10) * (Math.random() > 0.5 ? 1 : -1);
    viewsPerMinute += Math.floor(Math.random() * 5) * (Math.random() > 0.5 ? 1 : -1);

    // Prevent negative values
    activeUsers = Math.max(0, activeUsers);
    viewsPerMinute = Math.max(0, viewsPerMinute);

    // Update DOM
    document.getElementById("activeUsers").textContent = activeUsers.toLocaleString();
    document.getElementById("viewsPerMinute").textContent = viewsPerMinute.toLocaleString();
}
// Call every 3 seconds
setInterval(updateCounters, 2000);

// Pure JavaScript Counter
const counters = document.querySelectorAll('.counter');
counters.forEach(counter => {
    const updateCount = () => {
    const target = +counter.getAttribute('data-target');
    const count = +counter.innerText;

    // Faster increment: increase this number for faster counting
    const increment = Math.max(target / 50, 1); // count in bigger steps

    if (count < target) {
        counter.innerText = Math.ceil(count + increment);
        setTimeout(updateCount, 10); // reduce delay for quicker animation
    } else {
        counter.innerText = target.toLocaleString(); // format the final number
    }
    };

    updateCount();
});


// Ecommerce Chart - Sales Over 7 Days
var ecomChart = new ApexCharts(document.querySelector("#ecom-chart"), {
    chart: {
        type: 'line',
        height: 340,
        toolbar: { show: false },
        dropShadow: {
            enabled: true,
            top: 5,
            left: 0,
            blur: 5,
            opacity: 0.3
        }
    },
    stroke: {
        curve: 'smooth',
        width: [4, 2]
    },
    series: [{
            name: 'Orders Received',
            data: [45, 60, 55, 70, 238, 100, 120]
        }, {
            name: 'Total Sales',
            data: [8000, 9500, 9000, 11000, 17000, 14000, 11000]
        }
    ],
    xaxis: {
        categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yaxis: [
        {
            title: {
                text: 'Orders / Units',
            },
        }, {
            opposite: true,
            title: {
                text: 'Sales ($)',
            },
        }
    ],
    tooltip: {
        shared: true,
        intersect: false
    },
    colors: ['var(--bs-primary)', 'var(--bs-success)'],
    legend: {
        show: true,
        position: 'bottom',
        horizontalAlign: 'center',
    }
});
ecomChart.render();

// AI Tools - Task Completion
var options = {
    chart: {
        type: 'line',
        height: 360,
        toolbar: { show: false },
        dropShadow: {
            enabled: true,
            top: 5,
            left: 0,
            blur: 5,
            opacity: 0.3
        }
    },
    stroke: {
        curve: 'smooth',
        width: [4, 2, 3, 1]
    },
    series: [
        { name: 'Text Generator', data: [120, 145, 160, 140, 180, 200, 170] },
        { name: 'Image Creator', data: [80, 90, 150, 120, 110, 100, 130] },
        { name: 'Chatbot Queries', data: [150, 240, 210, 170, 190, 175, 220] },
        { name: 'Code Assistant', data: [90, 95, 100, 88, 115, 130, 110] }
    ],
    xaxis: {
        categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    tooltip: {
        shared: true,
        intersect: false
    },
    colors: ['var(--bs-primary)', 'var(--bs-success)', 'var(--bs-gray-400)', 'var(--bs-secondary)'],
};
var chart = new ApexCharts(document.querySelector("#ai-chart"), options);chart.render();

// Projects - Status
// Income Analysis by Domain
var options = {
    chart: {
        height: 360,
        type: 'bar',
        toolbar: {
            show: false,
        },
    },
    colors: ['var(--bs-primary)'],
    grid: {
        yaxis: {
        lines: {
            show: false,
        }
        },
        padding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
        },
    },
    plotOptions: {
        bar: {
        horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    series: [{
        data: [378, 430, 248, 470, 715, 89, ]
    }],
    xaxis: {
        categories: ['Hospital', ' RealEsate', 'Education', 'ERP', 'Banking', 'Other'],
    }
    }
var chart = new ApexCharts(document.querySelector("#apex-AnalysisDomain"), options);
chart.render();
// Statistics by Technology
var options = {
    chart: {
        height: 360,
        type: 'bar',
        toolbar: {
            show: false,
        },
    },
    colors: ['var(--bs-primary)'],
    grid: {
        yaxis: {
        lines: {
            show: false,
        }
        },
        padding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
        },
    },
    plotOptions: {
        bar: {
        horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    series: [{
        data: [55, 75, 22, 49, 7, 39]
    }],
    xaxis: {
        categories: ['React', 'PHP', 'VueJs', 'Angular', 'Wordpress', 'DotNet'],
    }
    }
    var chart = new ApexCharts(document.querySelector("#apex-StatisticsbyTechnology"), options);
    chart.render();