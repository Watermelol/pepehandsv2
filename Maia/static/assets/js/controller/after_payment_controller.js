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
                
                if (data.seconds === 0){
                    clearInterval() 
                    window.location = '/dashboard/'
                }else{
                    data.seconds--
                }
              }, 1000);
        },

        openPDF() {
            const fileName = document.querySelector('[name=pdfLink]').value;
            console.log(fileName)
            console.log('https://storage.googleapis.com/maia_report_1/pdf/' + fileName)
            window.open('https://storage.googleapis.com/maia_report_1/pdf/' + fileName, '_blank')
        }
    },

    mounted() {
        this.redirect_to_dashboard()
        this.openPDF()
    },
    delimiters : ['[$', '$]'],
})

after_payment.mount('#after_payment_page')