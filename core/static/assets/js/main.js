/* eslint-disable object-shorthand */

/* global Chart, coreui, coreui.Utils.getStyle, coreui.Utils.hexToRgba */

/**
 * --------------------------------------------------------------------------
 * CoreUI Boostrap Admin Template (v3.2.0): main.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

/* eslint-disable no-magic-numbers */
// Disable the on-canvas tooltip
Chart.defaults.global.pointHitDetectionRadius = 1;
Chart.defaults.global.tooltips.enabled = false;
Chart.defaults.global.tooltips.mode = 'index';
Chart.defaults.global.tooltips.position = 'nearest';
Chart.defaults.global.tooltips.custom = coreui.ChartJS.customTooltips;
Chart.defaults.global.defaultFontColor = '#646470';
Chart.defaults.global.responsiveAnimationDuration = 1;
document.body.addEventListener('classtoggle', function (event) {
  if (event.detail.className === 'c-dark-theme') {
    if (document.body.classList.contains('c-dark-theme')) {
      cardChart1.data.datasets[0].pointBackgroundColor = coreui.Utils.getStyle('--primary-dark-theme');
      cardChart2.data.datasets[0].pointBackgroundColor = coreui.Utils.getStyle('--info-dark-theme');
      Chart.defaults.global.defaultFontColor = '#fff';
    } else {
      cardChart1.data.datasets[0].pointBackgroundColor = coreui.Utils.getStyle('--primary');
      cardChart2.data.datasets[0].pointBackgroundColor = coreui.Utils.getStyle('--info');
      Chart.defaults.global.defaultFontColor = '#646470';
    }

    cardChart1.update();
    cardChart2.update();
    mainChart.update();
  }
}); // eslint-disable-next-line no-unused-vars

var janeiro = document.getElementById("card-chart1").getAttribute("totaljaneiro");
var fevereiro = document.getElementById("card-chart1").getAttribute("totalfevereiro");
var marco = document.getElementById("card-chart1").getAttribute("totalmarco");
var abril = document.getElementById("card-chart1").getAttribute("totalabril");
var maio = document.getElementById("card-chart1").getAttribute("totalmaio");
var junho = document.getElementById("card-chart1").getAttribute("totaljunho");
var julho = document.getElementById("card-chart1").getAttribute("totaljulho");
var agosto = document.getElementById("card-chart1").getAttribute("totalagosto");
var setembro = document.getElementById("card-chart1").getAttribute("totalsetembro");
var outubro = document.getElementById("card-chart1").getAttribute("totaloutubro");
var novembro = document.getElementById("card-chart1").getAttribute("totalnovembro");
var dezembro = document.getElementById("card-chart1").getAttribute("totaldezembro");
var cardChart1 = new Chart(document.getElementById('card-chart1'), {
  type: 'line',
  data: {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Agosto', 'Setembro', 'Outubro', 'Novembro'],
    datasets: [{
      label: 'Dados totais',
      backgroundColor: 'transparent',
      borderColor: 'rgba(255,255,255,.55)',
      pointBackgroundColor: coreui.Utils.getStyle('--primary'),
      data: [janeiro, fevereiro, marco, abril, maio, junho, julho, agosto, setembro, outubro, novembro, dezembro]
    }]
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          color: 'transparent',
          zeroLineColor: 'transparent'
        },
        ticks: {
          fontSize: 2,
          fontColor: 'transparent'
        }
      }],
      yAxes: [{
        display: false,
        ticks: {
          display: false,
          min: 0,
          max: 400
        }
      }]
    },
    elements: {
      line: {
        borderWidth: 1
      },
      point: {
        radius: 4,
        hitRadius: 10,
        hoverRadius: 4
      }
    }
  }
}); // eslint-disable-next-line no-unused-vars

var janeirov = document.getElementById("card-chart2").getAttribute("totaljaneirov");
var fevereirov = document.getElementById("card-chart2").getAttribute("totalfevereirov");
var marcov = document.getElementById("card-chart2").getAttribute("totalmarcov");
var abrilv = document.getElementById("card-chart2").getAttribute("totalabrilv");
var maiov = document.getElementById("card-chart2").getAttribute("totalmaiov");
var junhov = document.getElementById("card-chart2").getAttribute("totaljunhov");
var julhov = document.getElementById("card-chart2").getAttribute("totaljulhov");
var agostov = document.getElementById("card-chart2").getAttribute("totalagostov");
var setembrov = document.getElementById("card-chart2").getAttribute("totalsetembrov");
var outubrov = document.getElementById("card-chart2").getAttribute("totaloutubrov");
var novembrov = document.getElementById("card-chart2").getAttribute("totalnovembrov");
var dezembrov = document.getElementById("card-chart2").getAttribute("totaldezembrov");

