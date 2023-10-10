num_test = document.currentScript.getAttribute('num_test');
id_paciente = document.currentScript.getAttribute('paciente');
console.log(num_test)
function ms2Tog(x){
    return x * 0.10197162129779
}
function start_prediction() {
    localStorage.setItem("startTimeAnalize", Date.now());
    console.log("start_prediction")
    // Send AJAX GET request to get the CSV data
    var url = `/get_test/${id_paciente}/${num_test}`;
    $.get(url, function(csvData) {
        // Create a new Blob with the CSV content
        var blob = new Blob([csvData], { type: "text/csv" });

        // Create a FormData object and append the Blob as a file
        var formData = new FormData();
        formData.append("csv_file", blob, "test.csv");

        // Send the AJAX POST request
        $.ajax({
            type: 'POST',
            url: 'http://srv.ibc.bio:32840/predict',
            //url: 'http://localhost:8000/predict',
            data: formData,
            contentType: false, // Set to false to prevent jQuery from adding a content-type header
            processData: false, // Set to false to prevent jQuery from processing the data
            success: function(data, status, request) {
                task_id = data.task_id;
                console.log(task_id);
                poll(task_id);
            },
            error: function() {
                console.log("error");
                alert('Unexpected error');
            }
        });
    });
    alert("Analizando test");
}
function poll(task_id){
    console.log("poll")
    $.getJSON('http://srv.ibc.bio:32840/tasks/<task_id>?task_id=' + task_id, function(data) {
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