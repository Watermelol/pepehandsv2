const qualitative_page = Vue.createApp({
    data() {
        return{
            info: false,
            suggestion: false,
            articles: false,
            videos: false,
            networking: false,
            youtube_videos: [],
            recommanded_articles: [],
            people_networking: [],
            qualitative_suggestion: [],
            chartData: {},
            dataLoaded: false,
            fields: '',
        }
    },
    methods:{
        showInfo() {
            this.info= true
            this.suggestion= false
        },

        showSuggestion() {
            this.info= false
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
                url: "/qualitative/get",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.fields = result
                    data.dataLoaded = true
                }
            })
        },

        renderChart(){
            var fields = this.fields
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
                        return fields
                      },
                      color: '#000',
                      fontSize: '36px',
                      show: true,
                    }
                  }
                }
              },
              fill: {
                colors: ['#25d3d9'],
                opacity: 1
              },
              stroke: {
                lineCap: 'round'
              },
              };
      
            var chart = new ApexCharts(document.querySelector("#qualitative_data"), options);
            chart.render();                 
        },
        get_articles() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/qualitative/article",
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
                url: "/qualitative/videos",
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
                url: "/qualitative/networking",
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

        get_suggestion() {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let data = this
            $.ajax({
                url: "/qualitative/suggestion",
                headers:  {'X-CSRFToken': csrftoken},
                success: function(result) {
                    data.qualitative_suggestion = result.data
                }
            })
        },
    },
    mounted(){
        this.showArticles()
        this.showInfo()
        this.getChartData()
        this.get_suggestion()
        this.get_articles()
        this.get_networking()
        this.get_videos()
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

var checkIfExist= document.getElementById("qualitativePage")
if (checkIfExist){
    qualitative_page.mount('#qualitativePage')
}
