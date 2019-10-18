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

function sendMail(subject, message){
    var data_js = {};
    data_js['from'] = 'wenfenz@amazon.com';
    data_js['to'] = 'nanzhen@amazon.com';
    data_js['subject'] = subject;
    data_js['text'] = message;

    var params = toParams(data_js);

    var request = new XMLHttpRequest();
    request.open("GET", "sendmail.html?" + params, true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    request.send(params);
}


function onBRDPageNextButtonClicked() {
	var subject = '[chronos] NOTICE - Hi Dev, your task started just now';
	var content = 'See timeline details at http://dev-dsk-nanzhen-2b-443e6702.us-west-2.amazon.com:5000/devtimeline.html';
	sendMail(subject, content);

	window.location.href = 'timeline.html';
}

function onBRDPagePreviousButtonClicked() {
	window.location.href = 'update.html';
}

