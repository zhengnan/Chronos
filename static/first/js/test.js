function show() {
	var feeTypes = {
		"StorageBilling": {
			"SODR": {
				"sortable": ["true", "false"],
				"hazmat": ["true", "false"]
			}
		},
		"FBAOverageFee": {
			"SODR": {
				"panEU": ["true", "false"]
			}
		}
	};

	$.each(feeTypes, function(feeTypeName, value ) {
   		var select_option = "<option value='" + feeTypeName + "'>" + feeTypeName + "</option>";
   		$('#fee_type').append(select_option);
	});

	$('#fee_type').change(function() {
        $('#fee_specific_sodr').empty();
        $('#all_fee_sodr').empty();
        var feeTypeName = $('#fee_type').val();

        $.each(feeTypes[feeTypeName].SODR, function(datakeyName, value ) {
	   		var select_option = "<option value='" + datakeyName + "'>" + datakeyName + "</option>";
	   		$('#fee_specific_sodr').append(select_option);
		});
		$.each(feeTypes, function(feeTypeName, feeTypeVal ){
              var selectedFeeTypeName = $('#fee_type').val();
              if(selectedFeeTypeName != feeTypeName) {
                $.each(feeTypeVal.SODR, function(datakeyName, value ) {
                  var select_option = "<option value='" + datakeyName + "'>" + datakeyName + "</option>";
                  $('#all_fee_sodr').append(select_option);
                });
            }
        });
    });

//    $.each(feeTypes, function(feeTypeName, feeTypeVal ) {
//    	$.each(feeTypeVal.SODR, function(datakeyName, value ) {
//	   		var select_option = "<option value='" + datakeyName + "'>" + datakeyName + "</option>";
//	   		$('#all_fee_sodr').append(select_option);
//		});
//	});

	$('#generate-rate-table').click(function(){
	        $('#rate_table').empty();
    		var fee_specific_sodrs = $('#fee_specific_sodr').val();
    		var all_fee_sodrs = $('#all_fee_sodr').val();

    		var sodrs;
            if(fee_specific_sodrs != null && all_fee_sodrs != null) {
                sodrs = fee_specific_sodrs.concat(all_fee_sodrs);
            } else if(fee_specific_sodrs != null) {
                sodrs = fee_specific_sodrs;
            } else if(all_fee_sodrs != null) {
                sodrs = all_fee_sodrs;
            }

    		var sodrObjs = [];

    		$.each(feeTypes, function(feeTypeName, feeTypeValue ) {
    	   		$.each(feeTypeValue.SODR, function(datakeyName, datakeyValue ) {
    		   		$.each(sodrs, function(index, sodrName ) {
    			   		if(datakeyName == sodrName) {
    						sodrObjs.push(datakeyValue);
    			   		}
    				});
    			});
    		});

    		var rates = cartesianProduct(sodrObjs);

    		var rate_title = "<tr class='title'>"
    		$.each(sodrs, function(index, sodrName ) {
    	   		rate_title = rate_title + "<th>" + sodrName + "</th>"
    		});
    		rate_title = rate_title + "<th>rate</th>" + "</tr>"

    		$('#rate_table').append(rate_title);

    		$.each(rates, function(index, row ) {
    			var rate_row = "<tr class='item'>"
    	   		$.each(row, function(index, value ) {
    		   		rate_row = rate_row + "<td class='" + sodrs[index] + "'>" + value + "</td>"
    			});
    			rate_row = rate_row + '<td><input type="text" class="rateNum"/></td>';
    			rate_row = rate_row + "</tr>"
    			$('#rate_table').append(rate_row);
    		});
        });

    function cartesianProduct(arr) {
	    return arr.reduce(function(a,b){
	        return a.map(function(x){
	            return b.map(function(y){
	                return x.concat(y);
	            })
	        }).reduce(function(a,b){ return a.concat(b) },[])
	    }, [[]])
	}

	$('#generate-profitability_text').click(function(){
		  var max = 100000;
		  var min = 100;
          parseInt(Math.random()*(max-min+1)+min,10);
          var res1 = Math.floor(Math.random()*(max-min+1)+min);
          var res2 = Math.floor(Math.random()*(max-min+1)+min);
          var res3 = Math.floor(Math.random()*(max-min+1)+min);
          $('#profitability_text_1').val(res1);
          $('#profitability_text_2').val(res2);
          $('#profitability_text_3').val(res3);
    });


	$('#generate-eta_text').click(function(){
     $('#div_eta_table').empty();
     var myDate = new Date();

     var startTime = dateFormat(myDate);
     var endTime = document.getElementById('eta_time_box').value;
     var split_Time = splitTime(startTime,endTime,4);
     var rowdata = ["Validation Reguriment", "Development", "Test", "Deployment"];

     var div1=document.getElementById('div_eta_table')
     var tab='<table id="eta_table" border=1 width=500">'
     for(var i=0;i<4;i++){
         var nextTime = dateFormat(split_Time[i]);
         tab+='<tr>'
         tab+="<td>"+ rowdata[i] +"</td><td><input type='text' value=' "+nextTime+ " '></input></td>"
         tab+='</tr>'
     }
     tab+='</table>';
     div1.innerHTML=tab;
    });

    $('#send_approve').click(function(){
        var obj = document.getElementById("fee_type");
        var index = obj.selectedIndex;
        var feetype = obj.options[index].text;

        var fee_specific_sodrs = $('#fee_specific_sodr').val();
        var all_fee_sodrs = $('#all_fee_sodr').val();
        var change_desc = $('#change_desc_text').val();
        var profitability = $('#profitability_text_1').val();
        var profitability1 = $('#profitability_text_2').val();
        var profitability2 = $('#profitability_text_3').val();
        var endTime = document.getElementById('eta_time_box').value;

        var rate_json = getActualRate();
        var eta_json = getEtaJson();

        var total_json = {};
        var rate_title = getrateTitle();
        total_json.rate=rate_json;
        total_json.rateTitle = rate_title;
        total_json.feeType=feetype;
        total_json.datakey=fee_specific_sodrs;
        total_json.datakeyall=all_fee_sodrs;
        total_json.changeDesc=change_desc;
        total_json.profitability=profitability;
        total_json.eta=eta_json;
        total_json.etaTime=endTime;
        total_json.profitability1=profitability1;
        total_json.profitability2=profitability2;

        console.log(JSON.stringify(total_json));
        var subject = '[] ' + feetype + " Creation";
//        sendMail(subject);
        $.ajax({
           url: '/first',
           type: 'GET',
           dataType: 'json',
           data: JSON.stringify(total_json),
           success: function (data) {

         }
       });
 window.location.href = 'http://127.0.0.1:5000/brddetailp.html';

    });

    function splitTime(startDate,endDate,amount){
	var
		startTime=new Date(startDate+" 00:00:00"),
		endTime=new Date(endDate+" 23:59:59"),
		gap=(endTime-startTime)/amount
	;
	var temp=[];
	for(var i=0;i<amount;i++){
		startTime.setMilliseconds(startTime.getMilliseconds()+gap);
		temp[i]=new Date(startTime.getTime());
	}
	return temp;
    }

    function dateFormat(myDate){
         var myYear = myDate.getFullYear();
         var myMonth = myDate.getMonth() +1; // 获取当前月份
         var myDay = myDate.getDate() // 获取当前日（1- 31）
         var startTime = myYear+'-'+myMonth+'-'+myDay;
         return startTime;
    }

    function getActualRate(){

        var actual_rates = [];

        $("#rate_table tr.item").each(function() {
            var actual_rate = [];
            $.each(this.cells, function() {
                $this = $(this);
                //alert($this.html());
                //alert($this.find("input").val());
                if($this.find("input").length) {
                    actual_rate.push($this.find("input").val());
                    //alert($this.find("input").val());
                } else {
                    actual_rate.push($this.html());
                    //alert($this.html());
                }
            });
            actual_rates.push(actual_rate);
        });

        return JSON.stringify(actual_rates);
    };

        function getrateTitle(){

            var actual_rates = [];

            $("#rate_table tr.title").each(function() {
                var actual_rate = [];
                $.each(this.cells, function() {
                    $this = $(this);
                    //alert($this.html());
                    //alert($this.find("input").val());
                    if($this.find("input").length) {
                        actual_rate.push($this.find("input").val());
                        //alert($this.find("input").val());
                    } else {
                        actual_rate.push($this.html());
                        //alert($this.html());
                    }
                });
                actual_rates.push(actual_rate);
            });

            return JSON.stringify(actual_rates);
        };

    function getEtaJson(){
    var eta_arrays=[];
    var tableObj = document.getElementById("eta_table");
    for (var i = 0; i < tableObj.rows.length; i++) {
        var eta_item
        var step = tableObj.rows[i].cells[0].innerText;
        var eta = tableObj.rows[i].cells[1].getElementsByTagName("input")[0].value;
        eta_arrays.push({"step":step,"eta":eta});
    }
    return JSON.stringify(eta_arrays);

    };


//    function sendMail(subject, message){
//	var subject = "[IR2] Request to approve a fee program launch request";
//	var message = "Hi Nan,
//	There is an program launch approval request pending your approval.
//	Please review it at this page and give your opnion at: http://127.0.0.1:5000/brddetailn.html
//
//	Thanks,
//	Fee Program Launcher Website
//	";
//
//
//    var data_js = {
//        // send to nanzhen@amazon.com
//        "access_token": "3cbfz3355dtxvqcek519lbvn"
//        // // send to wenfenz@amazon.com:
//        // "access_token": "pxj48f5s4o4crtmd0r13oaxi",
//    };
//    data_js['subject'] = subject;
//    data_js['text'] = message;
//
//    var params = toParams(data_js);
//
//    var request = new XMLHttpRequest();
//    /*
//    request.onreadystatechange = function() {
//        if (request.readyState == 4 && request.status == 200) {
//            // window.location = window.location.pathname + "?message=Email+Successfully+Sent%21&isError=0";
//        } else if(request.readyState == 4) {
//            // window.location = window.location.pathname + "?message=Email+could+not+be+sent.&isError=1";
//        }
//    };
//    */
//    request.open("POST", "https://postmail.invotes.com/send", true);
//    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//
//    request.send(params);
//}
//
//    function toParams(data_js) {
//        var form_data = [];
//        for ( var key in data_js ) {
//            form_data.push(encodeURIComponent(key) + "=" + encodeURIComponent(data_js[key]));
//        }
//
//        return form_data.join("&");
//    }
}