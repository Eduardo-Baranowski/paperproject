/* eslint-disable object-curly-newline */

/* global Chart */

/**
 * --------------------------------------------------------------------------
 * CoreUI Boostrap Admin Template (v3.2.0): main.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

/* eslint-disable no-magic-numbers */
// random Numbers
var random = function random() {
  return Math.round(Math.random() * 100);
}; // eslint-disable-next-line no-unused-vars



var janeiro = document.getElementById("canvas-2").getAttribute("data-janeiro");
var fevereiro = document.getElementById("canvas-2").getAttribute("data-fevereiro");
var marco = document.getElementById("canvas-2").getAttribute("data-marco");
var abril = document.getElementById("canvas-2").getAttribute("data-abril");
var maio = document.getElementById("canvas-2").getAttribute("data-maio");
var junho = document.getElementById("canvas-2").getAttribute("data-junho");
var julho = document.getElementById("canvas-2").getAttribute("data-julho");
var agosto = document.getElementById("canvas-2").getAttribute("data-agosto");
var setembro = document.getElementById("canvas-2").getAttribute("data-setembro");
var outubro = document.getElementById("canvas-2").getAttribute("data-outubro");
var novembro = document.getElementById("canvas-2").getAttribute("data-novembro");
var dezembro = document.getElementById("canvas-2").getAttribute("data-dezembro");


var janeiron = document.getElementById("canvas-2").getAttribute("data-janeiron");
var fevereiron = document.getElementById("canvas-2").getAttribute("data-fevereiron");
var marcon = document.getElementById("canvas-2").getAttribute("data-marcon");
var abriln = document.getElementById("canvas-2").getAttribute("data-abriln");
var maion = document.getElementById("canvas-2").getAttribute("data-maion");
var junhon = document.getElementById("canvas-2").getAttribute("data-junhon");
var julhon = document.getElementById("canvas-2").getAttribute("data-julhon");
var agoston = document.getElementById("canvas-2").getAttribute("data-agoston");
var setembron = document.getElementById("canvas-2").getAttribute("data-setembron");
var outubron = document.getElementById("canvas-2").getAttribute("data-outubron");
var novembron = document.getElementById("canvas-2").getAttribute("data-novembron");
var dezembron = document.getElementById("canvas-2").getAttribute("data-dezembron");

var barChart = new Chart(document.getElementById('canvas-2'), {
  type: 'bar',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    datasets: [{
      backgroundColor: 'rgba(220, 220, 220, 0.5)',
      borderColor: 'rgba(220, 220, 220, 0.8)',
      highlightFill: 'rgba(220, 220, 220, 0.75)',
      highlightStroke: 'rgba(220, 220, 220, 1)',
      data: [janeiron, fevereiron, marcon, abriln, maion, junhon, julhon, agoston, setembron, outubron, novembron, dezembron]
    }, {
      backgroundColor: 'rgba(151, 187, 205, 0.5)',
      borderColor: 'rgba(151, 187, 205, 0.8)',
      highlightFill: 'rgba(151, 187, 205, 0.75)',
      highlightStroke: 'rgba(151, 187, 205, 1)',
      data: [janeiro, fevereiro, marco, abril, maio, junho, julho, agosto, setembro, outubro, novembro, dezembro]
    }]
  },
  options: {
    responsive: true
  }
}); // eslint-disable-next-line no-unused-vars

var total = document.getElementById("canvas-3").getAttribute("data-total");
var totalvenda = document.getElementById("canvas-3").getAttribute("data-venda");
var totalnaovenda = document.getElementById("canvas-3").getAttribute("data-naovenda");
var doughnutChart = new Chart(document.getElementById('canvas-3'), {
  type: 'doughnut',
  data: {
    labels: ['Paper de não venda', 'Paper de venda', 'Total de Papers'],
    datasets: [{
      data: [totalnaovenda, totalvenda, total],
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
    }]
  },
  options: {
    responsive: true
  }
}); // eslint-disable-next-line no-unused-vars

var papersvendedormes = document.getElementById("canvas-4").getAttribute("papersvendedormes");
var papersvendedormesv = document.getElementById("canvas-4").getAttribute("papersvendedormesv");
var papersvendedormesnv = document.getElementById("canvas-4").getAttribute("papersvendedormesnv");
var radarChart = new Chart(document.getElementById('canvas-4'), {
  type: 'pie',
  data: {
    labels: ['Papers de Não Venda', 'Papers de Venda', 'Total de Papers no mês'],
    datasets: [{
      data: [papersvendedormesnv, papersvendedormesv, papersvendedormes],
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
    }]
  },
  options: {
    responsive: true
  }
}); // eslint-disable-next-line no-unused-vars

var papersvendedor = document.getElementById("canvas-5").getAttribute("papersvendedor");
var papersvendedorv = document.getElementById("canvas-5").getAttribute("papersvendedorv");
var papersvendedornv = document.getElementById("canvas-5").getAttribute("papersvendedornv");
var pieChart = new Chart(document.getElementById('canvas-5'), {
  type: 'pie',
  data: {
    labels: ['Papers de Não Venda', 'Papers de Venda', 'Total de Papers'],
    datasets: [{
      data: [papersvendedornv, papersvendedorv, papersvendedor],
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
    }]
  },
  options: {
    responsive: true
  }
}); // eslint-disable-next-line no-unused-vars

var polarAreaChart = new Chart(document.getElementById('canvas-6'), {
  type: 'polarArea',
  data: {
    labels: ['Red', 'Green', 'Yellow', 'Grey', 'Blue'],
    datasets: [{
      data: [11, 16, 7, 3, 14],
      backgroundColor: ['#FF6384', '#4BC0C0', '#FFCE56', '#E7E9ED', '#36A2EB']
    }]
  },
  options: {
    responsive: true
  }
});
//# sourceMappingURL=charts.js.map

var total = document.getElementById("canvas-7").getAttribute("papersvendedor");
var totalvenda = document.getElementById("canvas-7").getAttribute("papersvendedorv");
var totalnaovenda = document.getElementById("canvas-7").getAttribute("papersvendedornv");
var doughnutChart = new Chart(document.getElementById('canvas-7'), {
  type: 'doughnut',
  data: {
    labels: ['Paper de não venda', 'Paper de venda', 'Total de Papers'],
    datasets: [{
      data: [totalnaovenda, totalvenda, total],
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
    }]
  },
  options: {
    responsive: true
  }
}); // eslint-disable-next-line no-unused-vars
