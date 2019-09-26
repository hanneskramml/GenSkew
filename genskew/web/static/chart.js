var ctx1 = document.getElementById('normalSkewChart').getContext('2d');
var ctx2 = document.getElementById('cumulativeSkewChart').getContext('2d');
var plot1 = $('#normalSkewChart').data('plot1');
var plot2 = $('#cumulativeSkewChart').data('plot2');

var chart1 = new Chart(ctx1, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Skew normal',
            backgroundColor: 'rgb(16,129,255)',
            borderColor: 'rgb(16,129,255)',
            fill: false,
            data: plot1.skew_normal,
            yAxisID: 'y-axis-normal',
        }]
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                scaleLabel: {
                    labelString: 'Position',
                }
            }],
            yAxes: [{
                type: 'linear',
                display: true,
                position: 'left',
                id: 'y-axis-normal',
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
        responsiveAnimationDuration: 0 // animation duration after a resize
    }
});

var chart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Skew cumulative',
            backgroundColor: 'rgb(255,221,49)',
            borderColor: 'rgb(255,221,49)',
            fill: false,
            data: plot2.skew_cumulative,
            yAxisID: 'y-axis-cumulative',
        }]
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                scaleLabel: {
                    labelString: 'Position',
                }
            }],
            yAxes: [{
                type: 'linear',
                display: true,
                position: 'left',
                id: 'y-axis-cumulative',
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
        responsiveAnimationDuration: 0 // animation duration after a resize
    }
});