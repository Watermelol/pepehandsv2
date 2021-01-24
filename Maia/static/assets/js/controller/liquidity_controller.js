const risk_pillars = Vue.createApp({
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
            liquidity_comment: [],
            liquidity_suggestion: [],
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
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            var data = this
            $.ajax({
                url: "/pillars/liquidity/chart-data",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.chartData = result
                    data.dataLoaded = true
                }
            })
        },

        renderChart(){
            gradientChartOptionsConfiguration =  {
                maintainAspectRatio: true,
                legend: {
                      display: false,
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
                        display: true,
                        ticks: {
                            beginAtZero: true,  // minimum value will be 0.
                            fontColor: '#fff'
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            fontColor: '#fff'
                        },
                    }]
                }
              };
            
              var checkIfExist = document.getElementById("liquidity_pillars")
            
              if (checkIfExist){
                var riskAnalysisPillarCTX = document.getElementById("liquidity_pillars").getContext("2d");
              
                var gradientStroke = riskAnalysisPillarCTX.createLinearGradient(0,230,0,50);
                
                gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
                gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
                gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
                
                var data = {
                  labels: [
                    'Quick Ratio',
                    'Current Ratio',
                    'Cash Ratio',
                  ],
                  datasets: [{
                    fill: true,
                    borderColor: ['#73CD73', '#1fd2ed', '#0a19f2'],
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: ['#73CD73', '#1fd2ed', '#0a19f2'],
                    pointHoverBackgroundColor: ['#73CD73', '#1fd2ed', '#0a19f2'],
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: [this.chartData.quick_ratio, this.chartData.current_ratio, this.chartData.cash_ratio],
                  }]
                };
                
                var performancePillarChart = new Chart(riskAnalysisPillarCTX, {
                  type: 'bar',
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
                url: "/pillars/liquidity/article",
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
                url: "/pillars/liquidity/videos",
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
                url: "/pillars/liquidity/networking",
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
                url: "/pillars/liquidity/comment",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.liquidity_comment = result.data
                }
            })
        },

        get_suggestion() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/liquidity/suggestion",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.liquidity_suggestion = result.data
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

var checkIfExist= document.getElementById("liquidityPillarPage")
if (checkIfExist){
    risk_pillars.mount('#liquidityPillarPage')
}
