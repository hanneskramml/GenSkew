var ctx1 = document.getElementById('normalSkewChart').getContext('2d');
var ctx2 = document.getElementById('cumulativeSkewChart').getContext('2d');
var data = $('#normalSkewChart').data('plot');

var drawHLines = [];
data.separator_pos.forEach(function(obj) {
    drawHLines.push({
        type: 'line',
        mode: 'vertical',
        scaleID: 'x-axis-0',
        value: obj,
        borderColor: 'brown',
        borderWidth: 1,
        borderDash: [2, 2]
    })
});
drawHLines.push({
    type: 'line',
    mode: 'vertical',
    scaleID: 'x-axis-0',
    value: data.origin,
    borderColor: 'rgba(255, 0, 0, 0.5)',
    borderWidth: 2,
    label: {
        enabled: true,
        position: 'top',
        yAdjust: 10,
        fontStyle: 'normal',
        content: 'origin'
    }
});

var chartOptions = {
    responsive: true,
    scales: {
        xAxes: [{
            type: 'linear',
            position: 'bottom',
            id: 'x-axis-0',
            scaleLabel: {
                labelString: 'Position',
            }
        }],
        yAxes: [{
            type: 'linear',
            display: true,
            position: 'left',
        }],
    },
    elements: {
        line: {
            tension: 0, // disables bezier curves (performance)
            borderWidth: 1,
        },
        point: {
            radius: 0,
        }
    },
    tooltips: {
        mode: 'index',
        intersect: false,
        position: 'nearest',
    },
    //events: ['click'],
    animation: {
        duration: 0 // general animation time
    },
    hover: {
        animationDuration: 0 // duration of animations when hovering an item
    },
    responsiveAnimationDuration: 0, // animation duration after a resize
    annotation: {
        drawTime: 'afterDraw',
        annotations: drawHLines
    }
};

var normalSkewChart = new Chart(ctx1, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Skew normal',
            backgroundColor: 'rgb(16,129,255)',
            borderColor: 'rgb(16,129,255)',
            fill: false,
            data: data.skew_normal,
        }]
    },
    options: chartOptions
});

var cumulativeSkewChart = new Chart(ctx2, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Skew cumulative',
            backgroundColor: 'rgb(255,221,49)',
            borderColor: 'rgb(255,221,49)',
            fill: false,
            data: data.skew_cumulative,
        }]
    },
    options: chartOptions
});