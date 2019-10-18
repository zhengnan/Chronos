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
    window.location.href = 'brddetailn.html';
}

function onBRDPageNextButtonClicked() {
	window.location.href = 'timeline.html';
}

function onBRDPagePreviousButtonClicked() {
	window.location.href = 'update.html';
}

