const value_pillars = Vue.createApp({
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
            asset_comment: [],
            asset_suggestion: [],
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

        get_chart_data() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            var data = this
            $.ajax({
                url: "/pillars/asset/chart-date",
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
                      display: false
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
                            beginAtZero: true   // minimum value will be 0.
                        }
                    }]
                }
              };
            
              var checkIfExist = document.getElementById("asset_pillars")
            
              if (checkIfExist){
                var valuePillarCTX = document.getElementById("asset_pillars").getContext("2d");
              
                var gradientStroke = valuePillarCTX.createLinearGradient(0,230,0,50);
                
                gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
                gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
                gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
                
                var data = {
                  labels: [
                    'Return of Asset',
                    'Asset Turnover Ratio',
                    'Debt to Asset Ratio',
                  ],
                  datasets: [{
                    label: "Return of Asset",
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
                    data: [this.chartData.return_of_asset, this.chartData.asset_turnover_ratio, this.chartData.debt_to_asset_ratio],
                  }]
                };
                
                var valuePillarChart = new Chart(valuePillarCTX, {
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
                url: "/pillars/asset/article",
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
                url: "/pillars/asset/videos",
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
                url: "/pillars/asset/networking",
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
                url: "/pillars/asset/comment",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.asset_comment = result.data
                }
            })
        },

        get_suggestion() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/pillars/asset/suggestion",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.asset_suggestion = result.data
                }
            })
        },
    },
    mounted(){
        this.get_chart_data()
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

var checkIfExist= document.getElementById("assetPillarPage")
if (checkIfExist){
    value_pillars.mount('#assetPillarPage')
}
