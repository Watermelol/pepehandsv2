const qualitative_data = Vue.createApp({
    data() {
        return {
            pageNumber: 1,
            Set1Q1:1, 
            Set1Q2:1, 
            Set1Q3:1, 
            Set1Q4:1, 
            Set1Q5:1, 
            Set2Q1:1, 
            Set2Q2:1, 
            Set2Q3:1, 
            Set2Q4:1, 
            Set2Q5:1, 
            Set3Q1:1, 
            Set3Q2:1, 
            Set3Q3:1, 
            Set3Q4:1, 
            Set3Q5:1, 
            Set4Q1:1, 
            Set4Q2:1, 
            Set4Q3:1, 
            Set4Q4:1, 
            Set4Q5:1, 
            Set5Q1:1, 
            Set5Q2:1, 
            Set5Q3:1, 
            Set5Q4:1, 
            Set5Q5:1, 
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
            this.showGlobalLoader()
            var result = {
                'set1': [this.Set1Q1, this.Set1Q2, this.Set1Q3, this.Set1Q4, this.Set1Q5],
                'set2': [this.Set2Q1, this.Set2Q2, this.Set2Q3, this.Set2Q4, this.Set2Q5],
                'set3': [this.Set3Q1, this.Set3Q2, this.Set3Q3, this.Set3Q4, this.Set3Q5],
                'set4': [this.Set4Q1, this.Set4Q2, this.Set4Q3, this.Set4Q4, this.Set4Q5],
                'set5': [this.Set5Q1, this.Set5Q2, this.Set5Q3, this.Set5Q4, this.Set5Q5],
                'internalisation': (parseInt(this.Set1Q1) + parseInt(this.Set1Q2) + parseInt(this.Set1Q3) + parseInt(this.Set1Q4) + parseInt(this.Set1Q5)),
                'investment': (parseInt(this.Set2Q1) + parseInt(this.Set2Q2) + parseInt(this.Set2Q3) + parseInt(this.Set2Q4) + parseInt(this.Set2Q5)),
                'innovation': (parseInt(this.Set3Q1) + parseInt(this.Set3Q2) + parseInt(this.Set3Q3) + parseInt(this.Set3Q4) + parseInt(this.Set3Q5)),
                'integration': (parseInt(this.Set4Q1) + parseInt(this.Set4Q2) + parseInt(this.Set4Q3) + parseInt(this.Set4Q4) + parseInt(this.Set4Q5)),
                'internationalisation': (parseInt(this.Set5Q1) + parseInt(this.Set5Q2) + parseInt(this.Set5Q3) + parseInt(this.Set5Q4) + parseInt(this.Set5Q5)),
            }
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                url: "/qualitative_questionaire/",
                headers:  {'X-CSRFToken': csrftoken},
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(result),
                type: 'POST',
                success: function(result) {
                    if (result == 'data saved'){
                        window.location = '/dashboard/'
                    }
                }
            })
        },

        showGlobalLoader() {
            $('#globalLoader').modal('show')
        },

        hideGlobalLoader() {
            $('#globalLoader').modal('hide')
        },

    },
    watch: {
        Set1Q1: function (val){
            if (val > 5){
                this.Set1Q1 = 5
            }else if (val < 1){
                this.Set1Q1 = 1
            }
        },
        Set1Q2: function (val){
            if (val > 5){
                this.Set1Q2 = 5
            }else if (val < 1){
                this.Set1Q2 = 1
            }
        },
        Set1Q3: function (val){
            if (val > 5){
                this.Set1Q3 = 5
            }else if (val < 1){
                this.Set1Q3 = 1
            }
        },
        Set1Q4: function (val){
            if (val > 5){
                this.Set1Q4 = 5
            }else if (val < 1){
                this.Set1Q4 = 1
            }
        },
        Set1Q5: function (val){
            if (val > 5){
                this.Set1Q5 = 5
            }else if (val < 1){
                this.Set1Q5 = 1
            }
        },
        Set2Q1: function (val){
            if (val > 5){
                this.Set2Q1 = 5
            }else if (val < 1){
                this.Set2Q1 = 1
            }
        },
        Set2Q2: function (val){
            if (val > 5){
                this.Set2Q2 = 5
            }else if (val < 1){
                this.Set2Q2 = 1
            }
        },
        Set2Q3: function (val){
            if (val > 5){
                this.Set2Q3 = 5
            }else if (val < 1){
                this.Set2Q3 = 1
            }
        },
        Set2Q4: function (val){
            if (val > 5){
                this.Set2Q4 = 5
            }else if (val < 1){
                this.Set2Q4 = 1
            }
        },
        Set2Q5: function (val){
            if (val > 5){
                this.Set2Q5 = 5
            }else if (val < 1){
                this.Set2Q5 = 1
            }
        },
        Set3Q1: function (val){
            if (val > 5){
                this.Set3Q1 = 5
            }else if (val < 1){
                this.Set3Q1 = 1
            }
        },
        Set3Q2: function (val){
            if (val > 5){
                this.Set3Q2 = 5
            }else if (val < 1){
                this.Set3Q2 = 1
            }
        },
        Set3Q3: function (val){
            if (val > 5){
                this.Set3Q3 = 5
            }else if (val < 1){
                this.Set3Q3 = 1
            }
        },
        Set3Q4: function (val){
            if (val > 5){
                this.Set3Q4 = 5
            }else if (val < 1){
                this.Set3Q4 = 1
            }
        },
        Set3Q5: function (val){
            if (val > 5){
                this.Set3Q5 = 5
            }else if (val < 1){
                this.Set3Q5 = 1
            }
        },
        Set4Q1: function (val){
            if (val > 5){
                this.Set4Q1 = 5
            }else if (val < 1){
                this.Set4Q1 = 1
            }
        },
        Set4Q2: function (val){
            if (val > 5){
                this.Set4Q2 = 5
            }else if (val < 1){
                this.Set4Q2 = 1
            }
        },
        Set4Q3: function (val){
            if (val > 5){
                this.Set4Q3 = 5
            }else if (val < 1){
                this.Set4Q3 = 1
            }
        },
        Set4Q4: function (val){
            if (val > 5){
                this.Set4Q4 = 5
            }else if (val < 1){
                this.Set4Q4 = 1
            }
        },
        Set4Q5: function (val){
            if (val > 5){
                this.Set4Q5 = 5
            }else if (val < 1){
                this.Set4Q5 = 1
            }
        },
        Set5Q1: function (val){
            if (val > 5){
                this.Set5Q1 = 5
            }else if (val < 1){
                this.Set5Q1 = 1
            }
        },
        Set5Q2: function (val){
            if (val > 5){
                this.Set5Q2 = 5
            }else if (val < 1){
                this.Set5Q2 = 1
            }
        },
        Set5Q3: function (val){
            if (val > 5){
                this.Set5Q3 = 5
            }else if (val < 1){
                this.Set5Q3 = 1
            }
        },
        Set5Q4: function (val){
            if (val > 5){
                this.Set5Q4 = 5
            }else if (val < 1){
                this.Set5Q4 = 1
            }
        },
        Set5Q5: function (val){
            if (val > 5){
                this.Set5Q5 = 5
            }else if (val < 1){
                this.Set5Q5 = 1
            }
        },
    }
})

qualitative_data.mount('#qualitative_data')