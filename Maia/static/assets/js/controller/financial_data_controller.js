const financial_data_questionaire_controller = Vue.createApp({
    data() {
        return {
            user_financial_data: {
                'q1_revenue': 0.00,
                'q1_profit_before_tax': 0.00,
                'q1_net_profit': 0.00,
                'q1_net_cash_flow': 0.00,
                'q2_revenue': 0.00,
                'q2_profit_before_tax': 0.00,
                'q2_net_profit': 0.00,
                'q2_net_cash_flow': 0.00,
                'q3_revenue': 0.00,
                'q3_profit_before_tax': 0.00,
                'q3_net_profit': 0.00,
                'q3_net_cash_flow': 0.00,
                'q4_net_profit': 0.00,
                'q4_revenue': 0.00,
                'q4_profit_before_tax': 0.00,
                'q4_net_cash_flow': 0.00,
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
                'total_liability' : 0.00,
                'shareholder_equity': 0.00,
                'return_on_equity': 0.00,
            },
        }
    },
    methods: {
        submit_financial_data_record () {
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
            }
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