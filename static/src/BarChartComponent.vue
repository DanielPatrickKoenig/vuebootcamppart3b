<template>
  <div class="bar-chart resizable-chart">
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
    props: ['chartdata', 'color', 'textcolor', 'title', 'sig'],
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
        var _data = []
        var _values = []
        var _keys = []
        for (var k in this.chartdata) {
          _keys.push(k)
          _values.push(this.chartdata[k][0])
          _data.push({name: k, value: this.chartdata[k]})
        }
        var option = {
          title: {
            text: this.title,
            textStyle: {
              color: this.textcolor
            }
          },
          textStyle: {
            color: this.textcolor
          },
          color: this.color,
          yAxis: {
            type: 'category',
            data: _keys
          },
          xAxis: {
            type: 'value'
          },
          series: [{
            data: _values,
            type: 'bar'
          }]
        }
        self.$data.chartObject.setOption(option)
      }
    }
  }
</script>
