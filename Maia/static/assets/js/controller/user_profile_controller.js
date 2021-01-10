const user_profile = Vue.createApp({
    data () {
        return{
            profile_data: {
                'firstName': '',
                'lastName': '',
                'companyName': '',
                'industryName': '',
                'address1': '',
                'address2': '',
                'city': '',
                'zipCode': '',
            },
            payment_history: []
        }
    },
    methods: {
        retrive_user_data () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/user/get/data/",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.profile_data.firstName = result.firstName
                    data.profile_data.lastName = result.lastName
                    data.profile_data.companyName = result.companyName
                    data.profile_data.industryName = result.company_industry
                    data.profile_data.address1 = result.address1
                    data.profile_data.address2 = result.address2
                    data.profile_data.city = result.city
                    data.profile_data.zipCode = result.zipCode
                }
            })
        },

        getPaymentHistory() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/user/get/payment_history",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    $.each(result.data, function(key, value){
                        data.payment_history.push(value)
                    })
                }
            })
        },

        openPaymentHistoryModal() {
            $('#paymentHistory').modal()
        }
    },
    mounted() {
        this.retrive_user_data()
        this.getPaymentHistory()
    },
    delimiters : ['[$', '$]'],
})

user_profile.mount('#user_profile')