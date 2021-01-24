const productivity_pillars = Vue.createApp({
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
            cash_comment: [],
            cash_suggestion: [],
            chartData: {},
            dataLoaded: false,
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
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/cash/chart-data",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.chartData = result
                    data.dataLoaded= true
                }
            })
        },

        renderChart(){
            gradientChartOptionsConfiguration =  {
                maintainAspectRatio: true,
                legend: {
                      display: true,
                      labels: {
                          fontColor: '#fff'
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
                            fontColor: '#fff'
                        },
                    }],
                  xAxes: [{
                        ticks: {
                            fontColor: '#fff'
                        },
                    }]
                } 
              };
            
              var checkIfExist = document.getElementById("cash_pillars")
            
              if (checkIfExist){
                var productivityPillarCTX = document.getElementById("cash_pillars").getContext("2d");
              
                var gradientStroke = productivityPillarCTX.createLinearGradient(0,230,0,50);
                
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
                    label: "Net Cash Flow",
                    fill: true,
                    borderColor: '#73CD73',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#73CD73',
                    pointBorderColor:'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#73CD73',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: [this.chartData.q1_net_cash_flow, this.chartData.q2_net_cash_flow, this.chartData.q3_net_cash_flow, this.chartData.q4_net_cash_flow,],
                  }]
                };
                
                var performancePillarChart = new Chart(productivityPillarCTX, {
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
                url: "/pillars/cash/article",
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
                url: "/pillars/cash/videos",
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
                url: "/pillars/cash/networking",
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
                url: "/pillars/cash/comment",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.cash_comment = result.data
                }
            })
        },

        get_suggestion() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/cash/suggestion",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.cash_suggestion = result.data
                }
            })
        },
    },
    mounted(){
        this.showArticles()
        this.showInfo()
        this.getChartData()
        this.get_videos()
        this.get_articles()
        this.get_networking()
        this.get_comment()
        this.get_suggestion()
    },
    watch: {
        dataLoaded() {
            if (this.dataLoaded){
                this.renderChart()
            }
        }
    },
    delimiters : ['[$', '$]'],
})

var checkIfExist= document.getElementById("cashPillarPage")
if (checkIfExist){
    productivity_pillars.mount('#cashPillarPage')
}
