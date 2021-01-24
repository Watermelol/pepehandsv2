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

            news_sentiment: {},
            data_loaded: false
        }
    },

    methods: {
        loadNewsSentimentChart() {
          var color = ''
          if (this.news_sentiment.overallSentimentScore <= -0.25){
            color = '#ff0505'
          }else if (this.news_sentiment.overallSentimentScore >= 0.25){
            color = '#00ff99'
          }else{
            color = '#25d3d9'
          }
          
          var options = {
              series: [100],
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
                    show: false,
                    color: '#fff',
                    fontSize: '17px'
                  },
                  value: {
                    formatter: function(val) {
                      if (this.news_sentiment.overallSentimentScore <= -0.25){
                        if (this.news_sentiment.overallMagnitude >= 5){
                          return 'Strongly Negative';
                        }else{
                          return 'Negative';
                        }
                        
                      }else if (this.news_sentiment.overallSentimentScore >= -0.25){
                        if (this.news_sentiment.overallMagnitude >= 5){
                          return 'Strongly Positive';
                        }else{
                          return 'Positive';
                        }
                      }else{
                        return 'Neutral'
                      }
                      
                    },
                    color: '#c8cbcf',
                    fontSize: '36px',
                    show: true,
                  }
                }
              }
            },
            fill: {
              colors: [color],
              opacity: 1
            },
            stroke: {
              lineCap: 'round'
            },
            labels: ['Overall News Sentiment'],
            };
    
          var chart = new ApexCharts(document.querySelector("#newsSentimentChart"), options);
          chart.render();
        },

        get_news_sentiment(){
          const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
          var data = this
          $.ajax({
            url: "/news-sentiment/get",
            headers:  {'X-CSRFToken': csrftoken},
            success: function(result) {
                data.news_sentiment = result
                data.data_loaded = true
            }
        })
        },

        goToNews(url){
          window.open(url)
        }

    },
    watch: {
      data_loaded() {
        if(this.data_loaded == true){
          this.loadNewsSentimentChart()
        }
      }
    },
    mounted() {
      this.get_news_sentiment()
    },
    delimiters : ['[$', '$]'],
})

var checkIfExist= document.getElementById("news_sentiment")
if (checkIfExist){
    news_sentiment.mount('#news_sentiment')
}