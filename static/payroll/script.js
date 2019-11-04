function getCurrentEarningAmount(url, data) {
    let response;
    console.log("getting stuff");
    $.ajax({
        url: url,
        data: data,
        success: function (data) {
            response = data['amount'];
        }
    });
    return response;
}