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
            
              var checkIfExist = document.getElementById("liquidity_pillars")
            
              if (checkIfExist){
                var riskAnalysisPillarCTX = document.getElementById("liquidity_pillars").getContext("2d");
              
                var gradientStroke = riskAnalysisPillarCTX.createLinearGradient(0,230,0,50);
                
                gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
                gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
                gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
                
                var data = {
                  labels: [
                    'Just A Thing',
                    'Another Thing',
                    'Third Thing',
                    'Fourth Thing',
                    'Fifth A Thing',
                  ],
                  datasets: [{
                    label: "Quater 1",
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
                    data: [33, 2.9, 0.9, 4.1, 5.1],
                  },{
                      label: "Quater 2",
                    fill: true,
                    borderColor: '#42f5f2',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#42f5f2',
                    pointBorderColor:'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#42f5f2',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: [2.7, 1.9, 1.5, 2.1, 1.1],
                  }]
                };
                
                var performancePillarChart = new Chart(riskAnalysisPillarCTX, {
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
        this.renderChart()
        this.get_videos()
        this.get_articles()
        this.get_networking()
        this.get_comment()
        this.get_suggestion()
    },
    delimiters : ['[$', '$]'],
})

var checkIfExist= document.getElementById("liquidityPillarPage")
if (checkIfExist){
    risk_pillars.mount('#liquidityPillarPage')
}
