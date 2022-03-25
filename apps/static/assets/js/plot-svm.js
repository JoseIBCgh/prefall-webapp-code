var counter = 0;
const bow = document.currentScript.getAttribute('bow');
const fall_to_left = document.currentScript.getAttribute('fall_to_left');
const fall_to_right = document.currentScript.getAttribute('fall_to_right');
const falling_backward = document.currentScript.getAttribute('falling_backward');
const falling_forward = document.currentScript.getAttribute('falling_forward');
const idle = document.currentScript.getAttribute('idle');
const sitting = document.currentScript.getAttribute('sitting');
const sleep = document.currentScript.getAttribute('sleep');
const standing = document.currentScript.getAttribute('standing');

var probabilidades = [["Bow", parseFloat(bow)], ["Fall to left", parseFloat(fall_to_left)], ["Fall to right", parseFloat(fall_to_right)], 
["Falling backward", parseFloat(falling_backward)], ["Falling forward", parseFloat(falling_forward)], ["Idle", parseFloat(idle)], 
["Sitting", parseFloat(sitting)], ["Sleep", parseFloat(sleep)], ["Standing", parseFloat(standing)]]

function ms2Tog(x){
    return x * 0.10197162129779
}
function buildChartSVM() {

    console.log("buildChartSVM")
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
        const acc_x_test = response.acc_x_test.map(ms2Tog);
        const acc_y_test = response.acc_y_test.map(ms2Tog);
        const acc_z_test = response.acc_z_test.map(ms2Tog);
        const acc_x_train = response.acc_x_train;
        const acc_y_train = response.acc_y_train;
        const acc_z_train = response.acc_z_train;
        const class_train = response.class_train;
        console.log(intercept)
        console.log(coef0)
        console.log(coef1)
        console.log(coef2)
        console.log(class_train)
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
        data_boundaries = []
        for(let j = 0; j < intercept.length; ++j){
            let z = []
            for(let i = 0; i < x.length; i++){
                z.push(calcZ(x[i], y[i],intercept[j], coef0[j], coef1[j], coef2[j]))
            }
            let data_boundary = {
                color:'rgb(100,100,100)',
                type: 'mesh3d',
                opacity: 0.3,
                x: x,
                y: y,
                z: z,
            }
            data_boundaries.push(data_boundary);
        }
        Plotly.newPlot('svm', get_initial_data_svm(data_boundaries, acc_x_test, acc_y_test, acc_z_test))
        var interval = create_interval_svm(acc_x_test, acc_y_test, acc_z_test, "counter", "svm");

        const play = document.getElementById("play_svm");
        play.onclick = function(){
            interval = create_interval_svm(acc_x_test, acc_y_test, acc_z_test, "counter", "svm");
        }
        const stop = document.getElementById("stop_svm");
        stop.onclick = function(){
            clearInterval_svm(interval)
            counter = 1
            Plotly.react('svm', get_initial_data_svm(data_boundaries, acc_x_test, acc_y_test, acc_z_test))
        }

        const pause = document.getElementById("pause_svm");
        pause.onclick = function(){
            clearInterval_svm(interval)
        }

        probabilidades_ordenadas = JSON.parse(JSON.stringify(probabilidades)).sort((a,b) => a[1] < b[1]? 1:-1)
        
        for(let i  = 0; i < probabilidades_ordenadas.length; i++){
            index = probabilidades.findIndex((y) => y[0] === probabilidades_ordenadas[i][0])
            probabilidades_ordenadas[i].push(index)
        }
        console.log(probabilidades)
        console.log(probabilidades_ordenadas)
        var data_subplots = []
        for(let j = 0; j < probabilidades_ordenadas.length; j++){
            let index = probabilidades_ordenadas[j][2]
            let z = []
            for(let i = 0; i < x.length; i++){
                z.push(calcZ(x[i], y[i],intercept[index], coef0[index], coef1[index], coef2[index]))
            }
            let data_boundary = {
                color:'rgb(100,100,100)',
                type: 'mesh3d',
                opacity: 0.3,
                x: x,
                y: y,
                z: z,
                scene: "scene" + (j + 1).toString()
            }
            data_subplots.push(data_boundary)
            let data_points = {
                type: 'scatter3d',
                mode: 'markers',
                marker: {
                    color: 'rgb(0, 200, 0)',
                    size: 2,
            
                    opacity: 0.8
                },
                x: acc_x_test,
                y: acc_y_test,
                z: acc_z_test,
                scene: "scene" + (j + 1).toString()
            }
            data_subplots.push(data_points)
            let clase = probabilidades_ordenadas[j][0]
            let indices_class = indices(class_train, clase)
            let indices_other = indicesNot(class_train, clase)
            let acc_x_class = returnIndices(acc_x_train, indices_class)
            let acc_y_class = returnIndices(acc_y_train, indices_class)
            let acc_z_class = returnIndices(acc_z_train, indices_class)
            let acc_x_other = returnIndices(acc_x_train, indices_other)
            let acc_y_other = returnIndices(acc_y_train, indices_other)
            let acc_z_other = returnIndices(acc_z_train, indices_other)
            console.log(clase)
            let class_points = {
                type: 'scatter3d',
                mode: 'markers',
                marker: {
                    color: 'rgb(0, 0, 200)',
                    size: 2,
            
                    opacity: 0.8
                },
                x: acc_x_class,
                y: acc_y_class,
                z: acc_z_class,
                scene: "scene" + (j + 1).toString()
            }
            data_subplots.push(class_points)
            let other_points = {
                type: 'scatter3d',
                mode: 'markers',
                marker: {
                    color: 'rgb(200, 0, 0)',
                    size: 2,
            
                    opacity: 0.8
                },
                x: acc_x_other,
                y: acc_y_other,
                z: acc_z_other,
                scene: "scene" + (j + 1).toString()
            }
            data_subplots.push(other_points)
        }
        var layout = {}
        for(let i = 0; i < probabilidades_ordenadas.length; ++i){
            let subLayout = {
                domain:{
                    x:[1/3*(i%3),1/3*(i%3) + 1/3],
                    y:[1-Math.floor(i/3) / 3 - 1/3,1-Math.floor(i/3) / 3]
                }
            }
            layout["scene" + (i + 1).toString()] = subLayout
        }
        var annotations = []
        for(let i = 0; i < probabilidades_ordenadas.length; ++i){
            let annotation = {
                text: probabilidades_ordenadas[i][0] + " " + (probabilidades_ordenadas[i][1] * 100).toFixed(2),
                    font: {
                    size: 16,
                    color: 'black',
                },
                showarrow: false,
                align: 'center',
                x:1/3*(i%3),
                y:1-Math.floor(i/3) / 3,
            }
            annotations.push(annotation)
        }
        layout["annotations"] = annotations
        layout["showlegend"] = false
        var subplots_div = document.querySelector("#svm-subplots");
        subplots_div.style.height = getComputedStyle(subplots_div).width;
        Plotly.newPlot('svm-subplots', data_subplots, layout)
    });
}
function get_initial_data_svm(data_boundaries, acc_x, acc_y, acc_z){
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
    var data = data_boundaries.concat(data_points)
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
function indices(data, value){
    return data.reduce(function(arr, e, i) {
        if (e === value) arr.push(i);
        return arr;
      }, [])
}
function indicesNot(data, value){
    return data.reduce(function(arr, e, i) {
        if (e !== value) arr.push(i);
        return arr;
      }, [])
}
function returnIndices(data, indices){
    let result = []
    for(let i = 0; i< indices.length; i++){
        result.push(data[indices[i]])
    }
    return result
}

probabilidad_caida = document.currentScript.getAttribute('probabilidad_caida');
if(probabilidad_caida > 0){
    buildChartSVM()
}