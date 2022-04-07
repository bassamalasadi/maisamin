// control navbar changes
$(window).scroll(function(){
  if ($(this).width() > 960){
    $('.main-nav').toggleClass('scrolled', $(this).scrollTop() > 200);
    $('.sec-nav').toggleClass('scrolled', $(this).scrollTop()> 100);
    $('.item-text').toggleClass('scrolled', $(this).scrollTop() > 200);
    if ($(this).scrollTop() > 200){
      $('.brand-img-1').removeAttr('hidden').show(2000);
      $('.brand-img-2').attr('hidden', '')
    }else{
      $('.brand-img-2').removeAttr('hidden').show(2000);
      $('.brand-img-1').attr('hidden', '')
    }
  }
});

setTimeout(
    function(){
      if (window.innerWidth < 906 ){
        if(document.getElementById('brand-img-1') && document.getElementById('brand-img-2')){
          document.getElementById('brand-img-1').removeAttribute("hidden")
          document.getElementById('brand-img-2').setAttribute("hidden", "")
        }
      }
    }, 300
)
// control datepicker in checkout
$(function () {
  let date = new Date()
  let endDate = new Date()
  date.setDate(date.getDate() + 3)
  endDate.setDate(endDate.getDate() + 90)
  $("#id_date").datepicker({
    format:'dd/mm/yyyy',
    startDate:date,
    endDate:endDate,
    daysMin: ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'],
    monthsShort: ['tammikuu', 'helmikuu', 'maaliskuu', 'huhtikuu', 'toukokuu', 'kesäkuu', 'heinäkuu', 'elokuu', 'syyskuu', 'lokakuu', 'marraskuu', 'joulukuu'],
    autoHide:true,
  });
  let newdate = $("#id_date").datepicker('getDate')
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

function deliverySend(){
  if ($('#agree_delivery').is(':checked')){
    $('#send-order').removeAttr('disabled')
  } else {
    $('#send-order').attr('disabled', '')
  }
}

// control delivery changes
function delivery_func() {
  let x = parseInt(document.querySelector("#delivery").value);
  x = parseFloat(x).toFixed(2).toString()
  if (x > 0){
    document.querySelector("#delv_price").innerHTML = '+ ' + x + ' Euro';
    $('#delivery-policy').removeAttr('hidden')
    $('#delivery_address').removeAttr('disabled')
    $('#delivery_address').removeAttr('hidden')
    $('#send-order').attr('disabled', '')
  }else{
    document.querySelector("#delv_price").innerHTML = '';
    $('#delivery-policy').attr('hidden', '')
    $('#delivery_address').attr('hidden', '')
    $('#delivery_address').attr('disabled', '')
    $('#send-order').removeAttr('disabled')

  }
}

// control product functionalty
function myFunction() {
  g = 0
  l = 0
  let x = document.getElementById("price").value;
  let y = parseInt(document.getElementById("amount").value);
  x = x.replace(',', '.')
  x = Number.parseFloat(x)
  if (document.getElementById("gluteen")){
    g = (document.getElementById("gluteen").checked) ? 9 : 0
  }
  if (document.getElementById("laktoos")){
    l = (document.getElementById("laktoos").checked) ? 5 : 0
  }
  if (Number.isNaN(x) == false){
    x = x + g + l
    res = parseFloat(x * y).toFixed(2)
    res = res.replace('.', ',')
    document.getElementById("addtocart").removeAttribute("disabled");
    document.getElementById("gluteen-field").removeAttribute("hidden");
    document.getElementById("amount-field").removeAttribute("hidden");
    document.getElementById("hinta").innerHTML = res;
  }
}

// contorl delete account
$(document).ready(function () {
  $('#deleteaccount').change(function () {
      if ($('#deleteaccount').val() === 'poista'){
        $('#deleteaccount').fadeOut(1000)
      }
  });
});

// new update for delete, increment, and decrement buttons
function increment(id){
  let totalPrice = document.getElementById('totalPrice').innerHTML;
  $('table > tbody  > tr').each(function(index, tr) {
    let trNumber = parseInt(tr.id)
    if (trNumber === id){
      apiUrl(`/increment/${id}/`)

      quantity = $($(tr).find('td')[2]).find('span')[0].id
      quantity = parseInt(quantity) + 1
      $($(tr).find('td')[2]).find('span')[0].id = quantity
      $($($(tr).find('td')[2]).find('span')[0]).html(quantity)

      itemPrice = $(tr).find('td')[1].id
      itemPrice = itemPrice.replace(',', '.')
      itemTotalPrice = $(tr).find('td')[3].id
      totalItemPrice = (parseFloat(itemTotalPrice) + parseFloat(itemPrice)).toFixed(2)
      totalItemPrice = totalItemPrice.concat(' €')
      $(tr).find('td')[3].id = totalItemPrice
      $($(tr).find('td')[3]).html(totalItemPrice)

      totalPrice = (parseFloat(totalPrice) + parseFloat(itemPrice)).toFixed(2)
      document.getElementById('totalPrice').innerHTML = totalPrice
    }
})
}
function decrement(id){
  let totalPrice = document.getElementById('totalPrice').innerHTML;
  $('table > tbody  > tr').each(function(index, tr) {
    let trNumber = parseInt(tr.id)
    if (trNumber === id){
      apiUrl(`/decrement/${id}`)
      quantity = $($(tr).find('td')[2]).find('span')[0].id
      quantity = parseInt(quantity) - 1
      $($(tr).find('td')[2]).find('span')[0].id = quantity
      $($($(tr).find('td')[2]).find('span')[0]).html(quantity)

      itemPrice = $(tr).find('td')[1].id
      itemPrice = itemPrice.replace(',', '.')
      itemTotalPrice = $(tr).find('td')[3].id
      totalItemPrice = (parseFloat(itemTotalPrice) - parseFloat(itemPrice)).toFixed(2)
      totalItemPrice = totalItemPrice.concat(' €')
      $(tr).find('td')[3].id = totalItemPrice
      $($(tr).find('td')[3]).html(totalItemPrice)

      totalPrice = (parseFloat(totalPrice) - parseFloat(itemPrice)).toFixed(2)
      document.getElementById('totalPrice').innerHTML = totalPrice
      if (quantity <= 0){
        deleteFunc(id)
        $(tr).remove();
        navCount = parseInt(document.getElementById("cart-count").innerHTML) - 1
        document.getElementById("cart-count").innerHTML = navCount
        if (navCount <= 0){
          $("#cart-row").fadeOut(1000)
        }
      }
    }
  })
}
function deleteFunc(item){
  let totalPrice = Number.parseFloat(document.getElementById('totalPrice').innerHTML).toFixed(2);
  $('table > tbody  > tr').each(function(index, tr) {
    let trNumber = parseInt(tr.id)
    if (trNumber === item){
      itemPrice = parseFloat($(tr).find('td')[3].id).toFixed(2)
      totalPrice = (totalPrice - itemPrice).toFixed(2).toString()
      navCount = parseInt(document.getElementById("cart-count").innerHTML) - 1
      document.getElementById('totalPrice').value = totalPrice
      document.getElementById('totalPrice').innerHTML = totalPrice
      document.getElementById("cart-count").innerHTML = navCount
      if (navCount === 0){
        $("#cart-row").fadeOut(1000)
      }
      apiUrl(`/delete/${item}`);
      $(tr).remove();
    }
  });
}
function apiUrl(item){
  let endpoint = item
    $.ajax({
        method: 'GET',
        url: endpoint,
        success: function (data) {},
        error: function (error_data) {
        }
    })
}


// let endpoint = $(".comfirm-delete").attr('data-url')
//         $.ajax({
//             method: 'GET',
//             url: endpoint,
//             success: function (data) {
//                 $.notify({
//                     title: '<b>Message<b> ',
//                     message: data.message,
//                 }, {
//                     type: 'success',
//                     delay: 3000,
//                     allow_dismiss: true,
//
//                 });
//             },
//             error: function (error_data) {
//                 console.log(error_data);
//                 $.notify({
//         title: '<b>Error</b><br>',
//         message: 'Anteeksi, jotain meni pieleen'
//     }, {
//         type: 'danger',
//         delay: 3000,
//     })
//             }
//         })
