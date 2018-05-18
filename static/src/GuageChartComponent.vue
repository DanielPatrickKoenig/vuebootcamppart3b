<template>
  <div class="guage-chart resizable-chart">
    <div v-bind:id="chartid"></div>
  </div>
</template>
<script>
import echarts from 'echarts'
export default {
  data () {
    return {
      chartid: 'CHART_' + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join(''),
      chartObject: undefined
    }
  },
  props: ['chartdata', 'colors', 'textcolor', 'title', 'sig'],
  watch: {
    chartdata: function () {
      var self = this
      if (document.getElementById(self.$data.chartid) !== undefined) {
        this.renderChart()
      }
    },
    sig: function () {
      var self = this
      self.$data.chartObject.resize()
    }
  },
  mounted: function () {
    var self = this
    self.$data.chartObject = echarts.init(document.getElementById(self.$data.chartid))
    this.renderChart()
  },
  methods: {
    renderChart: function () {
      var self = this
      var option = {
        title: {
          text: this.title,
          textStyle: {
            color: this.textcolor
          },
          x: 'center',
          y: 'bottom'
        },
        tooltip: {
          formatter: '{a} <br/>{c}%'
        },
        series: [
          {
            name: this.title,
            type: 'gauge',
            detail: {formatter: '{value}%'},
            data: [{value: Math.round((this.chartdata.value / this.chartdata.total) * 100), name: this.title}],
            axisLine: {
              show: true,
              lineStyle: {
                color: [
                  [0.33, this.colors[0]],
                  [0.66, this.colors[1]],
                  [1, this.colors[2]]
                ],
                width: 30
              }
            }
          }
        ]
      }
      self.$data.chartObject.setOption(option)
    }
  }
}
</script>

