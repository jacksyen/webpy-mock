$(document).ready(function (){


});
function submit(){
  var amount = $('#addAmount').val();
  if(amount == undefined || amount == ''){
    $('#errormsg').html('金额不能为空');
    return;
  }
  $.ajax({
    url: '/rechange/post',
    type: 'POST',
    data: {'amount': amount},
    dataType: 'json',
    success: function (result){
      if(status == undefined){
        return;
      }
      $('#errormsg').html(result.status);
      $('#curAmount').html(result.balance);
      $('#addAmount').val('');
      $('#errormsg').html('');
    }
  });
}


function itemHandler(t, operType){
  var ele = $(t.parentElement.parentElement);
  var usercode = ele.find('[usercode]').attr('usercode');
  var channelcode = ele.find('[channelcode]').attr('channelcode');
  if(usercode == undefined || usercode == ''){
    ele.find('[msg]').html('缴费号码不能为空');
    return;
  }
  if(channelcode == undefined || channelcode == ''){
    ele.find('[msg]').html('明细编号不能为空');
    return;
  }
  ele.find('[msg]').html('处理中，请稍候...');
  var url = '/rechange/change';
  if(operType == 'clear'){
    url = '/rechange/clear';
  }

  $.ajax({
    url: url,
    type: 'POST',
    data: {'usercode': usercode, 'channelcode': channelcode},
    dataType: 'json',
    success: function (result){
      var msg = '';
      msg = result.msg;
      if(result.status == 'SUCCESS'){
        responseHandler(ele, result, operType);
      }
      ele.find('[msg]').html(msg);
      ele.find('[msg]').fadeTo(5000, 0.50, function (){
        ele.find('[msg]').html('');
      });
    }
  });

  function responseHandler(ele, result, opertype){
    // 修改滞纳金
    if(opertype == 'change'){
      ele.find('[itemmoney]').html(result.itemmoney);
      ele.find('[breach]').html(result.breach);
    }
    // 清空滞纳金
    else if(opertype == 'clear'){
      ele.find('[breach]').html(result.breach);
    }
    // 修改总欠费金额、总滞纳金
    $('#info-'+usercode).find('[amount]').html(result.totalmoney);
    $('#info-'+usercode).find('[breach]').html(result.totalbreach);
  }
}

function switchStatus(t){
  var ele = $(t.parentElement.parentElement);
  var usercode = ele.find('[usercode]').attr('usercode');
  if(usercode == undefined || usercode == ''){
    ele.find('[msg]').html('缴费号码不能为空');
    return;
  }
  ele.find('[msg]').html('处理中，请稍候...');
  $.ajax({
    url: '/rechange/switch',
    type: 'POST',
    data: {'usercode': usercode},
    dataType: 'json',
    success: function (result){
      var msg = '';
      msg = result.msg;
      if(result.status == 'SUCCESS'){
        //result.busStatus
        ele.find('[status]').html(result.busStatus);
      }
      ele.find('[msg]').html(msg);
      ele.find('[msg]').fadeTo(5000, 0.50, function (){
        ele.find('[msg]').html('');
      });
    }
  });
}
