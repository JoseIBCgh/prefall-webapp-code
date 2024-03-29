const STREAM_WIDTH = 10;
var count_acc = 1;
var count_gyr = 1;
var count_mag = 1;
var count_3d = 1;
function buildChart() {

    console.log("buildChart")
    var colorlist = ['#FF3333','#4CFF33', '#3371FF']
    // Fetch the sample data for the plots
    paciente = document.currentScript.getAttribute('paciente'); 
    num_test = document.currentScript.getAttribute('num_test'); 
    var url = `/test_data/`+paciente+`/`+num_test;
    d3.json(url).then(function(response) {
        const item = response.item;
        const acc_x = response.acc_x;
        const acc_y = response.acc_y;
        const acc_z = response.acc_z;
        const gyr_x = response.gyr_x;
        const gyr_y = response.gyr_y;
        const gyr_z = response.gyr_z;
        const mag_x = response.mag_x;
        const mag_y = response.mag_y;
        const mag_z = response.mag_z;
  
    /*=========Build a bubble plot ==============*/
        var acc_x_data = {
            x: item,
            y: acc_x,
            name: "Acelerometro X"
        };
        var acc_y_data = {
            x: item,
            y: acc_y,
            name: "Acelerometro Y"
        };
        var acc_z_data = {
            x: item,
            y: acc_z,
            name: "Acelerometro Z"
        };
        var data_acc = [acc_x_data, acc_y_data, acc_z_data];
        var layout = {
            title: "Acelerometro",
            xaxis:{title:"item"},
            yaxis:{title:"m/s^2"},
        };
        Plotly.newPlot('acc', data_acc, layout, {responsive: true});

        var gyr_x_data = {
            x: item,
            y: gyr_x,
            name: "Giroscopio X"
        };
        var gyr_y_data = {
            x: item,
            y: gyr_y,
            name: "Giroscopio Y"
        };
        var gyr_z_data = {
            x: item,
            y: gyr_z,
            name: "Giroscopio Z"
        };
        var data_gyr = [gyr_x_data, gyr_y_data, gyr_z_data];
        var layout = {
            title: "Giroscopio",
            xaxis:{title:"item"},
            yaxis:{title:"deg/s"},
        };
        Plotly.newPlot('gyr', data_gyr, layout, {responsive: true});

        var mag_x_data = {
            x: item,
            y: mag_x,
            name: "Magnetometro X"
        };
        var mag_y_data = {
            x: item,
            y: mag_y,
            name: "Magnetometro Y"
        };
        var mag_z_data = {
            x: item,
            y: mag_z,
            name: "Magnetometro Z"
        };
        var data_mag = [mag_x_data, mag_y_data, mag_z_data];
        var layout = {
            title: "Magnetometro",
            xaxis:{title:"item"},
            yaxis:{title:"Tesla"},
        };
        Plotly.newPlot('mag', data_mag, layout, {responsive: true});



        Plotly.newPlot('acc_stream', get_initial_data(item, acc_x, acc_y, acc_z, "Acelerometro"))

        var interval_acc = create_interval(item, acc_x, acc_y, acc_z, "count_acc", "acc_stream");

        const play_acc = document.getElementById("play_acc");
        play_acc.onclick = function(){
            interval_acc = create_interval(item, acc_x, acc_y, acc_z, "count_acc", "acc_stream");
        }
        const stop_acc = document.getElementById("stop_acc");
        stop_acc.onclick = function(){
            clearInterval(interval_acc)
            count_acc = 1
            Plotly.react('acc_stream', get_initial_data(item, acc_x, acc_y, acc_z, "Acelerometro"))
        }

        const pause_acc = document.getElementById("pause_acc");
        pause_acc.onclick = function(){
            clearInterval(interval_acc)
        }



        Plotly.newPlot('gyr_stream', get_initial_data(item, gyr_x, gyr_y, gyr_z, "Giroscopio"))

        var interval_gyr = create_interval(item, gyr_x, gyr_y, gyr_z, "count_gyr", "gyr_stream");

        const play_gyr = document.getElementById("play_gyr");
        play_gyr.onclick = function(){
            interval_gyr = create_interval(item, gyr_x, gyr_y, gyr_z, "count_gyr", "gyr_stream");
        }
        const stop_gyr = document.getElementById("stop_gyr");
        stop_gyr.onclick = function(){
            clearInterval(interval_gyr)
            count_gyr = 1
            Plotly.react('gyr_stream', get_initial_data(item, gyr_x, gyr_y, gyr_z, "Giroscopio"))
        }

        const pause_gyr = document.getElementById("pause_gyr");
        pause_gyr.onclick = function(){
            clearInterval(interval_gyr)
        }



        Plotly.newPlot('mag_stream', get_initial_data(item, gyr_x, gyr_y, gyr_z, "Magnetometro"))

        var interval_mag = create_interval(item, gyr_x, gyr_y, gyr_z, "count_mag", "mag_stream");

        const play_mag = document.getElementById("play_mag");
        play_mag.onclick = function(){
            interval_mag = create_interval(item, mag_x, mag_y, mag_z, "count_mag", "mag_stream");
        }
        const stop_mag = document.getElementById("stop_mag");
        stop_mag.onclick = function(){
            clearInterval(interval_mag)
            count_mag = 1
            Plotly.react('mag_stream', get_initial_data(item, mag_x, mag_y, mag_z, "Magnetometro"))
        }

        const pause_mag = document.getElementById("pause_mag");
        pause_mag.onclick = function(){
            clearInterval(interval_mag)
        }
/*
        let data_3d = [{
            type: 'scatter3d',
            mode: 'lines',
            x: [acc_x[0]],
            y: [acc_y[0]],
            z: [acc_z[0]],
            opacity: 1,
            line: {
              width: 6,
              color: '#42adf5',
              reversescale: false
            }
        }]

        var layout_3d = {
            scene:{
               aspectmode: "manual",
             aspectratio: {
               x: 1, y: 1, z: 1,
              },
            xaxis: {
                  range: [Math.min(acc_x), Math.max(acc_x)],
                  fixedrange: true,
                },
            yaxis: {
                range: [Math.min(acc_y), Math.max(acc_y)],
                fixedrange: true,
            },
            zaxis: {
                range: [Math.min(acc_z), Math.max(acc_z)],
                fixedrange: true,
            }},
          };

        Plotly.newPlot('3d_plot', data_3d, layout_3d);
        var interval3d = setInterval(function(){
            Plotly.extendTraces('3d_plot', {
                x: [[acc_x[count_3d]]],
                y: [[acc_y[count_3d]]],
                z: [[acc_z[count_3d]]]
            }, [0], 3)
    
            count_3d++;
            if(count_3d >= acc_x.length) clearInterval(interval3d);
        }, 400)
        */
        var intensity = [0, 0.14285714285714285, 0.2857142857142857, 0.42857142857142855, 0.5714285714285714, 0.7142857142857143, 0.8571428571428571, 1];


        var data = [{
        
            type: "mesh3d",
        
            x: [0, 0, 1, 1, 0, 0, 1, 1],
        
            y: [0, 1, 1, 0, 0, 1, 1, 0],
        
            z: [0, 0, 0, 0, 1, 1, 1, 1],
        
            i: [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        
            j: [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        
            k: [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        
            intensity: intensity,
        
            colorscale: [
        
              [0, 'rgb(255, 0, 255)'],
        
              [0.5, 'rgb(0, 255, 0)'],
        
              [1, 'rgb(0, 0, 255)']
        
            ]
        
          },
          {
        
            type: "mesh3d",
        
            x: [0, 0, 1, 1, 0, 0, 1, 1],
        
            y: [0, 1, 1, 0, 0, 1, 1, 0],
        
            z: [0, 0, 0, 0, 1, 1, 1, 1],
        
            i: [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        
            j: [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        
            k: [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        
            intensity: intensity,
        
            colorscale: [
        
              [0, 'rgb(255, 0, 255)'],
        
              [0.5, 'rgb(0, 255, 0)'],
        
              [1, 'rgb(0, 0, 255)']
        
            ]
        
          },
          {
        
            type: "mesh3d",
        
            x: [0, 0, 1, 1, 0, 0, 1, 1],
        
            y: [0, 1, 1, 0, 0, 1, 1, 0],
        
            z: [0, 0, 0, 0, 1, 1, 1, 1],
        
            i: [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        
            j: [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        
            k: [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        
            intensity: intensity,
        
            colorscale: [
        
              [0, 'rgb(255, 0, 255)'],
        
              [0.5, 'rgb(0, 255, 0)'],
        
              [1, 'rgb(0, 0, 255)']
        
            ]
        
          }
        
        ];
        
    });
}
function get_initial_data(item, x, y, z, name){
    const data = [{
        x: [item[0]],
        y: [x[0]],
        mode: 'lines',
        line: {color: '#42adf5'},
        name: name + " X"
    }, {
        x: [item[0]],
        y: [y[0]],
        mode: 'lines',
        line: {color: '#f58742'},
        name: name + " Y"
    }, {
        x: [item[0]],
        y: [z[0]],
        mode: 'lines',
        line: {color: '#42f56c'},
        name: name + " Z"
    }];
    return data;
}
function create_interval(item, x, y, z, count_name, div){
    var interval = setInterval(function(){
        const count = window[count_name]
        Plotly.extendTraces(div, {
            x: [[item[count]], [item[count]], [item[count]]],
            y: [[x[count]], [y[count]], [z[count]]]
        }, [0, 1, 2])

        if(item[count] > STREAM_WIDTH){
            Plotly.relayout(div, {
                xaxis : {
                    range: [item[count] - STREAM_WIDTH, item[count]]
                }
            })
        }
        window[count_name] = window[count_name] + 1
        if(window[count_name] >= x.length) clearInterval(interval);
    }, 200)
    return interval
}
buildChart()
