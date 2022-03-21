var counter = 0;
function buildChart() {

    console.log("buildChart")
    var colorlist = ['#FF3333','#4CFF33', '#3371FF']
    // Fetch the sample data for the plots
    paciente = document.currentScript.getAttribute('paciente'); 
    num_test = document.currentScript.getAttribute('num_test'); 
    var url = `/plot_data/`+num_test+`/`+paciente;
    d3.json(url).then(function(response) {
        const intercept = response.intercept;
        const coef0 = response.coef0;
        const coef1 = response.coef1;
        const coef2 = response.coef2;
        const acc_x = response.acc_x;
        const acc_y = response.acc_y;
        const acc_z = response.acc_z;
        console.log(intercept)
        console.log(coef0)
        console.log(coef1)
        console.log(coef2)
        const N = 20;
        tmp = range(N, -1, 0.1)
        var x = []
        var y = []
        for(let i = 0; i< N; i++){
            for(let j = 0; j < N; j++){
                x.push(tmp[i])
                y.push(tmp[j])
            }
        }
        var z = []
        for(let i = 0; i < x.length; i++){
            z.push(calcZ(x[i], y[i],intercept, coef0, coef1, coef2))
        }
        /*
        var data_boundary=

            {   
              color:'rgb(100,100,100)',
              type: 'mesh3d',
              x: x,
              y: y,
              z: z,
            };

        var data_points =
            {
                type: 'scatter3d',
                mode: 'markers',
                marker: {
                    color: 'rgb(0, 200, 0)',
                    size: 2,
            
                    opacity: 0.8
                },
                x: acc_x,
                y: acc_y,
                z: acc_z,
            };
        Plotly.newPlot('svm', [data_boundary, data_points]);
        */
        Plotly.newPlot('svm', get_initial_data_svm(x, y, z, acc_x, acc_y, acc_z))
        var interval = create_interval_svm(acc_x, acc_y, acc_z, "counter", "svm");

        const play = document.getElementById("play_svm");
        play.onclick = function(){
            interval = create_interval_svm(acc_x, acc_y, acc_z, "counter", "svm");
        }
        const stop = document.getElementById("stop_svm");
        stop.onclick = function(){
            clearInterval_svm(interval)
            counter = 1
            Plotly.react('svm', get_initial_data_svm(x, y, z, acc_x, acc_y, acc_z))
        }

        const pause = document.getElementById("pause_svm");
        pause.onclick = function(){
            clearInterval_svm(interval)
        }
    });
}
function get_initial_data_svm(boundary_x, boundary_y, boundary_z, acc_x, acc_y, acc_z){
    var data_boundary=
        {   
            color:'rgb(100,100,100)',
            type: 'mesh3d',
            x: boundary_x,
            y: boundary_y,
            z: boundary_z,
        };
    var data_points =
        {
            type: 'scatter3d',
            mode: 'markers',
            marker: {
                color: 'rgb(0, 200, 0)',
                size: 2,
        
                opacity: 0.8
            },
            x: [acc_x[0]],
            y: [acc_y[0]],
            z: [acc_z[0]],
        };
    var data = [data_boundary, data_points]
    return data        
}
function create_interval_svm(x, y, z, count_name, div){
    var interval = setInterval(function(){
        const count = window[count_name]
        Plotly.extendTraces(div, {
            x: [[x[count]]],
            y: [[y[count]]],
            z: [[z[count]]]
        }, [1])

        window[count_name] = window[count_name] + 1
        if(window[count_name] >= x.length) clearInterval(interval);
    }, 200)
    return interval
}
function calcZ(x, y, intercept, coef0, coef1, coef2){
    return (-intercept - coef0 * x - coef1 * y) / coef2;
}
function range(size, startAt = 0, separation) {
    return [...Array(size).keys()].map(i => (i * separation) + startAt);
}

analizado = document.currentScript.getAttribute('analizado');
if(analizado){
    buildChart()
}