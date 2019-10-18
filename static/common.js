function onBRDPageApproveButtonClicked() {
	var approver = 'Zheng, Nan';
    var data = {};
    data[approver] = 'Approved';

    $.ajax(
        {
            type: 'GET',
            url: '/approve',
            data: data,
            dataType: "json",
            success: function(data) {
            }
        }
    );
    window.location.href = 'http://0.0.0.0:5000/brddetailn.html';
}

function onBRDPageNextButtonClicked() {
	window.location.href = 'http://0.0.0.0:5000/timeline.html';
}

function onBRDPagePreviousButtonClicked() {
	window.location.href = 'http://0.0.0.0:5000/update.html';
}

