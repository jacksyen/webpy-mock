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
  })
}
