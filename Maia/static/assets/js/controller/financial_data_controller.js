const financial_data_questionaire_controller = Vue.createApp({
    data() {
        return {
            user_financial_data: {
                data: [
                    {
                        'id': 1,
                        'quater': 'Q1',
                        'revenue': 0,
                        'net_profit': 0,
                        'expenses': 0,
                        'return_on_equity': 0,
                        'firm_value': 0,
                        'debt': 0,
                        'equity': 0,
                        'return_on_asset': 0,
                        'return_on_investment': 0,
                        'networking_capital': 0,
                        'spending_on_research': 0,
                        'property_plant_equipment': 0,
                        'cash_flow': 0,
                        'goodwill': 0,
                        'total_assets': 0,
                        'total_liabilities': 0,
                        'current_ratio': 0,
                        'quick_ratio': 0,
                        'cash_ratio': 0,
                    }
                ] 
            },
            data_size : 1,
        }
    },
    methods: {
        submit_financial_data_record () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            var financial_data = JSON.stringify(this.user_financial_data)
            $.ajax({
                url: "/financial_data_questionaire/",
                headers:  {'X-CSRFToken': csrftoken},
                contentType: "application/json; charset=utf-8",
                data: financial_data,
                dataType: "json",
                type: 'POST',
                success: function(result) {
                    console.log(result)
                }
            })
        },

        add_financial_data_record () {
            let financial_data = this.user_financial_data.data
            let financial_data_size = financial_data.length;
            if (financial_data_size < 4){
                this.data_size = this.data_size + 1
                let new_financial_data = {
                    'id': this.data_size,
                    'quater': 'Q1',
                    'revenue': 0,
                    'net_profit': 0,
                    'expenses': 0,
                    'return_on_equity': 0,
                    'firm_value': 0,
                    'debt': 0,
                    'equity': 0,
                    'return_on_asset': 0,
                    'return_on_investment': 3,
                    'networking_capital': 0,
                    'spending_on_research': 0,
                    'property_plant_equipment': 1,
                    'cash_flow': 0,
                    'goodwill': 0,
                    'total_assets': 0,
                    'total_liabilities': 0,
                    'current_ratio': 0,
                    'quick_ratio': 0,
                    'cash_ratio': 0,
                }
                this.user_financial_data.data.push(new_financial_data)
                toastr.success('Record Added')
            }else {
                toastr.info('The Maximum Record Is 4')
            }
        },

        remove_financial_data_record (index) {
            console.log(index)
            if (this.data_size > 1){
                Swal.fire({
                    title: 'Are you sure?',
                    text: "You won't be able to revert this!",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#d33',
                    cancelButtonColor: '#3085d6',
                    confirmButtonText: 'Remove'
                  }).then((result) => {
                    if (result.isConfirmed) {
                      this.user_financial_data.data.splice(index, 1)
                      this.data_size = this.data_size - 1
                      $.each(this.user_financial_data.data, function(index, value){
                        let removed_record_id = index + 1
                        if (value.id > removed_record_id){
                            value.id--
                        }
                      })
                      toastr.error('Record Removed')
                    }
                  })
            }else {
                toastr.warning('The Minimum Record Is 1')
            }
            
        }
    },
    delimiters : ['[$', '$]']
})

financial_data_questionaire_controller.mount('#financial_data_forms')