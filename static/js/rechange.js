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

function submit2(t){
  var ele = $(t.parentElement.parentElement);
  var usercode = ele.find('[usercode]').attr('usercode');
  if(usercode == undefined || usercode == ''){
    ele.find('[msg]').html('缴费号码不能为空');
    return;
  }
  ele.find('[msg]').html('处理中，请稍候...');
  $.ajax({
    url: '/rechange/change',
    type: 'POST',
    data: {'usercode': usercode},
    dataType: 'json',
    success: function (result){
      var msg = '';
      msg = result.msg;
      if(result.status == 'SUCCESS'){
        ele.find('[amount]').html(result.balance);
      }
      ele.find('[msg]').html(msg);
      ele.find('[msg]').fadeTo(5000, 0.50, function (){
        ele.find('[msg]').html('');
      });
    }
  });
}
