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

            overallGradientChartOptionsConfiguration:  {
                maintainAspectRatio: true,
                legend: {
                    display: false
                },
                responsive: false,
            },

            checkIfExist: document.getElementById("atDashboard"),
            overallScore: 0,
            profitabilityScore: 0,
            assetScore: 0,
            cashScore: 0,
            liquidityScore: 0,
            showChart: false,
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
                    data.showChart = true
                }
            })
        },

        loadOverallCharts() {
            if(this.checkIfExist){

                var options = {
                    series: [this.overallScore],
                    chart: {
                    height: 450,
                    type: 'radialBar',
                  },
                  plotOptions: {
                    radialBar: {
                      startAngle: 0,
                      endAngle: 360,
                       hollow: {
                        margin: 0,
                        size: '75%',
                        image: undefined,
                        imageOffsetX: 0,
                        imageOffsetY: 0,
                        position: 'front',
                        dropShadow: {
                          enabled: true,
                          top: 3,
                          left: 0,
                          blur: 4,
                          opacity: 0.24
                        }
                      },
                      track: {
                        background: '#fff',
                        strokeWidth: '67%',
                        margin: 0, // margin is in pixels
                        dropShadow: {
                          enabled: true,
                          top: -3,
                          left: 0,
                          blur: 4,
                          opacity: 0.35
                        }
                      },
                  
                      dataLabels: {
                        show: true,
                        name: {
                          offsetY: -10,
                          show: true,
                          color: 'black',
                          fontSize: '17px'
                        },
                        value: {
                          color: '#1792ad',
                          fontSize: '36px',
                          show: true,
                        }
                      }
                    }
                  },
                  fill: {
                    type: 'gradient',
                    gradient: {
                      shade: 'light',
                      type: 'horizontal',
                      shadeIntensity: 0.5,
                      gradientToColors: ['#00C5BF'],
                      inverseColors: false,
                      opacityFrom: 1,
                      opacityTo: 1,
                      stops: [0, 100]
                    }
                  },
                  stroke: {
                    lineCap: 'round'
                  },
                  labels: ['Overall Score'],
                  };
          
                var chart = new ApexCharts(document.querySelector("#overallChart"), options);
                chart.render();
            }else{
                
            }
        },
        loadProfitChart() {
            var options = {
                series: [this.profitabilityScore],
                chart: {
                height: 300,
                type: 'radialBar',
              },
              plotOptions: {
                radialBar: {
                  startAngle: 0,
                  endAngle: 360,
                   hollow: {
                    margin: 0,
                    size: '75%',
                    image: undefined,
                    imageOffsetX: 0,
                    imageOffsetY: 0,
                    position: 'front',
                    dropShadow: {
                      enabled: true,
                      top: 3,
                      left: 0,
                      blur: 4,
                      opacity: 0.24
                    }
                  },
                  track: {
                    background: '#fff',
                    strokeWidth: '67%',
                    margin: 0, // margin is in pixels
                    dropShadow: {
                      enabled: true,
                      top: -3,
                      left: 0,
                      blur: 4,
                      opacity: 0.35
                    }
                  },
              
                  dataLabels: {
                    show: true,
                    name: {
                      offsetY: -10,
                      show: true,
                      color: '#000',
                      fontSize: '17px'
                    },
                    value: {
                      color: '#1792ad',
                      fontSize: '36px',
                      show: true,
                    }
                  }
                }
              },
              fill: {
                type: 'gradient',
                gradient: {
                  shade: 'light',
                  type: 'horizontal',
                  shadeIntensity: 0.5,
                  gradientToColors: ['#00C5BF'],
                  inverseColors: false,
                  opacityFrom: 1,
                  opacityTo: 1,
                  stops: [0, 100]
                }
              },
              stroke: {
                lineCap: 'round'
              },
              labels: ['Profitability Score'],
              };
      
            var chart = new ApexCharts(document.querySelector("#profitChart"), options);
            chart.render();
        },

        loadAssetChart() {
            var options = {
                series: [this.assetScore],
                chart: {
                height: 300,
                type: 'radialBar',
              },
              plotOptions: {
                radialBar: {
                  startAngle: 0,
                  endAngle: 360,
                   hollow: {
                    margin: 0,
                    size: '75%',
                    image: undefined,
                    imageOffsetX: 0,
                    imageOffsetY: 0,
                    position: 'front',
                    dropShadow: {
                      enabled: true,
                      top: 3,
                      left: 0,
                      blur: 4,
                      opacity: 0.24
                    }
                  },
                  track: {
                    background: '#fff',
                    strokeWidth: '67%',
                    margin: 0, // margin is in pixels
                    dropShadow: {
                      enabled: true,
                      top: -3,
                      left: 0,
                      blur: 4,
                      opacity: 0.35
                    }
                  },
              
                  dataLabels: {
                    show: true,
                    name: {
                      offsetY: -10,
                      show: true,
                      color: '#000',
                      fontSize: '17px'
                    },
                    value: {
                      color: '#1792ad',
                      fontSize: '36px',
                      show: true,
                    }
                  }
                }
              },
              fill: {
                type: 'gradient',
                gradient: {
                  shade: 'light',
                  type: 'horizontal',
                  shadeIntensity: 0.5,
                  gradientToColors: ['#00C5BF'],
                  inverseColors: false,
                  opacityFrom: 1,
                  opacityTo: 1,
                  stops: [0, 100]
                }
              },
              stroke: {
                lineCap: 'round'
              },
              labels: ['Asset Score'],
              };
      
            var chart = new ApexCharts(document.querySelector("#assetChart"), options);
            chart.render();
        },

        loadCashChart() {
            var options = {
                series: [this.cashScore],
                chart: {
                height: 300,
                type: 'radialBar',
              },
              plotOptions: {
                radialBar: {
                  startAngle: 0,
                  endAngle: 360,
                   hollow: {
                    margin: 0,
                    size: '75%',
                    image: undefined,
                    imageOffsetX: 0,
                    imageOffsetY: 0,
                    position: 'front',
                    dropShadow: {
                      enabled: true,
                      top: 3,
                      left: 0,
                      blur: 4,
                      opacity: 0.24
                    }
                  },
                  track: {
                    background: '#fff',
                    strokeWidth: '67%',
                    margin: 0, // margin is in pixels
                    dropShadow: {
                      enabled: true,
                      top: -3,
                      left: 0,
                      blur: 4,
                      opacity: 0.35
                    }
                  },
              
                  dataLabels: {
                    show: true,
                    name: {
                      offsetY: -10,
                      show: true,
                      color: '#000',
                      fontSize: '17px'
                    },
                    value: {
                      color: '#1792ad',
                      fontSize: '36px',
                      show: true,
                    }
                  }
                }
              },
              fill: {
                type: 'gradient',
                gradient: {
                  shade: 'light',
                  type: 'horizontal',
                  shadeIntensity: 0.5,
                  gradientToColors: ['#00C5BF'],
                  inverseColors: false,
                  opacityFrom: 1,
                  opacityTo: 1,
                  stops: [0, 100]
                }
              },
              stroke: {
                lineCap: 'round'
              },
              labels: ['Cash Score'],
              };
      
            var chart = new ApexCharts(document.querySelector("#cashChart"), options);
            chart.render();
        },

        loadLiquidityChart() {
            var options = {
                series: [this.liquidityScore],
                chart: {
                height: 300,
                type: 'radialBar',
              },
              plotOptions: {
                radialBar: {
                  startAngle: 0,
                  endAngle: 360,
                   hollow: {
                    margin: 0,
                    size: '75%',
                    image: undefined,
                    imageOffsetX: 0,
                    imageOffsetY: 0,
                    position: 'front',
                    dropShadow: {
                      enabled: true,
                      top: 3,
                      left: 0,
                      blur: 4,
                      opacity: 0.24
                    }
                  },
                  track: {
                    background: '#fff',
                    strokeWidth: '67%',
                    margin: 0, // margin is in pixels
                    dropShadow: {
                      enabled: true,
                      top: -3,
                      left: 0,
                      blur: 4,
                      opacity: 0.35
                    }
                  },
              
                  dataLabels: {
                    show: true,
                    name: {
                      offsetY: -10,
                      show: true,
                      color: '#000',
                      fontSize: '17px'
                    },
                    value: {
                      color: '#1792ad',
                      fontSize: '36px',
                      show: true,
                    }
                  }
                }
              },
              fill: {
                type: 'gradient',
                gradient: {
                  shade: 'light',
                  type: 'horizontal',
                  shadeIntensity: 0.5,
                  gradientToColors: ['#00C5BF'],
                  inverseColors: false,
                  opacityFrom: 1,
                  opacityTo: 1,
                  stops: [0, 100]
                }
              },
              stroke: {
                lineCap: 'round'
              },
              labels: ['Liquidity Score'],
              };
      
            var chart = new ApexCharts(document.querySelector("#liquidityChart"), options);
            chart.render();
        }
    },
    watch: {
      showChart: function(val){
        if (val){
          this.loadOverallCharts()
          this.loadProfitChart()
          this.loadAssetChart()
          this.loadCashChart()
          this.loadLiquidityChart()
        }
      }
    },
    mounted() {
      this.getAnalysisResult()
    },
    delimiters : ['[$', '$]'],
})
var checkIfExist= document.getElementById("atDashboard")
if (checkIfExist){
    dashboard.mount('#dashboard')
}
