const financial_data_questionaire_controller = Vue.createApp({
    data() {
        return {
            user_financial_data: {
                'q1_revenue': 0.00,
                'q1_profit_before_tax': 0.00,
                'q1_net_profit': 0.00,
                'q2_revenue': 0.00,
                'q2_profit_before_tax': 0.00,
                'q2_net_profit': 0.00,
                'q3_revenue': 0.00,
                'q3_profit_before_tax': 0.00,
                'q3_net_profit': 0.00,
                'q4_net_profit': 0.00,
                'q4_revenue': 0.00,
                'q4_profit_before_tax': 0.00,
                'yearly_revenue': 0.00,
                'yearly_net_profit': 0.00,
                'cash': 0.00,
                'debt': 0.00,
                'total_debt': 0.00,
                'net_assets': 0.00,
                'current_ratio': 0.00,
                'quick_ratio': 0.00,
                'cash_ratio': 0.00,
                'return_on_asset': 0.00,
                'asset_turn_over_ratio': 0.00,
                'debt_to_asset_ratio': 0.00,
                'net_tangeble_asset': 0.00,
            },
        }
    },
    methods: {
        submit_financial_data_record () {
            this.showGlobalLoader()
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            var data = this
            var financial_data = JSON.stringify(this.user_financial_data)
            $.ajax({
                url: "/financial_data_questionaire/",
                headers:  {'X-CSRFToken': csrftoken},
                contentType: "application/json; charset=utf-8",
                data: financial_data,
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
    delimiters : ['[$', '$]']
})

financial_data_questionaire_controller.mount('#financial_data_forms')