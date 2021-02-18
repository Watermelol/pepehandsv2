const performance_pillars = Vue.createApp({
    data() {
        return{
            info: false,
            comments: false,
            suggestion: false,
            articles: false,
            videos: false,
            networking: false,
            youtube_videos: [],
            recommanded_articles: [],
            people_networking: [],
            profit_comment: [],
            profit_suggestion: [],
            chartData: {},
        }
    },
    methods:{
        showInfo() {
            this.info= true
            this.comments= false
            this.suggestion= false
        },

        showComment() {
            this.info= false
            this.comments= true
            this.suggestion= false
        },

        showSuggestion() {
            this.info= false
            this.comments= false
            this.suggestion= true
        },

        showArticles() {
            this.articles= true
            this.videos= false
            this.networking= false
        },

        showVideos() {
            this.articles= false
            this.videos= true
            this.networking= false
        },

        showNetworking() {
            this.articles= false
            this.videos= false
            this.networking= true
        },

        getChartData() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            var data = this
            $.ajax({
                url: "/pillars/profit/chart-date",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.chartData = result
                }
            })
        },

        renderChart(){
            gradientChartOptionsConfiguration =  {
                maintainAspectRatio: true,
                legend: {
                      display: true,
                      labels: {
                          fontColor: '#000'
                      }
                 },
              
                 tooltips: {
                   backgroundColor: '#fff',
                   titleFontColor: '#333',
                   bodyFontColor: '#666',
                   bodySpacing: 4,
                   xPadding: 12,
                   mode: "nearest",
                   intersect: 0,
                   position: "nearest"
                 },
                 responsive: true,
                 scales: {
                    yAxes: [{
                        ticks: {
                            fontColor: '#000'
                        },
                    }],
                  xAxes: [{
                        ticks: {
                            fontColor: '#000'
                        },
                    }]
                } 
              };
            
              var checkIfExist = document.getElementById("profit_pillars")
            
              if (checkIfExist){
                var performancePillarCTX = document.getElementById("profit_pillars").getContext("2d");
                
                var gradientStroke = performancePillarCTX.createLinearGradient(0,230,0,50);
                
                gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
                gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
                gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
                
                var data = {
                  labels: [
                    'Quater 1',
                    'Quater 2',
                    'Quater 3',
                    'Quater 4',
                  ],
                  datasets: [{
                    label: "Profit",
                    fill: true,
                    borderColor: '#04b01d',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#04b01d',
                    pointBorderColor:'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#04b01d',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: this.chartData.profit,
                  },{
                      label: "Revenue",
                    fill: true,
                    borderColor: '#0aabcf',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#0aabcf',
                    pointBorderColor:'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#0aabcf',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: this.chartData.revenue,
                  }]
                };
                
                var performancePillarChart = new Chart(performancePillarCTX, {
                  type: 'line',
                  data: data,
                  options: gradientChartOptionsConfiguration
                });
            }else{
            
            }                      
        },

        get_articles() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/profit/article",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.recommanded_articles = result.data
                }
            })
        },

        goToArticle(url) {
            window.open(url)
        },

        get_videos() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/profit/videos",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.youtube_videos = result.items
                }
            })
        },

        goToVideo(id) {
            window.open('https://www.youtube.com/watch?v=' + id )
        },

        get_networking() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/profit/networking",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    let array = []
                    $.each(result.data, function(k, v){
                        v.skills = v.skills.split('\n')
                    })
                    data.people_networking = result.data
                }
            })
        },

        goToLinkedin(url) {
            window.open(url)
        },

        get_comment() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/profit/comment",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.profit_comment = result.data
                    console.log(data.profit_comment)
                }
            })
        },

        get_suggestion() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/profit/suggestion",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.profit_suggestion = result.data
                    console.log(data.profit_suggestion)
                }
            })
        },
    },
    mounted(){
        this.getChartData()
        setTimeout(() => {
            this.renderChart()
        }, 350);
        this.showArticles()
        this.showInfo()
        this.get_videos()
        this.get_articles()
        this.get_networking()
        this.get_comment()
        this.get_suggestion()
    },
    delimiters : ['[$', '$]'],
})

var checkIfExist= document.getElementById("profitPillarPage")
if (checkIfExist){
    performance_pillars.mount('#profitPillarPage')
}
