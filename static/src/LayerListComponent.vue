<template>
  <ul v-bind:style="'padding:' + verticalPadding.toString() + 'px 0;z-index:' + z.toString()" v-bind:id="componentID" v-bind:class="draggingClass">
    <li v-for="(l, i) in layers" :key="i" v-bind:layer-index="i" v-bind:style="getLayerStyle(i)">
      <div v-bind:class="'layer-list-dragger ' + draggerclass" style="float:left;" v-bind:layer-index="i" v-on:mousedown="onDraggerDown" v-on:mouseup="onDraggerUp" v-on:mousemove="onDraggerMove"><div class="layer-list-release-listener" style="position:fixed; "></div></div>
      <div>
        <slot v-bind:name="'slot' + i.toString()"></slot>
      </div>
    </li>
  </ul>
</template>
<script>
import {EventBus} from './EventBus'
export default {
  data () {
    return {
      dragging: false,
      draggingIndex: -1,
      draggedLayerPosition: 0,
      draggingClass: 'layer-list-component',
      componentID: 'layerList' + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join(''),
      verticalPadding: 18,
      selectedLayerHeight: 0,
      sortedLayer: -1
    }
  },
  props: ['layers', 'z', 'draggerclass'],
  methods: {
    onDraggerDown: function (e) {
      var self = this
      e.currentTarget.getElementsByTagName('div')[0].style.display = 'block'
      self.$data.draggingIndex = Number(e.currentTarget.getAttribute('layer-index'))
      self.$data.draggedLayerPosition = this.filteredEventCoords(e, {x: 0, y: document.getElementById(self.$data.componentID).scrollTop - document.getElementsByTagName('html')[0].scrollTop}).y
      self.$data.dragging = true
      self.$data.selectedLayerHeight = document.getElementById(self.$data.componentID).children[self.$data.draggingIndex].getBoundingClientRect().height
      this.onDraggerMove(e)
    },
    onDraggerUp: function (e) {
      var self = this
      if (self.$data.dragging) {
        var sortingInfo = this.getSortingInfo()
        if (sortingInfo.layers.length === this.layers.length) {
          EventBus.$emit('layer-reposition-event', sortingInfo.layers)
        }
      }
      e.currentTarget.getElementsByTagName('div')[0].style.display = 'none'
      self.$data.dragging = false
      self.$data.layerPositionAttribute = 'relative'
      self.$data.draggingIndex = -1
      self.$data.draggingClass = 'layer-list-component'
      self.$data.selectedLayerHeight = 0
    },
    onDraggerMove: function (e) {
      var self = this
      if (self.$data.dragging) {
        self.$data.layerPositionAttribute = 'absolute'
        self.$data.draggedLayerPosition = this.filteredEventCoords(e, {x: 0, y: document.getElementById(self.$data.componentID).scrollTop - document.getElementsByTagName('html')[0].scrollTop}).y
        self.$data.draggingClass = 'layer-list-component is-dragging'
        var sortingInfo = this.getSortingInfo()
        self.$data.sortedLayer = sortingInfo.end ? -2 : sortingInfo.index
      }
    },
    getSortingInfo: function () {
      var self = this
      var addIndex = -1
      var addToEnd = false
      for (var j = 0; j < document.getElementById(self.$data.componentID).children.length; j++) {
        if (j !== self.$data.draggingIndex) {
          var beforeY = j > 0 ? document.getElementById(self.$data.componentID).children[j - 1].getBoundingClientRect().top : -900000
          var currentY = document.getElementById(self.$data.componentID).children[j].getBoundingClientRect().top
          var lastY = document.getElementById(self.$data.componentID).children[document.getElementById(self.$data.componentID).children.length - 1].getBoundingClientRect().top
          var draggedY = document.getElementById(self.$data.componentID).children[self.$data.draggingIndex].getBoundingClientRect().top
          if (draggedY > beforeY && draggedY <= currentY) {
            addIndex = j
            j = document.getElementById(self.$data.componentID).children.length
          } else if (draggedY > lastY) {
            addToEnd = true
            j = document.getElementById(self.$data.componentID).children.length
          }
        }
      }
      var layersCopy = []
      for (var i = 0; i < this.layers.length; i++) {
        if (i === addIndex) {
          layersCopy.push(this.layers[self.$data.draggingIndex])
        }
        if (i !== self.$data.draggingIndex) {
          layersCopy.push(this.layers[i])
        }
      }
      if (addToEnd) {
        layersCopy.push(this.layers[self.$data.draggingIndex])
      }
      return {layers: layersCopy, index: addIndex, end: addToEnd}
    },
    getLayerStyle: function (i) {
      var self = this
      var positioning = i === self.$data.draggingIndex ? 'position:absolute;z-index:' + (this.z + 100).toString() + ';top:' + self.$data.draggedLayerPosition.toString() + 'px;' : 'position:relative;'
      var topMargin = ''
      console.log('sorted = ' + self.$data.sortedLayer.toString())
      console.log('dragged = ' + self.$data.draggingIndex.toString())
      console.log(self.$data.sortedLaye === self.$data.draggingIndex + 1)
      if (i === self.$data.sortedLayer || (i === self.$data.draggingIndex + 1 && self.$data.sortedLayer === -1)) {
        topMargin = 'margin-top:' + self.$data.selectedLayerHeight + 'px;'
      } else {
        topMargin = ''
      }
      return 'display:block; margin:0; padding:4px 0; clear:both;' + positioning + topMargin
    },
    filteredEventCoords: function (e, offset) {
      return {x: e.pageX - offset.x, y: e.pageY + offset.y}
    }
  }
}
</script>
<style lang="scss">
div.layer-list-release-listener{
  position:fixed;
  left:0;
  top:0;
  bottom:0;
  right: 0;
  background-color: rgba(0,0,0,.1);
  display:none;
}
ul.layer-list-component{
  width:200px; 
  display: block; 
  height: 100%;
  margin:0;
}
ul.layer-list-component.is-dragging{
  user-select: none;
  -moz-user-select: none;
  -khtml-user-select: none;
  -webkit-user-select: none;
  -o-user-select: none;
}
</style>