var cardChart2 = new Chart(document.getElementById('card-chart2'), {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Agosto', 'Setembro', 'Outubro', 'Novembro'],
    datasets: [{
      label: 'Dados de vendas',
      backgroundColor: 'transparent',
      borderColor: 'rgba(255,255,255,.55)',
      pointBackgroundColor: coreui.Utils.getStyle('--info'),
      data: [janeirov, fevereirov, marcov, abrilv, maiov, junhov, julhov, agostov, setembrov, outubrov, novembrov, dezembrov]
    }]
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          color: 'transparent',
          zeroLineColor: 'transparent'
        },
        ticks: {
          fontSize: 2,
          fontColor: 'transparent'
        }
      }],
      yAxes: [{
        display: false,
        ticks: {
          display: false,
          min: 0,
          max: 400
        }
      }]
    },
    elements: {
      line: {
        tension: 0.00001,
        borderWidth: 1
      },
      point: {
        radius: 4,
        hitRadius: 10,
        hoverRadius: 4
      }
    }
  }
}); // eslint-disable-next-line no-unused-vars


var janeironv = document.getElementById("card-chart3").getAttribute("totaljaneironv");
var fevereironv = document.getElementById("card-chart3").getAttribute("totalfevereironv");
var marconv = document.getElementById("card-chart3").getAttribute("totalmarconv");
var abrilnv = document.getElementById("card-chart3").getAttribute("totalabrilnv");
var maionv = document.getElementById("card-chart3").getAttribute("totalmaionv");
var junhonv = document.getElementById("card-chart3").getAttribute("totaljunhonv");
var julhonv = document.getElementById("card-chart3").getAttribute("totaljulhonv");
var agostonv = document.getElementById("card-chart3").getAttribute("totalagostonv");
var setembronv = document.getElementById("card-chart3").getAttribute("totalsetembronv");
var outubronv = document.getElementById("card-chart3").getAttribute("totaloutubronv");
var novembronv = document.getElementById("card-chart3").getAttribute("totalnovembronv");
var dezembronv = document.getElementById("card-chart3").getAttribute("totaldezembronv");

var cardChart3 = new Chart(document.getElementById('card-chart3'), {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Agosto', 'Setembro', 'Outubro', 'Novembro'],
    datasets: [{
      label: 'Dados de não venda',
      backgroundColor: 'transparent',
      borderColor: 'rgba(255,255,255,.55)',
      pointBackgroundColor: coreui.Utils.getStyle('--info'),
      data: [janeironv, fevereironv, marconv, abrilnv, maionv, junhonv, julhonv, agostonv, setembronv, outubronv, novembronv, dezembronv]
    }]
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          color: 'transparent',
          zeroLineColor: 'transparent'
        },
        ticks: {
          fontSize: 2,
          fontColor: 'transparent'
        }
      }],
      yAxes: [{
        display: false,
        ticks: {
          display: false,
          min: 0,
          max: 400
        }
      }]
    },
    elements: {
      line: {
        tension: 0.00001,
        borderWidth: 1
      },
      point: {
        radius: 4,
        hitRadius: 10,
        hoverRadius: 4
      }
    }
  }
}); // eslint-disable-next-line no-unused-vars



var mainChart = new Chart(document.getElementById('main-chart'), {
  type: 'line',
  data: {
    labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S', 'M', 'T', 'W', 'T', 'F', 'S', 'S', 'M', 'T', 'W', 'T', 'F', 'S', 'S', 'M', 'T', 'W', 'T', 'F', 'S', 'S'],
    datasets: [{
      label: 'My First dataset',
      backgroundColor: coreui.Utils.hexToRgba(coreui.Utils.getStyle('--info'), 10),
      borderColor: coreui.Utils.getStyle('--info'),
      pointHoverBackgroundColor: '#fff',
      borderWidth: 2,
      data: [165, 180, 70, 69, 77, 57, 125, 165, 172, 91, 173, 138, 155, 89, 50, 161, 65, 163, 160, 103, 114, 185, 125, 196, 183, 64, 137, 95, 112, 175]
    }, {
      label: 'My Second dataset',
      backgroundColor: 'transparent',
      borderColor: coreui.Utils.getStyle('--success'),
      pointHoverBackgroundColor: '#fff',
      borderWidth: 2,
      data: [92, 97, 80, 100, 86, 97, 83, 98, 87, 98, 93, 83, 87, 98, 96, 84, 91, 97, 88, 86, 94, 86, 95, 91, 98, 91, 92, 80, 83, 82]
    }, {
      label: 'My Third dataset',
      backgroundColor: 'transparent',
      borderColor: coreui.Utils.getStyle('--danger'),
      pointHoverBackgroundColor: '#fff',
      borderWidth: 1,
      borderDash: [8, 5],
      data: [65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65]
    }]
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          drawOnChartArea: false
        }
      }],
      yAxes: [{
        ticks: {
          beginAtZero: true,
          maxTicksLimit: 5,
          stepSize: Math.ceil(250 / 5),
          max: 250
        }
      }]
    },
    elements: {
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
        hoverBorderWidth: 3
      }
    }
  }
});
//# sourceMappingURL=main.js.map