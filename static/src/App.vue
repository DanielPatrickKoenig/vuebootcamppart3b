<template>
  <div id="app">
    <layerlist v-if="!editingDisabled" :layers="elements" :z="handleZindexes.active + 100" draggerclass="layer-panel-drag-icon">
      <div v-for="(e, i) in elements" :key="'layer' + i.toString()" v-bind:slot="'slot' + i.toString()" v-bind:class="selectedElementIndex === i ? 'layer-list-slot layer-list-slot-selected' : 'layer-list-slot'">
        <label v-text="e.title"></label>
        <button v-on:click="onDeleteElement(i)" class="delete-button"></button>
        <ul class="layer-dimensions">
          <li><label>LEFT: </label><input type="number" v-model="e.coords.left" /></li>
          <li><label>TOP: </label><input type="number" v-model="e.coords.top" /></li>
          <li><label>WIDTH: </label><input type="number" v-model="e.size.width" /></li>
          <li><label>HEIGHT: </label><input type="number" v-model="e.size.height" /></li>
          <li><label>TYPE: </label><span v-text="e.tag"></span></li>
          <li><label>TEMPLATE: </label><span v-text="e.template"></span></li>
        </ul>
      </div>
    </layerlist>
    <label class="disable-switch"><input type="checkbox" v-model="editingDisabled" /> Disable Editing</label>
    <div v-if="!editingDisabled" class="add-panel">
      <select v-model="selectedDataPoint">
        <option value="-1">Please Select a DataPoint</option>
        <option v-for="(a, i) in availableDatapoints" :key="'datapoint' + i.toString()" v-bind:value="i" v-text="a.name"></option>
      </select>
      <select v-if="selectedDataPoint >= 0 && availableDatapoints[selectedDataPoint].templates != undefined" v-model="availableDatapoints[selectedDataPoint].template">
        <option v-for="(n, i) in availableDatapoints[selectedDataPoint].templates" :key="n.toString() + '_' + i" v-bind:value="n" v-text="n"></option>
      </select>
      <button v-if="selectedDataPoint >= 0" v-on:click="addElement(availableDatapoints[selectedDataPoint])">Add Element</button>
    </div>
    <draggableItem v-for="(e, i) in elements" :key="'item' + i.toString()" :coords="e.coords" :size="e.size" :dragid="i" :activez="handleZindexes.active" :inactivez="handleZindexes.inactive" :disabled="editingDisabled" border="#cccccc">
      <imagecom v-if="e.tag == elementTypes.IMAGE" :src="e.src" slot="content"></imagecom>
      <iframecom v-if="e.tag == elementTypes.IFRAME" :src="e.src" slot="content"></iframecom>
      <piechart v-if="e.tag == elementTypes.CHART && e.template == chartTypes.PIE" slot="content" :chartdata="dataset[e.data]" :colors="colors" :sig="e.size" textcolor="#000000" :title="e.title"></piechart>
      <bargroupchart v-if="e.tag == elementTypes.CHART && e.template == chartTypes.BARGROUP" slot="content" :chartdata="dataset[e.data]" :colors="colors" :sig="e.size" textcolor="#000000" :title="e.title"></bargroupchart>
      <barchart v-if="e.tag == elementTypes.CHART && e.template == chartTypes.BAR" slot="content" :chartdata="dataset[e.data]" :color="colors[0]" :sig="e.size" textcolor="#000000" :title="e.title"></barchart>
      <guagechart v-if="e.tag == elementTypes.CHART && e.template == chartTypes.GUAGE" slot="content" :chartdata="dataset[e.data]" :colors="colors" :sig="e.size" textcolor="#000000" :title="e.title"></guagechart>
      <checkall v-if="e.tag == elementTypes.UI && e.template == uiTypes.CHECK_ALL" slot="content" :choices="e.data.content" :context="e.data.context"></checkall>
    </draggableItem>
    <draggableItem v-for="(h, i) in handles" :key="'handle' + i.toString()" :coords="h.coords" :size="handleSize" :dragid="h.id" :activez="handleZindexes.active" :inactivez="handleZindexes.inactive" :disabled="editingDisabled" bg="#cccccc"></draggableItem>
  </div>
</template>

