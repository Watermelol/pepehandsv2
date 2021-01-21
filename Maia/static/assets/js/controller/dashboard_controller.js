var dashboard = Vue.createApp({
    data() {
        return {
            gradientChartOptionsConfiguration:  {
                maintainAspectRatio: true,
                legend: {
                    display: false
                },
                responsive: true,
            },

            checkIfExist: document.getElementById("atDashboard"),
            overallScore: 0,
            profitabilityScore: 0,
            assetScore: 0,
            cashScore: 0,
            liquidityScore: 0,
        }
    },

    methods: {
        getAnalysisResult() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/dashboard/get/analysisProduct",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.overallScore = (result.overallScore * 10).toFixed(2)
                    data.profitabilityScore = (result.profitabilityScore * 10).toFixed(2)
                    data.assetScore = (result.assetScore * 10).toFixed(2)
                    data.cashScore = (result.cashScore * 10).toFixed(2)
                    data.liquidityScore = (result.liquidityScore * 10).toFixed(2)
                }
            })
        },

        loadOverallCharts() {
            if(this.checkIfExist){
                
                var overallAnalysisCTX = document.getElementById("overallChart").getContext("2d");
            
                var gradientStroke = overallAnalysisCTX.createLinearGradient(0,230,0,50);
            
                gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
                gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
                gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

                var data = {
                    labels: [
                        'Score',
                        ''
                    ],
                    datasets: [{
                        label: "Data",
                        fill: true,
                        backgroundColor: ['#2FB585', '#2F4858'],
                        borderColor: '#5e72e4',
                        borderWidth: 2,
                        borderDash: [],
                        borderDashOffset: 0.0,
                        pointBackgroundColor: '#5e72e4',
                        pointBorderColor:'rgba(255,255,255,0)',
                        pointHoverBackgroundColor: '#5e72e4',
                        pointBorderWidth: 20,
                        pointHoverRadius: 4,
                        pointHoverBorderWidth: 15,
                        pointRadius: 4,
                        data: [this.overallScore, (100-this.overallScore)],
                    }]
                };
            
                var overallChart = new Chart(overallAnalysisCTX, {
                    type: 'doughnut',
                    data: data,
                    options: this.gradientChartOptionsConfiguration
                });
            }else{
                
            }
        },
        loadProfitChart() {
            var profitabilityCTX = document.getElementById("profitChart").getContext("2d");

            var gradientStroke = profitabilityCTX.createLinearGradient(0,230,0,50);
            
            gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
            gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
            gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
        
            var data = {
            labels: [
                'Score',
                ''
            ],
            datasets: [{
                label: "Data",
                fill: true,
                backgroundColor: ['#2FB585', '#2F4858'],
                borderColor: '#5e72e4',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#5e72e4',
                pointBorderColor:'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#5e72e4',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [this.profitabilityScore, (100-this.profitabilityScore)],
            }]
            };

            var profitabilityChart = new Chart(profitabilityCTX, {
                type: 'doughnut',
                data: data,
                options: this.gradientChartOptionsConfiguration
            });
        },

        loadAssetChart() {
            var assetCTX = document.getElementById("assetChart").getContext("2d");

            var gradientStroke = assetCTX.createLinearGradient(0,230,0,50);
            
            gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
            gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
            gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
        
            var data = {
            labels: [
                'Score',
                ''
            ],
            datasets: [{
                label: "Data",
                fill: true,
                backgroundColor: ['#2FB585', '#2F4858'],
                borderColor: '#5e72e4',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#5e72e4',
                pointBorderColor:'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#5e72e4',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [this.assetScore, (100-this.assetScore)],
            }]
            };

            var assetChart = new Chart(assetCTX, {
                type: 'doughnut',
                data: data,
                options: this.gradientChartOptionsConfiguration
            }); 
        },

        loadCashChart() {
            var cashCTX = document.getElementById("cashChart").getContext("2d");

            var gradientStroke = cashCTX.createLinearGradient(0,230,0,50);
            
            gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
            gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
            gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
        
            var data = {
            labels: [
                'Score',
                ''
            ],
            datasets: [{
                label: "Data",
                fill: true,
                backgroundColor: ['#2FB585', '#2F4858'],
                borderColor: '#5e72e4',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#5e72e4',
                pointBorderColor:'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#5e72e4',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [this.cashScore, (100-this.cashScore)],
            }]
            };

            var assetChart = new Chart(cashCTX, {
                type: 'doughnut',
                data: data,
                options: this.gradientChartOptionsConfiguration
            }); 
        },

        loadLiquidityChart() {
            var liquidityCTX = document.getElementById("liquidityChart").getContext("2d");

            var gradientStroke = liquidityCTX.createLinearGradient(0,230,0,50);
            
            gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
            gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
            gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
        
            var data = {
            labels: [
                'Score',
                ''
            ],
            datasets: [{
                label: "Data",
                fill: true,
                backgroundColor: ['#2FB585', '#2F4858'],
                borderColor: '#5e72e4',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#5e72e4',
                pointBorderColor:'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#5e72e4',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [this.liquidityScore, (100-this.liquidityScore)],
            }]
            };

            var assetChart = new Chart(liquidityCTX, {
                type: 'doughnut',
                data: data,
                options: this.gradientChartOptionsConfiguration
            }); 
        }
    },
    mounted() {
        this.getAnalysisResult()
        setTimeout(() => {
            this.loadOverallCharts()
            this.loadProfitChart()
            this.loadAssetChart()
            this.loadCashChart()
            this.loadLiquidityChart()
        }, 350);
    },
    delimiters : ['[$', '$]'],
})
var checkIfExist= document.getElementById("atDashboard")
if (checkIfExist){
    dashboard.mount('#dashboard')
}
