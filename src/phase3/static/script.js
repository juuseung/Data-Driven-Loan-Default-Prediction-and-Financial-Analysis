var slider_roi = document.getElementById("rate_of_interest");
var output_roi = document.getElementById("rate_of_interest_value");
output_roi.innerHTML = slider_roi.value;
slider_roi.oninput = function() { output_roi.innerHTML = this.value; }

var slider_loan_amount = document.getElementById("loan_amount");
var output_loan_amount = document.getElementById("loan_amount_value");
output_loan_amount.innerHTML = slider_loan_amount.value;
slider_loan_amount.oninput = function() { output_loan_amount.innerHTML = this.value; }

var slider_irs = document.getElementById("Interest_rate_spread");
var output_irs = document.getElementById("Interest_rate_spread_value");
output_irs.innerHTML = slider_irs.value;
slider_irs.oninput = function() { output_irs.innerHTML = this.value; }

var slider_upfront = document.getElementById("Upfront_charges");
var output_upfront = document.getElementById("Upfront_charges_value");
output_upfront.innerHTML = slider_upfront.value;
slider_upfront.oninput = function() { output_upfront.innerHTML = this.value; }

var slider_term = document.getElementById("term");
var output_term = document.getElementById("term_value");
output_term.innerHTML = slider_term.value;
slider_term.oninput = function() { output_term.innerHTML = this.value; }

var slider_property_value = document.getElementById("property_value");
var output_property_value = document.getElementById("property_value");
output_property_value.innerHTML = slider_property_value.value;
slider_property_value.oninput = function() { output_property_value.innerHTML = this.value; }

var slider_tu = document.getElementById("total_units");
var output_tu = document.getElementById("total_units_value");
output_tu.innerHTML = slider_tu.value || "";
slider_tu.oninput = function() { output_tu.innerHTML = this.value; }

var slider_income = document.getElementById("income");
var output_income = document.getElementById("income_value");
output_income.innerHTML = slider_income.value;
slider_income.oninput = function() { output_income.innerHTML = this.value; }

var slider_credit_score = document.getElementById("credit_score");
var output_credit_score = document.getElementById("credit_score_value");
output_credit_score.innerHTML = slider_credit_score.value;
slider_credit_score.oninput = function() { output_credit_score.innerHTML = this.value; }

var slider_ltv = document.getElementById("ltv");
var output_ltv = document.getElementById("ltv_value");
output_ltv.innerHTML = slider_ltv.value;
slider_ltv.oninput = function() { output_ltv.innerHTML = this.value; }

var slider_dtir1 = document.getElementById("dtir1");
var output_dtir1 = document.getElementById("dtir1_value");
output_dtir1.innerHTML = slider_dtir1.value;
slider_dtir1.oninput = function() { output_dtir1.innerHTML = this.value; }

function submit() {
    const submitData = {
        'loan_limit': document.getElementById('loanlimit').value || null,
        'Gender': document.getElementById('gender').value || null,
        'approv_in_adv': document.getElementById('approv_in_adv').value || null,
        'loan_type': document.getElementById('loantype').value || null,
        'loan_purpose': document.getElementById('loanpurpose').value || null,
        'Credit_Worthiness': document.getElementById('creditworthiness').value || null,
        'open_credit': document.getElementById('opencredit').value || null,
        'business_or_commercial': document.getElementById('bussiniessorcommercial').value || null,
        // 'loan_amount': document.getElementById('loan_amount').value || null,
        // 'rate_of_interest': document.getElementById('rate_of_interest').value || null,
        // 'Interest_rate_spread': document.getElementById('Interest_rate_spread').value || null,
        // 'Upfront_charges': document.getElementById('Upfront_charges').value || null,
        // 'term': document.getElementById('term').value || null,
        'Neg_ammortization': document.getElementById('neg_amortization').value || null,
        'interest_only': document.getElementById('interestonly').value || null,
        // 'property_value': document.getElementById('property_value').value || null,
        'construction_type': document.getElementById('construction_type').value || null,
        'occupancy_type': document.getElementById('occupancy_type').value || null,
        'Secured_by': document.getElementById('secured_by').value || null,
        'total_units': document.getElementById('total_units').value || null,
        // 'income': document.getElementById('income').value || null,
        'credit_type': document.getElementById('credittype').value || null,
        // 'Credit_Score': document.getElementById('credit_score').value || null,
        'co-applicant_credit_type': document.getElementById('coappl_credittype').value || null,
        'age': document.getElementById('age').value || null,
        'submission_of_application': document.getElementById('submission_of_application').value || null,
        // 'LTV': document.getElementById('ltv').value || null,
        'Region': document.getElementById('region').value || null,
        'Security_Type': document.getElementById('security_type').value || null,
        'Status': document.getElementById('status').value === '1(loan granted)' ? [1] : [0], // This retains the boolean status conversion.
        // 'dtir1': document.getElementById('dtir1').value || null       
    };

    const sliders = document.querySelectorAll('.slider');
    
    sliders.forEach(slider => {
        const value = document.getElementById(slider.id + '_value').textContent;
        // Check if the slider value is '' and set it to null in the object
        submitData[slider.id] = value === '' ? null: parseFloat(value);
        // console.log(slider.id+":"+value+":"+submitData[slider.id]);
    });
    console.log(submitData);

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'data': submitData}),
    })
    .then(response => response.json())
    .then(data => {
        console.log('response data: ', data);
        if (data['predicted'] == 0) {
            document.getElementById('predicted').innerText  = "Predicted as Loan Default";
        } else if (data['predicted'] == 1) {
            document.getElementById('predicted').innerText  = "Predicted as non Loan Default";
        }
        // document.getElementById('predicted').innerText  = "Acutal:"+data['actual']+"Predicted:"+data['predicted'];

        const plotviewbtn_div = document.getElementById('plotviewbtn_div');
        const check_pv_button = document.getElementById('plotview_btn');
        if (!check_pv_button) {
            const plotview_btn = document.createElement('button');
            plotview_btn.id = 'plotview_btn';
            plotview_btn.textContent = 'view plot';
            plotview_btn.addEventListener('click', () => plotview());
            plotviewbtn_div.appendChild(plotview_btn);
        } else {
            check_pv_button.style.visibility = 'visible';
            document.getElementById('plot').src = '';
        }
    })
    .catch(error => console.log('Error: ', error));
}
function plotview() {
    fetch('/plot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('network response was not okay');
        }
        return response.blob();
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        document.getElementById('plot').src = url;

        const plotview_btn = document.getElementById('plotview_btn');
        plotview_btn.style.visibility = 'hidden';
    })
    .catch(error => console.log('Error: ', error));
}