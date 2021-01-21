var news_sentiment = Vue.createApp({
    data() {
        return{
            gradientChartOptionsConfiguration:  {
                maintainAspectRatio: true,
                legend: {
                    display: false
                },
                responsive: false,
            },
        }
    },

    methods: {
        loadNewsSentimentChart() {
            var options = {
                series: [60],
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
                      color: '#fff',
                      fontSize: '17px'
                    },
                    value: {
                      formatter: function(val) {
                        return parseInt(val);
                      },
                      color: '#c8cbcf',
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
                  gradientToColors: ['#ABE5A1'],
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
      
            var chart = new ApexCharts(document.querySelector("#newsSentimentChart"), options);
            chart.render();
        },
    },

    mounted() {
        this.loadNewsSentimentChart()
    }
})

var checkIfExist= document.getElementById("news_sentiment")
if (checkIfExist){
    news_sentiment.mount('#news_sentiment')
}