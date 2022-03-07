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
        var data = [acc_x_data, acc_y_data, acc_z_data];
        var layout = {
            title: "Acelerometro",
            xaxis:{title:"item"},
            yaxis:{title:"m/s^2"},
        };
        Plotly.newPlot('acc', data, layout, {responsive: true});

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
        var data = [gyr_x_data, gyr_y_data, gyr_z_data];
        var layout = {
            title: "Giroscopio",
            xaxis:{title:"item"},
            yaxis:{title:"deg/s"},
        };
        Plotly.newPlot('gyr', data, layout, {responsive: true});

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
        var data = [mag_x_data, mag_y_data, mag_z_data];
        var layout = {
            title: "Magnetometro",
            xaxis:{title:"item"},
            yaxis:{title:"Tesla"},
        };
        Plotly.newPlot('mag', data, layout, {responsive: true});
    });
}
buildChart()