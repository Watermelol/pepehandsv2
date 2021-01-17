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
            profile_edit: {
                'firstName': '',
                'lastName': '',
                'companyName': '',
                'email': '',
                'industryName': '',
                'address1': '',
                'address2': '',
                'city': '',
                'zipCode': '',
            },
            payment_history: [],
            user_financial_data: {},
            user_purchased_report: [],
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
                    data.profile_data.email = result.email

                    data.profile_edit.firstName = result.firstName
                    data.profile_edit.lastName = result.lastName
                    data.profile_edit.companyName = result.companyName
                    data.profile_edit.industryName = result.company_industry
                    data.profile_edit.address1 = result.address1
                    data.profile_edit.address2 = result.address2
                    data.profile_edit.city = result.city
                    data.profile_edit.zipCode = result.zipCode
                    data.profile_edit.email = result.email
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

        validateAllField() {
            if (this.profile_edit.firstName=="" || this.profile_edit.companyName=="" ||
            this.profile_edit.address1=="" || this.profile_edit.city=="" || this.profile_edit.lastName=="" || this.profile_edit.industryName=="" ||
            this.profile_edit.zipCode=="" || this.profile_edit.email=="")
            {
                toastr.warning('Please Make Sure That You Have Enter All Required Fields')
            }
            else{
                this.updateProfile()
            }
        },

        updateProfile() {
            $('#editUserProfile').modal('hide')
            this.showGlobalLoader()
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            var user_data = JSON.stringify(this.profile_edit)
            var data = this
            $.ajax({
                url: "/user/update",
                headers:  {'X-CSRFToken': csrftoken},
                contentType: "application/json; charset=utf-8",
                data: user_data,
                type: 'POST',
                success: function(result) {
                    if (result == 'data saved'){
                        setTimeout(() => {
                            toastr.success("Profile Updated")
                            data.hideGlobalLoader()
                        }, 1000);
                        data.retrive_user_data()
                    }
                }
            })
        },

        getFinancialData () {
            $('#questionaireSelect').modal('hide')
            this.user_financial_data = []
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/user/get/data/financial",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.user_financial_data = result
                }
            })

            $('#editFinancialData').modal()
        },

        updateFinancialData () {
            $('#editFinancialData').modal('hide')
            this.showGlobalLoader()
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/user/update/data/financial",
                headers:  {'X-CSRFToken': csrftoken},
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(data.user_financial_data),
                type: 'POST',
                success: function(result) {
                    setTimeout(() => {
                        toastr.success("Data Updated")
                        data.hideGlobalLoader()
                    }, 1000);
                }
            })
        },

        getPurchasedReport() {
            this.user_purchased_report = []
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/user/get/purchased_report",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    $.each(result.data, function(key, value){
                        value.url = "https://storage.googleapis.com/maia_report_1/pdf/" + value.fileName
                        data.user_purchased_report.push(value)
                    })
                    data.openPurchasedReportModal()
                }
            })
        },

        openReport(url) {
            window.open(url)
        },

        openPurchasedReportModal() {
            $('#purchasedReport').modal()
        },

        openPaymentHistoryModal() {
            $('#paymentHistory').modal()
        },

        openEditUserProfileModal() {
            $('#editUserProfile').modal()
        },

        openQuestionaireSelectModel() {
            $('#questionaireSelect').modal()
        },

        showGlobalLoader() {
            $('#globalLoader').modal('show')
        },

        hideGlobalLoader() {
            $('#globalLoader').modal('hide')
        },

    },
    mounted() {
        this.retrive_user_data()
        this.getPaymentHistory()
    },
    delimiters : ['[$', '$]'],
})

user_profile.mount('#user_profile')