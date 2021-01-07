const report_payment = Vue.createApp({
    data () {
        return{
            stripe: '',
        }
    },
    methods: {
        report_payment() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/report_payment/",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.stripe = Stripe(result.publicKey);
                }
            })
        },

        report_checkout() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const stripe = this.stripe
            $.ajax({
                url: "/create-checkout-session/",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    return stripe.redirectToCheckout({sessionId: result.sessionId})
                },
                error: function(result){

                }
            })
        },
    },
    mounted() {
        this.report_payment()
    },
    delimiters : ['[$', '$]'],
})

report_payment.mount('#purchaseReport')