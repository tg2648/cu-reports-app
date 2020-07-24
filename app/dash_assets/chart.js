var trace1 = {
    x: [0, 1, 2, 3, 4, 5, 6],
    y: [1, 9, 4, 7, 5, 2, 4],
    mode: 'markers',
    marker: {
        size: [20, 40, 25, 10, 60, 90, 30],
    }
};

var data = [trace1];

var layout = {
    // title: 'Chart',
    showlegend: false,
    margin: {
        t: 50,
        l: 30,
        // r: 30,
        // b: 30
    }
};

var config = {
    responsive: true,
    displayModeBar: false,
    // autosize: true // set autosize to rescale
}

Plotly.newPlot('chart', data, layout, config);

// update the layout to expand to the available size
// when the window is resized
// window.onresize = function() {
//     Plotly.relayout('chart', {
//         'xaxis.autorange': true,
//         'yaxis.autorange': true
//     });
// };