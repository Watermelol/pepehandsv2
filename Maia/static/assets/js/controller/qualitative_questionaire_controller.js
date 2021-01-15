const qualitative_data = Vue.createApp({
    data() {
        return {
            pageNumber: 1
        }
    },
    methods: {
        nextPage () {
            this.pageNumber++
        },

        previousPage() {
            this.pageNumber--
        },

        checkNumber(event) {
            if (event.key > 5){
                event.key = '5'
                console.log(event)
            }else if (event.key < 1){
                event.key = '1'
            }
        },

        submitAnswer() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                url: "/qualitative_questionaire/",
                headers:  {'X-CSRFToken': csrftoken},
                contentType: "application/json; charset=utf-8",
                data: 'Hi',
                type: 'POST',
                success: function(result) {
                    if (result == 'data saved'){
                        window.location = '/dashboard/'
                    }
                }
            })
        },

        answerValidation (answer) {
            if (answer > 5){
                answer = 5
            }else if (answer < 1){
                answer = 1
            }
        }

    },
})

qualitative_data.mount('#qualitative_data')