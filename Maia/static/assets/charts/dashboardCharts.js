
gradientChartOptionsConfiguration =  {
  maintainAspectRatio: true,
  legend: {
        display: true
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
};

var checkIfExist = document.getElementById("atDashboard")

if(checkIfExist){
  var performanceCTX = document.getElementById("profitChart").getContext("2d");
  var businessValueCTX = document.getElementById("assetChart").getContext("2d");
  var productivityCTX = document.getElementById("cashChart").getContext("2d");
  var riskAnalysisCTX = document.getElementById("liquidityChart").getContext("2d");
  var overallAnalysisCTX = document.getElementById("overallChart").getContext("2d");

  var gradientStroke = performanceCTX.createLinearGradient(0,230,0,50);

  gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
  gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
  gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

  var data = {
    labels: [
      'good',
      'bad'
    ],
    datasets: [{
      label: "Data",
      fill: true,
      backgroundColor: ['#73CD73', '#2F4858'],
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
      data: [60, 40],
    }]
  };

  var businessPerformanceChart = new Chart(performanceCTX, {
    type: 'doughnut',
    data: data,
    options: gradientChartOptionsConfiguration
  });

  var businessValueChart = new Chart(businessValueCTX, {
    type: 'doughnut',
    data: data,
    options: gradientChartOptionsConfiguration
  });

  var productivityChart = new Chart(productivityCTX, {
    type: 'doughnut',
    data: data,
    options: gradientChartOptionsConfiguration
  });

  var riskAnalysisChart = new Chart(riskAnalysisCTX, {
    type: 'doughnut',
    data: data,
    options: gradientChartOptionsConfiguration
  });

  var riskAnalysisChart = new Chart(overallAnalysisCTX, {
    type: 'doughnut',
    data: data,
    options: gradientChartOptionsConfiguration
  });
}else{
  
}

