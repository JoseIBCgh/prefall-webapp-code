num_test = document.currentScript.getAttribute('num_test');
id_paciente = document.currentScript.getAttribute('paciente');
console.log(num_test)
function ms2Tog(x){
    return x * 0.10197162129779
}
function start_prediction() {
    console.log("start_prediction")
    // send ajax POST request to start background job
    var url = `/test_data/`+id_paciente+`/`+num_test;
    d3.json(url).then(function(response) {
        const acc_x = response.acc_x.map(ms2Tog);
        const acc_y = response.acc_y.map(ms2Tog);
        const acc_z = response.acc_z.map(ms2Tog);
        $.ajax({
            type: 'POST',
            url: 'http://0.0.0.0:8000/predict',
            data: JSON.stringify({"acc_x": acc_x, "acc_y":acc_y, "acc_z":acc_z}),
            success: function(data, status, request) {
                task_id = data.task_id
                console.log(task_id)
                poll(task_id)
            },
            error: function() {
                console.log("error")
                alert('Unexpected error');
            }
        });
    });
}
function poll(task_id){
    console.log("poll")
    $.getJSON('http://0.0.0.0:8000/tasks/<task_id>?task_id=' + task_id, function(data) {
        if(data['task_status'] == 'SUCCESS'){
            console.log("SUCCESS")
            $.ajax({
                type: 'POST',
                url: '/guardar_analisis/'+num_test+'/'+id_paciente,
                data: JSON.stringify({"result": data.task_result}),
                contentType: 'application/json;charset=UTF-8',
                success: function(data, status, request) {
                    window.location.reload();
                },
                error: function() {
                    alert('Unexpected error');
                }
            });
        }
        else if(data['task_status'] == 'FAILURE' || data['tast_status'] == 'REVOKED'){
            alert('Prediction error')
        }
        else {
            setTimeout(function() {
                poll(task_id);
            }, 1000);
        }
    });
}