<script>
import {EventBus} from './EventBus.js'
import DraggableItem from './DraggableItem.vue'
import Image from './ImageComponent.vue'
import Iframe from './IframeComponent.vue'
import PieChart from './PieChartComponent.vue'
import BarGroupChart from './BarGroupChartComponent.vue'
import BarChart from './BarChartComponent.vue'
import GuageChart from './GuageChartComponent.vue'
import CheckOne from './CheckOneComponent.vue'
import CheckAll from './CheckAllComponent.vue'
import LayerList from './LayerListComponent.vue'
import axios from 'axios'
export default {
  name: 'app',
  components: {
    draggableItem: DraggableItem,
    imagecom: Image,
    iframecom: Iframe,
    piechart: PieChart,
    bargroupchart: BarGroupChart,
    barchart: BarChart,
    guagechart: GuageChart,
    checkone: CheckOne,
    checkall: CheckAll,
    layerlist: LayerList
  },
  data () {
    return {
      handleZindexes: {active: 2000, inactive: 5},
      handles: [],
      handleSize: {width: 10, height: 10},
      elementDefaults: {width: 300, height: 300},
      selectedDataPoint: -1,
      elementTypes: {
        IMAGE: 'Image',
        IFRAME: 'iFrame',
        CHART: 'Chart',
        UI: 'UI'
      },
      chartTypes: {
        PIE: 'pie',
        BAR: 'bar',
        BARGROUP: 'bargroup',
        LINE: 'line',
        GUAGE: 'guage'
      },
      uiTypes: {
        CHECK_ONE: 'checkone',
        CHECK_ALL: 'checkall',
        SELECT: 'select'
      },
      selectedChartType: undefined,
      availableDatapoints: [
        {name: 'Video 1', src: 'https://www.youtube.com/embed/KvAk9718Jo8', type: 'iFrame'},
        {name: 'Image 1', src: 'https://upload.wikimedia.org/wikipedia/commons/b/bf/Bucephala-albeola-010.jpg', type: 'Image'}
      ],
      elements: [],
      c: -1,
      colors: ['#00aeef', '#fdc689', '#7cc576', '#f26d7d', '#a186be', '#ec008c', '#c69c6d', '#ed145b', '#f26522', '#acd373', '#aba000', '#f5989d'],
      dataset: {},
      editingDisabled: false,
      updateParams: {splitter: ':::'},
      selectedElementIndex: -1
    }
  },
  methods: {
    getHandleIndex: function (id) {
      var self = this
      var index = -1
      for (var i = 0; i < self.$data.handles.length; i++) {
        if (self.$data.handles[i].id === id) {
          index = i
        }
      }
      return index
    },
    addElement: function (data) {
      var self = this
      switch (data.type) {
        case self.$data.elementTypes.IMAGE:
        case self.$data.elementTypes.IFRAME:
        {
          self.$data.elements.push(
            {
              coords:
              {
                left: 10,
                top: 10
              },
              size:
              {
                width: self.$data.elementDefaults.width,
                height: self.$data.elementDefaults.height
              },
              tag: data.type,
              src: data.src
            }
          )
          break
        }
        case self.$data.elementTypes.CHART:
        case self.$data.elementTypes.UI:
        {
          self.$data.elements.push(
            {
              coords:
              {
                left: 10,
                top: 10
              },
              size:
              {
                width: self.$data.elementDefaults.width,
                height: self.$data.elementDefaults.height
              },
              tag: data.type,
              template: data.template,
              data: data.data,
              title: data.name
            }
          )
          break
        }
      }
    },
    renderHandles: function () {
      var self = this
      self.$data.handles = []
      self.$data.handles.push({
        coords: {
          left: self.$data.elements[self.$data.selectedElementIndex].coords.left - (self.$data.handleSize.width / 2),
          top: self.$data.elements[self.$data.selectedElementIndex].coords.top - (self.$data.handleSize.height / 2)
        },
        id: 'handle_topleft'
      })
      self.$data.handles.push({
        coords: {
          left: self.$data.elements[self.$data.selectedElementIndex].coords.left - (self.$data.handleSize.width / 2) + self.$data.elements[self.$data.selectedElementIndex].size.width,
          top: self.$data.elements[self.$data.selectedElementIndex].coords.top - (self.$data.handleSize.height / 2)
        },
        id: 'handle_topright'
      })
      self.$data.handles.push({
        coords: {
          left: self.$data.elements[self.$data.selectedElementIndex].coords.left - (self.$data.handleSize.width / 2) + self.$data.elements[self.$data.selectedElementIndex].size.width,
          top: self.$data.elements[self.$data.selectedElementIndex].coords.top - (self.$data.handleSize.height / 2) + self.$data.elements[self.$data.selectedElementIndex].size.height
        },
        id: 'handle_bottomright'
      })
      self.$data.handles.push({
        coords: {
          left: self.$data.elements[self.$data.selectedElementIndex].coords.left - (self.$data.handleSize.width / 2),
          top: self.$data.elements[self.$data.selectedElementIndex].coords.top - (self.$data.handleSize.height / 2) + self.$data.elements[self.$data.selectedElementIndex].size.height
        },
        id: 'handle_bottomleft'
      })
    },
    updateDataPoints: function (p) {
      var self = this
      axios.get('/update', {params: p}).then(response => {
        var dta = JSON.parse(response.data)
        self.$data.dataset = dta
        self.$data.availableDatapoints = dta.datapoints
      })
    },
    onDeleteElement: function (index) {
      var self = this
      self.$data.elements.splice(index, 1)
    },
    deselect: function () {
      self.$data.selectedElementIndex = -1
    }
  },
  created () {
    var self = this
    EventBus.$on('draggable-element-down', function (val) {
      if (val.dragid.toString().split('_')[0] !== 'handle') {
        self.$data.selectedElementIndex = val.dragid
        self.renderHandles()
      }
    })
    EventBus.$on('draggable-element-up', function (val) {
    })
    EventBus.$on('draggable-element-move', function (val) {
      if (val.dragid.toString().split('_')[0] === 'handle') {
        var handleIndex = self.getHandleIndex(val.dragid)
        self.$data.handles[handleIndex].coords = val.position
        switch (handleIndex) {
          case 0: {
            self.$data.handles[1].coords = {left: self.$data.handles[1].coords.left, top: val.position.top}
            self.$data.handles[3].coords = {left: val.position.left, top: self.$data.handles[3].coords.top}
            self.$data.handles[2].coords = {left: self.$data.handles[1].coords.left, top: self.$data.handles[3].coords.top}
            break
          }
          case 1: {
            self.$data.handles[0].coords = {left: self.$data.handles[0].coords.left, top: val.position.top}
            self.$data.handles[2].coords = {left: val.position.left, top: self.$data.handles[2].coords.top}
            self.$data.handles[3].coords = {left: self.$data.handles[0].coords.left, top: self.$data.handles[2].coords.top}
            break
          }
          case 2: {
            self.$data.handles[1].coords = {left: val.position.left, top: self.$data.handles[1].coords.top}
            self.$data.handles[3].coords = {left: self.$data.handles[3].coords.left, top: val.position.top}
            self.$data.handles[0].coords = {left: self.$data.handles[3].coords.left, top: self.$data.handles[1].coords.top}
            break
          }
          case 3: {
            self.$data.handles[0].coords = {left: val.position.left, top: self.$data.handles[0].coords.top}
            self.$data.handles[2].coords = {left: self.$data.handles[2].coords.left, top: val.position.top}
            self.$data.handles[1].coords = {left: self.$data.handles[2].coords.left, top: self.$data.handles[0].coords.top}
            break
          }
        }
        if (self.$data.selectedElementIndex >= 0) {
          self.$data.elements[self.$data.selectedElementIndex].coords = {left: self.$data.handles[0].coords.left + (self.$data.handleSize.width / 2), top: self.$data.handles[0].coords.top + (self.$data.handleSize.height / 2)}
          self.$data.elements[self.$data.selectedElementIndex].size = {width: self.$data.handles[1].coords.left - self.$data.handles[0].coords.left, height: self.$data.handles[3].coords.top - self.$data.handles[0].coords.top}
        }
      } else if (self.$data.selectedElementIndex >= 0) {
        self.$data.elements[self.$data.selectedElementIndex].coords = val.position
        self.$data.handles[0].coords = {left: self.$data.elements[self.$data.selectedElementIndex].coords.left - (self.$data.handleSize.width / 2), top: self.$data.elements[self.$data.selectedElementIndex].coords.top - (self.$data.handleSize.height / 2)}
        self.$data.handles[1].coords = {left: self.$data.handles[0].coords.left + self.$data.elements[self.$data.selectedElementIndex].size.width, top: self.$data.handles[0].coords.top}
        self.$data.handles[2].coords = {left: self.$data.handles[1].coords.left, top: self.$data.handles[0].coords.top + self.$data.elements[self.$data.selectedElementIndex].size.height}
        self.$data.handles[3].coords = {left: self.$data.handles[0].coords.left, top: self.$data.handles[2].coords.top}
      }
    })
    EventBus.$on('check-all-option-checked', (n) => {
      var self = this
      var context = n.context
      var choices = n.choices
      var contextParamList = []
      for (var c in choices) {
        if (choices[c].selected) {
          contextParamList.push(choices[c].text)
        }
      }
      if (contextParamList.length > 0) {
        self.$data.updateParams[context] = contextParamList.join(self.$data.updateParams.splitter)
      } else {
        var upCopy = {}
        for (var u in self.$data.updateParams) {
          if (u !== context) {
            upCopy[u] = self.$data.updateParams[u]
          }
        }
        self.$data.updateParams = upCopy
      }
      this.updateDataPoints(self.$data.updateParams)
    })
    EventBus.$on('layer-reposition-event', n => {
      console.log(n)
      var self = this
      self.$data.elements = n
      self.$data.selectedElementIndex = -1
    })
    this.updateDataPoints(self.$data.updateParams)
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.resizable-chart,
.resizable-chart > div:first-child,
.resizable-chart > div:first-child > div:first-child{
  width: 100%;
  height: 100%; 
}
ul.check-all{
  overflow-x: hidden;
  overflow-y: auto;
  width:100%;
  height: 100%;
  margin:0;
  padding:0;
  > li{
    display: block;
    clear: both;
    width: 100%;
    text-align: left;    
    label{
      width:100%;
      text-align: left;
    }
  }
}
ul.layer-list-component{
  background-color: rgba(0,0,0,.7);
  position: fixed;
  right: 0;
  top:0;
  bottom: 0;
  overflow-x: hidden;
  overflow-y: auto;
  > li{
    padding: 4px !important;
    box-shadow: 0 2px 0 #999999 inset;
    background-color: rgba(255,255,255,.7);
  }
}
div.layer-list-slot{
  
  > button.delete-button{
    float: right;
    background-color: transparent;
    border:none;
    cursor: pointer;
    color:#ffffff;
    border-radius: 30px;
    background-color: rgba(255,0,0,.4);
    padding: 1px 3px 2px 3px;
  }
  button.delete-button:hover{
    background-color: rgba(255,0,0,.8);
  }
  > button.delete-button::after{
    content:'\2297';
    
    
  }
  > label{
    float:left;
    font-weight:bold;
    padding-bottom:10px;
  }
  > ul.layer-dimensions{
    display: block;
    margin:0;
    padding: 0;
    width:100%;
    > li{
      display: block;
      margin:0;
      padding: 2px 0;
      clear:both;
      font-size: 11px;
      box-shadow: 0 1px 0 rgba(0,0,0,.2) inset;
      > label{
        width: 40%;
        padding: 0 0 0 2px;
        margin:0;
        float:left;
        text-align:left;
      }
      > input[type='number']{
        width: 40%;
        margin:0 0 0 2px;
        float:right;
        background: transparent;
        border: none;
      }
      > span{
        width:40px;
        display: inline-block;
        text-align:left;
      }
    }
  }
}
div.layer-list-slot-selected{
  background-color: #ffffff;
  box-shadow: 0 0 0 3px #ffffff;
}
.layer-panel-drag-icon{
  padding:0 8px 0 0;
  font-weight: bold;
  cursor: pointer;
  color: #999999;
  
}
.layer-panel-drag-icon:hover{
  color: #333333;
}
.layer-panel-drag-icon::before{
  content:'\2191';
}
.layer-panel-drag-icon::after{
  content:'\2193';
}

.add-panel{
  position: fixed;
  bottom: 0;
  padding: 12px;
  left: 0;
  right: 200px;
  text-align: left;
  background-color: rgba(0,0,0,.5);
  > button{
    float:right;
  }
}
.disable-switch{
  position: fixed;
  left:0;
  top:0;
  padding:10px;
}
</style>
