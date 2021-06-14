// control navbar changes
$(window).scroll(function(){
  $('nav').toggleClass('scrolled', $(this).scrollTop() > 200);
  $('.item-text').toggleClass('scrolled', $(this).scrollTop() > 200);
});

// control datepicker in checkout
$(function () {
  var date = new Date()
  date.setDate(date.getDate() + 3)
  $("#id_date").datepicker({
    format:'dd/mm/yyyy',
    startDate:date,
    daysMin: ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'],
    monthsShort: ['tammikuu', 'helmikuu', 'maaliskuu', 'huhtikuu', 'toukokuu', 'kesäkuu', 'heinäkuu', 'elokuu', 'syyskuu', 'lokakuu', 'marraskuu', 'joulukuu'],
    autoHide:true,
  });
});

// control messages
window.setTimeout(function() {
  $(".alert").fadeTo(1000, 0).slideUp(1000, function(){
    $(this).remove();
  });
}, 5000);

$(function () {
  $('[data-toggle="popover"]').popover()
})

//  control signup checkbox
function onToggle() {
 if (document.querySelector('#agree').checked) {
   document.querySelector('#regbtn').removeAttribute('disabled')
 } else {
   document.querySelector('#regbtn').setAttribute('disabled', '')
 }
}

// control delivery changes
function myFunction() {
  var x = parseInt(document.getElementById("delivery").value);
  x = parseFloat(x).toFixed(2).toString()
  if (x > 0){
    document.getElementById("delv_price").innerHTML = '+ ' + x + ' Euro';
  }else{
    document.getElementById("delv_price").innerHTML = '';
  }
}

// control product functionalty
function myFunction() {
  g = 0
  l = 0
  var x = document.getElementById("price").value;
  var y = parseInt(document.getElementById("amount").value);
  x = x.replace(',', '.')
  x = Number.parseFloat(x)
  if (document.getElementById("gluteen")){
    var g = (document.getElementById("gluteen").checked) ? 5.00 : 0
  }
  if (document.getElementById("laktoos")){
    var l = (document.getElementById("laktoos").checked) ? 5.00 : 0
  }
  if (Number.isNaN(x) == false){
    x = x + g + l
    res = parseFloat(x * y).toFixed(2)
    document.getElementById("addtocart").removeAttribute("disabled");
    document.getElementById("hinta").innerHTML = res;
  }
}
