const user_profile = Vue.createApp({
    data () {
        return{
            profile_data: {
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
            pageNumber: 1,

            Set1Q1:0, 
            Set1Q2:0, 
            Set1Q3:0, 
            Set1Q4:0, 
            Set1Q5:0, 
            Set2Q1:0, 
            Set2Q2:0, 
            Set2Q3:0, 
            Set2Q4:0, 
            Set2Q5:0, 
            Set3Q1:0, 
            Set3Q2:0, 
            Set3Q3:0, 
            Set3Q4:0, 
            Set3Q5:0, 
            Set4Q1:0, 
            Set4Q2:0, 
            Set4Q3:0, 
            Set4Q4:0, 
            Set4Q5:0, 
            Set5Q1:0, 
            Set5Q2:0, 
            Set5Q3:0, 
            Set5Q4:0, 
            Set5Q5:0, 
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
                    data.profile_data.company_size = result.company_size
                    data.profile_data.company_size_value = result.company_size_value

                    data.profile_edit.firstName = result.firstName
                    data.profile_edit.lastName = result.lastName
                    data.profile_edit.companyName = result.companyName
                    data.profile_edit.industryName = result.company_industry
                    data.profile_edit.address1 = result.address1
                    data.profile_edit.address2 = result.address2
                    data.profile_edit.city = result.city
                    data.profile_edit.zipCode = result.zipCode
                    data.profile_edit.email = result.email
                    data.profile_edit.company_size = result.company_size
                    data.profile_data.company_size_value = result.company_size_value
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

        getQuestionaireData () {
            $('#questionaireSelect').modal('hide')
            this.pageNumber = 1
            this.user_financial_data = []
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/user/get/data/questionaire",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.Set1Q1 = result.set1q1
                    data.Set1Q2 = result.set1q2
                    data.Set1Q3 = result.set1q3
                    data.Set1Q4 = result.set1q4
                    data.Set1Q5 = result.set1q5
                    data.Set2Q1 = result.set2q1
                    data.Set2Q2 = result.set2q2
                    data.Set2Q3 = result.set2q3
                    data.Set2Q4 = result.set2q4
                    data.Set2Q5 = result.set2q5
                    data.Set3Q1 = result.set3q1
                    data.Set3Q2 = result.set3q2
                    data.Set3Q3 = result.set3q3
                    data.Set3Q4 = result.set3q4
                    data.Set3Q5 = result.set3q5
                    data.Set4Q1 = result.set4q1
                    data.Set4Q2 = result.set4q2
                    data.Set4Q3 = result.set4q3
                    data.Set4Q4 = result.set4q4
                    data.Set4Q5 = result.set4q5
                    data.Set5Q1 = result.set5q1
                    data.Set5Q2 = result.set5q2
                    data.Set5Q3 = result.set5q3
                    data.Set5Q4 = result.set5q4
                    data.Set5Q5 = result.set5q5
                }
            })

            $('#editQuestionaireData').modal()
        },

        updateFinancialData () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            if (
                this.user_financial_data.q1_revenue === '' ||
                this.user_financial_data.q1_profit_before_tax === '' ||
                this.user_financial_data.q1_net_profit === '' ||
                this.user_financial_data.q1_net_cash_flow === '' ||
                this.user_financial_data.q2_revenue === '' ||
                this.user_financial_data.q2_profit_before_tax === '' ||
                this.user_financial_data.q2_net_profit === '' ||
                this.user_financial_data.q2_net_cash_flow === '' ||
                this.user_financial_data.q3_revenue === '' ||
                this.user_financial_data.q3_profit_before_tax === '' ||
                this.user_financial_data.q3_net_profit === '' ||
                this.user_financial_data.q3_net_cash_flow === '' ||
                this.user_financial_data.q4_revenue === '' ||
                this.user_financial_data.q4_profit_before_tax === '' ||
                this.user_financial_data.q4_net_profit === '' ||
                this.user_financial_data.q4_net_cash_flow === '' ||
                this.user_financial_data.yearly_revenue === '' ||
                this.user_financial_data.yearly_net_profit === '' ||
                this.user_financial_data.cash === '' ||
                this.user_financial_data.debt === '' ||
                this.user_financial_data.total_debt === '' ||
                this.user_financial_data.net_assets === '' ||
                this.user_financial_data.current_ratio === '' ||
                this.user_financial_data.quick_ratio === '' ||
                this.user_financial_data.cash_ratio === '' ||
                this.user_financial_data.return_on_asset === '' ||
                this.user_financial_data.asset_turn_over_ratio === '' ||
                this.user_financial_data.debt_to_asset_ratio === '' ||
                this.user_financial_data.net_tangeble_asset === '' ||
                this.user_financial_data.total_liability === '' ||
                this.user_financial_data.shareholder_equity === '' ||
                this.user_financial_data.return_on_equity === ''
            ){
                toastr.warning('Please make sure that you have fill in all the column')
            }
            else{
                $('#editFinancialData').modal('hide')
                this.showGlobalLoader()
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
            }
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

        submitAnswer() {
            $('#editQuestionaireData').modal('hide')
            this.showGlobalLoader()
            var data = this
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
                url: "/user/update/data/questionaire",
                headers:  {'X-CSRFToken': csrftoken},
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(result),
                type: 'POST',
                success: function(result) {
                    if (result == 'data saved'){
                        setTimeout(() => {
                            toastr.success("Data Updated")
                            data.hideGlobalLoader()
                        }, 1000);
                    }
                }
            })
        },

        nextPage () {
            this.pageNumber++
        },

        previousPage() {
            this.pageNumber--
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
    },
    delimiters : ['[$', '$]'],
})
var checkIfExist= document.getElementById("user_profile")
if (checkIfExist){
    user_profile.mount('#user_profile')
}
