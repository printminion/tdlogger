'use strict';

function test_drawVisualisation() {
    var data = [
        ['time', ''],
        ['10:00', 165 ],
        ['11:00', 135 ],
        ['12:00', 157 ],
        ['13:00', 139 ],
        ['14:00', 136 ]
    ];
    drawVisualization(data);
}

function drawVisualization(data) {

    var dataArr = google.visualization.arrayToDataTable(data);

    // Create and draw the visualization.
    var ac = new google.visualization.AreaChart(document.getElementById('visualization'));
    ac.draw(dataArr, {
        width: 400,
        height: 200,
        vAxis: {title: "messages"},
        hAxis: {title: "time"}
    });
}