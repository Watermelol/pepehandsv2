const after_payment = Vue.createApp({
    data() {
        return {
            seconds: 5,
        }
    },

    methods: {
        redirect_to_dashboard () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            window.setInterval(function(){
                data.seconds--
                if (data.seconds === 0){
                    clearInterval() 
                    window.location = '/dashboard/'
                }
              }, 1000);
        }
    },

    mounted() {
        this.redirect_to_dashboard()
    },
    delimiters : ['[$', '$]'],
})

after_payment.mount('#after_payment_page')