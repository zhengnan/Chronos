function hello() {
    var data = {
        'section1': 'section1'
    }
    $.ajax(
        {
            type: 'GET',
            url: '/hello',
            data: data,
            dataType: "json",
            success: function(data) {
            }
        }
    );
    window.location.href = 'http://127.0.0.1:5000/timeline.html';
}
