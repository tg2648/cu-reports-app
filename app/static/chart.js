var trace1 = {
    x: ['January', 'February', 'April', 'March', 'May'],
    y: [20, 14, 23, 25, 22],
    marker:{
      color: ['rgba(204,204,204,1)', 'rgba(222,45,38,0.8)', 'rgba(204,204,204,1)', 'rgba(204,204,204,1)', 'rgba(204,204,204,1)']
    },
    width: [0.6, 0.6, 0.6, 0.6, 0.6],
    type: 'bar'
  };
  
var data = [trace1];

var layout = {
    title: 'Sample chart',
    showlegend: false,
    margin: {
        t: 50,
        l: 30,
    }
};

var config = {
    responsive: true,
    displayModeBar: false,
}

Plotly.newPlot('chart', data, layout, config);
