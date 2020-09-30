//Step - 1
document.addEventListener("DOMContentLoaded", function(){
    let button = document.querySelector("#first-step");
    let checkBoxes = document.querySelectorAll("input[type=checkbox][name=category]")
    for (let i=0;i<checkBoxes.length;i++) {
        checkBoxes[i].checked = false;
        checkBoxes[i].classList.remove('selected')
    }
    button.disabled = true
    for (let i=0;i<checkBoxes.length;i++) {
        checkBoxes[i].addEventListener("click", function(){
            checkBoxes[i].classList.toggle('selected');
            let selected = document.querySelectorAll('input[type=checkbox][name=category]:checked')
            if (selected.length <1 ) {
                button.disabled = true
            } else {
                button.disabled = false
            }      
        });
    }
});


//Step - 2
document.addEventListener("DOMContentLoaded", function(){
    let quantity = document.querySelector('input#id_quantity');
    let step2button = document.querySelector('#second-step');
    //let value = Number.parseInt(quantity.value, 10)
    quantity.addEventListener('change', function() {
        if (quantity.value < 1 || quantity.value > 100 || quantity.value % 1 !== 0) {
            step2button.disabled = true
            //document.getElementById('quantity-help-text').innerHTML = "Ilość worków nie może byc mniejsza od 1 lub większą od 100"
        } else {
            step2button.disabled = false
        }
    });
});

//Step - 3
document.addEventListener("DOMContentLoaded", function(){
    let step3button = document.querySelector('#third-step')
    step3button.disabled = true
    let ajax = document.querySelector("#ajax");
    ajax.addEventListener("click", function(){
        step3button.disabled = false;
        });    
});

//Step - 4 thank you kind people on internet :) 
document.addEventListener("DOMContentLoaded", function() {
    let lastbutton = document.getElementById("summary-step");
    lastbutton.disabled = true
    let form = document.getElementById("pickup-info")
    form.addEventListener('change', function(){
        let allAreFilled = true;
        document.getElementById("pickup-info").querySelectorAll("[required]").forEach(function(i) {
            if (!allAreFilled) return;
            if (!i.value) allAreFilled = false
            });
        if (!allAreFilled) {
            lastbutton.disabled = true
        } else {
            lastbutton.disabled = false
            }
         });
    });


//step - 5 summary
document.addEventListener("DOMContentLoaded", function() {
    let lastStep = document.getElementById('summary-step');
    lastStep.addEventListener('click', function (){
        
        let quantity = document.getElementById('id_quantity').value;
        let address = document.getElementById('id_address').value;
        let city = document.getElementById('id_city').value;
        let zip_code = document.getElementById('id_zip_code').value;
        let phone = document.getElementById('id_phone_number').value;
        let date = document.getElementById('id_pick_up_date_time_0').value;
        let time = document.getElementById('id_pick_up_date_time_1').value;
        let comment = document.getElementById('id_pick_up_comment').value;
        let selected = document.querySelector("input[name='organization']:checked");
        let org = selected.getAttribute('data-desc')
        let categories = document.querySelectorAll('input[type=checkbox][name=category]:checked');
        let cats = ''
        for (let i=0;i<categories.length;i++) {
            cats = cats + categories[i].getAttribute('data-category') + ' '
        }


        document.getElementById('summarybox1').innerHTML = 'Worki do przekazania: '+ quantity +' w kat.:' + cats
        document.getElementById('summarybox2').innerText = "Dla " + org;
        document.getElementById('address').innerHTML = address
        document.getElementById('city').innerHTML = city
        document.getElementById('zip').innerHTML = zip_code
        document.getElementById('phone').innerHTML = phone
        document.getElementById('date').innerHTML = date
        document.getElementById('time').innerHTML = time
        document.getElementById('comments').innerHTML = comment
    })
});
